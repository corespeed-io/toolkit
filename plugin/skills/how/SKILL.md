---
name: how
description: "Explains how code works: \"how does X work\", code walkthroughs before a change, and placement, ownership, or layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Write architecture explanations at the level of a senior engineer who joins a subsystem. Give enough to build a working mental model. Do not write so much that it reads like annotated source code.

Each spawn is a general-purpose subagent (Claude Code: `subagent_type: "general-purpose"`; Codex: the default subagent). Tell each subagent that it must not edit files. After the subagents finish, run `git status` to make sure that they did not edit files.

Models:

- Explorers use the `how explorer` line in `~/.claude/rules/pstack-models.md` (default `inherit-parent`).
- Each explainer uses the `how explainer` line (default `opus xhigh`).
- If the file or the line does not exist, use the default.
- Set the model and the effort per the Subagents section of the **poteto-mode** skill. That section also tells what to do for `auto`, `inherit-parent`, a tool with no model choice, and a rejected value.

## 1. Assess the complexity

If the scope is not clear, state your interpretation and explore. The user can redirect you.

- **Simple** (one module, a small utility, or a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass. Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem across many files or services, a cross-cutting feature, or a full architecture overview): go to step 2.

If you are not sure, use the simple path.

## 2. Explore (complex only)

Divide the question into 2 to 4 angles. Each angle is a different slice of the subsystem. Spawn all explorers in one message. Give each one `references/explorer-prompt.md` with its angle filled in.

## 3. Synthesize (complex only)

When all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and the findings of each explorer filled in.

## 4. Present

Present the output of the explainer. You can make light edits for clarity or for context from the conversation. Do not rewrite it much.

## Output format

The explanation uses the sections in `references/explainer-prompt.md`: Overview, Key Concepts, How It Works, Where Things Live, Gotchas. Remove a section that does not apply.
