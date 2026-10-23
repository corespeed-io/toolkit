"""PreToolUse: block shell commands that destroy data. Exit 2 blocks the call."""
from __future__ import annotations
import json
import re
import sys

BLOCKED = [
    (r"\brm\s+(-\w*\s+)*-\w*[rR]\w*\s+(-\w+\s+)*(/|~|\$HOME|/\*|~/\*)(\s|$)", "rm -r on / or the home folder"),
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s\+).*\b(main|master)\b", "force push to main/master"),
    (r"\bgit\s+push\b.*\b(main|master)\b.*(\s--force\b|\s-f\b)", "force push to main/master"),
    (r"\bmkfs(\.\w+)?\b", "mkfs formats a disk"),
    (r"\bdd\b.*\bof=/dev/(disk|sd|nvme|rdisk)", "dd onto a disk device"),
    (r"\bchmod\s+-R\s+777\s+/(\s|$)", "chmod -R 777 /"),
]


def reason(command: str) -> str | None:
    for pattern, why in BLOCKED:
        if re.search(pattern, command):
            return why
    return None


if __name__ == "__main__":
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    why = reason(command)
    if why:
        print(f"Blocked by toolkit guard: {why}. Ask the user to run it themselves.", file=sys.stderr)
        sys.exit(2)
