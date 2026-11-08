#!/bin/sh
# Install the toolkit skills and subagents for each agent on this machine. Safe to run again.
#
#   curl -fsSL https://raw.githubusercontent.com/spinsirr/toolkit/main/install.sh | sh
#   curl -fsSL https://raw.githubusercontent.com/spinsirr/toolkit/main/install.sh | sh -s -- --personal
#
# --personal also installs my global instructions (AGENTS.md), my settings and the Lore MCP server.
# It needs ~/.config/toolkit/env: copy personal/env.example.
#
# Each agent then updates the plugin by itself. Run this again only after a change to settings/ or personal/.
# It reads those files from the agent's own copy of the marketplace, so it needs no clone.
# TOOLKIT_REPO and TOOLKIT_REF install another repo or branch, for tests.
set -eu

PERSONAL=0
case "${1:-}" in
  "") ;;
  --personal) PERSONAL=1 ;;
  *) echo "Usage: install.sh [--personal]" >&2; exit 2 ;;
esac
REPO="${TOOLKIT_REPO:-spinsirr/toolkit}"
REF="${TOOLKIT_REF:-}"

CLAUDE="$(command -v claude || true)"
CODEX="$(command -v codex || true)"
APP_CODEX=/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex
if [ -z "$CODEX" ] && [ -x "$APP_CODEX" ]; then CODEX="$APP_CODEX"; fi
export CODEX
if [ -z "$CLAUDE" ] && [ -z "$CODEX" ]; then
  echo "Found neither Claude Code (claude) nor Codex (codex)." >&2
  exit 1
fi

# Update first: an add of a marketplace that exists can succeed without a fetch, and leave an old copy.
# An update fails when nothing is installed yet, and then the add runs.
claude_setup() {
  claude plugin marketplace update toolkit >/dev/null 2>&1 || claude plugin marketplace add "$REPO${REF:+#$REF}"
  claude plugin update personal@toolkit >/dev/null 2>&1 || claude plugin install personal@toolkit
  copy="$HOME/.claude/plugins/marketplaces/toolkit"
  if [ "$PERSONAL" = 0 ]; then
    python3 "$copy/scripts/apply.py" claude
    return
  fi
  python3 "$copy/scripts/apply.py" claude --personal
  # The instructions come from the marketplace copy, so they update with the plugin.
  rm -f "$HOME/.claude/CLAUDE.md"  # it can be a symlink; do not write through it
  printf '@%s/AGENTS.md\n' "$copy" > "$HOME/.claude/CLAUDE.md"
}

codex_setup() {
  home="${CODEX_HOME:-$HOME/.codex}"
  if [ -n "$REF" ]; then set -- --ref "$REF"; else set --; fi
  "$CODEX" plugin marketplace upgrade toolkit >/dev/null 2>&1 || "$CODEX" plugin marketplace add "$REPO" "$@"
  "$CODEX" plugin add personal@toolkit
  if [ "$PERSONAL" = 0 ]; then return; fi
  copy="$home/.tmp/marketplaces/toolkit"
  ln -sfn "$copy/AGENTS.md" "$home/AGENTS.md"
  test -f "$home/AGENTS.md"
  python3 "$copy/scripts/apply.py" codex --personal
}

LOG="$(mktemp -d)"
trap 'rm -rf "$LOG"' EXIT
CLAUDE_PID=""
CODEX_PID=""
if [ -n "$CLAUDE" ]; then (set -e; claude_setup) > "$LOG/claude" 2>&1 & CLAUDE_PID=$!; fi
if [ -n "$CODEX" ]; then (set -e; codex_setup) > "$LOG/codex" 2>&1 & CODEX_PID=$!; fi
fail=0
if [ -n "$CLAUDE_PID" ]; then
  wait "$CLAUDE_PID" || { echo "Claude Code setup failed:"; fail=1; }
  cat "$LOG/claude"
fi
if [ -n "$CODEX_PID" ]; then
  wait "$CODEX_PID" || { echo "Codex setup failed:"; fail=1; }
  cat "$LOG/codex"
fi
[ "$fail" = 0 ] || exit 1
echo "Done. Start a new Claude Code or Codex session."
