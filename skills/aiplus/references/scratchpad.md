# Scratchpad Format

Every skill, connector, and agent ends its task with one. Standalone: emit at the end. Chained: each stage adds rows to one running scratchpad, emitted once at the end.

It opens with the request ledger: one row per individual request the user made during the task (split compound asks; include requests added mid-task, questions, and anything declined or deferred), so nothing goes unaccounted for. Status is one of done, partly done, in progress, failed, not started, needs you. Context is one clause: the result, the blocker, or what is left.

```
### Scratchpad: <Visible Name> v<version>
**Scope:** <what was run>

| # | Request | Status | Context |
|---|---|---|---|
| 1 | <one request, in the user's words> | <status> | <result, blocker, or what's left> |

| Area | Result |
|---|---|
| <thing built/checked/changed> | <done / pass / fail + one clause> |

**Changed:** <files or components, one line each>
**Flags:** <failures, assumptions, open items; omit if none>
**Next:** <single next action; omit if none>
```

Facts only. Omit inapplicable sections. Successes in one line; detail only for failures.
