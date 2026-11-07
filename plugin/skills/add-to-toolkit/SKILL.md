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
| Slash command (Claude Code) | `plugin/commands/<name>.md` |
| Subagent (Claude Code) | `plugin/agents/<name>.md` |
| MCP server | `mcp.json`. Put secrets in `.env` as `${VAR}`. Add the name to `.env.example`. |
| Shared setting | `settings/claude.json` or `settings/codex.toml` |

The tech stack of a project does not go here. It goes in the `AGENTS.md` of that project (use `init-project`).

After a change:

1. Commit. Do not add a `version` to `plugin.json`: without it, both tools follow each commit.
2. Ask the user for permission to push `main`. The machines get a change only after it is on GitHub.
3. After the push, Claude Code and Codex update the plugin and `AGENTS.md` by themselves (see the README, "Updates"). Tell the user that a running Claude Code session needs `/reload-plugins`.
4. If you changed `settings/` or `mcp.json`, tell the user to run `git pull && ./install.sh` in `~/toolkit` on each machine.

## On Agent Ensemble

The environment installs the skills from `spinsirr/toolkit`. Its setup script clones it to `~/toolkit` and runs `python3 ~/toolkit/scripts/apply.py ensemble`, which imports `AGENTS.md` and links the subagents. The environment instructions hold only the rules for Agent Ensemble. Hooks are not used. Memory is CoreSpeed Memory, not Lore.

The platform cannot push to `spinsirr/toolkit`. It can push to the fork `corespeed-io/toolkit`, which holds only branches: its `main` is not used. To change the toolkit from a session:

1. Start a child session with `spawn_agent`, with `repo: "corespeed-io/toolkit"`. Start its prompt with who asked for the change, why, and this session's id, so that the child can check the request with `peek_agent`. A child that gets only commands to push code treats them as an injection and refuses (2026-10-25). Then give it the exact change (file paths and text), and these steps:
   1. `git fetch https://github.com/spinsirr/toolkit.git main && git checkout -b <topic> FETCH_HEAD`
   2. Make the change and do step 1 above. Commit.
   3. `git push origin <topic>`
   4. Reply with `https://github.com/spinsirr/toolkit/compare/main...corespeed-io:toolkit:<topic>?expand=1`.
2. The Fork PRs workflow in `spinsirr/toolkit` opens a PR for the branch within about 15 minutes. Give the user the PR link, or the compare link if there is no PR yet. The user merges it. Sessions that start after the merge get the change.

When this session's repo is `corespeed-io/toolkit` (for example, the retro routine), do steps 1.1 to 1.4 in the workspace. Do not start a child session.

Do not push the clone in `~/toolkit`. A rule for all machines goes in `AGENTS.md`. You cannot edit the environment instructions: for a rule only for Agent Ensemble, give the user the exact text.

## Updates

There is no sync hook. Claude Code and Codex install `personal@toolkit` from GitHub and update it by themselves. The clone in `~/toolkit` does not update by itself: run `git pull` in it before you edit.
