"""Merge shared settings into one tool (Claude Code or Codex) and register its MCP servers.

`apply.py ensemble` sets up an Agent Ensemble sandbox instead: see apply_ensemble.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parent.parent
HOME = Path.home()
LORE_SECTION = "\n## Memory: Lore\n"
# A fresh sandbox has nothing to pull, and it has no macOS notifications.
SANDBOX_SKIP = ("sync.sh", "notify.py")


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
    env = dict(os.environ)
    env_file = TOOLKIT / ".env"
    if env_file.exists():
        for raw in env_file.read_text().splitlines():
            if "=" in raw and not raw.lstrip().startswith("#"):
                key, value = raw.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def expand(value, env: dict[str, str]):
    if isinstance(value, str):
        missing = [v for v in re.findall(r"\$\{(\w+)\}", value) if v not in env]
        if missing:
            sys.exit(f"Missing in .env: {', '.join(missing)}")
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


def apply_claude(servers: dict, env: dict[str, str]) -> None:
    settings = HOME / ".claude/settings.json"
    current = json.loads(settings.read_text()) if settings.exists() else {}
    settings.write_text(json.dumps(merge(current, json.loads((TOOLKIT / "settings/claude.json").read_text())), indent=2) + "\n")
    for name, raw in servers.items():
        server = expand(raw, for_tool(env, "claude"))
        run("claude", "mcp", "remove", "-s", "user", name, check=False)
        run("claude", "mcp", "add-json", "-s", "user", name, json.dumps({"type": "stdio", **server}))
        print(f"Claude Code MCP server added: {name}")


def apply_codex(servers: dict, env: dict[str, str]) -> None:
    codex = os.environ["CODEX"]
    config = HOME / ".codex/config.toml"
    shared = [l for l in (TOOLKIT / "settings/codex.toml").read_text().splitlines() if "=" in l and not l.startswith("#")]
    config.write_text(set_toml_keys(config.read_text() if config.exists() else "", shared))
    for name, raw in servers.items():
        server = expand(raw, for_tool(env, "codex"))
        run(codex, "mcp", "remove", name, check=False)
        env_args = [a for k, v in server.get("env", {}).items() for a in ("--env", f"{k}={v}")]
        run(codex, "mcp", "add", name, *env_args, "--", server["command"], *server.get("args", []))
        print(f"Codex MCP server added: {name}")


def ensemble_agents(base: str, ensemble: str) -> str:
    """AGENTS.md with its Lore section changed to the Agent Ensemble sections."""
    head, found, rest = base.partition(LORE_SECTION)
    if not found:
        sys.exit(f"AGENTS.md has no {LORE_SECTION.strip()!r} section to replace")
    next_section = rest.find("\n## ")
    return head + "\n" + ensemble.strip("\n") + "\n" + (rest[next_section:] if next_section >= 0 else "")


def ensemble_hooks(hooks: dict, plugin_root: str) -> dict:
    """The plugin hooks as user settings, without the hooks that do not apply in a sandbox, plus the PR hook."""
    out: dict = {}
    for event, groups in hooks.items():
        for group in groups:
            kept = [
                {**h, "command": h["command"].replace("${CLAUDE_PLUGIN_ROOT}", plugin_root)}
                for h in group["hooks"]
                if not any(skip in h["command"] for skip in SANDBOX_SKIP)
            ]
            if kept:
                out.setdefault(event, []).append({**group, "hooks": kept})
    pr_hook = {"type": "command", "command": f'python3 "{plugin_root}/hooks/ensemble_pr.py"', "timeout": 60}
    out.setdefault("Stop", []).append({"hooks": [pr_hook]})
    return out


def link_each(src_dir: Path, dest_dir: Path, pattern: str) -> None:
    """Symlink each item into dest_dir, so that an edit in the sandbox is an edit in the toolkit repo."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted(src_dir.glob(pattern)):
        dest = dest_dir / src.name
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        elif dest.is_dir():
            shutil.rmtree(dest)
        dest.symlink_to(src)


def apply_ensemble() -> None:
    """Agent Ensemble sandbox. Run from the environment setup script, after the toolkit is cloned to ~/toolkit.

    Lore is not reachable from a sandbox, so this does not register mcp.json. The environment supplies CoreSpeed MCP.
    """
    agents = ensemble_agents((TOOLKIT / "AGENTS.md").read_text(), (TOOLKIT / "ensemble/instructions.md").read_text())
    (HOME / "AGENTS.md").write_text(agents)
    (HOME / ".claude").mkdir(exist_ok=True)
    (HOME / ".claude/CLAUDE.md").write_text("@~/AGENTS.md\n")
    (HOME / ".codex").mkdir(exist_ok=True)
    (HOME / ".codex/AGENTS.md").write_text(agents)

    plugin = TOOLKIT / "plugin"
    link_each(plugin / "skills", HOME / ".claude/skills", "*")
    link_each(plugin / "skills", HOME / ".agents/skills", "*")
    link_each(plugin / "agents", HOME / ".claude/agents", "*.md")

    settings = HOME / ".claude/settings.json"
    current = json.loads(settings.read_text()) if settings.exists() else {}
    hooks = ensemble_hooks(json.loads((plugin / "hooks/hooks.json").read_text())["hooks"], str(plugin))
    settings.write_text(json.dumps(merge(current, {"hooks": hooks}), indent=2) + "\n")
    print(f"Toolkit applied to the sandbox: {len(list((plugin / 'skills').iterdir()))} skills, hooks, AGENTS.md")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("claude", "codex", "ensemble"):
        sys.exit("Usage: apply.py claude|codex|ensemble")
    if sys.argv[1] == "ensemble":
        apply_ensemble()
        sys.exit(0)
    servers = json.loads((TOOLKIT / "mcp.json").read_text())
    (apply_claude if sys.argv[1] == "claude" else apply_codex)(servers, load_env())
