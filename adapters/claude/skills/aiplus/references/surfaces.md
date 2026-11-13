# Claude surfaces: what works where

Researched 2026-11-06 from official Anthropic pages (treated as data). Re-check before relying on a cell; "?" means the docs do not state it. Used by rule 16.

| Capability | CC terminal / IDE | Desktop Code tab (local) | Code on web / mobile Code tab (cloud) | Cowork (desktop; web/mobile beta) | Chat (web, desktop, iOS/Android) |
|---|---|---|---|---|---|
| Plugins | Yes (`/plugin`, `--plugin-dir`) | Yes (+ > Add plugins); local and SSH sessions only | No local plugins; account-synced plugins only | Yes (account; Customize > Plugins) | Yes, subset (Customize > Plugins, account) |
| Skills | Yes (`~/.claude/skills`, plugins) | Yes | Yes (repo skills, account-enabled skills) | Yes | Yes (needs code execution on; upload zip; mobile use: ? ) |
| Subagents + model choice | Yes (Agent tool, `/model`, per-agent model) | Yes (model picker mid-session) | Yes (Agent tool; `/model sonnet` as argument) | Sub-agents yes; model choice ? | No subagents; model picker only |
| MCP / connectors | Yes (all kinds) | Yes (connectors GUI, manual MCP) | Via cloud mechanism; local MCP no | Yes (remote; local when session runs on your PC) | Remote connectors only (add in Connectors) |
| File access | Local FS, Bash | Local FS, Bash | Cloud VM clone of the GitHub repo | Folders you grant (desktop only) | Uploads and files created in code execution; no local FS |
| Instructions | CLAUDE.md, auto memory, settings | CLAUDE.md, settings | Repo CLAUDE.md | Account instructions, plugins | Project instructions + knowledge, profile preferences |
| Mobile (iOS/Android) | n/a | n/a | Code tab = client for cloud sessions, Remote Control (local session), Dispatch | Check progress and steer | Chat only; no subagents, no local files |

## Notes

- Claude Code engine is shared: CLAUDE.md, settings and MCP carry across terminal, IDE, desktop and cloud, but cloud sessions do not read local `~/.claude` settings or local plugins.
- Plugin components per surface (chat/Cowork/Code): skills yes/yes/yes; commands yes/yes/yes; agents ignored/yes/yes; local MCP ignored/yes (on your PC)/yes; bin/ executables cannot install on chat or Cowork.
- Terminal-only commands (`/plugin`, `/resume`) do not run from the mobile app or cloud sessions.
- Remote Control and Dispatch drive a session on your own computer from a phone; that session has terminal capabilities, the phone is only the client.
- Chat skills need Settings > Capabilities > code execution and file creation on; not stated for Claude Code via API keys or Bedrock.

## Sources

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/desktop
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/claude-code-on-the-web
- https://code.claude.com/docs/en/mobile
- https://claude.com/docs/plugins/platform-support
- https://support.claude.com/en/articles/12512180-using-skills-in-claude
- https://support.claude.com/en/articles/9517075-what-are-projects
- https://support.claude.com/en/articles/13345190-getting-started-with-cowork
