# === ПУТЬ К ФАЙЛУ: config.py ===
from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field
import tomllib

_CFG_FILE = Path.home() / ".r7kit.toml"          # optional

def _from_file(key: str, default: str) -> str:
    if not _CFG_FILE.is_file():
        return default
    try:
        data = tomllib.loads(_CFG_FILE.read_text())
        return data.get(key, default)
    except Exception:                            # noqa: BLE001 – конфиг опционален
        return default


class _Settings(BaseModel, frozen=True, extra="ignore"):
    redis_url:        str = Field(default_factory=lambda: _from_file("redis_url",  "redis://localhost:6379"))
    temporal_address: str = Field(default_factory=lambda: _from_file("temporal",   "localhost:7233"))
    stream_default:   str = Field(default_factory=lambda: _from_file("stream",    "task_events"))
    deleted_ttl:      int = Field(default_factory=lambda: int(_from_file("ttl",   "3600")))


@lru_cache()
def cfg() -> _Settings:                      # читается при первом обращении
    return _Settings(
        redis_url        = os.getenv("REDIS_URL")        or _Settings().redis_url,
        temporal_address = os.getenv("TEMPORAL_ADDRESS") or _Settings().temporal_address,
        stream_default   = os.getenv("R7KIT_STREAM")     or _Settings().stream_default,
        deleted_ttl      = int(os.getenv("R7KIT_DELETED_TTL") or _Settings().deleted_ttl),
    )


def configure(**override) -> None:
    """
    Позволяет переопределить значения ДО первого вызова cfg().
    """
    if cfg.cache_info().currsize:
        raise RuntimeError("r7kit уже настроен; configure() нужно вызвать ДО первого импорта")
    env = {
        "redis_url":        "REDIS_URL",
        "temporal_address": "TEMPORAL_ADDRESS",
        "stream_default":   "R7KIT_STREAM",
        "deleted_ttl":      "R7KIT_DELETED_TTL",
    }
    for k, v in override.items():
        if v is not None:
            os.environ[env[k]] = str(v)
