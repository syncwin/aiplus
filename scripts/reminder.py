"""SessionStart hook: print the short rule reminder (max 10 lines). Fails open."""
import os
import sys

try:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks", "reminder.txt")
    with open(p, encoding="utf-8") as f:
        print("".join(f.readlines()[:10]), end="")
except Exception:
    pass
sys.exit(0)
