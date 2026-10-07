"""Write the speaker notes of every slide into one readable file: exports/speaker-notes.md.

Reads expanded-slides.html (the text inside each slide's <aside>), so the notes always match the deck.
Run:  python export_notes.py
"""

import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "expanded-slides.html"), encoding="utf-8").read()

out = ["# Speaker notes: expanded presentation", "",
       "One section per slide, in order. Each starts with the time to spend, then what to say, then the questions to expect.",
       "The 12-minute hand-in deck is `../../Benchmark-Novelty-2-Confidence-Threshold Presentation/defense-slides.html`.", ""]
n = 0
for m in re.finditer(r'<section class="slide[^"]*" data-title="([^"]*)">(.*?)</section>', src, re.S):
    n += 1
    title, body = m.group(1), m.group(2)
    eyebrow = re.search(r'<div class="eyebrow">(.*?)</div>', body, re.S)
    heading = re.search(r"<h[12]>(.*?)</h[12]>", body, re.S)
    aside = re.search(r"<aside>(.*?)</aside>", body, re.S)
    clean = lambda t: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()
    out.append(f"## {n}. {html.unescape(title)}")
    if eyebrow:
        out.append(f"*{clean(eyebrow.group(1))}*")
    if heading:
        out.append(f"**On the slide:** {clean(heading.group(1))}")
    out.append("")
    if aside:
        for line in aside.group(1).strip().split("\n"):
            line = clean(line)
            if line:
                out.append(line)
                out.append("")
    out.append("---")
    out.append("")

os.makedirs(os.path.join(HERE, "exports"), exist_ok=True)
path = os.path.join(HERE, "exports", "speaker-notes.md")
open(path, "w", encoding="utf-8").write("\n".join(out))
print(f"{n} slides, written {path}")
