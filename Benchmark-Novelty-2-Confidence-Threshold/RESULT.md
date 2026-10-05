# Novelty 2: confidence-threshold refusal gate: RESULT

**Verdict (the rule fixed before the run): SIGNAL BUT NO GAIN FROM THE THRESHOLD.**
Qwen's refusal probability carries real information (S1 AUROC 0.73), but tuning a threshold on it does not significantly beat Qwen's default behavior in balanced accuracy. **Against the judged baseline (first 770 graded replies), no variant is clearly better: the best, the supervised hidden-state probe (S3), is +0.030 [-0.012, +0.067] in balanced accuracy, which includes zero, and the label-free S1 default is slightly worse.** We cannot claim that Novelty 2 beats the baseline. The comparison will be repeated when the baseline is fully judged (see "Is it better than the baseline?").

Full auto-generated numbers: `results/RESULT_AUTO.md`. Figures: `results/tradeoff.png`, `results/s1_distribution.png`. Raw download: `novelty2_results.zip`.

## What was run

Qwen1.5-7B-Chat (4-bit, T4), one forward pass per example, no generation, no judge, all 1,600 RefusalBench-NQ examples (100 source questions). Thresholds and the probe were cross-fitted over source questions (5 folds), and intervals are 95% cluster bootstrap over source questions. About 0.3 seconds per example once the model was loaded. S1 ran in `variants` mode (the pre-flight check passed).

## Results (all 1,600 examples)

| Scorer | AUROC [95% CI] | What it is |
|---|---|---|
| S1 refuse-code probability (the novelty) | 0.726 [0.699, 0.752] | Probability that Qwen opens with a refusal code, baseline prompt |
| S2 yes/no sufficiency probability | 0.751 [0.723, 0.777] | Probability of No vs Yes on "can the query be answered from the context?" |
| S3 hidden-state linear probe | 0.797 [0.770, 0.825] | Supervised, trained on the benchmark's labels in the other folds |

0.5 is chance. All three are clearly above chance.

| Decision rule | False refusal | Missed refusal | Balanced accuracy | Detection F1 |
|---|---|---|---|---|
| S1 default (p > 0.5) | 0.103 | 0.590 | 0.654 [0.631, 0.674] | 0.561 |
| S1 tuned threshold | 0.256 | 0.408 | 0.668 [0.642, 0.693] | 0.688 |
| S2 tuned threshold | 0.321 | 0.329 | 0.675 [0.650, 0.701] | 0.732 |
| S3 probe (tuned) | 0.250 | 0.307 | **0.721 [0.691, 0.749]** | 0.762 |

## The two pre-registered checks

1. **Signal check: passed.** S1 AUROC lower bound 0.699 is above 0.5.
2. **Gate check: failed.** Tuned minus default balanced accuracy for S1 is +0.015, 95% interval [-0.008, +0.036], which includes zero.

Note on F1: tuned S1 beats default S1 in F1 by +0.127 (significant). We do **not** use this to rescue the verdict. The rule fixed before the run was balanced accuracy, and F1 is inflated here because two thirds of the examples are refusal-required. What the threshold really does is move along one trade-off curve: fewer missed refusals (0.59 to 0.41) at the price of more false refusals (0.10 to 0.26), with no clear net gain.

## Secondary findings

- S3 beats S1 tuned in balanced accuracy by +0.053 [+0.024, +0.081]: significant. The information is in the hidden states more than in the first-token probability.
- S2 and S1 are similar (AUROC difference -0.025 [-0.047, -0.003], a small edge to S2).
- **By type (S1 tuned):** good on Epistemic Mismatch, False Premise and Granularity Mismatch (missed refusal about 0.22 each). Poor on **Ambiguity (0.67), Contradiction (0.63) and Missing Information (0.53)**. These are the same types where the baseline fails most. False Premise has a high false-refusal cost (0.54 of the answerable False-Premise examples get refused).

## Is it better than the baseline?

**Not clearly.** This is the fair comparison, run on the same examples against the baseline replies as judged by Gemini (script `code/compare_to_baseline.py`, full report in `results/comparison_all/COMPARISON.md`). **It uses the first 770 of 1,560 baseline replies graded** (day 1 of the free judge quota; the grading order is random, and the script found the sample representative). 509 refusal-required and 261 answerable examples, 99 source questions, 95% cluster-bootstrap intervals.

| Rule | Balanced accuracy | Difference from baseline [95% CI] | Verdict | Uses labels? |
|---|---|---|---|---|
| **Baseline (judged replies)** | **0.688** [0.654, 0.722] | | | no |
| S1 default threshold | 0.658 | -0.029 [-0.056, -0.002] | **WORSE** | no |
| S1 tuned threshold | 0.671 | -0.016 [-0.045, +0.011] | no clear difference | yes |
| S2 default (No > Yes) | 0.669 | -0.018 [-0.045, +0.008] | no clear difference | no |
| S2 tuned threshold | 0.668 | -0.019 [-0.054, +0.016] | no clear difference | yes |
| **S3 hidden-state probe** | **0.718** | **+0.030 [-0.012, +0.067]** | **no clear difference** | yes |

What this means:

- **The earlier "0.64 to 0.72" was wrong.** The 0.64 came from counting only clean `REFUSE_*` codes (a lower bound). The judged baseline is **0.688**. The honest gap to the probe is about 3 points, and its interval includes zero.
- **The label-free rules (S1 and S2 at their default thresholds) do not beat the baseline.** S1 default is slightly worse. Reading Qwen's refusal probability alone is not an improvement over letting Qwen answer.
- **The probe (S3) is the only candidate.** It has the best point estimate and the lowest missed-refusal rate (0.289 against 0.460), at the price of more false refusals (0.276 against 0.165). It was trained on the benchmark's labels, which the baseline was not, so even a clear win would need that caveat.
- **In the trade-off picture** (`results/comparison_all/baseline_vs_scorers.png`) the baseline's operating point lies on the S1 and S2 curves and just above the probe's curve: the baseline is already about as good as those scorers can do, and the probe is slightly better.
- **It can still change.** Only half the baseline is graded. With all 1,560 the intervals narrow, so the probe's +0.030 could become a clear (but small) win or stay unclear. The second half of the judging (about 494 more calls) needs one more day of free quota or a second key. Then re-run:
  `python Benchmark-Novelty-2-Confidence-Threshold/code/compare_to_baseline.py --baseline-dir Benchmark-Baseline-Reproduction/qwen15_7b_baseline --out Benchmark-Novelty-2-Confidence-Threshold/results/comparison_all`

**What can be said honestly now:** a probe on Qwen's hidden state is a plausible but small improvement (about 3 points of balanced accuracy, not yet statistically clear) over the baseline's answer-or-refuse decisions; Qwen's refusal probability read through a threshold is not.

## What this means for the project story

- Novelty 1 (writing a diagnosis first): clearly worse than the baseline (negative result).
- Novelty 2 (reading Qwen's probabilities): the signal exists, but against the judged baseline a simple threshold gives no gain, and the hidden-state probe is only a small, not yet statistically clear improvement (+0.030 balanced accuracy on the first half of the graded baseline).
- Together: for a 7B model, prompting it to reason about the evidence fails, while the information about whether to refuse is already inside the model and can be read out.

## Limitations

- S1 only sees openings that start with a refusal code; free-text refusals look like answers to it.
- 4-bit model, one model, one benchmark, one seed.
- Detection only: it does not say why to refuse, and it does not measure answer correctness (no judge).
- The baseline is only half graded (770 of 1,560); the comparison will be repeated when judging is complete.

## Next step

Finish judging the baseline (about 494 Gemini calls remain: one more day of free quota, or a second key) and re-run the comparison command above. Then decide the final claim.
