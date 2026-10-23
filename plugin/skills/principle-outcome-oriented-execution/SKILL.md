---
name: principle-outcome-oriented-execution
description: "Use for planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture. Do not keep smooth intermediate states with throwaway compatibility code."
disable-model-invocation: true
---

# Outcome-Oriented Execution

Optimize for the planned end state that you can verify. Do not optimize to keep intermediate states smooth.

**Why:** If you keep each intermediate step fully stable, you often add temporary compatibility code. That code often stays and becomes debt. Converge on the target architecture. Prove correctness at explicit verification boundaries.

**Core rule:**
- The integrity of the end state is more important than stability during the transition.
- Breakage in an intermediate state is acceptable when it is planned, limited in scope, and reversible.

**Guardrails:**
- Use this principle for planned rewrites and migrations with explicit phase boundaries.
- Declare where temporary breakage is acceptable.
- During the migration, keep high-signal checks for the areas that you change.
- At the end of the plan, do full static and runtime verification.
