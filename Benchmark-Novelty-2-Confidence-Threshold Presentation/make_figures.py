"""Draw the results chart for the defense slides at projector size (text of 18 pt or more).

Reads only files that are already in the repository:
  Benchmark-Novelty-2-Confidence-Threshold/results/scores.csv       (scores of S1, S2, S3 for all 1,600 examples)
  Benchmark-Baseline-Reproduction/qwen15_7b_baseline/judged_outputs.jsonl   (the judged baseline replies, 770 so far)
Writes assets/img/tradeoff-baseline.png.   Run:  python make_figures.py
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

# the course palette (assets/lu.css)
INK, INK2, PAPER = "#14171C", "#3E4650", "#F7F5F2"   # PAPER = the course figure frame colour (--lu-paper-2)
RED, GREEN, BLUE = "#96122B", "#0B5E3B", "#2447A0"
GRID = "#DDD8D0"

rows = list(csv.DictReader(open(os.path.join(ROOT, "Benchmark-Novelty-2-Confidence-Threshold/results/scores.csv"), encoding="utf-8")))
base = {}
for line in open(os.path.join(ROOT, "Benchmark-Baseline-Reproduction/qwen15_7b_baseline/judged_outputs.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    base[r["example_id"]] = normalize_classification(r["classification"]) in REFUSAL_CODES
rows = [r for r in rows if r["id"] in base]          # the same examples for every curve and for the baseline point
y = np.array([r["should_refuse"] == "1" for r in rows])
scores = {"S1 refusal probability": np.array([float(r["s1"]) for r in rows]),
          "S2 yes/no probability": np.array([float(r["s2"]) for r in rows]),
          "S3 hidden-state probe": np.array([float(r["s3_heldout"]) for r in rows])}
colors = {"S1 refusal probability": BLUE, "S2 yes/no probability": GREEN, "S3 hidden-state probe": RED}
pred = np.array([base[r["id"]] for r in rows])
b_frr, b_mrr = float(pred[~y].mean()), float((~pred[y]).mean())
print(f"{len(rows)} examples; baseline FRR {b_frr:.3f} MRR {b_mrr:.3f}")

plt.rcParams.update({"font.size": 18, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2})
fig, ax = plt.subplots(figsize=(8.4, 6.2), dpi=100, facecolor=PAPER)
ax.set_facecolor(PAPER)
for name, s in scores.items():
    cand = np.unique(s)
    cand = np.concatenate([[cand[0] - 1], cand[:: max(1, len(cand) // 250)], [cand[-1] + 1]])
    ax.plot([(s[~y] > t).mean() for t in cand], [(s[y] <= t).mean() for t in cand], color=colors[name], lw=3.2, label=name)
ax.plot(b_frr, b_mrr, "D", color=INK, ms=15, mec=PAPER, mew=2.5, label="Baseline (judged replies)", zorder=5)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("Answerable questions refused (lower is better)", fontsize=18)
ax.set_ylabel("Needed refusals missed (lower is better)", fontsize=18)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, color=GRID, lw=1)
ax.set_axisbelow(True)
leg = ax.legend(loc="upper right", frameon=False, fontsize=17, handlelength=1.6, labelcolor=INK)
fig.tight_layout()
out = os.path.join(HERE, "assets/img/tradeoff-baseline.png")
fig.savefig(out, facecolor=PAPER)
print("written", out)
