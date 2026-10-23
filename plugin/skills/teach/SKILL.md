---
name: teach
description: "Explain a body of work in plain words so that a person really understands it. Runs the `how` and `why` skills and combines their findings into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain this change or subsystem to me'."
disable-model-invocation: true
---

# Teach

**Explain what a thing is, how it works, and why it has its shape, in one plain account, at the speed of the person. The goal is that the person understands it. The goal is not to change anything.**

Teach uses `how` and `why`:

- First, learn what the work is and what it touches.
- Then run `how` for how it works, and `why` for why it has that shape. These are real skill invocations. They do their own research.
- Combine their findings into one plain explanation. Start with what is important to the person. Go deeper when the person asks.
- You can change the words freely for teaching, with one exception. Keep the confidence language of `why` without changes. Its hedges are findings, not style.

## Steps

1. Decide the few things that the person must understand at the end.
   - Choose them from why the person asks (to change it, to review it, to debug it, or because it is new to them) and from what the person already knows. Get both from the conversation. Do not quiz the person.
   - Do not explain what the person clearly knows already.
   - Put the depth where the question is.
2. Let `how` and `why` do the work. Do not do it again.
   - Read the code yourself to learn the general layout. Then run `how` for how it works and `why` for why.
   - Run them in parallel and combine the results.
   - Make the size agree with the question. For a subsystem, run both. For a small change, one can be sufficient.
   - Keep `why` narrow by default, because its full search is slow. Put the limit in the request itself (a scoped question, git and one or two sources). Then `why` records the skipped categories, as its contract says. Make it wider only when the reasons are the point.
3. Start with a plain definition.
   - Name the thing and say what it is in general terms, as a senior engineer says it aloud. Use its common name if it has one.
   - Then tie it to the current case ("in X, we use this to ...").
   - Then continue: how it works, the deeper reasons, the edge cases.
   - For each part, explain the idea so that it becomes clear: the problem that it solves, and how it really works. When it helps, go through what occurs as the person does the action (opens a long chat, scrolls up).
   - A list of functions and constants is reference, not teaching.
   - Do not print framing labels ("the one idea to hold onto", "the thing to walk away with", "the key insight", "at its core", "TL;DR").
   - Give the smallest complete answer first, one or two sentences, not a dense paragraph. Then stop. Add layers when the person asks. Never write a wall of text.
4. Keep it a conversation, not a lecture or a performance.
   - Offer to go deeper or to move on. Follow the lead of the person.
   - Do not give quizzes. Do not act out pauses. Do not print "Pause". Do not ask the person to say it back. Do not announce "the sentence to nail".
   - Do not mark a part as important or hard ("here is the part worth slowing down on", "this is the tricky part", "here is where it gets interesting"). Just say it.
   - Where you want to pause, stop and let the person answer.
   - If you run one time with no live human, give the full explanation and put each offer to go deeper at the end.
5. Show, do not only tell. Build the picture one diagram at a time.
   - Open the diff, the code, or the debugger when that is the fastest way to make the point clear.
   - Draw when a picture is faster than words.
   - For a thing with three or more moving parts, do not draw one diagram with all of them. Draw a short series. Each diagram draws the last one again and adds one part. Then the reader sees the system come together. One diagram with all parts, especially at the end, is reference, not teaching.
   - For example, to teach a flow from A to B to C, draw it three times. First A to B. Then draw it again and add C. Then draw it again and add the return edge or the next part.
   - Make the medium agree with the idea. Use the two types when the two help.
     - A Mermaid diagram is correct for a flow or a structure where the labels carry the meaning.
     - When the idea is spatial (layout, overlap, scroll position, or a before and after), use the image-generation tool, if the tool has one. Draw it as a marker drawing on a whiteboard, with a few short labels, because image models make long text wrong. Generate that picture. Do not only describe it in words. If the tool has no image generation, draw an SVG or an ASCII sketch.
     - The build-up rule also applies to generated images.
   - A simple single point needs no figure.

## Voice

Write each response with the **unslop** skill, and with the STE rules in AGENTS.md. Use plain spoken English, as you explain something to a colleague.

- Be short. Remove filler and hedging. Keep the part that makes the idea clear.
- State the concrete mechanism, not a metaphor, a framing, or a preview of what comes next.
- This is the target density: "Virtualization runs in two parts, one for rendering and one for loading from disk. When an item scrolls out past the buffer, both its DOM node and its in-memory data are evicted."
- Use normal sentence case, not all-lowercase.
- Do not use em dashes.
- Prefer periods to commas. Keep each sentence to one or two commas. If clauses collect, divide them into separate sentences.
- Give each concept one name, and keep it.
- Do not use mirror sentences ("A without B, or B without A") or tidy closers ("the rest follows", "it all falls out").
- The words in these steps are instructions to you, not labels to print. Do not repeat the structure as headers or stock phrases.

**Reply:** the explanation itself, never a report about what you did or gave. Start with the main point. Then give the plain account of what it is, how it works, and why. Then give the threads that are worth more research with `how` or `why`.
