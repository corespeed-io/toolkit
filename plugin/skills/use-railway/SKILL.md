---
name: use-railway
description: >
  Operate Railway: signup and sign-in, projects, services, databases, buckets,
  deploys, variables, domains, IaC, OpenTelemetry tracing, failures, metrics,
  feature flags, cloud agents, and usage. Use when the user mentions Railway,
  deployments, services, environments, or tracing.
allowed-tools: Bash(railway:*), Bash(which:*), Bash(command:*), Bash(npm:*), Bash(npx:*), Bash(curl:*), Bash(python3:*)
---

# Use Railway

## Railway resource model

Railway puts infrastructure in a hierarchy:

- **Workspace** is the billing and team scope. A user is a member of one or more workspaces.
- **Project** is a set of services in one workspace. It is one deployable unit of work.
- **Environment** is an isolated configuration plane in a project (for example, `production`, `staging`). Each environment has its own variables, config, and deployment history.
- **Service** is one deployable unit in a project. It can be an app from a repo, a Docker image, or a managed database.
- **Bucket** is an S3-compatible object storage resource in a project. You make buckets at the project level and deploy them to environments. Each bucket has credentials (endpoint, access key, secret key) for S3-compatible access.
- **Deployment** is a release of a service in an environment at one point in time. It has build logs, runtime logs, and a status lifecycle.

Most CLI commands operate on the linked project/environment/service context. To see the context, use `railway status --json`. To override it, use the `--project`, `--environment`, and `--service` flags.

## Tool routing

Railway has three operation paths for agents. Choose the path that agrees with the job:

- **Railway CLI** (`railway`): workflows that depend on the local machine state. Examples: deploys from the current working directory, `railway up`, `railway run`, SSH, database analysis scripts, local linking, interactive setup, or exact command output.
- **Remote MCP** (`https://mcp.railway.com`): the default plugin MCP path. Use it for account/project/service discovery, deployment state, bounded logs, traces, feature flags, simple redeploys, simple project creation, or complex Railway workflows that you can give to `railway-agent`. Remote MCP uses Railway OAuth. It does not depend on local CLI state.
- **GraphQL through `railway api`**: operations that do not have an MCP tool or a CLI command. Before you write an unfamiliar query, search and examine the schema.

If more than one path is available, choose the path that keeps the necessary context:

- The CLI is correct for workflows that need the current repo, local credentials, SSH, database scripts, or exact command output.
- Remote MCP is correct for OAuth-scoped platform operations that do not need local files or CLI state.

On a Railway cloud agent VM, the `railway` CLI has credentials only in an SSH terminal session. In a dashboard or mobile chat session (Railway Agent), the CLI is unauthenticated by design.

- In that session, do not run `railway` commands. This includes reads and `railway api`.
- The `railway` MCP server is authenticated in all sessions. Use its tools.
- To find IDs, use `list-services`, not `railway status --json`.
- If no tool can do the job, tell the user. Ask the user to make the change in the dashboard.

Optional: an in-process CLI MCP (`railway mcp local`) that is already configured can give operations that the hosted MCP does not have. A bare `railway mcp` starts the hosted MCP proxy with CLI authentication. It is not the in-process server. Published plugin configs connect directly to the hosted MCP with editor OAuth.

For GraphQL, use `railway api` (CLI 5.28+). For older CLIs, the legacy `scripts/railway-api.sh` is a compatibility fallback. Refer to [request.md](references/request.md).

## Parsing Railway URLs

Users frequently paste Railway dashboard URLs. Get the IDs from the URL before you do other work:

```
https://railway.com/project/<PROJECT_ID>/service/<SERVICE_ID>?environmentId=<ENV_ID>
https://railway.com/project/<PROJECT_ID>/service/<SERVICE_ID>
```

The URL always has `projectId` and `serviceId`. It can have `environmentId` as a query parameter. If the environment ID is missing and the user gives an environment name (for example, "production"), find the ID:

```bash
railway api \
  'query getProject($id: String!) {
    project(id: $id) {
      environments { edges { node { id name } } }
    }
  }' \
  --variables '{"id": "<PROJECT_ID>"}'
```

Match the environment name (case-insensitive) to get the `environmentId`.

**Pass explicit IDs** to CLI commands (`--project`, `--environment`, `--service`) and scripts (`--project-id`, `--environment-id`, `--service-id`). Do not run `railway link` for this. Explicit IDs do not change global state, and they are faster.

## Intent-based routing

Find the intent of the user *before* you run preflight checks. The preflight below is for diagnostic and configuration work. It adds unnecessary steps when the user only wants to ship something or sign up.

**Deploy-from-cwd intent** ("deploy", "ship", "push to Railway", "deploy this app"):
- Do not run the `railway whoami` / `railway status` preflights.
- Run `railway up` directly. It validates auth. If the user is not authenticated, it signs the user in (the CLI opens a browser). Then it makes the project and service and deploys.
- Before you run it, tell the user: *"Running `railway up` — it signs you in if necessary and deploys this directory."*
- **Do not ask the user to run `railway login` first.** `railway up` does the auth as part of the deploy.
- If the environment cannot open a browser, the CLI prints a device-code sign-in link and waits. Follow [Device-code sign-in: relay the link immediately](#account-creation--sign-in). Run the command in the background, and give the link to the user immediately when it prints.

**Signup intent** ("sign me up", "create my Railway account", "register me", "get me on Railway"):

When the user asks for an account, do it. Do not ask for confirmation. The only block is the OAuth sign-in, which the user must complete in the browser. Do not start a signup that the user did not ask for.

- **If the current directory has a deployable app (for example, `package.json`, `requirements.txt`, `go.mod`, `Dockerfile`, or source to build), run `railway up`.**
  - It signs the user up *and* deploys in one step. The result is a running app.
  - A detected agent harness authorizes the project creation. Thus, **bare `railway up` is sufficient**. No additional prompt occurs.
  - Use it also when the user only said "sign me up". The goal is to ship the app. Do not make the user choose a command, and do not use only a login.
  - For scripted or agent runs, `railway up -y` is the more reliable form. It skips prompts and forces the create non-interactively, also if harness detection fails.
  - `railway login` is NOT the default for signup when there is something to deploy.
- **Only when there is nothing to deploy**, use `railway login`. Examples: an empty directory, a directory that is not an app, or the user says that they want only an account and no deploy. `railway login` makes new accounts through the same OAuth flow. There is no separate signup command.
- Signup is the flow that most frequently gets the device-code wait (new users in sandboxed or headless agent environments). Follow [Device-code sign-in: relay the link immediately](#account-creation--sign-in). If the code expires, the signup fails and the user possibly does not try again.

**Sandbox / remote-build intent** ("give me a sandbox", "spin up a scratch environment", "build this remotely", "run this remotely", "checkpoint/snapshot the sandbox", "save this sandbox state", "restore my sandbox"):
- Load [sandbox.md](references/sandbox.md) and follow it.
- Sandboxes must be enabled in Priority Boarding. If a sandbox command fails with a feature-availability error, tell the user to enable Sandboxes in Priority Boarding. Do not retry.

**Other intents** (query state, list projects, configure variables, debug failures):
- Follow the Preflight section below.

## Preflight

Before each mutation, verify the tool path and the context:

```bash
command -v railway                # CLI installed
railway whoami --json
railway --version                 # check CLI version
```

**Exception**: `railway up` and `railway login` validate auth themselves and have their own flows for unauthenticated users. Do not run `railway whoami` before them. It adds a failing call that does not change your next step. Refer to [Account creation & sign-in](#account-creation--sign-in).

### Skill and agent tooling

This skill is a copy in the owner's toolkit plugin. It can differ from the upstream Railway skill.

- Do not run `railway skills update`, `railway skills`, or `railway setup agent` to update or install skills or MCP. They write the upstream skill and MCP configuration into the tool and replace this copy.
- Run them only when the user tells you to.
- If the guidance of this skill does not agree with the output of the CLI, trust the CLI.

When Railway MCP is available and the job is a platform-state read, use the applicable MCP read. Do not use the shell for it. If you use the CLI path, run the CLI checks above.

**Context resolution — URL IDs always have priority:**
- If the user gives a Railway URL, get the IDs from it. Do NOT run `railway status --json`. It gives the locally linked project, which is usually not related.
- If there is no URL, use `railway status --json` for the linked project/environment/service.
- When you use MCP tools after you get local context from `railway status --json`, pass the project, environment, and service IDs explicitly. Do not use the implicit linked context of MCP. MCP possibly does not share the current working directory link of the CLI.

If the CLI is missing, install it with one of these commands:

```bash
bash <(curl -fsSL https://railway.com/install.sh) # Shell script (macOS, Linux, Windows via WSL)
npm i -g @railway/cli # npm (macOS, Linux, Windows). Requires Node.js version 16 or higher.
brew install railway # Homebrew (macOS)
```

These variants also configure the agent tools that they find (skills and MCP). Use them only when the user asks for Railway agent tooling:

```bash
curl -fsSL agents.railway.com | sh # Install CLI and configure detected agents
bash <(curl -fsSL https://railway.com/install.sh) --agents -y # Install CLI and configure detected agents
```

If the user is not authenticated, refer to [Account creation & sign-in](#account-creation--sign-in) below. The CLI has unauthenticated `railway up` (deploy and sign up/in in one step) and `railway login` (sign up/in only; it makes new accounts). If the directory is not linked and the user gave no URL, run `railway link --project <id-or-name>`.

If the CLI does not recognize a command (for example, `railway environment edit`), the CLI can be old. Upgrade it:

```bash
railway upgrade
```

## Account creation & sign-in

Railway uses one OAuth flow for sign-in and sign-up.

- The backend finds new accounts from durable compliance state (a CLI client that did not accept ToS / Fair Use yet).
- It changes the consent screen and the page after auth. New users see a "Welcome to Railway!" page. Existing users see the standard confirmation.
- The CLI does not declare signup intent at the start.

Two commands start this flow:

| Command | When to use |
|---|---|
| `railway up` | Agent-friendly onboarding from the current directory. Unauthenticated → opens the browser (or device-code) to sign in / sign up. With no linked project, a detected agent harness (or `-y`) auto-creates a project + service and deploys; an interactive human is offered create / link-existing / cancel. Add `-y` to skip prompts and force the create non-interactively (works even if harness detection misses). |
| `railway login` | Sign in — *and* sign up. New accounts are created on the fly through the same OAuth surface; there is no separate signup command. |

Related: `railway up --new` makes a *new* project + service from the current directory and deploys it, also if a project is already linked. Use it when the user is signed in and wants a new app. `--name <name>` overrides the project name.

**Choose the path:**

- Deploy from cwd: run `railway up` (interactive) or `railway up -y` (skips the confirm prompt). Run it yourself. Do not ask the user to sign in separately first.
- New project from cwd when the user is signed in: `railway up --new`.
- **Sign up with a deployable app in cwd: `railway up`.** It signs up *and* deploys. Bare `up` works for a detected agent, also if the user only said "sign me up". Add `-y` to skip prompts or to force it non-interactively.
- Sign in, or sign up with nothing to deploy: `railway login`. It makes new accounts.

**Headless / no browser:**

The CLI **automatically detects** SSH sessions, CI, and a missing `DISPLAY`. Then it uses the device-code flow. You almost never need to force it.

**Do NOT pass `--browserless` only because you are an agent or because your shell is non-interactive.** If the human is at this machine (a local IDE or desktop session, which is the usual case), bare `railway login` opens *their* browser directly. This completes much more reliably than a device code (approximately 90% vs 60% success for sign-ins from agents). A coding agent does not make the machine headless.

```bash
railway login --browserless   # ONLY for machines with genuinely no browser
```

This forces the device-code flow (RFC 8628). It prints a sign-in link and a short code that the user opens on a device. Use it only on machines with no browser: SSH boxes, containers, or remote VMs that the auto-detection did not find. In a device-code flow, follow the relay procedure below. Give the sign-in link to the user immediately when it prints.

**Agent harness, human present**: when the CLI detects an agent harness (Claude Code, Codex, and others) with a human at the keyboard, `railway up` opens the browser and skips the confirm prompt. The CLI treats the agent call as consent. A human must still complete OAuth in the browser.

**Device-code sign-in: relay the link immediately (CRITICAL):**

When the CLI cannot open a browser (sandboxed shell, container, SSH, no `DISPLAY`), unauthenticated `railway up` and `railway login` do this:

- They print a sign-in URL and a short code.
- Then they **block and poll for a maximum of 10 minutes** while the user completes sign-in. The code expires after 10 minutes.

If you run the command as a normal foreground command, the harness keeps the output until the command exits. Thus, **the user sees the link only after the code expired**. This is the most frequent cause of failed agent signups. Do these steps:

1. **Preferred: run the command in the background.**
   - Claude Code: use `run_in_background`, then read the output of the background task.
   - Codex: run it in a background terminal session, if your Codex version has one. If not, use step 2.
   - Read the output frequently. When a sign-in block appears, **stop all other work and give it to the user word for word.** The block is `Sign in with one click: <url>` on newer CLIs, or `Sign in at: <url>` / `Enter this code: <code>` on older CLIs. Do not summarize, shorten, or delay it.
   - If there is a one-click URL, give that URL. If not, give the URL and the code together. Tell the user to open the link now.
   - Let the command continue to run, and continue to read the output. When the user completes sign-in, the same process gets the session and continues to the deploy. Then verify the deploy as the rules below tell you.
2. **No background support: tell the user what to expect, and use the longest timeout.**
   - Before you run the command, tell the user: *"This prints a sign-in link. I show it to you immediately. Complete it quickly. The code expires in 10 minutes."*
   - Run the command with the longest timeout that your harness permits.
   - If the command times out or stops before sign-in completes, nothing monitors the printed code. A late click does nothing. Give the user the link that appeared, for context. Then run the command again immediately and give the user the **new** link. Tell the user to always use the newest link.
3. **Do not** wait silently for the command to finish before you show the link. Do not report a failed sign-in before you give the user the link and a chance to use it.

The browser transport does not need these steps. The CLI opens the browser on the machine of the user.

**JSON / CI modes do not prompt automatically**: `railway up --json` and `railway up --ci` do NOT open a browser for an unauthenticated user. `--json` gives a structured error:

```json
{"error":"Not signed in.","code":"NOT_AUTHENTICATED","hint":"Run `railway login` to authenticate, then re-run."}
```

When you see `code: NOT_AUTHENTICATED`, authenticate the user with `railway login`. Then run the original command again.

`OAUTH_INSUFFICIENT_GRANT` is different. The session is valid, but it does not have access to the resource. Do not loop through login. Examine the IDs, the workspace membership, and the grant scope of the integration. Refer to [operate.md](references/operate.md).

**Fully unattended (no human)**: set `RAILWAY_API_TOKEN` (account-scoped) or `RAILWAY_TOKEN` (project-scoped). Do not run an interactive login. A new user with no token and no human present cannot complete signup. There is no headless account-creation path. If you do not have a token, ask the user for one.

## Agent tooling

Use direct Railway CLI commands for deterministic operations. Use `railway agent` only in these conditions:

- The user explicitly asks for Railway Agent.
- The user wants a natural-language investigation.
- The task is larger than one resource operation.

Only when the user tells you to, set up Railway skills, MCP, and authentication with:

```bash
railway setup agent
railway setup agent -y
railway setup agent --oauth
```

`railway setup agent -y` skips the interactive login flow. If the user is not authenticated after setup, run `railway login`.

When the user names a target tool and tells you to install or update MCP and skills, use:

```bash
railway mcp install                              # hosted MCP via CLI login
railway mcp install --agent codex --oauth         # direct HTTP, editor OAuth
railway mcp install --agent cursor --oauth
railway skills
railway skills update --agent codex
railway skills remove --agent cursor
```

Supported targets include `claude-code`, `cursor`, `codex`, `opencode`, `copilot`, and `factory-droid`.

| Install mode | Transport and authentication |
|---|---|
| Default / `--remote` | `railway mcp` stdio proxy to hosted MCP, authenticated by `railway login` |
| `--oauth` | Direct HTTP to `https://mcp.railway.com`, authenticated by editor OAuth; matches the published plugins |
| `--local` | In-process GraphQL-backed stdio server, invoked as `railway mcp local` |

These modes apply to `mcp install` and `setup agent`. Interactive setup gives a choice. `railway mcp proxy` is still an alias for the default proxy. The proxy can fill only a linked project ID, and only when the tool accepts it and the call gives no resource scope. For scoped work, continue to pass explicit project, environment, and service IDs.

Use Railway Agent chat with:

```bash
railway agent
railway agent -p "why is my service crashing?"
railway agent -p "summarize the deployment status" --json
railway agent --list --json
railway agent --thread-id <thread-id>
```

`railway agent` needs user OAuth authentication from `railway login`. Railway Agent chat does not support project tokens (`RAILWAY_TOKEN`). If an agent command is not available, upgrade with `railway upgrade --yes`.

## Common quick operations

You can do these frequent operations without a reference. When the job is platform-scoped and the MCP tool is available, use the MCP tool. If not, use the CLI:

```bash
railway status --json                                    # current context
railway whoami --json                                    # auth and workspace info
railway project list --json                              # list projects
railway service list --json                              # services in current environment (verify before retrying `add`)
railway add --database <type> --json                     # add one database; ALWAYS pass --json
railway add --service <name> --json                      # add empty service; ALWAYS pass --json
railway variable list --service <svc> --json             # list variables
railway variable set KEY=value --service <svc>           # set a variable
railway domain list --service <svc> --json               # domains and DNS status
railway logs --service <svc> --lines 200 --json          # recent logs
railway logs --service <svc> --network --lines 200 --json # network flow snapshot
railway metrics --service <svc> --since 1h --json        # resource and HTTP metrics summary
railway up --detach -m "<summary>"                       # deploy current directory (returns at QUEUED — verify before reporting)
railway deployment list --json                           # poll newest deployment status after a detached up
railway bucket list --json                               # list buckets in current environment
railway bucket info --bucket <name> --json               # bucket storage and object count
railway bucket credentials --bucket <name> --json        # S3-compatible credentials
```

## Routing

For work that is not a quick operation, load the references for the intent of the user. Most requests need one or two references. When the workflow crosses areas, load more.

| Intent | Reference | Use for |
|---|---|---|
| **Analyze a database** ("analyze \<url\>", "analyze db", "analyze database", "analyze service", "introspect", "check my postgres/redis/mysql/mongo") | [analyze-db.md](references/analyze-db.md) | Database introspection and performance analysis. analyze-db.md directs you to the DB-specific reference. **This takes priority over the status/operate routes when a Railway URL to a database service is provided alongside "analyze".** |
| Create or connect resources | [setup.md](references/setup.md) | Projects, services, databases, buckets, templates, workspaces |
| Ship code or manage releases | [deploy.md](references/deploy.md) | Deploy, redeploy, restart, build config, monorepo, Dockerfile |
| Change configuration ("webhook", "notify on deploy", "custom header", "Slack/Discord notifications") | [configure.md](references/configure.md) | Environments, variables, config patches, domains, networking, project webhooks with the `list-webhooks` / `create-webhook` / `update-webhook` / `test-webhook` / `delete-webhook` MCP tools and their custom headers |
| Manage feature flags | [feature-flags.md](references/feature-flags.md) | MCP registry operations; CLI targeting rules and rollouts; SDK runtime reads |
| Define configuration in source control ("IaC", "infrastructure as code", "config as code", `.railway/railway.ts`, `.railway/railway.py`, `.railway/railway.go`, "config migrate/plan/apply/pull") | [iac.md](references/iac.md) | Author/import IaC, migrate legacy JSON/TOML, save and apply reviewed plans, check drift |
| Manage databases ("PITR", "restore", "backup", "HA", "failover", "switchover", "PgBouncer", "connection pooling") | [databases.md](references/databases.md) | Postgres recovery, HA and pooling; MySQL/Redis HA; use analysis references for performance investigations |
| Inspect costs or manage spending limits | [usage.md](references/usage.md) | Workspace/project/service usage, billing periods, workspace and Railway Agent limits |
| Run a coding agent on Railway ("cloud agent", "railway ca", "railway code", "desktop SSH") | [cloud-agents.md](references/cloud-agents.md) | Provision, connect, wake, sleep, delete, or configure desktop access to cloud agent VMs |
| Check health or debug failures | [operate.md](references/operate.md) | Status, logs, metrics, build/runtime triage, recovery |
| Trace requests across services ("tracing", "traces", "trace ID", "spans", "OpenTelemetry", "OTel", "OTLP", "instrument my app", "instrument my function", "Bun function", "auto-instrumentation") | [tracing.md](references/tracing.md) | Enable tracing per service and environment with the `get-tracing` / `set-service-tracing` MCP tools or `railway trace enable`, the IaC `tracing` block (SDK and CLI version gates), SDK instrumentation (preferred) vs automatic (eBPF), what to instrument, instrumenting a Function (Bun), the provided `OTEL_*` variables, sampling, reading traces with the `list-traces` / `get-trace` MCP tools or `railway trace list` / `get`, checking what a service's instrumentation covers with `get-tracing-coverage`, the Traces tab |
| Use a sandbox or build remotely ("sandbox", "scratch environment", "ephemeral box", "build remotely", "remote build", "run this remotely", "checkpoint", "snapshot/save/restore sandbox state") | [sandbox.md](references/sandbox.md) | Create/fork sandboxes, run commands remotely, remote template builds, checkpoints (save/restore sandbox state), port forwarding, teardown. Requires Sandboxes enabled in Priority Boarding — if unavailable, prompt the user to enable it. |
| Request from API, docs, or community | [request.md](references/request.md) | Railway GraphQL API queries/mutations, metrics queries, Central Station, official docs |

If the request covers two areas (for example, "deploy and then check if it's healthy"), load the two references and write one response.

## Execution rules

1. Use the Railway CLI for workflows that need the current repo, the local shell, SSH, database scripts, local Railway context, or exact command output.
2. Use Remote MCP for OAuth-scoped platform operations that agree with an available MCP tool and do not need local files or CLI state.
3. Use the local CLI MCP only when the current agent already has it explicitly configured, and it has a necessary operation that Remote MCP does not have.
4. Use `railway api` for operations that do not have an MCP tool or a CLI command. Keep the legacy helper only for CLI compatibility.
5. Use `--json` output when it is available, for reliable parsing.
6. Find the context before a mutation. Know which project, environment, and service you change.
7. For destructive actions (delete service, remove deployment, drop database), you must state the impact and get the confirmation of the user before you run them. These actions cannot be undone.
8. After a mutation, verify the result with a read-back command or an MCP read.
9. **Do not report a successful deploy before you see SUCCESS for that deployment.**
   - `up --detach`, a non-TTY `up` without CI mode, or a stream that timed out can return after the upload.
   - Follow the deployment ID from the upload in `railway deployment list --json`, with the same project/environment/service scope. Do not use a different, newer deployment that runs at the same time.
   - If the status is `FAILED` or `CRASHED`, triage it as [operate.md](references/operate.md) tells you.
   - If the status is `NEEDS_APPROVAL`, `SLEEPING`, `SKIPPED`, `REMOVED`, `REMOVING`, or unknown, report that state and the next action.
   - Exit code 0 alone is not sufficient. For CI streaming and polling, refer to [deploy.md](references/deploy.md).

## User-only commands (NEVER run these yourself)

These commands change database state. The user must run them in their terminal. **Do NOT run these with Bash. Show the command and ask the user to run it.**

| Command | Why user-only |
|---------|---------------|
| `python3 scripts/enable-pg-stats.py --service <name>` | Modifies shared_preload_libraries, may restart database |
| `python3 scripts/pg-extensions.py --service <name> install <ext>` | Installs database extension |
| `python3 scripts/pg-extensions.py --service <name> uninstall <ext>` | Removes database extension |
| `ALTER SYSTEM SET ...` | Changes PostgreSQL configuration |
| `DROP EXTENSION ...` | Removes database extension |
| `CREATE EXTENSION ...` | Installs database extension |

When these operations are necessary:
1. Explain what the command does and its side effects (for example, a necessary restart).
2. Show the exact command that the user must run.
3. Wait until the user confirms that they ran it.
4. Verify the result with a read-only query.

## Composition patterns

Multi-step workflows usually follow these sequences:

- **Add object storage**: setup (make bucket), setup (get credentials), configure (set S3 variables on app service)
- **First deploy**: setup (make project + service), configure (set variables and source), deploy, operate (verify healthy)
- **Fix a failure**: operate (triage logs), configure (fix config/variables), deploy (redeploy), operate (verify recovery)
- **Add a domain**: configure (add domain + set port), operate (verify DNS and service health)
- **Add tracing**:
  1. tracing: enable it for the service in the correct environment with `set-service-tracing` or `railway trace enable`. Use SDK instrumentation, not automatic. Add spans around inbound work, I/O, and logical units. For a Function, edit its file with `get-function-source-code` / `update-function-source-code`.
  2. configure: set `OTEL_METRICS_EXPORTER`/`OTEL_LOGS_EXPORTER` and the start command.
  3. deploy: redeploy so that the service gets the `OTEL_*` variables.
  4. tracing: verify with `x-railway-trace-id` and `get-trace` or `railway trace get`. Then use `get-tracing-coverage` for the database and client spans.
- **Docs to action**: request (get the docs answer), then go to the applicable operational reference.

For a composed workflow, give one response for all steps. Do not ask the user to start each step separately.

## Setup decision flow

When the user wants to make or deploy something, find the correct action from the current context:

1. If the intent is deploy-from-cwd or signup-from-cwd, do not run `railway whoami`. Run `railway up` (or `railway up -y`) directly, as [Intent-based routing](#intent-based-routing) tells you. It does signup, project creation, service creation, and deploy in one sequence. For other setup flows that need workspace/account context first, run `railway whoami --json`. If it fails with an auth error, the user has no token. Go to [Account creation & sign-in](#account-creation--sign-in).
2. Run `railway status --json` in the current directory.
3. **If linked**: add a service to the existing project (`railway add --service <name>`). Do not make a new project unless the user explicitly says "new project" or "separate project".
4. **If not linked**: examine the parent directory (`cd .. && railway status --json`).
   - **Parent linked**: this is probably a monorepo sub-app. Add a service and set `rootDirectory` to the sub-app path.
   - **Parent not linked**: run `railway list --json` and find a project with the same name as the directory.
     - **Match found**: link to it (`railway link --project <name>`).
     - **No match**: make a new project (`railway init --name <name>`).
5. When there is more than one workspace, match by name from `railway whoami --json`.

**Naming rule**: app names such as "flappy-bird" or "my-api" are service names, not project names. Use the directory name or the repo name for the project.

## Response format

Keep the response short. For operational responses, give:
1. The result (IDs, status, key output).
2. The next step, or a statement that the task is complete.

Include command output only when it helps the user understand what occurred.
