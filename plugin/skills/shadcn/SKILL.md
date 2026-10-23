---
name: shadcn
description: 'Add, search, fix, debug, style, and compose shadcn/ui components, including chat UI. Use for shadcn/ui, components.json, registries, "shadcn init", --preset codes ("create an app with --preset", "switch to --preset"), or a design system from a DESIGN.md or brand spec.'
user-invocable: false
allowed-tools: Bash(npx shadcn@latest *), Bash(pnpm dlx shadcn@latest *), Bash(bunx --bun shadcn@latest *)
---

# shadcn/ui

shadcn/ui is a framework to build UI, components, and design systems. The CLI adds components as source code to the project of the user.

> **IMPORTANT:** Run all CLI commands with the package runner of the project: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, or `bunx --bun shadcn@latest`. Select the runner from the `packageManager` of the project. The examples below use `npx shadcn@latest`. Replace it with the correct runner for the project.

## Current Project Context

```json
!`npx shadcn@latest info --json`
```

In Claude Code, the block above runs when the skill loads and shows the output. Other harnesses (for example, Codex) show the command text only. In that case, run `npx shadcn@latest info --json` yourself first.

The JSON contains the project config and the installed components. Use `npx shadcn@latest docs <component>` to get the documentation and example URLs for a component.

## Principles

1. **Use existing components first.** Use `npx shadcn@latest search` to check registries before you write custom UI. Also check community registries.
2. **Compose components. Do not make them again.** Settings page = Tabs + Card + form controls. Dashboard = Sidebar + Card + Chart + Table.
3. **Use built-in variants before custom styles.** For example, `variant="outline"` and `size="sm"`.
4. **Use semantic colors.** Use `bg-primary` and `text-muted-foreground`. Never use raw values such as `bg-blue-500`.

## Critical Rules

These rules **always apply**. Each section links to a file with Incorrect/Correct code pairs.

### Styling & Tailwind → [styling.md](./rules/styling.md)

- **Use `className` for layout, not for styling.** Never override the colors or typography of a component.
- **Do not use `space-x-*` or `space-y-*`.** Use `flex` with `gap-*`. For vertical stacks, use `flex flex-col gap-*`.
- **Use `size-*` when width and height are equal.** Use `size-10`, not `w-10 h-10`.
- **Use the `truncate` shorthand.** Do not use `overflow-hidden text-ellipsis whitespace-nowrap`.
- **Do not add manual `dark:` color overrides.** Use semantic tokens (`bg-background`, `text-muted-foreground`).
- **Use `cn()` for conditional classes.** Do not write manual template literal ternaries.
- **Do not add a manual `z-index` to overlay components.** Dialog, Sheet, Popover, and similar components control their own stacking.

### Forms & Inputs → [forms.md](./rules/forms.md)

- **Forms use `FieldGroup` + `Field`.** Never use a raw `div` with `space-y-*` or `grid gap-*` for form layout.
- **`InputGroup` uses `InputGroupInput`/`InputGroupTextarea`.** Never put a raw `Input`/`Textarea` inside `InputGroup`.
- **Buttons inside inputs use `InputGroup` + `InputGroupAddon`.**
- **Option sets (2–7 choices) use `ToggleGroup`.** Do not loop `Button` with a manual active state.
- **Use `FieldSet` + `FieldLegend` to group related checkboxes/radios.** Do not use a `div` with a heading.
- **Field validation uses `data-invalid` + `aria-invalid`.** Put `data-invalid` on `Field` and `aria-invalid` on the control. For disabled: put `data-disabled` on `Field` and `disabled` on the control.

### Component Structure → [composition.md](./rules/composition.md)

- **Items are always inside their Group.** `SelectItem` → `SelectGroup`. `DropdownMenuItem` → `DropdownMenuGroup`. `CommandItem` → `CommandGroup`.
- **Use `asChild` (radix) or `render` (base) for custom triggers.** Check the `base` field from `npx shadcn@latest info`. → [base-vs-radix.md](./rules/base-vs-radix.md)
- **Dialog, Sheet, and Drawer always need a Title.** `DialogTitle`, `SheetTitle`, and `DrawerTitle` are necessary for accessibility. Use `className="sr-only"` to hide the title visually.
- **Use the full Card composition.** Use `CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter`. Do not put all content in `CardContent`.
- **Button has no `isPending`/`isLoading`.** Compose it with `Spinner` + `data-icon` + `disabled`.
- **`TabsTrigger` must be inside `TabsList`.** Never render triggers directly in `Tabs`.
- **`Avatar` always needs `AvatarFallback`.** The fallback shows when the image does not load.

### Use Components, Not Custom Markup → [composition.md](./rules/composition.md)

- **Use existing components before custom markup.** Before you write a styled `div`, check if a component exists.
- **Callouts use `Alert`.** Do not build custom styled divs.
- **Empty states use `Empty`.** Do not build custom empty state markup.
- **Toast follows the project base.** Use `toast` from the `toast` component for
  Base UI projects. Use `toast()` from `sonner` for Radix and React Aria
  projects.
- **Use `Separator`** in place of `<hr>` or `<div className="border-t">`.
- **Use `Skeleton`** for loading placeholders. Do not use custom `animate-pulse` divs.
- **Use `Badge`** in place of custom styled spans.

### Icons → [icons.md](./rules/icons.md)

- **Icons in `Button` use `data-icon`.** Put `data-icon="inline-start"` or `data-icon="inline-end"` on the icon.
- **Do not put sizing classes on icons inside components.** Components set the icon size through CSS. Do not use `size-4` or `w-4 h-4`.
- **Pass icons as objects, not as string keys.** Use `icon={CheckIcon}`, not a string lookup.

### Chat & Messaging → [chat.md](./rules/chat.md)

- **Chat UI composes the chat primitives.** Conversations use `MessageScroller`, rows use `Message`, and surfaces use `Bubble`. Never write custom bubble `div`s or a raw scroll container.
- **`MessageScroller` controls the scroll behavior.** Streaming follow, anchoring, and jump-to-latest (`MessageScrollerButton`) are built in. Do not write a `useStickToBottom`/`ResizeObserver` hook.
- **Attachments use `Attachment`. System notes and dividers use `Marker`.** Do not use `Item` cards or `Separator` + a label.
- **Assistant activity uses `Trace`.** Reasoning, tool calls, sources, and steps are `TraceLine`s in a `Trace`. Use one `Trace` for each run of message parts. Behavior wraps the line: `TraceCollapsible`, a sheet trigger, or a link. Do not use a custom `Collapsible` or a `Marker`.

### CLI

- **Never decode preset codes or build preset URLs manually.** Use `npx shadcn@latest preset decode <code>`, `preset url <code>`, or `preset open <code>`. To detect the preset of a project, use `npx shadcn@latest preset resolve`.
- **Apply preset codes directly with the CLI.** Use `npx shadcn@latest apply <code>` for existing projects. Use `npx shadcn@latest init --preset <code>` to initialize a project.

## Key Patterns

These are the most frequent patterns that make shadcn/ui code correct. For edge cases, see the linked rule files above.

```tsx
// Form layout: FieldGroup + Field, not div + Label.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validation: data-invalid on Field, aria-invalid on the control.
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email.</FieldDescription>
</Field>

// Icons in buttons: data-icon, no sizing classes.
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// Spacing: gap-*, not space-y-*.
<div className="flex flex-col gap-4">  // correct
<div className="space-y-4">           // wrong

// Equal dimensions: size-*, not w-* h-*.
<Avatar className="size-10">   // correct
<Avatar className="w-10 h-10"> // wrong

// Status colors: Badge variants or semantic tokens, not raw colors.
<Badge variant="secondary">+20.1%</Badge>    // correct
<span className="text-emerald-600">+20.1%</span> // wrong
```

## Component Selection

| Need                       | Use                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Button/action              | `Button` with appropriate variant                                                                   |
| Form inputs                | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Toggle between 2–5 options | `ToggleGroup` + `ToggleGroupItem`                                                                   |
| Data display               | `Table`, `Card`, `Badge`, `Avatar`                                                                  |
| Navigation                 | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                     |
| Overlays                   | `Dialog` (modal), `Sheet` (side panel), `Drawer` (bottom sheet), `AlertDialog` (confirmation)       |
| Feedback                   | `toast` (Base UI), `sonner` (Radix/Aria), `Alert`, `Progress`, `Skeleton`, `Spinner`                 |
| Command palette            | `Command` inside `Dialog`                                                                           |
| Charts                     | `Chart` (wraps Recharts)                                                                            |
| Layout                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                          |
| Empty states               | `Empty`                                                                                             |
| Menus                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                            |
| Tooltips/info              | `Tooltip`, `HoverCard`, `Popover`                                                                   |
| Chat / conversation UI     | `MessageScroller`, `Message`, `Bubble`, `Attachment`, `Marker`, `Trace`                             |

## Key Fields

The project context contains these key fields:

- **`aliases`** → Use the actual alias prefix for imports (for example, `@/`, `~/`). Never hardcode it.
- **`isRSC`** → When `true`, a component that uses `useState`, `useEffect`, event handlers, or browser APIs needs `"use client"` at the top of the file. Always check this field before you give advice about the directive.
- **`tailwindVersion`** → `"v4"` uses `@theme inline` blocks. `"v3"` uses `tailwind.config.js`.
- **`tailwindCssFile`** → The global CSS file that defines the custom CSS variables. Always edit this file. Never create a new one.
- **`style`** → The visual treatment of the components (for example, `nova`, `vega`).
- **`base`** → The primitive library (`radix` or `base`). It changes the component APIs and the available props.
- **`iconLibrary`** → Sets the icon imports. Use `lucide-react` for `lucide`, `@tabler/icons-react` for `tabler`, and so on. Never assume `lucide-react`.
- **`resolvedPaths`** → The exact file-system destinations for components, utils, hooks, and other files.
- **`framework`** → The routing and file conventions (for example, Next.js App Router vs Vite SPA).
- **`packageManager`** → Use this for all dependency installs that are not shadcn (for example, `pnpm add date-fns` vs `npm install date-fns`).
- **`preset`** → The resolved preset code and values for the current project. Use `npx shadcn@latest preset resolve --json` when you need only the preset information.

See [cli.md — `info` command](./cli.md) for the full field reference.

## Component Docs, Examples, and Usage

Run `npx shadcn@latest docs <component>` to get the URLs for the documentation, examples, and API reference of a component. Fetch these URLs to get the content.

```bash
npx shadcn@latest docs button dialog select
```

**Before you create, fix, debug, or use a component, always run `npx shadcn@latest docs` and fetch the URLs.** Then you use the correct API and usage patterns, and you do not guess.

## Workflow

1. **Get the project context.** See [Current Project Context](#current-project-context). Run `npx shadcn@latest info` again to refresh it.
2. **Check the installed components first.** Before you run `add`, always check the `components` list in the project context, or list the `resolvedPaths.ui` directory. Do not import components that are not added. Do not add again components that are installed.
3. **Find components.** Use `npx shadcn@latest search`.
4. **Get docs and examples.** Run `npx shadcn@latest docs <component>` to get the URLs, then fetch them. Use `npx shadcn@latest view` to look at registry items that are not installed. To preview changes to installed components, use `npx shadcn@latest add --diff`.
5. **Install or update.** Use `npx shadcn@latest add`. To update existing components, use `--dry-run` and `--diff` to preview the changes first (see [Updating Components](#updating-components) below).
6. **Fix the imports in third-party components.** After you add components from community registries (for example, `@bundui`, `@magicui`), check the added non-UI files for hardcoded import paths such as `@/components/ui/...`. These paths do not match the actual aliases of the project. Use `npx shadcn@latest info` to get the correct `ui` alias (for example, `@workspace/ui/components`), and change the imports to match. The CLI changes the imports of its own UI files. Third-party registry components can use default paths that do not match the project.
7. **Review the added components.** After you add a component or block from a registry, **always read the added files and make sure that they are correct.**
   - Check for missing sub-components (for example, `SelectItem` without `SelectGroup`), missing imports, incorrect composition, and violations of the [Critical Rules](#critical-rules).
   - Replace the icon imports with the `iconLibrary` of the project. For example, if the registry item uses `lucide-react` and the project uses `hugeicons`, change the imports and icon names.
   - Fix all problems before you continue.
8. **The registry must be explicit.** When the user asks to add a block or component, **do not guess the registry**. If the user does not specify a registry (for example, "add a login block" without `@shadcn`, `@tailark`, `owner/repo`, or similar), ask which registry to use. Never select a default registry for the user.
9. **Switch presets.** First ask the user: **overwrite**, **partial**, **merge**, or **skip**?
   - **Inspect the current preset**: `npx shadcn@latest preset resolve`. Use `--json` when you need structured values.
   - **Inspect the incoming preset**: `npx shadcn@latest preset decode <code>`. Use `preset url <code>` or `preset open <code>` to share or open the preset builder.
   - **Overwrite**: `npx shadcn@latest apply <code>`. This overwrites the detected components, fonts, and CSS variables.
   - **Partial**: `npx shadcn@latest apply <code> --only theme,font`. This updates only the selected preset parts and does not reinstall UI components. The supported values are `theme` and `font`. Comma-separated combinations are allowed. `icon` is intentionally not supported, because icon changes can need a full component reinstall and transforms.
   - **Merge**: Run `npx shadcn@latest init --preset <code> --force --no-reinstall`. Then run `npx shadcn@latest info` to list the installed components. Then, for each installed component, use `--dry-run` and `--diff` to [smart merge](#updating-components) it.
   - **Skip**: `npx shadcn@latest init --preset <code> --force --no-reinstall`. This updates only the config and CSS. It does not change the components.
   - **Important**: Always run preset commands in the project directory of the user. `apply` works only in an existing project with a `components.json` file. The CLI keeps the current base (`base` vs `radix`) from `components.json`. If you must use a scratch or temp directory (for example, for `--dry-run` comparisons), pass `--base <current-base>` explicitly. Preset codes do not encode the base.

## Design Systems from DESIGN.md

When the user asks for a design system from a `DESIGN.md` (or a brand spec), with or without a preset, follow all of [design-system.md](./design-system.md):

1. Run `init --preset <code> --template <vite|next> --name <app> --no-monorepo -y`. Without a preset code, select the closest style and pass `--base base --preset <style>`. Then run `add --all -y`.
2. Before you edit, read the DESIGN.md frontmatter, Do's and Don'ts, and Known Gaps.
3. Map its tokens to the shadcn variables in `tailwindCssFile`. Pin the radius scale, shadows, fonts, and `type-*` utilities.
4. Restyle the components through their `cva` variants. Change the control heights together.
5. Build the design system page as [design-system-page.md](./design-system-page.md) specifies: contrast-checked color roles, type specimens, pinned state matrices, edge cases, do/don't pairs, and recipes. Check the coverage with `scripts/showcase-coverage.mjs`.
6. Verify in a browser: typecheck, no console errors, the page loads at the top, no horizontal overflow, and dark mode works.

## Updating Components

When the user asks to update a component from upstream and keep their local changes, use `--dry-run` and `--diff` to merge. **NEVER fetch raw files from GitHub manually. Always use the CLI.**

Warning: **Never use `--overwrite` without the explicit approval of the user.**

1. Run `npx shadcn@latest add <component> --dry-run` to see all files that the update changes.
2. For each file, run `npx shadcn@latest add <component> --diff <file>` to compare upstream and local.
3. Decide for each file from the diff:
   - No local changes → you can overwrite safely.
   - Local changes → read the local file, analyze the diff, and apply the upstream updates. Keep the local changes.
   - The user says "just update everything" → use `--overwrite`, but confirm with the user first.

## Quick Reference

```bash
# Create a new project.
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# Create a design system app (then follow design-system.md).
npx shadcn@latest init --name my-ds --preset b0 --template vite --no-monorepo -y
npx shadcn@latest init --name my-ds --base base --preset maia --template vite --no-monorepo -y
npx shadcn@latest add --all -y

# Create a monorepo project.
npx shadcn@latest init --name my-app --preset base-nova --monorepo
npx shadcn@latest init --name my-app --preset base-nova --template next --monorepo

# Initialize existing project.
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults  # shortcut: --template=next --preset=nova (base style implied)

# Apply a preset to an existing project.
npx shadcn@latest apply a2r6bw
npx shadcn@latest apply a2r6bw --only theme
npx shadcn@latest apply a2r6bw --only font
npx shadcn@latest apply a2r6bw --only theme,font

# Inspect preset codes and project preset state.
npx shadcn@latest preset decode a2r6bw
npx shadcn@latest preset url a2r6bw
npx shadcn@latest preset open a2r6bw
npx shadcn@latest preset resolve
npx shadcn@latest preset resolve --json

# Add components.
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add owner/repo/item
npx shadcn@latest add --all

# Preview changes before adding/updating.
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx
npx shadcn@latest add owner/repo/item --dry-run

# Search registries.
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @tailark -q "stats"
npx shadcn@latest search owner/repo -q "login"
npx shadcn@latest search                          # all configured registries
npx shadcn@latest search @shadcn -q "menu" -t ui  # filter by item type

# Get component docs and example URLs.
npx shadcn@latest docs button dialog select

# View registry item details (for items not yet installed).
npx shadcn@latest view @shadcn/button
npx shadcn@latest view owner/repo/item
```

**Named presets:** `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`
**Templates:** `next`, `vite`, `start`, `react-router`, `astro` (all support `--monorepo`) and `laravel` (not supported for monorepo)
**Preset codes:** Version-prefixed base62 strings (for example, `a2r6bw` or `b0`), from [ui.shadcn.com](https://ui.shadcn.com).

## Detailed References

- [rules/forms.md](./rules/forms.md) — FieldGroup, Field, InputGroup, ToggleGroup, FieldSet, validation states
- [rules/composition.md](./rules/composition.md) — Groups, overlays, Card, Tabs, Avatar, Alert, Empty, Toast, Separator, Skeleton, Badge, Button loading
- [rules/chat.md](./rules/chat.md) — MessageScroller, Message, Bubble, Attachment, Marker, Trace; streaming, anchoring, jump-to-latest, assistant activity rows
- [rules/icons.md](./rules/icons.md) — data-icon, icon sizing, passing icons as objects
- [rules/styling.md](./rules/styling.md) — Semantic colors, variants, className, spacing, size, truncate, dark mode, cn(), z-index
- [rules/base-vs-radix.md](./rules/base-vs-radix.md) — asChild vs render, Select, ToggleGroup, Slider, Accordion
- [cli.md](./cli.md) — Commands, flags, presets, templates
- [registry.md](./registry.md) — Authoring source registries, `include`, item definitions, dependencies, GitHub registry rules
- [customization.md](./customization.md) — Theming, CSS variables, extending components
- [design-system.md](./design-system.md): DESIGN.md (with or without a preset) to a themed app: style picking, token mapping, radius, fonts, type scale, control heights, showcase traps, verification
- [design-system-page.md](./design-system-page.md): What goes on a design system page and how: foundations, component tiers, pinned state matrices, contrast pairs, edge cases, do/don't, recipes
