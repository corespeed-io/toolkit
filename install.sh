#!/bin/sh
# Link global instructions and install the personal plugin into Claude Code and Codex.
set -e
V="$(cd "$(dirname "$0")" && pwd)"
CODEX=$(command -v codex || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex)

ln -sfn "$V/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sfn "$V/AGENTS.md" ~/.codex/AGENTS.md

claude plugin marketplace add "$V" 2>/dev/null || claude plugin marketplace update vault
claude plugin install personal@vault 2>/dev/null || claude plugin update personal@vault

"$CODEX" plugin marketplace add "$V" 2>/dev/null || "$CODEX" plugin marketplace upgrade vault || true
"$CODEX" plugin add personal@vault
