---
name: principle-fix-root-causes
description: "Use when debugging. Trace each symptom back to the first place where the system went wrong, and fix it there. A guard is a fix only when the state it handles is legitimate."
disable-model-invocation: true
---

# Fix Root Causes

When you debug, fix the fault, not the location where it became visible. The symptom is where a wrong state became visible. The root cause is the first location where the system did something incorrect, or did not handle a state that it must handle.

**Why:** A symptom fix hides the evidence. The fault can then appear in a different location. Each symptom fix makes the system more difficult to understand, because the code now has a workaround for a bug that nobody identified.

**Pattern:**
- Reproduce the problem first.
- At each step, ask "why". Continue until the answer is a wrong decision in the code, not a consequence of an earlier decision.
- When you cannot continue, add instrumentation. Read the actual error and the actual state. Do not guess.
- Ask if the state that caused the symptom is legitimate.
  - If the system can be in that state, the code that failed on it is the root cause. The fix is to handle the state there.
  - If the state must never exist, a check where the code failed hides the bug. Find what made the state.
  - The usual ways to hide a bug are guards, retries, swallowed errors, clamped values, and discarded state.
- When a failure occurs only after a restart, suspect persisted state first: config files, caches, lock files, and serialized state.
- Find the pattern, not only the instance. Find all locations with the same fault and fix all of them.
- If a workaround needs a long comment to justify it, the code is wrong. Fix the code, not the comment.
- If you needed a deep search to find the important fact, propose a cheap signal that is always on and shows that fact immediately.
