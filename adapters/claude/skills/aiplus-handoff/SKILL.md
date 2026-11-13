---
name: aiplus-handoff
description: >
  Use when the user says "/aiplus:aiplus-handoff", "write a handoff", "wrap up for a new chat", "hand this off" or "summarize where we are so I can start a new chat", or when the context window is nearly full (rule 10). Writes ONE condensed handoff file so a fresh chat continues without re-explaining.
license: MIT
---

# AI+ Handoff

One file, condensed, verified. Never a transcript.

## Path

1. Outputs root: `${user_config.outputs_root}`. If empty, use `<default outputs folder>` (a folder you name once; ask if none is known).
2. If the root's drive or folder is missing, use `docs/handoff/` in the project.
3. File: `<root>\<project>\Handoff <YYYY-MM-DD>.md`. Project = working folder name, else the memory project. Same day twice: append ` 2`.
4. An older handoff exists: link it on line 1 as "Supersedes: <path>"; do not copy it.

## Write

Tables over prose. Sections, in order; omit one only if empty:

| Section | Holds |
|---|---|
| Next chat | One paste-ready line: `load_progress <project>, read <this file>, verify State, then do "Next"` |
| Who and rules | Only standing user rules and preferences learned or confirmed this session |
| Decisions | Dated; what was chosen and what was rejected |
| State | Repos, branches (last commit, clean or dirty), PRs (status, link), versions, installed tools, key paths, how to run the check that shows the work is healthy |
| Done this session | Short list |
| In progress | Who, what, where |
| Next | Ordered steps; one item at a time, highest priority first |
| Waiting on user | Items only the user can do |
| Open questions | Closed questions with options |
| Files and links | Paths and URLs that matter |

## Rules

- Leave work in a clean, resumable state (commit or say what is uncommitted) before writing; list what is NOT done and what is unverified so the next chat never declares victory early.
- Condense. Never paste transcripts or long output.
- Verify before writing: PR and branch states via `gh`, files exist via a listing. Mark anything unchecked `(unverified)`.
- No secrets. After writing, scan the file for `github_pat_`, `ghp_`, `sk-`, `Bearer `, `password=`. On a hit, stop, delete the file, tell the user, and do not echo the value.
- Save progress: call `save_progress` (memory tools) with a short summary and the file path, `tool` set to `claude-code`. Without memory tools, update `PROGRESS.md`.
- Never read or write memory for work the user marked separate or private.
- Tell the user the path and the Next-chat line.

## Scratchpad

End with the request ledger (`references/scratchpad.md`).
