# Novelty 1: Classify-then-Decide (category-first): ARCHIVED, negative result

Read **`RESULT.md`** first. Short version: Qwen1.5-7B-Chat writes `EVIDENCE_STATE: CLEAR` on 95% of examples, so it almost never refuses; correct-category rate fell from 6.8% (baseline) to 0.0%.

## What is in this folder

| Path | What it is |
|---|---|
| `RESULT.md` | The verdict, the three-condition table, the bootstrap intervals, why it failed |
| `code/conditions.py` | The two prompts (format-only control, category-first) and the reply extraction. Loaded by `scripts/run_all.py` through `experiment_dir` in the config |
| `code/compare.py`, `code/compare_conditions.py` | Paired cluster bootstrap over source questions, baseline vs format-only vs category-first |
| `code/selftest_conditions.py` | Tests for the prompts and the extraction |
| `configs/` | One config per condition (same 800 stratified examples in `data/novelty_sample_ids.json`) |
| `colab_novelty1.ipynb` | The notebook you upload to Colab to repeat the runs |
| `refusalbench_results.zip` | Earlier partial snapshot of the generated replies |

## How to repeat it on Colab (T4)

1. Upload `colab_novelty1.ipynb`, set **Runtime > T4 GPU**, add the `GEMINI_API_KEY` secret (optional, for the judge).
2. **Runtime > Run all.** Resumable: if Colab disconnects, run all again.
3. Needs the finished baseline run in `MyDrive/refusalbench-results/qwen15_7b_baseline` for the last comparison cell.

## Run the tests locally

```
python Benchmark-Novelty-1-Classify-then-Decide/code/selftest_conditions.py
```
