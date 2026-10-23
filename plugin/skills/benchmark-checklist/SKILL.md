---
name: benchmark-checklist
description: "Check a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work ran) before you report it or act on it. Use when you run a benchmark or report a speedup or regression that you measured."
disable-model-invocation: true
---

# Benchmark checklist

Use this checklist when you produce a performance number. Examples are the before and after of a PR, a regression claim, a hillclimb harness, or a choice of library or config. Answer each question with evidence from a run. Do not guess from the code.

If the user asks for a quick ballpark, one run is sufficient. You must still check questions 4 and 7, and say that it is one run. Do not do the other questions unless that run looks wrong. A choice between options is never a ballpark.

## Before you run anything

- Write down the claim that you expect to make, in the words that you will ship ("export is 30% faster at p50 on the 60k-row dataset"). The questions test that sentence.
- Read the measurement script. Write down what it times, what it counts, and what it ignores.
- Check the load average with `uptime` and the core count with `nproc`. If the machine is busy, find out what runs on it. If you cannot stop it, interleave the two sides so that both sides get the same noise. Say this in the report.

## The questions

1. **Why not double?** Name the limiter. Do these steps:
   - Profile in a run that you do not report. Profilers and tracers make the work slower.
   - Use CPU per process (`top`, `pidstat`), a runtime profiler (`node --cpu-prof`, `py-spy`, `perf`), I/O wait, and syscall counts (`strace -c` on Linux).
   - Map the hot spot to the source.
   - Monitor the load generator too. If it saturates first, you measured the load generator.
   - If a change did not move the number, the limiter tells you why. Find the limiter before you say that the change has no use.
2. **Was it tuned?** Run each side as production runs it. This includes release builds, production flags and env, batch and transaction settings, connection pools, caches as warm or cold as in production, and the same versions and data. If one side runs on defaults, you compared configurations, not implementations.
   - A limiter that is a setting (a commit per row, a debug build, a missing index) means that the side is not tuned. Tune it and measure again before you select a winner.
   - If you cannot tune it, do not select a winner from that run.
   - If the user must choose an option to adopt, do not make the claim narrower to "the code as it ships today". This does not fix the problem, because the user adopts the option, not the current settings.
3. **Did it go past a limit?** Do the arithmetic:
   - Compare bytes per second with the disk and network bandwidth.
   - Compare operations per second, multiplied by the cost per operation, with your cores.
   - Compare the time saved with the time of the changed part. If you remove a part that takes 10% of the run, the run can be at most approximately 11% faster.
   - A result past a limit measured something other than the work, for example a cache, a no-op, or a bug.
4. **Did it error?** Count failures and responses that are not success. Make sure that the outputs are correct, not only present. Rejections are frequently fast. Timeouts and retries are slow. If the script does not count errors, add the count.
5. **Does it reproduce?** Run each side a minimum of 5 times, in alternation (A, B, A, B, and so on). Then warmup, lazy initialization, caches, and drift do not help one side. Report the median and the range. A gap that is smaller than the run-to-run variation is no measurable difference. If the result is close, use a rank-sum test or the statistics of the harness.
6. **Is it important?** For each micro result, also measure the end-to-end path that a user waits on. Use realistic data sizes and concurrency. Report the micro result as a percentage of the whole. If a helper takes 1% of a request, the request can be at most 1% faster, however fast the helper becomes.
7. **Did the work occur?** Make sure that the work ran inside the timed region: the request got to the server, the rows were written, the bytes were read, and the code used the result. Lazy code and timeouts give numbers for work that did not occur. Examples of lazy code are generators that nothing iterates, promises that nothing awaits, and results that the JIT can discard.

## Report

- Start with the verdict: faster, slower, no measurable difference, or inconclusive.
- Give the number with its unit, the run count, the range, and the limiter. For example: "p50 41 ms → 33 ms, median of 7 runs per side, range 32 to 35 ms after, bound by JSON parsing on one core."
- The verdict is inconclusive in these conditions. Name the gap.
  - You claim a difference, but you cannot name the limiter.
  - One side ran without tuning.
  - You could not check questions 4 and 7.
- Put only one primary number in a PR body, as the **Opening a PR** playbook says. Put the runs, the range, and the limiter evidence in a linked artifact or notes file.

## Other perf material

- Check the baseline of the **Perf issue** playbook with this checklist before the playbook plans from it. Check each number after that too.
- Check the harness of the **Hillclimb** playbook before you freeze it. The frozen harness then prints error and work counts. Thus each keep-or-revert decision checks questions 4 and 7 automatically.
