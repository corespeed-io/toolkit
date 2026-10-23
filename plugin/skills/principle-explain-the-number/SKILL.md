---
name: principle-explain-the-number
description: "Use before you trust, report, or act on a measured number: speedup, regression, throughput, latency, or eval result. Find what limits it, and make sure it measured the work you think."
disable-model-invocation: true
---

# Explain the Number

- **Ask "why not double?"** Name the resource or code path that limits the result. Examples are a core, a lock, the disk, the network, or the load generator itself. Get it from a profile or from system counters that you record during a run. Then map it to the source code. A guess from the code is not a limiter. If you cannot say why the number is not two times better, you do not know what you measured.
- **List what else the number can measure, and use evidence to remove each possibility.** The usual causes are:
  - errors
  - skipped or cached work
  - code that did not run
  - a side that is not tuned (one side with default settings)
  - noise
  - a part that is too small to have an end-to-end effect
- **Keep the evidence with the number.** Put the run count, the spread, and the limiter in the notes or in a linked artifact.

For a performance number, do the full procedure with the [benchmark-checklist](../benchmark-checklist/SKILL.md) skill. For an eval result, ask the same questions about the trials:
- Did each run do the task?
- Does the gap stay the same across trials and models?
- Is the scenario important?

You did not apply this principle if the evidence for a number has no run count, no spread, or no named limiter. You also did not apply it if the time saved is more than the time that the changed part used.

This principle is different from [Prove It Works](../principle-prove-it-works/SKILL.md). That principle checks that an output is real.
