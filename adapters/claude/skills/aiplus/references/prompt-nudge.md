# Long-prompt nudge (recipe)

Applies to each user message, before work starts. No hook runs it.

## What to do

Read the user's prompt and, when it is long or multi-request, say one line: "AI+ rule 15: show the tight prompt block first, then proceed." Otherwise stay silent. Never block.

## Triggers

Any one is enough.

| Trigger | Test |
|---|---|
| Long prompt | more than 400 characters |
| List-like prompt | three or more lines that start (after optional spaces) with a list marker: a number followed by `.` or `)`, or `-`, or `*`, then a space |
| Many questions | three or more question marks |

## Steps

1. When a trigger fires, or the request is medium, large or ambiguous by your own judgment: show the tight rewritten prompt in one short Markdown block (rule 15: same requirements, no fluff, ASCII only, closed questions for real gaps), then proceed at once unless a gap needs a question.
2. When none fires and the request is simple, say nothing about it and do the work. Deep or reusable prompts go to aiaddon's `aiaddon-prompt` when it is installed.
