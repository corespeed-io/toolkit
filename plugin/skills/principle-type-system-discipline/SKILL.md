---
name: principle-type-system-discipline
description: "Use when you design types, review a function signature, or write code in a statically typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries."
disable-model-invocation: true
---

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Define errors and special cases out of existence. Do not add more and more handlers. For TypeScript syntax, see the `typescript-best-practices` skill.

- **Brand semantic primitives.** `UserId` and `OrderId` are strings, but you must not use one in place of the other. Give each its own type, for example a branded intersection in TypeScript or a newtype in other languages. Validate one time at creation, and trust the type after that. If two arguments have the same primitive type but different meanings, brand them.
- **External data has no type until you parse it.** This includes RPC payloads, JSON, IPC messages, CLI arguments, config files, environment variables, and database rows. Put a parse function at each boundary. It changes unstructured input into the typed model. The **principle-boundary-discipline** skill tells where to put validation.
- **Derive types from authoritative schemas.** When a file owns a shape, derive the type from it. Do not write a parallel type by hand. Examples of such files are a protocol buffer, an OpenAPI spec, a GraphQL schema, a database migration, or a design-token file. See the **principle-encode-lessons-in-structure** skill.
- **Exhaust variants.** Handle each variant of a union, and make the compiler report a variant that the code does not handle.
