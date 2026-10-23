---
name: architect
description: "Sketch types, signatures, and module structure before code, then stay in the loop while the implementation fills in. Use for /architect, 'architect this', 'design this', or work that is not trivial where code first would lock in the wrong shape."
disable-model-invocation: true
---

# Architect

Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across the views of more than one model when the subagent tool can choose a model. Then write the code against the chosen sketch.

To run another pstack skill, read `../<name>/SKILL.md` from this file and follow it.

## Start

Open a todo list with one entry for each phase before you start (Claude Code: `TodoWrite`; Codex: the plan tool).

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

Build a real mental model of each system that the new code touches. Run the **how** skill over the related subsystems. A file name is not grounding. Write the architecture explanation that `how` specifies. If the design changes ownership or layering, also run the **why** skill on the existing shape. Then the rationale becomes a constraint, not a guess.

Skip Phase A only when the work is truly new and has no surrounding system to integrate with.

## Phase B: Sketch

Run the **arena** skill with the design-sketch task and the grounding artifacts from Phase A. Give `references/runner-prompt.md` to each runner as its prompt.

Take the runners from the `architect runners` line in `~/.claude/rules/pstack-models.md`, not from the `arena runners` line. If the file or the line does not exist, use `opus xhigh, sonnet xhigh`. Alias entries and rejected entries follow the runner rules in Phase A of the **arena** skill.

Design it twice. Get a minimum of two candidates with different structures before synthesis, also when the first looks sufficient. This is the **exhaust-the-design-space** principle skill in practice. The alternatives are different whole shapes, not point fixes inside one shape.

Check each candidate against [`references/design-red-flags.md`](references/design-red-flags.md) before synthesis. Assume that the next contributor is an agent that sees only the files that it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks correct from one file is correct for the full repo.

Compare the candidates that can work by interface depth. Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short, because it puts the capability in one place and does not scatter it across layers.

Arena returns one synthesized design package. Its synthesis decision fills the "Synthesis decision" section of the rationale.

## Phase C: Agree (opt-in)

By default, go directly to implementation with the synthesized design. There is no human checkpoint.

Use a checkpoint only when the invoker asks for it: "/architect with checkpoint", "stop and show me before implementing", or similar. Then show the synthesized design and wait for approval.

In both cases, the synthesis can ship as its own commit. This is the "scaffold first" mode of the **foundational-thinking** principle skill. Planned breakage with a known scope during the fill-in is acceptable, per the **outcome-oriented-execution** principle skill. To put adversarial pressure on the design before implementation, run the **interrogate** skill on the synthesized sketch.

If the human disagrees with the shape (at a checkpoint or later), treat that as Phase A evidence. Ground again and run Phase B again before you write more code.

## Phase D: Implement against the sketch

Replace the `not implemented` bodies with code, and the pseudocode with logic. The synthesized sketch is the contract. A deviation from it is a signal to show, not friction to absorb silently. If a function needs a parameter that the sketch did not expect, ask yourself which is true: the sketch was wrong, the requirement was missed, or the implementation does too much.

## Phase E: Scrap when the architecture is wrong

If the implementation continues to cause friction that the sketch cannot absorb, discard the sketch. Do not add fixes to a wrong design, per the **redesign-from-first-principles** and **fix-root-causes** principle skills.

The signal is a *pattern*, not single instances. Signs:

- The same shape of workaround occurs again and again across unrelated code.
- Many unrelated edge cases each need a special-case branch.
- Types need escape hatches (`any`, casts, optional fields that are always set in practice) to compile.
- You want to add a lock, but the sketch said that the state was not shared.
- Callers must know the internal rules of the abstraction to use it.
- Two or more independent Phase D deviations have the same shape across the implementation.

Use judgment. Some edge cases do not mean that an architecture is wrong. Some problems are truly complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Run the **how** skill again over what you built.
2. Redesign as if the new constraints were assumptions from the first day, per redesign-from-first-principles.
3. Subtract before you add, per the **subtract-before-you-add** principle skill. The new sketch must be smaller than the old one before it grows.
4. Go back to Phase B and run arena again.

## Outputs

Write the caller's usage first, and derive the type sketch from it.

- For a small change: one file with the new types and signatures.
- For larger work: a module map and the type definitions.

The rationale ships with them, in the shape of `references/rationale-template.md`. It includes the usage sketch and the synthesis decision.
