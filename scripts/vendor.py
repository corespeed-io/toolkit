"""Keep the third-party skills in plugin/skills equal to upstream, plus our patches.

  python3 scripts/vendor.py                  update every skill in sources.json to upstream, then apply its patch
  python3 scripts/vendor.py patch <skill>    save the local edits of one skill as patches/<skill>.patch

Each copy is upstream plus patches/<skill>.patch. An update replaces the copy, so save each local edit as a patch.
Keep a patch small: only edits that change what the skill does. General rules (STE, memory, git) live in AGENTS.md.
A source can list "exclude" globs, relative to the skill folder, for files to leave out (such as build output).
"""
from __future__ import annotations

import difflib
import fnmatch
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parent.parent
SKILLS = TOOLKIT / "plugin/skills"
AGENTS = TOOLKIT / "plugin/agents"
PATCHES = TOOLKIT / "patches"
DOCS = TOOLKIT / "plugin/docs"
DOCS_KEY = "docs"  # its lock entry and patches/docs.patch
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


def copy_skill(upstream: Path, dest: Path, exclude: list[str]) -> None:
    """Copy one upstream skill to dest. `upstream` is a skill folder, or the SKILL.md of a repo whose root is one skill."""
    if upstream.name == "SKILL.md":
        dest.mkdir(parents=True)
        shutil.copy2(upstream, dest / "SKILL.md")
        return
    for path in sorted(upstream.rglob("*")):
        rel = path.relative_to(upstream).as_posix()
        if path.is_dir() or any(fnmatch.fnmatch(rel, pattern) for pattern in exclude):
            continue
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest / rel)


def skill_names(src: dict, base: Path) -> list[str]:
    if src["skills"] != "*":
        return src["skills"]
    return sorted(p.name for p in base.iterdir() if (p / "SKILL.md").exists())


def apply_patch(name: str) -> bool:
    patch = PATCHES / f"{name}.patch"
    if not patch.exists():
        return True
    result = subprocess.run(["git", "apply", "--whitespace=nowarn", str(patch)], cwd=TOOLKIT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"patch failed: {name}\n{result.stderr}", file=sys.stderr)
    return result.returncode == 0


def update() -> None:
    old_lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    lock: dict[str, dict] = {}
    failed: list[str] = []
    for src in json.loads((TOOLKIT / "sources.json").read_text()):
        repo, ref = src["repo"], src.get("ref", "HEAD")
        paths = [src["path"], *license_paths(src)] + [src[k] for k in ("agents", "docs") if k in src]
        checkout, sha = fetch(repo, ref, paths)
        base = checkout / src["path"]
        root_skill = base.name == "SKILL.md"
        if "docs" in src:
            # Files that the skills link to outside their own folder, such as the pstack harness adapter.
            if DOCS.exists():
                shutil.rmtree(DOCS)
            copy_skill(checkout / src["docs"], DOCS, [])
            if not apply_patch(DOCS_KEY):
                failed.append(DOCS_KEY)
            lock[DOCS_KEY] = {"repo": repo, "path": src["docs"], "commit": sha}
        for name in skill_names(src, base):
            upstream = base if root_skill else base / name
            if not (upstream if root_skill else upstream / "SKILL.md").exists():
                sys.exit(f"{repo}: no skill at {upstream.relative_to(checkout)}")
            if name in lock:
                sys.exit(f"Name clash: {name} comes from {lock[name]['repo']} and {repo}")
            dest = SKILLS / name
            if dest.exists() and name not in old_lock:
                sys.exit(f"Name clash: plugin/skills/{name} is our own skill, and {repo} has one with the same name")
            with tempfile.TemporaryDirectory() as tmp:
                saved = Path(tmp) / name
                if dest.exists():
                    shutil.move(dest, saved)
                copy_skill(upstream, dest, src.get("exclude", []))
                if not apply_patch(name):
                    shutil.rmtree(dest)
                    if saved.exists():
                        shutil.move(saved, dest)
                    failed.append(name)
                    if name in old_lock:
                        lock[name] = old_lock[name]
                    continue
            entry = {"repo": repo, "path": src["path"] if root_skill else f"{src['path']}/{name}", "commit": sha}
            lock[name] = {**entry, **({"pinned": True} if "ref" in src else {})}
            if old_lock.get(name, {}).get("commit") != sha:
                print(f"updated {name} from {repo} ({sha[:8]})")
        if "agents" in src:
            AGENTS.mkdir(parents=True, exist_ok=True)
            for agent in sorted((checkout / src["agents"]).glob("*.md")):
                shutil.copy2(agent, AGENTS / agent.name)
                lock[f"agents/{agent.name}"] = {"repo": repo, "path": f"{src['agents']}/{agent.name}", "commit": sha}
        for lic in license_paths(src):
            if (checkout / lic).exists():
                shutil.copy2(checkout / lic, TOOLKIT / "licenses" / f"{repo.replace('/', '__')}.txt")
                break
    for name in sorted(set(old_lock) - set(lock)):
        target = DOCS if name == DOCS_KEY else AGENTS / name.removeprefix("agents/") if name.startswith("agents/") else SKILLS / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        print(f"removed {name}: upstream or sources.json no longer has it")
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n")
    if failed:
        sys.exit(f"These skills kept their old copy because their patch did not apply: {', '.join(failed)}. "
                 "Update the copy by hand, then run: python3 scripts/vendor.py patch <skill>")


def diff_files(old: Path, new: Path, prefix: str) -> str:
    """Unified diff of two folders. `prefix` is new's path from the toolkit root, so `git apply` resolves the paths."""
    rels = sorted({p.relative_to(old).as_posix() for p in old.rglob("*") if p.is_file()}
                  | {p.relative_to(new).as_posix() for p in new.rglob("*") if p.is_file()})
    out: list[str] = []
    for rel in rels:
        a, b = old / rel, new / rel
        if a.exists() and b.exists() and a.read_bytes() == b.read_bytes():
            continue
        a_lines = a.read_text().splitlines(keepends=True) if a.exists() else []
        b_lines = b.read_text().splitlines(keepends=True) if b.exists() else []
        if a_lines == b_lines:
            continue
        path = f"{prefix}/{rel}"
        for line in difflib.unified_diff(a_lines, b_lines, f"a/{path}" if a.exists() else "/dev/null",
                                         f"b/{path}" if b.exists() else "/dev/null"):
            out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def save_patch(name: str) -> None:
    lock = json.loads(LOCK.read_text())
    if name not in lock:
        sys.exit(f"{name} is not a vendored skill (not in sources.lock.json)")
    entry = lock[name]
    if name == DOCS_KEY:
        exclude, ours = [], DOCS
    else:
        src = next(s for s in json.loads((TOOLKIT / "sources.json").read_text())
                   if s["repo"] == entry["repo"] and entry["path"] in (s["path"], f"{s['path']}/{name}"))
        exclude, ours = src.get("exclude", []), SKILLS / name
    checkout, _ = fetch(entry["repo"], entry["commit"], [entry["path"]])
    with tempfile.TemporaryDirectory() as tmp:
        pristine = Path(tmp) / name
        copy_skill(checkout / entry["path"], pristine, exclude)
        patch = diff_files(pristine, ours, ours.relative_to(TOOLKIT).as_posix())
    target = PATCHES / f"{name}.patch"
    if not patch:
        target.unlink(missing_ok=True)
        print(f"{name} equals upstream; no patch")
        return
    PATCHES.mkdir(exist_ok=True)
    target.write_text(patch)
    print(f"saved {target.relative_to(TOOLKIT)} ({patch.count(chr(10))} lines)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        update()
    elif len(args) == 2 and args[0] == "patch":
        save_patch(args[1])
    else:
        sys.exit("Usage: vendor.py | vendor.py patch <skill>")
