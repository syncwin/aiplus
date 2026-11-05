# AI+

Keeps every Claude session efficient: lead model plans and reviews, cheap subagents execute, minimal reads, one retry, routing to your installed plugins.

**Version** 0.0.1 - **Author** SyncWin - **License** MIT

## Skills

| Skill | Role |
|---|---|
| `aiplus` | Router |

## Install

```
/plugin marketplace add syncwin/aiplus
/plugin install aiplus@aiplus
```

Start with `/aiplus`, or let it load when a multi-step task begins. Requires Python 3 (`python3` on PATH) for the hooks and scan; without it the hooks fail without blocking.

## Companion prompt

`prompts/ai.json` is a ready-made form for Prompt Builder. It is delivered next to the package, never inside it. Import it there, fill in the fields, and send it to Claude to start this plugin without typing the request from scratch.

## What it runs, reads, and sends

- `scripts/scan.py`: reads `~/.claude/plugins/installed_plugins.json` and skill folders (local, read-only) and prints a table. No network.
- `scripts/reminder.py` (SessionStart): prints `hooks/reminder.txt`.
- `scripts/stop_check.py` (Stop): reads the session transcript; once per session may ask for a request ledger; writes a small flag file in the OS temp folder.
- No connectors, no network, no secrets.

Before a directory submission, add a square listing icon (PNG or JPEG, 512 to 2048 px) named icon in the .claude-plugin folder.
