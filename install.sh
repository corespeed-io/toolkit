#!/bin/sh
# Set up Claude Code and Codex from this toolkit. Safe to run again. Works on macOS and Linux.
set -e
T="$(cd "$(dirname "$0")" && pwd)"
CODEX="$(command -v codex || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex)"
export CODEX

mkdir -p ~/.claude ~/.codex
printf '@%s/AGENTS.md\n' "$T" > ~/.claude/CLAUDE.md
ln -sfn "$T/AGENTS.md" ~/.codex/AGENTS.md

claude plugin marketplace add "$T" >/dev/null 2>&1 || claude plugin marketplace update toolkit
claude plugin install personal@toolkit >/dev/null 2>&1 || claude plugin update personal@toolkit

"$CODEX" plugin marketplace add "$T" >/dev/null 2>&1 || "$CODEX" plugin marketplace upgrade toolkit >/dev/null 2>&1 || true
"$CODEX" plugin remove personal@toolkit >/dev/null 2>&1 || true
"$CODEX" plugin add personal@toolkit

python3 "$T/scripts/apply.py"
echo "Done. Restart Claude Code and Codex."
