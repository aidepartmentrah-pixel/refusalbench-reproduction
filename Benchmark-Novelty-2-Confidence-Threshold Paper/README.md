# Paper draft: "Reading, Not Asking" (IEEE conference format, 6 pages)

| File | What it is |
|---|---|
| `main.tex` | The paper (IEEEtran conference class). Main document for Overleaf |
| `references.bib` | 20 references, each verified against arXiv, Crossref or the ACL Anthology |
| `figures/` | The figures used (`baseline_vs_scorers.png`, `s1_distribution.png`) plus an unused spare (`tradeoff.png`) |
| `Novelty2_paper_draft.pdf` | The compiled draft, to read or to share |
| `Novelty2_paper_overleaf.zip` | Everything Overleaf needs (`main.tex`, `references.bib`, `figures/`) |

## Put it on Overleaf

1. Overleaf > **New Project > Upload Project** > pick `Novelty2_paper_overleaf.zip`.
2. Menu > Compiler: **pdfLaTeX**. Main document: `main.tex`. Click **Recompile**. (`IEEEtran` is built into Overleaf; no template download.)
3. Share the project with your doctor with **Share > Add people** (editor access). Red text in the PDF is an open to-do.

## Open to-dos (listed here; the reminder for the numbers is also a comment at the top of `main.tex`)

1. ~~Email address~~ done: name, affiliation and email are in the title block. (An earlier Overleaf copy showed the email three times in the text, because the two red to-do markers in the body were replaced by it; this version has no body markers. Replace your Overleaf copy with the new zip.)
2. **Update the numbers when the baseline is fully graded** (770 of 1,560 replies are graded now). Re-run `Benchmark-Novelty-2-Confidence-Threshold/code/compare_to_baseline.py` and replace the numbers in:
   - the Abstract (balanced accuracy 0.69, 0.72, difference +0.03 [-0.01, +0.07]),
   - Section IV, Table I (baseline) and the sentences under it,
   - Section VI-B, Table V, Figure 3 (`figures/baseline_vs_scorers.png`) and the paragraph, including the verdict wording,
   - Section VI-C, Table VI (baseline column) and Section VII (class-level baseline numbers),
   - Limitations (iii).
   If the new interval for the probe is entirely above 0, the title, abstract and conclusion can say the probe "modestly improves" detection; if it still includes 0, they stay as they are.
3. **Judge validation:** the 30-reply hand check is not done (Limitations ii). Fill `handcheck_sheet.csv` in the baseline run and add the agreement rate.
4. **References:** all 20 were checked against their sources. Two things to know: the RefusalBench proceedings title is written generically ("Proc. EACL, Long Papers", ACL Anthology ID 2026.eacl-long.321), so replace it with the exact proceedings title from the Anthology page; and the Qwen1.5 entry is the project blog post.
5. **Length:** 6 pages including references (limit 5 to 7).

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

## Changes made after the GPT review

Accepted (all 16 points; the one about the probe is applied with different wording, see below): judge-dependence caveat after Table V; Table VI recomputed on the same 770 examples for every rule; "one forward pass" corrected to "one pass per prompt"; AUROC intervals added to Table IV; the BETTER / WORSE / NO CLEAR DIFFERENCE rule defined before Table V; "knowledge is present" changed to "information predictive of refusal is present"; "failure is in what the model writes" replaced by a statement that does not claim a cause; the S1 default threshold no longer described as "what the model does on its own"; S3 labelled as a diagnostic, not an equal-training comparison; "improvement" for the probe changed to "no clear improvement"; "far above chance" softened; MRR claim for the easy classes qualified by FRR; the answer-accuracy comparison reworded; the multiplicity caveat attached to the S1-default result; "lying on the curves" reworded; related work extended with three verified references (Yin et al., Zhang et al., Asai et al.).

Added by us after reading the review: how the bootstrap is computed (held-out predictions are resampled, the fitting is not repeated) and that a unit test checks the no-leakage property.

Not applied: GPT's suggested phrase "upper-bound-style readout" for the probe, because a supervised probe is not an upper bound; we call it a diagnostic. Not done yet (needs you): the 30-reply judge hand check, and the final numbers when the baseline is fully graded.

## Round 3 (second GPT review)

Applied: Fig. 1 label now says "one forward pass per prompt"; "anchors it on clear" replaced by a non-causal wording; the Conclusion and the Discussion no longer say the probe is "slightly better" or that the scores are "more separable" than the generated decisions (they now say a small positive point estimate with no clear advantage, and that the scores contain predictive information); the related-work contrast is limited to the approaches that fine-tune; the Table IV caption says only AUROC has intervals; the bootstrap count and seed (2,000, seed 0) are stated; contribution 3 names the gap between decodability and deployable gain.

Found by that review and fixed in the code: Table I and Table V disagreed (baseline BA 0.690 vs 0.688) because the judge mistyped two refusal codes (for example `REFUSE_INFO_MISSING_IN CONTEXT`). `src/metrics.py` now maps any mistyped REFUSE code to the closest valid code (the stored judgements are untouched), and the comparison script uses the same function. Corrected numbers: baseline BA 0.690 [0.656, 0.724], detection F1 0.668; probe difference +0.028 [-0.014, +0.065]; S1 default -0.031 [-0.057, -0.005]. Verdicts are unchanged. The second review also flagged stray emails in the text; that was an older PDF, already fixed in the zip from commit 358d9bb.

## Round 4 (third GPT review): final wording polish

"The fair comparison" became "For comparison, we score ..." (the caveats follow right after, so "fair" invited an attack); "The probe is best" became "The probe has the highest AUROC" (no S3-versus-S2 test is shown); the judge sentence now says "in an LLM-as-a-judge setup [20]" because reference [20] is the LLM-as-a-judge paper, not Gemini documentation. After these, further prose rounds have little value: the open items are the full baseline grading, the 30-reply judge check, and the defense.
