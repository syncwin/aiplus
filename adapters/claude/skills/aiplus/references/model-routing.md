# Model routing by role

Pick the cheapest tier that does the job. Tiers, not model names: names change, and any model named here is an example only. If the user runs a router (for example OmniRoute), send cheap and bulk work through it.

| Role | Tier | Example (not fixed) |
|---|---|---|
| Summarise, classify, extract, transcribe, embed, lint, translate, format | Cheapest: local or free model | a small local model via the router |
| Search, reading, surveys, mechanical edits | Cheap | a small hosted model |
| Coding, tests, multi-step execution | Mid-tier | a mid-size hosted model |
| Planning, architecture, review, hard decisions | Lead | the best value-for-cost top model (rule 30) |

- Escalate one tier only after a clear failure, never by default (rule 5: one retry).
- Do one or two tool calls inline instead of delegating (rule 19).
- State the model and effort on every delegation line (rule 29).
