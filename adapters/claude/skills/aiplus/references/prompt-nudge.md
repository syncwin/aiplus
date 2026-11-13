# Long-prompt nudge (recipe)

Stands in for the UserPromptSubmit hook (`prompt_nudge.py`). Applies to each user message, before work starts.

## What the hook did

It read the user's prompt and, when the prompt was long or multi-request, printed one line: "AI+ rule 15: show the tight prompt block first, then proceed." Otherwise it stayed silent. It never blocked.

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
