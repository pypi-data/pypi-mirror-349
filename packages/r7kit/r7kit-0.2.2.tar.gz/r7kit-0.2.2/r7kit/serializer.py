# === ПУТЬ К ФАЙЛУ: r7kit/serializer.py ===
from __future__ import annotations
import gzip
import logging
from typing import Any, Final
import orjson

log = logging.getLogger(__name__)

_GZIP_THRESHOLD: Final[int] = 32 * 1024  # 32 KiB


def dumps(obj: Any) -> str:
    """
    • если obj — str, возвращаем его как есть (чтобы не плодить кавычки)
    • иначе сериализуем через orjson; если >32 KiB — gzip+base64 с префиксом 'gzip:'
    """
    if isinstance(obj, str):
        return obj

    raw = orjson.dumps(
        obj,
        option=orjson.OPT_SERIALIZE_DATACLASS
        | orjson.OPT_NAIVE_UTC
        | orjson.OPT_NON_STR_KEYS,
    )
    if len(raw) <= _GZIP_THRESHOLD:
        return raw.decode()

    import base64

    packed = base64.b64encode(gzip.compress(raw)).decode()
    return f"gzip:{packed}"


def loads(txt: str) -> Any:
    """
    • если txt выглядит как JSON (startswith '{' или '[') — orjson.loads
    • если txt.startswith('gzip:') — base64→gzip→orjson.loads
    • иначе возвращаем исходную строку
    """
    if not isinstance(txt, str):
        return txt
    try:
        if txt and txt[0] in "{[":
            return orjson.loads(txt)
        if txt.startswith("gzip:"):
            import base64
            raw = gzip.decompress(base64.b64decode(txt[5:]))
            return orjson.loads(raw)
    except Exception as exc:
        log.debug("serializer: cannot decode %r: %s", txt[:50], exc)
    return txt
