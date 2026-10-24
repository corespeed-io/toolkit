---
name: add-to-toolkit
description: Use when the user wants to save a skill, hook, command, agent, MCP server, setting, or global instruction in their personal toolkit at ~/toolkit.
---

# Add to toolkit

The toolkit is a git repo at `~/toolkit`. It sets up Claude Code and Codex (CLI and app) in the same way on each machine.

| Item | Location |
| --- | --- |
| Global instructions | `AGENTS.md` (Codex links to it; Claude Code imports it) |
| Skill | `plugin/skills/<name>/SKILL.md`, with `name` and `description` in the frontmatter |
| Hook | `plugin/hooks/hooks.json` and a script in `plugin/hooks/` |
| Slash command (Claude Code) | `plugin/commands/<name>.md` |
| Subagent (Claude Code) | `plugin/agents/<name>.md` |
| MCP server | `mcp.json`. Put secrets in `.env` as `${VAR}`. Add the name to `.env.example`. |
| Shared setting | `settings/claude.json` or `settings/codex.toml` |

The tech stack of a project does not go here. It goes in the `AGENTS.md` of that project (use `init-project`).

After a change:

1. Increase `version` in `plugin/.claude-plugin/plugin.json` and `plugin/.codex-plugin/plugin.json`.
2. Run `~/toolkit/install.sh`.
3. Commit. Do not push: the `sync.sh push` Stop hook pushes toolkit commits at the end of the turn.
4. Tell the user to restart Claude Code and Codex.

## On Agent Ensemble

The environment installs the skills from its skill source `spinsirr/toolkit`. Its setup script runs `python3 ~/toolkit/scripts/apply.py ensemble`, which links the subagents. The instructions come from the environment, not from `AGENTS.md`. Hooks are not used. Lore is not available.

A sandbox session cannot push to this repo. Do not try to push it in another way. Give the user the exact change (file path and text) to make on a machine that has the toolkit.

## Sync

Other machines sync by themselves after a push: the `sync.sh pull` SessionStart hook pulls the repo (fast-forward only) and runs `install.sh`. The new version loads in the session after that. Sync errors are in `~/.cache/toolkit-sync/error`, and the next session shows them.
