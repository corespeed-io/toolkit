#!/bin/sh
# SessionStart: show the last sync error, then pull the toolkit and reinstall in the background.
# Fast-forward only. Local changes or a diverged branch stop the sync and record an error.
T="${TOOLKIT_DIR:-$HOME/toolkit}"
S="$HOME/.cache/toolkit-sync"
mkdir -p "$S"

if [ -s "$S/error" ]; then
  echo "Toolkit sync error. Tell the user:"
  cat "$S/error"
fi

[ -n "$(find "$S/stamp" -mmin -10 2>/dev/null)" ] && exit 0
touch "$S/stamp"

sync() {
  cd "$T" || { echo "No toolkit repo at $T."; return 1; }
  [ -z "$(git status --porcelain)" ] || { echo "$T has local changes. Commit or stash them."; return 1; }
  git fetch -q origin || { echo "git fetch failed in $T."; return 1; }
  [ "$(git rev-list --count HEAD..@{u})" = 0 ] && return 0
  git merge -q --ff-only @{u} || { echo "$T cannot fast-forward to origin. Rebase or merge it."; return 1; }
  ./install.sh
}

(
  mkdir "$S/lock" 2>/dev/null || exit 0
  trap 'rmdir "$S/lock"' EXIT
  if out=$(sync 2>&1); then
    rm -f "$S/error"
  else
    printf '%s (%s)\n' "$out" "$(date '+%Y-%m-%d %H:%M')" > "$S/error"
  fi
) </dev/null >/dev/null 2>&1 &
