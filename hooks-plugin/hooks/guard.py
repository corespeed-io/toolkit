"""PreToolUse: block shell commands that destroy data or kill the calling shell. Exit 2 blocks the call."""
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
# The shell that runs `pkill -f <pattern>` has the pattern in its own command line, so it kills itself (exit 144).
SELF_KILL = (r"\bpkill\s+(-\w+\s+)*-\w*f", "pkill -f matches this shell itself. Kill by PID, or use pkill -x <name>")


def reason(command: str) -> str | None:
    for pattern, why in BLOCKED:
        if re.search(pattern, command):
            return f"{why}. Ask the user to run it themselves"
    if re.search(SELF_KILL[0], command):
        return SELF_KILL[1]
    return None


if __name__ == "__main__":
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    why = reason(command)
    if why:
        print(f"Blocked by toolkit guard: {why}.", file=sys.stderr)
        sys.exit(2)
