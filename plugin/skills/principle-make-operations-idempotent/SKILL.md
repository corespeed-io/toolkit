---
name: principle-make-operations-idempotent
description: "Use when you design commands, lifecycle steps, or processing loops that run with crashes, restarts, and retries. Each run must converge to the same end state, after any partial earlier run."
disable-model-invocation: true
---

# Make Operations Idempotent

Design operations so that they converge to the correct state. The number of runs and the point where the last run stopped must not change the result. Each operation that changes state must answer these questions: "What occurs if this runs two times? What occurs if the last run crashed halfway?"

**Why:** Commands, lifecycle operations, and processing loops run where crashes, restarts, and retries are normal. If partial state changes the result of the next run, each restart becomes a debugging session.

**The idea:** derive each step from the state that exists, not from what the last run tried to do.
1. Read the current state.
2. Compare it to the goal.
3. Apply only the difference.

A step of this type is safe to repeat, because a repeat finds no work to do.

The next run must be able to identify as stale anything that a run leaves: a lock, a temporary file, a half-written record, or a claimed job. Judge staleness with evidence that stays true at all points where the last run can stop, not only in the usual case. If the next run cannot judge a marker, each crash causes manual cleanup. For example, write to a temporary path and rename it into position. Or compare artifacts by content, not by creation order.

**The test:**
1. What occurs if this runs two times in sequence?
2. What occurs if the last run crashed at each possible point?
3. Does the next run converge to the same end state?

If an answer is "it depends on the state that the last run left", the operation needs a reconciliation step.
