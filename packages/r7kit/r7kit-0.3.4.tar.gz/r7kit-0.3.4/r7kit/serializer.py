# === ПУТЬ К ФАЙЛУ: serializer.py ===
from __future__ import annotations

import base64
import gzip
import logging
from typing import Any, Final

import orjson

log = logging.getLogger(__name__)
_GZIP_LIMIT: Final[int] = 32 * 1024  # 32 KiB

# ───────────────────── API ───────────────────────────────────────────
def dumps(obj: Any) -> str:
    if isinstance(obj, str):
        return obj

    raw = orjson.dumps(
        obj,
        option=(
            orjson.OPT_SERIALIZE_DATACLASS
            | orjson.OPT_NAIVE_UTC
            | orjson.OPT_NON_STR_KEYS
        ),
    )
    if len(raw) < _GZIP_LIMIT:
        return raw.decode()

    return "gzip:" + base64.b64encode(gzip.compress(raw)).decode()


def loads(txt: str) -> Any:
    if not isinstance(txt, str):
        return txt
    try:
        if txt.startswith("gzip:"):
            raw = gzip.decompress(base64.b64decode(txt[5:]))
            return orjson.loads(raw)
        if txt and txt[0] in "{[":
            return orjson.loads(txt)
    except Exception as exc:
        log.debug("serializer: cannot decode %r – %s", txt[:60], exc)
    return txt
