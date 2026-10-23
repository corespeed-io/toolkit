---
name: principle-never-block-on-the-human
description: "Use when you want to ask \"should I do X?\" about reversible work. Decide, do the work, and show the result. Ask only for irreversible actions or missing credentials."
disable-model-invocation: true
---

# Never Block on the Human

The human supervises asynchronously. Agents must not stop to wait. Make a reasonable decision, continue, and let the human correct the work later. Code changes are reversible and can be reviewed. Thus a wrong decision usually costs less than a stop.

- Do the work, then show it. Do not ask "should I do X?" Do X, and explain why.
- Make the system correct itself. When you see a problem, record it and fix it in the next round.
- Ask only when you are blocked:
  - An action that you cannot undo, for example force-push, deletion of production data, or an external message. These actions must have confirmation.
  - Missing credentials.
- Continue reversible actions without a stop: write code, edit notes, split tasks.
- The human sets the product direction. Execution must not stop to wait for the human.
