# Scratchpad Format

End the task with one scratchpad. Chained stages add rows to it.

Open with the request ledger. One row per request the user made. Include added, declined and deferred ones. Status: done, partly done, in progress, failed, not started, needs you.

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

Facts only. Omit inapplicable sections.
