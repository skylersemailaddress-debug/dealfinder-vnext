from __future__ import annotations
import requests
from app.core.config import env
from app.models import PriceObs, ProviderResult
from app.providers.base import Provider

import re
_PRICE_RE = re.compile(r"\$\s?([0-9]+(?:\.[0-9]{2})?)")

class GoogleAnchorProvider(Provider):
    name = "google"

    def fetch(self, query: str, *, limit: int = 8, include_shipping: bool = True, **kwargs) -> ProviderResult:
        key = env("GOOGLE_CSE_KEY", env("GOOGLE_API_KEY"))
        cx  = env("GOOGLE_CSE_CX", env("GOOGLE_CSE_ID"))
        if not key or not cx:
            return ProviderResult(provider=self.name, ok=False, error="missing GOOGLE_CSE_KEY/GOOGLE_CSE_CX", observations=[], debug={})

        url = "https://www.googleapis.com/customsearch/v1"
        qlist = [query, f"{query} retail price", f"{query} MSRP", f"buy {query} price"]
        obs: list[PriceObs] = []
        seen = set()

        for q in qlist:
            r = requests.get(url, params={"key": key, "cx": cx, "q": q, "num": str(min(max(limit,1),10)), "gl":"us", "hl":"en"}, timeout=25)
            if r.status_code >= 400:
                continue
            data = r.json()
            items = (data or {}).get("items") or []
            for it in items:
                title = (it.get("title") or "").strip()
                link = (it.get("link") or "").strip()
                snippet = (it.get("snippet") or "") + " " + (it.get("htmlSnippet") or "")
                m = _PRICE_RE.search(snippet)
                if not m:
                    continue
                price = float(m.group(1))
                k = (link, price)
                if k in seen:
                    continue
                seen.add(k)
                obs.append(PriceObs(provider=self.name, title=title, url=link, item_price=price, shipping=0.0, all_in=price, meta={"q": q}))
                if len(obs) >= max(1, min(limit, 10)):
                    break
            if len(obs) >= 5:
                break

        return ProviderResult(provider=self.name, ok=True, observations=obs, error=None, debug={"n": len(obs)})
