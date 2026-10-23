---
name: ketchup
description: "Tell the user what changed in this chat since their last message, in plain words and small visuals. List each item that waits on the user, with all the facts to decide it from the reply alone. Use for /ketchup."
disable-model-invocation: true
---

# Ketchup

Tell the user what changed in this chat since the last message that the user wrote before `/ketchup`. Help the user understand each change, not only its status. Then show each decision that waits on the user, so that the user can make it from your reply alone.

- Notifications and subagent results are not messages from the user.
- Assume that the user remembers their last message and nothing after it.

Use the voice of [`/bro`](../bro/SKILL.md), not its task: plain words, short sentences, no jargon, as one person tells another the news.

- Say what changed for the user, not how you did it. Say "the tests pass", not "CI is green".
- Do not include hashes, file paths, commands, build numbers, and test counts, unless the user needs one to act.
- Call each PR, branch, or agent by a name that the user knows, not by a label that you invented.
- If a fact needs context to make sense, give the context or do not include the fact.

## Collect what changed

Keep this turn read-only. Make visuals only from what you already have. Do not change code, start an app or a job, or post anything.

1. Collect your own work since that message, reports from subagents, and messages from other people in this chat.
2. Check the current state of each PR, CI run, or agent that this chat touched.
3. Check each number that you will show against the facts that it comes from. If you correct one, say so.

An action item is a decision or step that only the user can do. Examples are a product choice, an approval, an action that you cannot undo, or access that you do not have.

- Include each action item that still waits on the user, also one from before their last message.
- Work that you can still do yourself is not an action item.
- Never invent a decision to fill the reply.
- A step that the user did not ask for, and that the work does not need, is not an action item. The exception is a step that you cannot undo and that waits on the user. Give it one line and no visual.

One decision can cover many items, for example each PR in a set that waits for merge. For each item, collect these facts:

- its link
- what it changes for users
- the evidence for your recommendation
- its risk
- your recommendation

Write "unknown" for a fact that the decision needs and that you do not know. Do not include a link that you do not have.

## Write the reply

Use words for the decisions, not for the story.

- Keep the "what happened" part under 100 words, without pictures. Make it shorter when less happened.
- Do not include work that changed nothing for the user.
- Give each item approximately 30 words.
- The reply gets longer with the number of items. Two items need much less than 150 words in total, without pictures. Thirty items need much more.
- Never remove items or make them shorter to stay under a word count. Do not give a count instead of a list, or a link instead of an item. A link can add detail, but the reply alone must be sufficient to decide.

Start with one short sentence. It names what waits on the user, or says that nothing waits. The action items give the detail. If nothing happened and nothing waits on the user, say so and stop.

Then show what happened. Show pictures first:

1. Put the screenshots and videos that the work made inline in the reply.
2. Then add each diagram that explains a change.
3. Then give one short bullet for each thing that the user asked for. Say what the result is, and if it is done, still running, failed, or not checked.
   - Write each line as you say it aloud: "Search was slow from a missing index", not "Search review: done" or "Slow search: missing index".
   - Name each bug that you found and fixed during the work.
   - Each line must be true when a person reads it alone.
   - Never mark something as done if it still waits on the user.
   - Do not repeat what the action items say.
4. Under the summary, give a maximum of three short lines that change what the user knows or must do.
5. Then, in one line, name the remaining work that you can do yourself.

Then list the action items:

- Ask the decision that the user owns, for example merge, approve, or select. Give your recommendation.
- A step that you do first goes in your recommendation. So does each thing that must occur first, and each thing that you cannot undo.
- Give the number or link of each PR, issue, or agent that a decision is about. Do this also in a decision between options.

Make the shape agree with the decision:

- A decision about one item is one bullet. It has the decision, your recommendation, what it changes for users, the evidence for your recommendation, and its risk. Name the item one time.
- If items share a decision, write the decision and your recommendation one time. Then give each item its own bullet, with the highest risk first. Each bullet has the link and name, what it changes for users, the evidence for your recommendation, and its risk. Name the recommendation for an item only if it is different from the recommendation for the decision.
- Give the risk of each item, also when it is low. For example: "Low risk: only the colors change."
- Say what a delay costs only if it is more than a delay, for example a deadline or lost data.

For a decision between options, give each option that the work considered. For each option, say what it gives the user and what it costs, and the current state if there is one. Those costs are the risk of the decision, so do not add a separate risk line. If the screenshots above show the options, write the gain and cost of each option under its screenshot.

## Visuals

A visual is a picture: a screenshot, a video, a Mermaid diagram, a chart or diagram from `/visualize` (or a different chart tool, if `/visualize` is not available), or a generated image. A Markdown table is not a visual, also with before and after columns.

If something is easier to understand as a picture than as sentences, draw it. Examples:

- how a design or system works
- a PR stack or dependency chain, with the state of each PR
- a before and after of a fix
- options side by side

Rules for visuals:

- Never draw a status list, a list of action items, or boxes with no connections.
- Never give a fact two times, in text or in different visuals.
- Keep each visual small, so that a person can read it immediately: a maximum of six boxes, with a maximum of eight words in each box.
- Write labels as plain words that a person says, not tags such as "Tests: pass". A fact that needs a sentence goes in the text, or nowhere.
- Put screenshots and videos inline when the change is visible, not only as links. If a visible change has no screenshot or video, mark its summary line "No screenshot yet," and say there what changed on screen.
- Draw diagrams and charts from facts that you have. Use a Mermaid diagram for how things connect, and a `/visualize` chart for numbers.
- Never invent a number. Never draw or generate a picture of a screen that you did not capture.
- Link only artifacts that exist.
