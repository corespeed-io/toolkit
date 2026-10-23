---
name: ai-sdk
description: Vercel AI SDK (`ai` package) guidance. Use when you build AI features with the AI SDK or any LLM provider, such as chat UIs, useChat, text generation, structured output, tool calling, agents, MCP, streaming, embeddings, reranking, or image generation.
---

## What the AI SDK Is

The AI SDK by Vercel is the `ai` package on npm. It is a TypeScript toolkit to build AI applications. It gives one API for all model providers. The API covers text generation, structured output, tool calling, agents, embeddings, and UI integrations for frameworks.

- Repository: https://github.com/vercel/ai
- Documentation: https://ai-sdk.dev/docs

## Critical: Do Not Trust Your Own Memory

Your knowledge of the AI SDK is probably old. The SDK changes frequently between versions. APIs get new names, are removed, or are added. Your training data almost certainly contains old APIs, deprecated patterns, and model IDs that do not exist now. UI hooks such as `useChat` change very frequently, so be careful with client code.

**Do not write AI SDK code from memory.** You must verify each API, option, and pattern against the documentation and source code of the version that the project installs.

## Use the Bundled, Version-Matched Docs

The `ai` package includes its full documentation and source code in `node_modules`. These files always match the installed version. Trust them more than your memory.

1. Make sure that `ai` is installed. Look in `node_modules/ai/`. In a monorepo, find the workspace package that depends on `ai` (for example, `apps/<name>/node_modules/ai/`). If the project does not install `ai` anywhere, install **only** the `ai` package into the target package. Use the package manager of the project (for example, `pnpm add ai --filter <pkg>` or `npm install ai`). Install provider packages (for example, `@ai-sdk/openai`) and framework packages (for example, `@ai-sdk/react`) later, when the task needs them.
2. Read and grep the bundled docs at `node_modules/ai/docs/` (or `<package>/node_modules/ai/docs/`). Read the source at `node_modules/ai/src/`.
3. Provider packages and framework packages include their own docs at `node_modules/@ai-sdk/<name>/docs/` (or `<package>/node_modules/@ai-sdk/<name>/docs/`).
4. If the bundled docs do not have the answer, search https://ai-sdk.dev/docs. Add `.md` to the URL of a docs page to get its Markdown. To search, use `https://ai-sdk.dev/api/search-docs?q=your_query`.
5. If the docs and the source do not support an answer, tell the user. Do not guess.

## AI Gateway: Quick Start

The Vercel AI Gateway is a quick way to start with the AI SDK. It gives access to models from OpenAI, Anthropic, Google, and other providers through one API. You do not install provider packages or manage many API keys.

To set it up:

1. Authenticate with OIDC (for Vercel deployments), or get an AI Gateway API key.
2. Give the key to your app in the `AI_GATEWAY_API_KEY` environment variable.
3. Refer to models with `provider/model` strings.

For the exact setup, authentication, and usage, read the bundled guide and the AI Gateway docs. The `ai-gateway` skill also covers this.

### Choosing a Model

Do not use model IDs from memory. Providers release and retire models frequently. Get the current list before you write code that refers to a model. Do not truncate the list (for example, with `head`), so that you see the newest models:

```bash
# All available models
curl -s https://ai-gateway.vercel.sh/v1/models | jq -r '.data[].id'

# Filter by provider (e.g. anthropic, openai, google)
curl -s https://ai-gateway.vercel.sh/v1/models | jq -r '[.data[] | select(.id | startswith("anthropic/")) | .id] | reverse | .[]'
```

When there are many versions of a model, use the version with the highest number.

## Building and Consuming Agents

Use the agent abstraction of the SDK (such as `ToolLoopAgent`). Do not write your own tool-calling loop. For type safety from end to end, infer the UI message type from your agent definition when the client consumes the agent (for example, with `useChat`). The steps to consume an agent are different for each framework:

1. Read `package.json` to find the stack.
2. Follow the quickstart for that stack.

Find the current agent, tool, and type-safety APIs in the bundled docs (`node_modules/ai/docs/`, especially the agents section) or at https://ai-sdk.dev/docs.

## DevTools

AI SDK DevTools records your AI SDK calls: requests, responses, tool calls, token usage, and multi-step runs. Use it to see exactly what your agents do, and to debug generations during development. It is a separate package. Use it only for local development.

For setup instructions, read the bundled DevTools documentation.

## Keep the SDK Current

Old installs are the most frequent cause of errors. Compare the installed version with the latest version:

- **Installed:** the `version` field in `node_modules/ai/package.json`.
- **Latest:** run `npm view ai version`.

If the installed version is one or more major versions behind the latest, tell the user that the release is old. Recommend an upgrade before you continue. The migration guides are at https://ai-sdk.dev/docs/migration-guides.

## After Making Changes

1. Run the type checker of the project.
2. Keep options to a minimum. Set only the options that are different from the defaults. Find the defaults in the docs or the source. Do not specify more than necessary.
3. If type errors occur, check the current docs and source again. Most type errors come from APIs that you remember but that changed.
