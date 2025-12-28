# DealFinder VNext — Build Handoff Pack

This folder is **the spec + skeleton** for the “locked‑in” next version:
- Multi-source pricing (all sources contribute; none are silently skipped without a recorded reason)
- eBay-first + broad category coverage
- Hybrid vision (barcode/OCR + visual similarity + LLM validation)
- Deterministic aggregation + OpenAI-assisted *filtering / normalization / reasoning* (not “guessing”)

## What to do with this pack
1) Put this folder in a GitHub repo.
2) Use a coding agent (recommended: **GitHub Copilot coding agent**) to implement issues from `WORKPLAN.md`.
3) Keep this pack up to date as “source of truth” docs as the agent builds.

## Quick start (local dev)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

Open: http://127.0.0.1:8010/docs

## Key principles (non-negotiable)
- **Always return a result**: if some sources fail, still compute using what succeeded.
- **Every provider returns**: `observations[]`, `debug`, and `errors[]` with explicit cause.
- **No brittle matching**: use multi-stage matching (heuristics → embeddings/vision → LLM judge).
- **Auditability**: keep evidence links + reason codes for exclusions.
- **Category-agnostic**: classify item/category early and route to the right provider set.

See `ARCHITECTURE.md` for the full design.
