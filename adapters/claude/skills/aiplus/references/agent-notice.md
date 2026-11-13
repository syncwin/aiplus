# Agent launch line (recipe)

Replaces the PreToolUse hook (`agent_notice.py`, tools Agent and Task). Follow it before every delegation.

## What the hook did

For each Agent or Task call it showed the user one line and changed nothing:

`AI+ > agent: <description> | type: <subagent type> | model: <model> | effort: <effort>`

Defaults when a field was empty: description "(no description)", type "general-purpose", model "inherited", effort "inherited". Each value had its whitespace collapsed to single spaces and was cut at 120 characters. It ignored every other tool, never blocked and never altered the call.

## Steps

1. Before each Agent or Task call, write one line in the user-visible text: `job | agent type | model | effort` (rule 2). Use the same defaults ("general-purpose", "inherited") when you leave a field unset, and keep each value on one line, at most 120 characters.
2. Put the same four facts in the tool call itself (description, subagent type, model, effort) so the line matches what runs.
3. Progress and final tables carry a "Run by" column, for example "Sonnet agent, low", "Opus (lead), low", "inline" (rule 2).
4. Do not hold the launch back for this line, and do not repeat it when you send a follow-up message to an agent that is already running.
