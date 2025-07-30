# === r7kit/serializer.py ===
from __future__ import annotations
import gzip
import logging
from typing import Any, Final

import orjson

log = logging.getLogger(__name__)

_GZIP_THRESHOLD: Final[int] = 32 * 1024  # 32 KiB — начинаем сжимать


def _to_bytes(obj: Any) -> bytes:
    """
    Кодируем объект в bytes через orjson.
    Любые не-JSON-типы (dataclass, datetime…) сериализуются опциями.
    """
    return orjson.dumps(
        obj,
        option=orjson.OPT_SERIALIZE_DATACLASS
        | orjson.OPT_NAIVE_UTC
        | orjson.OPT_NON_STR_KEYS,
    )


# ─────────────────────  public API  ──────────────────────────
def dumps(obj: Any) -> str:
    """
    Возвращает **строку** JSON.

    • если итоговый JSON > _GZIP_THRESHOLD → сжимаем GZip и
      возвращаем base64-строку со схемой `gzip:<b64>`

    • обычные строки НЕ оборачиваем в JSON, т.к. они уже пригодны
      для хранения — это избавляет Redis от лишних кавычек.
    """
    if isinstance(obj, str):
        return obj

    raw = _to_bytes(obj)
    if len(raw) <= _GZIP_THRESHOLD:
        return raw.decode()

    import base64  # локальный import → быстрее импорт r7kit

    packed = base64.b64encode(gzip.compress(raw)).decode()
    return f"gzip:{packed}"


def loads(txt: str) -> Any:
    """
    Обратная операция:  
      • пытаемся распарсить JSON;  
      • если строка начинается с `gzip:` — декодируем/распаковываем;  
      • при ошибке парсинга возвращаем исходную строку.
    """
    if not isinstance(txt, str):
        return txt

    try:
        if txt.startswith("{") or txt.startswith("["):
            return orjson.loads(txt)

        if txt.startswith("gzip:"):
            import base64, bz2  # noqa: PLC0414 – возможно пригодится и bz2
            raw = gzip.decompress(base64.b64decode(txt[5:]))
            return orjson.loads(raw)

    except Exception as exc:  # noqa: BLE001
        log.debug("serializer: cannot decode value (%s)", exc)

    # plain string / нераспарсилось
    return txt
