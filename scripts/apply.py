"""Merge the toolkit settings into one tool (Claude Code or Codex).

  apply.py claude              settings/claude.json: the marketplace and its auto-update
  apply.py claude --personal   also personal/claude.json and the MCP servers in personal/mcp.json
  apply.py codex --personal    personal/codex.toml and the MCP servers in personal/mcp.json
  apply.py ensemble            set up an Agent Ensemble sandbox instead: see apply_ensemble
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parent.parent
HOME = Path.home()
# Machine-only values for personal/mcp.json. The file is not in git: copy personal/env.example.
ENV_FILE = HOME / ".config/toolkit/env"
BLOCK_MARK = "<!-- toolkit: apply.py ensemble writes below this line -->"


def merge(base: dict, extra: dict) -> dict:
    """Deep merge. Lists are joined without duplicates. Values in extra win."""
    out = dict(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        elif isinstance(value, list) and isinstance(out.get(key), list):
            out[key] = out[key] + [v for v in value if v not in out[key]]
        else:
            out[key] = value
    return out


def without_star_forms(rules: list[str]) -> list[str]:
    """Drop `Tool(*)` when the bare `Tool` rule is present.

    Claude Code 2.1.319 limits `Write(*)` and `Edit(*)` to the working directories. Older versions read them
    as the bare rule. The bare rule means "every path" in all versions, so it replaces the old form.
    """
    return [r for r in rules if not (r.endswith("(*)") and r[:-3] in rules)]


def set_toml_keys(text: str, lines: list[str]) -> str:
    """Set top-level `key = value` lines in TOML text. Keys go before the first table."""
    for line in lines:
        key = line.split("=", 1)[0].strip()
        pattern = re.compile(rf"^{re.escape(key)}\s*=.*$", re.M)
        first_table = re.search(r"^\[", text, re.M)
        head_end = first_table.start() if first_table else len(text)
        if pattern.search(text[:head_end]):
            text = text[:head_end].replace(pattern.search(text[:head_end]).group(0), line) + text[head_end:]
        else:
            text = text[:head_end].rstrip("\n") + ("\n" if text[:head_end].strip() else "") + line + "\n\n" + text[head_end:].lstrip("\n")
    return text


def load_env() -> dict[str, str]:
    if not ENV_FILE.exists():
        sys.exit(f"Missing {ENV_FILE}. Copy {TOOLKIT / 'personal/env.example'} to it and set the values.")
    env = dict(os.environ)
    for raw in ENV_FILE.read_text().splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def expand(value, env: dict[str, str]):
    if isinstance(value, str):
        missing = [v for v in re.findall(r"\$\{(\w+)\}", value) if v not in env]
        if missing:
            sys.exit(f"Missing in {ENV_FILE}: {', '.join(missing)}")
        return re.sub(r"\$\{(\w+)\}", lambda m: env[m.group(1)], value)
    if isinstance(value, list):
        return [expand(v, env) for v in value]
    if isinstance(value, dict):
        return {k: expand(v, env) for k, v in value.items()}
    return value


def for_tool(env: dict[str, str], tool: str) -> dict[str, str]:
    """Keys that end in _CLAUDE or _CODEX override the base key for that tool."""
    suffix = f"_{tool.upper()}"
    return {**env, **{k[: -len(suffix)]: v for k, v in env.items() if k.endswith(suffix)}}


def run(*cmd: str, check: bool = True) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"Failed: {' '.join(cmd)}\n{result.stdout}{result.stderr}")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def skip_mcp_on_windows() -> bool:
    """personal/mcp.json runs its servers through sh. Windows runs Lore through its own launcher."""
    if sys.platform != "win32":
        return False
    print("Skipped the MCP servers in personal/mcp.json: they need sh. Set up Lore on Windows by hand.")
    return True


def apply_claude(personal: bool) -> None:
    settings = HOME / ".claude/settings.json"
    settings.parent.mkdir(exist_ok=True)
    merged = merge(read_json(settings) if settings.exists() else {}, read_json(TOOLKIT / "settings/claude.json"))
    if personal:
        merged = merge(merged, read_json(TOOLKIT / "personal/claude.json"))
        allow = merged["permissions"]["allow"]
        merged["permissions"]["allow"] = without_star_forms(allow)
    settings.write_text(json.dumps(merged, indent=2) + "\n")
    if not personal or skip_mcp_on_windows():
        return
    env = for_tool(load_env(), "claude")
    for name, raw in read_json(TOOLKIT / "personal/mcp.json").items():
        server = expand(raw, env)
        run("claude", "mcp", "remove", "-s", "user", name, check=False)
        run("claude", "mcp", "add-json", "-s", "user", name, json.dumps({"type": "stdio", **server}))
        print(f"Claude Code MCP server added: {name}")


def apply_codex() -> None:
    """Personal only: the plugin needs no Codex settings."""
    codex = os.environ["CODEX"]
    config = Path(os.environ.get("CODEX_HOME", HOME / ".codex")) / "config.toml"
    keys = [l for l in (TOOLKIT / "personal/codex.toml").read_text().splitlines() if "=" in l and not l.startswith("#")]
    config.write_text(set_toml_keys(config.read_text() if config.exists() else "", keys))
    if skip_mcp_on_windows():
        return
    env = load_env()
    for name, raw in read_json(TOOLKIT / "personal/mcp.json").items():
        server = expand(raw, for_tool(env, "codex"))
        run(codex, "mcp", "remove", name, check=False)
        env_args = [a for k, v in server.get("env", {}).items() for a in ("--env", f"{k}={v}")]
        run(codex, "mcp", "add", name, *env_args, "--", server["command"], *server.get("args", []))
        print(f"Codex MCP server added: {name}")


def with_block(text: str, block: str) -> str:
    """text with the toolkit block at the end. A second run replaces the block. It does not add another one."""
    head = text.split(BLOCK_MARK, 1)[0].rstrip("\n")
    return (head + "\n\n" if head else "") + BLOCK_MARK + "\n" + block


def link_missing(src_dir: Path, dest_dir: Path, pattern: str) -> list[str]:
    """Symlink each item that dest_dir does not have. Return the names that dest_dir already has from another source."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    kept = []
    for src in sorted(src_dir.glob(pattern)):
        dest = dest_dir / src.name
        if dest.is_symlink() and dest.resolve() == src.resolve():
            continue
        if dest.exists() or dest.is_symlink():
            kept.append(src.name)
            continue
        dest.symlink_to(src)
    return kept


def apply_ensemble() -> None:
    """Agent Ensemble sandbox. Run from the environment setup script, after the toolkit is cloned to ~/toolkit.

    This only adds. The environment installs the skills from its skill source and keeps its own instructions.
    This adds AGENTS.md next to those instructions, and the subagents: the skills CLI does not install them, and
    some skills use them. Lore is not reachable from a sandbox, so this does not register mcp.json.
    """
    claude_md = HOME / ".claude/CLAUDE.md"
    claude_md.parent.mkdir(exist_ok=True)
    current = claude_md.read_text() if claude_md.exists() else ""
    line = f"@{TOOLKIT}/AGENTS.md"
    if line not in current.splitlines():
        claude_md.write_text(current.rstrip("\n") + ("\n\n" if current.strip() else "") + line + "\n")
    # Codex does not follow @imports, so its instructions file gets a copy.
    codex_md = HOME / ".codex/AGENTS.md"
    codex_md.parent.mkdir(exist_ok=True)
    codex_md.write_text(with_block(codex_md.read_text() if codex_md.exists() else "", (TOOLKIT / "AGENTS.md").read_text()))

    kept = link_missing(TOOLKIT / "plugin/agents", HOME / ".claude/agents", "*.md")
    print("Toolkit AGENTS.md and subagents added to the sandbox.")
    if kept:
        print(f"Already installed from another source, not changed: {', '.join(kept)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["ensemble"]:
        apply_ensemble()
    elif args in (["claude"], ["claude", "--personal"]):
        apply_claude(personal=len(args) == 2)
    elif args == ["codex", "--personal"]:
        apply_codex()
    else:
        sys.exit("Usage: apply.py claude [--personal] | codex --personal | ensemble")
