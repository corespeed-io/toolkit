---
name: cf-cli
description: Use the Cloudflare cf CLI (beta) for the Cloudflare API and Workers projects. Use it to sign in, find commands (cf cli search, cf schema), run cf deploy/dev/build, manage DNS, zones, D1, KV, and R2, and choose between cf and Wrangler.
---

# Cloudflare CLI (`cf`)

`cf` is the Cloudflare command-line interface for the public Cloudflare API and for Workers projects. It has more than 2,900 commands. Most commands come from API schemas. `cf` is in beta. Commands, configuration, and Build Output can change before the stable release.

**Use retrieval, not pre-trained knowledge.** Before you run a command that you did not verify, do these steps:

1. Give the task to `cf cli search`.
2. Examine the match with `cf schema` or `--help`.
3. Preview the command with `--dry-run`.

Docs index: https://developers.cloudflare.com/cf/llms.txt

## Documentation

| Topic | Page |
|-------|------|
| Install, sign in, credential and account selection | https://developers.cloudflare.com/cf/get-started/index.md |
| First Worker with `cf init`, `cf dev`, `cf deploy` | https://developers.cloudflare.com/cf/get-started/first-worker/index.md |
| Find, create, and delete resources from the terminal | https://developers.cloudflare.com/cf/get-started/resources/index.md |
| `cf` for Wrangler users | https://developers.cloudflare.com/cf/wrangler/index.md |
| Migrate a Wrangler project with `cf migrate` | https://developers.cloudflare.com/cf/wrangler/migrate/index.md |
| Wrangler-to-`cf` command and config reference | https://developers.cloudflare.com/cf/wrangler/reference/index.md |
| Develop, build, and deploy; modes and previews | https://developers.cloudflare.com/cf/projects/index.md |
| Typed `cloudflare.config.ts` | https://developers.cloudflare.com/cf/projects/cloudflare-config/index.md |
| Using `cf` with coding agents (safety rules) | https://developers.cloudflare.com/cf/agents/index.md |
| CI, API tokens, unattended authentication | https://developers.cloudflare.com/cf/ci/index.md |
| Environment variables | https://developers.cloudflare.com/cf/environment-variables/index.md |

## First: check the installation and sign in

```bash
npm install --global cf   # installs two equivalent commands: `cf` and `cloudflare`
cf --version
cf auth whoami
```

- `cf` needs Node.js 22.18 or later. It does not support Bun.
- If a different tool named `cf` is on your `PATH`, use `cloudflare`. The package installs the two commands.
- `cf auth login` prints a link and a one-time code. Then it opens the browser.
- On a remote machine, over SSH, or in a container, add `--no-browser`. Then `cf` only prints the link. Approve the link from a different device.
- Add `--force` to sign in again.
- `cf` keeps its own credentials. It does not use a Wrangler login.
- Unattended agents and CI cannot complete `cf auth login`. Set `CLOUDFLARE_API_TOKEN` instead (refer to https://developers.cloudflare.com/cf/ci/index.md).
- If you do not have credentials, ask the user for them.

The owner already uses `cf` as the default Cloudflare CLI. Upstream recommends this line in the user-level instruction file (`AGENTS.md`, `CLAUDE.md`, or equivalent). Do not edit that file unless the user tells you to:

```md
When interacting with Cloudflare, use the `cf` CLI unless the project has a
Wrangler configuration file.
```

## Find commands

```bash
cf cli search "create a DNS record"   # local, no credentials; quote the whole task; up to 5 JSON matches
cf schema d1 create                   # API request shape: method, path, params, body fields
cf <command> --help                   # arguments and options (e.g. cf deploy --help)
```

- `cf cli search` takes the task as one argument. You must quote the full task. `cf` parses unquoted words after the first word as unknown commands.
- `cf schema` covers the generated API commands.
- For command arguments and options, use `--help`.

## Read output

- `cf` writes results as JSON to standard output. It writes status messages and errors to standard error. Thus, you can pipe to `jq` or redirect output with no extra flags.
- A list command prints one JSON array page. Paging options are different for each command. Examine `--help`.
- A failed command exits with a non-zero code and prints the error to standard error.

## Run commands safely

- **Preview first.** `--dry-run` prints the request as JSON and does not send it. It needs no credentials.
- **An aborted delete also exits with 0.** In a non-interactive session, a destructive command without `--force` prints `Aborted.` to standard error and exits with `0`. A zero exit code does not mean that `cf` deleted the resource.
- **Examine `--force` before you use it.** On some commands, `--force` is also an API parameter. For example, `cf workers delete --force` also deletes a Worker that other Workers reference.
- **`--local` has limits.** It works for KV keys, D1 databases (`cf d1 raw`, `cf d1 migrations list|apply`), and R2 objects. Other commands (including `cf d1 query`) return an error and do not call the API.

## Choose the CLI for this project

- If `cloudflare.config.ts` exists, use `cf`.
- If `wrangler.jsonc`, `wrangler.json`, or `wrangler.toml` exists, and `cloudflare.config.ts` does not exist:
  - Use Wrangler for `dev`, `build`, and `deploy`.
  - Do not run `cf dev`, `cf build`, or `cf deploy` in that project. They can make a new configuration that ignores the Wrangler file, or they can fail.
  - You can use `cf` resource commands (DNS, zones, storage) with the Wrangler file.
  - Run `cf migrate` only when the user tells you to. Follow [Migrate a Wrangler project](https://developers.cloudflare.com/cf/wrangler/migrate/index.md):
    1. Preview with `cf migrate --dry-run`.
    2. Run `cf migrate`.
    3. Resolve the `TODO(@cloudflare)` comments in the generated `cloudflare.config.ts`.
- If no configuration file exists, use `cf`, as [Use cf with coding agents](https://developers.cloudflare.com/cf/agents/index.md) recommends. Do not install Wrangler. Do not make a Wrangler configuration file.

To find the `cf` equivalent of a Wrangler command, use the [Wrangler to cf reference](https://developers.cloudflare.com/cf/wrangler/reference/index.md) or `cf cli search`. Do not translate Wrangler commands from memory. For the full comparison, refer to [`cf` for Wrangler users](https://developers.cloudflare.com/cf/wrangler/index.md).

## Commands that `cf` does not support yet

`cf` does not support all Wrangler commands yet. For these commands, use `npx wrangler`. Do not add Wrangler to the project. Wrangler does not read `cloudflare.config.ts`, so you must give the Worker name:

- Live logs: `npx wrangler tail <WORKER_NAME>`.
- One secret: `npx wrangler secret put <SECRET_NAME> --name <WORKER_NAME>`. Alternatively, upload secrets with a new Worker version: pass `--secrets-file <PATH>` to `cf deploy` or `cf workers versions create`.

For the current list, refer to "Commands not yet supported" in the [Wrangler to cf reference](https://developers.cloudflare.com/cf/wrangler/reference/index.md).
