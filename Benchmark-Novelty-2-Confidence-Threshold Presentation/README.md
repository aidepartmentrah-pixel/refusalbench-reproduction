# Defense slides: "Reading, Not Asking"

8 slides in the course's own design system (one cover, six content slides, one reference slide), 12 minutes, with speaker notes on every slide.

| File | What it is |
|---|---|
| `defense-slides.html` | **The deck.** Open it in Chrome or Edge, nothing to install. The two web fonts load from Google; without internet the course falls back to system fonts |
| `exports/defense-slides.pdf` | The 8 slides as a PDF (backup if the room has no browser, and the file to hand in if a PDF is asked for) |
| `exports/defense-handout-with-notes.pdf` | The same slides with the speaker notes under each one: **your speaking script and question answers** |
| `OUTLINE.md` | The plan this deck was built from (requirements, timing, decisions) |
| `make_figures.py` | Redraws the results chart (`assets/img/tradeoff-baseline.png`) from the repository's own result files |
| `assets/` | `lu.css` and `lu-deck.js` (copied unchanged from the course repository, so the deck works from any folder) and the chart |

## Presenting

Open `defense-slides.html`. Keys: `Right` and `Left` arrows to move, `P` presenter view (notes and clock), `S` study mode, `O` contents, `/` search, `?` all shortcuts. Add `#/7` to the address to open slide 7 directly.

## The storyline and the time (12 minutes)

| # | Slide | Minutes | Rubric line it serves |
|---|---|---|---|
| 1 | Cover | 0.5 | |
| 2 | The paper and its problem (with the paper's own East India Company example) | 1.5 | Understanding of the research |
| 3 | The paper's method and findings | 1.75 | Understanding of the research |
| 4 | Our baseline reproduction: numbers next to the paper's, and what we changed | 2.0 | Code and reproduction |
| 5 | Extension 1, the limitation and the failure | 1.75 | Motivation, honesty |
| 6 | Extension 2, the idea and how it is built | 2.0 | Code, motivation |
| 7 | Extension 2, results against the baseline, and the limits | 2.25 | Result quality |
| 8 | References | 0 | |

## How it was checked

- Every slide was rendered in Chrome at 1600 x 900 and looked at.
- The course's own `scripts/audit-deck.js` was run through Chrome: **all 14 checks pass** (no slide overflows, nothing below the 20 px floor, no stray characters, notes and minutes agree, no hidden-element leaks).
- The PDF export was opened and checked (8 pages, same layout as on screen).
- Not checked: the presenter view (`P`) and study mode (`S`) were not exercised by hand. Open both once before the defense.

## Numbers on the slides, and where they come from

| On the slides | Source |
|---|---|
| Paper: 73.0%, 47.4%, 56.1%, 176 rules, six types, the East India Company example | The paper itself (local copy in your Obsidian folder), Figure 1, introduction and Section 4 |
| Baseline table | `Benchmark-Baseline-Reproduction/qwen15_7b_baseline` (770 graded replies) and the paper |
| Extension 1 table and the 95% | `Benchmark-Novelty-1-Classify-then-Decide/RESULT.md` |
| Extension 2 table and chart | `Benchmark-Novelty-2-Confidence-Threshold/results/` and `.../comparison_all/COMPARISON.md` |

## Update this deck when the baseline is fully graded

Slides 4 and 7 carry the 770-of-1,560 numbers. After the remaining replies are graded: re-run the comparison script, run `python make_figures.py` (needs matplotlib), and replace the numbers on slides 4 and 7 and in their notes. Remove "770 graded so far" and "770 of 1,560 graded" from the two "Honest status" and "Limits" boxes, and re-export the two PDFs.

## Open items before the defense

1. The 30-reply judge hand check (slide 7 says "judge unchecked").
2. The repository layout the course expects (`baseline/`, `extension/`, `report/REPORT.md`, `slides/`) is not done yet; this folder is the content for `slides/`.
3. Decide whether the PDF or the HTML is the hand-in file.
