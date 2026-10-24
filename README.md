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

Agent Ensemble uses the fork [corespeed-io/toolkit](https://github.com/corespeed-io/toolkit), because the platform can write only to `corespeed-io` repositories. In the environment:

- Skill source: `corespeed-io/toolkit`, all skills. The `skills` CLI finds them in `plugin/skills`.
- Setup script:

  ```sh
  git clone -q https://github.com/corespeed-io/toolkit.git ~/toolkit
  python3 ~/toolkit/scripts/apply.py ensemble
  ```
- Instructions: the environment's own. `AGENTS.md` is not used there, because Lore is not available in a sandbox.

`apply.py ensemble` only links each subagent that is not installed yet. The `skills` CLI does not install subagents, and some skills use them.

A session changes the toolkit through a PR on the fork (see `add-to-toolkit`). Keep the two repositories in step:

- This repo to the fork: `gh repo sync corespeed-io/toolkit`.
- The fork to this repo: open a PR from `corespeed-io:main` to `spinsirr:main`.
