# AI+ (Claude plugin)

AI+ keeps every Claude session efficient and accountable: the lead model plans and reviews, cheaper subagents execute, reads stay minimal, retries are capped, and each answer ends with a short evidence table. It works on claude.ai, Cowork, the desktop app and Claude Code.

## Use

Install it from the marketplace and it loads on its own at session start; you can also type `/aiplus`. Python 3.9+ enables the hooks (agent notice, prompt nudge, evidence check, injection screen, plugin scan); without it the rules still apply and AI+ offers to install Python after you confirm.

Rules are generated from `core/rules.md` in the repository root; see the root README for install, layout and what the scripts read.
