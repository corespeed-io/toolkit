---
name: nextjs
description: "Next.js App Router guidance. Use when you build, debug, or design Next.js apps: routing, Server Components, Server Actions, Cache Components, layouts, middleware/proxy, data fetching, metadata, images, fonts, hydration errors, rendering, self-hosting, and deployment on Vercel."
---

# Next.js Best Practices

**Version-matched docs first:** If the project has `node_modules/next/dist/docs/`, read the applicable doc there first. Those docs match the installed Next.js version. Use this skill only as a summary.

Apply these rules when you write or review Next.js code.

## File Conventions

See [file-conventions.md](./references/file-conventions.md) for:
- Project structure and special files
- Route segments (dynamic, catch-all, groups)
- Parallel and intercepting routes
- The middleware rename in v16 (middleware → proxy)

## RSC Boundaries

Find React Server Component patterns that are not valid.

See [rsc-boundaries.md](./references/rsc-boundaries.md) for:
- How to find async client components (not valid)
- How to find props that are not serializable
- Server Action exceptions

## Async Patterns

Next.js 15+ changed some APIs to async.

See [async-patterns.md](./references/async-patterns.md) for:
- Async `params` and `searchParams`
- Async `cookies()` and `headers()`
- The migration codemod

## Runtime Selection

See [runtime-selection.md](./references/runtime-selection.md) for:
- Why the Node.js runtime is the default
- When the Edge runtime is applicable

## Directives

See [directives.md](./references/directives.md) for:
- `'use client'`, `'use server'` (React)
- `'use cache'` (Next.js)

## Functions

See [functions.md](./references/functions.md) for:
- Navigation hooks: `useRouter`, `usePathname`, `useSearchParams`, `useParams`
- Server functions: `cookies`, `headers`, `draftMode`, `after`
- Generate functions: `generateStaticParams`, `generateMetadata`

## Error Handling

See [error-handling.md](./references/error-handling.md) for:
- `error.tsx`, `global-error.tsx`, `not-found.tsx`
- `redirect`, `permanentRedirect`, `notFound`
- `forbidden`, `unauthorized` (auth errors)
- `unstable_rethrow` for catch blocks

## Data Patterns

See [data-patterns.md](./references/data-patterns.md) for:
- When to use Server Components, Server Actions, or Route Handlers
- How to prevent data waterfalls (`Promise.all`, Suspense, preload)
- Data fetching in client components

## Route Handlers

See [route-handlers.md](./references/route-handlers.md) for:
- `route.ts` basics
- Conflicts between a GET handler and `page.tsx`
- Environment behavior (no React DOM)
- When to use Route Handlers instead of Server Actions

## Metadata & OG Images

See [metadata.md](./references/metadata.md) for:
- Static and dynamic metadata
- The `generateMetadata` function
- OG image generation with `next/og`
- File-based metadata conventions

## Image Optimization

See [image.md](./references/image.md) for:
- Why you must use `next/image`, not `<img>`
- Configuration for remote images
- The responsive `sizes` attribute
- Blur placeholders
- Priority loading for LCP

## Font Optimization

See [font.md](./references/font.md) for:
- `next/font` setup
- Google Fonts and local fonts
- Tailwind CSS integration
- Preloading subsets

## Bundling

See [bundling.md](./references/bundling.md) for:
- Packages that do not work on the server
- CSS imports (not link tags)
- Polyfills (Next.js already includes them)
- ESM/CommonJS problems
- Bundle analysis

## Scripts

See [scripts.md](./references/scripts.md) for:
- `next/script` compared with native script tags
- Why inline scripts need an `id`
- Loading strategies
- Google Analytics with `@next/third-parties`

## Hydration Errors

See [hydration-error.md](./references/hydration-error.md) for:
- Frequent causes (browser APIs, dates, HTML that is not valid)
- Debugging with the error overlay
- The fix for each cause

## Suspense Boundaries

See [suspense-boundaries.md](./references/suspense-boundaries.md) for:
- CSR bailout with `useSearchParams` and `usePathname`
- Which hooks need Suspense boundaries

## Parallel & Intercepting Routes

See [parallel-routes.md](./references/parallel-routes.md) for:
- Modal patterns with `@slot` and `(.)` interceptors
- `default.tsx` for fallbacks
- How to close modals correctly with `router.back()`

## Self-Hosting

See [self-hosting.md](./references/self-hosting.md) for:
- `output: 'standalone'` for Docker
- Cache handlers for multi-instance ISR
- What works, and what needs more setup

## Debug Tricks

See [debug-tricks.md](./references/debug-tricks.md) for:
- The MCP endpoint for AI-assisted debugging
- How to rebuild specific routes with `--debug-build-paths`
