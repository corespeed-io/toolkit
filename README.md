# toolkit

My setup for Claude Code and Codex (CLI and app), the same on each machine.

```sh
git clone git@github.com:spinsirr/toolkit.git ~/toolkit
cp ~/toolkit/.env.example ~/toolkit/.env   # add keys if mcp.json needs them
~/toolkit/install.sh
```

- `AGENTS.md`: global instructions (engineering taste, Lore memory). Tech stacks stay in each project's own `AGENTS.md`.
- `plugin/`: skills and hooks, installed as `personal@toolkit`.
- `mcp.json`, `settings/`: merged into each tool's config by `install.sh`.
- Check: `python3 tests/check.py`.

## Agent Ensemble sandbox

In the environment:

- Skill source: `spinsirr/toolkit`, all skills. The `skills` CLI finds them in `plugin/skills`.
- Setup script:

  ```sh
  git clone -q https://github.com/spinsirr/toolkit.git ~/toolkit
  python3 ~/toolkit/scripts/apply.py ensemble
  ```

`apply.py ensemble` only adds. It writes `~/toolkit-AGENTS.md` and imports it from `~/.claude/CLAUDE.md`, appends a copy to `~/.codex/AGENTS.md`, and links each subagent that is not installed yet. It does not change the environment instructions, the skills, or the hooks.

- Memory is CoreSpeed Memory, not Lore: `ensemble/instructions.md` replaces the Lore section of `AGENTS.md`.
- Write-back: `add-to-toolkit` runs `scripts/ensemble_pr.py`, which pushes to `ensemble/<AGENT_ID>` and opens a PR. It needs `TOOLKIT_GH_TOKEN` in the environment: a fine-grained token for this repo only, with Contents and Pull requests read and write.
