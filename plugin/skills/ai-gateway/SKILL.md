---
name: ai-gateway
description: Vercel AI Gateway guidance for setup, model choice, authentication, routing, fallbacks, Virtual Models, decisions (evaluation), BYOK, budgets, spend, logs, and coding-agent routing. Use when you add AI Gateway, migrate provider calls, debug gateway requests, or run `vercel ai-gateway` commands.
---

# Vercel AI Gateway

AI Gateway gives access to models from many providers. It shares authentication, model IDs, routing, billing, and observability across them. Model availability, SDK APIs, CLI commands, prices, and product capabilities change frequently. Verify them from current sources before you change code.

## Start with current sources

Before you implement:

1. Examine the language, package manager, installed AI SDK version, and current provider integration of the project.
2. Read the applicable Vercel page under <https://vercel.com/docs/ai-gateway>. If a tool needs Markdown, use the `.md` form of the page.
3. Get the complete live model list. Do not make model variant names by analogy:

   ```bash
   curl -fsSL https://ai-gateway.vercel.sh/v1/models
   ```

4. If the code uses the `ai` package, load the `ai-sdk` skill. Read the version-matched docs under `node_modules/ai/docs/` and the source under `node_modules/ai/src/`. If the skill is not available, use those bundled files directly.
5. Run `vercel ai-gateway <command> --help` before you document or script CLI flags.

The live model endpoint and the installed package have priority over model names or SDK syntax from your training data.

## Vercel CLI inventory

The `vercel ai-gateway` command manages gateway resources for the current team. The `setup` subcommand connects local coding agents. The other subcommands do the jobs that before needed the dashboard:

| Command | What it does |
| --- | --- |
| `api-keys create/list/inspect/remove` | Create and manage AI Gateway API keys, with budgets, spend alerts, expiry, and restriction exemptions |
| `budgets set/list/inspect/remove` | Set metered spend limits for the team, a project, a user, or an API key |
| `budgets set/inspect/remove --default`, `budgets list --defaults` | Set default limits for each scope. They apply to projects, keys, or members that do not have a custom budget. Needs CLI 59.13+. The older `budgets defaults` group is deprecated |
| `models list` / `models endpoints <model>` | List the model catalog, and list the provider endpoints of one model |
| `virtual-models create/list/inspect/edit/remove/restore` | Manage reusable model configurations for the team, with the address `vmc/<slug>` |
| `rules add/list/edit/remove` | Manage routing rules. The CLI marks rules as beta, so check `--help` before you use them. REST CRUD is at `https://api.vercel.com/ai-gateway/rules` |
| `setup` | Configure supported coding agents. See [references/coding-agents.md](references/coding-agents.md) |
| `leaderboard` | Show public, anonymized usage leaderboards. Implementation work almost never needs it |

When the user works from a terminal or in CI, use the CLI to manage credentials and spend. Before you write a script, check `vercel ai-gateway <command> --help` for the current flags. Do not copy a flag list from this skill into generated code.

## Route the request to the right guide

| User's job | Read |
| --- | --- |
| Ask a coding agent to make one Gateway request, or handle first-request credentials, compatible SDKs, or migration | [references/setup.md](references/setup.md) |
| Provider selection, model fallbacks, caching, BYOK, or timeouts | [references/routing.md](references/routing.md) |
| Reusable model configuration, a `vmc/<slug>`, or provider options for a client that cannot send them | [references/virtual-models.md](references/virtual-models.md) |
| Typed decisions (formerly evaluation) through AI SDK, `POST /v1/evaluate`, the OpenAI-compatible `POST /v1/decisions`, or the TypeSafe-compatible API | [references/evaluation.md](references/evaluation.md) |
| Credits, budgets, reporting, Logs, or request debugging | [references/spend-observability.md](references/spend-observability.md) |
| Route the model traffic of Claude Code, Codex, OpenCode, Pi, or another coding agent through Gateway | [references/coding-agents.md](references/coding-agents.md) |

Read each applicable reference before you edit. A task can need more than one reference.

## Choose the integration surface

| Existing project | Default path |
| --- | --- |
| JavaScript or TypeScript using AI SDK | Use a plain `provider/model` string with `generateText`, `streamText`, `ToolLoopAgent`, or the applicable modality API |
| Python using AI SDK for Python | Use `ai.get_model('provider/model')` and the current Python SDK docs |
| Existing OpenAI SDK | Keep the SDK. Set `baseURL` or `base_url` to `https://ai-gateway.vercel.sh/v1` |
| Existing Anthropic SDK | Keep the SDK. Set `baseURL` or `base_url` to `https://ai-gateway.vercel.sh` |
| Evaluation over provider-neutral HTTP | Send the Gateway evaluation request shape to `POST https://ai-gateway.vercel.sh/v1/evaluate` |
| Existing TypeSafe evaluation client | Keep `@typesafe-ai/sdk`. Set `baseURL` to `https://ai-gateway.vercel.sh/typesafe` |
| Provider-neutral HTTP | Use an AI Gateway compatible endpoint, such as Chat Completions or OpenResponses |
| Existing direct-provider AI SDK integration | Replace the provider instance with a live AI Gateway `provider/model` string. Remove the provider credentials only after you verify the gateway path |
| Coding agent | Use `vercel ai-gateway setup`. Read its help before you say that it supports an agent. Use a Virtual Model when the agent needs reusable routing, or provider options that it cannot send in each request |

AI Gateway also supports:

- OpenAI Responses, Anthropic Messages, and OpenResponses.
- Cohere Rerank and embeddings.
- Image and video generation, speech, and transcription.
- Realtime sessions.
- Decisions (formerly evaluation).

The modality pages under <https://vercel.com/docs/ai-gateway/modalities> show each request shape. This includes background jobs for long video generation.

Decisions are available through these surfaces:

- AI SDK: `experimental_decide` in `ai` 7.0.128+, or the deprecated `experimental_evaluate` alias in earlier AI SDK 7 releases.
- `POST /v1/evaluate`.
- The OpenAI-compatible `POST /v1/decisions`.
- A TypeSafe-compatible API under `/typesafe`.

Decisions are not available through Chat Completions, Responses, or the Anthropic-compatible or Cohere-compatible endpoints. Read [references/evaluation.md](references/evaluation.md) before you choose a surface. Read the applicable modality or API page. Do not translate one request shape from memory.

## Minimal AI SDK request

The current AI SDK needs Node.js 22 or later. In an existing project, check the `engines` field of the installed package before you enforce a version.

```ts
import { generateText } from 'ai';

const model = process.env.AI_GATEWAY_MODEL;
if (!model) {
  throw new Error('Set AI_GATEWAY_MODEL to an ID returned by /v1/models');
}

const { text } = await generateText({
  model,
  prompt: 'Explain the project in one paragraph.',
});

console.log(text);
```

If the user or the task gives an exact model, confirm that it exists, then use it. If not:

1. Get `/v1/models`.
2. Choose a model that fits the modality, capabilities, price, context window, data-retention policy, and team access that the task needs.
3. Set `AI_GATEWAY_MODEL` to that ID.

Do not put a model recommendation that changes with time in reusable examples.

Plain model strings go through AI Gateway. Add `@ai-sdk/gateway` only when the task needs its exported provider, types, model discovery, generation lookup, or spend-report helpers.

## Authentication decision

- Use an **AI Gateway API key** for local scripts, CI, external servers, and deployments that are not on Vercel. Keep it in `AI_GATEWAY_API_KEY`. Do not print or commit it.
- Use **Vercel OIDC** for Vercel deployments and linked local projects. Vercel deployments get `VERCEL_OIDC_TOKEN`. For local development, use `vercel link` and `vercel env pull`.
- **BYOK provider credentials do not replace AI Gateway request authentication.** They set how AI Gateway authenticates to a model provider.
- A plain Node.js script does not load `.env.local` automatically. Export the variables in the shell, or load that file explicitly. Frameworks can behave differently.

Do not ask the user to paste a secret into chat, source code, a committed config file, or a command that goes into shell history. The only exception is when the repository already has a secure mechanism for this.

## Implementation workflow

1. Find the user's job, runtime, deployment target, current provider, and required capabilities.
2. Select the authentication from the rules above. If a current method works, keep it, unless the user asked to migrate it.
3. Get live model metadata and choose a compatible model. Tell why it fits.
4. Read the matching SDK, API, modality, routing, or coding-agent docs.
5. Make the smallest change that works from end to end. Use the current project structure and error handling.
6. Handle only the errors that the application can act on. Frequent gateway results are authentication failure, insufficient credits, exhausted budget, rate limits, and provider capacity failure.
7. Run the formatter, the type checker, and the focused tests of the project.
8. If the task permits a live request, send one. Examine the returned model, text or media, usage, and provider metadata.
9. If you have dashboard access, verify the request in AI Gateway Logs. Logs can take approximately 90 seconds to appear.

Do these outward-facing actions only when the user asked for them or approved them: spend credits, create keys, change budgets, change routing rules, or write coding-agent config. Use dry runs and interactive previews when they are available.

## Routing invariants

- Model IDs use the exact `provider/model` strings that `/v1/models` returns.
- `order` sets the provider preference. `only` limits the providers. `sort` ranks providers by a supported metric.
- `models` lists the fallback models that come after the primary model.
- `caching: 'auto'` manages provider prompt-cache markers. It is not an HTTP response cache.
- `providerTimeouts` applies to BYOK provider attempts. Streaming requests clear it at the first stream chunk. Non-streaming requests measure the time of the complete response.
- A reasoning entry in `providerOptions` fully overrides the AI SDK top-level `reasoning` value. The two values do not merge.
- `user` and `tags` add reporting dimensions. They do not create rate limits for each user.
- Provider credentials for one request go under `providerOptions.gateway.byok`. They must stay secret.
- Virtual Model IDs use `vmc/<slug>`. A Virtual Model can set routing and provider options on the server. Settings that it defines usually override the same request settings. Settings that it does not define stay configurable in the request.

Read [references/routing.md](references/routing.md) before you add any of these fields.

## Verification checklist

- [ ] A direct model ID exists in the full live model response, or a Virtual Model exists for the authenticated team and resolves as `vmc/<slug>`.
- [ ] The selected API or SDK supports the requested modality and feature.
- [ ] Authentication works in the real runtime, including `.env.local` loading where applicable.
- [ ] The example prints or returns a result. It does not discard the response.
- [ ] The type checker and focused tests of the project pass.
- [ ] You sent a live request only with permission, and you know its cost.
- [ ] Response metadata or Logs show the provider routing or fallback behavior.
- [ ] No secret appears in source, logs, diffs, or the final response.
- [ ] The final report keeps code verification separate from live verification and dashboard verification.

## Current documentation

- Getting started: <https://vercel.com/docs/ai-gateway/getting-started>
- Models and providers: <https://vercel.com/docs/ai-gateway/models-and-providers>
- Virtual Models: <https://vercel.com/docs/ai-gateway/models-and-providers/virtual-models>
- SDKs and APIs: <https://vercel.com/docs/ai-gateway/sdks-and-apis>
- Authentication and BYOK: <https://vercel.com/docs/ai-gateway/authentication-and-byok>
- Observability and spend: <https://vercel.com/docs/ai-gateway/observability-and-spend>
- Modalities: <https://vercel.com/docs/ai-gateway/modalities>
- Decision: <https://vercel.com/docs/ai-gateway/modalities/decision>
- TypeSafe API: <https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe>
- REST API reference: <https://vercel.com/docs/ai-gateway/sdks-and-apis/rest-api>
- FAQ: <https://vercel.com/docs/ai-gateway/faq>
- Coding agents: <https://vercel.com/docs/ai-gateway/coding-agents>
- AI SDK provider: <https://ai-sdk.dev/providers/ai-sdk-providers/ai-gateway>
