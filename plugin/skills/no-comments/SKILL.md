---
name: no-comments
description: "Start Comment Sicko to find comments to delete, fix the accepted findings, and offer to encode claimed constraints in code. Keeps only comments that explain a why the code cannot make clear."
disable-model-invocation: true
---

# No comments

Start Comment Sicko. Act on the findings that you accept.

Give priority to the new view of Comment Sicko.

**Rule from AGENTS.md:** Write a comment only for a "why" that the code does not make clear. This rule wins over Comment Sicko. If a comment explains a "why" that no rename, extract, type, or test can make clear, keep it. If a reshape can make the "why" clear, do the reshape and delete the comment.

## Scope

Use the files or diff that the caller gives. If there are none, use the current diff against the base branch (default `main`), including the working tree.

## Steps

1. Start the `comment-sicko` subagent and give it the scope. Do not restate its rules.
   - Claude Code: use the Agent tool with `subagent_type: "comment-sicko"`.
   - Codex, or a tool that cannot start that agent type: start a general subagent with the instructions in [`agents/comment-sicko.md`](../../agents/comment-sicko.md) of this plugin. If the tool has no subagents, do the review yourself with those instructions.
   - If the tool lets you, choose the model and reasoning effort of the subagent for this task, as the Subagents section of the **poteto-mode** skill says.
2. Examine its report and diff.
   - Reject these items: edits to application code, edits outside the scope, deletions that an exception protects, `MUST KILL` reasons that are not correct, and flags that treat kept intentional code as guilty.
   - Reshape flags on surprises in our own code stay actionable. Do not restore those comments.
   - A keep stays only with proof that it is about something that we cannot change, or about a "why" that the code cannot make clear (the AGENTS.md rule).
   - Audit scoped lint and TypeScript suppressions that it did not flag. Suppressions for correctness or safety stay actionable `MUST KILL`s.
   - Restore a deletion only with an exact exception and scoped proof.
   - Before you accept a thin `IMPORTANT` or `do not remove` kill or keep, run `/how` or `/why` on its symbol.
   - If a kill is ambiguous, do not restore the comment. If a keep is refuted or still ambiguous, delete it.
   - If you reject a report, revert it and run it again one time, with the failure named. If you reject a second report, report it as open, and fail `/no-comments`.
3. Fix trivial accepted flags directly: delete a dead path, remove a parameter, or use the real API. If a fix needs a new shape, run `/architect` one time for the accepted set and the code around it. Stop at the sketch. Architect makes the shape. Step 4 implements it.
4. Implement the smallest root-cause fix in the scope. Remove each named workaround.
   - If the root cause is outside the scope, land the smallest fix in the scope and report the remainder as open.
   - The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills give only the intent. Neither lets you make the scope wider or fix instances outside it.
   - Never add guards that only hide a symptom.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`.
   - Keep the comments about things that we cannot change.
   - For the others, offer the cheapest type, runtime check, test, or CI lint in the scope.
   - In an interactive session, wait for approval. An unattended run or an eval needs approval from the caller before the run.
   - If you get approval, encode the constraint, then delete the comment. If not, delete the comment, report the constraint as open, and sketch the work outside the scope.
6. Report the deletion count, restored comments, runs again, the architect sketch, fixes, encoding offers, encodings, constraints that nothing enforces, and other open work.
