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

The environment setup script clones the toolkit to `~/toolkit` and runs `python3 ~/toolkit/scripts/apply.py ensemble`. The skills and subagents are symlinks into `~/toolkit`, so an edit there is an edit in the repo. Lore is not available. The memory section of `~/AGENTS.md` comes from `ensemble/instructions.md`.

- A rule for all machines goes in `AGENTS.md`. A rule only for Agent Ensemble goes in `ensemble/instructions.md`.
- Do not run `install.sh`. After you change a hook or an instruction file, run `python3 ~/toolkit/scripts/apply.py ensemble`.
- Do steps 1 and 3 above. The sandbox is deleted after the session. The `ensemble_pr.py` Stop hook pushes the commits to the branch `ensemble/<AGENT_ID>` and opens a PR. The user merges it. New sessions get the change after the merge.
- If the Stop hook reports an error, tell the user. Do not push in another way.

## Sync

Other machines sync by themselves after a push: the `sync.sh pull` SessionStart hook pulls the repo (fast-forward only) and runs `install.sh`. The new version loads in the session after that. Sync errors are in `~/.cache/toolkit-sync/error`, and the next session shows them.
