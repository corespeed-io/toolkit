---
name: unslop
description: Remove AI tells from any writing. Use to edit or review prose, docs, PR text, or chat replies.
disable-model-invocation: true
---

# Unslop

Edit text to remove AI patterns. Find the patterns below, then rewrite. Keep the meaning and the intended tone.

**Priority:** The writing standard of the owner is ASD-STE100 Simplified Technical English (see AGENTS.md). If a rule here conflicts with STE, the STE rule wins.

## Patterns to find and fix

Rule numbers are stable ids that other skills cite. A removed rule leaves a gap.

### Content

3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete them, or expand them with real sources.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source, or delete the attribution.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace them with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Say "is" or "has".
9. **"Not just X, but Y."** State the point directly.
10. **Rule of three.** Do not force ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, and hero all in one paragraph. Select one word and repeat it.
12. **False ranges.** "from X to Y" where X and Y are not on a meaningful scale. List the topics directly.

### Style

13. **Em dash overuse.** Do not use em dashes. Use only periods or commas. Do not use parentheses, en dashes, or hyphens as dash substitutes. If a thought needs separation, end the sentence or use a comma.
14. **Colon overuse.** A colon is correct before a list or an example. Do not use a colon to connect two parts of a sentence. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Rewrite it so that the point stands alone, without a comparison frame. "Describing when the scheduler should fire works best as plain English." The meaning is the same, with no unnecessary punctuation.
15. **Boldface overuse.** Do not make each proper noun or acronym bold.
16. **Inline-header lists.** The tell is a bold label and colon that repeats the line: "**Performance:** Performance improved...". Change those to prose. A bold lead-in is correct, not a tell, if it ends in a period, names the item, and the text after it gives really new detail ("**Schema in TypeScript.** Tables live in one file.").
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove them from headings and bullets.
19. **Curly quotes.** Use straight quotes.

### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove them.
22. **Sycophantic tone.** "Great question! You're absolutely right!" Answer directly.

### Filler

23. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". Delete "It is important to note that".
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "can".
25. **Generic conclusions.** "The future looks bright." State specific plans or facts.

### Jargon

26. **Abstract metaphor nouns.** Substrate (base), wedge, wedge in (add), vector (way, method), locus, vantage, nexus, primitive as a noun, harness as a metaphor, surface as in "API surface", bedrock, scaffolding as a metaphor, modality, paradigm, gold-plating (more than the job needs), ratchet as a metaphor (the real name of the mechanism, or a limit that only gets tighter), evacuate for moving code (move out), endgame (the last phase), north star, flywheel. These words look technical, but usually a plainer concrete word exists. Use the concrete word.

### Plain speech

27. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", and "types that follow your schema" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build".
    - Ask what the sentence tells the reader to do or know. Then write that.
    - If you cannot restate it as a concrete instruction, fact, or number, remove it.
    - One more check: if the sentence can appear without changes in the docs of a different project, it says nothing about this project. Remove it.
28. **Make dense sentences shorter, or divide them.** If the reader must go back to understand a sentence, divide it into two sentences or remove clauses. Write one idea in each sentence. Keep each sentence within the STE limit (20 words for an instruction, 25 words for descriptive text).
29. **Active voice.** Use it. Find "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Use the passive only when the actor is unknown or really not important.
30. **Remove adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured difference. An adverb that supports a weak verb shows that the verb is wrong.
31. **Prefer the plain word.** "utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is almost never clearer.
32. **Mannered prose.** Metaphor or decoration where a literal phrase exists: aphorisms ("wire it or delete it"), rhetorical fragments for effect, code as a person ("the plan holds it"), figurative verbs ("rides along", "stands on"), stock framing phrases. "A dial worth turning" becomes "a parameter worth varying". Say what you mean. Rule 26 covers the metaphor nouns.
33. **Over-compression.** Removed articles, fragments with no verb, symbol-speak, and abbreviations make the reader decode instead of read. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing." Write full sentences with their articles and verbs. Spell out arrows and abbreviations.
