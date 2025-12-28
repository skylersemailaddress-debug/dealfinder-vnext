import os
from dotenv import load_dotenv

load_dotenv()

def env(key: str, default: str | None = None) -> str | None:
    v = os.getenv(key)
    if v is None or str(v).strip() == "":
        return default
    return str(v).strip()

def env_bool(key: str, default: bool = False) -> bool:
    v = env(key)
    if v is None:
        return default
    return v.lower() in ("1","true","yes","on")

def env_int(key: str, default: int) -> int:
    v = env(key)
    if v is None:
        return default
    try:
        return int(v)
    except Exception:
        return default
