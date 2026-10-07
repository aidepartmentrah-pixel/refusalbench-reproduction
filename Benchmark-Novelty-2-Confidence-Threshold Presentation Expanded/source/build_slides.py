"""Build the 12-slide deck: fill slides.template.html with three diagrams drawn from the numbers below.

Run from anywhere:  python source/build_slides.py      ->  writes ../defense-12-slides.html

To update the deck after the baseline is fully graded: change the numbers in NUMBERS, edit slides.template.html if a
sentence changes, run this script, then re-export the PDF and the notes (export_notes.py).
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "defense-12-slides.html")

INK, MUTED, LINE, GREY = "#14213d", "#5b6577", "#dfe3ea", "#9aa3b2"
BLUE, TEAL, RUST, ROSE = "#2f6fde", "#0f9d8a", "#b5541a", "#d6336c"
SOFT = {"teal": ("#def4f0", TEAL), "rust": ("#fbf1e9", RUST), "blue": ("#e6effc", BLUE), "rose": ("#fde4ec", ROSE),
        "white": ("#ffffff", INK), "navy": (INK, INK)}

# ---- every number drawn in a diagram comes from here (all verified against the repository's result files)
NUMBERS = {
    "auroc": {"S1": (0.726, 0.699, 0.752), "S2": (0.751, 0.723, 0.777), "S3": (0.797, 0.770, 0.825)},
    "ba": {"base": 0.690, "S1": 0.658, "S2": 0.669, "S3": 0.718},
    "diff": {"S1": (-0.031, -0.057, -0.005), "S2": (-0.020, -0.047, 0.007), "S3": (0.028, -0.014, 0.065)},
    "repro": {"answer": (0.561, 0.690), "refusal": (0.05, 0.114)},
    "clean": (528, 34), "other": (1032, 66),
}


def esc(t):
    return html.escape(t, quote=False)


def box(x, y, w, h, title, subs=(), kind="white", tsize=21, ssize=18):
    fill, stroke = SOFT[kind]
    tcol = "#fff" if kind == "navy" else INK
    scol = "#c9d0de" if kind == "navy" else MUTED
    subs = [subs] if isinstance(subs, str) else list(subs)
    total = tsize * 1.2 + len(subs) * ssize * 1.3
    y0 = y + (h - total) / 2 + tsize
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>',
           f'<text x="{x + w / 2}" y="{y0:.1f}" text-anchor="middle" font-size="{tsize}" font-weight="600" fill="{tcol}">{esc(title)}</text>']
    for k, s in enumerate(subs):
        out.append(f'<text x="{x + w / 2}" y="{y0 + tsize * 0.2 + (k + 1) * ssize * 1.3:.1f}" text-anchor="middle" '
                   f'font-size="{ssize}" fill="{scol}">{esc(s)}</text>')
    return "\n".join(out)


def arrow(path, mid):
    return f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="2.2" marker-end="url(#{mid})"/>'


def defs(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>')


# ------------------------------------------------------------------ 1. parse-first evaluation pipeline (reproduction)
def svg_pipeline():
    c, o = NUMBERS["clean"], NUMBERS["other"]
    p = [f'<svg width="1136" height="300" viewBox="0 0 1136 300" role="img" aria-label="Evaluation pipeline: reply goes to a parser; clean refusal codes are compared with the expected code, everything else goes to the Gemini judge; both feed the metrics.">',
         defs("a1")]
    p.append(box(0, 0, 230, 62, "Question + passage"))
    p.append(box(268, 0, 230, 62, "Qwen1.5-7B-Chat", "writes a reply", "teal"))
    p.append(box(536, 0, 230, 62, "Generated reply"))
    p.append(box(804, 0, 332, 62, "Parser", "exactly one clean refusal code?", "rust"))
    p.append(arrow("M230 31 H264", "a1") + arrow("M498 31 H532", "a1") + arrow("M766 31 H800", "a1"))
    p.append(arrow("M970 62 V92 H190 V132", "a1"))
    p.append(arrow("M970 62 V132", "a1"))
    p.append(f'<text x="204" y="120" font-size="19" font-weight="600" fill="{TEAL}">Yes: {c[0]} replies ({c[1]}%)</text>')
    p.append(f'<text x="956" y="120" font-size="19" font-weight="600" text-anchor="end" fill="{RUST}">No: {o[0]:,} replies ({o[1]}%)</text>')
    p.append(box(40, 136, 300, 62, "Compare with expected code", "plain text match, no judge", "teal"))
    p.append(box(810, 136, 320, 62, "Gemini judge", "answer or refusal · score 1 to 5", "rust"))
    p.append(arrow("M190 198 V267 H286", "a1"))
    p.append(arrow("M970 198 V267 H854", "a1"))
    p.append(box(290, 236, 560, 62, "Metrics", "answer and refusal accuracy · false and missed refusal", "navy"))
    p.append("</svg>")
    return "\n".join(p)


# ------------------------------------------------------------------ 2. paper versus ours: grouped bars (reproduction results)
def svg_bars():
    (pa, oa), (pr, orf) = NUMBERS["repro"]["answer"], NUMBERS["repro"]["refusal"]
    base, scale = 270, 230
    p = ['<svg width="520" height="340" viewBox="0 0 520 340" role="img" aria-label="Answer accuracy and refusal accuracy, paper versus ours.">']
    p.append(f'<rect x="0" y="6" width="16" height="16" rx="3" fill="{GREY}"/><text x="24" y="20" font-size="19">Paper</text>')
    p.append(f'<rect x="112" y="6" width="16" height="16" rx="3" fill="{BLUE}"/><text x="136" y="20" font-size="19">Ours</text>')
    p.append(f'<line x1="40" y1="{base}" x2="500" y2="{base}" stroke="{INK}" stroke-width="2"/>')
    for gx, (pv, ov), lab, sub, ptxt in ((150, (pa, oa), "Answer accuracy", "", f"{pa:.3f}"),
                                         (390, (pr, orf), "Refusal accuracy", "right reason", f"~{pr:.2f}")):
        for dx, v, col, txt in ((-78, pv, GREY, ptxt), (4, ov, BLUE, f"{ov:.3f}")):
            h = v * scale
            p.append(f'<rect x="{gx + dx}" y="{base - h:.1f}" width="74" height="{h:.1f}" fill="{col}" rx="3"/>')
            p.append(f'<text x="{gx + dx + 37}" y="{base - h - 9:.1f}" text-anchor="middle" font-size="20" font-weight="600">{txt}</text>')
        p.append(f'<text x="{gx}" y="{base + 28}" text-anchor="middle" font-size="20" font-weight="600">{lab}</text>')
        if sub:
            p.append(f'<text x="{gx}" y="{base + 50}" text-anchor="middle" font-size="18" fill="{MUTED}">{sub}</text>')
    p.append("</svg>")
    return "\n".join(p)


# ------------------------------------------------------------------ 3. Extension 2 results: A (signal) and B (decision)
def svg_results():
    au, ba, df = NUMBERS["auroc"], NUMBERS["ba"], NUMBERS["diff"]
    col = {"S1": BLUE, "S2": TEAL, "S3": RUST}
    desc = {"S1": "refusal prob.", "S2": "yes or no", "S3": "probe"}
    rows = {"S1": 150, "S2": 225, "S3": 300}
    ax = lambda v: 140 + (v - 0.5) / 0.4 * 350          # AUROC 0.5 .. 0.9
    bx = lambda v: 950 + v * 2000                          # difference -0.08 .. +0.08 (zero at 950)
    p = ['<svg width="1136" height="410" viewBox="0 0 1136 410" role="img" aria-label="Left: AUROC of the three readouts with 95 percent intervals, all above chance. Right: difference in balanced accuracy versus the baseline; only S1 excludes zero, and it is worse; the probe interval crosses zero.">']
    # panel titles
    p.append('<text x="0" y="26" font-size="23" font-weight="600">A. Is there information inside the model?</text>')
    p.append(f'<text x="0" y="54" font-size="18" fill="{MUTED}">AUROC with 95% interval: 0.5 is chance, 1.0 is perfect</text>')
    p.append('<text x="616" y="26" font-size="23" font-weight="600">B. Does using it beat the baseline?</text>')
    p.append(f'<text x="616" y="54" font-size="18" fill="{MUTED}">Balanced accuracy minus baseline ({ba["base"]:.3f}), 95% interval</text>')
    # axes
    for v in (0.5, 0.6, 0.7, 0.8, 0.9):
        p.append(f'<line x1="{ax(v):.1f}" y1="92" x2="{ax(v):.1f}" y2="338" stroke="{LINE}" stroke-width="1.5"/>')
        p.append(f'<text x="{ax(v):.1f}" y="366" text-anchor="middle" font-size="18" fill="{MUTED}">{v:.1f}</text>')
    p.append(f'<line x1="{ax(0.5):.1f}" y1="92" x2="{ax(0.5):.1f}" y2="338" stroke="{INK}" stroke-width="2.2" stroke-dasharray="6 5"/>')
    p.append(f'<text x="{ax(0.5) + 8:.1f}" y="108" font-size="18" fill="{MUTED}">chance</text>')
    for v in (-0.08, -0.04, 0.0, 0.04, 0.08):
        lab = "0" if v == 0 else f"{v:+.2f}"
        p.append(f'<line x1="{bx(v):.1f}" y1="92" x2="{bx(v):.1f}" y2="338" stroke="{LINE}" stroke-width="1.5"/>')
        p.append(f'<text x="{bx(v):.1f}" y="366" text-anchor="middle" font-size="18" fill="{MUTED}">{lab}</text>')
    p.append(f'<line x1="{bx(0):.1f}" y1="92" x2="{bx(0):.1f}" y2="338" stroke="{INK}" stroke-width="2.2" stroke-dasharray="6 5"/>')
    p.append(f'<text x="{bx(0) + 8:.1f}" y="108" font-size="18" fill="{MUTED}">same as baseline</text>')
    p.append(f'<text x="{bx(-0.08):.1f}" y="396" font-size="18" fill="{MUTED}">worse</text>')
    p.append(f'<text x="{bx(0.08):.1f}" y="396" text-anchor="end" font-size="18" fill="{MUTED}">better</text>')
    # rows
    for k, y in rows.items():
        v, lo, hi = au[k]
        p.append(f'<text x="0" y="{y - 2}" font-size="22" font-weight="600">{k}</text>')
        p.append(f'<text x="0" y="{y + 20}" font-size="18" fill="{MUTED}">{desc[k]}</text>')
        p.append(f'<line x1="{ax(lo):.1f}" y1="{y}" x2="{ax(hi):.1f}" y2="{y}" stroke="{col[k]}" stroke-width="5" stroke-linecap="round"/>')
        p.append(f'<circle cx="{ax(v):.1f}" cy="{y}" r="10" fill="{col[k]}" stroke="#fff" stroke-width="2.5"/>')
        p.append(f'<text x="{ax(v):.1f}" y="{y - 20}" text-anchor="middle" font-size="20" font-weight="600">{v:.3f}</text>')
        d, dlo, dhi = df[k]
        p.append(f'<text x="616" y="{y - 2}" font-size="22" font-weight="600">{k}</text>')
        p.append(f'<text x="616" y="{y + 20}" font-size="18" fill="{MUTED}">accuracy {ba[k]:.3f}</text>')
        p.append(f'<line x1="{bx(dlo):.1f}" y1="{y}" x2="{bx(dhi):.1f}" y2="{y}" stroke="{col[k]}" stroke-width="5" stroke-linecap="round"/>')
        p.append(f'<circle cx="{bx(d):.1f}" cy="{y}" r="10" fill="{col[k]}" stroke="#fff" stroke-width="2.5"/>')
        p.append(f'<text x="{bx(d):.1f}" y="{y - 20}" text-anchor="middle" font-size="20" font-weight="600">{d:+.3f}</text>')
    p.append("</svg>")
    return "\n".join(p)


def main():
    tpl = open(os.path.join(HERE, "slides.template.html"), encoding="utf-8").read()
    for key, fn in (("{{SVG_PIPELINE}}", svg_pipeline), ("{{SVG_BARS}}", svg_bars), ("{{SVG_RESULTS}}", svg_results)):
        assert key in tpl, key
        tpl = tpl.replace(key, fn())
    open(OUT, "w", encoding="utf-8").write(tpl)
    print("written", OUT, len(tpl), "chars")


if __name__ == "__main__":
    main()
