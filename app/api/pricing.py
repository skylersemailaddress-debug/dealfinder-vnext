from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.pricing_service import suggest_price

router = APIRouter()

class SuggestRequest(BaseModel):
    query: str = Field(..., min_length=2)
    condition: str | None = None  # "new", "good", "fair", etc.
    include_shipping: bool | None = None

class SuggestResponse(BaseModel):
    ok: bool
    suggested_price: float | None = None
    range_low: float | None = None
    range_high: float | None = None
    confidence: float | None = None
    sources: list[dict] = []
    debug: list[dict] = []
    error: str | None = None

@router.post("/suggest", response_model=SuggestResponse)
def suggest(req: SuggestRequest):
    return suggest_price(req.model_dump())
