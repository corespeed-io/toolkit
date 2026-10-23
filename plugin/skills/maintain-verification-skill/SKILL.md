---
name: maintain-verification-skill
description: "Regular pass that keeps the verification skill and feature map of a project correct: parallel source readers for each feature, one live session that drives each feature, a maximum of one branch of proven fixes. Use for /maintain-verification-skill or \"audit the verify skill\"."
disable-model-invocation: true
---

# Maintain a verification skill

A feature map becomes wrong as soon as the app changes. This skill is the maintenance loop for a skill that `/create-verification-skill` made, or for a different project-local verification skill with a feature map.

The unit of rigor is the feature, not each sentence. Cover each feature file from the source, and use each feature live. You do not have to check each bullet in a terminal.

## Outcomes

Select one outcome, and say which:

- **clean**: Each feature got source and live coverage. Nothing is worth a change. No branch, no commit.
- **changed**: One branch has the proven corrections to the doc, harness, or map.
- **blocked**: The coverage could not finish, or a proven fix could not ship safely. Say exactly what blocked it.

## Edit scope

Edit only the directory of the verification skill: its SKILL.md, `features/`, and the harness scripts that it owns. Never edit product code during a run.

If the map describes a behavior that the app does not do now, it is one of these:

- Doc drift: fix the map.
- A product regression: report it. Do not hide it with a doc change.

## Pass

0. **Find the target.** Find the verification skill to maintain. It is the project-local skill whose body has launch and drive sections and a feature map. Usually it is in `.claude/skills/verify-*/` (Claude Code) or `.agents/skills/verify-*/` (Codex).
   - If there is more than one candidate, ask the user which one.
   - If there is none, stop. Tell the user to use `/create-verification-skill`. Do not invent a target.

1. **Clean the index.** Read the README of the feature map, and glob its sibling files. Fix entries that are missing, extra, duplicate, or dead. Keep this step light. Do not make a generated inventory.

2. **Source wave.** Start one read-only subagent for each feature file, at the same time. If the tool has no subagents, do this for each feature yourself.
   - Each subagent explains "how does this user-facing feature work?" from the source.
   - It flags possible doc drift, with citations.
   - It returns one short recipe for live verification.
   - Subagents never drive the app and never edit files.
   - Return shape: feature summary / source entry points / possible drift or none / one recipe.

3. **Reconcile.**
   - Make sure that each feature file has a returned summary.
   - Merge recipes that overlap into as few app states as possible.
   - Spot-check the cited drift. Do not prove again the claims that are clean.
   - Look at recent changes for user-facing surfaces that the map does not have. Call a surface missing only if you have a concrete source path for it.

4. **Live pass.** This step is necessary also when the source looks clean.
   - The coordinator does all the driving.
   - Follow the launch model of the verification skill. For servers and UIs, this is one long-lived instance that you drive in series. For short-lived CLIs, this is a new isolated session for each drive. The Launch section of the verification skill decides, not this skill.
   - Use each feature a minimum of one time.

   Keep these three invariants for the full pass, whatever the failure:
   1. Never drive an instance that you did not health-check since it last did something unexpected.
      - Run doctor before the first drive.
      - Where sessions are the unit, run doctor on each new session.
      - Run doctor again after each failed drive.
      - Doctor cannot see some failures, for example a UI state that is stuck on a healthy process. For these, reset to a known state or launch again. Do not hope.
   2. The evidence that you captured stays after each cleanup. Check it at its named location. Do not assume.
   3. Nothing that a drive started stays after the drive is no longer useful. Clean the residue of failed iterations, whether the session is stuck, exited, or shared. For a shared instance, clean the residue, not the instance.

   A doctor failure that skill drift causes is drift. Fix it within the edit scope, and try again one time. Restart only what the fix made invalid. If it still fails, the pass is `blocked`.

   A feature that you cannot get to is `verified-unreachable` only if you give the concrete prerequisite (auth, entitlement, OS, external state) and the route that you tried. If the map does not state that prerequisite, that is drift.

   Drive each harness fix from triage live again before it ships. Do the final teardown after the last drive of the run, including those new proofs. Then nothing stays after the run. The evidence stays, as the skill says.

5. **Triage.**
   - The user-POV description is wrong or missing: this is doc drift. Fix it.
   - The behavior works, but the harness cannot drive it: this is a harness gap. Fix it. A harness fix follows the same helpers rule as generation: scripts are executable, and the skill body shows how to call them.
   - The app behavior is really broken: this is a product gap. Record it for the user. Keep it out of this change.

6. **Commit or stop.**
   - For changed: Read each changed file again first. If you are on `main` or `master`, make a branch. Commit the proven corrections on that one branch. Do not push or open a PR unless the user tells you to.
   - For clean or blocked: No commit. Report the outcome and the coverage honestly.

Keep short run notes (features covered, unreachable prerequisites, confirmed drift, outcome) in a scratch location. Do not commit them.
