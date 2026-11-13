"""Tests that the Markdown recipes (the hook-free edition) match the scripts and rules. Run: python tests/test_recipes.py"""
import json
import os
import re
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKILL_DIR = os.path.join(ROOT, "adapters", "claude", "skills", "aiplus")
REFS = os.path.join(SKILL_DIR, "references")
NAMES = ("session-start", "prompt-nudge", "agent-notice", "screen-injection", "evidence-check", "plugin-scan")


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as f:
        return f.read()


class T(unittest.TestCase):
    def test_recipes_exist_and_are_linked(self):
        skill = read(SKILL_DIR, "SKILL.md")
        for n in NAMES:
            self.assertTrue(os.path.isfile(os.path.join(REFS, n + ".md")), n)
            self.assertIn("references/%s.md" % n, skill, n)
        self.assertLess(len(skill.splitlines()), 500)

    def test_no_home_or_absolute_paths_in_recipes(self):
        for n in NAMES:
            t = read(REFS, n + ".md")
            self.assertNotIn("~/", t, n)
            self.assertIsNone(re.search(r"\b[A-Za-z]:[\/]", t), n)

    def test_trusted_prefixes_match_the_script_data(self):
        cfg = json.loads(read(ROOT, "core", "guardrail", "trusted_sources.json"))
        t = read(REFS, "screen-injection.md")
        for p in cfg["trusted_prefixes"]:
            self.assertIn(p, t, p)

    def test_prompt_nudge_thresholds(self):
        t = read(REFS, "prompt-nudge.md")
        for x in ("400 characters", "three or more lines", "three or more question marks"):
            self.assertIn(x, t, x)

    def test_agent_notice_defaults(self):
        t = read(REFS, "agent-notice.md")
        for x in ("(no description)", "general-purpose", "inherited", "120"):
            self.assertIn(x, t, x)

    def test_must_rules_listed_in_session_start(self):
        must = [int(m.group(1)) for m in re.finditer(r"id:\s*(\d+),[^}]*level:\s*must", read(ROOT, "core", "rules.yaml"))]
        t = read(REFS, "session-start.md")
        line = t.split("in force", 1)[1].splitlines()[0]
        listed = [int(x) for x in re.findall(r"(?:: |, )(\d+) ", line)]
        self.assertEqual(sorted(must), sorted(listed))

    def test_evidence_check_matches_contract(self):
        contract = read(ROOT, "adapters", "claude", "contract.yaml")
        t = read(REFS, "evidence-check.md")
        for tool in re.search(r'"when_tool": "\^\(([^)]*)\)\$"', contract).group(1).split("|"):
            self.assertIn(tool, t, tool)
        for x in ("20,000", "8,000", "2,000", "30 requirements", "200 characters"):
            self.assertIn(x, t, x)

    def test_plugin_scan_limits(self):
        t = read(REFS, "plugin-scan.md")
        for x in ("installed_plugins.json", "80 characters", "skills/*/SKILL.md"):
            self.assertIn(x, t, x)


if __name__ == "__main__":
    unittest.main()
