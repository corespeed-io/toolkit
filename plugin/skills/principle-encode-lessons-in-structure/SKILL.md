---
name: principle-encode-lessons-in-structure
description: "Use when you write the same instruction a second time, or see a recurring correction. Encode the rule as a lint, metadata flag, runtime check, test, or script, not as more text."
disable-model-invocation: true
---

# Encode Lessons in Structure

When you write the same instruction a second time, or you see the same correction again, encode the rule in structure. Use a lint rule, a type, a metadata flag, a runtime check, a test, or a script. Do not add more text.

If the lesson needs judgment and you cannot encode it, make the instruction more prominent. Add an example of the failure mode.

**Corollary:** If the fix is structural, use only the structural fix. The instruction is the symptom.

**Durable lessons that are not code:** save a durable decision, convention, or failure fix in memory. Search memory first, then save it, or update the memory that already covers it. Do not write lessons to local memory files or rules files.
