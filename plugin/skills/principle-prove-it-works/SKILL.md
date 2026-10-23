---
name: principle-prove-it-works
description: "Use after a task, before you say it is done. Verify the real artifact (run the feature, read the actual value, examine the diff), not a proxy, a self-report, or \"it compiles\"."
disable-model-invocation: true
---

# Prove It Works

Verify each task output. Check the real thing directly. Do not infer from proxies, self-reports, or "it compiles".

**Why:** Work that you did not verify has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) seems cheaper than direct observation. But an action on a wrong inference costs much more than a check of the source.

Check the real thing, not a proxy:
- Check directly that the process is live. Do not check it through derived state.
- Read the actual value, not a cached or derived representation.
- When verification fails, suspect the observation method before you suspect the system.

## Script the check when you can

The strongest proof is a deterministic script that does the same comparison again. A single visual check is weaker. Write the script and run it. Keep its output as an artifact that a reviewer can run again. Then the reviewer does not need to trust your word.

Keep the artifact visible for the human. Commit it only for large or complex work where the record must be auditable later, for example a large port or migration (the **show-me-your-work** skill).
