---
name: vercel-cli
description: Vercel CLI (`vercel`, `vc`) guidance. Use when you deploy to Vercel, link projects, manage env vars, domains, or feature flags, read logs, metrics, or traces, or debug a deployed app (errors, 5xx, timeouts, slow routes, one failed request).
---

# Vercel CLI Skill

The Vercel CLI (`vercel` or `vc`) deploys, manages, and develops projects on the Vercel platform from the command line. For all flags of a command, use `vercel <command> --help`.

The installed CLI help is the source of truth for rare or new flags. If an example here is not sufficient, check `vercel <command> --help` before you act. Do not guess.

Parse only stdout for URLs and JSON. Warnings, progress, and `--help` output go to stderr. Merge the streams only when you search help text. Some help commands exit with code 2 after they print usage. If the usage text prints, the help read is successful.

In agent or non-interactive mode, many commands report errors and required confirmations as one JSON object on stdout. The object has `status`, `reason`, `hint`, and `next` (follow-up commands that you can run).

- Use a suggested `next` command instead of a retry that you write yourself. First, confirm that it keeps the target and authorization that the user intends.
- Do not automatically run follow-up commands that link, authenticate, or mutate.
- Read commands such as `list`, `logs`, `inspect`, and `api` keep their usual output shape.

## Critical: Project Linking

The project context depends on the working directory of the command. Before an important read or mutation:

1. Run `vercel project inspect --non-interactive` from the intended directory.
2. Confirm the reported owner and project.
3. If you get `link_required` or a target mismatch, stop. Do not link automatically.

In non-interactive mode, this command only resolves context that already exists.

Many commands that use a project also accept `--project <name-or-id>` with `--scope <team>`. This sets an explicit target for one command. Before you use them, confirm that the target and the scope agree with the intent of the user.

- **`<cwd>/.vercel/project.json`**: `vercel link` creates it. This link for the exact working directory has priority over a repository link. When you run the CLI from a random subdirectory, it usually does not inherit a root `project.json`.
- **`<repo-root>/.vercel/repo.json`**: `vercel link --repo` creates it. The CLI selects the deepest project directory that contains the working directory.
- **Unmatched repository path**: If no repo mapping contains the working directory, interactive repo resolution asks the user to select one of the configured projects. Non-interactive repo resolution currently selects the only configured project. If there are many projects, it stays unresolved. Commands that set up projects can then start a link flow. Thus, non-interactive mode does not always fail closed.

A working directory inside an app directory does not prove that the CLI selected the intended project. Check the resolved project explicitly, especially when no repo mapping covers that directory.

`vercel whoami --format json` shows the authenticated user and the effective team. Plain `vercel whoami` without a TTY prints only the username. Neither command verifies the linked project. Read-only project commands can also need a login or a team SAML re-authentication, and can open a browser or device flow. Ask the user to complete that flow before you continue.

## Quick Start

```bash
npm i -g vercel
vercel login
vercel link              # single project
# OR
vercel link --repo       # monorepo
vercel pull
vercel dev        # local development
vercel deploy     # preview deployment
vercel --prod     # production deployment
```

## Decision Tree

Use this list to find the correct reference file:

- **Deploy, redeploy, forced builds, no-cache builds, or deployment source/provenance** → `references/deployment.md`
- **Rolling releases, deploy hooks, cron jobs, cache, git connection, Edge Config, redirects, custom environments** → `references/project-infra.md`
- **Local development** → `references/local-development.md`
- **Environment variables** → `references/environment-variables.md`
- **CI/CD automation** → `references/ci-automation.md`
- **Domains or DNS** → `references/domains-and-dns.md`
- **Projects or teams** → `references/projects-and-teams.md`
- **Vercel Toolbar comments (`vercel comments`)** → `references/comments.md`
- **Build failures, deployment errors, logs, metrics, Speed Insights, Core Web Vitals, activity, performance, preview access, or production debugging** → `references/monitoring-and-debugging.md`
- **Alerts, usage, contracts, billing purchases, tokens, telemetry, or CLI upgrades** → `references/platform-ops.md`
- **Blob storage** → `references/storage.md`
- **Container Registry (`vercel vcr`: repositories, images, tags, docker/podman/buildah login, push/pull)** → `references/container-registry.md`
- **Integrations (databases, storage, and others)** → `references/integrations.md`
- **Connectors (`vercel connect`)** → `references/connectors.md`
- **Routing rules** → `references/routing.md`
- **Firewall (WAF rules, IP blocks, rate limiting)** → `references/firewall.md`
- **Access a preview deployment** → use `vercel curl` (see `references/monitoring-and-debugging.md`)
- **A CLI command is not available, or its output does not have the required fields** → use `vercel api` only after the first-class CLI paths are not available or not sufficient (see `references/advanced.md`)
- **Node.js backends (Express, Hono, and others)** → `references/node-backends.md`
- **Monorepos (Turborepo, Nx, workspaces)** → `references/monorepos.md`
- **Bun runtime** → `references/bun.md`
- **Feature flags (`vercel flags`: create, inspect, set, split, rollout, rules, segments, sdk-keys)** → `references/flags.md`
- **Microfrontends** → `references/microfrontends.md`
- **Sandbox** → `references/sandbox.md`
- **Agent, MCP, skills discovery, or AI Gateway** → `references/agent-and-ai.md`
- **Captured request traces (`vercel traces`, including `--open` / `--view`)** → `references/advanced.md`. For span search, trace inspection, sampling rules, and OpenTelemetry setup, also read the current Vercel docs.
- **Advanced (`vercel api` fallback, webhooks)** → `references/advanced.md`
- **Global flags** → `references/global-options.md`
- **First-time setup** → `references/getting-started.md`

## Anti-Patterns

- **Incorrect link type in a monorepo with many projects**: `vercel link` creates `project.json`, which tracks only one project. Use `vercel link --repo` instead. When a problem occurs, check `.vercel/` first.
- **Commands that link automatically in monorepos**: If `.vercel/` does not exist, many commands run `vercel link` implicitly. This creates `project.json`, which can be incorrect. Run `vercel link` (or `--repo`) explicitly first.
- **The assumption that an app subdirectory sets the project**: Verify with `vercel project inspect --non-interactive`. In non-interactive mode, an unmatched repo path can currently fall back to the only configured project.
- **`vercel whoami` used to verify the linked project**: `vercel whoami --format json` shows the authentication and team context. It does not show the selected project.
- **No non-interactive flags in plain CI runs**: Detected agents get `--non-interactive` by default. Plain CI does not. Pass it explicitly in CI. Add `--yes` only for commands that need confirmation.
- **`vercel deploy` after `vercel build` without `--prebuilt`**: The deploy ignores the build output.
- **`vercel redeploy` for no-cache rebuilds**: `vercel redeploy` has no no-cache flag. For a fresh deployment without build cache, use `vercel deploy --force` without `--with-cache`.
- **Tokens hardcoded in flags**: Use the `VERCEL_TOKEN` environment variable, not `--token`.
- **Deployment protection disabled**: To access preview deployments, use `vercel curl` instead.
- **`vercel api` used too early**: Use first-class CLI commands when they give the necessary data or mutation.
