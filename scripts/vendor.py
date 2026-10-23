"""Copy third-party skills into plugin/skills and record where they came from.

  python3 scripts/vendor.py          import skills that are not in plugin/skills yet
  python3 scripts/vendor.py --diff   show upstream changes since the locked commit

An imported skill is never overwritten: we edit our copy. Use --diff to pull upstream changes by hand.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parent.parent
SKILLS = TOOLKIT / "plugin/skills"
AGENTS = TOOLKIT / "plugin/agents"
LOCK = TOOLKIT / "sources.lock.json"
CACHE = Path.home() / ".cache/toolkit-vendor"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def fetch(repo: str, ref: str, paths: list[str]) -> tuple[Path, str]:
    """Sparse, shallow checkout of `paths` at `ref`. Returns the checkout dir and the commit sha."""
    dest = CACHE / repo.replace("/", "__")
    if not dest.exists():
        dest.mkdir(parents=True)
        git(dest, "init", "-q")
        git(dest, "remote", "add", "origin", f"https://github.com/{repo}.git")
    git(dest, "sparse-checkout", "set", "--no-cone", *paths)
    git(dest, "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref)
    git(dest, "checkout", "-q", "--force", "FETCH_HEAD")
    return dest, git(dest, "rev-parse", "HEAD")


def license_paths(src: dict) -> list[str]:
    return [src["license"]] if "license" in src else ["LICENSE", "LICENSE.md", "LICENSE.txt"]


def import_all() -> None:
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    for src in json.loads((TOOLKIT / "sources.json").read_text()):
        repo, ref = src["repo"], src.get("ref", "HEAD")
        paths = [src["path"], *license_paths(src)] + ([src["agents"]] if "agents" in src else [])
        checkout, sha = fetch(repo, ref, paths)
        base = checkout / src["path"]
        names = sorted(p.name for p in base.iterdir() if (p / "SKILL.md").exists()) if src["skills"] == "*" else src["skills"]
        for name in names:
            if not (base / name / "SKILL.md").exists():
                sys.exit(f"{repo}: no skill at {src['path']}/{name}")
            if (SKILLS / name).exists():
                if lock.get(name, {}).get("repo") != repo:
                    sys.exit(f"Name clash: {name} from {repo} is already in plugin/skills")
                continue
            shutil.copytree(base / name, SKILLS / name)
            lock[name] = {"repo": repo, "path": f"{src['path']}/{name}", "commit": sha, **({"pinned": True} if "ref" in src else {})}
            print(f"imported {name} from {repo}")
        if "agents" in src:
            AGENTS.mkdir(parents=True, exist_ok=True)
            for agent in (checkout / src["agents"]).glob("*.md"):
                if not (AGENTS / agent.name).exists():
                    shutil.copy2(agent, AGENTS / agent.name)
                    lock[f"agents/{agent.name}"] = {"repo": repo, "path": f"{src['agents']}/{agent.name}", "commit": sha}
                    print(f"imported agent {agent.name} from {repo}")
        for lic in license_paths(src):
            if (checkout / lic).exists():
                shutil.copy2(checkout / lic, TOOLKIT / "licenses" / f"{repo.replace('/', '__')}.txt")
                break
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n")


def diff() -> None:
    lock = json.loads(LOCK.read_text())
    for name, entry in lock.items():
        if entry.get("pinned"):
            continue
        checkout, sha = fetch(entry["repo"], "HEAD", [entry["path"]])
        if sha == entry["commit"]:
            continue
        git(checkout, "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", entry["commit"])
        out = git(checkout, "diff", entry["commit"], sha, "--", entry["path"])
        if out:
            print(f"### {name}: {entry['commit'][:8]} -> {sha[:8]}\n{out}\n")


if __name__ == "__main__":
    diff() if "--diff" in sys.argv else import_all()
