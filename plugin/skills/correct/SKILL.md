---
name: correct
description: "Find the mistakes that agents repeat in this repo and make each one impossible: architecture, then types, then a lint that names the fix, then a test, then docs. Prove each check fails on a real past mistake. Use for /correct, and each time the operator corrects you."
disable-model-invocation: true
---

# Correct

The operator corrects agents in this repo for the same mistakes again and again. Change the repo so that the next agent cannot make them.

Assume that each contributor is an agent with these properties:

- It sees only the files that it opened.
- It copies the nearest example.
- It takes the shortest path that compiles.

Design the repo so that a change that looks correct from one file is correct for the full repo.

## Find the mistake classes

1. Read the recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds.
2. Put the mistakes into classes. A class counts when it occurred two times.

## Fix each class at the highest level that works

1. **Remove it with architecture.**
   - Give each piece of state one owner, and each task one supported method.
   - Hide internals, so that the wrong import fails.
   - Replace lists that people keep in sync by hand with one source of truth.
   - Delete old methods and dead code that an agent can copy.
2. **Enforce it with types, so that nobody can write the bad state.** If bad code still compiles, add a lint or CI check. Its error must name the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more of it.
3. **Test the behavior.** Fix or delete a test that still passes when its behavior breaks. Do the same for a test that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent ignores them.

## Fix and prove

1. Fix the most frequent classes now, one commit for each class.
2. Prove that each new check fails on a real past mistake.
3. Run the same command locally and in CI.
4. Put each exception on the line that breaks the rule. Include a reason, an expiry date, and the approval of a human.

## Keep the rule table

Keep a table in the agent instruction file. The table pairs each rule with the thing that enforces it.

- When the operator corrects you, fix the mistake and add the rule.
- If the rule was already in the table and nothing enforces it, the mistake is a repeat. Fix it at the highest level in the same change.
- Remove a rule when its mistake cannot occur.

**Reply:** each class with its evidence, the level that you selected, and why a higher level did not work.
