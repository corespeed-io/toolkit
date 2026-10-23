---
name: show-me-your-work
description: "Keep a decision trail that a reviewer can check for long or unattended work: a TSV log with one row for each decision (what, why, evidence, result). Local by default. Use for /show-me-your-work, autonomous or multi-phase runs, or work that a human reviews later."
disable-model-invocation: true
---

# Show me your work

Keep one canonical log.

## The format

The log is one TSV file, with one row for each decision. Each cell is one line. Evidence is a pointer, not prose.

To start a clean log, copy `references/decision-log-template.tsv` (the header row). Columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or the workstream.
- **decision.** What you chose or did, in one line.
- **why.** The reason in plain words. If a principle caused the decision, say it plainly, not as a jargon tag.
- **evidence.** A link or a path that proves it: a commit SHA, a PR number, `file:line`, or the path of an artifact, a trace, or a screenshot. Never a paragraph.
- **result.** The outcome or the predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

An example, in plain words, so that a reviewer can read it quickly:

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Log a row

Write each entry as you tell a teammate what you did. Use plain words and concrete actions. Do not use AI phrasing or abstract jargon (the **unslop** skill applies to the log text too).

Use the helper `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. It:

- writes `ts`,
- writes the header on the first use,
- removes tabs and newlines from the cells,
- puts a single quote before each cell that starts with `=`, `+`, `-`, or `@`.

A plain `printf` that appends a row also works. But if the cells come from generated text or text from users, you must handle the same characters.

Log decision points and checkpoints, not each action. Examples: a fork that you chose, a unit that you completed with its verification result, a pivot or a revert with its cause, a blocker that you found, a gate that you fixed. For loop runs, write one row for each iteration. Do not log trivial or obvious items.

A run is one agent conversation, with its later turns and any summary of it. A pickup, a replacement agent, or a new chat starts a new run.

- When a run adds to a log that already has rows, its first row has phase `start`.
- Its first row after a `start` row of a different run also has phase `start`.
- So when a run comes back to a log in a later turn, it first reads the last rows of the log, to find out whether a different run wrote since.
- A `start` row names the `ts` range of the earlier rows that this run did not write. Its evidence names this run, such as its agent id or session id.
- Use phase `start` for nothing else.

## Where the log is

By default, the log is a working artifact. Do not commit it. Keep it at `decisions.tsv` in the work directory, or at `.audit/<task-slug>.tsv` when many efforts run at the same time. Keep it out of git.

Commit it only when the work is so large that a reviewer needs the trail to trust the result.

## Rules

- Only append. To correct a wrong decision, add a new row that replaces it. Never edit or delete history.
- Prefer evidence from committed scripts to evidence from one-time manual steps (the **encode-lessons-in-structure** principle skill).

## Audit the log against the transcript

At the end of the run, before you give the work back, make sure that the log tells the truth. Read the transcript of this run:

- Claude Code: `~/.claude/projects/<slug>/<session>.jsonl`. The slug is the workspace path with each `/` and `.` changed to `-`. The newest `.jsonl` directly in that folder is the current session.
- Codex: the newest session file under `~/.codex/sessions/` for this workspace.

Read only the transcripts of this workspace. Do not glob across all projects, because that reads unrelated private chats.

Compare the rows of this run with what actually happened. Each stretch of rows starts at one of this run's `start` rows, or at the first row if this run created the log. It ends at the next `start` row of a different run.

- Make sure that each row maps to a real decision or action.
- Make sure that the evidence of each row resolves and shows what the row says.
- A fork, a pivot, or an abandoned approach that shaped the work but is not in the log is a gap. Add it.

Correct the log, not the story. The audit never edits or removes a row, also an invented row. When a row records no real decision and no real action, or its claim or evidence is wrong, add a row that replaces it. The new row tells what actually happened and has a pointer that resolves. This audit does not check rows outside the stretches of this run. If the work of this run shows that one of those rows is wrong, replace it as you replace any wrong decision.

## Review of the trail by a different model

Before you give the work back, spawn a subagent on a model that is different from the model that did the work. Self-review is not a replacement. If the subagent tool cannot choose a model (for example in Codex), spawn a fresh subagent on the parent model, and say in the Attention section that the review used the same model. The subagent reads the audit trail and the transcript of the run. Then it flags what the user must look at. It does not do the work again. It looks for what is not optimal or has risk:

- Decisions logged with weak evidence or no evidence.
- Verification steps that were skipped, or that the run said it did without proof in the transcript.
- Choices that look risky now (premature, scope creep, a fix for a symptom only).
- Gaps that the user can miss on a fast read.

Pick each subagent's reasoning effort for the job, per the Subagents section of the **poteto-mode** skill.

Each reply for a run that made a trail ends with an "Attention" section. Put the model of the reviewer first, on its own line (`reviewed by <model>`). Then list each flag, with a pointer to specific rows or moments. "No flags" is a valid value. The model name is not.

## Review the trail

Read from top to bottom. Follow the evidence pointers, and do spot checks. GitHub shows a committed TSV as a table. `column -s$'\t' -t decisions.tsv` shows it as a table in a terminal.

## Use this skill from other skills

Other skills send their audit trail to this skill. They do not make a different one. Refer to this skill by name and let it own the format. Do not repeat the columns.
