---
name: interrogate
description: "Adversaries try to break a change or a design, and only findings that a run proves survive. Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\"."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do NOT apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree.

State the intent with the **in-your-own-words** skill. Use the user's message, the commits, and the PR description. If you are not sure about the intent, write your best interpretation, mark it as an assumption, and continue. Ask the user only if the change can mean two very different things and the review depends on which one.

## Fan out

Run Phase A steps 3 and 4 and Phase B of the **arena** skill, with these changes:

- Read the `interrogate reviewers` line in place of the `arena runners` line.
- Copy the uncommitted changes of the scope into each worktree.
- Spawn each adversary as a general-purpose subagent (Claude Code: `subagent_type: "general-purpose"`; Codex: the default subagent).
- In place of the arena task and rationale, give each adversary the scope, the intent, and the brief below.

If the subagent tool cannot choose a model (for example in Codex), all adversaries run on the parent model. The review still runs, but it has less model diversity. Say that in the output.

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Verify each finding per arena Phase F: run its command again.

- Keep a finding when the output shows the failure and the failure breaks the intent. Drop the other findings.
- Merge findings that have the same root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps each verified finding, not the list of one adversary.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, the number of dropped findings and why.
