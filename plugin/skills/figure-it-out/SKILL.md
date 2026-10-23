---
name: figure-it-out
description: "Design an auditable playbook when no narrower one fits: a large migration, a large multi-part change, or work that a human reviews later. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'."
disable-model-invocation: true
---

# Figure it out

If no playbook matches the task, design one. Before any code, the deliverable is the workflow itself. The workflow is a sequence of phases with these properties:

- Its rigor agrees with the task.
- It uses the scientific method.
- It leaves a decision trail. A human can audit the trail after a period away.

## Start

Make a todo list. The first item is to read the Principles section of the **poteto-mode** skill. Then add the phases below as todo items.

## Phase A: Frame

Get the facts first, then commit. Do not start the run until you can state these items:

- The definition of done, as a predicate that a test can show to be false (the **prove-it-works** principle skill).
- The scope, with numbers: approximate units and effort, and the blockers that you found.
- The rigor level. Choose a high level when you are not sure.
  - A decision that you cannot undo, or a large blast radius, gets more rigor.
  - A step that you can undo and that has low risk gets less rigor.
  - Rigor means gates and artifacts, not "try harder".

Show the framing and the tradeoffs before you commit to a long run. Continue with work that you can undo (the **never-block-on-the-human** principle skill). But a run of many hours gets one checkpoint with the user.

## Phase B: Design the workflow

Divide the work into atomic units. Each unit must be able to land independently. Do the unit with the riskiest unknown first. Do scaffolding and verification before features (the **foundational-thinking** principle skill).

- Build the verification harness before the work. Capture the baseline from the state before the change. Then the check reads as "old value vs new value".
- For a design decision that you cannot undo, run the **architect** skill (it runs **arena**). Do not run it for mechanical work whose shape is already clear. A second arena over a design that is already decided is over-engineering (the **laziness-protocol** principle skill).
- Decide which work goes to parallel workers. Do work in parallel only across seams. Give each worker its own worktree or branch (the **separate-before-serializing-shared-state** principle skill). Do not use too many workers. If the tool lets you, choose the model and reasoning effort of each subagent for its task, as the Subagents section of the **poteto-mode** skill says.
- Write down the phase list that you designed. The human reviews that list.

Then do the design:

1. Add its steps to the todo list as concrete items, between the Phase C and Phase D items.
2. Run each step with the loop discipline of Phase C.
3. Add a row to the Phase D log as each step lands. Do not keep the full trail until the end.

## Phase C: Run the loop

Each unit is an experiment:

1. State the hypothesis.
2. Make the smallest change.
3. Measure the real artifact against the predicate.
4. If the change moved the work forward, keep it. If not, revert it.

Apply the **sequence-verifiable-units** principle skill. Verify each unit before you start the next. Do not keep all checks until the end.

- Verify by inspecting the artifact. Never trust a self-report. If something passes too easily, examine the observation method before the system.
- Pair delegated work with a judge. If a worker games the gate, reset and make the contract stronger. If the gate itself is wrong, fix the gate in a separate change. Do not go around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Do not hide a negative result.

## Phase D: Keep the audit trail

Log the run with the **show-me-your-work** skill. The work of figure-it-out is usually large. Thus, commit the trail so that the reviewer can read it in the PR. The trail and the diff let the human come back and trust the work.

## Phase E: Verify and give back

Check the full result against the Phase A predicate on the real product, not only the harness. Encode each correction that occurs again as a gate, a lint rule, a check, or a script (the **encode-lessons-in-structure** principle skill).

**Reply:** the playbook that you designed, the rigor level and why, the path of the decision trail, what is verified against the predicate, and what is still open.
