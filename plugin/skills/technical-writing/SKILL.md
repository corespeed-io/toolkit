---
name: technical-writing
description: "Layered technical-writing standard: ASD-STE100 rules first, then Diátaxis structure, Google developer style sentences, and Global English syntax. Use for /technical-writing or to write or review docs, RFCs, readmes, PR descriptions, or commit messages."
disable-model-invocation: true
---

# Technical writing

Write so that a tired engineer understands the text on the first read. Apply all four layers.

**Priority:** The writing standard of the owner is ASD-STE100 Simplified Technical English (see AGENTS.md). If a rule in this skill conflicts with STE, the STE rule wins. The STE layer below includes the STE rules from AGENTS.md.

Three rules apply above the layers:

- **Remove each word that does no work.** If the sentence is correct without a word, remove the word. "In order to" is "to". "It is important to note that" is nothing.
- **Use the short, everyday word.** "Use", not "utilize". "Help", not "facilitate". "Do", not "perform". A long word must give more precision for its length.
- **If a style rule makes a sentence worse, fix the sentence in a different way.** A sentence that obeys each rule and sounds like a machine wrote it is a failure. The STE rules are not optional. Do not break them to fix a sentence.

The codebase is the word list. Write the real name of the symbol, file, flag, or command. Do not write a synonym or a description of it.

Do not invent jargon. Use the words that a developer says aloud: "move", "delete", "a budget that only decreases", not "evacuate", "ratchet", or "endgame". A named pattern is permitted if the doc says what it means the first time. If you find a new bad word, propose it and its replacement in your reply, with the diff, as an addition to the abstract-metaphor rule of `unslop`. Do not edit that skill.

## Change the rhythm

A doc can obey each layer and still read as if a machine wrote it: each sentence short and clipped, no opinion anywhere, nothing specific.

- Use different sentence lengths intentionally, within the STE limits (20 words for an instruction, 25 words for descriptive text). Short sentences make a point. Longer sentences carry a fact with its condition or its result.
- One thought in each sentence does not mean one length for each sentence. Divide a sentence that carries two thoughts. Keep a long sentence that carries one thought, if it is in the limit.
- Give an opinion where the mode permits it. Explanation compares trade-offs, so say what you think of them. Do not only list advantages and disadvantages. Reference stays dry.
- Be specific, not sterile. Not "schema changes can cause issues", but "a column rename fails the build".

## Select the mode first (Diátaxis)

One document has one mode. Two questions select it:

- Does the content help a person act (doing) or understand (thinking)?
- Does it help a person learn, or help a person work?

The four modes are:

- Action + learning: **tutorial**.
- Action + work: **how-to**.
- Understanding + work: **reference**.
- Understanding + learning: **explanation**.

Use these questions on a full document or on one sentence.

**Tutorial: learning by doing.** The success of the learner is your job, not the job of the learner.

- Start with what the learner will build, not what the learner will "learn".
- Each step gives a visible result, early and frequently.
- Tell the learner what they must see: the expected output, the prompt change, the log line.
- Make each explanation one clause and a link.
- Stay concrete. Write as "we", in commands: "First, do x. Now, do y."

**How-to: steps to a goal.** Solve a problem that a person has, not an operation that the machine can do.

- Assume competence. Do not teach.
- Give only actions: no digressions, no background, no completeness for its own sake. Link to those instead.
- Permit forks and judgment: "If you want x, do y."
- Name the guide by the task: "How to calibrate the radar array", not "Radar array calibration".

**Reference: facts for lookup.** Only describe. No instructions, no persuasion, no opinion.

- Be dry, complete, and sure. State facts, options, limits, and errors with no hedging.
- Use the same structure as the thing that you describe, so that a reader can move through code and docs together.
- Put material where readers expect it.
- Generate it from code where possible.

**Explanation: understanding and why.** One topic with limits, that a person can read away from the product.

- Each title must make sense with an implied "About..." before it.
- Start from a real "why" question.
- Give context: design decisions, history, constraints, alternatives.
- Opinion is permitted here and nowhere else.

Do not mix modes. Do not put reference tables in a tutorial, tutorial help in reference, or arguments in a how-to. Divide the content and link the parts.

## Write sentences to the reader (Google developer style)

- Talk to the reader as "you", in the present tense. Use "will" only for things that really occur later.
- Say who does what: "the compiler checks", not "is checked". Use the passive only when the actor is unknown or not important.
- Write instructions as commands: "Click Submit." State facts plainly. Never write "should be done".
- Put the condition before the instruction: "To delete the document, click Delete."
- Put the common case first. Put exceptions after it.
- Sound like a friend who knows the subject. Do not use buzzwords or figurative language. Do not use "please" in instructions. Never use "simply", "easy", or "quickly" in a procedure. If it was simple, the reader would not be here.
- Do not announce future work ("we will soon support..."). Do not start two sentences in sequence with the same phrase.
- Write link text that says where the link goes: the page title or a short description. Never write "click here". Prefer a sentence of context on the page to a link to a different page.
- Headings carry the point, not only the topic ("Select the mode first", not "Modes"). Use sentence case.
  - A task heading is a verb phrase with no subject ("Create an instance").
  - A concept heading is a noun phrase.
  - Use one h1 for each page. Do not skip levels.
- Use numbered lists for sequences and bullets for all other lists. Start a list with a complete sentence. Keep the items parallel.
- Put code in code font. Put UI elements in bold. Use serial commas. Do not use "etc.". Say at the start that a list is not complete.

## Make statements load one at a time (STE rules)

- Write one instruction in each sentence. Write one thought in each sentence everywhere else.
- Keep an instruction to 20 words or less, and a descriptive sentence to 25 words or less. Divide longer sentences.
- Keep a paragraph to six sentences or less.
- Use the active voice and the present tense.
- Use "must" for a requirement. Do not use "shall" or "should" for a requirement.
- Put the warning or condition before the step that it applies to: "If hot oil touches your skin, injuries can occur."
- Keep "the" and "a". "Remove backup file" has two meanings. "Remove the backup file" has one.
- Give each word one meaning and one function, and keep it. If "check" means inspect, do not also use it to mean restrain.
- Select one word for each action and use only that word: "start", not "start" here and "initiate" there.
- Use a verb instead of a noun cluster ("the server checks" instead of "server-side check").
- Write procedures as direct commands. Never write them as narration or in the passive: "Install the component", not "the component must be installed".
- Use a list for a sequence of steps or a set of items.
- Do not use "-ing" words where you can.
- Do not use slang, idiom, or metaphor.

## Leave no sentence open to two meanings (Global English)

- Keep words like "only" and "not" next to the word that they change: "only fails on growth" and "fails only on growth" say different things.
- Divide long noun strings: "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Make each "it", "they", and "this" point to one clear thing. If you are not sure, repeat the noun. Never use "this" or "which" to point to a full clause.
- Do not remove verbs: "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without a verb. Give it one.
- Keep the small words that show structure, for example "that" in "Ensure that the switch is off". Never make clarity worse to get a lower word count.
- Repeat the article in a series when this prevents a wrong reading: "the client and the host", not "the client and host", when they are two things.
- Say which parts "and" or "or" joins when a sentence can group in two ways. "Both...and", "either...or", and "if...then" make the meaning clear at no cost.
- Use periods, not semicolons. Replace an em dash with a new sentence.
- Make text in parentheses a full grammatical unit or its own sentence. Never make plurals with "(s)".
- Do not use slashes: write "a, b, or both" instead of "a/b" or "and/or".
- Call each thing by one name, everywhere. A doc that says "the gate", "the ratchet", and "the budget check" for one thing teaches three things. Do not change text that did not change in meaning.
- Do not use idioms, colloquialisms, Latin abbreviations, or metaphors.

## Voice and repo specifics

- Apply the **unslop** skill to each doc that this skill touches. That skill has the catalog of slop patterns: AI vocabulary, filler, hedging, formatting tells.
- PR descriptions and commit messages are also writing. Each layer except Diátaxis applies to them. A PR body is a briefing that a reviewer can read in less than one minute. Do not paste swarm logs, SHA lists, or metric tables. Link to them.
- Product UI strings are not documentation. Use the copy guidelines of your product for them.
- Indent code snippets with tabs. Write real paths. Make each count or tree claim true at the commit that lands it, and include the command that makes it again.

## Example

Before:

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.
