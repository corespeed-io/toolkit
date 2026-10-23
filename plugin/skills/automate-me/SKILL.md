---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", or to capture the user's preferences or working style in a skill. Writes or revises a personal -mode skill with skill-creator and unslop, and can mine recent transcripts for evidence."
disable-model-invocation: true
---

# Automate me

This skill is a guided flow. It changes the working conventions of the user into a skill that agents follow. The output is one `-mode` skill for the user (for example, `jay-mode` or `priya-mode`).

This skill puts three other parts in sequence. It does not replace them:

- A mining pass, in this skill (step 1).
- The **skill-creator** skill, for authoring.
- The **unslop** skill, for prose discipline.

## Flow

### 0. Look for an existing skill

Look recursively for a `*-mode/SKILL.md` that matches the handle of the user. Look in these locations:

- Project skills: `.claude/skills/**/` (Claude Code) and `.agents/skills/**/` (Codex).
- Personal skills: `~/.claude/skills/` (Claude Code) and `~/.codex/skills/` or `~/.agents/skills/` (Codex).
- Plugin skills that the user maintains, if the user names a plugin repo.

A mode skill can be in a personal category directory (for example, `.claude/skills/<handle>/`), not only at the top level.

If a mode skill exists, ask the user which action to do. Do not ask if the user already said "update my skill" or a similar phrase. The options are:

- Update the existing skill. This is the default for a repeat run.
- Start a new skill. This is rare. Ask why before you do it.

Update mode changes the remaining steps:

- Step 1 mines only the history after the last edit of the skill (`git log -1 --format=%cI <path>`).
- Step 2 asks what changed or what is missing. It does not ask what to capture from zero.
- Step 4 edits the existing file in place. Keep the sections that the user did not contradict. Revise the sections that have new evidence. Add a new section only for a rule that is really new.

### 1. Mine the history of the user

Find the transcripts of the active workspace before you start subagents. Read only the transcripts of this workspace:

- Claude Code: `~/.claude/projects/<slug>/*.jsonl`. `<slug>` is the workspace path with each "/" changed to "-".
- Codex: `~/.codex/sessions/**/rollout-*.jsonl`. Use only the files whose session metadata `cwd` is this workspace.

Do not read transcripts of other workspaces. They are private chats from projects that are not related.

Look for patterns that occur again and again in recent agent conversations in that scope. Do these steps:

1. Divide the history into slices. For example, divide the last 2–4 weeks into 3 slices, so that each slice has sufficient material.
2. Give each slice to one mining subagent, in parallel, if the tool has subagents. If it does not, mine each slice yourself.
3. Give each subagent the workspace transcript path. The subagent looks for the signals below. It returns a short structured list of patterns, with a pointer to the evidence for each.

Look for these default signals:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, special workflows, parallel work)
- Verification posture (what "done" means, unit tests or live repro, reviewers)
- Code and prose discipline (style, principles that the user cites, lint and format tools)
- Process conventions (worktrees, commits, PRs, review and merge tools)
- Meta preferences (fixing skills during a task, proposing new skills)

Compare the slices before you accept a signal. A pattern that occurs in 2 or more slices has high confidence. A signal that occurs in only one slice is weak. Usually, drop it.

### 2. Ask the user directly

Mining does not find intent that did not come up yet. Ask the user multiple-choice questions. Use a structured question tool if the tool has one (Claude Code: `AskUserQuestion`). Otherwise, ask in chat with numbered options.

Use this shape:

1. Ask one or two questions with 4–6 options each. Let the user select more than one option for a category question.
2. Start with a broad question ("Which areas are most important?").
3. Ask about the selected areas with specific options.
4. After the structured rounds, ask one free-form question in chat. This finds the items that the options did not include.

Do not ask 20 questions.

### 3. Put the findings into groups

Put the combined signals into sections. Use only the sections that apply. These are the usual sections:

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to use when you scope or investigate a change.
- **Subagents**: default, parallel work, which model for which task, special workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review and merge tools.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **poteto-mode** skill shows the shape. Read it to see the level of detail. Do not copy its content. The rules of the user are not the same as the rules of poteto-mode.

### 4. Write the skill

Use the **skill-creator** skill to write the skill. Use these rules:

- Path: keep the category of an existing mode skill. For a new mode skill, use `<skills-dir>/<handle>/<handle>-mode/SKILL.md` if the repo has a personal category for that handle. Otherwise, use `<skills-dir>/<handle>-mode/SKILL.md` in the project. `<skills-dir>` is `.claude/skills` (Claude Code) or `.agents/skills` (Codex). If the user prefers a personal skill, use the personal skills directory from step 0.
- Handle: the first name of the user, or the identifier that the user chooses.
- Frontmatter `description`: trigger on the name of the user, `/<handle>-mode`, and "work in their style". Do not trigger on general keywords such as "write code" or "review PR".
- Frontmatter format: follow the YAML rules of `skill-creator`. Keep `description` as one YAML scalar. Put it in quotes, or use `description: >-` with indented continuation lines, if punctuation or line wrap makes this necessary.
- Frontmatter `disable-model-invocation: true` is the default. Remove it only if the user explicitly wants the mode to apply on each turn. Claude Code uses this key. Codex ignores it.

### 5. Improve the prose

Apply the **unslop** skill and the writing guidelines of `skill-creator` to each line.

Show the draft to the user and get feedback. Expect more than one iteration. Remove all text that is not necessary. A mode skill is not a manual.

### 6. Commit it

1. If you are on `main` or `master`, make a branch or a worktree first.
2. Commit the skill in a small commit.
3. Do not push, and do not open a PR, unless the user tells you to.

## Guardrails

- **Do not fit the skill to one conversation.** A preference that the user states one time and contradicts another time is noise. Codify a preference only if it occurs more than one time.
- **Keep it simple.** Do not restate the content of other skills, invent metaphors, or write "poetic" prose for an agent reader. This adds cost and gives no benefit. Keep it operational.
- **Refer, do not copy.** Refer to other skills that the user uses by path. Do not paste excerpts. Do the same for principle documents that the user keeps in other locations.
- **Keep sections to a minimum.** Add a section only if the user has a specific rule there that is not a default. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is a section.
- **Use general names.** In instructions, use "the user" or "the human". Do not use the first name of the author.
- **Do not force symmetry.** If the user has no process rules to write down, do not include the Process section.

## Evaluation

A `-mode` skill is subjective output. A test-and-iterate benchmark loop, as in `skill-creator`, does not help here. Check with the user: does it read like the user? Is something missing? Then commit it.

Run a description-optimization loop only if the trigger accuracy of the skill is a real problem in use.

## When not to use this skill

- The user wants a skill for one task, not for working conventions. Use `skill-creator` alone. Mining is not necessary.
- The user wants to capture one narrow workflow (for example, "how I write commit messages"). That is a usual skill, not a mode skill.
