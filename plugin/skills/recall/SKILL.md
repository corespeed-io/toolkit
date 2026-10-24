---
name: recall
description: "Rebuild recent working context from memory, chat history, live state, and the shared record (user reports, past fixes, incidents), then give a short current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before you start or resume work."
disable-model-invocation: true
---

# Recall

**Before you start or resume work, rebuild the recent working context of the user. Give back a short capsule: the current state, and what to do next.**

Keep it short and on the topic. Read only what the threads in scope need, then stop.

The context is in three records:

- **Memory** (the service that `AGENTS.md` names) has the durable decisions, conventions, and failure fixes that agents saved.
- **Your chat history** has what you did and decided.
- **The shared record** has all that occurred around the same code under other names: the symptoms that users report again and again, the fixes that shipped and were reverted, the errors that still occur in prod. The **why** skill searches this record across source control, the issue tracker, chat and issue channels, long-form docs, and error tracking. A feature with many bugs keeps most of its story there. Do not rebuild it from your transcripts alone.

Transcripts are in these locations. Each line is one chat message.

- Claude Code: `~/.claude/projects/<slug>/<session-uuid>.jsonl`. `<slug>` is the workspace path with each "/" changed to "-" (thus `/Users/you/proj` becomes `-Users-you-proj`).
- Codex: `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-<timestamp>-<uuid>.jsonl`. The `session_meta` line gives the `cwd`. Use only the files whose `cwd` is the workspace.

## Steps

1. Classify the request, then route it.
   - To resume one specific past chat, use the `session-pickup` playbook, not this skill.
   - To change habits into a durable skill, use `automate-me`.
   - A summary of your work for a human to read is a different task.
   - Recall loads the working context across recent chats before you act.
   - If the user already gave you a full state capsule (paths, branch, the change), use it and do not mine.
2. Fix the scope before you search.
   - Set the window. "Recent" is a real range. The default is the last 7 days.
   - Set the topic, if the user named one.
   - Set the workspace. The default is the active workspace. Never read the transcripts of a different project unless the user asks.
   - State the scope back to the user. Never change "all" to "recent N" without saying so.
3. Search memory first, with 2–3 short queries: the project, the component, the topic. If memory is not available, tell the user and continue.
4. Mine your chat history in parallel.
   - Start parallel subagents. Give each subagent a slice of the transcripts. If the tool lets you choose, use a fast, cheap model, as the Subagents section of the **poteto-mode** skill says.
   - Tell each subagent these rules:
     - Order the candidates by real modification time (`ls -t`). Never order them by UUID name.
     - Grep the topic first. Then read only the matching chats, and only their related regions.
     - Skip the current chat and clear noise (subagent, eval, and test chats).
   - Each subagent returns the same schema, one block for each chat: topic, goal of the user, decisions, open threads, problems and corrections, and artifacts (PRs, tickets, branches). Each item cites the chat UUID.
   - For one or two chats, do not use subagents. Search directly.
   - The raw transcripts stay in the subagents. The main thread gets only their findings.
5. Search the shared record each time the topic names a feature, file, subsystem, area, or bug. This is the default, not a judgment call. "My work on X" does not change this.
   - Give it to the source investigators of the **why** skill. Change their question from "why was this built this way" to "what is the current state, what did people try that did not hold, and what do users still report".
   - Use its per-source playbooks again. Run the investigators in parallel with the chat-history mining.
   - Use its posture: one investigator for each source, a null result is a finding, and skip an MCP that is not available and say so.
   - Put the results into the brief.
   - Skip this step only for pure activity recall with no named target ("what did I do this week"). There, your own history and live state are the full answer.
6. Verify against live state. Check the PRs, branches, and tickets that the mining and the search found, with `git` and `gh`. If the answer depends on what an agent really did (the tools it ran, the files it read, the errors it got), read the full transcript, not only a trimmed local copy.
7. Write the brief to the contract below. Group by thread. Stay on the named topic.
8. Keep memory current. If you found a durable decision, convention, or failure fix that memory does not have, save it. If a finding contradicts a memory, update it (read it first). Do not save state that an agent can check live.

## Output contract

Start with the capsule, then the thread status, then the problems, then the next move. Put more detail below, or remove it.

- **Capsule.** A maximum of 5 bullets. What this work is, and its general state.
- **Threads.** One line each. Start each line with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done yet, so tag it.
- **Problems.** A maximum of 5, the ones that occur again. Include the symptoms that users report again and again, and each fix that shipped and was reverted. Then the next attempt starts where the last one failed.
- **Next move.** The one most useful next action, concrete.

Do not include an adjacent feature or ticket unless it blocks this one. If the capsule and thread lines are longer than one screen, remove detail before you remove threads.

Write the brief with the **unslop** skill. Cite chat findings by UUID. Cite memory findings by memory id. Cite shared-record findings by their source (PR #, ticket ID, chat permalink, error-tracker issue). Remove private context before any public output.

**Reply:** the brief, to the contract above.
