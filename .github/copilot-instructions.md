# Copilot / Coding Agent Instructions (must follow)

## Source of truth
Implement DealFinder VNext per ARCHITECTURE.md and related handoff docs. If anything conflicts, the handoff docs win.

## Goal
Reliability + auditability: every decision should be explainable and testable.

## Hard rules
- Never silently skip providers. Every provider must produce a result entry with:
  - status: "ok" | "error"
  - error_type (if error)
  - message (if error)
  - retryable: true|false (if error)
- Never remove debug fields. Add more if needed, but:
  - Put debug under a single `debug` object
  - Never include secrets
  - Truncate long debug strings to a safe limit
- Any LLM calls must use temperature=0 and strict JSON schema output.
- Add/keep unit tests for parsing, filtering, and aggregation logic.
- Respect rate limits: implement exponential backoff + cooldown/circuit breaker on 429/RateLimit errors.

## Implementation style
- Python 3.12 (keep README/CI consistent with this)
- FastAPI
- Typed functions (typing + pydantic)
- Provider plugins are isolated, independently testable, and mockable.

## Deliverables for every PR
- Plain-English summary of changes (What/Why/Risk)
- Updated docs if behavior changes
- Tests added/updated
- Example curl + PowerShell commands in PR description
- Update CHANGELOG.md (What/Why/Risk/How-to-test)
- Update ACCEPTANCE_TESTS.md (plain English)

## Working agreement
I do not read code. Work like a senior engineer:
- Summarize understanding before changes
- Prefer minimal safe edits; no rewrites unless explicitly approved
- Do not change output formats or pricing intent without asking
