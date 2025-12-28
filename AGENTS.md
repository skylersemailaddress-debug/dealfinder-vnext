# Agent Playbook (human + coding agent)

## When to use a coding agent
- Creating providers
- Refactoring to plugin architecture
- Adding tests and CI
- Wiring endpoints and config

## When to ask ChatGPT (this assistant)
- Architecture decisions & tradeoffs
- Debugging a failing provider
- Prompt/JSON schema design for LLM judge
- Aggregation math & confidence scoring

## Definition of Done
- /api/pricing/suggest returns:
  - suggested_price, range_low/high, confidence
  - sources[] with evidence links
  - debug[] with provider status
- Works for at least 5 different categories in tests/examples
