# AI+ rule reasons

Why behind each rule in SKILL.md, with its level and enforcement. Generated from core/rules.md by scripts/build_adapters.py. Do not edit here.

1. **Model routing.** a strong model earns its cost on judgment, not on mechanical work; the same outcome costs less, unchecked worker output is a risk, a delegation has a fixed overhead, and most delegated work does not need deep reasoning; quality per dollar is what makes AI affordable for everyone. (should, guidance)
2. **Transparency.** the user decides on cost and quality only when the routing is visible. (must, hook)
3. **Lean context.** every token read is paid for again on each later turn; repetition adds cost and no value; stable prefixes are cached and cheaper; deterministic tools are faster, cheaper and repeatable. (must, guidance)
4. **One retry.** repeated failures burn budget without new information. (must, guidance)
5. **Know before asking.** the answer may already exist, and every round trip costs time and context. (must, guidance)
6. **Never pick permanent names.** renaming shipped things is expensive. (must, guidance)
7. **Log improvement ideas.** ideas are kept without widening scope. (should, guidance)
8. **Clear output.** output tokens and reading time are costs, and scanning is cheaper than reading prose. (should, guidance)
9. **Use what is installed.** a dedicated tool beats improvising, specialists know their domain better than a general guard, installs change the user's environment, and outside services must not receive private data unasked. (must, guidance)
10. **Continuity.** the next session continues instead of rediscovering, and quality drops and cost rises as context fills. (should, guidance)
11. **Right-size.** the user decides on cost before it is spent, extra code and output are paid for twice (now and in maintenance), and rework is the largest hidden cost. (must, guidance)
12. **User can overrule.** rules serve the user, yet an accidental override must not slip through. (must, guidance)
13. **Security first.** a leak or a regression costs far more than any saving. (must, guidance)
14. **Accountability and enforcement.** the user sees at a glance what was actually done, checkable promises beat good intentions, and one table keeps the audit cheap. (must, hook)
15. **Lean prompt crafting.** a faithful, tight prompt prevents rework without altering what the user asked, and closed questions cost one quick answer. (must, guidance)
16. **Surface fit.** claiming a feature the surface lacks wastes a turn and misleads the user, and home-folder paths fail on cloud and chat surfaces and trigger permission prompts. (must, guidance)
17. **Research before building.** guessed configs go stale or insecure, and a short lookup is cheaper than a rework. (should, guidance)
