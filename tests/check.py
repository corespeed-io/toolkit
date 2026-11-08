"""Run: python3 tests/check.py. CI runs it on each pull request."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "scripts")]

from apply import BLOCK_MARK, for_tool, merge, set_toml_keys, with_block, without_star_forms

assert merge({"a": [1], "b": {"x": 1}, "k": 0}, {"a": [1, 2], "b": {"y": 2}}) == {"a": [1, 2], "b": {"x": 1, "y": 2}, "k": 0}

old = ["Bash(rm -rf ~/x)", "Bash(*)", "Write(*)", "Edit(*)", "WebFetch(*)"]
allow = without_star_forms(merge({"allow": old}, {"allow": ["Write", "Edit"]})["allow"])
assert allow == ["Bash(rm -rf ~/x)", "Bash(*)", "WebFetch(*)", "Write", "Edit"], allow

toml = 'model = "m"\nx = 1\n\n[desktop]\nx = 2\n'
out = set_toml_keys(toml, ["x = 5", "new = true"])
assert out.startswith('model = "m"\nx = 5\nnew = true\n'), out
assert "[desktop]\nx = 2\n" in out, out
assert set_toml_keys(out, ["x = 5", "new = true"]) == out
assert set_toml_keys("", ["a = 1"]) == "a = 1\n\n"
env = {"LORE_PROFILE_CLAUDE": "", "LORE_PROFILE_CODEX": "codex", "X": "1"}
assert for_tool(env, "codex")["LORE_PROFILE"] == "codex"
assert for_tool(env, "claude")["LORE_PROFILE"] == ""
assert for_tool(env, "claude")["X"] == "1"
once = with_block("platform\n", "toolkit v1\n")
assert once == f"platform\n\n{BLOCK_MARK}\ntoolkit v1\n", once
assert with_block(once, "toolkit v2\n") == f"platform\n\n{BLOCK_MARK}\ntoolkit v2\n"
assert with_block("", "t\n") == f"{BLOCK_MARK}\nt\n"

# The plugin reaches every machine as soon as a change merges, so it must stay content only.
PLUGIN = ROOT / "plugin"
for runs_code in ["hooks", "bin", ".mcp.json", "monitors", ".lsp.json", "settings.json"]:
    assert not (PLUGIN / runs_code).exists(), f"plugin/{runs_code}: the plugin must not run code"
for manifest in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
    assert "version" not in json.loads((PLUGIN / manifest).read_text()), f"plugin/{manifest}: no version, so updates follow each commit"
marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
assert [p["source"] for p in marketplace["plugins"]] == ["./plugin"], marketplace

# Skills must work in every agent: the Agent Skills format, and nothing that only one agent has.
for skill_dir in sorted((PLUGIN / "skills").iterdir()):
    if not skill_dir.is_dir():
        continue
    skill = skill_dir / "SKILL.md"
    assert skill.exists(), f"{skill_dir.name}: no SKILL.md"
    front = re.match(r"---\n(.*?)\n---\n", skill.read_text(), re.S)
    assert front, f"{skill}: no frontmatter"
    name = re.search(r"^name:\s*(\S+)", front.group(1), re.M)
    assert name and name.group(1) == skill_dir.name, f"{skill}: name must be {skill_dir.name}"
    assert re.search(r"^description:", front.group(1), re.M), f"{skill}: no description"
    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".sh", ".py", ".js", ".ts", ".json"}:
            assert "CLAUDE_PLUGIN_" not in path.read_text(errors="ignore"), f"{path}: CLAUDE_PLUGIN_* works only in Claude Code"

# Each patch belongs to a vendored skill (or to the vendored docs), so vendor.py applies it.
lock = json.loads((ROOT / "sources.lock.json").read_text())
for patch in (ROOT / "patches").glob("*.patch"):
    assert patch.stem in lock, f"{patch.name}: {patch.stem} is not in sources.lock.json"

for path in ["settings/claude.json", "personal/claude.json", "personal/mcp.json"]:
    json.loads((ROOT / path).read_text())
print("ok")
