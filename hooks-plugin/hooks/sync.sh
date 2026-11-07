#!/bin/sh
# Keep ~/toolkit in step with GitHub.
#   sync.sh pull  (SessionStart) show the last error, then fast-forward and reinstall if behind
#   sync.sh push  (Stop)         push local commits; rebase onto GitHub first if it is ahead
# Work runs in the background under one lock. Errors go to $S/error; the next session shows them.
T="${TOOLKIT_DIR:-$HOME/toolkit}"
S="$HOME/.cache/toolkit-sync"
MODE="${1:-pull}"
mkdir -p "$S"

if [ "$MODE" = pull ]; then
  if [ -s "$S/error" ]; then
    echo "Toolkit sync error. Tell the user:"
    cat "$S/error"
  fi
  [ -n "$(find "$S/stamp" -mmin -10 2>/dev/null)" ] && exit 0
  touch "$S/stamp"
else
  [ "$(git -C "$T" rev-list --count @{u}..HEAD 2>/dev/null)" -gt 0 ] 2>/dev/null || exit 0
fi

pull() {
  [ -z "$(git status --porcelain)" ] || { echo "$T has local changes. Commit or stash them."; return 1; }
  git fetch -q origin || { echo "git fetch failed in $T."; return 1; }
  [ "$(git rev-list --count HEAD..@{u})" = 0 ] && return 0
  git merge -q --ff-only @{u} || { echo "$T cannot fast-forward to origin. Rebase or merge it."; return 1; }
  ./install.sh
}

push() {
  git fetch -q origin || { echo "git fetch failed in $T."; return 1; }
  behind=$(git rev-list --count HEAD..@{u})
  if [ "$behind" != 0 ]; then
    git pull -q --rebase --autostash >/dev/null 2>&1 || { git rebase --abort 2>/dev/null; echo "Rebase onto origin failed in $T. Resolve it, then push."; return 1; }
  fi
  git push -q || { echo "git push failed in $T."; return 1; }
  [ "$behind" = 0 ] || ./install.sh
}

(
  mkdir "$S/lock" 2>/dev/null || exit 0
  trap 'rmdir "$S/lock"' EXIT
  cd "$T" || { echo "No toolkit repo at $T." > "$S/error"; exit 1; }
  if out=$($MODE 2>&1); then
    rm -f "$S/error"
  else
    printf '%s (%s)\n' "$out" "$(date '+%Y-%m-%d %H:%M')" > "$S/error"
  fi
) </dev/null >/dev/null 2>&1 &
