---
name: blast-radius
description: "Find what a change can break outside the diff before it ships. Prove the one fact that makes it safe by running real code. Use for 'blast radius of X', 'what could this break', or to review a small diff that you do not trust."
disable-model-invocation: true
---

# Blast radius

Find what a change breaks in other parts of the code, before it ships. Use this skill for "blast radius of X", "what could this break", or to review a small diff that you do not trust yet.

This skill is a companion to `how` and `why`:

- `how` tells you what the code does.
- `why` tells you why the code has its shape.
- Blast radius tells you what the change breaks in other parts of the code.

A list of the callers is not the task. An agent can find them with grep in one second. The task is to find the breakage that grep does not show.

## Do not trust your own writeup

A blast-radius writeup that sounds correct has no value. It is convincing whether it is true or not. Thus, do not give back only the writeup. Find the one or two facts that the full analysis depends on. Prove them with code that you run.

### How sure are you

For each fact that the safety of the change depends on, move it as far down this list as is cheap. Say where it stopped.

1. You said it. This has no value alone.
2. You pointed at the line. A real `file:line`, or the source of the library.
3. You showed that the bad case cannot occur. You followed the failure step by step, and it does not get there.
4. You ran it. A script or test calls the real code and fails loudly if you are wrong.
5. You reproduced it in the running app.

Usually, step 4 is one small script. The script imports the same library that the app ships, and calls the exact function that you are not sure about.

## Steps

1. Read the change. Read the diff and the symbols that it adds, changes, and deletes. Find what it now does differently, also the part that the diff does not show. Use step 2 of `why` to get the PR and commits.
2. Find the one fact that makes it safe. Most changes that look risky are safe because of one fact. For example: "this call only drops cache entries that are already dead, and does nothing else". Find that fact. If it is true, it clears most risky cases at the same time. Spend your time here, not on a long list of possible risks.
3. Look where grep stops:
   - Read the source of the library that you call. Check its pinned version and any local patch.
   - Find when things run: microtasks, unmount and teardown, Solid compared to React.
   - Follow what a symbol search does not find: the JSON that an API returns, a DB column, a wire format, another language that reads the same bytes, a feature flag, code three hops downstream.
4. Be honest about each risk. Give it a real probability and a real cost. Keep the risks that you confirmed. List the risks that you checked and cleared separately. Use the same rules as `why`:
   - Cite a real `file:line`.
   - A search that finds nothing is also an answer.
   - Never invent a caller or an API.
5. Prove the one fact. Write a script or test that runs the real code. Run it, and paste the result.
6. For a large or wide change, run it as an `arena`. Ask more than one model the same question, and merge the answers. Different models find different real bugs.

## What to give back

- **What it does.** What changed, also the part that is not clear.
- **The one fact that makes it safe.** State it. Say which step of the list you got it to, and show the proof. If you could not prove it, write "unproven".
- **Risks.** For each risk, give how it breaks, the `file:line`, the probability and the cost, and how to check it. Paste the proof for the important risks.
- **Cleared.** What you checked, and why it is correct.
- **Before you merge.** The cheapest test or repro that finds the real bug. Include the script that you wrote.

Write it with `unslop`. Cite real code. Remove all private data before you put it in a public location.

**Reply:** the writeup above, with the one safety fact proven or marked "unproven".
