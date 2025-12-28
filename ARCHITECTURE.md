# Architecture

## High-level flow
1) **Input**
   - text query and/or images
   - optional: condition, locale, shipping preference, target marketplace, category hint

2) **Identity & normalization**
   - Extract entities: brand, model, UPC/EAN/ISBN, storage/size, generation, year
   - If image provided: barcode → OCR → labels → visual embedding neighbors
   - Output: a canonical `ItemIdentity` (structured)

3) **Source plan**
   - Choose provider set by category + identity confidence
   - Always include **eBay live** (your preference) and (when allowed) eBay sold.
   - Add category-specific marketplaces (examples below) + retail anchors (optional)

4) **Gather**
   - Run providers concurrently with per-provider budgets (timeouts, pagination caps)
   - Each provider returns: `PriceObs[]` + `ProviderDebug`

5) **Clean & match**
   - Stage A: deterministic rules (currency, obvious parts/broken)
   - Stage B: similarity (title tokens + embeddings)
   - Stage C: LLM judge (OpenAI) *only on the borderline set* and always returning strict JSON

6) **Aggregate**
   - Robust stats: median, trimmed mean, IQR filtering, recency weighting
   - Output: `suggested_price`, `confidence`, `range_low/high`, explanation + evidence list
   - Record source contribution (how many obs kept from each provider)

## Providers (recommended)
**Core marketplaces**
- eBay Browse (live) — primary
- eBay Sold (Finding or other approved sold endpoint) — secondary (with cooldown)
- Facebook Marketplace (if accessible via compliant method) / OfferUp (where available) — optional
- Craigslist — optional

**Category-specific resale**
- Electronics: Swappa (phones), BackMarket (retail-ish used), Gazelle (buyback)
- Sneakers/streetwear: StockX, GOAT
- Apparel: Grailed, Poshmark, Depop
- Collectibles: TCGplayer, PriceCharting, Discogs (music), Comic price sources
- Instruments: Reverb
- Cameras: MPB/KEH (buyback + listing)
- Tools: eBay + (optional) Home Depot/Lowes for anchors
- Books: ISBN sources (Google Books) + AbeBooks (marketplace)

**Retail anchors (optional)**
- Google CSE “retail anchor” (structured price extraction)
- Walmart API, BestBuy API, Target (affiliate APIs), etc
- Keepa for Amazon price history (requires paid key) for stable anchors

## Vision (hybrid)
Use a **hybrid** pipeline:
1) Barcode decode (ZXing / pyzbar)
2) OCR + label detection (Google Cloud Vision)
3) Visual embedding similarity (CLIP / OpenAI embeddings)
4) LLM vision verification (OpenAI vision model) to confirm “same model vs variant vs part”

## Data model
- `PriceObs`: provider, title, url, item_price, shipping, all_in, condition_id, timestamp, meta
- `ItemIdentity`: canonical brand/model, identifiers, category, confidence, extracted attributes
- `ProviderDebug`: request params, counts, exclusions, errors, elapsed_ms

## Non-negotiable engineering rules
- Every provider must be:
  - idempotent, cached, and rate-limited
  - safe to fail (errors are returned but do not kill overall request)
  - measurable (timings + counts)

- Determinism:
  - For the same inputs and same underlying marketplace data, result should be stable.
  - LLM used for classification must be temperature=0 and strict JSON.

See `RULES.md` for more.
