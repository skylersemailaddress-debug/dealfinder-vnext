from __future__ import annotations
import os, time, json
import requests
from base64 import b64encode

from app.core.config import env, env_int
from app.models import PriceObs, ProviderResult
from app.providers.base import Provider

_TOKEN = None
_TOKEN_EXP = 0.0

def _mint_token() -> tuple[str | None, str | None]:
    global _TOKEN, _TOKEN_EXP
    cid = env("EBAY_CLIENT_ID")
    csec = env("EBAY_CLIENT_SECRET")
    if not cid or not csec:
        return None, "missing EBAY_CLIENT_ID/EBAY_CLIENT_SECRET"

    now = time.time()
    if _TOKEN and (_TOKEN_EXP - now) > 60:
        return _TOKEN, None

    basic = b64encode(f"{cid}:{csec}".encode("ascii")).decode("ascii")
    headers = {"Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"}
    body = "grant_type=client_credentials&scope=" + requests.utils.quote("https://api.ebay.com/oauth/api_scope", safe="")
    r = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=body, timeout=25)
    if r.status_code >= 400:
        return None, f"token mint failed HTTP {r.status_code}: {r.text[:200]}"
    j = r.json()
    tok = (j.get("access_token") or "").strip()
    exp = int(j.get("expires_in") or 0)
    if not tok or exp <= 0:
        return None, "token mint returned empty access_token"
    _TOKEN = tok
    _TOKEN_EXP = now + exp
    return tok, None

class EbayLiveProvider(Provider):
    name = "ebay_live"

    def fetch(self, query: str, *, limit: int = 40, include_shipping: bool = True, **kwargs) -> ProviderResult:
        tok, err = _mint_token()
        if err or not tok:
            return ProviderResult(provider=self.name, ok=False, error=err or "missing token", observations=[], debug={})

        url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        flt = "buyingOptions:{AUCTION|FIXED_PRICE},conditionIds:{3000|4000|5000}"
        headers = {
            "Authorization": f"Bearer {tok}",
            "Accept": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US"),
        }

        max_scan = env_int("PRICING_EBAY_LIVE_MAX_SCAN", 250)
        page_size = 50
        max_pages = max(1, (max_scan + page_size - 1) // page_size)

        obs: list[PriceObs] = []
        scanned = 0

        for page in range(max_pages):
            params = {"q": query, "limit": str(page_size), "offset": str(page*page_size), "filter": flt}
            r = requests.get(url, headers=headers, params=params, timeout=25)
            if r.status_code == 401:
                # force refresh once
                global _TOKEN, _TOKEN_EXP
                _TOKEN, _TOKEN_EXP = None, 0.0
                tok2, err2 = _mint_token()
                if not tok2:
                    return ProviderResult(provider=self.name, ok=False, error=err2 or "401", observations=[], debug={})
                headers["Authorization"] = f"Bearer {tok2}"
                r = requests.get(url, headers=headers, params=params, timeout=25)

            if r.status_code >= 400:
                return ProviderResult(provider=self.name, ok=False, error=f"HTTP {r.status_code}: {r.text[:200]}", observations=[], debug={"params": params})

            data = r.json()
            items = (data or {}).get("itemSummaries") or []
            if not items:
                break

            for it in items:
                scanned += 1
                if scanned > max_scan:
                    break
                try:
                    title = (it.get("title") or "").strip()
                    price_obj = (it.get("price") or {}) or (it.get("currentBidPrice") or {})
                    val = float(price_obj.get("value") or 0)
                    cur = (price_obj.get("currency") or "USD").upper()
                    if val <= 0 or cur != "USD":
                        continue

                    ship = 0.0
                    shipping_opts = it.get("shippingOptions") or []
                    if isinstance(shipping_opts, list):
                        for opt in shipping_opts:
                            sc = (opt or {}).get("shippingCost") or {}
                            try:
                                if (sc.get("currency") or "USD").upper() == "USD":
                                    ship = max(ship, float(sc.get("value") or 0.0))
                            except Exception:
                                pass

                    all_in = val + (ship if include_shipping else 0.0)
                    link = (it.get("itemWebUrl") or it.get("itemHref") or "").strip()

                    obs.append(PriceObs(
                        provider=self.name,
                        title=title,
                        url=link,
                        item_price=val,
                        shipping=ship,
                        all_in=all_in,
                        condition_id=int(it.get("conditionId")) if it.get("conditionId") else None,
                        meta={"itemId": it.get("itemId")}
                    ))
                    if len(obs) >= max(1, min(limit, 50)):
                        break
                except Exception:
                    continue

            if scanned > max_scan or len(obs) >= max(1, min(limit, 50)):
                break

        return ProviderResult(provider=self.name, ok=True, observations=obs, error=None, debug={"scanned": scanned})
