---
name: principle-subtract-before-you-add
description: "Use when you plan the order of an addition, refactor, or rewrite. First remove dead code, redundant validators, and stub references. Then build on the simpler base."
disable-model-invocation: true
---

# Subtract Before You Add

When you change a system, remove complexity first. Then build. Use subtraction by default.

Simplify continuously. Leave the design a little simpler and more capable than you found it, behind the same or a smaller surface.

- Remove before you build.
- Cut before you polish. Get to the minimum before you put effort into quality.
- Design for the usage that you see, not for speculative edge cases.
- Do not add speculative validators, parsers, or guards that the spec does not require.
- Simplify prompts. Remove redundant instructions and too many templates.
- When a reference has no new content, delete it. Do not keep a stub.
- Do not write again what a good, well-known library does well. Use the library.
