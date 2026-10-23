---
name: statechart
description: "Draw what the user of an app sees as a Mermaid statechart from a TLA+ model. States are gray if they work, red if still wrong, green if fixed. Each bug that TLC finds is a numbered path. Use for /statechart, \"show the PM the bug\", or to change an agreed chart into a TLA+ skeleton."
disable-model-invocation: true
---

# Statechart

The chart shows what the user of an app sees. A PM reads it to decide if that behavior is correct.

- Label each state with what is on the screen, for example "Paying".
- Label each step with what the user does or sees, for example "tap Pay" or "the charge goes through".
- Do not put variable names or action names in labels.

The scripts call this user the reader, as in `readerActions` and reader steps.

Run `node <skill dir>/scripts/statechart.mjs --help` to see the commands and how to read a chart. Work in a scratch folder outside the repo. The command writes its files next to its input.

## Select the direction

- Use `from-spec` when a TLA+ model exists, or when the code is sufficiently concrete to model.
- Use `from-chart` when there is no model and the PM must agree on the behavior before somebody writes or changes the code.

If the code already has a TLA+ spec, start from a copy of that spec.

- Add the variables that the user sees. Keep the existing invariants of the spec.
- To audit the code against that spec, make the copy model what the code does. Pass the spec without changes as `--against`.
- Check it with the config that its authors say it passes. Pass that config as `--against-config`, unless it has the file name of the spec.
- One mapping labels the two models. Thus, label states and steps only from variables that the two models have.

In a code model or a new spec:

- Tie each variable and action to code that a reviewer can open. Take its name from that code.
- Make each action one indivisible step in the code.
- Put the file and line of the code that checks each condition of an action in a comment on that condition, as in `\* pay.ts:120`.

## Spec to chart

1. Choose the states of the chart.
   - If the PM cares about something that the screen does not show, put it in the state name. For example, a second charge while the screen still says "Paying" is the state "Paying, charged twice".
   - Start with few states. Divide a state only when the division separates two bugs.
2. Write each rule that the PM agrees to as one invariant, with the sentence of the PM as its comment.
   - Each rule names what the user sees on a screen or gets from a request, and the code that can change it. Refuse a rule that does not have the two.
   - For a rule that applies after everything settles, define `Settled == ~ENABLED System`. `System` is the disjunction of the actions that the user does not do.
   - Report each broken rule as a bug. Never make a rule weaker to make the chart pass.
3. Run `from-spec`. Then complete the mapping file that it writes.
   - Put the labels in `state` and `step`.
   - List the actions of the user in `readerActions`, by action name.
   - If two bugs end on the same screen through different code paths, add `cause` and make it name the code path.
   - To color the states by what the PM cares about, for example "Toast shown", return that group from `group`. The legend names the groups. States that break a rule still get a red border.
4. If there is an open fix, model it from the code and pass that model as `--fixed`.
5. Render each chart with `--png` and look at each PNG. Make sure that each numbered path reads in order. If a label reads like code, fix `state` or `step` and run the command again.
6. Replay the story of each bug against the real code, as a test or a live repro, one step for each model action.
   - Drive only entry points that a user or client can get to. Assert only what they see.
   - A test that asserts a flag that it sets, or that searches the source text, proves nothing.
   - If a run proves part of the story and reading the code proves the remainder, say which part each one proves.
   - If the test copies code that it cannot import, give the commit and line range of the copy. List what the copy does not include.
   - If a bug does not reproduce, assume that the model is wrong until you show otherwise. Fix the model, not the rule.

## Chart to spec

1. Draw the chart that the PM agrees to.
   - Use one region for each thing that changes independently, for example the connection and the sync badge.
   - Add one `%% never` line for each rule, with the sentence of the PM.
   - Draw "the app closes" as an edge to the state that the user sees next.
2. Run `from-chart`. If a rule breaks, the agreed chart has a design bug. Take the bug to the PM.
3. Add the guards and variables of the real code to the spec that `from-chart` wrote. Run `from-chart` again. For each difference that it prints, ask the PM if the code is wrong or if the chart needs a correction.

## Give it to the PM

- Give the PM the PNG and the Mermaid source of each chart.
- Add one line for each bug. Give the rule that it breaks, its steps as the chart numbers them, if it reproduced, and if the open fix fixes it.
- With `--against`, also say if the spec already lists the bug: in the configs that `stories.md` names, in the notes of the spec on what the model does not include, or not at all.
- Do not report that a rule holds while the command lists conditions with no file and line.
- Take each count that you quote from `summary.json`.
- Attach `stories.md` and the command that makes all the files again.
- Say what the model does not include.
