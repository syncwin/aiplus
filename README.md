# AI+

Keeps every Claude session efficient: lead model plans and reviews, cheap subagents execute, minimal reads, one retry, routing to your installed plugins.

**Version** 0.0.4 - **Author** SyncWin - **License** MIT

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
