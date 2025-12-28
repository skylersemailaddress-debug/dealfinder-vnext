# Work Plan (issue-ready)

## Milestone 0 — Repo hygiene
- [ ] Add CI: lint + unit tests + type checks
- [ ] Add `.github/copilot-instructions.md` + `AGENTS.md` (agent rules)
- [ ] Add secrets + `.env.example` + docs

## Milestone 1 — Core API
- [ ] `/api/pricing/suggest` accepts (query, condition, images?)
- [ ] Provider interface + parallel execution + caching
- [ ] Deterministic aggregation + debug payload

## Milestone 2 — eBay-first
- [ ] eBay Browse (live) provider with OAuth auto-mint + pagination + shipping
- [ ] eBay Sold provider with cooldown + rate limiter
- [ ] Title heuristics + parts/broken filters

## Milestone 3 — OpenAI judge
- [ ] Strict JSON judge helper (response_format JSON schema)
- [ ] Apply judge only to ambiguous candidates
- [ ] Log judge decisions for audit

## Milestone 4 — Retail anchors
- [ ] Google CSE multi-query anchor extraction
- [ ] Add optional Keepa / Walmart / BestBuy providers (stubs first, then real)

## Milestone 5 — Hybrid vision
- [ ] Image upload endpoint
- [ ] Barcode decode
- [ ] Google Vision OCR/labels
- [ ] Visual embeddings + nearest-neighbor match
- [ ] LLM vision verify (optional)

## Milestone 6 — Category expansion
- [ ] Category classifier routes to provider sets
- [ ] Add 2 category-specific providers as templates (e.g., StockX, Reverb)
