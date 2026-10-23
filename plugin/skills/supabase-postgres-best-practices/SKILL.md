---
name: supabase-postgres-best-practices
description: "Postgres best practices from Supabase, for all Postgres databases. Load before you change tables, columns, migrations, RLS, indexes, triggers, functions, pg_cron, pgmq, pgvector, or imports, and when you debug slow queries, EXPLAIN, connections, locks, or bloat."
license: MIT
metadata:
  author: supabase
  version: "1.1.1"
  organization: Supabase
  date: January 2026
  abstract: Postgres performance guide for developers who use Supabase and Postgres. It has rules in 8 categories, in sequence of impact, from critical (query performance, connection management) to incremental (advanced features). Each rule has an explanation, incorrect and correct SQL examples, query plan analysis, and performance metrics for automated optimization and code generation.
---

# Supabase Postgres Best Practices

This is a Postgres performance guide from Supabase. It has rules in 8 categories, in sequence of impact. Use it for query optimization and schema design.

This skill is not only about performance. Schema, migration, security, and SQL tasks must also follow these rules, also for a one-column change or one query.

## When to apply

Use these guidelines when you:
- Write SQL queries or design schemas, including the selection of column types.
- Write migrations or declarative schema files.
- Add indexes or optimize queries.
- Write RLS policies and the tests that verify them.
- Write triggers, database functions, queues, or scheduled jobs (pg_cron, pgmq).
- Add vector or semantic search (pgvector).
- Restore dumps (pg_restore) or import data.
- Review database performance problems: slow queries, high CPU, timeouts, EXPLAIN plans, connection exhaustion, locking, or bloat.
- Configure connection pooling or scaling.
- Use features that are specific to Postgres.
- Find why the wrong user or tenant can see rows.

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to use

Read the rule files for explanations and SQL examples:

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

Each rule file has:
- A short explanation of why the rule is important
- An incorrect SQL example with an explanation
- A correct SQL example with an explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Notes for Supabase (when applicable)

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
