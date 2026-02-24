"""Backend : Pushover — envoie une notification push via l'API Pushover."""

import json
import logging
import urllib.request
import urllib.parse

import os

from backends import register

log = logging.getLogger("sms-gw")

PUSHOVER_TOKEN = os.environ.get("PUSHOVER_TOKEN", "")
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY", "")


@register("pushover")
class PushoverBackend:
    def send(self, msg):
        if not PUSHOVER_TOKEN or not PUSHOVER_USER_KEY:
            raise RuntimeError("PUSHOVER_TOKEN et PUSHOVER_USER_KEY doivent être définis dans .env")

        data = urllib.parse.urlencode({
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": msg["numero"],
            "message": msg["message"],
        }).encode()

        req = urllib.request.Request(
            "https://api.pushover.net/1/messages.json",
            data=data,
            method="POST",
        )

        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            log.info("Pushover OK — status=%s request=%s", body.get("status"), body.get("request"))
