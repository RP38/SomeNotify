"""
Backends de notification.
Chaque backend est un module avec une fonction send(msg).
msg est un dict avec : email, pass, numero, message
"""

import importlib
import logging
import pkgutil

log = logging.getLogger("sms-gw")

# ── Registre des backends ─────────────────────────────────────

_BACKENDS = {}


def register(name):
    """Décorateur pour enregistrer un backend."""
    def wrap(cls):
        _BACKENDS[name] = cls()
        return cls
    return wrap


def get_backend(name):
    if name not in _BACKENDS:
        raise ValueError(f"Backend inconnu: {name} (dispo: {list(_BACKENDS.keys())})")
    return _BACKENDS[name]


# ── Auto-discovery : importe tous les modules frères ──────────

def _auto_discover():
    package_path = __path__
    for _importer, modname, _ispkg in pkgutil.iter_modules(package_path):
        importlib.import_module(f".{modname}", __name__)


_auto_discover()
