# gateway_app/utils/logger.py

import logging
import sys
import socket
import inspect
from datetime import datetime
from django.conf import settings
from src.utils.kibana_log import send_log_to_kibana
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# === SENTRY SETUP ===
if getattr(settings, "ENVIRONMENT", "local") != "local":
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[sentry_logging],
        send_default_pii=True
    )

# === LOGGER SETUP ===
logger = logging.getLogger("gateway_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s | %(extra)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# === LOGGING HELPERS ===

def log_info(func_name, msg="", request=None, extra=None):
    caller = _get_caller()
    metadata = _build_context(request, extra)
    metadata["caller"] = caller

    logger.info(f"[{func_name}] {msg} -- {caller}", extra={"extra": metadata})
    send_log_to_kibana("INFO", msg, metadata)


def log_error(func_name, error=None, request=None, extra=None):
    caller = _get_caller()
    metadata = _build_context(request, extra)
    metadata["caller"] = caller

    logger.error(f"[{func_name}] {str(error)} -- {caller}", extra={"extra": metadata})
    send_log_to_kibana("ERROR", str(error), metadata)


def _build_context(request=None, extra=None):
    context = {
        "host": socket.gethostname(),
        "env": getattr(settings, "ENVIRONMENT", "local"),
        "timestamp": datetime.utcnow().isoformat()
    }

    if request:
        context.update({
            "ip": request.META.get("REMOTE_ADDR", ""),
            "token": request.headers.get("Authorization") or request.headers.get("TOKEN"),
            "user_agent": request.headers.get("User-Agent", ""),
            "uri": request.get_full_path(),
            "method": request.method
        })

    if extra and isinstance(extra, dict):
        context.update(extra)

    return context


def _get_caller():
    frame = inspect.stack()[2]
    filename = frame.filename.split("/")[-1]
    lineno = frame.lineno
    return f"{filename}:{lineno}"
