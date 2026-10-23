---
name: web-design-guidelines
description: Review UI code against the Web Interface Guidelines. Use when the user asks to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files against the Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below.
2. Read the specified files. If the user did not specify files, ask for the files or a pattern.
3. Check the files against all rules in the fetched guidelines.
4. Write the findings in the terse `file:line` format.

## Guidelines Source

Fetch new guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use the web fetch tool of your harness to get the latest rules (`WebFetch` in Claude Code). If the harness has no fetch tool, use `curl -sL <url>`. The fetched content contains all the rules and the output format instructions.

## Usage

When the user gives a file or a pattern argument:

1. Fetch the guidelines from the source URL above.
2. Read the specified files.
3. Apply all rules from the fetched guidelines.
4. Write the findings in the format that the guidelines specify.

If the user specifies no files, ask the user which files to review.
