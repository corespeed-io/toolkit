---
name: poteto-help
description: Helps the user with pstack setup, /poteto-mode, and the choice of a skill, playbook, or principle for a task. Use for /poteto-help with a question about pstack.
disable-model-invocation: true
---

# Poteto help

Answer the user's question about pstack. Give them a prompt that they can send. Link the file that the answer came from. For a help question, do not start the work. The user asked how, and a pstack run uses many tokens, so let the user send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`poteto-mode`](../poteto-mode/SKILL.md) and do the work under it.

This file maps questions to the skills and guide pages that have the answers. Those files own the details. Read the file that you route to before you quote it. When that file and this map do not agree, trust the file.

The skills are in this toolkit's `personal` plugin. Give the user the local path of a skill, such as `~/toolkit/plugin/skills/<name>/SKILL.md`. The guide pages and the README are not in the toolkit. Link their public copies at `https://github.com/cursor/plugins/blob/main/pstack/` followed by the path. These pages are written for Cursor. Tell the user that when a page describes a Cursor-only feature.

## Find out what the user needs

Get the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes directly to its section. If the need is still not clear, ask one multiple-choice question with these options, then answer only the section that the user picks:

- Get set up
- Start a task with `/poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer. Mention it only when it changes the answer:

- If `~/.claude/rules/pstack-models.md` does not exist, `/setup-pstack` did not run for this user. Each role uses its default model.
- If the project has no `verify-*` skill or other app harness, agents have no scripted way to drive the app. Mention `/create-verification-skill` when the question is about how to prove that a change works.
- If the project has no formal verification skill, no property is checked past what tests reach. Mention `/create-formal-verification-skill` when the question is about a race, an invariant, or another case that tests do not often hit. If one exists, and the code that it covers changed after the commit that it records as the last sync, mention `/maintain-formal-verification-skill` when the question is about that code.

When the model file does not exist and it is important, ask whether the user wants to pick a model for each role and a reasoning budget now. It is important when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask a maximum of one time in each chat. If the need is also not clear, ask the two questions together. Give two choices:

- Now: give them `/setup-pstack` to type, and also answer their question.
- Later: answer their question. Add one line that says each role keeps its default model until they run `/setup-pstack`.

## Get set up

1. pstack comes in this toolkit's `personal` plugin. `~/toolkit/install.sh` installs it in Claude Code and in Codex.
2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes the model file. New chats use the file. At the end, it mentions the verification skill and the formal verification skill for the project, if the project does not have one.
3. Start a real task with `/poteto-mode`, a goal, and a check that can pass or fail.

The install changes nothing until the user starts a skill. Only `/setup-pstack` loads from the user's words. The [README](https://github.com/cursor/plugins/blob/main/pstack/README.md) and [guide page 1](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md) have the details. Offer to write the first prompt with the user, per [`references/prompting.md`](references/prompting.md).

If the user is concerned about cost, say where the tokens go and how to use fewer:

- pstack uses extra tokens on subagents and review panels.
- Run `/setup-pstack` again, and pick a smaller budget or cheaper models.
- A role set to `auto` or `inherit-parent` runs on the model of the chat. This uses fewer tokens when the chat runs on a cheaper model.
- A shorter panel list runs fewer subagents, one for each entry.
- Use `/poteto-mode` only for work that needs rigor.

pstack works in Claude Code and in Codex.

- In Claude Code, a command can need the plugin prefix, such as `/personal:poteto-mode`.
- In Codex, name the skill in the message, such as `$poteto-mode`.
- A step that needs a feature that the tool does not have (for example a Cursor cloud agent, or `/loop` in Codex) is skipped with a one-line note.
- Codex has no `poteto-agent` subagent type and usually no model choice for each subagent. There, the subagents run on the parent model.

## Start a task with `/poteto-mode`

`/poteto-mode` matches the task to a playbook, copies the steps of the playbook into the todo list, and runs the other skills when the steps need them. A step that it skips stays in the list as `skip: <reason>`. A good prompt gives the goal and how to know that it is done. It does not list skills, because a hand-written sequence frequently drops or reorders steps that the playbook keeps. Read [`references/prompting.md`](references/prompting.md) before you help to write a prompt. [Guide page 2](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md) has examples.

In Claude Code and Codex, `/poteto-mode` attaches the skill to one message. Its effect becomes weaker as the chat continues. Start each new task with `/poteto-mode`. (Cursor Custom Modes keep it on for each turn. Claude Code and Codex do not have them.)

In the middle of a chat, "new task" makes the mode match a new playbook. `/poteto-mode` already uses `poteto-agent` for the subagents that its playbook steps spawn. To get the same style from a subagent of your own in Claude Code, spawn it with the `poteto-agent` type (for example `subagent_type: "personal:poteto-agent"`).

## Pick a skill

The default answer is `/poteto-mode`. It runs most of the other skills when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any task that is not trivial, with rigor | [`/poteto-mode`](../poteto-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before they send it: what a top professional adds, their raw material and methods, and an outside check. It returns the prompt and does not do the task | [`/sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code goes | [`/how`](../how/SKILL.md) |
| Know why code has this shape, or where a number came from | [`/why`](../why/SKILL.md) |
| Understand a change or a subsystem, explained in plain words | [`/teach`](../teach/SKILL.md) |
| Get up to date on their own recent work on a topic | [`/recall`](../recall/SKILL.md) |
| Get up to date on what changed in this chat since their last message, in plain words and small visuals, with each item that waits on them listed and decidable from the reply alone | [`/ketchup`](../ketchup/SKILL.md) |
| Know what a small diff can break outside itself | [`/blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/architect`](../architect/SKILL.md) |
| Get many attempts at one brief, merged into the best one | [`/arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as parallel subagents | [`/swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Remove comments before review, with a reviewer that did not write them | [`/no-comments`](../no-comments/SKILL.md) |
| Remove AI tells from prose | [`/unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, an invariant, or another property that tests do not often reach | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code that it covers changed, and learn whether a failure is drift or a bug | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a model, with each bug drawn as a numbered path, turn an agreed chart into a TLA+ skeleton, or audit the code against its TLA+ spec | [`/statechart`](../statechart/SKILL.md) |
| Check a performance number before they report it or act on it | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after they come back | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it after | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/reflect`](../reflect/SKILL.md) |
| Stop agents from making the same mistakes again in this repo | [`/correct`](../correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`/make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around pstack | `/poteto-help` |

If a skill directory next to this one is not in the table, read its frontmatter and route by its description. The `principle-*` directories are in the principles section below.

Close choices:

- `/how` explains what the code does. `/why` explains the reasons. `/teach` runs one or both and explains the result in plain words.
- `/arena` gives each worker the same brief and merges the best parts. `/swarm` splits the work into slices or a race and returns one report.
- `/architect` implements directly after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `/interrogate` reviews the diff. `/blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/recall` builds context again across recent chats. `/ketchup` covers only this chat since the user's last message. To continue one specific chat or branch, use the Session pickup playbook.
- `/figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program across many days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- pstack does not ship `/deslop`, `control-cli`, or `control-ui` (they are in Cursor's `cursor-team-kit` plugin). In this toolkit, the AI-slop pass in `/poteto-mode`, the **unslop** skill, and the **webapp-testing** skill do these jobs.
- `/loop` is built into Claude Code. Codex has no `/loop`.
- To write a skill, use the **skill-creator** skill.
- pstack has no `/orchestrate` skill. Orchestrate is a `/poteto-mode` playbook. If the slash menu shows `/orchestrate`, a different plugin supplies it.

## Playbooks and principles

Playbooks are step lists inside `/poteto-mode`. They are not skills, so they have no slash command. Inside `/poteto-mode`, a description of the task picks one. These phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It does not merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `/poteto-mode`, a phrase such as "babysit this pr" can start a different skill for the same job. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists each playbook and when it applies. [Guide page 6](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md) covers how to open, babysit, and land a PR.

pstack has no planning skill. A plan mode in the tool, such as Plan Mode in Claude Code, works with it. For work across phases or stacked PRs, ask `/poteto-mode` for a plan. It runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and does not implement it. For a design question, the Prototype playbook or `/architect` settles it in code first.

Principles are skills with one rule each. `/poteto-mode` reads them and cites them in its replies. The user does not often start one. They steer with the names instead, as in "apply prove it works. show me the real output." Type `/principle-<name>` to load one when you need it. [Guide page 8](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped after some turns | Its effect becomes weaker as the chat continues. Start each task with `/poteto-mode`. |
| A question was treated as the next step of the last task | Say "new task", or say that the turn does not need the mode. |
| A new model choice had no effect | New chats use the model file from `/setup-pstack`. Start a new chat. |
| Runs cost more than expected | See the cost list under Get set up. |
| A skill did not load automatically | Only `/setup-pstack` loads from the user's words. The others load when the user types them or when `/poteto-mode` runs them, and it does not run each skill. |
| Parallel agents overwrote the work of each other | Give each agent its own worktree. Where the tool has cloud agents, you can run them there, because each gets its own machine. |
| An overnight run made progress but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See [guide page 7](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md). |
| The reply says success from a green build | Ask for the real command, flow, stored value, or profile. That is the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes to copy.

## Make pstack my own

- [`/automate-me`](../automate-me/SKILL.md) writes a draft of a personal mode skill from the user's own history, to use with `/poteto-mode`.
- [`/reflect`](../reflect/SKILL.md), after a session, turns its lessons into skill edits that the user approves.
- `/poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a skill that does not work correctly in its own commit, not inside the feature work where it went wrong.

[Guide page 9](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Give the answer first. Give a maximum of one example prompt in a code block. Adapt it from [`references/recipes.md`](references/recipes.md) when one fits, then link that file. Keep the reply short unless the user asked for the full map.
