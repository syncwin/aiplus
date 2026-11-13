"""Stop hook: check that the evidence promised by installed contracts exists in the transcript.

Finds contract.yaml files (own plugin root, installed plugins' roots and skills/*/), keeps
the contracts that apply to this session, checks each required signal against the
transcript and blocks ONCE per session, listing what is missing per contract. Stdlib only.
Fails open on any error or when over a 3 s time budget, never blocks twice, never
executes anything from a contract (bounded regexes and relative paths only).
A contract applies only when its own plugin's skill or tool was used. See core/contracts.md.
"""
import glob
import json
import os
import re
import sys
import tempfile
import threading

MAX_BYTES, MAX_REGEX, MAX_REQ = 20000, 200, 30
MAX_TEXT, MAX_CMD, BUDGET_S = 8000, 2000, 3.0


def config_home():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def plugin_name(root):
    try:
        with open(os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return str(json.load(f).get("name") or "")
    except (OSError, ValueError, AttributeError):
        return ""


def contract_paths(own_root=None):
    """Return [(path, plugin_name, is_own)]: the running plugin first, then installed ones."""
    roots = []
    if own_root:
        roots.append((own_root, plugin_name(own_root) or os.path.basename(os.path.normpath(own_root)), True))
    try:
        with open(os.path.join(config_home(), "plugins", "installed_plugins.json"), encoding="utf-8") as f:
            plugins = json.load(f).get("plugins", {})
        for key, entries in plugins.items():
            for e in entries if isinstance(entries, list) else [entries]:
                if isinstance(e, dict) and e.get("installPath"):
                    roots.append((e["installPath"], str(key).split("@")[0], False))
    except (OSError, ValueError, AttributeError):
        pass
    found, seen = [], set()
    for r, name, own in roots:
        for p in [os.path.join(r, "contract.yaml")] + sorted(glob.glob(os.path.join(r, "skills", "*", "contract.yaml"))):
            key = os.path.normcase(os.path.realpath(p))
            if os.path.isfile(p) and key not in seen:
                seen.add(key)
                found.append((os.path.normpath(p), name, own))
    return found


def parse_contracts(text):
    """Lines of the form `- {json object}` inside `contracts:`; anything else is ignored."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- {"):
            try:
                c = json.loads(s[2:])
            except ValueError:
                continue
            if isinstance(c, dict) and c.get("id") and isinstance(c.get("require"), list):
                out.append(c)
    return out


def load_contracts(paths):
    allc = []
    for p, name, own in paths:
        try:
            if os.path.getsize(p) <= MAX_BYTES:
                with open(p, encoding="utf-8") as f:
                    for c in parse_contracts(f.read()):
                        c["_plugin"], c["_own"] = name, own
                        allc.append(c)
        except OSError:
            pass
    return allc


def rx(pattern, text):
    if not isinstance(pattern, str) or len(pattern) > MAX_REGEX:
        return False
    try:
        return re.search(pattern, text) is not None
    except re.error:
        return False


def facts_from(path):
    f = {"tools": [], "skills": [], "bash": [], "last": ""}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            msg = e.get("message") if isinstance(e, dict) else None
            if not isinstance(msg, dict) or msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            text = ""
            for b in content or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    name, inp = str(b.get("name", ""))[:200], b.get("input") or {}
                    f["tools"].append(name)
                    if name == "Skill":
                        f["skills"].append(str(inp.get("skill", ""))[:200])
                    elif name in ("Bash", "PowerShell"):
                        f["bash"].append(str(inp.get("command", ""))[:MAX_CMD])
                elif b.get("type") == "text":
                    text += b.get("text", "")
            if text.strip():
                f["last"] = text
    f["last"] = f["last"][-MAX_TEXT:]
    return f


def own_skill(name, plugin):
    return name == plugin or name.startswith(plugin + ":")


def own_tool(name, plugin, own):
    """A plugin's own tools; the running plugin may also watch built-in tools."""
    return own or ("mcp__plugin_%s_" % plugin) in name or ("mcp__%s__" % plugin) in name


def applies(c, f):
    """A contract only applies when its own plugin's skill or tool was used."""
    plugin, own = c.get("_plugin", ""), bool(c.get("_own"))
    checks = []
    if c.get("when_skill"):
        checks.append(any(own_skill(s, plugin) and rx(c["when_skill"], s) for s in f["skills"]))
    if c.get("when_tool"):
        checks.append(any(own_tool(t, plugin, own) and rx(c["when_tool"], t) for t in f["tools"]))
    return any(checks)


def satisfied(req, f, cwd):
    if "tool" in req:
        return any(rx(req["tool"], t) for t in f["tools"])
    if "skill" in req:
        return any(rx(req["skill"], s) for s in f["skills"])
    if "bash" in req:
        return any(rx(req["bash"], b) for b in f["bash"])
    if "text" in req:
        return rx(req["text"], f["last"])
    if "file" in req:
        p = str(req["file"])
        if os.path.isabs(p) or p[:1] in "/\\" or ":" in p[:2] or ".." in p.replace("\\", "/").split("/"):
            return True  # unsafe path: ignore, never block on it
        return os.path.exists(os.path.join(cwd, p))
    return True  # no known signal: nothing to check


def evaluate(contracts, f, cwd="."):
    """Return {contract id: (reason, [missing labels])} for applicable, unmet contracts."""
    missing = {}
    for c in contracts:
        if not applies(c, f):
            continue
        for req in c["require"][:MAX_REQ]:
            if isinstance(req, dict) and not satisfied(req, f, cwd):
                entry = missing.setdefault(str(c["id"]), (str(c.get("reason") or "")[:200], []))
                entry[1].append(str(req.get("label") or "required evidence")[:200])
    return missing


def render(missing):
    out = []
    for cid, (reason, labels) in missing.items():
        out.append("- %s%s:" % (cid, " (%s)" % reason if reason else ""))
        out += ["  - " + x for x in labels]
    return "\n".join(out)


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return
    sid = "".join(c for c in str(data.get("session_id", "x")) if c.isalnum() or c in "-_")[:64]
    flag = os.path.join(tempfile.gettempdir(), "aiplus_contract_" + sid)
    if os.path.exists(flag):
        return
    tp = data.get("transcript_path")
    if not tp or not os.path.isfile(tp):
        return
    own = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    result = {}

    def work():
        result["m"] = evaluate(load_contracts(contract_paths(own)), facts_from(tp), data.get("cwd") or os.getcwd())

    t = threading.Thread(target=work, daemon=True)
    t.start()
    t.join(BUDGET_S)
    if t.is_alive():
        os._exit(0)  # over the time budget: fail open
    missing = result.get("m")
    if not missing:
        return
    fd = os.open(flag, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    os.close(fd)
    print(json.dumps({"decision": "block", "reason": "AI+ contract check: complete these before saying done, "
                      "then end with the combined ledger and compliance table:\n" + render(missing)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
