"""PreToolUse hook (Agent/Task): show the user which job runs on which agent type, model and effort.

Reads the hook JSON on stdin and prints {"systemMessage": "..."} on stdout. Fails open: any error
or unexpected input prints nothing and exits 0. Never blocks, never changes the tool call. Stdlib only.
"""
import json
import sys

MAX = 120


def clean(v, default):
    s = " ".join(str(v).split()) if v not in (None, "") else default
    return s[:MAX]


def message(data):
    if not isinstance(data, dict) or data.get("tool_name") not in ("Agent", "Task"):
        return ""
    ti = data.get("tool_input")
    if not isinstance(ti, dict):
        return ""
    return "AI+ > agent: %s | type: %s | model: %s | effort: %s" % (
        clean(ti.get("description"), "(no description)"),
        clean(ti.get("subagent_type"), "general-purpose"),
        clean(ti.get("model"), "inherited"),
        clean(ti.get("effort"), "inherited"),
    )


def main():
    try:
        msg = message(json.loads(sys.stdin.read(200000) or "{}"))
        if msg:
            print(json.dumps({"systemMessage": msg}))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
