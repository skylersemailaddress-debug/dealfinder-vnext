from fastapi import FastAPI
from app.api.pricing import router as pricing_router

app = FastAPI(title="DealFinder VNext", version="0.1.0")
app.include_router(pricing_router, prefix="/api/pricing", tags=["pricing"])

@app.get("/health")
def health():
    return {"ok": True}
