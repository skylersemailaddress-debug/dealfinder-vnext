# Rules & Quality Bar

## Reliability
- Hard timeouts per provider (default 25s)
- Global request budget (default 40s)
- Circuit breakers for rate-limited providers (cooldown with explicit reason)
- Retries: only for transient failures (401 token, 429, network), max 1-2

## Accuracy
- Keep evidence links for every kept observation
- Drop reasons must be explicit and countable
- Prefer *sold* data for “resale value”, but fall back to *live* when sold is unavailable.

## Aggregation
- Always compute:
  - median all-in (primary)
  - trimmed mean (secondary)
  - confidence score based on n, dispersion, and source diversity
- Output:
  - suggested_price
  - range_low/high
  - confidence (0-1)
  - explanation string
  - per-source contribution

## Category coverage
- If item category is unknown:
  - use eBay live + Google retail anchor + a small set of general sources
  - run vision if images exist
  - attempt to classify (electronics/apparel/media/tools/collectibles/etc.)

## OpenAI usage
OpenAI is used for:
- parsing/normalizing identities from messy text
- strict JSON listing classification (“same exact item?”)
- summarizing evidence into explanation

OpenAI is *not* used to invent prices.
