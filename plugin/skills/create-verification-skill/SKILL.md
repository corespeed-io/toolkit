---
name: create-verification-skill
description: "Make a project-local verification skill that drives the app as a user does, in any language, framework, or platform. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove UI/CLI/service behavior."
disable-model-invocation: true
---

# Create a verification skill

Each serious project needs a scripted way to drive the real app and prove its behavior. The script launches the app, uses a feature as a user does, and captures evidence. This skill makes that script as a project-local skill, `<skills-dir>/verify-<app>/`, for the repo.

`<skills-dir>` is the project skills directory of the tool: `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex). If the repo uses both tools, write the skill in one directory and add a symlink in the other.

Write the output for the next agent, not for a human. An agent that never saw the app reads it for the first time, during a task.

## 1. Interview the repo, not the user

Get these answers from the codebase. Ask the user only for what you cannot see.

- **Surface:** What does a user touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have more than one. Select the primary surface and write down the others.
- **Run:** How does the app start locally? Prefer the dev command that the repo documents (package scripts, Makefile, README quickstart). Write down ports, env vars, seed data, and auth.
- **Drive:** How can an agent use the app with a program? First use the existing harnesses: Playwright/Cypress specs, expect scripts, PTY helpers, endpoints that curl can call, a debug port. Only if none exist, select a general recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** What evidence can you capture? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** Can two instances run at the same time (ports, data dirs, profiles)? If not, say so in the new skill. It is better to refuse to drive a shared instance two times than to corrupt the session of the user.

If the checkout does not build or start as it is, fix that first, or report it precisely, before you make the skill. A skill that you write against a broken base teaches wrong steps. Sometimes a missing asset that is not related blocks startup (for example, a static dir that the API never serves, or a sample config). Then the new skill can create it. Mark it clearly as verification scaffolding, and remove it in cleanup.

## 2. Make the skill

Write `<skills-dir>/verify-<app>/SKILL.md` with YAML frontmatter. The frontmatter has `name: verify-<app>` and a `description` that names the app, the surface, and when to use the skill. Without frontmatter, the skill does not register.

Add the sections that follow. Base each section on what the interview found. Do not leave placeholders.

- **Launch:** the exact command that starts the app for verification, and how to tell that it is ready (a log line, a prompt).
  - Launch must get to a usable state from an empty data dir, with all migrations and seed data.
  - Ready means usable, not only that a process answers. A database health check can pass while its init scripts still run.
  - Include teardown.
  - A short-lived CLI or TUI has no server to keep alive. For it, launch means: build the binary (or install deps) one time, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only check that answers "is this instance worth driving?" It checks that the process is up, that the version or build is correct, that the port is ours, and that auth is valid. An agent runs this first each time something looks wrong.
- **Drive:** the harness recipe with real selectors and commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) to coordinates and tab order.
- **Evidence:** what to capture for a proof, and where it goes. State these proof standards:
  - Use the real user path, not internal setters or test-only endpoints.
  - Capture the action and the state that it causes, not only the last screen.
  - Verify side effects (files written, rows inserted, messages sent) and also what is visible.
  - Use mocks only where a production boundary already isolates the external system.
  - If the safe path is a dry-run or test mode, observe what it really skips (files, network, git refs). Do not trust its name. Some dry-runs still use the network or open a browser.
- **Cleanup:** how to remove the instances that the run created.
  - Never kill by process name. Kill what you started.
  - Cleanup removes instances and scratch state. It never removes the evidence. Proof artifacts stay after teardown, in a location that the skill names.
- **Helpers:** each script that the skill ships must be executable. The skill body must show how to call it. If the reader must reverse-engineer a helper, it is not a helper.

## 3. Start the feature map

Create `<skills-dir>/verify-<app>/features/README.md`. Add one file for each user-facing feature that you can find. Start with the top 3–5 features from routes, commands, menus, or docs. Use the shape in [`references/feature-map-example/`](references/feature-map-example/): a README index and one file for each feature.

Each file answers these questions from the point of view of the user:

- What is the feature?
- How do you get to it?
- How do you drive it with the harness?
- What observable end state proves that it works?

The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.

If the seed data does not have a precondition that a journey needs, the journey reports a failure. Put the reason in the `Gotchas` of that feature. Never make the journey weaker to make it pass.

The map is the verification source that the repo maintains. If the map lists more than one entry point, a proof that drives only one convenient entry point is not complete.

## 4. Prove the new skill before you give it to the user

1. Follow its instructions from start to end one time: launch, doctor, drive ONE mapped feature, capture evidence, clean up. One feature is sufficient. Later runs use the map to cover the others.
2. After cleanup, confirm that the evidence is still at the named location. If cleanup deletes the proof, this step fails.
3. Fix what fails. After each failed iteration, run the cleanup of the new skill. Then broken attempts do not leave processes and ports.

A new skill that nobody ran is a draft, not a deliverable.

If you proved it in a stand-in for the real target (a container instead of a new VM, a local stack instead of a remote one), list each setup step that the stand-in did and the target does not do. Those steps are not verified until a run on the real target covers them.

## 5. Offer the maintenance loop

Tell the user to use `/maintain-verification-skill` to keep the map correct when the app changes. Suggest a schedule only if the user asks.
