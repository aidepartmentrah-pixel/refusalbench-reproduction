# Expanded presentation: "Reading, Not Asking" (23 slides)

The long version of the defense: the paper explained first (problem, how the benchmark is built, the three kinds of models, what the judge does, the measurements, the findings), then our baseline and how we ran it, Extension 1 (the failure), Extension 2 (the signal), and the verdict.

**It does not replace the hand-in.** The course allows at most 8 slides and 12 minutes, so the 8-slide deck in `../Benchmark-Novelty-2-Confidence-Threshold Presentation/` stays the hand-in. This deck is for your preparation, for backup slides during the 12 minutes of questions, and for a longer talk if the doctor allows it (ask him whether appendix slides are accepted).

| File | What it is |
|---|---|
| `expanded-slides.html` | **The deck.** Open it in Chrome or Edge, nothing to install |
| `exports/expanded-slides.pdf` | The 23 slides as a PDF (all build steps shown, no notes) |
| `exports/speaker-notes.md` | **Your script**: for every slide, the time to spend, what to say, the questions to expect and honest answers |
| `assets/slides.css`, `assets/slides.js` | Our own stylesheet and slide runner, written for this deck |
| `assets/img/tradeoff.png` | The trade-off chart, drawn by `make_figures.py` from the repository's result files |
| `make_figures.py`, `export_notes.py` | Redraw the chart, and rebuild `speaker-notes.md` from the deck |

## Presenting

Open `expanded-slides.html`. Keys: **right arrow or space** next, **left arrow** back, **N** shows the speaker notes, **F** fullscreen, **Home** and **End**. Some slides build step by step (the next click reveals the next box). An address ending in `#7` opens slide 7.

## The slides

| Part | Slides | In the 12-minute deck |
|---|---|---|
| Overview | 1 cover, 2 the story in one minute | cover |
| **The paper** | 3 the problem, 4 six reasons to refuse, 5 how the benchmark was built, 6 what is inside it, 7 three kinds of models, 8 what the judge decides, 9 the measurements, 10 what the paper found | slides 2 and 3 |
| **Our baseline** | 11 the scenario we recreated, 12 how we ran it (Colab T4, for classmates), 13 what we kept and what we changed, 14 our numbers | slide 4 |
| **Extension 1** | 15 the idea, 16 the result | slide 5 |
| **Extension 2** | 17 the idea, 18 how we kept the test honest, 19 the numbers, 20 the trade-off picture, 21 per failure type | slides 6 and 7 |
| Closing | 22 verdict and limits, 23 references | slide 7, references |

## The look

Our own design, in the spirit of your Data Science lifecycle deck: white background, navy text, one rust accent, colour-coded boxes, plain bars. Nothing is taken from the course's lecture system; the stylesheet and the runner were written for this deck. Fonts load from Google Fonts (Source Serif 4 and IBM Plex Sans); without internet the browser uses Georgia and Segoe UI.

## How it was checked

- All 23 slides were rendered in Chrome at 1280 x 720 with every build step showing, and looked at one by one.
- A script measured every slide: no content past the slide edge, no text below 18 px, every image loaded. All 23 pass.
- The PDF was exported and checked (23 pages, steps all shown, notes absent).
- Not tested: a projector, other browsers, the touch screen. Open the deck once in the room's setup before the defense.

## Facts to trust and facts to keep an eye on

- Paper facts (73.0%, 47.4%, 56.1%, 93.1%, 176 levers, Claude-4-Sonnet as judge, score 4 or 5 is correct, unanimous verification) were read from the paper itself.
- Our numbers come from the repository's result files and match the IEEE paper.
- The invented worked examples (slides 8 and 9) are marked as illustrations.
- "Four A100 GPUs, 80 GB each" and "likely full precision" on slide 13 come from our project notes, not directly from the paper; the notes say "likely".

## Update when the baseline is fully graded

Slides 14, 19, 20, 21 and 22 carry the 770-of-1,560 numbers. After grading: re-run `compare_to_baseline.py`, run `python make_figures.py` (needs matplotlib), then update those slides and the "770" mentions in the notes, run `python export_notes.py`, and re-export the PDF.

## Open items

1. The 30-reply judge hand check, and grading the other 790 replies.
2. Ask the doctor whether extra slides after the references are accepted.
3. The 8-slide hand-in deck still uses the course's lecture style. If you want it in this look too, it is a re-skin of that file with the same content.
