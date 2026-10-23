---
name: arena
description: "Spawn N parallel candidates on the same task, pick a base, and graft the strongest parts of the other candidates into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at an artifact that is not trivial can lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Before you start anything, open a todo list with one entry for each phase: Frame, Fan out, Cross-judge, Pick, Graft, Verify (Claude Code: `TodoWrite`; Codex: the plan tool).

## Phase A: Frame

Each candidate gets the same prompt, so the prompt is the contract.

1. State the artifact that each candidate makes.
2. Derive the rubric: 3–6 concrete criteria that you can grade, which tell what success is on *this* task. The rubric is the tool for the pick in Phase D. The candidates see only the task.
3. Pick the runners.
   - Use the `arena runners` line in `~/.claude/rules/pstack-models.md`. If the file or the line does not exist, use one runner on `opus xhigh` and one on `sonnet xhigh`.
   - An `auto` or `inherit-parent` entry in this line or in the cross-judge line means the parent model. Do not set a model for it.
   - If the subagent tool cannot choose a model (for example in Codex), or it rejects an entry, run that seat on the parent model and say so. The arena then gets its diversity from separate attempts, not from different models.
   - Spawn more runners when the arena covers more than one design direction.
   - Use the same model N times when the work depends on the amount of generation more than on judgment.
   - Pick each subagent's reasoning effort for the job, per the Subagents section of the **poteto-mode** skill.
4. Give each candidate its own output location, per the **separate-before-serializing-shared-state** principle skill. Use a git worktree where possible (Claude Code: `isolation: "worktree"`). Otherwise use `/tmp/arena-<slug>/candidate-<n>/`.

## Phase B: Fan out

Spawn all N subagents in one message, in the background (Claude Code subagents run in the background by default). Give each one:

- the task,
- the path to the shared grounding,
- its own output path,
- the instruction to make the artifact and a short rationale that names the alternatives that it considered and what it rejected.

If a candidate makes no output, continue with N-1 and record the dropout.

## Phase C: Cross-judge

When all Phase B candidates are complete, choose one model from the `arena cross-judge pool` line in `~/.claude/rules/pstack-models.md`. If the file or the line does not exist, choose from `opus xhigh` and `sonnet xhigh`. Prefer a model that is different from the parent model. Spawn one judge subagent on that model, and tell it not to edit files. The judge sees the rubric and the candidates by path label. It scores each criterion and recommends a base with a rationale. It runs in parallel with your reading in Phase D. Do not spawn it while the candidates still write.

## Phase D: Pick a base

Read each candidate from start to end before you pick. Score each one against the rubric, one criterion at a time, not by a general feeling. Compare your scores with the cross-judge. If you agree on the base, the pick is confirmed. If you do not agree, one of you is biased or the rubric was not clear. Read both rationales before you decide.

Pick the base that a future maintainer can extend most easily without breaking invariants. When two candidates seem equal, prefer the cleaner boundary or the smaller API, per the Laziness Protocol.

## Phase E: Graft

Read each candidate that lost one more time, and find what to port into the base. This is usually one or two things for each candidate, not most of it. Add each graft by hand, per the **redesign-from-first-principles** principle skill, so that the result stays coherent under one mental model. Do not paste mechanically.

If the candidates converge on one shape, that is strong agreement. Record it and ship the shape that they agree on. No graft is necessary. If they are very different, Phase A did not specify enough. Frame the task again and run it again. Do not average the differences.

## Phase F: Verify

Verify the synthesized artifact as you verify any other output, per the **prove-it-works** principle skill. If verification finds a problem that the arena missed, there are two possible causes:

- Phase A was wrong. Frame again and run again.
- A candidate found the problem and you missed the graft. Go back to Phase E.

Do not hide the problem.

## Outputs

One synthesized artifact, with a short synthesis note next to it. The note names:

- the base and why you picked it,
- the verdict of the cross-judge,
- each graft and its source candidate,
- what you rejected and why,
- any convergence or dropouts,
- the verification result.
