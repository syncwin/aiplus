"""Tests for contract_check.py. Run: python tests/test_contract_check.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SCRIPT = os.path.join(ROOT, "adapters", "claude", "scripts", "contract_check.py")
TABLE = "| item | followed | evidence |\n|---|---|---|\n| fix | yes | tests pass |"


def line(*blocks):
    return json.dumps({"message": {"role": "assistant", "content": list(blocks)}})


def tool(name, **inp):
    return {"type": "tool_use", "name": name, "input": inp}


def text(t):
    return {"type": "text", "text": t}


class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.cfg = os.path.join(self.d, "cfg")
        os.makedirs(self.cfg)
        self.n = 0

    def run_hook(self, lines, sid=None, extra=None, contract=None):
        tp = os.path.join(self.d, "t%d.jsonl" % self.n)
        self.n += 1
        with open(tp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        env = dict(os.environ, CLAUDE_CONFIG_DIR=self.cfg, CLAUDE_PLUGIN_ROOT=contract or os.path.join(ROOT, "adapters", "claude"))
        payload = dict({"session_id": sid or "s%d" % self.n + os.path.basename(self.d), "transcript_path": tp, "cwd": self.d}, **(extra or {}))
        r = subprocess.run([sys.executable, "-I", SCRIPT], input=json.dumps(payload), capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0)
        return r.stdout.strip(), payload["session_id"]

    def test_blocks_without_table_after_edit(self):
        out, _ = self.run_hook([line(tool("Edit", file_path="a"), text("done"))])
        self.assertIn('"decision": "block"', out)
        self.assertIn("aiplus-file-changes", out)

    def test_passes_with_combined_table(self):
        out, _ = self.run_hook([line(tool("Write"), text(TABLE))])
        self.assertEqual(out, "")

    def test_no_edits_no_contract(self):
        out, _ = self.run_hook([line(tool("Read"), text("answer"))])
        self.assertEqual(out, "")

    def test_blocks_only_once_per_session(self):
        lines = [line(tool("Write"), text("done"))]
        a, sid = self.run_hook(lines, sid="once" + os.path.basename(self.d))
        b, _ = self.run_hook(lines, sid=sid)
        self.assertIn("block", a)
        self.assertEqual(b, "")

    def test_stop_hook_active_never_blocks(self):
        out, _ = self.run_hook([line(tool("Write"), text("done"))], extra={"stop_hook_active": True})
        self.assertEqual(out, "")

    def test_fail_open_on_garbage(self):
        tp = os.path.join(self.d, "bad.jsonl")
        open(tp, "w").write("not json\n{\n")
        r = subprocess.run([sys.executable, "-I", SCRIPT], input=json.dumps({"session_id": "g", "transcript_path": tp}), capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, ""))
        r = subprocess.run([sys.executable, "-I", SCRIPT], input="garbage", capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, ""))

    def test_third_party_contract_all_signals(self):
        plug = os.path.join(self.d, "plug")
        os.makedirs(os.path.join(plug, "skills", "rel"))
        c = {"id": "rel", "when_skill": "^plug:release$", "require": [
            {"label": "tests ran", "bash": "pytest"},
            {"label": "reviewer ran", "tool": "^Agent$"},
            {"label": "skill used", "skill": "^plug:release$"},
            {"label": "report exists", "file": "REPORT.md"},
            {"label": "unsafe location", "file": "/etc/passwd"}]}
        with open(os.path.join(plug, "skills", "rel", "contract.yaml"), "w") as f:
            f.write("contracts:\n  - " + json.dumps(c) + "\n")
        os.makedirs(os.path.join(self.cfg, "plugins"))
        with open(os.path.join(self.cfg, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"plugins": {"plug@m": [{"installPath": plug}]}}, f)
        start = [line(tool("Skill", skill="plug:release"))]
        out, _ = self.run_hook(start)
        for label in ("tests ran", "reviewer ran", "report exists"):
            self.assertIn(label, out)
        self.assertNotIn("skill used", out)
        self.assertNotIn("unsafe location", out)
        open(os.path.join(self.d, "REPORT.md"), "w").write("x")
        full = start + [line(tool("Bash", command="pytest -q"), tool("Agent", prompt="review"))]
        out, _ = self.run_hook(full)
        self.assertEqual(out, "")

    def test_bad_regex_and_unknown_signal_ignored(self):
        plug = os.path.join(self.d, "p2")
        os.makedirs(plug)
        c = {"id": "x", "when_tool": "^Write$", "require": [{"label": "bad", "bash": "("}, {"label": "unk", "weird": 1}]}
        open(os.path.join(plug, "contract.yaml"), "w").write("contracts:\n  - " + json.dumps(c) + "\n")
        out, _ = self.run_hook([line(tool("Write"), text("done"))], contract=plug)
        self.assertIn("bad", out)      # invalid regex counts as not satisfied
        self.assertNotIn("unk", out)   # unknown signal is not checked


if __name__ == "__main__":
    unittest.main(verbosity=1)
