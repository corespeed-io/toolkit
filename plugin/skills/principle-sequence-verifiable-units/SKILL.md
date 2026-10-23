---
name: principle-sequence-verifiable-units
description: "Use for multi-step work (sweeps, migrations, series of similar edits) and for stacking commits and PRs. Make small units that each end in a checkable state. Check each before the next."
disable-model-invocation: true
---

# Sequence work into verifiable units

Put the work in a sequence of small units. Each unit must end in a state that you can check. Do not go to the next unit until the current one passes.

**Why:** When you find a break at the unit that caused it, it is easy to find the cause. When you find a break after a batch, the cause is hidden, and you already built more work on a broken base. When you put the same units in a delivery that a reviewer can replay, "trust me" becomes "watch it fail, then pass".

**Execution.** In a sweep, a migration, or a series of similar edits, verify each change before you start the next. Each unit is a before/after bracket:
1. Start from a known-good state.
2. Make one change.
3. Run the check.
4. Continue.

Rebase onto a clean trunk first, so that each check compares against the real baseline. When a lever does the edits, the check for each unit costs almost nothing. Run it anyway.

**Delivery.** Stack commits and PRs in the order that proves the work. The standard shape is the failing test first, then the fix on top. Other orders are:
- a subtraction before the reshape
- a baseline capture before the treatment
- the scaffold before the feature

Each commit must work alone, and the sequence must read as an argument. Make a small commit at each step that works. Do not push unless the user tells you to.

This principle adds sequencing to the **principle-prove-it-works** skill, which keeps each check real, and to the **principle-build-the-lever** skill, which makes the check for each unit cheap.
