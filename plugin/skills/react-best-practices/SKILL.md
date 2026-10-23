---
name: react-best-practices
description: Vercel performance rules for React and Next.js (70 rules in 8 categories, sorted by impact). Use when you write, review, or refactor React components, Next.js pages, or data fetching for speed, bundle size, waterfalls, or re-renders. It is not a guide for accessibility or TypeScript style.
---

# Vercel React Best Practices

This is a performance guide for React and Next.js applications. Vercel maintains it. It has 70 rules in 8 categories. The categories are sorted by impact. Use the rules to guide refactors and code generation.

## When to Apply

Use these rules when you:
- Write new React components or Next.js pages.
- Write data fetching on the client or on the server.
- Review code for performance problems.
- Refactor React or Next.js code.
- Make the bundle smaller or make pages load faster.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-cheap-condition-before-await` - Check cheap synchronous conditions before you await flags or remote values.
- `async-defer-await` - Move each `await` into the branch that uses the value.
- `async-parallel` - Use `Promise.all()` for operations that do not depend on each other.
- `async-dependencies` - Use `better-all` for operations that depend on some of the others.
- `async-api-routes` - In API routes, start promises early and await them late.
- `async-suspense-boundaries` - Use Suspense to stream content.

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly from the source module. Do not import from barrel files.
- `bundle-analyzable-paths` - Use import paths and file-system paths that the bundler can analyze statically. This prevents large bundles and traces.
- `bundle-dynamic-imports` - Use `next/dynamic` for heavy components.
- `bundle-defer-third-party` - Load analytics and logging after hydration.
- `bundle-conditional` - Load a module only when the user activates its feature.
- `bundle-preload` - Preload on hover or focus, so that the page feels faster.

### 3. Server-Side Performance (HIGH)

- `server-auth-actions` - Authenticate server actions the same way as API routes.
- `server-cache-react` - Use `React.cache()` to remove duplicate work in one request.
- `server-cache-lru` - Use an LRU cache to cache across requests.
- `server-dedup-props` - Do not serialize the same data two times in RSC props.
- `server-hoist-static-io` - Move static I/O (fonts, logos) to module level.
- `server-no-shared-module-state` - Do not keep mutable request state at module level in RSC or SSR.
- `server-serialization` - Send the minimum data to client components.
- `server-parallel-fetching` - Change the component structure so that fetches run in parallel.
- `server-parallel-nested-fetching` - Chain the nested fetches for each item inside `Promise.all`.
- `server-after-nonblocking` - Use `after()` for operations that must not block the response.

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR to remove duplicate requests automatically.
- `client-event-listeners` - Remove duplicate global event listeners.
- `client-passive-event-listeners` - Use passive listeners for scroll.
- `client-localstorage-schema` - Add a version to `localStorage` data and keep it small.

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Do not subscribe to state that only callbacks use.
- `rerender-memo` - Move expensive work into memoized components.
- `rerender-memo-with-default-value` - Hoist default props that are not primitives.
- `rerender-dependencies` - Use primitive values as effect dependencies.
- `rerender-derived-state` - Subscribe to derived booleans, not to raw values.
- `rerender-derived-state-no-effect` - Derive state during render, not in effects.
- `rerender-functional-setstate` - Use functional `setState` to keep callbacks stable.
- `rerender-lazy-state-init` - Pass a function to `useState` for expensive initial values.
- `rerender-simple-expression-in-memo` - Do not use memo for simple primitive values.
- `rerender-split-combined-hooks` - Split a hook that has independent dependencies.
- `rerender-move-effect-to-event` - Put interaction logic in event handlers.
- `rerender-transitions` - Use `startTransition` for updates that are not urgent.
- `rerender-use-deferred-value` - Defer expensive renders, so that input stays responsive.
- `rerender-use-ref-transient-values` - Use refs for values that change frequently and do not affect render.
- `rerender-no-inline-components` - Do not define components inside other components.

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate a `div` wrapper, not the SVG element.
- `rendering-content-visibility` - Use `content-visibility` for long lists.
- `rendering-hoist-jsx` - Move static JSX outside of components.
- `rendering-svg-precision` - Decrease the precision of SVG coordinates.
- `rendering-hydration-no-flicker` - Use an inline script for data that only the client has.
- `rendering-hydration-suppress-warning` - Suppress hydration mismatches that you expect.
- `rendering-activity` - Use the `Activity` component to show and hide content.
- `rendering-conditional-render` - Use a ternary, not `&&`, for conditional render.
- `rendering-usetransition-loading` - Use `useTransition` for loading state.
- `rendering-resource-hints` - Use React DOM resource hints to preload.
- `rendering-script-defer-async` - Use `defer` or `async` on script tags.

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes with classes or `cssText`.
- `js-index-maps` - Build a `Map` for repeated lookups.
- `js-cache-property-access` - Cache object properties in loops.
- `js-cache-function-results` - Cache function results in a module-level `Map`.
- `js-cache-storage` - Cache `localStorage` and `sessionStorage` reads.
- `js-combine-iterations` - Combine many `filter`/`map` calls into one loop.
- `js-length-check-first` - Compare array lengths before an expensive comparison.
- `js-early-exit` - Return early from functions.
- `js-hoist-regexp` - Create a `RegExp` outside of loops.
- `js-min-max-loop` - Use a loop, not a sort, to find a minimum or a maximum.
- `js-set-map-lookups` - Use `Set` or `Map` for O(1) lookups.
- `js-tosorted-immutable` - Use `toSorted()` to keep arrays immutable.
- `js-flatmap-filter` - Use `flatMap` to map and filter in one pass.
- `js-request-idle-callback` - Defer work that is not critical until the browser is idle.

### 8. Advanced Patterns (LOW)

- `advanced-effect-event-deps` - Do not put `useEffectEvent` results in effect dependencies.
- `advanced-event-handler-refs` - Keep event handlers in refs.
- `advanced-init-once` - Initialize the app one time for each app load.
- `advanced-use-latest` - Use `useLatest` to get stable callback refs.

## How to Use

Read a rule file for the full explanation and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

Each rule file contains:
- A short explanation of why the rule is important.
- An incorrect code example, with an explanation.
- A correct code example, with an explanation.
- More context and references.

## Full Compiled Document

The file `AGENTS.md` in this skill folder contains the full guide, with all rules expanded.
