---
name: init-project
description: Use when a project has no AGENTS.md, or the user asks to set up or refresh a project's agent instructions or tech stack notes.
---

# Init project

Write `AGENTS.md` at the project root. Write `CLAUDE.md` next to it with the one line `@AGENTS.md`, so Claude Code reads the same file.

Read the repo first: package manifests, lockfiles, config files, CI files, README. Write only facts that you can see in the repo. If you cannot find a fact, leave it out. Do not guess.

Use this template. Delete a section if it has no content. Keep the file short.

```markdown
# <Project name>

<One sentence: what the project does.>

## Stack

- Language and runtime: <e.g. TypeScript 5, Node 24>
- Framework: <e.g. Next.js App Router>
- Data: <database, ORM, cache>
- Hosting: <where it deploys>
- Package manager: <pnpm / uv / ...>

## Commands

- Install: `<cmd>`
- Dev: `<cmd>`
- Test: `<cmd>`
- Lint and format: `<cmd>`
- Build: `<cmd>`

## Layout

- `<dir>/`: <what is in it>

## Conventions

- <Rules for this project that differ from the global rules or add to them.>
```

If `AGENTS.md` exists, update it. Keep the text the user wrote. Commit the change.
