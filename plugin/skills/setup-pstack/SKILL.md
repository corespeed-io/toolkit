---
name: setup-pstack
description: Set the model and reasoning budget that pstack uses for each role. Detects the available models and writes a model file that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or a change to pstack's model choices.
---

# Setup pstack

Write `~/.claude/rules/pstack-models.md`. This file sets pstack's model for each role. It is configuration, not memory.

- The pstack skills read this file in Claude Code and in Codex.
- Claude Code also loads each `.md` file in `~/.claude/rules/` into each new session.
- Do not put the role lines in `CLAUDE.md` or `AGENTS.md`.

## Steps

### 1. Detect the available models

List the model values that you can pass to a subagent in this session. The schema of the subagent tool is the dependable source.

- In Claude Code, the `Agent` tool lists `model` values (`opus`, `sonnet`, `haiku`, `fable`) and `effort` values (`low` to `max`). Write a real model as `<model> <effort>`, such as `opus xhigh`.
- If the subagent tool takes no model (for example in Codex, where the agent role configuration sets the model), the only valid values are `inherit-parent` and `auto`. Tell the user that each role runs on the parent model.
- If you cannot detect any model, ask the user to paste the model values that they can use.

Do not write a real model value that you did not confirm is available. The aliases `inherit-parent` and `auto` are always valid, although they are not detected values.

### 2. Load the current state

The default mapping from role to model is the file shape in step 5 below. If `~/.claude/rules/pstack-models.md` exists, read it. Use its `# budget` line and its role values as the current choices. Otherwise, start from the defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Remove it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** This is a preference decision, so ask the user. In Claude Code, use `AskUserQuestion` when it is available. Otherwise ask in plain text. Give these four options with these exact labels. Name the current budget when the file records one. If there is no file, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply the budget.** Build the working table from the skill defaults. On a run after the first, keep each role that the user changed by model, list, or alias (`inherit-parent`, `auto`).

- `unlimited`, `large`, `medium`, and `small` set the effort of each real value, panel entries included, to `max`, `xhigh`, `high`, or `medium`.
- The effort is the last token of the value. The ladder is `max` > `xhigh` > `high` > `medium` > `low`.
- If the result is not a detected value, use the highest detected effort of the same model at or below the target. If there is none, mark the role as one that needs a choice.
- `inherit-parent` and `auto` do not change.
- Example: `unlimited` changes `opus xhigh` to `opus max`. `large` keeps the defaults. `small` changes `opus xhigh` to `opus medium`.

**(c) Show the roles and confirm.** Show each role with its model. Mark each real value that is not in the detected set as one that needs a choice. Also list each line that step 2 removed. Ask whether to accept the table as it is, or to change specific roles. Give the detected models, `inherit-parent`, and `auto` as the options. `inherit-parent` and `auto` both mean that the role runs on the parent chat model. In Claude Code, use `AskUserQuestion` when it is available.

- For panel roles (`arena runners`, `architect runners`, `interrogate reviewers`), the value is a list. One subagent runs for each entry, alias entries included. The length of the list sets the count.
- `arena cross-judge pool` is also a list. Arena selects one value from it, if possible a model that is different from the parent model.
- `swarm workers` is the default model for each worker, unless a race or a comparison sets a different model for each arm.

### 4. Validate

Each real value that you write must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real value is not available, stop and ask again.

### 5. Write the file

Write `~/.claude/rules/pstack-models.md` with no frontmatter. Write the comment lines, a `# budget` line with the chosen label and its target effort, and one line for each role. Use the role labels that poteto-mode uses. Overwrite the full file, so that each run gives the same result. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Value: `<model> <effort>` (such as `opus xhigh`), a comma-separated list of these for a panel, or `inherit-parent` / `auto` (the role runs on the parent chat model; do not set a model). Alias entries in a panel list still count toward its fan-out.
# If the subagent tool rejects a model (for example in Codex), the role runs on the parent model.
# budget: large (xhigh)
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: opus xhigh
hardest tasks: opus xhigh
how explorer: inherit-parent
how explainer: opus xhigh
why investigators: inherit-parent
why synthesizer: opus xhigh
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: opus xhigh
arena runners: opus xhigh, sonnet xhigh
arena cross-judge pool: opus xhigh, sonnet xhigh
swarm workers: inherit-parent
architect runners: opus xhigh, sonnet xhigh
interrogate reviewers: opus xhigh, sonnet xhigh
```

### 6. Confirm

Tell the user that you wrote the file and that new sessions use it. A new run of this skill updates it.

### 7. Mention a verification skill (optional)

Find out whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If it does not, add one line to the final reply: "`/create-verification-skill` can generate a project-local verification skill, so that agents can drive the app as a user does and prove that changes work." Do not wait for an answer. If the user asks for it, run `/create-verification-skill`. It is in the same plugin as this skill.

### 8. Mention a formal verification skill (optional)

Find out whether the project has a formal verification skill (a project skill that runs a model checker, a proof, or a different verifier against the code). If it does not, add one line to the final reply: "`/create-formal-verification-skill` can generate a formal verification skill, so that agents can prove that a key property of your code holds in each case in scope, not only in the cases that tests reach." Do not wait for an answer. If the user asks for it, run `/create-formal-verification-skill`. It is in the same plugin as this skill.
