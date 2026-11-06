# aiplus-setup

## Context

A new project without agent instructions, README or changelog makes every AI session start cold and every contributor guess. Users often do not know what a good start contains. This skill gives anyone with AI+ a best-practice start, scaled to the project (smallest set that earns its place).

## Behaviour

- Triggers on `/aiplus:aiplus-setup`, "set up this project", "new repo" (explicit phrases only; not on session start).
- Detects the surface: with files and git it writes them; on chat surfaces it outputs artifacts or paste-ready blocks and recommends Project instructions.
- Asks one batched question round, then creates only missing files and never overwrites (offers a diff).
- Optional extras, each with a one-line reason: reviewer agent, `scripts/check.*`, `.mcp.json` (no keys), CI, license, GitHub repo (private by default, only after an explicit yes).

## How it works

1. Detect surface, stack (manifest files) and existing files.
2. One question round: type, public/private, GitHub, CI, license, extras.
3. Fill templates from `assets/` (AGENTS.md, CLAUDE.md with `@AGENTS.md`, README, CHANGELOG at 0.0.1, feature doc, CI with SHA-pinned actions and `contents: read`, reviewer agent).
4. Scan created files for secrets; report created, skipped and declined.

## UI in text

One question box, then a short list: created / skipped (exists) / declined.

## Limits

- Templates are generic; stack-specific `.gitignore` and check commands are generated per stack.
- CI action SHAs must be looked up at setup time.
- The AI Extender validator warns (X005) that a SKILL.md line reads like an instruction to the model; accepted false positive, since a skill is instructions.
- Chat surfaces cannot write files or run `gh`.

## Sources (read 2026-11-06, treated as data)

- AGENTS.md: https://agents.md (open Markdown format, no required headings; build/test commands, style, security; nearest file wins in monorepos).
- Claude Code memory: https://code.claude.com/docs/en/memory (CLAUDE.md is context, not enforced config; keep it specific and short; AGENTS.md can be imported).
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/ (Unreleased on top, ISO dates, Added/Changed/Deprecated/Removed/Fixed/Security).
- Semantic Versioning: https://semver.org (read earlier knowledge; 0.0.1 start follows Keep a Changelog practice).
- GitHub Actions hardening: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions (pin to full commit SHA from the original repo; read-only GITHUB_TOKEN by default).
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents (`name` and `description` required; `tools` comma-separated or list).
- Claude Code MCP: https://code.claude.com/docs/en/mcp (project `.mcp.json`, `type: http` with `url`; use `${VAR}` for secrets, never literal keys).
- Unverified: stack-specific `.gitignore` contents (generated from the detected stack at setup, check against github.com/github/gitignore), license texts (use choosealicense.com / SPDX), `gh repo create` flags (check `gh repo create --help` before running).

## History

- 2026-11-06: added in 0.2.0.
