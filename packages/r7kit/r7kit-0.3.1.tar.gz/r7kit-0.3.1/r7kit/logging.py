# === ПУТЬ К ФАЙЛУ: logging.py ===
import logging, os, json, datetime
from logging.config import dictConfig

def _json(record: logging.LogRecord) -> str:
    d = {
        "ts": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        "lvl": record.levelname,
        "logger": record.name,
        "msg": record.getMessage(),
    }
    if record.exc_info:
        d["exc"] = logging.Formatter().formatException(record.exc_info)
    return json.dumps(d, ensure_ascii=False)

def setup(level: str | int | None = None) -> None:
    log_fmt = "json" if os.getenv("R7KIT_LOG_FORMAT") == "json" else "std"
    formatter = {"()": _json} if log_fmt == "json" else {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"std": formatter, "json": formatter} if log_fmt == "json" else {"std": formatter},
        "handlers":   {"console": {"class": "logging.StreamHandler", "formatter": log_fmt}},
        "root":       {"handlers": ["console"], "level": level or os.getenv("R7KIT_LOG_LEVEL", "INFO")},
    })
