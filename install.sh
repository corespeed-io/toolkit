#!/bin/sh
# Set up Claude Code and Codex from this toolkit. Safe to run again. Works on macOS and Linux.
# The two tools install in parallel. Steps for one tool stay in order: they write the same config files.
# Both tools install the plugin from GitHub (spinsirr/toolkit) and update it by themselves.
# Run this again only after a change to settings/ or mcp.json.
set -e
T="$(cd "$(dirname "$0")" && pwd)"
CODEX="$(command -v codex || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex)"
export CODEX
REPO=spinsirr/toolkit

mkdir -p ~/.claude ~/.codex
# The global instructions come from each tool's copy of the marketplace, so they update with the plugin.
rm -f ~/.claude/CLAUDE.md  # it can be a symlink; do not write through it
printf '@%s/.claude/plugins/marketplaces/toolkit/AGENTS.md\n' "$HOME" > ~/.claude/CLAUDE.md

claude_setup() {
  claude plugin marketplace add "$REPO" >/dev/null 2>&1 || claude plugin marketplace update toolkit
  claude plugin install personal@toolkit >/dev/null 2>&1 || claude plugin update personal@toolkit
  python3 "$T/scripts/apply.py" claude
  test -f ~/.claude/plugins/marketplaces/toolkit/AGENTS.md
}

codex_setup() {
  "$CODEX" plugin marketplace add "$REPO" >/dev/null 2>&1 || "$CODEX" plugin marketplace upgrade toolkit
  "$CODEX" plugin add personal@toolkit
  ln -sfn ~/.codex/.tmp/marketplaces/toolkit/AGENTS.md ~/.codex/AGENTS.md
  test -f ~/.codex/AGENTS.md
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
