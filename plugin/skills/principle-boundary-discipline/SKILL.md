---
name: principle-boundary-discipline
description: "Use when you write validation, error handling, or framework adapters. Put guards at system boundaries (CLI, config, network, external APIs). Trust internal types. Keep business logic in pure functions."
disable-model-invocation: true
---

# Boundary Discipline

Put validation, type narrowing, and error handling at system boundaries. Trust internal code fully. Put business logic in pure functions. Keep the shell thin and mechanical.

**Why:** Validation in many locations adds noise and repetition, and it gives a false feeling of safety. Keep logic out of the framework code, so that you can test the logic without the framework.

**The pattern:**
- **At boundaries** (CLI arguments, config files, external APIs, network protocols): validate, return errors, and handle input defensively.
- **Inside the system:** use typed data and propagate errors. Do not validate again. Trust the types.
- **Across the boundary:** show domain concepts, not the private representation of the boundary. Keep general-purpose mechanism inside. Keep special-purpose policy at the edge.

**Applications:**

Validation and error handling:
- Validate config when you parse it (at the boundary), not in business logic.
- Parse raw data into domain types at the boundary.
- Do not export transport, storage, framework, or wire types again through the public surface.
- Do not add nil checks deep in call chains if the boundary already validated the data.

Code organization:
- Put business logic in pure functions with no framework dependencies.
- Parse functions: pure transforms from raw bytes to typed state.
- Prompt construction: structured state in, string out.
- Scoring and assessment: pure transforms from state to results.

**The tests:**
- "Does this data cross a system boundary at this point?" If not, the validation is redundant.
- "Can this be a pure function that the shell only calls?" If yes, extract it.
