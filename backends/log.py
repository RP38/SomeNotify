"""Backend : log (pour tester, écrit juste dans la console)."""

import logging

from backends import register

log = logging.getLogger("sms-gw")


@register("log")
class LogBackend:
    def send(self, msg):
        log.info(
            "LOG BACKEND — de=%s numero=%s message=%s",
            msg["email"], msg["numero"], msg["message"],
        )
