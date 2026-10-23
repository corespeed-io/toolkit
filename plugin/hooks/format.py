"""PostToolUse: run the project's formatter on the edited file, if the project has one."""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

JS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".css", ".scss", ".html", ".md", ".yaml", ".yml"}


def find_up(start: Path, name: str) -> Path | None:
    for d in [start, *start.parents]:
        if (d / name).exists():
            return d / name
    return None


def formatter(path: Path) -> list[str] | None:
    ext = path.suffix
    if ext in JS:
        for tool in ("biome", "prettier"):
            bin_ = find_up(path.parent, f"node_modules/.bin/{tool}")
            if bin_:
                return [str(bin_), "format", "--write"] if tool == "biome" else [str(bin_), "--write"]
    if ext == ".py" and shutil.which("ruff") and (find_up(path.parent, "pyproject.toml") or find_up(path.parent, "ruff.toml")):
        return ["ruff", "format"]
    if ext == ".go" and shutil.which("gofmt"):
        return ["gofmt", "-w"]
    if ext == ".rs" and shutil.which("rustfmt"):
        return ["rustfmt"]
    return None


if __name__ == "__main__":
    file_path = json.load(sys.stdin).get("tool_input", {}).get("file_path")
    if not file_path or not os.path.isfile(file_path):
        sys.exit(0)
    path = Path(file_path).resolve()
    cmd = formatter(path)
    if cmd:
        result = subprocess.run([*cmd, str(path)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Formatter failed on {path}:\n{result.stderr}", file=sys.stderr)
