# Legacy DealFinder — Reference Extract (READ-ONLY)

## IMPORTANT
This document summarizes useful, battle-tested ideas from an older DealFinder implementation.

Rules:
- This document is NOT source of truth.
- Do NOT copy architecture or structure from the legacy app.
- vNext handoff docs and ARCHITECTURE.md override everything here.
- Extract concepts, heuristics, and edge cases only.
- Explain what you plan to reuse before implementing anything.

---

## What the old DealFinder did well (high value)

### 1. Real-world pricing heuristics
- Used retail anchors (Amazon / BestBuy / Walmart) when available.
- Fell back to secondary markets (eBay sold comps) when retail was missing.
- Applied category-based resale bands:
  - Electronics: ~40–70% of retail
  - Appliances / heavy items: ~30–50%
  - Small consumer goods: ~50–90%
- Penalized:
  - missing accessories
  - cosmetic damage
  - heavy / local-pickup-only items
- Never listed “for parts / repair” items.

---

### 2. Marketplace CSV expectations (Facebook Marketplace focus)
The old system exported CSVs intended for bulk upload with:
- Stable column order
- Explicit fields for:
  - title
  - description
  - price
  - condition
  - category
  - quantity
  - location
  - shipping/local flags
- Descriptions often included:
  - condition summary
  - what’s included
  - simple bullet-style formatting

Column naming and ordering mattered more than internal data structures.

---

### 3. Data cleaning & normalization lessons
- Titles often needed aggressive cleanup:
  - remove “NEW!!!”, emojis, seller fluff
  - normalize model numbers
- Condition normalization was essential:
  - “Used – Good”, “Good”, “Gently Used” → GOOD
  - Anything ambiguous defaulted conservative
- Duplicate price observations were common and needed deduplication.
- Outliers were frequent; median or trimmed mean worked better than averages.

---

### 4. Error reality (why auditability matters)
The old app frequently encountered:
- Partial provider failures
- API timeouts
- Rate limiting
- Inconsistent data formats

When errors were hidden, pricing decisions became impossible to explain.

vNext should ALWAYS:
- surface provider failures explicitly
- explain exclusions
- show how the final price was computed

---

### 5. Explainability expectations (from real use)
Users trusted pricing more when they could see:
- how many sources were used
- which prices were ignored and why
- what rule caused the final number

Even simple text explanations increased confidence.

---

## What to ignore from the old app
- Folder structure
- Concurrency model
- Ad-hoc scripts
- Env handling
- Caching hacks
- Any undocumented logic

Those were experimental and should NOT be reused.

---

## How this reference should be used
Before implementing any feature inspired by this document:
1. Summarize what you plan to reuse (in plain English).
2. Explain how it fits within vNext ARCHITECTURE.md.
3. Implement minimally with tests and acceptance criteria.

If there is conflict:
- vNext architecture wins.
- Determinism, auditability, and tests win.

End of reference.
