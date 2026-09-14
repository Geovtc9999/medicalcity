#!/usr/bin/env python3
"""Rend le deck « ma lecture du programme » en PDF 16:9 depuis un YAML de contenu.

    python3 tools/build_slides.py                  # cv/annexes/deck-lecture-programme.yml
    python3 tools/build_slides.py --png            # + aperçu image de la première slide

Chaque slide porte un titre d'action et un seul message. La mise en page suit le bloc
présent dans le YAML (`cards`, `steps`, `table`, `timeline`, `criteres`), ce qui évite
un moteur de gabarits pour cinq slides.
"""
from __future__ import annotations

import argparse
import html
import re
import tempfile
from pathlib import Path

import yaml

from build_cv import chrome, run_chrome  # noqa: E402 — même répertoire, exécution en script

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "cv/annexes/deck-lecture-programme.yml"

BOLD = re.compile(r"\*\*(.+?)\*\*")
CODE = re.compile(r"`([^`]+)`")

CSS = r"""
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #111; }
body {
  font-family: "Liberation Sans", "Segoe UI", Helvetica, Arial, sans-serif;
  color: #1B2430; -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.slide {
  width: 1280px; height: 720px; background: #fff; padding: 40px 56px 112px;
  position: relative; overflow: hidden; page-break-after: always; break-after: page;
  display: flex; flex-direction: column;
}
/* Le contenu occupe l'espace disponible : une slide à moitié vide se lit comme un brouillon. */
.content { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 16px; }
.slide:last-child { page-break-after: auto; break-after: auto; }
.topbar {
  position: absolute; top: 0; left: 0; right: 0; height: 6px;
  background: linear-gradient(90deg, #0E8A80 0 72%, #C4A574 72% 100%);
}
.kicker {
  font-size: 11px; letter-spacing: .18em; text-transform: uppercase;
  color: #0A5F58; font-weight: 700; margin: 8px 0 10px;
}
h1 { font-size: 30px; line-height: 1.24; color: #0A1628; margin: 0 0 14px; max-width: 1080px; }
.intro { font-size: 17px; line-height: 1.45; color: #45535F; max-width: 1060px; margin: 0 0 6px; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.card { background: #F6F4EF; border: 1px solid #D9D3C7; border-radius: 4px; padding: 14px 16px; }
.card h3 { margin: 0 0 8px; font-size: 16px; color: #0A5F58; }
.card p { margin: 0; font-size: 14.4px; line-height: 1.5; color: #26333F; }
.highlight { background: #E7F4F2; border-left: 4px solid #0E8A80;
  padding: 12px 16px; border-radius: 3px;
}
.highlight h3 { margin: 0 0 6px; font-size: 15.5px; color: #0A1628; }
.highlight p { margin: 0; font-size: 14.2px; line-height: 1.5; color: #16323A; }
.steps { display: flex; flex-direction: column; gap: 15px; }
.step { display: flex; align-items: baseline; gap: 14px; }
.step .num {
  flex: 0 0 38px; height: 38px; border-radius: 50%; background: #0A1628; color: #F6F4EF;
  font-weight: 700; font-size: 14px; display: flex; align-items: center; justify-content: center;
}
.step .body { flex: 1; border-bottom: 1px solid #E3E0D8; padding-bottom: 6px; }
.step .t { font-size: 16px; font-weight: 700; color: #0A5F58; }
.step .d { font-size: 14.2px; color: #37474F; margin-left: 8px; }
table { width: 100%; border-collapse: collapse; font-size: 13.8px; }
th {
  background: #0A1628; color: #F6F4EF; text-align: left; padding: 8px 10px;
  font-size: 12px; letter-spacing: .03em;
}
td { padding: 9px 10px; border-bottom: 1px solid #E3E0D8; vertical-align: top; line-height: 1.4; }
tr:nth-child(even) td { background: #FAF9F6; }
td:first-child { font-weight: 700; color: #0A5F58; white-space: nowrap; }
.split { display: grid; grid-template-columns: 1.05fr 1fr; gap: 26px; }
.timeline { display: flex; flex-direction: column; gap: 14px; }
.tl { display: flex; gap: 12px; align-items: baseline; }
.tl .w {
  flex: 0 0 62px; font-size: 12.5px; font-weight: 700; color: #F6F4EF; background: #0E8A80;
  border-radius: 3px; text-align: center; padding: 3px 0;
}
.tl .x { font-size: 14.2px; color: #26333F; line-height: 1.42; }
.crit { background: #0A1628; color: #F6F4EF; border-radius: 4px; padding: 16px 18px; }
.crit h3 { margin: 0 0 9px; font-size: 15px; color: #C4A574; }
.crit ol { margin: 0; padding-left: 18px; }
.crit li { font-size: 13.8px; line-height: 1.46; margin-bottom: 7px; }
.note {
  position: absolute; left: 56px; right: 56px; bottom: 30px;
  font-size: 12.6px; line-height: 1.42; color: #45535F;
  border-top: 1px solid #E3E0D8; padding-top: 8px;
}
.foot {
  position: absolute; left: 56px; right: 56px; bottom: 12px;
  display: flex; justify-content: space-between; font-size: 10px; color: #8A97A0;
  letter-spacing: .04em;
}
.cover { background: #0A1628; color: #F6F4EF; }
.cover h1 { color: #F6F4EF; font-size: 40px; max-width: 960px; }
.cover .kicker { color: #C4A574; }
.cover .intro { color: #B7C4CE; }
"""


def inline(text: str) -> str:
    out = html.escape(" ".join(str(text).split()))
    out = BOLD.sub(r"<b>\1</b>", out)
    out = CODE.sub(r"<code>\1</code>", out)
    return out


def render_slide(slide: dict, meta: dict, index: int, total: int) -> str:
    parts = ['<div class="slide"><div class="topbar"></div>']
    parts.append(f'<div class="kicker">{inline(slide.get("kicker", ""))}</div>')
    parts.append(f'<h1>{inline(slide["titre"])}</h1>')
    parts.append('<div class="content">')
    if slide.get("intro"):
        parts.append(f'<p class="intro">{inline(slide["intro"])}</p>')

    if slide.get("cards"):
        cards = "".join(
            f'<div class="card"><h3>{inline(c["titre"])}</h3><p>{inline(c["texte"])}</p></div>'
            for c in slide["cards"]
        )
        parts.append(f'<div class="cards">{cards}</div>')

    if slide.get("highlight"):
        h = slide["highlight"]
        parts.append(
            f'<div class="highlight"><h3>{inline(h["titre"])}</h3><p>{inline(h["texte"])}</p></div>'
        )

    if slide.get("steps"):
        steps = "".join(
            f'<div class="step"><div class="num">{inline(s["id"])}</div>'
            f'<div class="body"><span class="t">{inline(s["titre"])}</span>'
            f'<span class="d">{inline(s["texte"])}</span></div></div>'
            for s in slide["steps"]
        )
        parts.append(f'<div class="steps">{steps}</div>')

    if slide.get("table"):
        t = slide["table"]
        head = "".join(f"<th>{inline(c)}</th>" for c in t["head"])
        rows = "".join(
            "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in t["rows"]
        )
        parts.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")

    if slide.get("timeline") or slide.get("criteres"):
        left = ""
        if slide.get("timeline"):
            left = '<div class="timeline">' + "".join(
                f'<div class="tl"><div class="w">{inline(w)}</div><div class="x">{inline(x)}</div></div>'
                for w, x in slide["timeline"]
            ) + "</div>"
        right = ""
        if slide.get("criteres"):
            c = slide["criteres"]
            items = "".join(f"<li>{inline(i)}</li>" for i in c["items"])
            right = f'<div class="crit"><h3>{inline(c["titre"])}</h3><ol>{items}</ol></div>'
        parts.append(f'<div class="split">{left}{right}</div>')

    parts.append("</div>")
    if slide.get("note"):
        parts.append(f'<div class="note">{inline(slide["note"])}</div>')
    parts.append(
        f'<div class="foot"><span>{inline(meta["pied"])}</span>'
        f"<span>{index}/{total}</span></div>"
    )
    parts.append("</div>")
    return "".join(parts)


def render_cover(meta: dict, total: int) -> str:
    return (
        '<div class="slide cover"><div class="topbar"></div>'
        f'<div class="kicker">Candidature Lead Solution Architect / Technical Lead</div>'
        f'<h1>{inline(meta["titre"])}</h1>'
        f'<p class="intro">{inline(meta["sous_titre"])}</p>'
        f'<div class="note" style="color:#B7C4CE;border-top-color:#2A3D55">{inline(meta["auteur"])}</div>'
        f'<div class="foot"><span>{inline(meta["pied"])}</span><span>0/{total}</span></div>'
        "</div>"
    )


def build(source: Path, out_dir: Path, png: bool, cover: bool) -> int:
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    meta, slides = data["meta"], data["slides"]
    total = len(slides)
    body = render_cover(meta, total) if cover else ""
    body += "".join(render_slide(s, meta, i, total) for i, s in enumerate(slides, start=1))
    page = (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        f'<title>{html.escape(meta["titre"])}</title><style>{CSS}</style></head>'
        f"<body>{body}</body></html>"
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "deck-lecture-programme.html"
    pdf_path = out_dir / "deck-lecture-programme.pdf"
    html_path.write_text(page, encoding="utf-8")
    print(f"html  {html_path}")

    binary = chrome()
    if not binary:
        print("! Chrome introuvable : PDF non généré")
        return 0
    url = html_path.resolve().as_uri()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        base = [
            binary, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
            "--hide-scrollbars", f"--user-data-dir={profile}", "--virtual-time-budget=4000",
        ]
        if run_chrome(base + ["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", url], pdf_path):
            print(f"pdf   {pdf_path}  ({total + (1 if cover else 0)} slides)")
        if png:
            # Une image par slide : Chrome ne capture que le premier écran d'une page.
            fragments = [render_cover(meta, total)] if cover else []
            fragments += [render_slide(s, meta, i, total) for i, s in enumerate(slides, start=1)]
            for n, fragment in enumerate(fragments):
                one = out_dir / f"deck-slide-{n}.html"
                one.write_text(
                    '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
                    f"<style>{CSS}</style></head><body>{fragment}</body></html>",
                    encoding="utf-8",
                )
                shot = out_dir / f"deck-slide-{n}.png"
                run_chrome(
                    base + ["--window-size=1280,720", f"--screenshot={shot}", one.resolve().as_uri()],
                    shot,
                )
                one.unlink(missing_ok=True)
            print(f"png   {out_dir}/deck-slide-0..{len(fragments) - 1}.png")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--out", type=Path, default=ROOT / "cv/build")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--sans-couverture", action="store_true", help="cinq slides sans page de titre")
    args = ap.parse_args()
    source = args.source if args.source.is_absolute() else ROOT / args.source
    if not source.exists():
        ap.error(f"introuvable : {source}")
    return build(source, args.out, args.png, cover=not args.sans_couverture)


if __name__ == "__main__":
    raise SystemExit(main())
