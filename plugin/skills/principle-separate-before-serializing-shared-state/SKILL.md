---
name: principle-separate-before-serializing-shared-state
description: "Use when concurrent actors can write the same file, branch, key, or state object. Remove the sharing first. Serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate Before Serializing Shared State

When concurrent actors can share mutable state, first ask if they need the same mutable object. If not, remove the sharing. When the sharing is real, enforce serialization in the structure: lockfiles, sequential phases, exclusive ownership. Instructions and conventions are not concurrency control.

**Why:** Concurrent writes to shared state cause race conditions. These are intermittent, difficult to reproduce, and expensive to debug.

**Pattern:**
1. **Identify shared mutable state.** Examples: files that two actors read and write, branches that two actors push to, APIs that one actor defines and another consumes.
2. **Default: remove the shared write target.** Ask: "Do these actors need one canonical object, or do they publish independent facts?" Give each actor its own file, key, branch, or state directory. Merge only at the read or report boundary. Two workers that write their own `lastX` field into one `state.json` is still shared mutation. `indexer-state.json` + `metrics-state.json` is not.
3. **Serialize access in the structure only when one shared write target is a real invariant.** Use lockfiles, sequential phases, a single-writer actor, or atomic compare-and-swap. "We need a lock" is a sign of a possible design problem. Examine it. Do not use it as the default answer.
