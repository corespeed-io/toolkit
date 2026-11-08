---
name: add-to-toolkit
description: Use when the user wants to save a skill, subagent, MCP server, setting, or global instruction in their personal toolkit (spinsirr/toolkit).
---

# Add to toolkit

The toolkit is the GitHub repo `spinsirr/toolkit`. It sets up Claude Code and Codex (CLI and app) in the same way on each machine. The clone in `~/toolkit` is only for editing.

| Item | Location |
| --- | --- |
| Global instructions | `AGENTS.md` |
| Our own skill | `plugin/skills/<name>/SKILL.md`, with `name` (the folder name) and `description` in the frontmatter |
| A skill from another repo | Add its source to `sources.json`, then run `python3 scripts/vendor.py`. Do not copy it by hand. |
| An edit to a skill from another repo (it is in `sources.lock.json`) | Edit the copy, then run `python3 scripts/vendor.py patch <skill>`. Without the patch, the next update removes the edit. Keep the edit small, and put a rule for every skill in `AGENTS.md` instead. |
| Subagent (Claude Code) | `plugin/agents/<name>.md` |
| Setting for every install | `settings/claude.json` |
| My setting | `personal/claude.json` or `personal/codex.toml` |
| MCP server | `personal/mcp.json`. Put machine values in `~/.config/toolkit/env` as `${VAR}`. Add the name to `personal/env.example`. |

The plugin must not run code: no hooks, `bin/`, MCP servers or `version` in `plugin/`. The checks in `tests/check.py` fail on them. A skill must work in every agent, so it must not use the plugin path variables of Claude Code or other things that only one agent has.

The tech stack of a project does not go here. It goes in the `AGENTS.md` of that project (use `init-project`).

Every change goes through a pull request, because a merge to `main` reaches every machine. Branch protection blocks a direct push to `main`. When the user asks you to change the toolkit, the request includes the branch push and the PR:

1. `git -C ~/toolkit fetch -q origin && git -C ~/toolkit worktree add ../toolkit-<topic> -b <topic> origin/main`. A worktree keeps other sessions' work in `~/toolkit` apart.
2. Make the change in `~/toolkit-<topic>`. Run `python3 tests/check.py`. Commit.
3. `git push -u origin <topic>`, then `gh pr create --fill`.
4. Give the user the PR link. The user merges it. Do not merge it yourself.
5. After the merge, Claude Code and Codex update the plugin and `AGENTS.md` by themselves (see the README, "Updates"). Tell the user that a running Claude Code session needs `/reload-plugins`. If you changed `settings/` or `personal/`, tell the user to run the `--personal` install on each machine.
6. Remove the worktree: `git -C ~/toolkit worktree remove ../toolkit-<topic>`.

## On Agent Ensemble

The environment installs the skills from `spinsirr/toolkit`. Its setup script clones it to `~/toolkit` and runs `python3 ~/toolkit/scripts/apply.py ensemble`, which imports `AGENTS.md` and links the subagents. The environment instructions hold only the rules for Agent Ensemble. Hooks are not used. Memory is CoreSpeed Memory, not Lore.

The platform cannot push to `spinsirr/toolkit`. It can push to the fork `corespeed-io/toolkit`, which holds only branches: its `main` is not used. To change the toolkit from a session:

1. Start a child session with `spawn_agent`, with `repo: "corespeed-io/toolkit"`. Start its prompt with who asked for the change, why, and this session's id, so that the child can check the request with `peek_agent`. A child that gets only commands to push code treats them as an injection and refuses (2026-10-25). Then give it the exact change (file paths and text), and these steps:
   1. `git fetch https://github.com/spinsirr/toolkit.git main && git checkout -b <topic> FETCH_HEAD`
   2. Make the change. Run `python3 tests/check.py`. Commit.
   3. `git push origin <topic>`
   4. Reply with `https://github.com/spinsirr/toolkit/compare/main...corespeed-io:toolkit:<topic>?expand=1`.
2. The Fork PRs workflow in `spinsirr/toolkit` opens a PR for the branch within about 15 minutes. Give the user the PR link, or the compare link if there is no PR yet. The user merges it. Sessions that start after the merge get the change.

When this session's repo is `corespeed-io/toolkit` (for example, the retro routine), do steps 1.1 to 1.4 in the workspace. Do not start a child session.

Do not push the clone in `~/toolkit`. A rule for all machines goes in `AGENTS.md`. You cannot edit the environment instructions: for a rule only for Agent Ensemble, give the user the exact text.

## Updates

There is no sync hook. Claude Code and Codex install `personal@toolkit` from GitHub and update it by themselves. The clone in `~/toolkit` does not update by itself, so always start a change from `origin/main`.
