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

Put this in the environment setup script:

```sh
git clone -q https://github.com/spinsirr/toolkit.git ~/toolkit
python3 ~/toolkit/scripts/apply.py ensemble
```

- It only adds. It writes `~/toolkit-AGENTS.md` and imports it from `~/.claude/CLAUDE.md`. It appends a copy to `~/.codex/AGENTS.md`. It links each skill and subagent that is not installed yet.
- It does not change the environment instructions, a skill that is already installed, or the hooks. The environment's skill sources install after the setup script, so a skill that they also install keeps their version.
- Memory is CoreSpeed Memory, not Lore: `ensemble/instructions.md` replaces the Lore section of `AGENTS.md`.
- Write-back: `add-to-toolkit` runs `scripts/ensemble_pr.py`, which pushes to `ensemble/<AGENT_ID>` and opens a PR. It needs `TOOLKIT_GH_TOKEN` in the environment: a fine-grained token for this repo only, with Contents and Pull requests read and write.
