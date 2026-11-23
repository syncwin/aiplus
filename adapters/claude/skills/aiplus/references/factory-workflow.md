# Factory workflow (coding work done by delegated agents)

Keep this lean. A dedicated development plugin owns the detail (stack, review lenses, release steps); when one is installed it wins (rule 9). This page only sets the shape.

1. **Issue first.** Every coding change starts as an issue with acceptance criteria. Write the tests first: the merge gate only knows what the tests know.
2. **Isolated work.** The agent works in its own worktree and branch and opens a pull request. When CI fails, send the failure back to the agent. Allow a bounded number of tries (one retry, rule 4), then stop and report.
3. **Merge gate.** Tests passed, review approved, and the change matches the issue scope. A human reviews every pull request; the requester is not the approver.
4. **Holdout scenarios (optional, larger work).** Keep a few test scenarios the building agent never sees, and run them before merge.
5. **Start small.** One agent and small, well-described issues. Never run a setup without review.
