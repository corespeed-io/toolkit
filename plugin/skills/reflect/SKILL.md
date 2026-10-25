---
name: reflect
description: "Start three parallel review subagents on the active transcript, find learnings, and route each one to a concrete edit on an existing skill or to memory. Use when the user says reflect or /reflect."
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings. Then route them into skill edits, or into memory for facts that are not skill rules.

Use this skill when the user says "reflect" or "/reflect". Do not use it when the conversation is trivial or off-topic, or when an existing skill already covers it and the parent followed that skill correctly. A one-time event is not a learning.

## 1. Find the active transcript

Before you start subagents, find the transcript of this conversation. Look only in the transcript directory of this workspace:

- Claude Code: `~/.claude/projects/<slug>/`. `<slug>` is the workspace path with each "/" changed to "-". Subagent transcripts are in `<session-uuid>/subagents/`.
- Codex: `~/.codex/sessions/<yyyy>/<mm>/<dd>/`. Use only the files whose `session_meta` `cwd` is this workspace.

Do not glob across the transcript directories of other workspaces. They contain private chats from projects that are not related.

```bash
# Claude Code
ls -t ~/.claude/projects/<slug>/*.jsonl ~/.claude/projects/<slug>/*/subagents/*.jsonl 2>/dev/null | head -10
# Codex
ls -t ~/.codex/sessions/*/*/*/rollout-*.jsonl 2>/dev/null | head -10
```

For each candidate, read the first lines until you find the first user message. Take the file whose first user message is the opening prompt of this conversation. If no file matches, give the reviewers a short digest of the session instead.

## 2. Start three reviewers in parallel

Start three subagents in one message. Use a general-purpose subagent type with write access and MCP access (Claude Code: `subagent_type: "general-purpose"`). The reviewers need MCP access to look up the tickets, chat threads, and observability traces that the transcript refers to. A read-only subagent type can remove MCPs.

If the tool lets you choose the model, use the strongest model for Judgment, Divergent, and the synthesizer. Use a fast model for Tooling. Choose the reasoning effort of each subagent for its task, as the Subagents section of the **poteto-mode** skill says. If the tool has no subagents, run each lens yourself, one after the other.

| Lens | Model choice | Prompt template |
|---|---|---|
| Judgment | strongest, high effort | `references/judgment-reviewer.md` |
| Tooling | fast, high effort | `references/tooling-reviewer.md` |
| Divergent | strongest, high effort | `references/divergent-reviewer.md` |

Pass each template without changes. Put the transcript path or digest where the template marks it. Reviewers return their findings in the response body of the subagent.

## 3. Synthesize

Start one more subagent with the same type and access. Use the model choice of Judgment. It spot-checks citations through MCP, so it must not be read-only. Pass `references/synthesizer.md` without changes, with the full output of each reviewer inline where the template marks it. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move each Accepted item to Backlog if a lint rule, script, metadata flag, or runtime check can enforce it more reliably. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Show the full Accepted / Rejected / Backlog output of the synthesizer. Wait for explicit approval before you apply an Accepted edit. The user selects the subset and can change routings. Skill changes affect all future agents in the org. Do not apply them automatically.

Record each Accepted and Backlog item as a lesson in memory without waiting, in the ledger format of the **retro** skill. Only the edits wait for approval.

The skills come from the toolkit. Make each skill edit in the toolkit, not in the installed copy, and follow `add-to-toolkit`: on my machines in `~/toolkit`, on Agent Ensemble as a PR. Set the lesson to `proposed`.

Follow the Routing of each approved row exactly:

- Trivial edit to an existing skill (a one-line bullet, a shorter sentence, a corrected old fact): the parent does it directly.
- Large edit to an existing skill (a new section, a new pattern table, more than approximately 10 lines): give it to the **skill-creator** skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists, but it did not trigger when it should): give it to `skill-creator` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: give the creation to `skill-creator`. Do not invent the shape yourself.

Route durable facts to memory, not to local files:

- A finding can be a durable decision, convention, or failure fix about the user or a project, and not a rule for a skill. Save it to memory (`shared` scope; `private` scope for details of one machine). Do this without waiting for approval.
- Search memory first. If a memory already covers it, update that memory (read it first). Do not add a duplicate.
- Never write learnings to local memory files, `MEMORY.md`, or rule directories of the tool. If memory is not available, tell the user.

If your environment has a SKILL.md validator, run it on each skill that you changed before you say that you are done.

## 6. Summarize for the user

Give a short list, with no introduction:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Memories saved or updated: `<memory id>`. One line each.
- Lessons recorded: `<key>` (`<status>`). One line each.
- Dropped: one line for each rejected finding, with the reason from the synthesizer.
