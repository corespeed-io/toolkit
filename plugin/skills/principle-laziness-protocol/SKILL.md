---
name: principle-laziness-protocol
description: "Use when you refactor, judge diff size, or want to add abstractions, layers, or signal threading. Prefer deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

# Laziness Protocol

Prefer deletion. Make the smallest change that works.

- **Consolidate decisions.** Do not make the same choice in many locations. Put it behind one source of truth, and pass the result as a simple flag.
- **Make the diff small.** Make the smallest change that solves the problem. Fewer lines are better than "elegant" boilerplate.
- **Do not write again what a library does well.** When a good, well-known library fits, use it. Do not add an abstraction for one use.
