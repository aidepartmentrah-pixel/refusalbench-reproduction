# Defense presentation, 12 slides: "Reading, Not Asking"

A 12-slide talk of about 12 minutes, in our own look (white, navy, one rust accent). It replaces the earlier 23-slide version (still available in git history, commit `75ff094`).

**About the course limit.** The course allows at most 8 slides (cover, up to 6 content slides, references). This deck has 12. The 8-slide deck in `../Benchmark-Novelty-2-Confidence-Threshold Presentation/` is still the version that fits the rule. Ask the doctor whether 12 is accepted; if not, the 12 can be cut to 8: cover, the paper in 2 slides (problem; methodology with findings), reproduction in 1 slide (design with results), Extension 1 with the turning point in 1, Extension 2 in 1, conclusion, references.

| File | What it is |
|---|---|
| `defense-12-slides.html` | **The deck.** Open it in Chrome or Edge, nothing to install |
| `exports/defense-12-slides.pdf` | The 12 slides as a PDF (build steps all shown, no notes) |
| `exports/speaker-notes.md` | **Your script**: for every slide, the time to spend, what to say, the questions to expect and honest answers |
| `source/slides.template.html`, `source/build_slides.py` | The source of the deck and the script that draws the three diagrams from a table of numbers and writes the HTML |
| `assets/slides.css`, `assets/slides.js` | Our own stylesheet and slide runner |
| `export_notes.py` | Rebuilds `speaker-notes.md` from the deck |

## Presenting

Open `defense-12-slides.html`. Keys: **right arrow or space** next, **left arrow** back, **N** shows the speaker notes, **F** fullscreen, **Home** and **End**. Some slides build step by step. An address ending in `#7` opens slide 7. The top-right of every slide shows which of the five parts of the talk you are in (the paper, reproduction, extension 1, extension 2, conclusion); the paper part ends with an explicit "That is the paper" line.

## The 12 slides

| # | Part and label | Slide | Minutes |
|---|---|---|---|
| 1 | Cover | Title | 0.5 |
| 2 | The paper · Problem | Selective refusal, with the paper's own before/after example and the six reasons | 1.25 |
| 3 | The paper · Methodology | How the benchmark is built, and how a reply is scored (target model, judge) | 1.5 |
| 4 | The paper · Findings | Three big numbers, the terms we use, "That is the paper" | 1.0 |
| 5 | Reproduction · Design | The evaluation pipeline (parse first, then judge), the Colab T4 memory band, what was kept and changed | 1.5 |
| 6 | Reproduction · Results | Paper against ours, false and missed refusal | 1.0 |
| 7 | Extension 1 · Hypothesis, method and result | The three prompts, one dominant number (762 of 800), refusals caught | 1.25 |
| 8 | Turning point (dark slide) | "Do not ask the model. Read it." | 0.5 |
| 9 | Extension 2 · Hypothesis and method | Three readouts, the threshold rule, the evaluation design | 1.25 |
| 10 | Extension 2 · Results | Two questions: is there information (yes), does it beat the baseline (not shown) | 1.5 |
| 11 | Conclusion and limitations | Decodable is not deployable; can say, cannot say, full run needs | 0.75 |
| 12 | References | | 0 |

Material that is no longer on a slide but is kept in the notes, in case it is asked: the worked example of the metrics, the per-failure-type results, the trade-off picture, the model-size scaling in the paper, and the details of the evaluation design.

## How it was checked

- Every slide was rendered in Chrome at 1280 x 720 with all build steps showing, and looked at.
- A script measured every slide: nothing past the slide edge, no text under 18 px, images and diagrams drawn. All 12 pass.
- The PDF was exported and checked (12 pages, no notes in it, the dark slide prints correctly).
- Not tested: a projector, other browsers.

## Numbers and where they come from

Paper facts (73.0%, 47.4%, 56.1%, 13.0%, 176 rules, 93.1%, Claude-4-Sonnet as judge) are from the paper itself. Our numbers match the IEEE report and the result files in the repository. Slide 5 says "four A100 GPUs" and "likely full precision" for the paper: these come from our project notes, not directly from the paper, and the slide says "likely".

## Update when the baseline is fully graded

Slides 5, 6 and 10, and their notes, carry the 770-of-1,560 numbers. Change the numbers in `source/build_slides.py` (table `NUMBERS`) and the text in `source/slides.template.html`, run `python source/build_slides.py`, then `python export_notes.py`, and re-export the PDF.

## Open items

1. Grade the other 790 replies and do the 30-reply check of the judge.
2. Ask the doctor whether 12 slides are accepted.
