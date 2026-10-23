---
name: tdd
description: "Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has a clear, cheap local test target. Do not use when the test path is not clear, is expensive, needs much integration, or nobody asked for it."
disable-model-invocation: true
---

# TDD Bug Fix

When you fix a bug that has a clear, cheap test path, make the broken behavior executable before you change production code. The goal is a focused regression test that fails before the fix and passes after it.

Do not force a test if it is not practical. Do not add a new test if it needs one of these:

- a large harness setup
- brittle mocks
- slow end-to-end infrastructure
- state that only production has
- reproduction steps that are not clear
- many changes to fixtures that are not related

In these cases, use the nearest useful verification instead.

## Workflow

1. **Understand the bug.** Find the intended behavior, the current behavior, the affected path, and the smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the nearest unit, component, integration, or regression test that the codepath already uses. If no practical test path is clear, do not create one from zero only to follow this workflow.
3. **Write the failing test first.** Add the smallest focused test that finds the bug. The test must encode the intended behavior. It must not copy the current implementation.
4. **Run the new test before you fix the bug.** Make sure that it fails for the intended reason. If it passes, or fails for a reason that is not related, correct the test or the reproduction before you edit the implementation.
5. **Fix the bug.** Make the smallest production change that gives the intended behavior. Keep the nearby contracts.
6. **Run the regression test again.** Make sure that the test now passes.

## If a failing test is not practical

Use the nearest executable regression check instead: a targeted script, a manual reproduction command, browser automation, a snapshot comparison, a log assertion, or a focused integration check.

No new test is better than a bad test. A bad test has one of these properties:

- It tests mostly mocks.
- It encodes details of the current implementation.
- It depends on timing or on global state that is not related.
- It needs expensive infrastructure for a small fix.
- You will delete it immediately after it proves the fix.

## Guardrails

- Do not change tests only to agree with a wrong implementation.
- Do not make existing assertions weaker, unless the expected behavior really changed and the reason is clear.
- Keep the regression test focused on the bug. Do not make large changes to fixtures or add coverage that is not related.
- If the bug is flaky, make the test deterministic where possible. Write down the signal that the test locks.
- If the bug shows a larger class of failures, first land the focused regression path. Then think about more coverage for the related cases.

## Final response

Report the evidence, not only the result:

- Name the test or executable check that failed before the fix, and the failure that it gave.
- Name the test run that passed after the fix, and each nearby validation that you did.
- If you could not show a failure before the fix, say why. Describe the nearest regression check that you used instead.
