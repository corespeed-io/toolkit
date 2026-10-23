---
name: principle-attack-the-premise
description: "Use when two or more fixes with the same premise fail the same gate. Write the premise down and test it before you write a fix that assumes it."
disable-model-invocation: true
---

# Attack the Premise

When two or more fixes with the same premise fail the same gate, suspect the premise. Do not suspect only the fixes.

**Why:** Each failed fix is evidence against the belief that it assumed. A third fix on the same premise puts effort where the evidence says the cause is not.

**Pattern:**
- **Write the premise down.** The premise is the one sentence that all the failed fixes assumed.
- **Test the premise before the next fix.** Find an observation that gives a different result if the premise is false. Then make that observation. Examine how the failures are distributed, not only how large they are. Make the check easy to run again, per [Build the Lever](../principle-build-the-lever/SKILL.md).
- **Follow the evidence.**
  - If the evidence contradicts the premise, the cause is in a different location. Find what the failures have in common that the premise did not predict.
  - If the evidence confirms the premise, ask the next "why", per [Fix Root Causes](../principle-fix-root-causes/SKILL.md). The earlier fixes possibly treated a consequence and not the cause.
- **Remove the condition. Do not compensate for it**, per the [Laziness Protocol](../principle-laziness-protocol/SKILL.md). If the evidence shows that one part always gets the bad result, change the thing that causes this. A mechanism that cleans up after the condition keeps the cause. It also adds work on each run.

**Stop:** Do not start the next fix before you write down and test the premise.

This principle is different from [Redesign from First Principles](../principle-redesign-from-first-principles/SKILL.md). That principle builds a design again around a new requirement. This principle questions a fact that the current design assumes.
