"""Tests for compare_to_baseline.py (no network, no GPU, no model). Run:
  python Benchmark-Novelty-2-Confidence-Threshold/code/selftest_compare.py
"""

import csv
import json
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import compare_to_baseline as C  # noqa: E402

rng = np.random.default_rng(3)
N_SRC, PER = 40, 10
n = N_SRC * PER
source = np.repeat([f"q{i}" for i in range(N_SRC)], PER)
y = np.tile(np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1], bool), N_SRC)
utype = np.tile(np.array(["A", "B"]), n // 2)
ids = [f"id{i}" for i in range(n)]
good = np.where(y, 2.0, -2.0) + rng.normal(0, 1.5, n)  # a scorer with real signal
pred_good = good > 0


def write_scores(d, s3_pred):
    with open(os.path.join(d, "scores.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "source", "uncertainty_type", "intensity", "should_refuse", "fold", "s1", "s2", "s3_heldout",
                    "s1_default", "s1_tuned", "s2_tuned", "s3_tuned"])
        for i in range(n):
            w.writerow([ids[i], source[i], utype[i], "HIGH", int(y[i]), 0, f"{good[i]:.4f}", f"{good[i]:.4f}",
                        f"{good[i]:.4f}", int(pred_good[i]), int(pred_good[i]), int(pred_good[i]), int(s3_pred[i])])


def write_baseline(d, refuse, judged_ids=None, code="REFUSE_OTHER", empty_for=()):
    with open(os.path.join(d, "target_outputs.jsonl"), "w", encoding="utf-8") as f:
        for i in ids:
            f.write(json.dumps({"example_id": i}) + "\n")
    with open(os.path.join(d, "judged_outputs.jsonl"), "w", encoding="utf-8") as f:
        for k, i in enumerate(ids):
            if judged_ids is not None and i not in judged_ids:
                continue
            cls = "EMPTY" if k in empty_for else (code if refuse[k] else "answer_attempt")
            f.write(json.dumps({"example_id": i, "classification": cls}) + "\n")


with tempfile.TemporaryDirectory() as tmp:
    nov, base = os.path.join(tmp, "nov"), os.path.join(tmp, "base")
    os.makedirs(nov), os.makedirs(base)
    write_scores(nov, pred_good)

    def run(refuse, **kw):
        write_baseline(base, refuse, **kw)
        dec, n_gen, n_judged, n_empty = C.load_baseline(base)
        d = C.build_arrays(C.load_scores(nov), dec, kw.get("subset"))
        return d, C.bootstrap(d, 300, 0), (n_gen, n_judged, n_empty)

    # --- a coin-flip baseline: the good rules must be judged BETTER
    d, res, _ = run(rng.random(n) < 0.5)
    assert d["y"].shape[0] == n and res["n_sources"] == N_SRC
    for k in ("s1_tuned", "s2_tuned", "s3_tuned", "s1_default"):
        assert C.judgement(res["rules"][k]["diff"]["bal_acc"]) == "BETTER", k

    # --- a baseline identical to the rules: no difference at all
    same = pred_good.copy()
    d, res, _ = run(same)
    dd = res["rules"]["s3_tuned"]["diff"]["bal_acc"]
    assert dd["value"] == 0.0 and dd["ci"] == [0.0, 0.0] and C.judgement(dd) == "NO CLEAR DIFFERENCE"

    # --- an oracle baseline: the rules must be judged WORSE
    d, res, _ = run(y.copy())
    assert C.judgement(res["rules"]["s3_tuned"]["diff"]["bal_acc"]) == "WORSE"
    assert res["rules"]["baseline"]["bal_acc"]["value"] == 1.0

    # --- how the judge's labels are read: any REFUSE_* code refuses, EMPTY and answer_attempt answer
    refuse = np.zeros(n, bool)
    refuse[:5] = True
    dec, _, _, n_empty = (lambda: (write_baseline(base, refuse, empty_for={0, 1}), C.load_baseline(base))[1])()
    assert dec[ids[0]] is False and dec[ids[1]] is False and n_empty == 2, "EMPTY must count as answering"
    assert dec[ids[2]] is True and dec[ids[4]] is True and dec[ids[5]] is False
    write_baseline(base, refuse, code="REFUSE_CONTRADICTORY_CONTEXT")
    assert C.load_baseline(base)[0][ids[2]] is True

    # --- a mistyped refusal code still counts as a refusal
    write_baseline(base, np.zeros(n, bool))
    rows_ = [json.loads(l) for l in open(os.path.join(base, "judged_outputs.jsonl"), encoding="utf-8")]
    rows_[0]["classification"] = "REFUSE_INFO_MISSING_IN CONTEXT"
    with open(os.path.join(base, "judged_outputs.jsonl"), "w", encoding="utf-8") as f:
        for r in rows_:
            f.write(json.dumps(r) + chr(10))
    assert C.load_baseline(base)[0][ids[0]] is True and C.load_baseline(base)[0][ids[1]] is False

    # --- only part of the baseline is judged: compare on the overlap, and warn if it is not representative
    part = set(ids[: n // 2])
    d, res, (n_gen, n_judged, _) = run(rng.random(n) < 0.5, judged_ids=part)
    assert res["n"] == n // 2 and n_gen == n and n_judged == n // 2
    rows = C.load_scores(nov)
    assert C.coverage_warning(rows, set(ids)) == ""  # everything judged: nothing to warn about
    biased = {r["id"] for r in rows if r["uncertainty_type"] == "A" and r["should_refuse"] == "1"}
    assert "NOT a representative" in C.coverage_warning(rows, biased)

    # --- subset restriction
    sub = set(ids[:100])
    write_baseline(base, rng.random(n) < 0.5)
    d = C.build_arrays(rows, C.load_baseline(base)[0], sub)
    assert len(d["ids"]) == 100

    # --- report and (when matplotlib exists) the figure
    write_baseline(base, rng.random(n) < 0.5)
    dec, n_gen, n_judged, n_empty = C.load_baseline(base)
    d = C.build_arrays(rows, dec)
    res = C.bootstrap(d, 200, 0)
    text = C.render(res, {"baseline_dir": base, "n_generated": n_gen, "n_judged": n_judged, "n_empty": n_empty}, "")
    assert "BETTER" in text and "Uses labels?" in text and "no labels used" in text and "WARNING" not in text
    assert "WARNING" in C.render(res, {"baseline_dir": base, "n_generated": 1, "n_judged": 1, "n_empty": 0}, "oops")
    try:
        import matplotlib  # noqa: F401

        C.plot(os.path.join(tmp, "p.png"), d, res)
        assert os.path.getsize(os.path.join(tmp, "p.png")) > 0
        print("  figure written")
    except ImportError:
        print("  (matplotlib not installed here: figure not tested)")

print("selftest_compare: all assertions passed")
