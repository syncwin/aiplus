# aiplus-handoff

## Context

A long chat loses its state when it ends or the context fills. Re-explaining costs tokens and drops decisions. AI+ rule 10 already suggests a new chat with a handoff summary; this skill produces that summary as one verified file.

## Behaviour

- Triggers on `/aiplus:aiplus-handoff`, "write a handoff", "wrap up for a new chat", or a nearly full context.
- Writes one file: `<outputs root>\<project>\Handoff <YYYY-MM-DD>.md`.
- Never includes secrets or transcripts; marks unverified facts.
- Links the previous handoff instead of copying it.
- Saves progress to memory (or `PROGRESS.md`) with the file path.

## How it works

1. Resolve the path: plugin option `outputs_root`, else `D:\SyncWin\AI Outputs`, else `docs/handoff/` if that drive is missing.
2. Collect facts, verify them (`gh` for PRs and branches, file listings), mark the rest `(unverified)`.
3. Write the sections: Next chat, Who and rules, Decisions, State, Done this session, In progress, Next, Waiting on user, Open questions, Files and links.
4. Scan for `github_pat_`, `ghp_`, `sk-`, `Bearer `, `password=`; stop on a hit.
5. Call `save_progress`, then end with the request ledger.

## UI in text

The user sees the file path and one line to paste into a new chat, then the ledger table. Setting: "Handoff outputs folder" (`outputs_root`) in the plugin options.

## Sources

Applied to the template:

- Anthropic, "Effective context engineering for AI agents" (2025-09-29), https://www.anthropic.com/research/effective-context-engineering-for-ai-agents : smallest set of high-signal tokens; structured note-taking outside the context window; compaction keeps decisions and unresolved issues; keep lightweight references (paths, links) instead of pasting data.
- Anthropic, "Effective harnesses for long-running agents" (2025-11-26), https://www.anthropic.com/research/effective-harnesses-for-long-running-agents : progress file plus git history as the bridge between sessions; leave a clean state; one item at a time; verify the state before new work; do not declare the job done early.
- Examples reviewed (not copied): https://github.com/anthropics/claude-code/issues/11455 (session handoff file proposal), https://github.com/jumpifequal/handoff-skill, https://github.com/googlarz/context-handoff.

Resulting changes: Next-chat line includes "verify State"; State records last commit and clean or dirty; Next is one item at a time; the file lists what is not done and unverified.

## Limits

- Only as accurate as the facts the session can verify.
- Does not read prior chats; it summarizes the current one.
- Memory saving needs memory tools; otherwise `PROGRESS.md`.

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-11-06 | Added |
