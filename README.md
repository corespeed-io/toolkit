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
- Instructions: only the rules for Agent Ensemble. `AGENTS.md` has the rest, and its memory section names the service for each place: Lore on my machines, CoreSpeed Memory on Agent Ensemble.

`apply.py ensemble` only adds. It imports `AGENTS.md` from `~/.claude/CLAUDE.md`, appends a copy to `~/.codex/AGENTS.md`, and links each subagent that is not installed yet. The `skills` CLI does not install subagents, and some skills use them.

This repo is the only source. The platform can push only to `corespeed-io` repositories, so a session pushes a branch to the fork [corespeed-io/toolkit](https://github.com/corespeed-io/toolkit). The Fork PRs workflow (`.github/workflows/fork-prs.yml`) opens a PR here for each new fork branch, every 15 minutes. It needs Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests". The fork's `main` is not used, so nothing needs to be synced.

Self-improvement: sessions record lessons in memory when you correct them (`AGENTS.md`, Memory). The daily `retro` routine curates them and proposes fixes on the branch `retro/next`.
