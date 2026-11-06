# AI+

Keeps every Claude session efficient: lead model plans and reviews, cheap subagents execute, minimal reads, one retry, routing to your installed plugins.

**Download:** [aiplus.plugin](https://github.com/syncwin/aiplus/releases/latest/download/aiplus.plugin) (always the latest release)

**Version** 0.2.0 - **Author** SyncWin - **License** MIT

## Layout

```
core/                 platform-neutral rules (rules.md, rules.yaml): the single source
adapters/claude/      the Claude plugin (.claude-plugin, skills, hooks, scripts, evals)
adapters/README.md    how to add another platform
tests/                run `python tests/test_contract_check.py`
scripts/build_adapters.py   regenerates adapter files from core
.claude-plugin/marketplace.json   points to adapters/claude
```

`core/contracts.md` specifies `contract.yaml`, the evidence a plugin or skill can require.

Edit rules in `core/`, then run `python scripts/build_adapters.py` (`--check` verifies nothing is stale).

## Skills

| Skill | Role |
|---|---|
| `aiplus` | Router |
| `aiplus-handoff` | One condensed handoff file for a new chat |
| `aiplus-setup` | Best-practice project setup (AGENTS.md, CLAUDE.md, README, CHANGELOG, CI) |

## Connect Composio

AI+ declares one connector, Composio (`https://connect.composio.dev/mcp`), so tasks can reach apps Claude has no connector for. It ships no account and no key. It is optional: every skill works without it.

1. Install AI+ (below).
2. Open Customize > Plugins > AI+ > Connectors and choose Connect on Composio (in Claude Code, run `/mcp` and pick it).
3. Sign in with your own Composio account.

AI+ asks once per connector per task before using it and never sends personal data or secrets without asking. If Composio is already connected at the same address, Claude uses that one.

## Injection guardrail

A PostToolUse hook screens output from MCP tools (connectors such as Composio) with a small local model. Nothing leaves your machine. If output looks like a prompt injection, Claude is warned to treat it as data and ask you first. It is silent when clean, never blocks if Python is missing, and is a screen, not a verdict. Remove the `PostToolUse` entry in `hooks/hooks.json` to turn it off.

## Install

```
/plugin marketplace add syncwin/aiplus
/plugin install aiplus@aiplus
```

Start with `/aiplus`, or let it load when a multi-step task begins. Requires Python 3 (`python3` on PATH) for the hooks and scan; without it the hooks fail without blocking.

## Credits

Rule 20 (no overengineering) draws its generic ideas (build only what is asked, prefer built-in and existing tools, never trim security, validation or accessibility) from the MIT-licensed Ponytail skill. No text or code is copied.

## Companion prompt

`prompts/ai.json` is a ready-made form for Prompt Builder. It is delivered next to the package, never inside it. Import it there, fill in the fields, and send it to Claude to start this plugin without typing the request from scratch.

## What it runs, reads, and sends

- `adapters/claude/scripts/scan.py`: reads `~/.claude/plugins/installed_plugins.json` and skill folders (local, read-only) and prints a table. No network.
- `adapters/claude/scripts/reminder.py` (SessionStart): prints `hooks/reminder.txt`.
- `adapters/claude/scripts/contract_check.py` (Stop): reads the session transcript and the `contract.yaml` files of installed plugins (local, read-only; never executed); once per session may block with the list of missing evidence; writes a small flag file in the OS temp folder.
- No connectors, no network, no secrets.

Before a directory submission, add a square listing icon (PNG or JPEG, 512 to 2048 px) named icon in the adapters/claude/.claude-plugin folder.
