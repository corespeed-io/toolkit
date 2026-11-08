# toolkit

My skills and subagents for Claude Code and Codex (CLI and app), the same on each machine.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/spinsirr/toolkit/main/install.sh | sh
```

Or, in a Claude Code session: `/plugin install personal --marketplace spinsirr/toolkit`.

`install.sh` finds Claude Code and Codex on the machine and installs the plugin `personal@toolkit` in each one. It needs no clone.

On my machines, add `--personal`. It also installs my global instructions (`AGENTS.md`), my settings (`personal/`) and the Lore MCP server. First copy `personal/env.example` to `~/.config/toolkit/env` and set the values.

```sh
curl -fsSL https://raw.githubusercontent.com/spinsirr/toolkit/main/install.sh | sh -s -- --personal
```

On Windows, use `install.ps1` in PowerShell. It needs Python 3.9 or newer.

```powershell
irm https://raw.githubusercontent.com/spinsirr/toolkit/main/install.ps1 | iex
```

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/spinsirr/toolkit/main/install.ps1))) -Personal
```

On Windows, `-Personal` does not set up the Lore MCP server, because `personal/mcp.json` needs `sh`. It links the Codex `AGENTS.md`, so it needs Developer Mode (Settings → System → For developers).

CI runs both installers on Linux and Windows for each PR (`tests/check_install.py`).

## Layout

- `plugin/`: skills and subagents, installed as `personal@toolkit`.
- `settings/claude.json`: the marketplace and its auto-update. Every install gets it.
- `personal/`: my permissions, Claude Code and Codex settings, and MCP servers. Only `--personal` installs them.
- `AGENTS.md`: my global instructions (engineering taste, Lore memory). Only `--personal` installs them. Tech stacks stay in each project's own `AGENTS.md`.

## Updates

Claude Code and Codex install the plugin from GitHub (`spinsirr/toolkit`, branch `main`) and update it by themselves. There are no hooks and no sync script.

- Codex updates when it starts. Claude Code updates in an interactive session, up to 10 minutes after the first message, and then shows "Run /reload-plugins to apply".
- `plugin.json` has no `version`, so both tools follow each commit on `main`.
- With `--personal`, the global instructions come from each tool's copy of the marketplace (`~/.claude/plugins/marketplaces/toolkit/AGENTS.md`, `~/.codex/.tmp/marketplaces/toolkit/AGENTS.md`), so they update too.
- A change to `settings/` or `personal/` needs `install.sh` again on each machine.

## Change the toolkit

Every change goes through a pull request to `main`. A merge reaches every machine, so `main` accepts only a PR that passes the Check workflow (`.github/workflows/check.yml`), and only the owner merges.

1. Clone, and make a branch from `main`.
2. Make the change. Run `python3 tests/check.py`.
3. Push the branch and open a PR.

The checks keep the plugin safe and portable: no hooks, executables or MCP servers in `plugin/`, no `version`, and each skill in the Agent Skills format (`SKILL.md` with a `name` that matches its folder, and a `description`).

## Third-party skills

Most skills come from other repositories, listed in `sources.json`. Each copy is upstream plus a small patch in `patches/<skill>.patch`, so one command updates every skill:

```sh
python3 scripts/vendor.py
```

- It replaces each copy with upstream (at `HEAD`, or at the `ref` that a source pins), applies the patch, and records the commits in `sources.lock.json`. It also copies new skills from a source that lists `"skills": "*"`, and removes skills that upstream removed.
- If a patch no longer applies, that skill keeps its old copy, and the command fails and names the skill. Update the copy by hand, then save the patch again.
- The Upstream update workflow (`.github/workflows/upstream.yml`) runs it every Monday and opens or updates a PR from the branch `upstream/update`. Review the diff, then merge.
- `exclude` in a source leaves out files, such as Vercel build output. `docs` copies a folder that the skills link to into `plugin/docs`.

To change a third-party skill, edit its copy, then save the edit as a patch:

```sh
python3 scripts/vendor.py patch <skill>
```

Keep a patch small: only edits that change what the skill does. General rules, such as the writing style, memory and git, stay in `AGENTS.md`, which applies to every skill. Our own skills (not in `sources.lock.json`) need no patch.

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

The platform can push only to `corespeed-io` repositories, so a session pushes a branch to the fork [corespeed-io/toolkit](https://github.com/corespeed-io/toolkit). The Fork PRs workflow (`.github/workflows/fork-prs.yml`) opens a PR here for each new fork branch, every 15 minutes. It needs Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests". The fork's `main` is not used, so nothing needs to be synced.

Self-improvement: sessions record lessons in memory when you correct them (`AGENTS.md`, Memory). The daily `retro` routine curates them and proposes fixes on the branch `retro/next`.
