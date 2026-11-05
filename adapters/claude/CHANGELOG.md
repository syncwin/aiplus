# Changelog

Newest first.

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
