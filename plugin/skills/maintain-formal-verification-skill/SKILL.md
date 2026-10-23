---
name: maintain-formal-verification-skill
description: "Bring formal verification back in line after the code changes: find commits that touched verified code, update the model, harness, or properties, run again, and tell drift from bugs. Use for /maintain-formal-verification-skill, \"is the model still true to the code\", or after merges and refactors."
disable-model-invocation: true
---

# Maintain a formal verification skill

A formal check proves a property of what it describes. If the code changes and the verification does not, the check can continue to pass while it describes code that does not exist now. That pass is the dangerous case, because it looks like a proof.

This skill is the maintenance loop for these skills:

- A verify skill that `/create-formal-verification-skill` made.
- A project-local skill that runs a model checker, prover, or code-level verifier against named code.

The project-local skill handles a change that an agent makes while it uses that skill. This skill handles the changes that did not use it: merges, edits made without the skill, and drift that collects across many commits.

## Outcomes

Give each check one outcome, and say which:

- **in sync**: No change since the last sync changes what the check describes, and the check passes.
- **updated**: The code changed. The verification now describes the new code, and the check passes.
- **bug**: The verification describes the current code, and the code breaks the property. This is a finding about the code. It is not drift.
- **blocked**: You could not bring the check back in line, or the check could not run. Say exactly why.

A check can be both updated and bug. The update makes the verification describe the code again, and then the property fails on the code.

## Edit scope

Edit only the verification: models, harnesses, property files, and the verify skill itself. Never edit product code during a run, unless the user tells you to. If a property fails on the current code, do not make the property or the model weaker to make it pass. Report the failure.

## Pass

1. **Find the checks.** A verify skill has no fixed name. Find it by what it does: a project skill that runs a model checker, a prover, or a different verifier against named code. Look in the project skills directories (`.claude/skills/`, `.agents/skills/`).
   - Read each one that you find, or the one that the user named.
   - For each check, collect the property, the code that it covers, the bounds and assumptions, the command that runs it, and the commit where somebody last confirmed that it describes the code.
   - If no verify skill exists, stop. Tell the user to use `/create-formal-verification-skill`.
   - If the skill does not record a sync commit, use the last commit that changed the verification files. Say that you did this.

2. **Run it as it is.** Run each check one time before you change anything. Record the result.
   - A pass here does not tell you that the code is correct. It tells you that the old description is still true.
   - A failure here can be drift or a bug. Do not decide which until step 5.

3. **Read each change to covered code.** Diff the covered files from the sync commit to the current commit. Read each commit message.
   - Also look for code that moved. A covered function that has a new name, is divided, or is in a different file is still covered code.
   - Also look for new code that touches the state that a check guards, for example a new function that writes the same fields.

   For each change, decide which type it is:
   - **No effect.** The change does not change anything that the verification describes. Examples are formatting, comments, or code paths that the verification does not cover. Check this against the model or harness, not against the commit message.
   - **The verification does not describe the code now.** A step that was one indivisible action is now two. A branch was added or removed. A check moved. A new path gets to the guarded state. A value now has a different range. The model or harness must change.
   - **The promise changed intentionally.** The change changes what the code promises, and evidence in the change says that this is intentional. The evidence is the doc comment, the tests, the changelog, or the commit message. The property must change, and you must cite that evidence.
   - **The promise is possibly broken.** The code changed, and no evidence says that the promise changed. Treat a failure that follows as a possible bug.

4. **Update from the code, not from the result.**
   - Change the model or harness so that each changed part again points to code that a reviewer can open.
   - Keep one indivisible step in the code as one step in the verification.
   - Write the update from the code before you run again. Do not change it to make the check pass.
   - Change a property only for a promise that changed intentionally. Write down the old wording, the new wording, and the evidence.
   - Keep the bounds unless the change makes them wrong. If you must make a bound smaller, say so in the report.

5. **Run again and judge each result.**
   - **Pass:** The check can now pass on a description that cannot fail. Break the new code in the way that the property guards against. For example, remove a new check or change the order of a new step. Confirm that the check finds the break. Then remove the break.
   - **Fail:** Replay the counterexample against the real code, step by step.
     - If a step cannot occur in the code, the verification is wrong. Fix the verification, and say what was wrong.
     - If each step can occur, it is a bug. Name the commit that caused it. Tell the counterexample as a sequence of steps in the words of the code. State the harm in one sentence.
     - If a cheap test or reproduction against the real code shows the bug, add it to the report as evidence. Do not commit it to the product code.

6. **Update the verify skill.**
   - Update the code that each check covers, the commands, the bounds, the assumptions, and the sync commit.
   - Set the sync commit to the commit that you checked.
   - Do not move the sync commit for a blocked check. Say so in the report.
   - Then follow the verify skill one time as the next agent does, to make sure that its steps still run.

## Report

Tell the user these items for each check:

- the outcome, and the commits that you read;
- what changed in the verification and why, with a short reason for each change: the code changed shape, or the promise changed intentionally (with the evidence);
- the result of the new run, and the break that showed that the updated check can still fail;
- each bug, in plain words: the counterexample as steps in the words of the code, the harm, and the commit that caused it;
- what the verification still does not cover, including new code that it must cover and does not.

Say clearly which failures were drift in the verification and which were bugs in the code. If a check passed before your update and fails after it, say that the old pass was on an old description.

Put the verification updates in a separate commit, not in the same commit as a product fix. If you are on `main` or `master`, make a branch first. Do not push unless the user tells you to.
