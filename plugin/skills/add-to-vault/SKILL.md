---
name: add-to-vault
description: Use when the user wants to save a new skill, or change their global CLAUDE.md or AGENTS.md, in their personal vault at ~/vault.
---

# Add to vault

The vault is a git repo at `~/vault`:

- `plugin/skills/<name>/SKILL.md`: one folder per skill. The frontmatter needs `name` (matching the folder) and a `description` that says when to use it.
- `CLAUDE.md`: global instructions for Claude Code (linked from `~/.claude/CLAUDE.md`).
- `AGENTS.md`: global instructions for Codex (linked from `~/.codex/AGENTS.md`).

After a change:

1. Bump `version` in `plugin/.claude-plugin/plugin.json` so installed copies refresh.
2. Commit in `~/vault`.
3. Run `~/vault/install.sh` to refresh both tools, then tell the user to restart them.
