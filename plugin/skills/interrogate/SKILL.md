---
name: interrogate
description: "Reviewers on different models challenge a change from independent angles. Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\"."
disable-model-invocation: true
---

# Interrogate

Spawn one reviewer for each configured model to do an adversarial review of code changes. The adversarial signal comes from the different models, not from assigned personas. The deliverable is a synthesized verdict. Do NOT apply changes automatically.

If the subagent tool cannot choose a model (for example in Codex), all reviewers run on the parent model. The review still runs, but it has less model diversity. Say that in the output.

## Step 1, Scope

Find what to review from the context:

- If the user points to specific files or a diff, use that.
- If you are on a feature branch, run `git diff main...HEAD` (or the correct base branch) to get the full changeset.
- If the user's message refers to recent work, collect the related files.

Package the diff or the file contents with the context files that the reviewers need to understand the code.

## Step 2, Intent

Before you spawn reviewers, state the intent in one clear paragraph. Use the user's message, the commit messages, the PR description if one exists, and the code. If you are not sure about the intent, write your best interpretation, mark it as an assumption, and continue. Ask the user only if the change can mean two very different things and the review depends on which one.

## Step 3, Spawn reviewers

Launch all reviewers in one message. Spawn one reviewer for each entry on the `interrogate reviewers` line in `~/.claude/rules/pstack-models.md`. Label them Reviewer A, B, and so on, to match the number of entries. If the file or the line does not exist, use the table defaults.

| Subagent | Default model |
|----------|---------------|
| Reviewer A | `opus xhigh` |
| Reviewer B | `sonnet xhigh` |

Each reviewer is a general-purpose subagent (Claude Code: `subagent_type: "general-purpose"`; Codex: the default subagent). Tell each reviewer that it must not edit files. Set its model to its configured entry, or to its table default when there is no configured line, per the Subagents section of the **poteto-mode** skill. Do not set a model for an `auto` or `inherit-parent` entry. That reviewer runs on the parent model.

If the subagent tool rejects a configured entry or a table default, run that reviewer on the parent model and say so. Do not stop the review because of the model value. An alias entry is not a rejected value. Do not apply this fallback to it.

Read `references/reviewer-prompt.md`. Fill in the same template for each reviewer with:

- the stated intent,
- the diff or the file contents,
- the rubric from `references/rubric.md`,
- the code-quality lens from `references/code-quality-review.md`.

Pick each subagent's reasoning effort for the job, per the Subagents section of the **poteto-mode** skill.

## Step 4, Synthesize

When the results come back, build one picture.

- Parse the findings of each reviewer.
- Merge findings that describe the same issue in different words. Record which models found each one.
- Findings that two or more models found independently are the strongest signal.
- Read a finding from only one model, but give it less weight.
- Record disagreements. If one model flags something and another model explicitly says the opposite, that is context for the verdict.

## Step 5, Lead judgment

You are the lead reviewer. You are a practical senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put each finding in one of four buckets, with the models that found it and a one-line rationale.

- **Act on**. Real issues that affect correctness, security, or maintainability for the actual goals. They block a real PR.
- **Consider**. Valid, but you are not sure that they are worth the cost to fix now. The user must see them.
- **Noted**. Technically valid but not actionable. They depend on context, are premature optimization, or have low impact at this stage.
- **Dismissed**. Wrong, a nitpick, or missing context. Give a short reason.

## Output Format

### Intent
> [The intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet for each reviewer)

### Act On
[Each: description, which models found it, why it is important.]

### Consider
[Each: description, which models found it, the tradeoff.]

### Noted
[Short list.]

### Dismissed
[Each with a short rationale.]

### Agreement Map
[Where the models agreed and where they did not, and what that pattern tells us.]
