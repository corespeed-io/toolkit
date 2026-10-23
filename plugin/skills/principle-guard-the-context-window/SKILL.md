---
name: principle-guard-the-context-window
description: "Use when context fills up: large outputs, long files, repeated reads, fan-out planning. Send bulk work to subagents. Keep summaries, not raw payloads, in the main thread."
disable-model-invocation: true
---

# Guard the Context Window

Send bulk work to subagents. Keep summaries in the main thread, not raw payloads.

**Why:** Context overflow decreases the quality of reasoning, causes compression errors, and stops progress.

**Pattern:**
- **Size the phases and limit the scope.** Limit the number of files in each phase. Set turn budgets. Include the cost of each mechanism in the budget.
