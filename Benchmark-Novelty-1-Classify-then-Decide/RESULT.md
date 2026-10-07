# Novelty 1: Classify-then-Decide (category-first): RESULT

**Verdict: negative result. The novelty did not work. Drop it and try another idea.**

## The idea

Before answering, Qwen1.5-7B-Chat first writes `EVIDENCE_STATE:` (CLEAR, AMBIGUOUS, CONTRADICTORY, MISSING_INFORMATION, FALSE_PREMISE, GRANULARITY_MISMATCH, EPISTEMIC_MISMATCH), then `FINAL:`. If the state is not CLEAR, the answer is the matching `REFUSE_*` code. If it is CLEAR, the text after `FINAL:` is the answer. One model call per example. Prompts and extraction are in `src/conditions.py`.

## The three conditions

All use the same model (Qwen1.5-7B-Chat, 4-bit, temperature 1.0, top_p 1.0, seed 0) and the same examples. Only the instruction changes.

| Condition | What Qwen is told | Purpose |
|---|---|---|
| Baseline | The original RefusalBench prompt: answer, or reply with a `REFUSE_*` code | The paper's method |
| Format-only control | Baseline plus one rule: end with a `FINAL:` line | Separates "tidier output" from "better reasoning" |
| Novelty (Classify-then-Decide) | Write `EVIDENCE_STATE:` first, then `FINAL:` | Our idea |

The comparison that matters is **Novelty vs Format-only control**.

## Data

- 776 examples common to all three runs (the stratified 800 minus 24 baseline examples that failed with CUDA out-of-memory), covering 99 source questions.
- 517 refusal-required and 259 answerable.
- Scored by code parsing only (clean `REFUSE_*` code). No judge calls were needed.
- Baseline and format-only numbers are **lower bounds**: free-text refusals with no code would need the judge. The novelty's state is read directly from the text, so its number is exact.

## Results

| Condition | Refusal detected (clean code) | Correct refusal category | False refusal on answerable |
|---|---|---|---|
| Baseline | 43.3% | 6.8% | 15.4% |
| Format-only control | 35.8% | 3.3% | 7.7% |
| **Novelty** | **1.9%** | **0.0%** | 0.4% |

Paired bootstrap over source questions (2,000 resamples, 95% CI), correct-category rate:

| Comparison | Difference | 95% CI |
|---|---|---|
| Novelty - Format-only | -3.3 points | [-4.8, -1.9] |
| Novelty - Baseline | -6.8 points | [-9.0, -4.5] |
| Format-only - Baseline | -3.5 points | [-5.9, -1.3] |

All intervals exclude zero.

## Why it failed

Qwen wrote `EVIDENCE_STATE: CLEAR` on **762 of 800 examples (95%)**, including almost every example that should be refused (for example 89 of 93 false-premise and 68 of 69 ambiguous cases). It then answered normally. Only 7 replies (0.9%) named a valid non-CLEAR state, and another 31 had a missing or malformed state (`C`, `CLARITY`, `_CLEAR`). Even if every non-CLEAR reply were a perfect refusal, the ceiling would be 38 of 800, about 5%.

The format-only control also did not beat the baseline, so formatting alone does not explain the failure. The diagnosis step is what made Qwen commit to "the evidence is fine".

This matches the "what could invalidate the novelty" conditions in Obsidian note 9.

## Caveats

- The 800 are a stratified subset, not the full 1,600.
- Judging was incomplete (Gemini free tier: 500 requests per day), so answer accuracy for this condition is not available. The refusal results above do not need it.
- The prompts were not piloted on the real Qwen before the runs (see `PROGRESS.md`, E12b).
- Single seed, single model.

## Next step

Try a different novelty. Recommended: the probability-based answer/refuse threshold (note 9, section 16). It reads Qwen's token probabilities instead of trusting what Qwen writes, so it cannot collapse to "always CLEAR". Keep this negative result, with the format-only control, for the report and the defense.

## Source data

`refusalbench_results.zip` in this folder: generated replies for the Classify-then-Decide and format-only runs (an earlier partial snapshot). The complete 800-example runs are in `Benchmark-Reproduction-Data/refusalbench_results.zip`.
