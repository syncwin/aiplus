---
name: aiplus-setup
description: >
  Use when the user says "/aiplus:aiplus-setup", "set up this project", "new repo", "init this project properly" or "add AGENTS.md". Sets up a project with best-practice agent and repo files: AGENTS.md, CLAUDE.md, README, CHANGELOG, feature docs, .gitignore, optional CI, license, agents, check script, connectors, GitHub repo. Not for handoff files (aiplus-handoff).
license: MIT
---

# AI+ Setup

Anyone gets a sound project start. Smallest set of files that earns its place (rule 11): create nothing speculative.

## 1. Detect

- Surface (rule 16): with files and git (Claude Code CLI, desktop Code tab) the skill writes files. On chat (claude.ai web, desktop chat, mobile) there are no local files, so each file is offered as a downloadable artifact or a paste-ready block, and the AGENTS.md text suits Project instructions.
- Stack: manifest files (`package.json`, `pubspec.yaml`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json`). Existing files: list which of the set below already exist. Git state and remote.

## 2. Ask once

One batched question round, defaults first, skipping anything detectable: project type, public or private, GitHub repo (yes/no), CI (yes/no), license. Also offer the extras below with a one-line reason each, recommended per stack; default no. Permanent names (repo, project) are never chosen here (rule 8): propose options.

## 3. Create only what is missing

Never overwrite. If a file exists, show a diff of the proposed change and ask. Templates: `assets/` (fill the `{{...}}` slots; plain ASCII).

| Item | When it earns its place |
|---|---|
| `AGENTS.md` (`assets/AGENTS.md`) | Always. Short: overview, commands, style, tests, security, what not to touch |
| `README.md` (`assets/README.md`) | Always |
| `CLAUDE.md` (`assets/CLAUDE.md`) | Claude Code use: line 1 `@AGENTS.md`, then Claude-only notes only |
| `CHANGELOG.md` (`assets/CHANGELOG.md`) | Anything versioned or shared: Keep a Changelog, SemVer, start 0.0.1 |
| `docs/features/<feature>.md` (`assets/feature.md`) | Per real feature, not up front: Context, Behaviour, How it works, UI in text, Limits, History |
| `.gitignore` | Always with git; for the detected stack, plus `.env*`, `.claude/settings.local.json`, `.claude/worktrees/` |
| `.github/workflows/ci.yml` (`assets/ci.yml`) | CI yes. Actions pinned to a full commit SHA (look up the current SHA; never invent one), `permissions: contents: read` |
| `LICENSE` | License chosen; holder name from the user, never guessed |
| `.claude/agents/<role>.md` (`assets/agent-reviewer.md`) | Code that others review: one read-only reviewer (Read, Grep, Glob) with a stack lens |
| `scripts/check.*` | A stack with lint and test commands: one script running them, so AGENTS.md says "run scripts/check" |
| `.mcp.json` | Only servers the project needs: context7 for library docs, Composio for apps. Remote URLs only; never keys; the user connects through `/mcp` |
| GitHub repo | Only after an explicit yes: `gh repo create`, private by default, never public unasked; never push to main |

A tiny project (script, notes, one-file tool) gets AGENTS.md + README.md only.

## Research first (rule 17)

Before writing a stack-specific file (`.gitignore`, CI steps, check script, license text), look up current official docs or `gh ... --help`, scoped to what this project needs; mark anything unverified.

## 4. Check

- Search every created file for `github_pat_`, `ghp_`, `sk-`, `Bearer `, `password=`; on a hit stop and tell the user without echoing the value.
- Keep AGENTS.md under about 100 lines; list what was created, skipped (exists) and declined.

## Sources

Research notes and citations: `docs/features/aiplus-setup.md` in the AI+ repo.

## Scratchpad

End with the request ledger (`references/scratchpad.md`).
