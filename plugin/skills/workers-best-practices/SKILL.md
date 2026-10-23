---
name: workers-best-practices
description: Best practices for production Cloudflare Workers. Use when you write, review, or configure Workers code or Worker configuration.
---

Your knowledge of Cloudflare Workers APIs, types, and configuration can be old. **Use retrieval, not pre-training,** when you write or review Workers code.

- For existing code, use the installed versions, the generated types, and the Wrangler compatibility settings of the project as the baseline.
- Get the applicable Cloudflare documentation to verify statements about APIs, configuration, runtime behavior, and limits.
- For CLI commands, use the `cf-cli` skill. It tells you when to use `cf` and when Wrangler is still necessary.

## References

Read the sections that apply to the task:

| Reference | When to use it |
|-----------|----------------|
| [Configuration and observability](references/configuration.md) | Compatibility dates, bindings, generated types, secrets, logs, and traces |
| [Runtime patterns](references/runtime-patterns.md) | Streaming, promise lifetime, request state, service calls, security, and runtime tests |
| [Platform API checks](references/platform-apis.md) | Handler signatures, platform classes, binding access, and serialization |

- If you do not have sufficient evidence, read [Workers best practices](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/index.md), or find the product in the [Cloudflare docs directory](https://developers.cloudflare.com/directory/index.md).
- For configuration fields, use the installed Wrangler schema.
- A newer type package does not replace the configured target of the project.

## Keep compatibility dates current

- For a new Worker, use the date of today.
- For an existing Worker, recommend periodic updates. Examine the compatibility changes and run the applicable tests.
- Evaluate existing behavior against its configured date and flags. Refer to the [compatibility guidance](references/configuration.md#keep-compatibility_date-current).

## Enable observability

When you make a Worker or prepare it for production, enable [Workers Logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/index.md) and [Traces](https://developers.cloudflare.com/workers/observability/traces/index.md).

- Set `observability.enabled` and `observability.traces.enabled` to `true`. The top-level setting alone does not enable traces.
- Use structured JSON logging.
- Configure sampling for the workload.
- During a review, report missing logs or traces.

Refer to the [configuration example](references/configuration.md#enable-workers-logs-and-traces).

## Anti-patterns to report

| Anti-pattern | Consequence and preferred pattern |
|-------------|-----------------------------------|
| `await response.text()` or similar buffering on unbounded data | Can use all Worker memory. [Stream large or unbounded bodies](references/runtime-patterns.md#stream-request-and-response-bodies). |
| Hardcoded secrets in source or config | Credentials go into version control. Use Worker secrets (refer to the `cf-cli` skill for the secret commands). |
| `Math.random()` for security-sensitive tokens or IDs | The values are predictable. Use `crypto.randomUUID()` or `crypto.getRandomValues()`. |
| Async work that you start and do not await, return, or attach to `ctx.waitUntil()` | The runtime can drop the work, and you do not see the errors. Attach the work to the request lifetime or to the background-work lifetime. |
| Module-level mutable request state | Data goes from one request to a different request, and I/O ownership errors can occur. Pass request state explicitly. |
| Cloudflare REST API calls for operations that Worker bindings supply | Adds network and authentication overhead. Use the binding. |
| `ctx.passThroughOnException()` as general error handling | Can hide Worker failures because it forwards to the origin. Use explicit error handling and structured error responses. |
| Hand-written `Env` that copies Wrangler bindings | Can become different from the configuration. Generate binding types with `wrangler types`. In a `cf` project, find the equivalent with `cf cli search`. |
| Direct string comparison of secret values | Can show timing differences. Use the [Web Crypto comparison pattern](references/runtime-patterns.md#use-web-crypto-for-secure-token-generation). |
| Destructuring `ctx` methods, such as `const { waitUntil } = ctx` | The method loses its receiver. Call `ctx.waitUntil(...)`. |
| `any` on `Env` or handler parameters | Hides binding and handler contract errors. Use the generated types and the platform types of the project. |
| `as unknown as T` to force a platform type match | Hides incompatibilities. Fix the contract. |
| `implements` in place of extending a platform base class | The class does not get the runtime behavior, `this.ctx`, or `this.env`. Extend the correct base class. |
| Unbound `env.X` in a platform class method | Bindings are in `this.env.X`. Refer to [binding access patterns](references/platform-apis.md#binding-access--the-most-common-error). |
| One serialization rule for Queues, Workflow steps, storage, and WebSockets | Can refuse valid payloads or accept payloads that are not supported. Examine the [specific API and encoding](references/platform-apis.md#serialization-boundaries). |

## Validation

Use the existing checks of the project for the Workers behavior that the change affects:

- When you change a binding or a handler contract, run the type check.
- When you change behavior, run the applicable runtime tests.
- Keep the checks that the repository requires. A small edit does not need a full Workers audit.

## Scope

This skill covers best practices and code review for Workers. For related topics:

- **Durable Objects**: load the `durable-objects` skill.
- **Workflows**: refer to [Rules of Workflows](https://developers.cloudflare.com/workflows/build/rules-of-workflows/index.md).
- **CLI commands**: load the `cf-cli` skill. It also covers projects that have a Wrangler configuration file.
