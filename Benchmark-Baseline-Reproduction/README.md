# Baseline: RefusalBench-NQ with Qwen1.5-7B-Chat

Reproduce the paper's selective-refusal evaluation for one model (Qwen1.5-7B-Chat, 4-bit on a free Colab T4), on all 1,600 RefusalBench-NQ examples. Scoring is parse-first: a clean `REFUSE_*` code is scored by code, everything else goes to the Gemini judge.

## What is in this folder

| File | What it is |
|---|---|
| `colab_baseline.ipynb` | The notebook you upload to Colab. Runs everything with **Runtime > Run all** |
| `configs/qwen15_7b_baseline.yaml` | Model, precision, sampling settings, judge settings, stages (10, 100, all) |
| `qwen15_7b_baseline.zip` | Downloaded result of the first Colab run (1,560 of 1,600 generated, 40 hit CUDA out-of-memory) |
| `refusalbench_results.zip` | Local run on the Windows machine: partial judging only, **not a valid result** (judge quota stopped it) |
| `RESULT.md` | Status and what the data says (updated as the baseline is completed) |

The shared code is at the top of the repo (`src/`, `scripts/run_all.py`), because every experiment uses it.

## How to run it on Google Colab (T4)

1. Open Colab, **File > Upload notebook**, pick `colab_baseline.ipynb`.
2. **Runtime > Change runtime type > T4 GPU**.
3. Optional, for the judge: key icon on the left > add a secret named `GEMINI_API_KEY` and switch "Notebook access" on. The free tier allows **500 judge requests per day per model**, so judging can take more than one day. If the repo you clone is private, also add a `GITHUB_TOKEN` secret.
4. **Runtime > Run all.** Keep the tab open and the computer awake.
5. If Colab disconnects, click **Run all** again. It resumes and never repeats finished work.

Results are written to `MyDrive/refusalbench-results/qwen15_7b_baseline/` (`target_outputs.jsonl`, `judged_outputs.jsonl`, `metrics.json`, `reproduction_report.md`, `handcheck_sheet.csv`). The last cell also downloads a zip. Put that zip in this folder.

Command line equivalent (what the notebook runs):

```
python scripts/run_all.py --config Benchmark-Baseline-Reproduction/configs/qwen15_7b_baseline.yaml --out /content/drive/MyDrive/refusalbench-results
```

## Known open items

- 40 examples failed with CUDA out-of-memory in the first run. The pushed fix retries them one by one: just run the notebook again.
- Judging is incomplete (free-tier quota). Metrics from a partial judge run are marked INCOMPLETE and must not be compared with the paper.
- Paper targets for Qwen-7B on NQ: answer accuracy 56.1%, refusal accuracy about 5% (read from a small plot).
