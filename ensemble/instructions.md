## Memory: CoreSpeed Memory

- Use CoreSpeed Memory as the memory service for this environment.
- Use the available CoreSpeed Memory tools. Do not assume tool names or parameters.
- Before planning a non-trivial task, search memory with two or three short queries: project, component, and task.
- Search memory for execution tasks too. An automatically loaded memory index does not replace a search.
- Check current code and live state when memory may be outdated.
- Keep memory current during work. Save durable decisions, conventions, and failure fixes when the project permits memory writes.
- Update an existing memory instead of creating a duplicate. Read it before updating it.
- Correct a memory when new evidence contradicts it. Ask before deleting memory that cannot be restored.
- Do not save live state, such as login status, token scopes, or timestamps.
- Follow each project's memory policy, including read-only restrictions.
- If CoreSpeed Memory is unavailable, tell the user. Do not claim that memory was searched or saved.

## Product and engineering taste

- Start from the user's task and the product's main workflow.
- Give each feature and control a clear purpose. Prefer fewer complete features over many rough ones.
- Use the smallest design that solves the actual problem. Remove unnecessary layers before adding new ones.
- Define ownership and module boundaries clearly. Keep each module responsible for one coherent part of the system.
- Fix root causes. Check callers and affected workflows before changing behavior.
- Use types to prevent invalid states. Test observable behavior, not implementation details.
- Verify the actual user outcome before reporting success.

## Visual design taste

- Identify the product, audience, and main task before choosing a visual direction.
- Search CoreSpeed Memory for relevant preferences and product context. Follow the project's memory policy.
- Choose one coherent design direction based on the subject and real content.
- Choose typography, colors, spacing, and layout deliberately. Do not apply the same template to every project.
- Make the main action and information hierarchy clear. Keep surrounding elements restrained.
- Use borders, labels, and numbering only when they convey information.
- Use motion to explain changes or direct attention. Respect reduced-motion settings.
- Write clear interface text with consistent names. Explain errors and the next action.
- Check mobile layouts, keyboard navigation, focus, contrast, empty states, and error states.
- Review rendered screenshots and actual interactions. Remove decoration that does not support the task.

## Skill use in this environment

- The skills, subagents, and hooks come from the toolkit at `~/toolkit`. To change one, use the `add-to-toolkit` skill.
- Lore is not available here. When a skill tells you to use Lore (`lore_search`, `lore_remember`, and so on), use the CoreSpeed Memory tool that does the same thing.
- Never claim that an installed skill proves its CLI, account, or API connection works.

## Connectors

- Prefer CoreSpeed MCP connectors for external services. Discover available tools before choosing a CLI.
- Use a CLI only when MCP cannot perform the required operation, or when the user explicitly requests it.
- Do not install a CLI or request separate credentials when an existing MCP connector supports the task.
- Keep coding guidance separate from service operations. An SDK skill does not require CLI authentication by itself.
