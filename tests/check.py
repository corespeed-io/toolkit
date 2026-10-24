"""Run: python3 tests/check.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "plugin/hooks"), str(ROOT / "scripts")]

from apply import ensemble_agents, ensemble_hooks, for_tool, merge, set_toml_keys
from guard import reason

for bad in ["rm -rf /", "rm -rf ~", "rm -fr $HOME", "sudo rm -rf /*", "git push --force origin main", "git push -f origin master", "mkfs.ext4 /dev/sda1", "dd if=x of=/dev/disk2"]:
    assert reason(bad), bad
for ok in ["rm -rf node_modules", "rm -rf ./build", "rm -rf ~/tmp/cache", "git push origin main", "git push --force origin feature", "ls -la /"]:
    assert not reason(ok), ok

assert merge({"a": [1], "b": {"x": 1}, "k": 0}, {"a": [1, 2], "b": {"y": 2}}) == {"a": [1, 2], "b": {"x": 1, "y": 2}, "k": 0}

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
base = "# G\n\n## Git\n\n- branch\n\n## Memory: Lore\n\n- lore_search\n\n## Later\n\n- kept\n"
out = ensemble_agents(base, "## Memory: CoreSpeed Memory\n\n- search\n")
assert out == "# G\n\n## Git\n\n- branch\n\n## Memory: CoreSpeed Memory\n\n- search\n\n## Later\n\n- kept\n", out
assert ensemble_agents(base.split("\n## Later")[0] + "\n", "## M\n") == "# G\n\n## Git\n\n- branch\n\n## M\n"

hooks = json.loads((ROOT / "plugin/hooks/hooks.json").read_text())["hooks"]
sandbox = ensemble_hooks(hooks, "/t/plugin")
commands = [h["command"] for groups in sandbox.values() for g in groups for h in g["hooks"]]
assert not any("sync.sh" in c or "notify.py" in c or "CLAUDE_PLUGIN_ROOT" in c for c in commands), commands
assert "SessionStart" not in sandbox and "Notification" not in sandbox, sandbox.keys()
assert any(c.endswith('"/t/plugin/hooks/guard.py"') for c in commands), commands
assert sandbox["Stop"][-1]["hooks"][0]["command"] == 'python3 "/t/plugin/hooks/ensemble_pr.py"'
print("ok")
