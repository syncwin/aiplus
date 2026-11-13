# Plugin and skill scan (recipe)

Replaces `scan.py`. Use it once per session, when a task may fit an installed plugin or skill (rule 9), to build the routing table `| skill | use for |`.

## Contents

- 1. What the script did
- 2. Steps
- 3. Output
- 4. Limits

## 1. What the script did

It listed every installed skill as a compact table, read-only, local, no network: skills of installed plugins (named `<plugin>:<skill>`), skills in the user's Claude config folder, and skills in the project's `.claude/skills` folder. It read only the first 4,000 characters of each `SKILL.md`.

## 2. Steps

1. If the session already lists the available skills with one-line descriptions (Claude Code does), build the table from that list and stop; it is the cheapest path.
2. Otherwise find the Claude config folder (the one that holds `plugins` and `skills`; the environment variable `CLAUDE_CONFIG_DIR` names it when set, else the `.claude` folder in the user's home). Do not put its path in a shell command; use Read and Glob on it.
3. Read `plugins/installed_plugins.json` in that folder. Its `plugins` object maps `<plugin>@<marketplace>` to an install entry (or a list of them) with an `installPath`. The plugin name is the part of the key before `@`. If the file is missing or unreadable, treat the plugin list as empty.
4. For each plugin in key order, Glob `skills/*/SKILL.md` under its `installPath`. Then Glob `skills/*/SKILL.md` in the Claude config folder (no prefix), then `.claude/skills/*/SKILL.md` in the working folder (no prefix). Sort by folder name inside each group.
5. For each file, Read only the first 40 lines. Take `name` and `description` from the frontmatter between the first two `---` lines. A description may be folded (`>` or `|`): join its lines with single spaces. If `name` is missing, use the folder name. Prefix plugin skills with `<plugin>:`.
6. The "use for" text is the description's first sentence, cut at 80 characters.
7. Keep the first row for each skill name; drop later duplicates.

## 3. Output

```
| skill | use for |
|---|---|
| <plugin>:<skill> | <first sentence, max 80 chars> |

<N> skills, <M> plugins
```

Use the table to pick the skill that fits, and load it with the Skill tool. For a plugin that is not installed, read `recommended.md` and offer install steps; never install without asking (rule 9).

## 4. Limits

Reading 40 lines instead of 4,000 characters can cut a very long frontmatter; the first sentence is almost always inside it. Skills of plugins that are installed but disabled still appear; check that the Skill tool lists the one you pick.
