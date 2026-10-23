---
name: create-formal-verification-skill
description: "Make a project-local skill that formally verifies the code where a bug costs most and tests reach least, in any language and tool. Use for /create-formal-verification-skill, \"model-check this race\", \"prove this invariant\", or concurrency, retries, state machines, parsers, or unsafe code."
disable-model-invocation: true
---

# Create a formal verification skill

A test checks the cases that a person thought to write. Formal verification checks all cases in a stated scope: each order of steps in a model, each input up to a bound, or each input. This skill does these tasks:

1. It finds the part of the repo where formal verification is most important.
2. It verifies one property of that part.
3. It makes a project-local skill. With that skill, the next agent can check a change against that property.

Write that skill for an agent that reads it for the first time, during a change, and that never saw your work. The user must be able to trust the result and act on it without learning the verification language.

## Choose the target from the code

Get the answers from the codebase. Ask the user only for what you cannot see. If the user named an area or a bug, start there.

A good target is a promise of the code with these properties:

- A break causes harm to users.
- Tests do not usually get to the case that breaks it.

Choose the strongest such target in the repo, not the target that is easiest to verify.

## Let the question choose the tool

Choose the tool that answers the question at the lowest cost: a model checker, a proof assistant, an SMT-backed verifier, or a different tool.

- Can events occur in a bad order? Usually, a model checker over a small model of the design is correct for this. TLA+ is the default for this, in any language.
- Does the code itself behave correctly for each input? Examples are memory safety, overflow, or a data-structure invariant. Usually, a verifier that runs on the code is correct for this.
- If no verifier runs on this language, say so. Then test the real code with generated inputs, not with a hand model of the function.
- A property that must be true at each size, where a bound is not sufficient, can need a proof.

Prefer a tool that the developers of the repo can install and run. Tell the user why you chose it.

## What makes it good

- **True to the code.** Each part of the model or proof points to code that a reviewer can open. A step that the verification treats as one indivisible step is one indivisible step in the code. Names come from this repo.
- **Able to fail.** A check that you never saw fail proves nothing. Show that each property fails on a broken variant of the code that it guards. Examples are a removed check or a step in a different order.
- **Findings stay findings.** If the current code breaks the property, report it with the counterexample in the terms of the code. Do not make the property or the model weaker until it passes. Do not change product code unless the user asks.
- **Honest about scope.** Say what is verified, under which bounds and assumptions, and what is not included. A pass covers the model or the bound, not the full system.
- **Readable without the tool.** State the property in one plain sentence, and the harm in one plain sentence. Tell a counterexample as a short sequence of steps in the words of the code.
- **Cheap to run again.** One command, a reproducible tool version, and a run that is short. Then the next agent uses it on each related change.
- **In step with the code.** Record which files and functions each check covers. Record the commit at which you last confirmed that the verification describes them. When the covered code changes after that commit, the next agent can see that the verification needs a new check.

## Make the verify skill

Write a project-local skill in the project skills directory of the tool: `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex). If the repo uses both tools, write it in one directory and add a symlink in the other. Give it frontmatter that names the area and says when to use it. Without frontmatter, the skill does not register.

With only the skill, the next agent must be able to do these tasks:

- Tell whether a change touches the verified code.
- Run the check.
- Tell a real bug from a modeling error.
- Update the verification when a change is intentional.

Put the coverage record and the sync commit in the skill. Tell the next agent to move the sync commit forward only after it confirms that the verification describes the code at the new commit. Use the real commands, paths, and nouns of this repo. Do not leave placeholders.

## Prove it before you give it to the user

1. Follow the new skill one time, as the next agent does, on a scratch change that breaks the property in the real code. The skill must find the break.
2. Remove the scratch change.
3. Confirm that the check is back at its start state: it passes, or it fails only on the findings that you will report.

A verify skill that nobody ran is a draft. If the skill does not find the break, or a step does not run, fix the skill or the verification. Do not change the scratch change.

## Give it to the user

Tell the user these items:

- What you verified.
- Which tool you used, and why.
- The bounds.
- What the check found, in plain words.
- How to run it.
- What it does not cover.

Suggest a second target only if you found a close one. Tell the user to use `/maintain-formal-verification-skill` to bring the verification back in line after changes that did not check it again.
