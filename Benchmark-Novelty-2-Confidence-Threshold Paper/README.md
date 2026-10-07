# Paper draft: "Reading, Not Asking" (IEEE conference format, 5 pages)

| File | What it is |
|---|---|
| `main.tex` | The paper (IEEEtran conference class). Main document for Overleaf |
| `references.bib` | 17 references, each verified against arXiv, Crossref or the ACL Anthology |
| `figures/` | The figures used (`baseline_vs_scorers.png`, `s1_distribution.png`) plus an unused spare (`tradeoff.png`) |
| `Novelty2_paper_draft.pdf` | The compiled draft, to read or to share |
| `Novelty2_paper_overleaf.zip` | Everything Overleaf needs (`main.tex`, `references.bib`, `figures/`) |

## Put it on Overleaf

1. Overleaf > **New Project > Upload Project** > pick `Novelty2_paper_overleaf.zip`.
2. Menu > Compiler: **pdfLaTeX**. Main document: `main.tex`. Click **Recompile**. (`IEEEtran` is built into Overleaf; no template download.)
3. Share the project with your doctor with **Share > Add people** (editor access). Red text in the PDF is an open to-do.

## Open to-dos (all marked in red in the PDF or listed here)

1. **Authors, affiliation, email** (title block).
2. **Update the numbers when the baseline is fully graded** (770 of 1,560 replies are graded now). Re-run `Benchmark-Novelty-2-Confidence-Threshold/code/compare_to_baseline.py` and replace the numbers in:
   - the Abstract (balanced accuracy 0.69, 0.72, difference +0.03 [-0.01, +0.07]),
   - Section IV, Table I (baseline) and the sentences under it,
   - Section VI-B, Table V, Figure 3 (`figures/baseline_vs_scorers.png`) and the paragraph, including the verdict wording,
   - Section VI-C, Table VI (baseline column) and Section VII (class-level baseline numbers),
   - Limitations (iii).
   If the new interval for the probe is entirely above 0, the title, abstract and conclusion can say the probe "modestly improves" detection; if it still includes 0, they stay as they are.
3. **Judge validation:** the 30-reply hand check is not done (Limitations ii). Fill `handcheck_sheet.csv` in the baseline run and add the agreement rate.
4. **References:** all 17 were checked against their sources. Two things to know: the RefusalBench proceedings title is written generically ("Proc. EACL, Long Papers", ACL Anthology ID 2026.eacl-long.321), so replace it with the exact proceedings title from the Anthology page; and the Qwen1.5 entry is the project blog post.
5. **Length:** 5 pages including references (limit 5 to 7).

## Where every number comes from

| In the paper | Source file |
|---|---|
| Baseline (Table I) | `Benchmark-Baseline-Reproduction/qwen15_7b_baseline/reproduction_report.md` (day-1 zip) |
| Extension 1 (Tables II, III) | `Benchmark-Novelty-1-Classify-then-Decide/RESULT.md` and the 800-example run in `Benchmark-Baseline-Reproduction/refusalbench_results.zip` |
| Extension 2 (Table IV, Fig. 2) | `Benchmark-Novelty-2-Confidence-Threshold/results/RESULT_AUTO.md`, `metrics.json`, `scores.csv` |
| Baseline comparison (Table V, Fig. 3) | `Benchmark-Novelty-2-Confidence-Threshold/results/comparison_all/COMPARISON.md` |
| Per-class table (Table VI) | computed from `results/scores.csv` and the baseline's `judged_outputs.jsonl` |

## Rebuild the PDF locally

Overleaf is the simplest. Any LaTeX install works: `pdflatex main`, `bibtex main`, `pdflatex main` twice.
