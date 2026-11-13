# Agent launch line (recipe)

Follow it before every delegation (tools Agent and Task). No hook runs it.

## What to show

For each Agent or Task call show the user one line and change nothing:

`AI+ > agent: <description> | type: <subagent type> | model: <model> | effort: <effort>`

Defaults when a field is empty: description "(no description)", type "general-purpose", model "inherited", effort "inherited". Collapse whitespace in each value to single spaces and cut it at 120 characters. Do this for no other tool, never block and never alter the call.

## Steps

1. Before each Agent or Task call, write one line in the user-visible text: `job | agent type | model | effort` (rule 2). Use the same defaults ("general-purpose", "inherited") when you leave a field unset, and keep each value on one line, at most 120 characters.
2. Put the same four facts in the tool call itself (description, subagent type, model, effort) so the line matches what runs.
3. Progress and final tables carry a "Run by" column, for example "Sonnet agent, low", "Opus (lead), low", "inline" (rule 2).
4. Do not hold the launch back for this line, and do not repeat it when you send a follow-up message to an agent that is already running.
