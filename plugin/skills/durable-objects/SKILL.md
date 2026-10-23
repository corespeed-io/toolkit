---
name: durable-objects
description: Build, debug, or review Cloudflare Durable Objects code for persistent state, coordination, RPC, alarms, WebSockets, and SQLite storage.
---

# Durable Objects

Use Durable Objects to build stateful, coordinated applications on the Cloudflare edge.

## Retrieval sources

Your knowledge of Durable Objects APIs and configuration can be old. **Use retrieval, not pre-training,** for all Durable Objects tasks.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/durable-objects/index.md |
| API Reference | https://developers.cloudflare.com/durable-objects/api/index.md |
| Best Practices | https://developers.cloudflare.com/durable-objects/best-practices/index.md |
| Examples | https://developers.cloudflare.com/durable-objects/examples/index.md |
| Roles and permissions | https://developers.cloudflare.com/workers/authorization/durable-objects/index.md |

When you make a feature, get the applicable doc page.

## When to use

- To make new Durable Object classes for stateful coordination.
- To make RPC methods, alarms, or WebSocket handlers.
- To review existing DO code for best practices.
- To configure DO bindings and migrations in wrangler.jsonc/toml or `cloudflare.config.ts`. For CLI commands, load the `cf-cli` skill.
- To write tests with the Cloudflare Vitest integration.
- To design sharding strategies and parent-child relationships.

## Reference documentation

- `./references/rules.md` - Core rules, storage, concurrency, RPC, alarms
- [Testing reference](./references/testing.md) - Current Vitest documentation, migration choices, and test selection
- `./references/workers.md` - Workers handlers, types, wrangler config, observability

Search: `blockConcurrencyWhile`, `idFromName`, `getByName`, `setAlarm`, `sql.exec`

## Core principles

### Use Durable Objects for

| Need | Example |
|------|---------|
| Coordination | Chat rooms, multiplayer games, collaborative docs |
| Strong consistency | Inventory, booking systems, turn-based games |
| Per-entity storage | Multi-tenant SaaS, per-user data |
| Persistent connections | WebSockets, real-time notifications |
| Scheduled work per entity | Subscription renewals, game timeouts |

### Do not use Durable Objects for

- Stateless request handling. Use plain Workers.
- Requirements for maximum global distribution.
- Many independent requests in parallel (high fan-out).

## Quick reference

### Wrangler configuration

This example uses `wrangler.jsonc`. In a `cf` project (`cloudflare.config.ts`), load the `cf-cli` skill and find the equivalent configuration in the [Wrangler to cf reference](https://developers.cloudflare.com/cf/wrangler/reference/index.md).

```jsonc
// wrangler.jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MY_DO", "class_name": "MyDurableObject" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDurableObject"] }]
}
```

### Basic Durable Object pattern

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MY_DO: DurableObjectNamespace<MyDurableObject>;
}

export class MyDurableObject extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => {
      this.ctx.storage.sql.exec(`
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          data TEXT NOT NULL
        )
      `);
    });
  }

  async addItem(data: string): Promise<number> {
    const result = this.ctx.storage.sql.exec<{ id: number }>(
      "INSERT INTO items (data) VALUES (?) RETURNING id",
      data
    );
    return result.one().id;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stub = env.MY_DO.getByName("my-instance");
    const id = await stub.addItem("hello");
    return Response.json({ id });
  },
};
```

## Critical rules

1. **Model around coordination atoms.** Use one DO for each chat room, game, or user. Do not use one global DO.
2. **Use `getByName()` for deterministic routing.** The same input gives the same DO instance.
3. **Use SQLite storage.** Configure `new_sqlite_classes` in migrations.
4. **Initialize in the constructor.** Use `blockConcurrencyWhile()` only for schema setup.
5. **Use RPC methods.** Do not use the fetch() handler (compatibility date >= 2024-04-03).
6. **Persist first, then cache.** You must write to storage before you update in-memory state.
7. **One alarm for each DO.** `setAlarm()` replaces the existing alarm.

## Authorization

Durable Objects do not have their own roles or permissions. Access follows the Worker that implements them.

1. Before you give observability or Data Studio access, get the current [Durable Objects authorization guidance](https://developers.cloudflare.com/workers/authorization/durable-objects/index.md).
2. Limit the Workers role to the intended Worker or Workers product.

## Anti-patterns (never do these)

- One global DO for all requests. It becomes a bottleneck.
- `blockConcurrencyWhile()` on each request. It stops throughput.
- Critical state only in memory. Eviction or a crash deletes it.
- `await` between related storage writes. It breaks atomicity.
- `blockConcurrencyWhile()` held across `fetch()` or external I/O.

## Stub creation

```typescript
// Deterministic - preferred for most cases
const stub = env.MY_DO.getByName("room-123");

// From existing ID string
const id = env.MY_DO.idFromString(storedIdString);
const stub = env.MY_DO.get(id);

// New unique ID - store mapping externally
const id = env.MY_DO.newUniqueId();
const stub = env.MY_DO.get(id);
```

## Storage operations

```typescript
// SQL (synchronous, recommended)
this.ctx.storage.sql.exec("INSERT INTO t (c) VALUES (?)", value);
const rows = this.ctx.storage.sql.exec<Row>("SELECT * FROM t").toArray();

// KV (async)
await this.ctx.storage.put("key", value);
const val = await this.ctx.storage.get<Type>("key");
```

## Alarms

```typescript
// Schedule (replaces existing)
await this.ctx.storage.setAlarm(Date.now() + 60_000);

// Handler
async alarm(): Promise<void> {
  // Process scheduled work
  // Optionally reschedule: await this.ctx.storage.setAlarm(...)
}

// Cancel
await this.ctx.storage.deleteAlarm();
```

## Testing

Before you configure a test suite or write Durable Object tests, read the [testing reference](./references/testing.md). It links to the current setup, APIs, and examples. It also tells you which behavior to test.
