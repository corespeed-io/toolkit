---
name: principle-build-the-lever
description: "Use for any work that is not trivial: edits, migrations, analyses, checks. Build the tool that does or proves the work (codemod, script, generator, delegate skill). A reviewer can run the tool again."
disable-model-invocation: true
---

# Build the Lever

When the work is not trivial, build the tool that does it. Do not do the work by hand.

A codemod, generator, or script does the work the same way each time, and you can run it again at no cost. The tool is one artifact that a reviewer can read and run again to check the work. You can verify changes made by hand only if you make them again. A deterministic script changes "trust me" into "run this".

Build the lever by default. Do not build it only when the task is trivial: a few obvious edits that you can see immediately.

- Do the first unit by hand to learn the recipe. Then build the tool. To prove the tool, run it on that unit and diff the result against your hand-made version. Make sure that the lever is safe to run again.
- Use a codemod or script for edits, a generator for repetitive files, a dump-to-sqlite query for analysis, and a check that you can run again for verification.
- A deterministic lever is better than fan-out. If the tool can process all units in one pass, run it yourself. Do not send delegates to apply by hand what a script can do.
- When you send work to subagents, write the lever as a skill that all of them read. Put the recipe, the verification contract, and the do-not-touch limits in that one artifact. Keep it outside the write scope of the delegates, so that they cannot change the contract without notice.
- When you apply this principle, you make a file. If you cite this principle and the diff has no codemod, script, generator, or delegate skill, you did not apply it.
- Commit the lever when the work continues after the session.

The rule is triviality, not repetition. A one-time task also gets a lever when the lever makes the work possible to check. Per the [Laziness Protocol](../principle-laziness-protocol/SKILL.md), build the smallest script that does or proves the job. Do not build a framework.

This principle is different from [Encode Lessons in Structure](../principle-encode-lessons-in-structure/SKILL.md). That principle makes a recurring instruction into a permanent guardrail. This principle is about throughput and reviewability for the current work. To script the verification itself, see [Prove It Works](../principle-prove-it-works/SKILL.md).
