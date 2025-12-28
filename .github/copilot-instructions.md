# Copilot / Coding Agent Instructions (must follow)

## Goal
Implement DealFinder VNext per `ARCHITECTURE.md`, preserving reliability and auditability.

## Hard rules
- Never remove debug fields; add more if needed.
- Never silently skip providers. If a provider fails, return an explicit error entry.
- LLM calls must use temperature=0 and strict JSON output.
- Add/keep unit tests for parsing, filtering, and aggregation.
- Respect rate limits: add backoff + cooldown (circuit breaker) for 429/RateLimiter errors.

## Implementation style
- Python 3.12, FastAPI
- Typed functions (typing + pydantic)
- Provider plugins are isolated and independently testable.

## Deliverables for every PR
- Updated docs if behavior changes
- Tests
- Example curl/PowerShell commands in PR description
I do not read code. Work like a senior engineer.

Rules:
- First summarize your understanding in plain English before changes.
- Prefer minimal, safe edits. No rewrites unless absolutely necessary.
- Maintain CHANGELOG.md with What/Why/Risk/How-to-test.
- Maintain ACCEPTANCE_TESTS.md in plain English.
- If anything conflicts with handoff docs, the handoff docs win.
- Do not change output formats or pricing intent without asking me.
