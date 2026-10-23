---
name: supabase
description: "Use for all Supabase tasks: Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues, supabase-js, @supabase/ssr, RLS, JWT and session issues, Supabase CLI or MCP, migrations, extensions, and debugging Supabase errors or logs."
metadata:
  author: supabase
  version: "0.1.2"
---

# Supabase

## Core principles

**1. Supabase changes frequently. Verify against the changelog and the current docs before you make a change.**

Do not use training data for Supabase features. Function signatures, config.toml settings, and API conventions change between versions.

1. Get `https://supabase.com/changelog.md`. It is a small summary index.
2. Find the `breaking-change` tags that apply to your task. Follow the linked page for each one.
3. Find the applicable topic with the documentation methods below.

**2. Verify your work.**

After you make a fix, run a test query to make sure that the change works. A fix without verification is not complete.

**3. Recover from errors. Do not loop.**

If an approach fails after 2-3 attempts, stop and think again. Then do one or more of these:

- Try a different method.
- Read the documentation.
- Examine the error more carefully.
- Examine the applicable logs, if they are available.

Retrying the same command does not always solve a Supabase problem. The logs do not always contain the answer, but examine them before you continue.

**4. Exposing tables to the Data API.**

The [Data API settings](https://supabase.com/dashboard/project/<ref>/integrations/data_api/settings) of the user control this. Possibly the Data (REST) API does not expose new tables automatically. In that case, you must grant access to the `anon` and `authenticated` roles explicitly.

> This is different from RLS. RLS controls which _rows_ are visible when a table is accessible. It does not control whether the table is accessible.

When a user reports that a table made with SQL is not accessible:

1. Examine the Data API settings.
2. Examine whether an explicit `GRANT` gives the roles access.
3. When you grant public (`anon`/`authenticated`) access, always enable RLS too.

For the full setup procedure, refer to [Exposing a Table to the Data API](https://supabase.com/docs/guides/api/securing-your-api.md).

**5. RLS in exposed schemas.**

- Enable RLS on each table in each exposed schema. `public` is an exposed schema by default.
- This is critical in Supabase. When the `anon`/`authenticated` roles have access, the Data API can reach tables in exposed schemas (refer to [Exposing a Table to the Data API](https://supabase.com/docs/guides/api/securing-your-api.md)).
- For private schemas, use RLS as defense in depth.
- After you enable RLS, make policies that agree with the real access model. Do not give all tables the same `auth.uid()` pattern by default.

**6. Security checklist.**

Use this checklist for all Supabase tasks that touch auth, RLS, views, storage, or user data. These Supabase traps make vulnerabilities and do not show an error:

- **Auth and session security**
  - **Do not use `user_metadata` claims for JWT authorization decisions.** In Supabase, the user can edit `raw_user_meta_data`, and it can be in `auth.jwt()`. Thus, it is not safe for RLS policies or other authorization logic. Store authorization data in `raw_app_meta_data` / `app_metadata`.
  - **When you delete a user, the existing access tokens stay valid.**
    - Sign out or revoke sessions first.
    - For sensitive apps, keep the JWT expiry short.
    - For strict guarantees, validate `session_id` against `auth.sessions` on sensitive operations.
  - **If you use `app_metadata` or `auth.jwt()` for authorization, JWT claims can be old until the token of the user refreshes.**

- **API key and client exposure**
  - **Do not put the `service_role` or secret key in public clients.** Use publishable keys for frontend code. Legacy `anon` keys are only for compatibility. In Next.js, the browser gets all `NEXT_PUBLIC_` env vars.
  - **Use scoped personal access tokens for the Management API, CLI, and MCP server.**
    - A classic personal access token has full access to the account of the user, on all organizations and projects.
    - For scripts, CI, and agents, the user must make a scoped token. Limit it to the organizations, projects, and permissions that the task needs.
    - The [personal access tokens guide](https://supabase.com/docs/guides/platform/personal-access-tokens.md) lists the permission that each Management API endpoint and MCP tool needs. Find the permissions there. Do not guess.

- **RLS, views, and privileged database code**
  - **By default, views bypass RLS.** In Postgres 15 and higher, use `CREATE VIEW ... WITH (security_invoker = true)`. In older versions of Postgres, revoke access from the `anon` and `authenticated` roles, or put the views in a schema that is not exposed.
  - **UPDATE needs a SELECT policy.** In Postgres RLS, an UPDATE must first SELECT the row. Without a SELECT policy, updates return 0 rows. You get no error and no change.
  - **`auth.role()` is deprecated. Use the `TO` clause.** Supabase replaced `auth.role()` with `TO authenticated` or `TO anon` on the policy. Also, `auth.role() = 'authenticated'` fails silently when anonymous sign-ins are enabled. Anonymous users have the `authenticated` Postgres role, so they pass the check also when they did not sign in.
    ```sql
    -- Deprecated (do not use)
    create policy "example" on table_name for select
    using ( auth.role() = 'authenticated' );
    ```
  - **`TO authenticated` alone gives authentication without authorization (BOLA / IDOR).** `TO authenticated` only examines the role. It does not limit the rows that a user can access. Use `TO authenticated` together with an ownership predicate in `USING`:
    ```sql
    create policy "example" on table_name for select
    to authenticated
    using ( (select auth.uid()) = user_id );
    ```
  - **UPDATE policies need `USING` and `WITH CHECK`.** Without `WITH CHECK`, a user can change the `user_id` of a row to a different user:
    ```sql
    create policy "example" on table_name for update
    to authenticated
    using ( (select auth.uid()) = user_id )
    with check ( (select auth.uid()) = user_id );
    ```
  - **`SECURITY DEFINER` functions bypass RLS.** A `SECURITY DEFINER` function runs with the privileges of its creator. That is usually a role with `bypassrls` (for example, `postgres`). Do not add `SECURITY DEFINER` to solve a permission error. It removes access control silently and does not fix the cause. Use `SECURITY INVOKER`.
  - **All roles can call `SECURITY DEFINER` functions in `public`.** By default, Postgres grants `EXECUTE` to `PUBLIC` for each new function. Thus, a `SECURITY DEFINER` function in `public` is a public API endpoint. `anon` and `authenticated` inherit from `PUBLIC`, so they can call it without an additional grant. When you must use `SECURITY DEFINER` (for example, to bypass RLS on an internal lookup table):
    - Keep the function in a schema that is not exposed.
    - Always put an `auth.uid()` check in the function body.
    - Run `supabase db advisors` after the change.

- **Storage access control**
  - **Storage upsert needs INSERT + SELECT + UPDATE.** With only INSERT, new uploads work, but file replacement (upsert) fails silently. You must grant all three.

- **Dependency and supply-chain security**
  - **Always pin package versions and commit lockfiles** when you install Supabase packages (`supabase-js`, `@supabase/ssr`, `supabase-py`, and others). For the full checklist, refer to the [npm security guide](https://supabase.com/docs/guides/security/npm-security.md).

For a security concern that is not in this list, get the Supabase product security index: `https://supabase.com/docs/guides/security/product-security.md`

## Supabase CLI

Always find commands with `--help`. Do not guess. The CLI structure changes between versions.

```bash
supabase --help                    # All top-level commands
supabase <group> --help            # Subcommands (e.g., supabase db --help)
supabase <group> <command> --help  # Flags for a specific command
```

**Known Supabase CLI gotchas:**

- `supabase db query` needs **CLI v2.79.0+**. As an alternative, use MCP `execute_sql` or `psql`.
- `supabase db advisors` needs **CLI v2.81.3+**. As an alternative, use MCP `get_advisors`.
- The browser flow of `supabase login` makes a classic token with full account access. In CI, set `SUPABASE_ACCESS_TOKEN` to a scoped personal access token. It has priority over a saved login. The token permissions do not limit commands that connect with the database password (`--password` or `SUPABASE_DB_PASSWORD`, for example `supabase db push`).
- In imperative migration projects, make each new hand-written migration file with `supabase migration new <name>` first. Do not invent a migration filename. Do not use memory for the expected format. Declarative schema projects generate migrations from `supabase/schemas/`. Refer to "Making and committing schema changes" below.

**Version check and upgrade:** To examine the version, run `supabase --version`. For CLI changelogs and features of each version, refer to the [CLI documentation](https://supabase.com/docs/reference/cli/introduction) or [GitHub releases](https://github.com/supabase/cli/releases).

## Supabase MCP server

For setup instructions, the server URL, and configuration, refer to the [MCP setup guide](https://supabase.com/docs/guides/getting-started/mcp).

**Troubleshoot connection problems.** Do these steps in sequence:

1. **Examine whether the server is reachable:**
   `curl -so /dev/null -w "%{http_code}" https://mcp.supabase.com/mcp`
   A `401` is expected (no token). It means that the server is up. A timeout or "connection refused" means that the server can be down.

2. **Examine the MCP configuration of the tool:**
   - Claude Code: a project `.mcp.json`.
   - Codex: the `[mcp_servers]` section of `~/.codex/config.toml` (or the project `.codex/config.toml`).

   Make sure that the configuration has the correct server URL. If the entry is missing, add one that points to `https://mcp.supabase.com/mcp`.

3. **Authenticate the MCP server:**
   If the server is reachable and the configuration is correct, but you cannot see the tools, the user must authenticate. The Supabase MCP server uses OAuth 2.1. Tell the user to start the auth flow in their agent, complete it in the browser, and reload the session.
   In CI or other environments where the browser flow cannot run, send a scoped personal access token in the `Authorization: Bearer` header.

4. **Examine the scoped token permissions:**
   A tool can fail with "You do not have permission to perform this action" while you use a scoped personal access token. This means that the token does not have the permission for that tool, or the project is outside the token scope. Find the permission that the tool needs in the [personal access tokens guide](https://supabase.com/docs/guides/platform/personal-access-tokens.md#mcp-tools).

## Supabase documentation

Before you make a Supabase feature, find the applicable documentation. Use these methods in this sequence of priority:

1. **MCP `search_docs` tool.** This is the best method. It gives applicable snippets directly.
2. **Get docs pages as markdown.** To get a docs page as markdown, add `.md` to the URL path.
3. **Web search** for Supabase topics when you do not know which page to read.

## Making and committing schema changes

First, find which schema workflow the project uses.

### Option A: Declarative schemas

Use this option when `supabase/schemas/` exists or `config.toml` sets `schema_paths`.

1. Edit the desired schema state in those files.
2. Generate the migration and review it.

Do not start with a hand-written migration. Refer to the [Declarative database schemas guide](https://supabase.com/docs/guides/local-development/declarative-database-schemas).

### Option B: Imperative migrations

Use this option when the project does not use declarative schemas.

**To make schema changes, use `execute_sql` (MCP) or `supabase db query` (CLI).** These run SQL directly on the database and do not make migration history entries. Thus, you can change the SQL many times and then generate a clean migration.

Do not use `apply_migration` to change a local database schema. Each call writes a migration history entry. Thus, you cannot change the SQL again, and `supabase db diff` / `supabase db pull` give empty or conflicting diffs. If you use it, you must keep the SQL of the first call.

**When you are ready to put the changes in a migration file:**

1. **Run advisors:** `supabase db advisors` (CLI v2.81.3+) or MCP `get_advisors`. Fix all issues.
2. **Review the security checklist above** if the changes have views, functions, triggers, or storage.
3. **Generate the migration:** `supabase db pull <descriptive-name> --local --yes`
4. **Verify:** `supabase migration list --local`

## Debugging

You can get an error on a Supabase request. Examples:

- An error code from the Supabase REST API, the Postgres database, or PostgREST.
- An empty result.
- RLS blocks a request and you do not expect it.
- An error from a Supabase service: Auth, Realtime, Edge Functions, or Storage.

Before you diagnose or propose a fix, you **must** get the Supabase [Monitoring and Debugging](https://supabase.com/docs/guides/monitoring-and-debugging.md) documentation. Do not work from memory. These docs also cover performance problems, such as slow queries and missing indexes.

## Reference guides

- **Skill Feedback** → [references/skill-feedback.md](references/skill-feedback.md)
  You **must** read it when the user reports that this skill gave incorrect guidance or does not have necessary information.
