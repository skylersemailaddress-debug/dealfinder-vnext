from cachetools import TTLCache
from threading import RLock
from typing import Any

_cache: TTLCache[str, Any] = TTLCache(maxsize=2048, ttl=900)
_lock = RLock()

def get(key):
    with _lock:
        return _cache.get(key)

def set(key, val, ttl: int | None = None):
    # TTLCache uses global ttl; for per-key ttl, store timestamp in value (future enhancement)
    with _lock:
        _cache[key] = val
