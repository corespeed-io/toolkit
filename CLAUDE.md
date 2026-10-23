# Memory

All memory lives in **Lore** (on devbox), accessed through the `lore` MCP server. Don't use gbrain, and don't use Claude Code's local auto-memory files (it is turned off).

- Before answering questions about the user, their past decisions, projects, or infrastructure, check Lore first with `lore_retrieve_context` or `lore_search`.
- Save durable facts, preferences, and decisions with `lore_remember`. Use `shared` scope for knowledge about the user or their projects, and `private` scope for machine-specific details. Search first so you update an existing memory with `lore_update` instead of creating a duplicate.
- If the `lore` MCP is unreachable (it runs `ssh devbox ~/.local/bin/lore-mcp` over Tailscale), tell the user. Don't silently fall back to local files.
