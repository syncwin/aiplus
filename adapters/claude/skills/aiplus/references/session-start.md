# Session start (recipe)

Replaces the SessionStart hook (`reminder.py`, `hooks/reminder.txt`) and its Python check. Follow it on the first reply of a session when no AI+ reminder was injected (no line starting "AI+ is active").

## Contents

- 1. What the hook did
- 2. Steps
- 3. Python

## 1. What the hook did

At session start, resume, clear and compact it printed at most 20 lines: the heading "AI+ is active. Core rules (all 17 in the aiplus skill; the user may overrule one only after explicit confirmation)", then one line per must-level rule (first sentence of each), then an order to invoke the `aiplus:aiplus` skill once with the Skill tool before the first reply (skipped on surfaces without skills).

## 2. Steps

1. Load the `aiplus` skill once (Skill tool, slug `aiplus:aiplus`). On a surface without the Skill tool, read `skills/aiplus/SKILL.md` by relative path from the plugin root.
2. Keep these must-level rules in force for the whole session (the full text is in the rules block of `SKILL.md`): 2 transparency, 3 lean context, 4 one retry, 5 know before asking, 6 never pick permanent names, 9 use what is installed, 11 right-size, 12 user can overrule, 13 security first, 14 accountability, 15 lean prompt crafting, 16 surface fit. Rule 5 is "should" for its look-up part and "must" for early clarifying questions. If the rules block and this list ever differ, the rules block wins.
3. After a resume, clear or compact, repeat step 2 in your head; do not print the list again unless asked.
4. Rule 14 starts here: before work, one line naming the rules and skills in play.

## 3. Python

The hook also checked for Python 3 and offered to install it. The directory edition and these recipes need no Python: do nothing. Only the local edition (with `hooks/`) uses Python, and its own session-start hook asks.
