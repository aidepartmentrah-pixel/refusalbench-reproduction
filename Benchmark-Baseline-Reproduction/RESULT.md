# Baseline: Qwen1.5-7B-Chat on RefusalBench-NQ: RESULT (provisional, judging half done)

**Status:** all replies are generated (1,560 of 1,600; 40 failed with CUDA out-of-memory and are excluded, 2.5%). **770 of 1,560 replies are graded** so far (day 1 of the free Gemini quota: 272 scored by code, 498 by the judge). The grading order is random (seeded), so these 770 are a random sample, not the first IDs. The automatic report still carries an INCOMPLETE banner. Numbers below are **provisional** until all 1,560 are graded.

Data: `qwen15_7b_baseline_judged_day1.zip` in this folder (unzipped locally as `qwen15_7b_baseline/`, not tracked in git). Full automatic report: inside that zip, `reproduction_report.md`.

## Provisional results (770 graded replies: 509 refusal-required, 261 answerable)

| Metric | Ours (provisional) | Paper, Qwen1.5-7B | Note |
|---|---|---|---|
| Answer accuracy | 0.690 | 0.561 (text, Section 4.3) | We are higher: different judge (Gemini, not Claude Sonnet 4), 4-bit, a different inference stack |
| Refusal accuracy (exact category) | 0.114 | about 0.05 (read from a small plot) | Low in both: Qwen-7B almost never names the right reason |
| False refusal rate | 0.165 | not extracted | |
| Missed refusal rate | 0.456 | not extracted | |
| Refusal detection F1 | 0.665 | not extracted | |
| Calibrated refusal score | 0.402 | not extracted | |

Reading: the baseline reproduces the paper's qualitative finding (Qwen-7B almost never gives the correct refusal reason, refusal accuracy near the floor, and it misses many refusals) but the exact numbers differ from the paper because of the documented deviations (judge, quantization, inference stack, sampling at temperature 1.0). By type, the baseline misses most refusals for **Ambiguity (0.74) and Contradiction (0.71)**, and over-refuses **False Premise** (false refusal 0.33).

Reply format on all 1,560: 528 clean `REFUSE_*` codes (34%), 991 free text with no code (64%), 40 unknown codes, 1 with several codes. So most of the work falls to the judge.

## Still to do

- Grade the remaining **790 replies** (about 494 Gemini calls, one more day of free quota or a second key). Use `colab_baseline_judge.ipynb` (steps in `README.md`).
- Hand-check about 30 graded replies (`handcheck_sheet.csv`) to validate the substitute judge, and report the agreement rate.
- Final comparison with the paper once grading is complete.
