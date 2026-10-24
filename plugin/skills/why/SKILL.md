---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Searches memory, git, and each available MCP evidence category in parallel, and gives a cited read on decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

Investigate the motivation and intent of code. The companion `how` skill answers what the code does and how it works. `why` answers which forces gave the code its shape.

## Subagents

- Start each subagent as a general-purpose subagent with write access and MCP access (Claude Code: `subagent_type: "general-purpose"`). **Do not use a read-only subagent type or Ask mode.** It can remove MCP access, and this disables the MCP investigators and the citation spot-checks of the synthesizer. Investigators must still not write anything.
- If the tool lets you choose the model, use a fast model for investigators and the strongest model for the synthesizer. Choose the reasoning effort of each subagent for its task, as the Subagents section of the **poteto-mode** skill says.
- If the tool has no subagents, do each investigation yourself, one source at a time, and then do the synthesis.

## Operating posture

Work as a **careful, cautious, and precise investigator**. Be honest about what you know and what you infer. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the target and the question

The **target** is usually a part of the code, a pattern, a feature, or a named design decision. The **question** is usually about a design rationale, a tradeoff, an edge case that caused the code, an external constraint, dead code, or a broad history search.

If the target is not clear ("why do we do it this way?" with no clear referent), make your best guess from the conversation context: open files, recent edits, the editor cursor location, what you just discussed. State your interpretation briefly, so that the user can correct you. Then continue.

## Step 2. Make the code anchor

Before you start investigators, collect the seed context yourself:

- file paths and line ranges
- key symbols (functions, classes, constants)
- the last few commits that touch the target
- PR numbers from merge commits (pattern `(#1234)` in the subject line)
- linked ticket IDs
- Memories about the target: search memory (2–3 short queries: the project, the component, the question). Memory has the saved decisions of the owner. If memory is not available, tell the user.

Use these commands:

- `git blame -L <start>,<end> <file>` for the last commits that touched the lines.
- `git log --follow -p -- <file>` for the full history with patches, through renames.
- `git log --oneline -20 -- <file>` for recent commits, with PR numbers visible.
- `git log -1 --format=%B <commit>` to get PR numbers.

Then get the PR bodies and discussion for each important commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`.

Give this anchor to each investigator and to the synthesizer.

## Step 3. Start parallel investigators

**The default is the full parallel investigation.** The goal is a complete coverage map, not a minimal one. Record a null result. Do not skip the search.

### Discovery

Before you start investigators, list the MCP servers and tools that this session has. Use the tool list of the session. In Claude Code, `claude mcp list` also shows the configured servers. In Codex, `codex mcp list` shows them.

Map each available MCP to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Source control is always available through git and `gh`. For the other six, classify each MCP by its name, server instructions, tool names, and resource descriptors. If an MCP can fit more than one category, choose the category of its primary evidence. Record the cases that are not clear in the coverage map.

Start one investigator for each category that has a matching MCP. Start all of them in one message, so that they run at the same time. Each investigator owns exactly one tool or MCP. Do not ask one agent to cover more than one MCP.

The prompt of each investigator is `references/investigator-prompt.md`, completed, plus these items:

- the category playbook `references/sources/<source>.md` for the selected MCP, adapted from the examples in `references/source-playbook.md`
- `references/sources/incident-postmortem.md`, **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the original question of the user

### Investigator roster, one for each available evidence category

Each category below is the best source for one type of "why", shown after "Best at". Use this list to know what to expect back, to name a gap when a category returns nothing, and, only in the rare case that it is provably irrelevant, to justify a skip.

1. **Source control** (git history, `gh` for PRs, code comments, tests). Always start it. It is the only guaranteed source. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (for example Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at *the product or business forcing function*. Strongest when the why is outside engineering.
3. **Long-form documents** (for example Notion, Confluence, Google Docs, Coda MCP). Best at *long-form design rationale*, written before it became code.
4. **Real-time team chat** (for example Slack, Discord, Microsoft Teams, Mattermost MCP). Best at *real-time deliberation that never reached a doc*. Especially important when the record in source control, tickets, and docs is thin.
5. **Infrastructure observability** (for example Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Best at *infrastructure and runtime reality that motivated the code*. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).
6. **Error / exception tracking** (for example Sentry, Rollbar, Bugsnag, Airbrake MCP). Best at *the specific exceptions and error trajectories that motivated defensive or corrective code*. Strongest for catch blocks, null guards, type checks, retries, and other defenses.
7. **Product analytics warehouse** (for example Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Best at *product and data reality that shaped the code*. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

### When to skip an investigator

Skip one only with an **explicit, written justification**. Put it in the final Sources Consulted. There are two valid reasons:

- **No MCP is available for that category** in this environment. Mark it as a gap, not a choice: "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **The source is provably irrelevant**, not only "probably irrelevant". This is a high bar: "Error / exception tracking skipped. Target is a build-time script with no runtime code path."

Sometimes the target is one trivial commit, and its PR description already has the complete answer. Then you can answer inline, **but only after** you confirm that all seven available category searches are redundant. Say so explicitly. This must be rare.

## Step 4. Synthesize

Start one synthesizer. Give it these items:

1. The findings of the investigators, including null results and categories skipped with a justification
2. The code anchor
3. The original question of the user
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Show the output of the synthesizer to the user. You can make small edits for clarity or add context from the conversation. **Do not rewrite the confidence language.**

If the result is a durable decision that memory does not have, save it (`shared` scope). If it contradicts a memory, update that memory (read it first).

## Output format

Use the structure in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary.

- You can adapt it, but keep the confidence separation.
- Keep Sources Consulted as one line for each investigator. Include the investigators that returned nothing or that you skipped, with the reason.

After Sources Consulted: if the `why` question of the user comes before a change to this code, change the lineage findings into a Preserve / Change / Avoid / Risk constraint set for the plan of the change.

## Common failure modes to avoid

- **Recency bias.** Do not assume that the most recent commit is authoritative. The current shape is frequently the result of many earlier decisions. Trace back.
