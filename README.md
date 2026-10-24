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

Put this in the environment setup script. Clear the environment's skill sources and instructions: the toolkit supplies them.

```sh
git clone -q https://github.com/spinsirr/toolkit.git ~/toolkit
python3 ~/toolkit/scripts/apply.py ensemble
```

- Memory is CoreSpeed Memory, not Lore: `ensemble/instructions.md` replaces the Lore section of `AGENTS.md`.
- Hooks: `guard.py` and `format.py` run. The sync and notification hooks do not.
- Write-back: the `ensemble_pr.py` Stop hook pushes toolkit commits to `ensemble/<AGENT_ID>` and opens a PR. It needs `TOOLKIT_GH_TOKEN` in the environment: a fine-grained token for this repo only, with Contents and Pull requests read and write.
- Codex sessions get the skills and `AGENTS.md`, but not the hooks.
