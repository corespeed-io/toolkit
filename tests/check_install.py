"""Check the result of install.sh or install.ps1 in this HOME. CI runs it after each install.

Run: python3 tests/check_install.py [--personal]
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
personal = sys.argv[1:] == ["--personal"]
windows = sys.platform == "win32"
skills = {p.name for p in (ROOT / "plugin/skills").iterdir() if (p / "SKILL.md").exists()}


def installed_skills(cache: Path) -> set[str]:
    versions = [p for p in cache.iterdir() if p.is_dir()]
    assert len(versions) == 1, f"{cache}: expected one installed version, found {versions}"
    return {p.name for p in (versions[0] / "skills").iterdir()}


claude_cache = HOME / ".claude/plugins/cache/toolkit/personal"
assert installed_skills(claude_cache) == skills, "Claude Code: the installed skills differ from plugin/skills"
codex_cache = Path(os.environ.get("CODEX_HOME", HOME / ".codex")) / "plugins/cache/toolkit/personal"
assert installed_skills(codex_cache) == skills, "Codex: the installed skills differ from plugin/skills"

settings = json.loads((HOME / ".claude/settings.json").read_text())
assert settings["extraKnownMarketplaces"]["toolkit"]["autoUpdate"] is True, settings
assert settings["enabledPlugins"]["personal@toolkit"] is True, settings

claude_md = HOME / ".claude/CLAUDE.md"
codex_md = Path(os.environ.get("CODEX_HOME", HOME / ".codex")) / "AGENTS.md"
if not personal:
    assert "permissions" not in settings, "a plain install must not add my permissions"
    assert not claude_md.exists() and not os.path.lexists(codex_md), "a plain install must not add my AGENTS.md"
    print("plain install: ok")
    sys.exit(0)

allow = settings["permissions"]["allow"]
assert "Write" in allow and "Edit" in allow and "Write(*)" not in allow and "Edit(*)" not in allow, allow
target = claude_md.read_text().strip().removeprefix("@")
assert Path(target).read_text().startswith("# Global instructions"), target
assert codex_md.is_symlink() and codex_md.read_text().startswith("# Global instructions"), codex_md
config = (codex_md.parent / "config.toml").read_text()
assert 'personality = "pragmatic"' in config, config
if not windows:
    assert "lore" in json.loads((HOME / ".claude.json").read_text()).get("mcpServers", {}), "Claude Code: no lore MCP server"
    assert "[mcp_servers.lore]" in config, "Codex: no lore MCP server"
print("personal install: ok")
