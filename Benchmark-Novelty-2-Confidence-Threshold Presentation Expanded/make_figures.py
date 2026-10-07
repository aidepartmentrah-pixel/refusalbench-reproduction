"""Draw the trade-off chart for the expanded slides (white background, shown at 1:1 so text stays 18 px or more).

Reads only files that are already in the repository:
  Benchmark-Novelty-2-Confidence-Threshold/results/scores.csv                  (S1, S2, S3 scores, all 1,600 examples)
  Benchmark-Baseline-Reproduction/qwen15_7b_baseline/judged_outputs.jsonl      (the judged baseline replies, 770 so far)
Writes assets/img/tradeoff.png.   Run:  python make_figures.py   (needs numpy and matplotlib)
"""

import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.metrics import normalize_classification
from src.schema_adapter import REFUSAL_CODES

INK, MUTED, GRID = "#14213d", "#5b6577", "#e6e9ef"
BLUE, TEAL, RUST = "#2f6fde", "#0f9d8a", "#b5541a"

rows = list(csv.DictReader(open(os.path.join(ROOT, "Benchmark-Novelty-2-Confidence-Threshold/results/scores.csv"), encoding="utf-8")))
base = {}
for line in open(os.path.join(ROOT, "Benchmark-Baseline-Reproduction/qwen15_7b_baseline/judged_outputs.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    base[r["example_id"]] = normalize_classification(r["classification"]) in REFUSAL_CODES
rows = [r for r in rows if r["id"] in base]  # the same examples for every curve and for the baseline point
y = np.array([r["should_refuse"] == "1" for r in rows])
scores = {"S1 refusal probability": (np.array([float(r["s1"]) for r in rows]), BLUE),
          "S2 yes/no probability": (np.array([float(r["s2"]) for r in rows]), TEAL),
          "S3 hidden-state probe": (np.array([float(r["s3_heldout"]) for r in rows]), RUST)}
pred = np.array([base[r["id"]] for r in rows])
b_frr, b_mrr = float(pred[~y].mean()), float((~pred[y]).mean())
print(f"{len(rows)} examples; baseline FRR {b_frr:.3f} MRR {b_mrr:.3f}")

plt.rcParams.update({"font.size": 15, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=100, facecolor="white")
for name, (s, color) in scores.items():
    cand = np.unique(s)
    cand = np.concatenate([[cand[0] - 1], cand[:: max(1, len(cand) // 250)], [cand[-1] + 1]])
    ax.plot([(s[~y] > t).mean() for t in cand], [(s[y] <= t).mean() for t in cand], color=color, lw=3, label=name)
ax.plot(b_frr, b_mrr, "D", color=INK, ms=13, mec="white", mew=2, label="Baseline (judged replies)", zorder=5)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("Answerable questions refused", fontsize=16)
ax.set_ylabel("Needed refusals missed", fontsize=16)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, lw=1)
ax.set_axisbelow(True)
ax.legend(loc="upper right", frameon=False, fontsize=14, labelcolor=INK, handlelength=1.5)
fig.tight_layout()
out = os.path.join(HERE, "assets", "img", "tradeoff.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, facecolor="white")
print("written", out)
