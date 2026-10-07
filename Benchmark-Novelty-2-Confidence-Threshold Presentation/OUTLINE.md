# Defense presentation: outline

> **Status (updated): the deck is built.** See `README.md` and `defense-slides.html`. Decisions taken after this outline was first written:
> - **Format:** HTML in the course's own design system (not PowerPoint).
> - **Solo defense.** The notes prepare you to answer on every part yourself.
> - **Extension 1 has its own slide** (slide 5). The paper's problem, the paper's method and findings, the baseline, Extension 1, Extension 2 (how) and Extension 2 (results) are slides 2 to 7; cover is slide 1 and references slide 8.
> - "What we chose to mask" was read as "what we chose to make": our design choices and deviations, on slide 4.
> The sections below are the original plan and requirements; the timing table in `README.md` is the final one.

## 1. What the course requires (from `dsca-project-guide.html` and `PROJECT-REDESIGN.md`)

| Rule | Detail |
|---|---|
| Slides | **At most 8**: a cover, **up to 6 content slides**, references. Numbers from the comparison belong on slides; long method text does not |
| Order of the content slides | The baseline paper's **problem, solution, results**, then **our extension's idea and results** |
| Time | **12 minutes to present, 12 minutes of questions**. Slides are handed in **before** Module 6, not brought on the day |
| Honesty | A smoke test must be stated plainly, with what a full run would need. Related follow-up work must be named and contrasted |
| Cost | Personal computer or at most $20 in total (we spent $0) |
| What is graded (4 x 25 points) | **Code and reproduction** (does it run, is it correct) / **Understanding of the research** (explain the paper's problem, method, results, and answer about all of it) / **Motivation and value** (a real, specific weakness) / **Result quality** (a real comparison with the baseline, credible, honest) |
| Q&A | Every teammate can be asked about the paper, the extension and the code. Questions follow the four lines above |

## 2. Proposed storyline: 8 slides, about 12 minutes

| # | Slide | One-sentence message | Evidence and numbers on the slide | Visual | Time | Rubric line |
|---|---|---|---|---|---|---|
| 0 | Cover | Reading, Not Asking: probing a small model's signal for selective refusal | Title, name, course, the paper (RefusalBench, EACL 2026) | none | 0:15 | |
| 1 | **The problem** (paper) | A grounded model must refuse when the evidence is bad, and today's models rarely do it correctly | The six failure classes with one tiny example each; answer vs refuse vs why | six-box diagram | 1:30 | Understanding |
| 2 | **The paper's solution** | RefusalBench builds controlled bad evidence and measures detection (when) separately from categorization (why) | 1,600 NQ examples from 100 questions, 3 intensities, judge, metrics (answer acc, refusal acc, FRR, MRR); paper's finding: nobody is good at both (best refusal accuracy 73.0%) | pipeline sketch | 1:45 | Understanding |
| 3 | **Baseline: what we reproduced** | We reproduced Qwen1.5-7B-Chat on free resources, with documented choices | Paper vs ours: answer acc 0.561 vs 0.690, refusal acc about 0.05 vs 0.114; our choices: Colab T4 in 4-bit, Gemini judge instead of Claude, parse-first scoring, 1,560 of 1,600 generated, 770 graded so far | Table I + a "what we changed" box | 2:15 | Code and reproduction |
| 4 | **The limitation, and extension 1 (a failure)** | The baseline misses 46% of required refusals; asking the model to diagnose first made it worse | Baseline: 64% of replies are free text, misses ambiguity 0.74 and contradiction 0.71. Extension 1: model says CLEAR on 95% (762 of 800); refusals detected 1.9% vs 43.3%; format-only control | the 3-column table (baseline / control / ours) | 1:45 | Motivation |
| 5 | **Extension 2: how we built it** | Do not ask the model, read it: one forward pass, three readouts, no generation | S1 refusal-code probability, S2 yes/no probability, S3 hidden-state probe; cross-fitted over source questions (why: 100 questions leak); cluster bootstrap; 0.3 s per example, $0 | overview diagram | 2:00 | Code, Motivation |
| 6 | **Results and honest verdict** | The signal is real; a threshold does not beat the baseline; the probe is a small, unclear gain | AUROC .73 / .75 / .80; BA vs judged baseline: .690 vs S1 .658, S2 .669, probe .718 (+0.028 [-0.014, +0.065]); contradiction misses .71 to .19 for the probe but false refusals .17 to .29; limits and what a full run needs | trade-off plot with the baseline point | 2:30 | Result quality |
| 7 | References | | The 20 references from the paper (cut to those cited on slides, plus related work) | | 0:00 | |

Total about 12:00. Related work (Self-RAG, R-Tuning, probing papers) goes in one line on slide 5 or 6 and in the references.

## 3. The numbers to have in your head

- **Paper (Qwen1.5-7B, NQ):** answer accuracy 0.561, refusal accuracy about 0.05. Best refusal accuracy of any model on NQ: 73.0% (Claude 4 Sonnet).
- **Our baseline (770 graded replies):** answer 0.690, refusal 0.114, FRR 0.165, MRR 0.456, detection F1 0.668, balanced accuracy 0.690.
- **Extension 1 (776 common examples):** CLEAR on 762 of 800 (95%), detection 1.9% vs 43.3%, correct category 0.0% vs 6.8%.
- **Extension 2 (1,600 examples):** AUROC S1 .726, S2 .751, S3 .797. Against the judged baseline: S1 default -0.031 (worse), others no clear difference, probe +0.028.
- **Cost and compute:** $0, one free Colab T4, about 8 minutes per scoring pass.

## 4. Decisions I need from you

1. **Format of the slides:** PowerPoint (.pptx, easy for your doctor to edit), or LaTeX Beamer (same look as the paper), or Google Slides. I recommend **.pptx**.
2. **"What we chose to mask":** I read this as **what we chose to make** (our design choices and deviations), covered on slide 3. Is that right, or did you mean something else?
3. **Slide 4:** I put the baseline's limitation and the Extension 1 failure together, to stay within 6 content slides. Do you prefer to give the failure its own slide and shrink slide 2?
4. **Who presents:** is this a solo defense or a team? It changes the Q&A preparation.

## 5. Risks to fix before the hand-in (not slides, but graded)

- **Repository layout:** the course expects `baseline/` and `extension/` folders with the exact run commands, plus `report/REPORT.md` and `slides/`. Ours are named `Benchmark-...`. This is worth 25 points (code and reproduction).
- **Half-graded baseline** and **no judge hand check**: the committee's likeliest attack. Finish both before the defense.
- **Q&A:** I will prepare a question sheet from the rubric, with honest answers drawn only from our evidence.
