# Novelty 2: confidence-threshold refusal gate

Status: **code built and tested, not yet run on the real model.** The result goes into `RESULT.md` after the Colab run.

## The idea in plain words

Novelty 1 asked Qwen to *write* a diagnosis before answering, and Qwen wrote "CLEAR" 95% of the time (see `../Benchmark-Novelty-1-Classify-then-Decide/RESULT.md`). So this time we do not read what Qwen writes. We read **how likely Qwen is to start a refusal**, and turn that probability into an answer-or-refuse decision with a threshold.

- No text is generated. One forward pass per example, so it is fast and the Gemini judge is not needed.
- It targets **refusal detection** (should the model answer or refuse?), the skill Qwen actually has. It does not try to name *why* (the paper reports about 5% category accuracy for Qwen-7B).

## Research question and the rule for success (fixed before the run)

> Does a probability threshold on Qwen's own refusal probability separate refusal-required from answerable examples better than chance, and does a tuned threshold make better answer-or-refuse decisions than Qwen's default behavior?

`RESULT_AUTO.md` applies this rule mechanically, so nobody (including us) can bend it after seeing the numbers:

1. **Signal check:** the lower end of the 95% interval of S1's AUROC is above 0.5.
2. **Gate check:** the tuned threshold beats the default threshold (p > 0.5) in balanced accuracy, with the 95% interval of the difference above 0.

Both true = **SUPPORTED**. Only the first = **SIGNAL BUT NO GAIN FROM THE THRESHOLD**. Neither = **NOT SUPPORTED**. A negative result is still reportable.

## The three scorers

Every scorer gives one number per example, higher = refuse.

| Scorer | What is read | Role |
|---|---|---|
| **S1 refuse-code probability** | With the original baseline prompt, the probability that Qwen's reply opens with a refusal code, including the wrapped forms (`**REFUSE`, a backtick before `REFUSE`, `ANSWER: REFUSE`) which are about 30% of the baseline's coded refusals | **The novelty** (note 9, idea 5) |
| **S2 yes/no sufficiency probability** | A separate prompt: "Can the query be answered completely and faithfully from the context? Yes or No". Probability of No against Yes | Ablation (note 9, idea 2, read as a probability instead of trusting text) |
| **S3 hidden-state linear probe** | A small logistic regression on Qwen's last-token hidden state | Stronger variant (note 9, idea 6) |

## Protocol (why it is trustworthy)

- **All 1,600 examples** are scored. The 800 novelty examples are also reported as a subset, to match Novelty 1.
- **No leakage.** All 100 source questions appear in both the dev pool and the novelty 800, so a threshold or probe tuned on one half would see the same questions in the other half. Instead everything is **cross-fitted over source questions** (5 folds): an example's own source question is never in the data used to choose its threshold or fit its probe. This is unit-tested (`code/selftest_novelty2.py`).
- Thresholds are chosen on training folds only, by balanced accuracy.
- **Intervals** are 95% cluster bootstrap over the 100 source questions (examples from one question are not independent).
- **Judge-free:** every number comes from the benchmark's own labels. The Gemini quota does not matter here.

## Metrics

False refusal rate (answerable examples that were refused), missed refusal rate (refusal-required examples that were answered), balanced accuracy, detection F1, AUROC and AUPRC, plus the full false-vs-missed trade-off curve (`tradeoff.png`).

## How to run it on Google Colab (T4)

**Option A: upload the notebook.** Colab > File > Upload notebook > `colab_novelty2.ipynb` > Runtime > Change runtime type > **T4 GPU** > Runtime > **Run all**.

**Option B: paste one block.** Open a new Colab notebook, set the runtime to **T4 GPU**, paste this into a single cell and run it:

```python
# NOVELTY 2 - confidence-threshold refusal gate (Qwen1.5-7B-Chat, T4). ONE cell: Runtime > Run all.
# Safe to re-run after a disconnect: finished work is kept on Google Drive and skipped.
import os, subprocess, sys

REPO = 'aidepartmentrah-pixel/refusalbench-reproduction'   # the repo that holds this code (change if you push elsewhere)
OUT  = '/content/drive/MyDrive/refusalbench-results'        # results are saved here, on your Drive

from google.colab import drive
drive.mount('/content/drive')

token = ''
try:
    from google.colab import userdata
    token = userdata.get('GITHUB_TOKEN') or ''              # only needed if the repo is private
except Exception:
    pass
url = f'https://{token + "@" if token else ""}github.com/{REPO}.git'
if not os.path.exists('/content/refusalbench-reproduction'):
    subprocess.run(['git', 'clone', '-q', url, '/content/refusalbench-reproduction'], check=True)
os.chdir('/content/refusalbench-reproduction')
subprocess.run(['git', 'pull', '-q'], check=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements-colab.txt'], check=True)

# GPU check
print(subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv'], capture_output=True, text=True).stdout)

# The experiment: scores all 1,600 examples (about 30-60 min on a T4, an estimate), then analyses. No judge, no API key.
BASELINE = f'{OUT}/qwen15_7b_baseline'                       # optional: adds a reference line if the baseline run is there
cmd = [sys.executable, 'Benchmark-Novelty-2-Confidence-Threshold/code/run_novelty2.py', '--out', OUT]
if os.path.exists(f'{BASELINE}/target_outputs.jsonl'):
    cmd += ['--baseline-dir', BASELINE]
subprocess.run(cmd, check=True)

# Show the figures and make a zip to download (the Drive copy is already saved)
from IPython.display import Image, display
R = f'{OUT}/novelty2_confidence_threshold'
for f in ('tradeoff.png', 's1_distribution.png'):
    if os.path.exists(f'{R}/{f}'):
        display(Image(f'{R}/{f}'))
try:
    from google.colab import files
    subprocess.run(f'cd {OUT} && zip -qr /content/novelty2_results.zip novelty2_confidence_threshold -x "*/shards/*"', shell=True)
    files.download('/content/novelty2_results.zip')
except Exception as e:
    print('download skipped:', e)
```

- The code must be on GitHub first (Colab clones it). Change `REPO` in the block if you push to a different repo. If that repo is private, add a Colab secret `GITHUB_TOKEN`.
- If Colab disconnects, run the cell again: finished shards on Drive are skipped.
- Expected time: about 30 to 60 minutes on a T4 (*estimate, not measured yet*). The first lines of the log show seconds per example.
- A pre-flight check runs first. If the cached scoring disagrees with a slow reference, the run falls back to "first token only" and says so in the log and in `RESULT_AUTO.md`.

## What you get (in `MyDrive/refusalbench-results/novelty2_confidence_threshold/`)

| File | What it is |
|---|---|
| `RESULT_AUTO.md` | The auto-written report with the mechanical verdict, all tables and intervals. **Start here** |
| `tradeoff.png` | False vs missed refusal for every threshold, with default and tuned points |
| `s1_distribution.png` | S1 score for answerable vs refusal-required examples |
| `scores.csv` | Every example with its scores and decisions |
| `metrics.json` | All numbers in machine-readable form |
| `shards/` | Raw per-example scores and hidden states (resume data, not needed afterwards) |
| `run.log`, `config.json`, `config_full.yaml` | What was run |

After the run, put the downloaded zip in this folder and write the final `RESULT.md` (what it means in words).

## Limitations (stated up front)

- S1 reads only openings that start with `REFUSE`-type text. A free-text refusal ("The context does not say...") has no code and gets a low S1 score; the probe (S3) and S2 do not have this weakness.
- 4-bit quantization (a documented deviation from the paper's full precision).
- One model, one benchmark, one seed.
- It improves *when* to refuse, not *why*.
- The baseline reference line (sampled replies, clean codes only) is a lower bound because no judge counts free-text refusals.

## Files

| Path | What it is |
|---|---|
| `code/scorer.py` | The forward pass, the token probabilities, hidden states, resumable shards, a fake scorer for tests |
| `code/analysis.py` | Cross-fitting, thresholds, probe, bootstrap, plots, report |
| `code/run_novelty2.py` | The one entry point |
| `configs/novelty2.yaml` | All settings |
| `code/selftest_novelty2.py` | Unit tests: metrics checked by hand, no leakage, the success rule |
| `code/selftest_model.py` | Tests the scorer on a tiny random Qwen2 with the real tokenizer (needs torch) |
| `colab_novelty2.ipynb` | The notebook for Colab |
| `RESULT.md` | The final write-up (after the run) |

Local tests (no GPU needed): `python Benchmark-Novelty-2-Confidence-Threshold/code/selftest_novelty2.py`
