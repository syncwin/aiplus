"""UserPromptSubmit hook: for long or multi-request prompts, remind rule 15. Quiet otherwise. Fails open."""
import json
import re
import sys

try:
    text = str(json.load(sys.stdin).get("prompt", ""))
    multi = len(re.findall(r"(?m)^\s*(?:\d+[.)]|[-*])\s", text)) >= 3 or text.count("?") >= 3
    if len(text) > 400 or multi:
        print("AI+ rule 15: show the tight prompt block first, then proceed.")
except Exception:
    pass
sys.exit(0)
