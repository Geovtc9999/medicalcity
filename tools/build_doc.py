#!/usr/bin/env python3
"""Rend un document Markdown en PDF A4 présentable, même charte que le CV.

    python3 tools/build_doc.py cv/annexes/poc-ecomms-recordkeeping.md \
        --sous-titre "Richard YI — note d'architecture" --out cv/build

Sous-ensemble Markdown couvert : titres, paragraphes, listes à puces et numérotées,
tableaux (avec alignement), blocs de code, citations, filets, gras, italique, code
en ligne, liens. Suffisant pour les notes de ce dossier, et volontairement court :
un rendu à maintenir vaut mieux qu'une dépendance de plus.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from build_cv import run_chrome, chrome  # noqa: E402 — même répertoire, exécution en script

ROOT = Path(__file__).resolve().parents[1]

BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"\[\[(.+?)\]\]", re.DOTALL)

CSS = r"""
@page { size: A4; margin: 16mm 17mm 18mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Liberation Serif", Georgia, "Times New Roman", serif;
  font-size: 10.2pt; line-height: 1.5; color: #1B2430;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
@media screen {
  html { background: #E5E7EB; }
  body { width: 210mm; padding: 16mm 17mm; margin: 0 auto; background: #fff; }
}
.doc-head { border-bottom: 2px solid #0E8A80; padding-bottom: 9px; margin-bottom: 16px; }
.doc-head .kicker {
  font-family: "Liberation Sans", Helvetica, sans-serif; font-size: 7.8pt; font-weight: 700;
  letter-spacing: .16em; text-transform: uppercase; color: #0A5F58;
}
.doc-head .who {
  font-family: "Liberation Sans", Helvetica, sans-serif; font-size: 8.6pt; color: #5C6B73; margin-top: 3px;
}
h1 {
  font-family: "Liberation Sans", Helvetica, sans-serif;
  font-size: 17pt; line-height: 1.2; color: #0A1628; margin: 6px 0 0; letter-spacing: -.01em;
}
h2 {
  font-family: "Liberation Sans", Helvetica, sans-serif; font-size: 11.4pt; color: #0A1628;
  margin: 17px 0 7px; padding-bottom: 3px; border-bottom: 1px solid #D9D3C7;
  break-after: avoid;
}
h3 {
  font-family: "Liberation Sans", Helvetica, sans-serif; font-size: 10pt; color: #0A5F58;
  margin: 13px 0 4px; break-after: avoid;
}
p { margin: 0 0 8px; text-align: justify; hyphens: auto; }
ul, ol { margin: 0 0 9px; padding-left: 17px; }
li { margin: 0 0 4px; }
li::marker { color: #0E8A80; }
strong { color: #0A1628; }
code {
  font-family: "Liberation Mono", "DejaVu Sans Mono", monospace; font-size: 8.8pt;
  background: #F1F5F4; padding: 0 3px; border-radius: 2px; color: #0A5F58;
}
pre {
  background: #0A1628; color: #E7F4F2; padding: 10px 13px; border-radius: 3px;
  font-size: 7.4pt; line-height: 1.4; overflow: hidden; break-inside: avoid;
  margin: 0 0 10px;
}
pre code { background: none; color: inherit; padding: 0; font-size: 7.4pt; }
blockquote {
  margin: 0 0 10px; padding: 7px 12px; background: #E7F4F2; border-left: 3px solid #0E8A80;
  font-size: 9.8pt; color: #16323A;
}
blockquote p { margin: 0; text-align: left; }
table {
  width: 100%; border-collapse: collapse; margin: 0 0 11px; font-size: 8.9pt;
  break-inside: avoid;
  font-family: "Liberation Sans", Helvetica, sans-serif;
}
th {
  background: #0A1628; color: #F6F4EF; text-align: left; padding: 5px 7px; font-weight: 700;
  font-size: 8.2pt; letter-spacing: .02em;
}
td { padding: 4px 7px; border-bottom: 1px solid #E3E0D8; vertical-align: top; }
tr:nth-child(even) td { background: #FAF9F6; }
hr { border: 0; border-top: 1px solid #D9D3C7; margin: 15px 0; }
a { color: #0A5F58; text-decoration: none; border-bottom: 1px dotted #9DC3BE; }
.todo { background: #FFF3C4; border-bottom: 1px dotted #B45309; color: #7A4A06; font-style: italic; }
.footer {
  position: fixed; bottom: -11mm; left: 0; right: 0;
  font-family: "Liberation Sans", Helvetica, sans-serif; font-size: 7.4pt; color: #8A97A0;
  border-top: 1px solid #E3E0D8; padding-top: 4px;
  display: flex; justify-content: space-between;
}
"""


def inline(text: str) -> str:
    out = html.escape(text)
    out = CODE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)
    out = PLACEHOLDER.sub(lambda m: f'<span class="todo">{m.group(1)}</span>', out)
    return out


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _aligns(line: str) -> list[str]:
    out = []
    for cell in _cells(line):
        if cell.endswith(":") and cell.startswith(":"):
            out.append("center")
        elif cell.endswith(":"):
            out.append("right")
        else:
            out.append("left")
    return out


def markdown_to_html(md: str) -> tuple[str, str]:
    """Retourne (titre, corps html). Le premier `# titre` est extrait pour l'en-tête."""
    lines = md.splitlines()
    title = ""
    body: list[str] = []
    i = 0
    para: list[str] = []

    def flush_para() -> None:
        if para:
            body.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para()
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(html.escape(lines[i]))
                i += 1
            i += 1
            body.append("<pre><code>" + "\n".join(block) + "</code></pre>")
            continue

        if stripped.startswith("|"):
            flush_para()
            table = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table.append(lines[i])
                i += 1
            if len(table) >= 2 and set(table[1].replace("|", "").replace(" ", "")) <= set("-:"):
                aligns = _aligns(table[1])
                head = "".join(
                    f'<th style="text-align:{aligns[j] if j < len(aligns) else "left"}">{inline(c)}</th>'
                    for j, c in enumerate(_cells(table[0]))
                )
                rows = []
                for row in table[2:]:
                    tds = "".join(
                        f'<td style="text-align:{aligns[j] if j < len(aligns) else "left"}">{inline(c)}</td>'
                        for j, c in enumerate(_cells(row))
                    )
                    rows.append(f"<tr>{tds}</tr>")
                body.append(f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>")
            else:
                for row in table:
                    para.append(row)
                flush_para()
            continue

        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            items: list[str] = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            body.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+[.)]\s+", line):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]).strip())
                i += 1
            body.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
            continue

        if stripped.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            paragraphs = []
            buffer: list[str] = []
            for chunk in quote:
                if chunk:
                    buffer.append(chunk)
                elif buffer:
                    paragraphs.append(" ".join(buffer))
                    buffer = []
            if buffer:
                paragraphs.append(" ".join(buffer))
            body.append("<blockquote>" + "".join(f"<p>{inline(p)}</p>" for p in paragraphs) + "</blockquote>")
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            flush_para()
            body.append("<hr>")
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flush_para()
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1 and not title:
                title = text
            else:
                body.append(f"<h{min(level, 4)}>{inline(text)}</h{min(level, 4)}>")
            i += 1
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return title, "".join(body)


def render(md_path: Path, kicker: str, sous_titre: str, footer: str) -> tuple[str, str]:
    title, body = markdown_to_html(md_path.read_text(encoding="utf-8"))
    head = (
        '<div class="doc-head">'
        f'<div class="kicker">{html.escape(kicker)}</div>'
        f"<h1>{inline(title)}</h1>"
        f'<div class="who">{inline(sous_titre)}</div>'
        "</div>"
    )
    page = (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>"
        f'{head}{body}<div class="footer"><span>{inline(footer)}</span>'
        f"<span>{html.escape(title)}</span></div></body></html>"
    )
    return title, page


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="fichier Markdown")
    ap.add_argument("--kicker", default="Note d'architecture")
    ap.add_argument("--sous-titre", dest="sous_titre",
                    default="Richard YI — candidature Lead Solution Architect")
    ap.add_argument("--footer", default="Richard YI · document de travail · données et hypothèses à confirmer")
    ap.add_argument("--out", type=Path, default=ROOT / "cv/build")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    source: Path = args.source if args.source.is_absolute() else ROOT / args.source
    if not source.exists():
        ap.error(f"introuvable : {source}")

    _title, page = render(source, args.kicker, args.sous_titre, args.footer)
    args.out.mkdir(parents=True, exist_ok=True)
    html_path = args.out / f"{source.stem}.html"
    pdf_path = args.out / f"{source.stem}.pdf"
    html_path.write_text(page, encoding="utf-8")
    print(f"html  {html_path}")

    if not chrome():
        print("! Chrome introuvable : PDF non généré")
        return 0
    url = html_path.resolve().as_uri()
    with __import__("tempfile").TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        base = [
            chrome(), "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
            "--hide-scrollbars", f"--user-data-dir={profile}", "--virtual-time-budget=4000",
        ]
        if run_chrome(base + ["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", url], pdf_path):
            print(f"pdf   {pdf_path}")
        if args.png:
            shot = pdf_path.with_suffix(".png")
            run_chrome(base + ["--window-size=1240,1754", f"--screenshot={shot}", url], shot)
            print(f"png   {shot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
