# Novelty 2: confidence-threshold refusal gate: RESULT

**Verdict (the rule fixed before the run): SIGNAL BUT NO GAIN FROM THE THRESHOLD.**
Qwen's refusal probability carries real information (S1 AUROC 0.73), but tuning a threshold on it does not significantly beat Qwen's default behavior in balanced accuracy. We **cannot claim that this beats the baseline.** The only variant that looks clearly better is the supervised hidden-state probe (S3), and the baseline comparison for it is not yet fair (see below).

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

Not provably, for three reasons:

1. **The baseline reference is a lower bound.** From the sampled baseline replies, counting only clean `REFUSE_*` codes (no judge): false refusal 0.155, missed refusal 0.569, which gives balanced accuracy about 0.638. Free-text refusals are counted as answers, so the true baseline is higher.
2. **A judged reference is higher.** The format-only control (Novelty 1, judged by Gemini on 669 of its 800 examples) had false refusal 0.088 and missed refusal 0.534, balanced accuracy about 0.689. That is above S1 tuned (0.668) and S2 tuned (0.675), and below S3 (0.721). It is a different prompt and subset, so this is context, not a paired test.
3. **S3 is supervised and the baseline is not.** The probe uses the benchmark's labels (cross-fitted, so no leakage, but it is still a trained component). A fair claim would compare it with a judged baseline on the same examples.

**What can be said honestly:** a hidden-state probe on Qwen reaches about 0.72 balanced accuracy for answer-vs-refuse detection, roughly 3 to 8 points above the available baseline references, with the caveats above. A threshold on the refusal probability alone does not help.

## What this means for the project story

- Novelty 1 (writing a diagnosis first): clearly worse than the baseline (negative result).
- Novelty 2 (reading Qwen's probabilities): the signal exists and it is usable by a probe, but a simple threshold gives no significant gain.
- Together: for a 7B model, prompting it to reason about the evidence fails, while the information about whether to refuse is already inside the model and can be read out.

## Limitations

- S1 only sees openings that start with a refusal code; free-text refusals look like answers to it.
- 4-bit model, one model, one benchmark, one seed.
- Detection only: it does not say why to refuse, and it does not measure answer correctness (no judge).
- No judged baseline on the same examples yet.

## Next step to settle "better than the baseline"

Finish judging the baseline (about 517 Gemini calls remain, roughly one day of free quota, or a second key) and compare it with S1, S2 and S3 on the same examples with a paired bootstrap.
