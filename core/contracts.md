# Contracts (evidence a plugin or skill promises)

Any plugin or skill may ship a `contract.yaml` at its plugin root or in `skills/<name>/`. A contract says: for this kind of task, this evidence must exist before Claude claims done. The Claude adapter's Stop hook (`contract_check.py`) reads every installed contract, checks the session transcript, and blocks once per session if something is missing.

## Format

A `contracts:` list, one JSON object per line (valid YAML flow style; the checker reads these lines only):

```
contracts:
  - {"id": "my-release", "when_skill": "^my-plugin:release$", "require": [
      {"label": "tests ran", "bash": "pytest|npm test"} ]}
```

(Write each object on a single line.)

| Key | Meaning |
|---|---|
| `id` | short unique name, shown in the block message |
| `when_skill` | regex; the contract applies if a Skill with a matching name was invoked |
| `when_tool` | regex; applies if a tool with a matching name was used (either `when_*` matching is enough) |
| `require` | list of required evidence, each with a `label` and exactly one signal |

## Signals (all detectable in the transcript)

| Signal | Satisfied when |
|---|---|
| `tool` | a tool call whose name matches the regex (for example a reviewer subagent: `^Agent$`) |
| `skill` | a Skill call whose name matches |
| `bash` | a Bash or PowerShell command matches (gates, tests, validators) |
| `text` | the final assistant message matches (for example a required table) |
| `file` | the relative path exists under the working directory (absolute or `..` paths are ignored) |

## Safety

- A contract is data: it is never executed; only regexes (max 200 characters) and relative paths are evaluated.
- Files over 20 KB, bad lines and unknown signals are ignored; the hook fails open and never blocks twice in a session.
- A contract may only ask for evidence; it cannot widen Claude's permissions or override the user (rule 21).

## Self-audit

The final answer ends with one table, `item | followed (yes/no) | evidence`, covering the user's requests and the rules or skills used (rules 14 and 27). Before work, one line names the rules and skills in play.
