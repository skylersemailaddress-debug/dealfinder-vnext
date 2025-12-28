from __future__ import annotations
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.core.config import env_bool, env_int
from app.core.cache import get as cache_get, set as cache_set
from app.models import PriceObs, ProviderResult
from app.providers.ebay_live import EbayLiveProvider
from app.providers.google_anchor import GoogleAnchorProvider

# Provider registry (expand via plugins later)
PROVIDERS = [
    EbayLiveProvider(),
    GoogleAnchorProvider(),
]

def _aggregate(observations: list[PriceObs]) -> tuple[float | None, float | None, float | None, float | None]:
    if not observations:
        return None, None, None, None
    xs = sorted([o.all_in for o in observations if o.all_in and o.all_in > 0])
    if not xs:
        return None, None, None, None
    n = len(xs)
    med = xs[n//2] if n % 2 == 1 else (xs[n//2-1] + xs[n//2]) / 2.0
    # naive range: 25th–75th percentile-ish
    lo = xs[max(0, int(0.25*(n-1)))]
    hi = xs[min(n-1, int(0.75*(n-1)))]
    # confidence: increases with n; decreases with dispersion
    spread = hi - lo
    conf = min(1.0, (n / 15.0)) * (1.0 if med <= 0 else max(0.1, 1.0 - (spread / max(med, 1e-6))))
    return float(med), float(lo), float(hi), float(conf)

def suggest_price(payload: dict) -> dict:
    q = (payload.get("query") or "").strip()
    if not q:
        return {"ok": False, "error": "missing query", "sources": [], "debug": []}

    include_shipping = payload.get("include_shipping")
    if include_shipping is None:
        include_shipping = env_bool("PRICING_INCLUDE_SHIPPING", True)

    cache_key = f"suggest::{q}::{include_shipping}"
    ttl = env_int("PRICING_CACHE_TTL_SEC", 900)
    hit = cache_get(cache_key)
    if hit is not None:
        return hit

    debug = []
    all_obs: list[PriceObs] = []
    sources = []

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=min(8, len(PROVIDERS))) as ex:
        futs = {ex.submit(p.fetch, q, limit=40, include_shipping=include_shipping): p for p in PROVIDERS}
        for fut in as_completed(futs):
            prov = futs[fut]
            try:
                res: ProviderResult = fut.result()
            except Exception as e:
                res = ProviderResult(provider=prov.name, ok=False, error=str(e), observations=[], debug={})

            debug.append({"provider": res.provider, "ok": res.ok, "count": len(res.observations), "error": res.error})
            for o in res.observations:
                all_obs.append(o)
                sources.append(o.model_dump())

    suggested, lo, hi, conf = _aggregate(all_obs)
    out = {
        "ok": True,
        "suggested_price": suggested,
        "range_low": lo,
        "range_high": hi,
        "confidence": conf,
        "sources": sources,
        "debug": debug + [{"provider": "__agg__", "elapsed_ms": int((time.time()-t0)*1000), "n_obs": len(all_obs)}],
    }
    cache_set(cache_key, out)
    return out
