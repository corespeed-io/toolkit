---
name: principle-minimize-reader-load
description: "Use when you review or shape code that is hard to trace. Count layers between question and answer, and hidden state the reader must remember. Remove one-caller wrappers and reduce mutable scope."
disable-model-invocation: true
---

# Minimize Reader Load

Maintainability is the work that a reader must do to understand code. Measure two axes:
- **Layers to trace:** the indirections between the question and the answer.
- **State to hold:** the hidden or mutable context that the reader must remember.

LOC, cyclomatic complexity, and "clean architecture" are only proxies. Reader load is the important thing. The two axes are independent. A flat file with 50 globals can be as difficult to understand as a stack of 6 adapter layers. Control both axes. This principle is the human version of [Guard the Context Window](../principle-guard-the-context-window/SKILL.md). Readers also have limited working memory.

- **Remove layers** that cost more than they save: wrappers with one caller, adapters with no second implementation, and speculative indirection that the code never needed. Put their code inline.
- **Make each layer change the abstraction.** A layer that repeats the same methods and arguments adds reader load and gives no compression. Remove pass-through layers.
- **Require interface compression.** A broad interface that hides little complexity makes readers learn both the surface and the implementation. Use boundaries that hide important decisions.
- **Reduce the scope of state.** Use pure functions (return values, not mutations). Use locals before fields, fields before module state, and module state before globals. Derive values. Do not sync them.
- **Name the invariant at the boundary,** not in each consumer. Then the reader learns it one time.
- Before you add a layer or a piece of state, ask: "Does it decrease reader load in a different location by the same amount or more?"

**The test:** can a new reader answer "Where does X come from?" and "What can change X?" in less than 30 seconds? If not, remove layers or remove state.
