#!/bin/sh
# Set up Claude Code and Codex from this toolkit. Safe to run again. Works on macOS and Linux.
# The two tools install in parallel. Steps for one tool stay in order: they write the same config files.
set -e
T="$(cd "$(dirname "$0")" && pwd)"
CODEX="$(command -v codex || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex)"
export CODEX

mkdir -p ~/.claude ~/.codex
rm -f ~/.claude/CLAUDE.md  # it can be a symlink; do not write through it
printf '@%s/AGENTS.md\n' "$T" > ~/.claude/CLAUDE.md
ln -sfn "$T/AGENTS.md" ~/.codex/AGENTS.md

claude_setup() {
  claude plugin marketplace add "$T" >/dev/null 2>&1 || claude plugin marketplace update toolkit
  claude plugin install personal@toolkit >/dev/null 2>&1 || claude plugin update personal@toolkit
  python3 "$T/scripts/apply.py" claude
}

codex_setup() {
  "$CODEX" plugin marketplace add "$T" >/dev/null 2>&1 || "$CODEX" plugin marketplace upgrade toolkit >/dev/null 2>&1 || true
  "$CODEX" plugin remove personal@toolkit >/dev/null 2>&1 || true
  "$CODEX" plugin add personal@toolkit
  python3 "$T/scripts/apply.py" codex
}

LOG="$(mktemp -d)"
trap 'rm -rf "$LOG"' EXIT
(set -e; claude_setup) > "$LOG/claude" 2>&1 & CLAUDE_PID=$!
(set -e; codex_setup) > "$LOG/codex" 2>&1 & CODEX_PID=$!
fail=0
wait $CLAUDE_PID || { echo "Claude Code setup failed:"; fail=1; }
cat "$LOG/claude"
wait $CODEX_PID || { echo "Codex setup failed:"; fail=1; }
cat "$LOG/codex"
[ $fail = 0 ] || exit 1
echo "Done. Restart Claude Code and Codex."
