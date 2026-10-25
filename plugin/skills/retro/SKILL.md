---
name: retro
description: "Review the user's recent agent sessions, record each correction as a lesson in memory, propose toolkit changes as PRs, and check whether merged fixes stopped the correction. Use for /retro, the daily retro routine, or 'what do agents keep getting wrong'."
---

# Retro

This is the self-improvement loop of the toolkit. `reflect` reviews one conversation. Retro reviews many sessions, and it checks the result of each fix.

The rules:

- Every change to the toolkit goes through a PR that the user merges. Never push `main`.
- Memory needs no review. Save and update lessons without asking.
- You cannot edit the Agent Ensemble environment instructions. For a rule that belongs there, put the exact text in the report.

## The lesson ledger

Each lesson is one memory in the service that `AGENTS.md` names, with `shared` scope. `reflect` uses the same ledger.

- The text starts with `[rsi-lesson:<key>]`. `<key>` is a short kebab-case name for the class of mistake, for example `push-without-asking`. Use the same key each time the same mistake occurs.
- Then: the rule in one sentence, the status, the occurrences, and the fix.
- Status is one of:
  - `open`: seen, no fix yet.
  - `proposed`: a fix branch exists. Give the compare link.
  - `fixed`: the fix PR is merged. Give the PR and the merge date.
  - `verified`: fixed, and not seen again for 14 days after the merge.
  - `regressed`: seen again in a session that started after the fix was merged.
- Occurrences: one line each, `<date> <session id>: <what the agent did> → <what the user wanted>`. Keep the last 10.
- Tags: `rsi: lesson`, `key: <key>`, `status: <status>`.

To find a lesson, search memory for `rsi-lesson` plus the topic. Read the memory before you update it.

## 1. Choose the sessions

- On Agent Ensemble: `list_agents` with `owner` set to the user, sorted by `activity`. Take the sessions with activity since the last retro. The routine prompt gives the previous run. With no previous run, take the last 24 hours.
- Skip the runs of this routine, sessions with no message from the user, and sessions that are still running.
- On a local machine: the transcripts in `~/.claude/projects/` and `~/.codex/sessions/` for the same window.

## 2. Find the corrections

Start subagents in parallel, about five sessions each, so that the transcripts stay out of the main context. Each one reads its sessions with `peek_agent` (follow `before` to read all of a long session) and returns findings only.

A finding is one of these, with the session id and a short quote of the user:

- The user corrected the agent: "no", "wrong", "not that", "I said", a rejected tool call, or the same request asked again.
- The user stated a rule: "always", "never", "from now on", "remember".
- The agent failed in the same way two or more times in one session.

A one-time slip that the agent fixed at once is not a finding. A question about the product is not a finding. Do not quote secrets or personal data.

## 3. Update the ledger

For each finding, find its lesson. If none matches, make a new one with status `open`. Add the occurrence. If the status is `fixed` or `verified`, and the session started after the fix was merged, set the status to `regressed`.

Then check each `proposed` lesson: find its PR with `gh api "repos/spinsirr/toolkit/pulls?state=all&head=corespeed-io:<branch>"`. If it is merged, set `fixed` with the merge date. If it is closed without a merge, set `open` and record why, if the PR says. Set `verified` for each `fixed` lesson with no occurrence in the 14 days after the merge.

## 4. Choose what to fix

Propose a fix for a lesson when one of these is true:

- It has two or more occurrences.
- The user stated it as a rule.
- Its status is `regressed`.

For a `regressed` lesson, more text did not work. Use the **encode-lessons-in-structure** principle skill: a script, a check, or a change to the skill's steps. Do not add another sentence.

Route each fix to one place:

- A rule for one skill: that skill in `plugin/skills/`. A large edit goes through the **skill-creator** skill.
- A rule for all places: `AGENTS.md`.
- A rule only for Agent Ensemble: the report, as exact text for the environment instructions.
- A fact that is not a rule: memory only. No PR.

## 5. Make the branch

Put all fixes of one run on one branch, `retro/<date>`. Follow `add-to-toolkit`. When this session's repo is `corespeed-io/toolkit`, do the steps in the workspace and do not start a child session. Set each lesson in the branch to `proposed` with the compare link.

## 6. Report

The final message, with no introduction:

1. **Regressed**: each `regressed` lesson, with the session that shows it.
2. **Proposed**: the compare link, and one line for each fix with its lesson key.
3. **For the environment instructions**: exact text, if there is any.
4. **Verified**: lessons that changed to `verified` in this run.
5. **Ledger**: counts by status, and the number of sessions reviewed.

If nothing changed, say so in one line.
