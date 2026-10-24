---
name: skill-creator
description: Create new skills, change and improve existing skills, and measure skill performance. Use to write a skill from scratch, edit or optimize a skill, run evals or benchmarks with variance analysis on a skill, or optimize a skill description for better triggering.
---

# Skill Creator

This skill creates new skills and improves them in iterations.

## Overview

The process to create a skill has these steps:

1. Decide what the skill must do, and approximately how it does it.
2. Write a draft of the skill.
3. Create some test prompts. Run an agent that has access to the skill on them.
4. Help the user evaluate the results, qualitatively and quantitatively.
   - While the runs operate in the background, write draft quantitative evals if there are none. If evals exist, use them as they are, or change them if necessary. Then explain the evals to the user.
   - Use the `eval-viewer/generate_review.py` script to show the results and the quantitative metrics to the user.
5. Write the skill again from the feedback of the user. Also fix clear flaws that the quantitative benchmarks show.
6. Do the steps again until the result is satisfactory.
7. Make the test set larger and try again at a larger scale.

When you use this skill, find the current step of the user in this process. Then help the user complete the steps that remain. For example:

- The user says "I want to make a skill for X". Help make the intent specific, write a draft, write the test cases, decide how to evaluate, run all the prompts, and do it again.
- The user already has a draft of the skill. Go directly to the eval/iterate part of the loop.

Be flexible. If the user says "I don't need to run a bunch of evaluations, just vibe with me", do that.

After the skill is done (the order is flexible), you can also run the description improver. A separate script optimizes the triggering of the skill.

### Harness support

This skill works in Claude Code and in Codex. Some steps depend on the harness:

- **Skill location.** Claude Code loads skills from `.claude/skills/`, `~/.claude/skills/`, and plugins. Codex loads skills from `~/.codex/skills/`, the project, and plugins. Both read the same `SKILL.md` format (YAML frontmatter with `name` and `description`, then Markdown).
- **Parallel test runs.** Claude Code has subagents. In Codex, run each test as a separate non-interactive process (`codex exec`) if subagents are not available. If neither works, run the tests one at a time yourself (see [Without subagents](#without-subagents-claudeai-and-other-harnesses)).
- **Timing data.** Claude Code sends `total_tokens` and `duration_ms` in each subagent notification. Other harnesses can lack this data. Then record the wall-clock time yourself, or leave the token field out.
- **Description optimization** (`scripts/run_loop.py`, `scripts/run_eval.py`, `scripts/improve_description.py`) calls the `claude -p` CLI and measures triggering in Claude Code only. In Codex, it works only if the `claude` CLI is installed, and the result does not measure Codex triggering.

### Owner rules

- **Memory.** Before you research, search memory for earlier decisions about the skill or its domain. Save durable decisions and lessons in memory (or update the memory that already covers them). Do not write memory to local files.
- **Git.** If the skill is in a git repository and you are on `main` or `master`, make a branch first. Make a small commit at each iteration that works. Do not push unless the user tells you to.

## Communicate with the user

Users of the skill creator have very different knowledge of coding words. Some users have little technical experience. Most users know computers well.

Use the context to decide how to write to the user. Default guidance:

- "evaluation" and "benchmark" are borderline, but you can use them.
- Use "JSON" and "assertion" without explanation only when the user clearly shows that they know these words.

If you are not sure that the user knows a word, give a short definition.

---

## Create a skill

### Capture the intent

First, understand the intent of the user. The current conversation can already contain a workflow that the user wants to capture (for example, "turn this into a skill"). If so, get the answers from the conversation history first: the tools used, the sequence of steps, the corrections that the user made, and the input/output formats. The user can fill the gaps. The user must confirm before you go to the next step.

1. What must this skill let the agent do?
2. When must this skill trigger? (Which user phrases and contexts?)
3. What is the expected output format?
4. Do we need test cases to verify that the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) get value from test cases. Skills with subjective outputs (writing style, art) frequently do not need them. Suggest the applicable default for the skill type, but let the user decide.

### Interview and research

Find the answers about edge cases, input/output formats, example files, success criteria, and dependencies. First, get them from the conversation, memory, and the files. Ask the user only for the answers that you cannot find and that are real preference decisions. Do not write test prompts until you have this information.

Check the available MCP servers. If they help the research (search docs, find similar skills, find best practices), do the research in parallel with subagents if the harness has them. If not, do it yourself. Prepare the context so that the user has less work.

### Write the SKILL.md

From the user interview, fill in these components:

- **name**: The skill identifier.
- **description**: When to trigger, and what the skill does. This is the primary triggering mechanism. Include what the skill does AND the specific contexts when to use it. Put all "when to use" information here, not in the body.
  - At this time, models tend to "undertrigger" skills: they do not use a skill when it is useful. To prevent this, make the descriptions slightly "pushy".
  - For example, do not write only "How to build a simple fast dashboard to display internal Anthropic data." Write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: The necessary tools and dependencies (optional, rarely necessary).
- **The rest of the skill.**

### Skill writing guide

#### Anatomy of a skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive disclosure

Skills load in three levels:

1. **Metadata** (name + description): Always in context (~100 words).
2. **SKILL.md body**: In context when the skill triggers (<500 lines is ideal).
3. **Bundled resources**: Loaded when necessary (no limit; scripts can run without loading).

These word counts are approximate. You can go longer if necessary.

**Key patterns:**

- Keep SKILL.md under 500 lines. If it comes near this limit, add one more level of hierarchy. Add clear pointers that tell the model where to go next.
- Reference files clearly from SKILL.md. Say when to read each file.
- For large reference files (>300 lines), include a table of contents.

**Domain organization**: When a skill supports many domains or frameworks, organize it by variant:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The model reads only the applicable reference file.

#### Principle of lack of surprise

Skills must not contain malware, exploit code, or content that can compromise system security. If someone describes the contents of a skill, the intent must not surprise the user. Do not create misleading skills, or skills that help unauthorized access, data exfiltration, or other malicious activities. A skill such as "roleplay as an XYZ" is permitted.

#### Writing patterns

Use the imperative form in instructions.

**Define output formats** like this:

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern.** Examples are useful. Format them like this (if the examples contain "Input" and "Output", you can change the format slightly):

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing style

- Write the skill text in ASD-STE100 Simplified Technical English, as AGENTS.md specifies. Use "must" for a requirement.
- Explain to the model why each requirement is important. A reason is more effective than many uppercase MUSTs.
- Think about what the model knows and needs. Make the skill general. Do not make it narrow to specific examples.
- Write a draft first. Then read it again with fresh eyes and improve it.

### Test cases

After you write the skill draft, write 2-3 realistic test prompts. Each prompt must be a thing that a real user says. Show them to the user, for example: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save the test cases to `evals/evals.json`. Do not write assertions yet. Write only the prompts. You write draft assertions in the next step, while the runs operate.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema. The schema includes the `assertions` field, which you add later.

## Run and evaluate test cases

Do all of this section as one continuous sequence. Do not stop before the end. Do NOT use `/skill-test` or a different testing skill.

Put the results in `<skill-name>-workspace/`, next to the skill directory. In the workspace, organize the results by iteration (`iteration-1/`, `iteration-2/`, and so on). In each iteration, each test case has a directory (`eval-0/`, `eval-1/`, and so on). Do not create all directories at the start. Create them when you need them.

### Step 1: Start all runs (with-skill AND baseline) in the same turn

For each test case, start two subagents in the same turn: one with the skill and one without it. Do not start the with-skill runs first and the baselines later. Start all runs at the same time, so that they finish at approximately the same time.

In Codex without subagents, start each run as a separate background `codex exec` process with the same instructions.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (the same prompt; the baseline depends on the context):

- **Create a new skill**: No skill. Use the same prompt without the skill path. Save to `without_skill/outputs/`.
- **Improve an existing skill**: The old version. Before you edit, make a snapshot of the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`). Then point the baseline subagent to the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case. The assertions can be empty for now. Give each eval a descriptive name that says what it tests, not only "eval-0". Use this name for the directory too. If this iteration uses new or changed eval prompts, create these files for each new eval directory. They do not carry over from earlier iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While the runs operate, write draft assertions

Do not only wait for the runs to finish. Use this time. Write draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

- Good assertions are objectively verifiable and have descriptive names. A person who looks at the benchmark viewer must immediately understand what each assertion checks.
- Evaluate subjective skills (writing style, design quality) qualitatively. Do not force assertions onto things that need human judgment.

When the assertions are written, update the `eval_metadata.json` files and `evals/evals.json`. Also explain to the user what the viewer shows: the qualitative outputs and the quantitative benchmark.

### Step 3: When runs complete, capture the timing data

In Claude Code, when each subagent task completes, you get a notification with `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only time that you can capture this data. It comes in the task notification, and the harness does not keep it in a different location. Process each notification when it arrives. Do not try to collect them into a batch.

In other harnesses, record the start and end time of each run yourself. If the token count is not available, leave it out.

### Step 4: Grade, aggregate, and start the viewer

When all runs are done:

1. **Grade each run.** Start a grader subagent (or grade yourself) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save the results to `grading.json` in each run directory.
   - The `expectations` array in grading.json must use the fields `text`, `passed`, and `evidence`. Do not use `name`/`met`/`details` or other variants. The viewer depends on these exact field names.
   - For assertions that a program can check, write and run a script. Do not check them by eye. Scripts are faster and more reliable, and you can use them again in later iterations.

2. **Aggregate into a benchmark.** Run the aggregation script from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This makes `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If you make benchmark.json manually, see `references/schemas.md` for the exact schema that the viewer expects.
   Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass.** Read the benchmark data and find patterns that the aggregate statistics can hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for. Examples are assertions that always pass with or without the skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Start the viewer** with the qualitative outputs and the quantitative data:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2 and later, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork, Codex, or headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file. This does not start a server. When the user clicks "Submit All Reviews", the browser downloads the feedback as a `feedback.json` file. After the download, copy `feedback.json` into the workspace directory, so that the next iteration can read it.

   Always use generate_review.py to create the viewer. Do not write custom HTML.

5. **Tell the user**, for example: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:

- **Prompt**: The task that the run got.
- **Output**: The files that the skill made, rendered inline where possible.
- **Previous Output** (iteration 2+): A collapsed section with the output of the last iteration.
- **Formal Grades** (if grading ran): A collapsed section with the assertion pass/fail results.
- **Feedback**: A textbox that saves automatically while the user types.
- **Previous Feedback** (iteration 2+): The comments of the user from the last iteration, below the textbox.

The "Benchmark" tab shows the statistics summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

The user moves between test cases with the prev/next buttons or the arrow keys. When done, the user clicks "Submit All Reviews". This saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you that they are done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means that the user found the result satisfactory. Improve the test cases where the user had specific complaints.

Stop the viewer server when you are done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improve the skill

This is the most important part of the loop. You ran the test cases, and the user reviewed the results. Now you make the skill better from the feedback.

### How to think about improvements

1. **Make the feedback general.** The skill must work across a very large number of different prompts. You and the user iterate on only a few examples, because this is faster: the user knows these examples well and can quickly assess new outputs. But if the skill works only for those examples, it has no value.
   - Do not add small changes that overfit the examples, or MUSTs that restrict the model too much.
   - If a problem stays, try different explanations or recommend different work patterns. This costs little, and it can find a good solution.

2. **Keep the prompt small.** Remove the parts that do not help. Read the transcripts, not only the final outputs. If the skill makes the model spend time on work that does not help, remove the parts of the skill that cause it. Then see what changes.

3. **Explain the reason.** Explain the **reason** for each thing that you ask the model to do. Current LLMs are capable. They understand intent well, and with a good harness they can do more than follow fixed instructions.
   - If the feedback of the user is short or frustrated, try to understand the task, why the user wrote the feedback, and what the user actually wrote. Put this understanding into the instructions.
   - If you write ALWAYS or NEVER in uppercase, or use very rigid structures, stop and examine it. Where possible, explain the reason so that the model understands why the requirement is important. Use lowercase "must" with a reason.

4. **Find repeated work across test cases.** Read the transcripts of the test runs. Find where the subagents each wrote similar helper scripts or used the same multi-step procedure. For example, if all 3 test cases made the subagent write a `create_docx.py` or a `build_chart.py`, the skill must bundle that script. Write it one time, put it in `scripts/`, and tell the skill to use it. Then each future run does not need to write it again.

This task is important, and thinking time is not the limit. Take the necessary time. Write a draft revision, then read it again and improve it. Try to understand what the user wants and needs.

### The iteration loop

After you improve the skill:

1. Apply your improvements to the skill. If the skill is in a git repository, commit this iteration.
2. Run all test cases again into a new `iteration-<N+1>/` directory, with the baseline runs.
   - For a new skill, the baseline is always `without_skill` (no skill). It does not change across iterations.
   - For an existing skill, decide which baseline is applicable: the original version from the user, or the previous iteration.
3. Start the reviewer with `--previous-workspace` that points to the previous iteration.
4. Wait for the user to review and to tell you that they are done.
5. Read the new feedback, improve again, and do the loop again.

Continue until one of these conditions occurs:

- The user says that they are satisfied.
- All feedback is empty (all results are satisfactory).
- You do not make meaningful progress.

---

## Advanced: Blind comparison

Use this when you need a more rigorous comparison between two versions of a skill (for example, the user asks "is the new version actually better?"). Read `agents/comparator.md` and `agents/analyzer.md` for the details.

The procedure:

1. Give two outputs to an independent agent. Do not tell it which output comes from which version.
2. The agent judges the quality.
3. Analyze why the winner won.

This is optional and needs subagents (or separate `codex exec` processes in Codex). Most users do not need it. The human review loop is usually sufficient.

---

## Description optimization

The `description` field in the SKILL.md frontmatter is the primary mechanism that decides if the agent uses a skill. After you create or improve a skill, offer to optimize the description for better triggering.

Note: The scripts in this section call the `claude -p` CLI and measure triggering in Claude Code only. See [Harness support](#harness-support).

### Step 1: Generate trigger eval queries

Create 20 eval queries: a mix of should-trigger and should-not-trigger. Save them as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic. They must be things that a Claude Code, Codex, or Claude.ai user actually types.

- Do not write abstract requests. Write concrete, specific requests with sufficient detail. For example: file paths, personal context about the job or situation of the user, column names and values, company names, URLs, and some backstory.
- Some queries can be in lowercase or contain abbreviations, typos, or casual speech.
- Use a mix of lengths.
- Focus on edge cases, not on clear cases. (The user can approve them later.)

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage:

- Use different phrasings of the same intent, some formal and some casual.
- Include cases where the user does not name the skill or file type, but clearly needs it.
- Add some uncommon use cases.
- Add cases where this skill competes with a different skill but must win.

For the **should-not-trigger** queries (8-10), the most valuable queries are the near-misses. These queries share keywords or concepts with the skill but need something different. Think about:

- adjacent domains;
- ambiguous phrasing where a simple keyword match triggers incorrectly;
- cases where the query touches a function of the skill, but in a context where a different tool is more applicable.

Do not make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy. It does not test anything. The negative cases must be difficult.

### Step 2: Review with the user

Show the eval set to the user for review with the HTML template:

1. Read the template from `assets/eval_review.html`.
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it is a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the name of the skill
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the current description of the skill
3. Write it to a temp file (for example, `/tmp/eval_review_<skill-name>.html`) and open it: `open /tmp/eval_review_<skill-name>.html`
4. The user can edit queries, toggle should-trigger, add or remove entries, and then click "Export Eval Set".
5. The file downloads to `~/Downloads/eval_set.json`. Check the Downloads folder for the most recent version, because there can be more than one (for example, `eval_set (1).json`).

This step is important. Bad eval queries cause bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

Save the eval set to the workspace. Then run this in the background:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt (the model of the current session). Then the triggering test matches what the user actually experiences.

While it runs, read the end of the output periodically. Tell the user the current iteration and the scores.

The script does the full optimization loop automatically:

1. It divides the eval set into 60% train and 40% held-out test.
2. It evaluates the current description. It runs each query 3 times to get a reliable trigger rate.
3. It calls Claude to propose improvements from the failures.
4. It evaluates each new description on train and test again, for a maximum of 5 iterations.
5. When it is done, it opens an HTML report in the browser with the results for each iteration. It returns JSON with `best_description`. The script selects this description by the test score, not the train score, to prevent overfitting.

### How skill triggering works

When you understand the triggering mechanism, you can design better eval queries.

- Skills appear in the `available_skills` list of the agent with their name and description. The agent decides from that description if it uses a skill.
- The agent uses skills only for tasks that it cannot easily do alone. Simple, one-step queries such as "read this PDF" possibly do not trigger a skill, even when the description matches exactly. The agent can do them directly with basic tools.
- Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

Thus, your eval queries must be substantial enough that the agent gets value from a skill. Simple queries such as "read file X" are bad test cases. They do not trigger skills, independent of the description quality.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the SKILL.md frontmatter of the skill. Show the before and after to the user, and report the scores.

---

### Package and present (only if the `present_files` tool is available)

Check if you have access to the `present_files` tool. If not, skip this step. If you have it, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, give the user the path of the `.skill` file so that they can install it.

---

## Without subagents (Claude.ai and other harnesses)

In Claude.ai, and in harnesses without subagents or `codex exec`, the core workflow is the same (draft → test → review → improve → repeat). Some mechanics change:

**Run test cases**: Without subagents, there is no parallel execution. For each test case, read the SKILL.md of the skill. Then follow its instructions to do the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents, because you wrote the skill and also run it with full context. But it is a useful check, and the human review step compensates. Skip the baseline runs. Use the skill to do the task only.

**Review results**: If you cannot open a browser (for example, the Claude.ai VM has no display, or you are on a remote server), skip the browser reviewer. Show the results directly in the conversation. For each test case, show the prompt and the output. If the output is a file that the user must see (such as a .docx or .xlsx), save it to the filesystem and tell the user its location, so that they can download and examine it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking. It needs baseline comparisons, and these have no meaning without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: The same as before. Improve the skill, run the test cases again, and ask for feedback, but without the browser reviewer. If you have a filesystem, you can still organize the results into iteration directories.

**Description optimization**: This section needs the `claude` CLI (specifically `claude -p`), which only Claude Code has. Skip it on Claude.ai.

**Blind comparison**: Needs subagents. Skip it.

**Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem. On Claude.ai, you can run it, and the user can download the `.skill` file.

**Update an existing skill**: The user can ask you to update an existing skill, not to create a new one. In this case:

- **Keep the original name.** Record the directory name and the `name` frontmatter field of the skill, and use them without change. For example, if the installed skill is `research-helper`, the output is `research-helper.skill` (not `research-helper-v2`).
- **Copy the skill to a writable location before you edit.** The installed skill path can be read-only. Copy it to `/tmp/skill-name/`, edit it there, and package from the copy.
- **If you package manually, prepare the files in `/tmp/` first**, then copy them to the output directory. Direct writes can fail because of permissions.

---

## Cowork-specific instructions

In Cowork:

- You have subagents, so the main workflow works: start the test cases in parallel, run baselines, grade, and so on. If timeouts cause severe problems, you can run the test prompts in series.
- You have no browser or display. When you generate the eval viewer, use `--static <output_path>` to write a standalone HTML file. Do not start a server. Then give the user a link to open the HTML in their browser.
- Cowork frequently makes the agent skip the eval viewer after the tests. In all harnesses, after the tests run, you must generate the eval viewer with `generate_review.py` (not custom HTML) so that the human can look at examples. Do this before you revise the skill yourself. **GENERATE THE EVAL VIEWER *BEFORE* you evaluate the outputs yourself.** The human must see them as soon as possible.
- Feedback works differently. There is no running server, so the "Submit All Reviews" button of the viewer downloads `feedback.json` as a file. Read it from that location (you possibly must request access first).
- Packaging works. `package_skill.py` needs only Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) works in Cowork, because it uses `claude -p` through a subprocess, not a browser. But do it only after the skill is complete and the user agrees that it is in good condition.
- **Update an existing skill**: The user can ask you to update an existing skill, not to create a new one. Follow the update guidance in the [Without subagents](#without-subagents-claudeai-and-other-harnesses) section above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you start the applicable subagent.

- `agents/grader.md` — How to evaluate assertions against outputs.
- `agents/comparator.md` — How to do a blind A/B comparison between two outputs.
- `agents/analyzer.md` — How to analyze why one version won against a different version.

The references/ directory has more documentation:

- `references/schemas.md` — JSON structures for evals.json, grading.json, and other files.

---

## Core loop summary

1. Find what the skill is about.
2. Write a draft of the skill, or edit it.
3. Run an agent with access to the skill on the test prompts.
4. With the user, evaluate the outputs:
   - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them.
   - Run quantitative evals.
5. Do the loop again until you and the user are satisfied.
6. Package the final skill and give it to the user.

If your harness has a todo list, add these steps to it, so that you do not forget them. In Cowork, add specifically "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" to the todo list.
