"""Stop hook: once per session, remind to end with a request ledger.

Reminds only if files were changed this session and the last assistant message has
no markdown table. Reads hook JSON from stdin. Fails open; never blocks twice.
"""
import json
import os
import sys
import tempfile

EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
REASON = ("AI+: files changed this session. End with a request ledger: a short table of "
          "request | status | evidence. Then stop.")


def scan(path):
    changed, last = False, ""
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
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
                if b.get("type") == "tool_use" and b.get("name") in EDIT_TOOLS:
                    changed = True
                elif b.get("type") == "text":
                    text += b.get("text", "")
            if text.strip():
                last = text
    return changed, last


def has_table(text):
    for r in (l.strip() for l in text.splitlines()):
        if r.startswith("|") and "-" in r and set(r.replace("|", "").strip()) <= set("-: "):
            return True
    return False


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return
    sid = "".join(c for c in str(data.get("session_id", "x")) if c.isalnum() or c in "-_")[:64]
    flag = os.path.join(tempfile.gettempdir(), "aiplus_stop_" + sid)
    if os.path.exists(flag):
        return
    tp = data.get("transcript_path")
    if not tp or not os.path.isfile(tp):
        return
    changed, last = scan(tp)
    if not changed or has_table(last):
        return
    # Create the once-per-session flag atomically and never through a planted symlink.
    fd = os.open(flag, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    os.close(fd)
    print(json.dumps({"decision": "block", "reason": REASON}))


try:
    main()
except Exception:
    pass
sys.exit(0)
