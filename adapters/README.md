# Adapters

`core/` holds the rules once, platform-neutral. An adapter turns them into the format one platform reads.

| Adapter | Output | Status |
|---|---|---|
| `claude` | Claude plugin: skill, hooks, scripts | 0.5.1 |
| `chatgpt` | custom instructions text, or a custom GPT | not started |
| `gemini` | Gem instructions or GEMINI.md | not started |

## Add an adapter

1. Create `adapters/<platform>/` with the files that platform needs (instructions file, config, docs).
2. In `scripts/build_adapters.py`, add a function that reads `load_rules()` and writes the generated parts (use marker comments for blocks inside hand-written files). Rules marked `enforce: hook` need a platform feature; where there is none, list them as plain guidance.
3. Run `python scripts/build_adapters.py`, then `--check`.
4. Keep platform-specific wording in the adapter, never in `core/`.
5. Add the adapter to the table above and to the changelog.

Never edit generated blocks by hand; change `core/rules.md` or `core/rules.yaml` instead.
