---
name: swarm
description: "Fan out N parallel workers, collect their results, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

## Start

Before you start anything, open a todo list with one entry for each phase (Claude Code: `TodoWrite`; Codex: the plan tool).

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report that the swarm must return.
2. Choose the shape. Divide the work into slices, race N workers on the same brief, or mix the two. For a race or a mixed shape, declare `first pass`, `rank all`, or `best-of` before you spawn.
3. Pick the worker model from the `swarm workers` line in `~/.claude/rules/pstack-models.md`. If the file or the line does not exist, use `inherit-parent`.
   - For `auto` or `inherit-parent`, do not set a model. The workers run on the parent model.
   - If the subagent tool cannot choose a model, or it rejects a value, use the parent model and say so.
   - For a model race, name the model of each arm before you start. A model race needs a tool that can choose a model for each subagent (for example Claude Code).
   - Pick each subagent's reasoning effort for the job, per the Subagents section of the **poteto-mode** skill.
4. Give each worker that writes its own writable output.
   - When workers verify or measure commits, each brief names the exact SHAs.
   - A measurement brief also names the method (sample count, what one sample is, order).
   - The worker records the SHAs and the method in its result.

## Phase B: Fan out

Spawn all N workers in one message as general-purpose subagents (Claude Code: `subagent_type: "general-purpose"`; Codex: the default subagent). Run them in the background (Claude Code subagents run in the background by default). Set the model from step 3, or do not set it for `auto` or `inherit-parent`.

- Give each worker its own checkout. In Claude Code, use `isolation: "worktree"`. Otherwise, create a git worktree for each worker before the spawn.
- If the tool can run a subagent on a remote machine, you can use that for a worker that does not need the user's computer.
- When a worker must start from a pushed branch that is not the default, tell it to check out that branch first.

Each brief must stand alone. Include the goal, the scope, the exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED`, with evidence. A worker that can prove a defect reports `ISSUES` and lists each issue that it can prove, not only the first.

If a worker drops out, continue with N-1 and record it.

## Phase C: Aggregate

Read the final results.

- Discard a result that does not record the SHAs and the method that its brief names. Spawn that worker again one time. After a second miss, record a gap. A gap is not a pass.
- For coverage, each required slice needs a result.
- For a race, apply the selection rule that you declared at the start: first pass, rank all, or best-of.
- Do not paste the raw output of the workers.

## Phase D: Report

Return one consolidated report in the chat. Include the table, a one-line summary of each issue, the gaps or dropouts, and the race rule when you used one.
