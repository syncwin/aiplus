"""List installed Claude plugins/skills as a compact routing table. Stdlib only.

Run: python -I scripts/scan.py
"""
import json
import os
import re

home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def front(path):
    """Return (name, description) from SKILL.md frontmatter."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4000)
    except OSError:
        return None, ""
    m = re.match(r"---\s*\r?\n(.*?)\r?\n---", head, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r"^description:\s*(?:[>|][-+]?)?\s*(.*?)(?=^[A-Za-z][\w-]*:|\Z)", fm, re.M | re.S)
    desc = " ".join(d.group(1).split()) if d else ""
    return (name.group(1).strip().strip("\"'") if name else None), desc


def short(desc):
    return re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0][:80]


def skills_in(root, prefix):
    out = []
    if not os.path.isdir(root):
        return out
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d, "SKILL.md")
        if os.path.isfile(p):
            n, desc = front(p)
            out.append((prefix + (n or d), short(desc)))
    return out


plugins = {}
try:
    with open(os.path.join(home, "plugins", "installed_plugins.json"), encoding="utf-8") as f:
        plugins = json.load(f).get("plugins", {})
except (OSError, ValueError, AttributeError):
    pass

rows = []
for key, entries in sorted(plugins.items()):
    pname = key.split("@")[0]
    for e in entries if isinstance(entries, list) else [entries]:
        ip = e.get("installPath") if isinstance(e, dict) else None
        if ip:
            rows += skills_in(os.path.join(ip, "skills"), pname + ":")
rows += skills_in(os.path.join(home, "skills"), "")
rows += skills_in(os.path.join(os.getcwd(), ".claude", "skills"), "")

print("| skill | use for |")
print("|---|---|")
seen = set()
for n, d in rows:
    if n not in seen:
        seen.add(n)
        print("| %s | %s |" % (n, d))
print("\n%d skills, %d plugins" % (len(seen), len(plugins)))
