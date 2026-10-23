---
name: env-vars
description: Vercel environment variable guidance. Use when you work with .env files, `vercel env` commands (pull, add, ls, rm, run), Secret or Config variable types, VERCEL_OIDC_TOKEN, or configuration for each environment (production, preview, development).
---

# Vercel Environment Variables

This skill covers Vercel environment variable management: `.env` file conventions, the `vercel env` CLI, the OIDC token lifecycle, and configuration for each environment.

## .env File Hierarchy

Vercel and Next.js load environment variables in a specific order. Later files override earlier files:

| File | Purpose | Git-tracked? |
|------|---------|-------------|
| `.env` | Default values for all environments | Yes |
| `.env.local` | Local overrides and secrets | **No** (gitignored) |
| `.env.development` | Defaults for development | Yes |
| `.env.development.local` | Local overrides for development | **No** |
| `.env.production` | Defaults for production | Yes |
| `.env.production.local` | Local overrides for production | **No** |
| `.env.test` | Defaults for tests | Yes |
| `.env.test.local` | Local overrides for tests | **No** |

### Load Order (Next.js)

1. `.env` (lowest priority)
2. `.env.[environment]` (development, production, or test)
3. `.env.local` (skipped in the test environment)
4. `.env.[environment].local` (highest priority)

### Critical Rules

- **Do not commit secrets** to `.env`, `.env.development`, or `.env.production`. Use the `.local` variants or Vercel environment variables.
- Next.js always gitignores `.env.local`. `vercel env pull` writes secrets to this file.
- Variables with the `NEXT_PUBLIC_` prefix go into the browser bundle. Do not put secrets in `NEXT_PUBLIC_` variables.
- All other variables are available only on the server (API routes, Server Components, middleware).

## vercel env CLI

### Pull Environment Variables

```bash
# Pull all env vars for the current environment into .env.local
vercel env pull .env.local

# Pull for a specific environment
vercel env pull .env.local --environment=production
vercel env pull .env.local --environment=preview
vercel env pull .env.local --environment=development

# Overwrite existing file without prompting
vercel env pull .env.local --yes

# Pull to a custom file
vercel env pull .env.production.local --environment=production
```

### Add Environment Variables

Each variable has a type:

| Type | After saving | Use for |
|------|--------------|---------|
| **Secret** | Hidden in the dashboard and in `vercel env ls`. You can replace it, but you cannot read it back. `vercel env pull` does not return Production and Preview Secrets. | Passwords, API keys, tokens, database URLs |
| **Config** | Members with access can read it | Values that are not sensitive and that you must read later |

Deployments get both types at build time and at runtime. Secret and Config replaced the Sensitive toggle. Existing Sensitive variables are now Secrets.

```bash
# Interactive — prompts for value, environments, and type
vercel env add MY_SECRET

# Non-interactive: read the value from a file so it never lands in shell
# history or process arguments (echo "value" | ... and --value do both)
vercel env add MY_SECRET production < ./secret.txt

# Add to production and preview in one command
vercel env add MY_SECRET production,preview < ./secret.txt

# Set the type explicitly
vercel env add MY_SECRET production --type secret < ./secret.txt
vercel env add SITE_REGION production --type config < ./region.txt

# Add development in its own command; development-only adds default to Config
vercel env add MY_SECRET development < ./dev-secret.txt

# Update an existing value
vercel env update MY_SECRET production < ./secret.txt
```

- **Defaults**: A non-interactive add to production, preview, or a custom environment stores the variable as Secret.
- **Public prefixes are always Config**: Variables such as `NEXT_PUBLIC_*` or `VITE_*` go to browsers. Thus, the CLI refuses `--type secret` for them. Keep a private value under a name without the prefix.
- **Flags**: `--type config|secret` needs Vercel CLI 59.6 or later. Older CLIs use `--visibility`, which is now a deprecated alias of `--type`. `--sensitive` (Secret) and `--no-sensitive` (Config) work in all versions.
- **Team policy**: The **Separate Production Secret Values** policy requires a Production Secret to be different from the Preview, Development, and custom environment values of the same key. With this policy, create separate Production and non-Production values. Do not add one value to all targets. This policy replaces the deprecated **Enforce Sensitive Environment Variables** policy.

### List Environment Variables

```bash
# List all environment variables
vercel env ls

# Filter by environment
vercel env ls production
```

### Remove Environment Variables

```bash
# Remove from specific environment
vercel env rm MY_SECRET production

# Remove from all environments
vercel env rm MY_SECRET
```

## Bootstrap Flow (Fresh Clone / New Machine)

Use this sequence to set up a project from the start:

```bash
# 1) Link first so pulls target the correct Vercel project
vercel link --yes --project <name-or-id> --scope <team>

# 2) Pull env vars into .env.local
vercel env pull .env.local --yes

# 3) Verify required keys from .env.example exist in .env.local
while IFS='=' read -r key _; do
  [[ -z "$key" || "$key" == \#* ]] && continue
  grep -q "^${key}=" .env.local || echo "Missing in .env.local: $key"
done < .env.example
```

### Temporary Path: Run With Vercel Envs Without Writing a File

If you need Vercel environment variables now, but you do not want to write `.env.local` yet:

```bash
vercel env run -- npm run dev
```

This is useful for a quick check during bootstrap. For a usual local workflow, pull `.env.local` anyway.

### Re-pull After Secret or Provisioning Changes

Run this command again after one of these changes:

- You create or update secrets (`vercel env add`, or changes in the dashboard).
- You provision integrations that add environment variables (for example, Neon or Upstash).

```bash
vercel env pull .env.local --yes
```

## OIDC Token Lifecycle

Vercel uses **OIDC (OpenID Connect)** tokens for secure authentication without keys between your app and Vercel services (AI Gateway, storage, and others).

### How It Works

1. **On Vercel deployments**: Vercel automatically injects `VERCEL_OIDC_TOKEN` as a short-lived JWT and refreshes it automatically. No configuration is necessary.
2. **Local development**: `vercel env pull .env.local` provisions a `VERCEL_OIDC_TOKEN` that is valid for approximately 12 hours.
3. **Token expiry**: When the local OIDC token expires, run `vercel env pull .env.local --yes` again to get a new token. To prevent authentication failures during a session, pull again at the start of each development session.

### Common OIDC Patterns

```ts
// The @vercel/oidc package reads VERCEL_OIDC_TOKEN automatically
import { getVercelOidcToken } from '@vercel/oidc'

// AI Gateway uses OIDC by default — no manual token handling needed
import { gateway } from 'ai'
const result = await generateText({
  model: gateway('openai/gpt-5.2'),
  prompt: 'Hello',
})
```

### Troubleshooting OIDC

| Symptom | Cause | Fix |
|---------|-------|-----|
| `VERCEL_OIDC_TOKEN` missing locally | You did not pull the environment variables | `vercel env pull .env.local` |
| Authentication errors locally after approximately 12h | The token expired | `vercel env pull .env.local --yes` |
| Works on Vercel, fails locally | The token is not in `.env.local` | `vercel env pull .env.local` |
| `AI_GATEWAY_API_KEY` vs OIDC | Both are set, and the key has priority | Remove `AI_GATEWAY_API_KEY` to use OIDC |

## Environment-Specific Configuration

### Vercel Dashboard vs .env Files

| Use Case | Where to Set |
|----------|-------------|
| Secrets (API keys, tokens) | Vercel Dashboard (`https://vercel.com/{team}/{project}/settings/environment-variables`) or `vercel env add`, as type Secret |
| Public config (site URL, feature flags) | `.env` or `.env.[environment]` files |
| Local-only overrides | `.env.local` |
| CI/CD secrets | Vercel Dashboard (`https://vercel.com/{team}/{project}/settings/environment-variables`) with environment scoping |

### Environment Scoping on Vercel

In the Vercel Dashboard at `https://vercel.com/{team}/{project}/settings/environment-variables`, you can scope variables to:

- **Production**: deployments on the production domain
- **Preview**: branch and PR deployments
- **Development**: `vercel dev` and `vercel env pull`

You can assign a variable to one, two, or all three environments.

### Git Branch Overrides

You can scope Preview environment variables to specific Git branches:

```bash
# Add a variable only for the "staging" branch
vercel env add DATABASE_URL preview --git-branch=staging < ./staging-database-url.txt
```

## Gotchas

### `vercel env pull` Merges Into an Existing File

`vercel env pull .env.local` merges into an existing file:

- It keeps variables that are defined only locally. It logs them as `Kept <KEYS>` (Vercel CLI 56+).
- Keys that also exist on Vercel get the pulled value. Thus, a local override of such a key is replaced.
- Current CLIs keep a real local value for a Secret that they cannot read.
- Current CLIs always refresh `VERCEL_OIDC_TOKEN`.

Older CLIs replace the full file. With an older CLI, back up custom variables first:

```bash
# Save custom vars before pulling
grep -v '^#' .env.local | grep -v '^VERCEL_\|^POSTGRES_\|^NEXT_PUBLIC_' > .env.custom.bak
vercel env pull .env.local --yes
cat .env.custom.bak >> .env.local  # Re-append custom vars
```

Alternatively, keep custom variables in a separate `.env.development.local` file. Next.js loads it after `.env.local`.

### Pulled Files Omit Production and Preview Secrets

`vercel env pull --environment=production` (or `preview`) does not write Secret values. Thus, a pulled file cannot reproduce production credentials. Keep separate Development values for local work. Do not try to copy production Secrets onto a machine.

### Scripts Don't Auto-Load `.env.local`

Only Next.js loads `.env.local` automatically. Standalone scripts (`drizzle-kit`, `tsx`, custom Node scripts) must load it explicitly:

```bash
# Use dotenv-cli
npm install -D dotenv-cli
npx dotenv -e .env.local -- npx drizzle-kit push
npx dotenv -e .env.local -- npx tsx scripts/seed.ts

# Or source manually
source <(grep -v '^#' .env.local | sed 's/^/export /') && node scripts/migrate.js
```

## Best Practices

1. **Use `vercel env pull` in your setup workflow.** Document it in your README.
2. **Do not hardcode secrets.** Always use environment variables.
3. **Keep the scope narrow.** Do not give preview deployments access to the production database.
4. **Refresh OIDC tokens regularly in local development.** Pull again when you see authentication errors.
5. **Use `.env.example`.** Commit a template with empty values, so that team members know which variables are necessary.
6. **Add the `NEXT_PUBLIC_` prefix to client-side variables.** Do not put secrets in them.
7. **Keep custom variables in `.env.development.local`.** This prevents `vercel env pull` from overwriting them.

## Official Documentation

- [Environment Variables](https://vercel.com/docs/environment-variables)
- [Vercel CLI: env](https://vercel.com/docs/cli/env)
- [Secret and Config types](https://vercel.com/changelog/environment-variables-now-use-config-and-secret-types)
- [Next.js Environment Variables](https://nextjs.org/docs/app/guides/environment-variables)
