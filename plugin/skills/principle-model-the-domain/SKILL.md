---
name: principle-model-the-domain
description: "Use when you write stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a data structure, not in scattered conditionals."
disable-model-invocation: true
---

# Model the Domain

Encode the real domain in a data structure. Do not spread it across conditionals. A structure that matches the domain makes invalid states impossible to represent, and it removes branches. When you write the code, this choice costs little. If you add it later, it is a refactor, and people delay it.

Use:

- A state machine, not scattered booleans, phases, or lifecycle checks.
- A typed model, not loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union, not branches spread across files.
- A reducer or a command/event model, not ad hoc state mutations.
- A module that contains one body of domain knowledge, not a sequence such as load, validate, transform, and save. Execution order is not ownership.
- A small module boundary that collects repeated behavior, ownership, or invariants.
- A queue, cache, index, graph, tree, or normalized collection where the access pattern needs it.
- A different structure that fits. When no structure fits, find what the code must never allow and how the code reads the data. Then find the structure that encodes exactly that.

Do not force an abstraction. Use simple code if the current shape is already clear, local, and not likely to grow. Be careful with an abstraction that adds indirection but does not remove branches, duplicate rules, invalid states, or lifecycle risk.

These signs show that you did not apply this principle:
- A new feature adds one more branch to an existing if/else chain.
- A second boolean must stay in sync with the first.
- The code uses temporal decomposition. Modules named after phases repeat the same domain rules across steps.
