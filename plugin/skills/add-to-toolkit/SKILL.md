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

The environment installs the skills from `spinsirr/toolkit`. Its setup script clones it to `~/toolkit` and runs `python3 ~/toolkit/scripts/apply.py ensemble`, which imports `AGENTS.md` and links the subagents. The environment instructions hold only the rules for Agent Ensemble. Hooks are not used. Memory is CoreSpeed Memory, not Lore.

The platform cannot push to `spinsirr/toolkit`. It can push to the fork `corespeed-io/toolkit`, which holds only branches: its `main` is not used. To change the toolkit from a session:

1. Start a child session with `spawn_agent`, with `repo: "corespeed-io/toolkit"`. Give it the exact change (file paths and text), and these steps:
   1. `git fetch https://github.com/spinsirr/toolkit.git main && git checkout -b <topic> FETCH_HEAD`
   2. Make the change and do step 1 above. Commit.
   3. `git push origin <topic>`
   4. Reply with `https://github.com/spinsirr/toolkit/compare/main...corespeed-io:toolkit:<topic>?expand=1`.
2. Give the user that link. The user opens the PR and merges it. Sessions that start after the merge get the change.

Do not push the clone in `~/toolkit`. A rule for all machines goes in `AGENTS.md`. You cannot edit the environment instructions: for a rule only for Agent Ensemble, give the user the exact text.

## Sync

Other machines sync by themselves after a push: the `sync.sh pull` SessionStart hook pulls the repo (fast-forward only) and runs `install.sh`. The new version loads in the session after that. Sync errors are in `~/.cache/toolkit-sync/error`, and the next session shows them.
