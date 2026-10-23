---
name: typescript-best-practices
description: TypeScript best practices. Use when you read or edit a .ts or .tsx file.
paths: ["**/*.ts", "**/*.tsx"]
disable-model-invocation: true
---

# TypeScript best practices

Apply the **type-system-discipline** principle skill first.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant, so that impossible states cannot exist in the types. Do not use bags of optional fields. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }`, so that nobody can mix them. Validate one time at the boundary. A brand comes from a type guard that verifies (`input is AgentId`), never from `as`. |
| Constructive modeling | Build the shape so that nobody can construct the illegal value. Use `[T, ...T[]]` for non-empty, `[T, T][]` for even length, and `start` plus `duration` for a range. Do not use a runtime guard. Do not wait for refinement types. |
| Simplest total type | Keep `T[]` while each operation on it stays total. Change it to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. |
| Schemas before guards | Before you write a type guard by hand, property by property, use the runtime schema library of the repository. Infer the type from the schema, for example `z.infer`. |
| No `as` casts | Each `as` can cause a runtime crash. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | A type guard must verify the claim. A false guard is worse than `as`, because the bug hides behind a name that says that it is safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Put `const _exhaustive: never = x;` inline in default arms. Then the compiler gives an error when somebody adds a new variant. |
| `satisfies` over `as` | It validates the value and does not widen literal types. |
| Boundary validation | Parse data where it comes in, into a named domain type. `Record<string, unknown>` (in any spelling) stops at that parse. Trust the types inside. See the **boundary-discipline** principle skill. |
| Schema-derived types | Use `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before you declare a new interface. |
| Object args | Pass objects, not positional arguments, so that the argument order documents itself. Do not do this on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Do not mock what you can run. Prefer the real test primitives of the framework, with leak and disposable checks. Verify UI in a running build. Mock only what you cannot run locally. |
| Structured telemetry | Prefer structured logger diagnostics with sufficient context to debug from an id. Do not use `console.log` in shipped code. |

Examples: `references/patterns.md`.
