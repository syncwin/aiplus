"""Tests for agent_notice.py. Run: python tests/test_agent_notice.py"""
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SCRIPT = os.path.join(ROOT, "dev", "scripts", "agent_notice.py")
HOOKS = os.path.join(ROOT, "dev", "hooks", "hooks.json")


def run(raw):
    r = subprocess.run([sys.executable, "-I", SCRIPT], input=raw, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


class T(unittest.TestCase):
    def test_full_input(self):
        out = run(json.dumps({"tool_name": "Agent", "tool_input": {
            "description": "Scan repo", "subagent_type": "Explore", "model": "haiku", "effort": "low"}}))
        self.assertEqual(json.loads(out)["systemMessage"],
                         "AI+ > agent: Scan repo | type: Explore | model: haiku | effort: low")

    def test_defaults(self):
        out = run(json.dumps({"tool_name": "Task", "tool_input": {"description": "Fix bug"}}))
        self.assertEqual(json.loads(out)["systemMessage"],
                         "AI+ > agent: Fix bug | type: general-purpose | model: inherited | effort: inherited")

    def test_other_tools_ignored(self):
        self.assertEqual(run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}})), "")

    def test_fails_open_on_bad_input(self):
        for raw in ("", "not json", "[]", json.dumps({"tool_name": "Agent", "tool_input": "x"})):
            self.assertEqual(run(raw), "")

    def test_long_and_multiline_values_are_cut(self):
        out = run(json.dumps({"tool_name": "Agent", "tool_input": {"description": "a\nb" + "x" * 500}}))
        self.assertNotIn("\n", json.loads(out)["systemMessage"])
        self.assertLess(len(out), 400)

    def test_hook_registered_without_blocking_event(self):
        with open(HOOKS, encoding="utf-8") as f:
            h = json.load(f)["hooks"]["PreToolUse"][0]
        self.assertEqual(h["matcher"], "Agent|Task")
        self.assertIn("agent_notice.py", h["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
