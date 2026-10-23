---
name: principle-test-behavior-not-implementation
description: "Use when you write, change, or keep a test. Assert what users of the code can observe, so the test fails when that behavior breaks and passes when only the internals change."
disable-model-invocation: true
---

# Test Behavior, Not Implementation

A test is a claim about what the code does for its users: a caller, an end user, or a different service.
- **Behavior** is what those users can observe through the interface that they use. This includes return values, errors, state that they can read back, and effects on systems outside the code. Examples of effects are a sent request, a written row, or an emitted message.
- **Implementation** is what they cannot observe: private helpers, internal call order, intermediate data, and which internal collaborator did the work.

Judge each test against two imagined edits:

- **Break the behavior.** Make the code return a wrong value, skip an effect, or do the effect two times. If the test still passes, it proves nothing. The usual causes are:
  - an assertion that is looser than the contract
  - an expected value that the code under test calculates
  - a copied constant or prompt string that never runs the code that reads it
  - an assertion on data that the test itself made
- **Change the internals.** Keep all observable results the same, and change the structure of the code below them. If the test now fails, it is attached to the implementation. It needs a rewrite at each refactor, and it still finds no bug.

Keep a test that finds the first edit and passes the second. Rewrite or delete the other tests. To write a test that does both:
1. Run the code through the interface of its users with a concrete input.
2. Derive the expected value from the requirement, not from a run of the code.
3. Assert what the contract promises, no less and no more.

The contract decides, not the shape of the assertion:
- When the promise is "an empty cart never charges", an assertion that the payment client got no call is behavior. Add a case where the charge occurs, so that the test shows that it can see a call.
- The payload that a mocked external service receives is behavior, because that service observes it.
- A call to an internal helper is implementation, because no user can see it.
- An empty list is the exact answer when no record matches. It is an empty check when the test only needs some result.
- An exact error message attaches the test to wording that no caller reads. The error type that callers branch on is the contract.

A test can assert an invariant instead of a call, for example a key that must exist in two tables, or a compile-time type check. The invariant is the behavior.
