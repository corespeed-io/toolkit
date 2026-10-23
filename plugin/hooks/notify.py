"""Stop/Notification: show a macOS notification. Does nothing on other systems."""
import json
import os
import subprocess
import sys

if __name__ == "__main__" and sys.platform == "darwin":
    title = sys.argv[1] if len(sys.argv) > 1 else "Agent"
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    project = os.path.basename(event.get("cwd") or os.getcwd())
    message = (event.get("message") or project).replace('"', "'")
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}" subtitle "{project}"'])
