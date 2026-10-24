"""Agent Ensemble: push the toolkit commits of this session and open a PR for them. Run it again to update the PR.

  python3 ~/toolkit/scripts/ensemble_pr.py

The sandbox is deleted after the session, so a commit that stays local is lost.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

TOOLKIT = Path(os.environ.get("TOOLKIT_DIR", Path.home() / "toolkit"))
BASE = "main"


def fail(message: str) -> None:
    print(f"Toolkit PR: {message}", file=sys.stderr)
    sys.exit(1)


def git(*args: str) -> str:
    result = subprocess.run(["git", "-C", str(TOOLKIT), *args], capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"git {args[0]} failed in {TOOLKIT}: {result.stderr.strip()}")
    return result.stdout.strip()


def github(method: str, path: str, token: str, body: dict | None = None) -> list | dict:
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        fail(f"GitHub {method} {path} returned {e.code}: {e.read().decode()[:300]}")
    raise AssertionError("unreachable")


def main() -> None:
    if git("status", "--porcelain"):
        fail(f"{TOOLKIT} has changes that are not committed. Commit them or revert them.")
    git("fetch", "-q", "origin", BASE)
    commits = git("log", "--reverse", "--format=%s", f"origin/{BASE}..HEAD").splitlines()
    if not commits:
        print(f"Toolkit PR: no commits after origin/{BASE}. Nothing to push.")
        return
    token = os.environ.get("TOOLKIT_GH_TOKEN")
    if not token:
        fail(f"{len(commits)} toolkit commit(s) are not pushed: TOOLKIT_GH_TOKEN is not set in the environment. Tell the user.")
    match = re.search(r"github\.com[:/]([^/]+)/(.+?)(\.git)?$", git("remote", "get-url", "origin"))
    if not match:
        fail("origin is not a GitHub repository.")
    owner, repo = match.group(1), match.group(2)
    branch = f"ensemble/{os.environ['AGENT_ID']}"
    # A credential helper reads the token from the environment, so the token is not in argv.
    helper = "!f() { echo username=x-access-token; echo password=$TOOLKIT_GH_TOKEN; }; f"
    git("-c", "credential.helper=", "-c", f"credential.helper={helper}", "push", "-q", "--force", "origin", f"HEAD:refs/heads/{branch}")
    existing = github("GET", f"/repos/{owner}/{repo}/pulls?state=open&head={owner}:{branch}", token)
    if existing:
        print(f"Toolkit PR updated: {existing[0]['html_url']}")
        return
    title = commits[0] if len(commits) == 1 else f"Toolkit: {len(commits)} changes from an Agent Ensemble session"
    body = "\n".join([*(f"- {c}" for c in commits), "", f"From Agent Ensemble session `{os.environ['AGENT_ID']}`."])
    pr = github("POST", f"/repos/{owner}/{repo}/pulls", token, {"title": title, "head": branch, "base": BASE, "body": body})
    print(f"Toolkit PR: {pr['html_url']}")


if __name__ == "__main__":
    main()
