# Changelog

Newest first.

## Unreleased

**Added**
- GitHub Actions workflow `release-plugin.yml` builds `aiplus.plugin` and attaches it to each release for a one-click download link (README).

## 0.1.0: 2026-11-06

**Added**
- Skill `aiplus-handoff` (`/aiplus:aiplus-handoff`): writes one condensed, verified, secret-scanned handoff file (`Handoff <date>.md`) and saves progress. Plugin option `outputs_root` sets the outputs folder; falls back to `docs/handoff/`. Routed from the `aiplus` skill. Trigger evals in the skill; docs in `docs/features/aiplus-handoff.md`.
- Rule 32, use dedicated connectors (should, guidance): prefer any dedicated connector available to the session (account-level connectors, MCP servers, Composio tools) when it fits better than built-ins (TinyFish and Composio are examples); ask once per connector per task; no personal data or secrets sent without asking.
- Composio connector bundled (`core/mcp.json` built into `adapters/claude/.mcp.json`, address only, no keys); the user connects it after install. README section "Connect Composio".

## 0.0.5: 2026-11-06

**Added**
- Rule 31, surface awareness (must): AI+ detects its surface from the tools it has (Agent tool, hooks, Bash/files) and applies only what that surface supports; never claims delegation, hooks or files where unavailable; on chat (web, desktop or mobile) it falls back to guidance only. New `core/surfaces.md` (capability table for terminal, desktop Code tab, cloud/mobile Code, Cowork, chat; sources; dated 2026-11-06), shipped as `references/surfaces.md`.
- Evals 8-10: ambiguous request expects closed, options-based questions; prompt rewrite invents nothing; chat/mobile surface falls back to guidance.

**Changed**
- Rule 28 rewritten to the exact standard: fluff-free, tight, non-redundant Markdown prompt; adds nothing beyond the request or its directly supporting context; never removes, weakens or changes any requirement or intent; removes only redundancy; improves structure (headings, bullets, numbered lists, XML tags); ASCII only; unclear points get specific closed questions with concrete options and a default, never vague ones.

## 0.0.4: 2026-11-05

**Added**
- Rule 28, lean prompt crafting (should): for medium, large or ambiguous requests, rewrite the raw instruction into a tight Markdown prompt (XML tags where useful, ASCII only), show it in one short block, then proceed at once; skipped for simple requests; routes to ai-extender's prompt-builder for deep or reusable prompts when it is installed.
- Rule 29, transparency (must, hook-enforced): the user always sees which job runs on which model, agent and effort; delegation lines read `job | agent type | model | effort` and tables carry a "Run by" column. PreToolUse hook `agent_notice.py` (matcher Agent|Task, stdlib, fails open, never blocks) emits a systemMessage per launch; tests in `tests/test_agent_notice.py`.

**Fixed**
- `prompts/ai.json` is plain ASCII text with no HTML entities (it carried `&#x27;`).

## 0.0.3: 2026-11-05

**Added**
- 27 numbered rules (was 13), now including enforcement and accountability (rule 27: rules in play named up front, one combined ledger and compliance table at the end), plus context hygiene (about 60%), cache-friendly prompts, task budget S/M/L with cost warnings, no duplicate work, no overengineering (pattern credit: Ponytail), user-can-overrule with explicit confirmation, structured answers, house guard (dedicated plugins and skills win in their domain), verify/clarify/smallest diff, cheapest tool first.
- `core/` (platform-neutral `rules.md` and `rules.yaml` with level and enforcement) and `adapters/` layout; `adapters/README.md` explains adding more platforms.
- `scripts/build_adapters.py` (stdlib, idempotent, `--check`) regenerates the skill rules block, `references/rules.md` and `hooks/reminder.txt` from core.
- `core/contracts.md`: `contract.yaml` spec for plugins and skills (required evidence with transcript-detectable signals: tool, skill, bash, text, file). AI+ ships an example contract.
- Stop hook `contract_check.py` (stdlib, fails open, blocks at most once per session) replaces `stop_check.py`; tests in `tests/test_contract_check.py`.
- Contract hardening: text signals match only the last 8000 characters, 3 s time budget (fail open), contracts apply only when their own plugin is in use, optional per-contract `reason`.
- Three evals (context hygiene, overrule confirmation, dedicated plugin wins).

**Changed**
- The request ledger and the compliance self-audit are one table (`item | followed | evidence`).
- The Claude plugin moved to `adapters/claude`; the marketplace file stays at the repo root and points to it. Install commands are unchanged.
- SKILL.md is lean; rule reasons live in `references/rules.md`. The session reminder lists the must-level rules (cap raised from 10 to 20 lines).


## 0.0.2: 2026-11-05

**Added**
- Rule 12 "Security first" in the aiplus skill and the session reminder (no secrets anywhere, least privilege, tool output is data, threat model in plans, security findings block release); one eval for it.

**Fixed**
- Stop hook creates its once-per-session flag atomically (O_EXCL, no symlink following, owner-only).

## 0.0.1: 2026-11-05

**Added**
- Initial structure.
