---
name: deployments-cicd
description: Vercel deployment and CI/CD guidance. Use when you deploy, promote, roll back, or inspect Vercel deployments, build with `--prebuilt`, or write CI workflows (GitHub Actions, GitLab CI, Bitbucket Pipelines) that deploy to Vercel.
---

# Vercel Deployments & CI/CD

This skill covers Vercel deployment workflows: `vercel deploy`, `vercel promote`, `vercel rollback`, `vercel inspect`, and `vercel build`. It also covers CI/CD pipelines with GitHub Actions, GitLab CI, and Bitbucket Pipelines.

## Deployment Commands

### Preview Deployment

```bash
# Deploy from project root (creates preview URL)
vercel

# Equivalent explicit form
vercel deploy
```

With the Git integration, Vercel automatically creates a preview deployment for each push to a branch that is not the production branch. Each preview deployment has a unique URL for tests.

### Production Deployment

```bash
# Deploy directly to production
vercel --prod
vercel deploy --prod

# Force a new deployment (skip cache)
vercel --prod --force
```

### Build Locally, Deploy Build Output

```bash
# Build locally (uses preview env vars by default)
vercel build

# Build with production env vars
vercel build --prod

# Deploy only the build output (no remote build)
vercel deploy --prebuilt
vercel deploy --prebuilt --prod
```

**When to use `--prebuilt`:** Use it in custom CI pipelines where:
- You control the build step.
- You need build caching at the CI level.
- You must run tests between the build and the deploy.

**Prebuilt limits:** [System Environment Variables are missing at build time](https://vercel.com/docs/cli/deploy#when-not-to-use---prebuilt). Next.js Skew Protection needs a [custom deployment ID](https://vercel.com/docs/skew-protection#custom-deployment-id).

### Promote & Rollback

```bash
# Stage a production deployment without assigning domains
vercel deploy --prod --skip-domain

# Promote it (instant, no rebuild)
vercel promote <deployment-url-or-id>

# Show pending rollback status (no argument does not roll back)
vercel rollback status

# Rollback to a specific deployment
vercel rollback <deployment-url-or-id>
```

**Promote a production deployment, not a preview.** The promotion of a staged production deployment is instant and serves the same build. The promotion of a preview rebuilds it with production environment variables. Then the released build is not the build that you tested.

**A rollback turns off auto-assignment.** New production pushes do not go live until `vercel promote` turns it on again.

### Inspect Deployments

```bash
# View deployment details (build info, functions, metadata)
vercel inspect <deployment-url>

# List recent deployments
vercel ls

# View recent runtime logs for a deployment
vercel logs --deployment <url>
```

## CI/CD Integration

### When to Add a CI Pipeline

The Git integration builds each push, posts preview URLs on pull requests, and deploys the production branch. Use CI for the jobs that Vercel does not run: tests, security scans, performance budgets, and approval gates. Use [Deployment Checks](references/deployment-checks.md) to make releases wait for these jobs while Vercel continues to build. Deploy from CI only when the build must run in your runner. Examples: to keep source code off Vercel, or for GitHub Enterprise Server.

### Required Environment Variables

Each CI pipeline needs these three variables:

```bash
VERCEL_TOKEN=<your-token>        # Personal or team token
VERCEL_ORG_ID=<org-id>           # From .vercel/project.json
VERCEL_PROJECT_ID=<project-id>   # From .vercel/project.json
```

Set these as secrets in your CI provider. Do not commit them to source control. The CLI reads `VERCEL_TOKEN` from the environment. Do not pass `--token`, because it shows the token in process lists and logs.

### GitHub Actions

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]

env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production

      - name: Build
        run: vercel build --prod

      - name: Deploy
        run: vercel deploy --prebuilt --prod
```

### Other CI Pipelines and Backend Access

| Task | Read |
| --- | --- |
| Post preview URLs on pull requests from GitHub Actions, or deploy from GitLab CI or Bitbucket Pipelines | [references/cli-pipelines.md](references/cli-pipelines.md) |
| Let deployed functions reach AWS, GCP, or Vault without static secrets (OIDC federation) | [references/oidc-federation.md](references/oidc-federation.md) |
| Deployment Checks, or testing protected deployments from CI | [references/deployment-checks.md](references/deployment-checks.md) |
| Live status (MCP) | [references/live-status.md](references/live-status.md) |

## Common CI Patterns

### Release Only Tested Builds

With Git deployments, require [Deployment Checks](references/deployment-checks.md). When CI deploys with the CLI:

1. Stage a production deployment.
2. Test it.
3. Promote that build.

```yaml
env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  stage:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    steps:
      # ... checkout, install, vercel pull --environment=production, vercel build --prod ...
      - id: deploy
        run: echo "url=$(vercel deploy --prebuilt --prod --skip-domain)" >> $GITHUB_OUTPUT

  e2e-tests:
    needs: stage
    runs-on: ubuntu-latest
    steps:
      # ... checkout, install, bypass header in playwright.config.ts (see references/deployment-checks.md) ...
      - run: npx playwright test
        env:
          BASE_URL: ${{ needs.stage.outputs.url }}
          VERCEL_AUTOMATION_BYPASS_SECRET: ${{ secrets.VERCEL_AUTOMATION_BYPASS_SECRET }}

  promote:
    needs: [stage, e2e-tests]
    runs-on: ubuntu-latest
    steps:
      - run: npm install -g vercel
      - run: vercel promote ${{ needs.stage.outputs.url }}
```

## Global CLI Flags for CI

| Flag | Purpose |
|------|---------|
| `--token <token>` | Authenticate. In CI, set `VERCEL_TOKEN` instead |
| `--yes` / `-y` | Skip confirmation prompts |
| `--scope <team>` | Run as a specific team |
| `--cwd <dir>` | Set the working directory |

## Best Practices

1. **Use `--prebuilt` in CI.** It separates the build from the deploy. It also enables build caching and test gates.
2. **Use `vercel pull` before the build.** It gets the correct environment variables and project settings.
3. **Release only tested builds.** Use Deployment Checks (Git) or staged production builds (CLI).
4. **Use OIDC federation for runtime access to backends.** Vercel functions can then authenticate to AWS or GCP without static secrets. It does not replace `VERCEL_TOKEN` for the CLI.
5. **Pin the Vercel CLI version in CI.** `npm install -g vercel@latest` can break the pipeline without warning.
6. **Add the `--yes` flag in CI.** It prevents interactive prompts that stop the pipeline.

## Deployment Strategy Matrix

| Scenario | Strategy | Commands |
|----------|----------|----------|
| Standard team workflow | Git-push deploy | Push to main/feature branches |
| Custom CI/CD (Actions, CircleCI) | Prebuilt deploy | `vercel build && vercel deploy --prebuilt` |
| Monorepo with Turborepo | Affected + remote cache | `turbo run build --affected` |
| Preview for every PR | Default behavior | Creates a preview URL for each branch automatically |
| Release a tested build | Deployment Checks (Git) or staged production (CLI) | Required checks, or `vercel deploy --prod --skip-domain` → test → `vercel promote <url>` |
| Atomic deploys with DB migrations | Two-phase | Run migration → verify → `vercel promote` |
| Latency-sensitive regional data | Vercel Functions | Keep the Node.js default. Set the function region near the data |

## Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ERR_PNPM_OUTDATED_LOCKFILE` | The lockfile does not match `package.json` | Run `pnpm install`, then commit the lockfile |
| `NEXT_NOT_FOUND` | The root directory is configured incorrectly | Set Root Directory in Project Settings |
| `Invalid next.config.js` | Syntax error in the config | Validate the config locally with `next build` |
| `functions/api/*.js` mismatch | Incorrect file structure | Move the files to the `app/api/` directory (App Router) |
| `Error: EPERM` | File permission problem in the build | Do not use `chmod` in build scripts. Use `postinstall` |

## Deploy Summary Format

Show the deploy result in this structured block:

```
## Deploy Result
- **URL**: <deployment-url>
- **Target**: production | preview
- **Status**: READY | ERROR | BUILDING | QUEUED
- **Commit**: <short-sha>
- **Framework**: <detected-framework>
- **Build Duration**: <duration>
```

If the deployment failed, add:

```
- **Error**: <summary of failure from logs>
```

For production deploys, also add:

```
### Post-Deploy Observability
- **Error scan**: <N errors found / clean> (scanned via vercel logs -q level:error --since 1h)
- **Drains**: <N configured / none>
- **Monitoring**: <active / gaps identified>
```

## Deploy Next Steps

Tell the user the next step that agrees with the deployment result:

- **Success (preview)** → "Open the preview URL to verify it. When it is ready, deploy to production with `vercel --prod`, or stage with `vercel deploy --prod --skip-domain` and then `vercel promote <url>`."
- **Success (production)** → "Your production site is live. Run `vercel inspect <url>` or `vercel ls` to see the project status."
- **Build error** → "Read the build logs above. Frequent fixes: verify the `build` script in `package.json`, find missing environment variables with `vercel env ls`, and make sure that the dependencies are installed."
- **Missing env vars** → "Run `vercel env pull` to get the environment variables locally, or `vercel env ls` to see the variables configured on Vercel."
- **Monorepo issues** → "Set the Root Directory in Project Settings to the folder of the app. `vercel.json` has no `rootDirectory` key."
- **Post-deploy errors detected** → "Examine the errors above. Run `vercel logs --deployment <url> -q level:error` for details. If drains are configured, compare with the external monitoring."
- **No monitoring configured** → "Set up drains or install an error-tracking integration before the next production deploy."

## Official Documentation

- [Deployments](https://vercel.com/docs/deployments)
- [Vercel CLI](https://vercel.com/docs/cli)
- [GitHub Actions](https://vercel.com/docs/git/vercel-for-github)
- [GitLab CI](https://vercel.com/docs/git/vercel-for-gitlab)
- [Bitbucket Pipelines](https://vercel.com/docs/git/vercel-for-bitbucket)
- [OIDC Federation](https://vercel.com/docs/oidc)
