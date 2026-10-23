---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Use when you add a new internal API and old callers still exist. Migrate the callers and delete the old API in the same wave. Do not keep compatibility layers."
disable-model-invocation: true
---

# Migrate Callers Then Delete Legacy APIs

When you add a new internal API, migrate all callers and delete the old API in the same wave. Do not keep a compatibility layer.

- Update the tests so that they assert the new contract. Delete tests that only protect implementation details from before the refactor.

**When this applies:**
- No external users need backward compatibility.
- The project can accept coordinated breaking changes.
- The new API is part of a simplification or refactor effort.
