---
name: principle-foundational-thinking
description: "Use before you write logic: choosing core types and data structures, ordering scaffold and feature work, deciding what concurrent actors share. Get the data structures right first."
disable-model-invocation: true
---

# Foundational Thinking

**Structural decisions** keep options open. **Code-level decisions** keep the code simple.

**Data structures first.** Get the data shape correct before you write logic. Define the core types early. Trace each access pattern. Choose structures that match the most frequent paths.

At code level, remove repetition in the structure, not in each line. Types and data models must converge. Three similar statements are better than an abstraction that comes too early. Use explicit code, not clever code. Test behavior and edge cases, not line counts.

**Concurrency corollary.** Before actors share state, ask: "What occurs if a different actor changes this at the same time?" If the answer is not "nothing", isolate the state.

**Scaffold first.** If something helps all later phases, do it first. Ask: "Do all later phases get a benefit when this exists?" CI, linting, test infrastructure, and shared types are scaffold. Put the work in the order that keeps options open: setup before features, tests before fixes. Keep commits small, with one purpose each.

Each increment must add a coherent abstraction or make an existing one deeper. Do not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding. Remove dead code first. Then make the foundations.
