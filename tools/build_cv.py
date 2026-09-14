#!/usr/bin/env python3
"""Génère le CV ciblé (Markdown + HTML + PDF A4) depuis cv/data/cv-<lang>.yml.

    python3 tools/build_cv.py            # fr + en, mode brouillon
    python3 tools/build_cv.py fr         # une seule langue
    python3 tools/build_cv.py --strict   # échoue s'il reste un [[trou]]
    python3 tools/build_cv.py --png      # PNG de la page 1 (aperçu / revue)

Les `[[...]]` sont des trous que Richard doit combler. Tant qu'il en reste, le PDF porte
un filigrane BROUILLON : impossible d'envoyer par accident un CV à trous.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "cv/data"
BUILD = ROOT / "cv/build"

PLACEHOLDER = re.compile(r"\[\[(.+?)\]\]", re.DOTALL)
BOLD = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)
CODE = re.compile(r"`([^`]+)`")

CHROME_CANDIDATES = ("google-chrome", "chromium", "chromium-browser", "google-chrome-stable")

LABELS = {
    "fr": {"draft": "BROUILLON", "holes": "trous à combler", "page": "CV"},
    "en": {"draft": "DRAFT", "holes": "gaps to fill", "page": "CV"},
}

CSS = r"""
@page { size: A4; margin: 12mm 13mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Liberation Sans", "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 9.1pt; line-height: 1.36; color: #1B2430;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
/* L'aperçu HTML/PNG n'a pas les marges de @page : on les simule à l'écran. */
@media screen {
  body { width: 210mm; padding: 12mm 13mm; margin: 0 auto; background: #fff; }
  html { background: #E5E7EB; }
}
a { color: #0A5F58; text-decoration: none; }
h1 { font-size: 20pt; line-height: 1.1; margin: 0; color: #0A1628; letter-spacing: -.01em; }
.role { font-size: 11pt; font-weight: 700; color: #0A5F58; margin: 3px 0 0; }
.target { font-size: 8.6pt; color: #5C6B73; margin: 4px 0 0; font-style: italic; }
header { border-bottom: 2px solid #0E8A80; padding-bottom: 7px; margin-bottom: 10px; }
.contact { font-size: 8.3pt; color: #37474F; margin: 6px 0 0; }
.contact span:not(:last-child)::after { content: " · "; color: #B0BEC5; }
section { margin: 0 0 9px; }
h2 {
  font-size: 8.4pt; text-transform: uppercase; letter-spacing: .14em; font-weight: 700;
  color: #0A1628; margin: 0 0 6px; padding-bottom: 3px; border-bottom: 1px solid #D9D3C7;
}
p { margin: 0 0 5px; }
.lead { font-size: 9.8pt; }
ul { margin: 0; padding: 0; list-style: none; }
li { margin: 0 0 4px; padding-left: 10px; position: relative; break-inside: avoid; }
li::before {
  content: ""; position: absolute; left: 0; top: .52em;
  width: 4px; height: 4px; background: #0E8A80; border-radius: 50%;
}
li b.h { color: #0A1628; }
.skills { display: grid; grid-template-columns: 1fr 1fr; gap: 5px 16px; }
.skill { break-inside: avoid; }
.skill .k {
  display: block; font-size: 8pt; font-weight: 700; color: #0A5F58;
  text-transform: uppercase; letter-spacing: .06em;
}
.skill .v { font-size: 8.7pt; color: #26333F; }
.job { margin: 0 0 9px; break-inside: avoid; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }
.job-title { font-size: 9.9pt; font-weight: 700; color: #0A1628; }
.job-org { font-weight: 700; color: #0A5F58; }
.job-when { font-size: 8.3pt; color: #5C6B73; white-space: nowrap; }
.job-ctx { font-size: 9pt; color: #45535F; margin: 2px 0 4px; }
.job .stack { font-size: 8.3pt; color: #5C6B73; margin: 3px 0 0; }
.job .stack b { color: #37474F; }
.tail { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.tail section { margin: 0; }
.note {
  background: #E7F4F2; border-left: 3px solid #0E8A80; padding: 6px 9px;
  font-size: 8.8pt; color: #16323A;
}
.todo {
  background: #FFF3C4; border-bottom: 1px dotted #B45309; color: #7A4A06;
  padding: 0 2px; font-style: italic;
}
.watermark {
  position: fixed; top: 46%; left: -4%; width: 108%; text-align: center;
  font-size: 78pt; font-weight: 700; color: rgba(180, 83, 9, .10);
  letter-spacing: .12em; transform: rotate(-24deg); z-index: 99;
}
.stamp {
  position: fixed; top: 4mm; right: 0; font-size: 7.4pt; font-weight: 700;
  color: #B45309; letter-spacing: .1em;
}
"""


# --------------------------------------------------------------------------- data


def load(lang: str) -> dict:
    path = DATA / f"cv-{lang}.yml"
    if not path.exists():
        sys.exit(f"introuvable : {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def find_holes(node, path: str = "") -> list[tuple[str, str]]:
    """Remonte tous les [[trous]] avec leur emplacement dans le YAML."""
    holes: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            holes += find_holes(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            holes += find_holes(value, f"{path}[{i}]")
    elif isinstance(node, str):
        for match in PLACEHOLDER.finditer(node):
            holes.append((path, " ".join(match.group(1).split())))
    return holes


# ------------------------------------------------------------------------- inline


def inline_html(text: str) -> str:
    out = html.escape(" ".join(str(text).split()))
    out = PLACEHOLDER.sub(lambda m: f'<span class="todo">{m.group(1)}</span>', out)
    out = BOLD.sub(r"<b>\1</b>", out)
    out = CODE.sub(r"<code>\1</code>", out)
    return out


def inline_md(text: str) -> str:
    return " ".join(str(text).split())


# --------------------------------------------------------------------------- html


def render_html(cv: dict, lang: str) -> str:
    holes = find_holes(cv)
    labels = LABELS[lang]
    meta = cv["meta"]
    parts: list[str] = []

    if holes:
        parts.append(f'<div class="watermark">{labels["draft"]}</div>')
        parts.append(
            f'<div class="stamp">{labels["draft"]} — {len(holes)} {labels["holes"]}</div>'
        )

    contact = "".join(f"<span>{inline_html(c)}</span>" for c in meta.get("contact", []))
    parts.append(
        "<header>"
        f'<h1>{html.escape(meta["nom"])}</h1>'
        f'<p class="role">{inline_html(meta["titre"])}</p>'
        f'<p class="target">{inline_html(meta.get("cible", ""))}</p>'
        f'<p class="contact">{contact}</p>'
        "</header>"
    )

    profil = cv.get("profil")
    if profil:
        parts.append(
            f'<section><h2>{html.escape(profil["titre"])}</h2>'
            f'<p class="lead">{inline_html(profil["texte"])}</p></section>'
        )

    apport = cv.get("apport")
    if apport:
        items = "".join(
            f'<li><b class="h">{inline_html(p["titre"])}.</b> {inline_html(p["texte"])}</li>'
            for p in apport["puces"]
        )
        parts.append(
            f'<section><h2>{html.escape(apport["titre"])}</h2><ul>{items}</ul></section>'
        )

    comp = cv.get("competences")
    if comp:
        groups = "".join(
            '<div class="skill">'
            f'<span class="k">{inline_html(g["titre"])}</span>'
            f'<span class="v">{inline_html(g["items"])}</span>'
            "</div>"
            for g in comp["groupes"]
        )
        parts.append(
            f'<section><h2>{html.escape(comp["titre"])}</h2>'
            f'<div class="skills">{groups}</div></section>'
        )

    exp = cv.get("experiences")
    if exp:
        jobs = []
        for job in exp["entrees"]:
            bullets = "".join(f"<li>{inline_html(b)}</li>" for b in job.get("puces", []))
            stack = job.get("stack")
            stack_html = f'<p class="stack"><b>Stack :</b> {inline_html(stack)}</p>' if stack else ""
            jobs.append(
                '<div class="job"><div class="job-head">'
                f'<span class="job-title">{inline_html(job["poste"])} — '
                f'<span class="job-org">{inline_html(job["org"])}</span></span>'
                f'<span class="job-when">{inline_html(job.get("lieu", ""))} · '
                f'{inline_html(job.get("dates", ""))}</span></div>'
                f'<p class="job-ctx">{inline_html(job.get("contexte", ""))}</p>'
                f"<ul>{bullets}</ul>{stack_html}</div>"
            )
        parts.append(
            f'<section><h2>{html.escape(exp["titre"])}</h2>{"".join(jobs)}</section>'
        )

    ann = cv.get("annexes_liees")
    if ann:
        parts.append(
            f'<section><h2>{html.escape(ann["titre"])}</h2>'
            f'<p class="note">{inline_html(ann["texte"])}</p></section>'
        )

    tail = []
    for key in ("formation", "langues", "disponibilite"):
        block = cv.get(key)
        if not block:
            continue
        items = "".join(f"<li>{inline_html(e)}</li>" for e in block["entrees"])
        tail.append(f'<section><h2>{html.escape(block["titre"])}</h2><ul>{items}</ul></section>')
    if tail:
        parts.append(f'<div class="tail">{"".join(tail)}</div>')

    return (
        "<!doctype html><html lang=\"" + lang + "\"><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(meta['nom'])} — {html.escape(meta['titre'])}</title>"
        f"<style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
    )


# ----------------------------------------------------------------------- markdown


def render_md(cv: dict, lang: str) -> str:
    meta = cv["meta"]
    holes = find_holes(cv)
    out = [f"# {meta['nom']}", "", f"**{inline_md(meta['titre'])}**", ""]
    out += [f"*{inline_md(meta.get('cible', ''))}*", ""]
    out.append(" · ".join(inline_md(c) for c in meta.get("contact", [])))
    out.append("")
    if holes:
        warn = (
            f"> **{LABELS[lang]['draft']} — {len(holes)} {LABELS[lang]['holes']}.** "
            "Chaque `[[...]]` est un fait que seul Richard peut fournir. "
            "Voir `cv/README.md`."
        )
        out += [warn, ""]

    for key in ("profil",):
        block = cv.get(key)
        if block:
            out += [f"## {block['titre']}", "", inline_md(block["texte"]), ""]

    apport = cv.get("apport")
    if apport:
        out += [f"## {apport['titre']}", ""]
        out += [f"- **{inline_md(p['titre'])}.** {inline_md(p['texte'])}" for p in apport["puces"]]
        out.append("")

    comp = cv.get("competences")
    if comp:
        out += [f"## {comp['titre']}", ""]
        for g in comp["groupes"]:
            out += [f"**{inline_md(g['titre'])}** — {inline_md(g['items'])}", ""]

    exp = cv.get("experiences")
    if exp:
        out += [f"## {exp['titre']}", ""]
        for job in exp["entrees"]:
            out += [
                f"### {inline_md(job['poste'])} — {inline_md(job['org'])}",
                "",
                f"*{inline_md(job.get('lieu', ''))} · {inline_md(job.get('dates', ''))}*",
                "",
            ]
            if job.get("contexte"):
                out += [inline_md(job["contexte"]), ""]
            out += [f"- {inline_md(b)}" for b in job.get("puces", [])]
            if job.get("stack"):
                out += ["", f"Stack : {inline_md(job['stack'])}"]
            out.append("")

    ann = cv.get("annexes_liees")
    if ann:
        out += [f"## {ann['titre']}", "", inline_md(ann["texte"]), ""]

    for key in ("formation", "langues", "disponibilite"):
        block = cv.get(key)
        if block:
            out += [f"## {block['titre']}", ""]
            out += [f"- {inline_md(e)}" for e in block["entrees"]]
            out.append("")

    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------- rendering


def chrome() -> str | None:
    for name in CHROME_CANDIDATES:
        found = shutil.which(name)
        if found:
            return found
    return None


def run_chrome(args: list[str], expected: Path, timeout: float = 90.0) -> bool:
    """Chrome headless écrit le fichier puis ne rend pas toujours la main : on attend le
    fichier, on vérifie que sa taille s'est stabilisée, puis on coupe le processus."""
    expected.unlink(missing_ok=True)
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + timeout
    last_size = -1
    try:
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                break
            time.sleep(0.5)
            if expected.exists():
                size = expected.stat().st_size
                if size > 0 and size == last_size:
                    break
                last_size = size
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    return expected.exists() and expected.stat().st_size > 0


def to_pdf(html_path: Path, pdf_path: Path, png: bool) -> bool:
    binary = chrome()
    if not binary:
        print("  ! Chrome introuvable : PDF non généré (HTML et Markdown le sont)")
        return False
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        base = [
            binary,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-first-run",
            "--hide-scrollbars",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=4000",
        ]
        url = html_path.resolve().as_uri()
        ok = run_chrome(
            base + ["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", url], pdf_path
        )
        if not ok:
            print("  ! Chrome n'a pas produit de PDF")
            return False
        if png:
            shot = pdf_path.with_suffix(".png")
            run_chrome(base + ["--window-size=1240,1754", f"--screenshot={shot}", url], shot)
    return True


def build(lang: str, png: bool) -> list[tuple[str, str]]:
    cv = load(lang)
    holes = find_holes(cv)
    BUILD.mkdir(parents=True, exist_ok=True)

    stem = f"CV-RichardYI-{lang.upper()}"
    html_path = BUILD / f"{stem}.html"
    pdf_path = BUILD / f"{stem}.pdf"
    md_path = ROOT / "cv" / f"{stem}.md"

    html_path.write_text(render_html(cv, lang), encoding="utf-8")
    md_path.write_text(render_md(cv, lang), encoding="utf-8")
    print(f"[{lang}] {md_path.relative_to(ROOT)}")
    print(f"[{lang}] {html_path.relative_to(ROOT)}")
    if to_pdf(html_path, pdf_path, png):
        print(f"[{lang}] {pdf_path.relative_to(ROOT)}")
    return holes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("langs", nargs="*", help="fr, en, ou rien pour les deux")
    ap.add_argument("--strict", action="store_true", help="échouer s'il reste des [[trous]]")
    ap.add_argument("--png", action="store_true", help="générer aussi un PNG de la page 1")
    args = ap.parse_args()

    langs = args.langs or ["fr", "en"]
    unknown = [lang for lang in langs if lang not in ("fr", "en")]
    if unknown:
        ap.error(f"langue inconnue : {', '.join(unknown)}")
    remaining: dict[str, list[tuple[str, str]]] = {}
    for lang in langs:
        remaining[lang] = build(lang, args.png)

    total = sum(len(v) for v in remaining.values())
    if not total:
        print("\nAucun [[trou]] : version envoyable (relire quand même la règle de sincérité).")
        return 0

    print(f"\n{total} trou(s) à combler avant envoi :")
    for lang, holes in remaining.items():
        if not holes:
            continue
        print(f"\n  {lang} — {len(holes)}")
        for path, text in holes:
            short = text if len(text) <= 96 else text[:93] + "..."
            print(f"    · {path}: {short}")

    if args.strict:
        print("\n--strict : le CV n'est pas envoyable en l'état.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
