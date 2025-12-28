from pydantic import BaseModel
from typing import Any

class PriceObs(BaseModel):
    provider: str
    title: str
    url: str
    item_price: float
    shipping: float = 0.0
    all_in: float
    condition_id: int | None = None
    meta: dict[str, Any] = {}

class ProviderResult(BaseModel):
    provider: str
    ok: bool
    observations: list[PriceObs] = []
    error: str | None = None
    debug: dict[str, Any] = {}
