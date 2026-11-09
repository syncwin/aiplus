"""Regenerate adapter files from core/ (single source of truth). Stdlib only.

Writes, for the Claude adapter:
  - the rules block between the BEGIN/END markers in skills/aiplus/SKILL.md
  - skills/aiplus/references/rules.md (the why, level and enforcement per rule)
  - hooks/reminder.txt (the "must" rules, one line each)
  - .mcp.json (Composio connector, from core/mcp.json)
  - scripts/screen_text.py + injection_model.json (from core/guardrail)
  - copies of LICENSE and CHANGELOG.md into adapters/claude

Idempotent: files are rewritten only when content changes.
Usage: python scripts/build_adapters.py [--check]   (--check exits 1 if anything is stale)
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CORE = os.path.join(ROOT, "core")
CLAUDE = os.path.join(ROOT, "adapters", "claude")
BEGIN, END = "<!-- BEGIN GENERATED RULES (scripts/build_adapters.py) -->", "<!-- END GENERATED RULES -->"
META = re.compile(r"-\s*\{id:\s*(\d+),\s*title:\s*(.+?),\s*level:\s*(must|should),\s*enforce:\s*(guidance|hook)(?:,\s*was:\s*\[[\d,\s]*\])?\s*\}\s*$")
RULE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+(.*?)\s+\*Why:\*\s+(.*)$")


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def load_rules():
    meta = {}
    for line in read(os.path.join(CORE, "rules.yaml")).splitlines():
        s = line.strip()
        if s.startswith("- {"):
            m = META.match(s)
            if not m:
                sys.exit("rules.yaml: bad line: " + s)
            meta[int(m.group(1))] = {"title": m.group(2), "level": m.group(3), "enforce": m.group(4)}
    rules = []
    for line in read(os.path.join(CORE, "rules.md")).splitlines():
        m = RULE.match(line)
        if m:
            n = int(m.group(1))
            if n not in meta:
                sys.exit("rules.md rule %d missing in rules.yaml" % n)
            rules.append({"id": n, "head": m.group(2), "text": m.group(3), "why": m.group(4), **meta[n]})
    ids = [r["id"] for r in rules]
    if ids != list(range(1, len(ids) + 1)) or set(ids) != set(meta):
        sys.exit("rule numbers must be 1..N and match between rules.md and rules.yaml")
    return rules


def first_sentence(text):
    return re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]


def skill_block(rules):
    lines = ["%s" % BEGIN]
    for r in rules:
        lines.append("%d. **%s** %s" % (r["id"], r["head"], r["text"]))
    lines.append(END)
    return "\n".join(lines)


def reminder(rules):
    must = [r for r in rules if r["level"] == "must"]
    out = ["AI+ is active. Core rules (all %d in the aiplus skill; the user may overrule one only after explicit confirmation):" % len(rules)]
    out += ["%d. %s %s" % (r["id"], r["head"], first_sentence(r["text"])) for r in must]
    out.append("Before your first reply in this session, invoke the aiplus:aiplus skill once with the Skill tool (skip only on surfaces without skills).")
    return "\n".join(out) + "\n"


def full_rules(rules):
    out = ["# AI+ rule reasons", "", "Why behind each rule in SKILL.md, with its level and enforcement. Generated from core/rules.md by scripts/build_adapters.py. Do not edit here.", ""]
    for r in rules:
        out.append("%d. **%s** %s (%s, %s)" % (r["id"], r["head"], r["why"], r["level"], r["enforce"]))
    return "\n".join(out) + "\n"


def write(path, content, stale):
    old = read(path) if os.path.exists(path) else None
    if old == content:
        return
    stale.append(os.path.relpath(path, ROOT))
    if not CHECK:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)


def main():
    rules = load_rules()
    stale = []
    skill = os.path.join(CLAUDE, "skills", "aiplus", "SKILL.md")
    text = read(skill)
    if BEGIN not in text or END not in text:
        sys.exit("SKILL.md is missing the generated-rules markers")
    pre, rest = text.split(BEGIN, 1)
    post = rest.split(END, 1)[1]
    write(skill, pre + skill_block(rules) + post, stale)
    write(os.path.join(CLAUDE, "skills", "aiplus", "references", "rules.md"), full_rules(rules), stale)
    write(os.path.join(CLAUDE, "hooks", "reminder.txt"), reminder(rules), stale)
    write(os.path.join(CLAUDE, "skills", "aiplus", "references", "surfaces.md"), read(os.path.join(CORE, "surfaces.md")), stale)
    write(os.path.join(CLAUDE, ".mcp.json"), read(os.path.join(CORE, "mcp.json")), stale)  # Composio connector, no keys
    for name in ("screen_text.py", "injection_model.json", "trusted_sources.json"):  # prompt-injection screen for MCP tool output
        write(os.path.join(CLAUDE, "scripts", name), read(os.path.join(CORE, "guardrail", name)), stale)
    for name in ("LICENSE", "CHANGELOG.md"):  # the installed plugin ships only adapters/claude
        write(os.path.join(CLAUDE, name), read(os.path.join(ROOT, name)), stale)
    verb = "stale" if CHECK else "updated"
    print("%d rules; %s: %s" % (len(rules), verb, ", ".join(stale) if stale else "none"))
    return 1 if (CHECK and stale) else 0


CHECK = "--check" in sys.argv[1:]
if __name__ == "__main__":
    sys.exit(main())
