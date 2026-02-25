#!/usr/bin/env python3
"""
Micro SMS gateway — serveur HTTP.
Reçoit :  GET /http.php?email=x&pass=y&numero=z&message=hello
Dispatche le message vers le(s) backend(s) de notification configuré(s).
"""

import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv

_BASE_DIR = Path(__file__).resolve().parent
_ENV_FILE = _BASE_DIR / ".env"

if not _ENV_FILE.exists():
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("sms-gw").warning(
        "Fichier .env introuvable — copiez .env.example vers .env et renseignez vos identifiants."
    )

load_dotenv(_ENV_FILE)

from backends import get_backend

# ── Configuration ─────────────────────────────────────────────
LISTEN_HOST = os.environ.get("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "80"))

# Backend à utiliser : "pushover", "telegram", "ntfy", "log"
BACKEND = os.environ.get("BACKEND", "log")
# ──────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("sms-gw")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        # Extraire les valeurs (premier élément de chaque liste)
        msg = {
            "email":   (params.get("email", [""]))[0],
            "pass":    (params.get("pass", [""]))[0],
            "numero":  (params.get("numero", [""]))[0],
            "message": (params.get("message", [""]))[0],
        }

        log.info("Reçu: numero=%s message=%s", msg["numero"], msg["message"])

        if not msg["message"]:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"missing 'message' parameter")
            return

        try:
            backend = get_backend(BACKEND)
            backend.send(msg)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            log.error("Erreur backend [%s]: %s", BACKEND, e)
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"error: {e}".encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    log.info("Backend: %s", BACKEND)
    server = HTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    log.info("Écoute sur %s:%d", LISTEN_HOST, LISTEN_PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Arrêt.")
        server.server_close()