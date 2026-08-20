#!/usr/bin/env python3
"""Génère le deck McKinsey MedicalCity (HTML 16:9) puis le PDF via Chrome."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT / "docs/comex/deck.html"
OUT_PDF = ROOT / "docs/comex/MedicalCity-Comex-IA-ScaleUp.pdf"

CSS = r"""
:root {
  --navy: #0A1628;
  --navy-2: #12243C;
  --teal: #0E8A80;
  --teal-dk: #0A5F58;
  --gold: #C4A574;
  --paper: #F6F4EF;
  --ink: #1B2430;
  --muted: #5C6B73;
  --line: #D9D3C7;
  --white: #FFFFFF;
  --red: #9B2C2C;
  --ok: #1F7A4D;
  --warn: #B45309;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #111; }
body {
  font-family: "Liberation Sans", "Segoe UI", Helvetica, Arial, sans-serif;
  color: var(--ink);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
@page { size: 1280px 720px; margin: 0; }
.slide {
  width: 1280px; height: 720px; background: var(--white);
  padding: 36px 52px 52px;
  position: relative; overflow: hidden;
  page-break-after: always; break-after: page;
}
.slide:last-child { page-break-after: auto; break-after: auto; }
.slide.dark { background: var(--navy); color: var(--paper); }
.topbar {
  position: absolute; top: 0; left: 0; right: 0; height: 6px;
  background: linear-gradient(90deg, var(--teal) 0 72%, var(--gold) 72% 100%);
}
.eyebrow {
  font-size: 11px; letter-spacing: .16em; text-transform: uppercase;
  color: var(--teal-dk); font-weight: 700; margin: 10px 0 8px;
}
.dark .eyebrow { color: var(--gold); }
h1.action {
  font-size: 26px; line-height: 1.28; font-weight: 700; color: var(--navy);
  margin: 0 0 18px; max-width: 1120px; letter-spacing: -.01em;
}
.dark h1.action { color: var(--paper); font-size: 34px; max-width: 920px; }
.sub { font-size: 15px; color: var(--muted); margin: -8px 0 18px; }
.footer {
  position: absolute; left: 52px; right: 52px; bottom: 16px;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10px; color: var(--muted); border-top: 1px solid var(--line);
  padding-top: 8px; letter-spacing: .04em;
}
.dark .footer { border-top-color: #2A3D55; color: #9AA8B5; }
.brand { font-weight: 700; color: var(--navy); letter-spacing: .12em; }
.dark .brand { color: var(--gold); }
.grid { display: grid; gap: 12px; }
.g2 { grid-template-columns: 1fr 1fr; }
.g3 { grid-template-columns: 1fr 1fr 1fr; }
.g4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.g7 { grid-template-columns: repeat(7, 1fr); }
.card {
  background: var(--paper); border: 1px solid var(--line); border-radius: 4px;
  padding: 12px 14px;
}
.card h3 { margin: 0 0 6px; font-size: 13px; color: var(--navy); }
.card p, .card li { font-size: 12.5px; line-height: 1.4; margin: 0; color: var(--ink); }
.card.teal { background: #E7F4F2; border-color: #B7DED9; }
.card.navy { background: var(--navy); color: var(--paper); border: 0; }
.card.navy h3, .card.navy p { color: var(--paper); }
.kpi {
  background: var(--paper); border-top: 3px solid var(--teal); padding: 10px 12px;
}
.kpi .v { font-size: 22px; font-weight: 700; color: var(--navy); line-height: 1.1; }
.kpi .l { font-size: 11px; color: var(--muted); margin-top: 4px; line-height: 1.3; }
table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
th { text-align: left; font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
     color: var(--muted); border-bottom: 1px solid var(--navy); padding: 6px 8px; }
td { border-bottom: 1px solid var(--line); padding: 7px 8px; vertical-align: top; line-height: 1.35; }
tr:nth-child(even) td { background: #FAF8F4; }
ul.tight { margin: 0; padding-left: 16px; }
ul.tight li { margin: 0 0 4px; font-size: 13px; line-height: 1.4; }
.pill { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: .06em;
        text-transform: uppercase; padding: 2px 7px; border-radius: 2px; }
.p-auto { background: #D1FAE5; color: var(--ok); }
.p-rec { background: #FEF3C7; color: var(--warn); }
.p-man { background: #FEE2E2; color: var(--red); }
.so {
  margin-top: 12px; background: var(--navy); color: var(--paper);
  padding: 10px 14px; font-size: 13px; line-height: 1.4;
}
.so strong { color: var(--gold); }
.num {
  display: inline-flex; width: 22px; height: 22px; align-items: center; justify-content: center;
  background: var(--teal); color: white; font-size: 11px; font-weight: 700; border-radius: 2px;
  margin-right: 6px;
}
.flow { display: flex; gap: 8px; align-items: stretch; }
.flow .step { flex: 1; background: var(--paper); border: 1px solid var(--line); padding: 10px; }
.flow .arr { display: flex; align-items: center; color: var(--teal); font-weight: 700; }
.tiny { font-size: 11px; color: var(--muted); line-height: 1.35; }
.cover-meta { position: absolute; bottom: 70px; left: 52px; right: 52px; color: #C5D0DA; font-size: 13px; }
.rule { height: 2px; width: 88px; background: var(--gold); margin: 18px 0 22px; }
.toc-row { display: flex; justify-content: space-between; border-bottom: 1px solid var(--line);
           padding: 8px 0; font-size: 15px; }
.toc-row span { color: var(--teal-dk); font-weight: 700; }
.seat { text-align: left; min-height: 148px; }
.seat .code { font-size: 10px; letter-spacing: .14em; color: var(--teal-dk); font-weight: 700; }
.seat h3 { font-size: 13px; margin: 4px 0 6px; }
.rag { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.r { background: #C4A574; } .a { background: var(--warn); } .g { background: var(--ok); }
.bar { height: 8px; background: #E8E4DA; border-radius: 4px; overflow: hidden; }
.bar > i { display: block; height: 100%; background: var(--teal); }
"""


def footer(source: str = "Sources : medicalcity.ai ; CNSA 2026 ; RCS Paris") -> str:
    return f"""<div class="footer">
      <span class="brand">MEDICALCITY</span>
      <span>STRICTEMENT CONFIDENTIEL  ·  Comex IA &amp; scale-up  ·  août 2026</span>
      <span>{source}</span>
    </div>"""


def slide(inner: str, dark: bool = False) -> str:
    cls = "slide dark" if dark else "slide"
    return f'<section class="{cls}"><div class="topbar"></div>{inner}</section>'


def build_slides() -> list[str]:
    s: list[str] = []

    s.append(slide(f"""
      <div class="eyebrow">Document de travail  ·  Président</div>
      <div style="height:72px"></div>
      <div style="font-size:13px;letter-spacing:.28em;color:var(--gold);font-weight:700">MEDICALCITY</div>
      <h1 class="action" style="font-size:42px;margin-top:12px">Organiser le Comex d'agents IA exécutifs<br>et scaler la société.</h1>
      <div class="rule"></div>
      <p style="font-size:18px;color:#C5D0DA;max-width:820px;line-height:1.45">
        Architecture de gouvernance · 7 sièges · 12 sujets scale-up · feuille de route 18 mois.
      </p>
      <div class="cover-meta">
        SASU RCS Paris 107 542 565  ·  66 avenue des Champs-Élysées  ·  20 août 2026<br>
        Destinataire : Richard YI, Président  ·  Copie : Sreypov UM, Care &amp; field
      </div>
      {footer("Livrable interne — ne pas diffuser")}
    """, dark=True))

    s.append(slide(f"""
      <div class="eyebrow">01  —  Intention</div>
      <h1 class="action">Ce document répond à trois questions du Président — pas à un exercice d'organigramme.</h1>
      <div class="grid g3">
        <div class="card navy">
          <h3>1. Comment organiser le « CA / Comex » ?</h3>
          <p>En SASU, le Président est le seul organe social. Le Comex d'agents est opérationnel, pas fiduciaire. Un CA formel se justifie à la levée, pas avant.</p>
        </div>
        <div class="card">
          <h3>2. Quelle architecture d'agents ?</h3>
          <p>7 sièges MECE orchestrés par l'AGE, framework SMCI, protocoles MCP/A2A, HITL calé sur Bayon (AUTO / RECOMMENDED / MANDATORY).</p>
        </div>
        <div class="card teal">
          <h3>3. Quels sujets pour scaler ?</h3>
          <p>12 sujets, 4 chantiers : PMF, GTM institutionnel, Trust (HDS/AI Act), Capital &amp; org. Tout le reste est un stop-doing jusqu'au pilote CD77.</p>
        </div>
      </div>
      <div class="so"><strong>So what.</strong> MedicalCity peut opérer comme une scale-up dès maintenant : le Comex IA est l'effet de levier du fondateur, pas un organigramme fantôme. Les prompts, la charte et ce PDF sont le système d'exploitation — pas un slideware.</div>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">02  —  Messages clés</div>
      <h1 class="action">Six convictions pour gouverner une SASU AI-native sans diluer la responsabilité du Président.</h1>
      <ol style="margin:0;padding-left:22px;font-size:15px;line-height:1.55">
        <li style="margin-bottom:8px"><strong>Séparer le pouvoir de signer du pouvoir d'exécuter.</strong> Les agents préparent, chiffrent, rédigent. L'humain signe. Aucun agent n'est organe social.</li>
        <li style="margin-bottom:8px"><strong>Sept sièges, pas quinze.</strong> Produit, Clinique, Finance, GTM, Ops, Stratégie, plus l'AGE. Les agents métier (APA, Bayon, drones) ne votent pas.</li>
        <li style="margin-bottom:8px"><strong>HITL identique à Bayon.</strong> AUTO / RECOMMENDED / MANDATORY — même langage du MDM au Comex, journal WORM sur le critique.</li>
        <li style="margin-bottom:8px"><strong>Le wedge dicte l'agenda.</strong> Agent APA + RaaS, LOI CD77, pilote Q1 2027. Les drones ne sont pas le chemin critique 2026.</li>
        <li style="margin-bottom:8px"><strong>Le capital suit la preuve, pas l'inverse.</strong> Tour seed 5 M€ pour le PMF. Recrutements humains seniors post-traction.</li>
        <li><strong>Mémoire unique dans Git.</strong> Packs, décisions, risques versionnés. Pas de Comex dans des chats éphémères.</li>
      </ol>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">03  —  Situation</div>
      <h1 class="action">MedicalCity est incorporée, le wedge est identifié, la preuve institutionnelle a commencé — l'entreprise n'a pas encore de Comex instrumenté.</h1>
      <div class="grid g4" style="margin-bottom:14px">
        <div class="kpi"><div class="v">07 / 2026</div><div class="l">SASU Paris · SIREN 107 542 565 · NAF 5829C · capital 1 299 €</div></div>
        <div class="kpi"><div class="v">LOI CD77</div><div class="l">Seine-et-Marne · pilote Q1 2027 · codes APA mappés · modèle tripartite</div></div>
        <div class="kpi"><div class="v">205</div><div class="l">Pré-réservations robots RaaS (source dirigeant, août 2026)</div></div>
        <div class="kpi"><div class="v">5 M€</div><div class="l">Tour seed visé pour le product-market fit (thèse medicalcity.ai)</div></div>
      </div>
      <div class="grid g2">
        <div class="card">
          <h3>Ce qui est déjà vrai</h3>
          <ul class="tight">
            <li>Quatre piliers publics : plateforme, agents, drones, robots.</li>
            <li>Bayon — MDM agentique FHIR R4, golden record &lt; 30 s, 281 tests CI.</li>
            <li>Wedge : Agent APA HITL, payeur public (branche Autonomie).</li>
            <li>RaaS : 350–750 €/mois, GM cible 70–75 %, LTV/CAC visé &gt; 5×.</li>
            <li>Modèle opérant AI-native : essaims d'agents, hires humains post-seed.</li>
            <li>Membre Claude for Startups (Anthropic).</li>
          </ul>
        </div>
        <div class="card">
          <h3>Ce qui n'est pas encore vrai</h3>
          <ul class="tight">
            <li>Pas d'organe exécutif cadencé (packs, RACI, journal de décisions).</li>
            <li>HDS : intention « ready », dossier non lancé.</li>
            <li>Comité médical nommé mais pas encore institutionnalisé.</li>
            <li>LOI ≠ convention de pilote ≠ premier euro d'ARR.</li>
            <li>Quatre piliers créent un risque de dispersion avant le PMF.</li>
            <li>Span of control du Président saturé (produit, GTM, levée, care).</li>
          </ul>
        </div>
      </div>
      {footer("Sources : medicalcity.ai ; annonce légale 13/07/2026 ; LinkedIn R. YI")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">04  —  Complication</div>
      <h1 class="action">Sans Comex instrumenté, le Président est le goulot unique sur quatre marchés à cycle long.</h1>
      <div class="grid g4">
        <div class="card"><h3>1. Span of control</h3><p>Plateforme + APA + RaaS + drones + levée + CD77. Un humain ne tient pas un Comex de scale-up 18 h par jour. Les agents existent déjà — ils ne siègent pas.</p></div>
        <div class="card"><h3>2. Trust stack</h3><p>RGPD, HDS, AI Act (risque élevé probable), MDR/ANSM robots, OTA, claims. Un incident P1 sans war-room tue la thèse institutionnelle.</p></div>
        <div class="card"><h3>3. GTM B2G</h3><p>Cycle départemental : élu, DGA solidarités, équipe AGGIR, finances. Playbook non encore reproductible au-delà de 77.</p></div>
        <div class="card"><h3>4. Capital vs capex</h3><p>SASU à 1 299 € vs industrialisation RaaS. Le seed finance le PMF, pas les quatre piliers en parallèle.</p></div>
      </div>
      <div class="card teal" style="margin-top:12px">
        <h3>Implication pour le design du Comex</h3>
        <p>Chaque siège doit <strong>réduire une contrainte</strong>, pas « avoir un VP ». Produit accélère Bayon/APA. Care tient le droit d'opérer. GTM industrialise le département. Ops rend le pilote exécutable. CFO rend l'entreprise finançable. Strat empêche la dispersion. L'AGE libère le Président des interfaces.</p>
      </div>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">05  —  Recommandation</div>
      <h1 class="action">Adopter en 30 jours une gouvernance duale : humains pour le légal, agents pour l'exécution, Board humain à la levée.</h1>
      <div class="grid g3">
        <div class="card navy">
          <h3>Volet A — Pouvoir légal (humain)</h3>
          <p>Président SASU : signature, représentation, responsabilité pénale, contrats, levée, veto. Care &amp; field (Sreypov UM) : qualité terrain, contenu, ops care. Aucune délégation statutaire aux agents.</p>
        </div>
        <div class="card teal">
          <h3>Volet B — Pouvoir d'exécution (Comex IA)</h3>
          <p>7 sièges + AGE. Cadence hebdo 90 min. Packs Git. HITL Bayon. Décisions AUTO / RECOMMENDED / MANDATORY. Mémoire unique. Multi-vendor, pas de lock-in modèle.</p>
        </div>
        <div class="card">
          <h3>Volet C — Board (humain, post-seed)</h3>
          <p>3 à 5 sièges : Président + 1 indépendant santé + 1 indépendant payeur public + 1 investisseur. Pas de CA statutaire avant la levée — complexité sans protection.</p>
        </div>
      </div>
      <table style="margin-top:16px">
        <tr><th>Ne pas faire</th><th>Pourquoi</th><th>Faire à la place</th></tr>
        <tr><td>Créer un « CA d'IA » dans les statuts</td><td>Un agent n'a pas la personnalité juridique</td><td>Charte Comex + journal de décisions signé par le Président</td></tr>
        <tr><td>Recruter 7 VP humains maintenant</td><td>Brûle le seed avant le PMF</td><td>2–3 seniors post-traction (clinique, CFO, public affairs)</td></tr>
        <tr><td>Laisser le Comex dans le chat</td><td>Pas d'audit, pas de WORM, pas de reprise</td><td>Dépôt Git = livre de gouvernance</td></tr>
      </table>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">06  —  Cartographie des instances</div>
      <h1 class="action">Le Comex IA s'insère sous le Président ; il ne se substitue à aucun organe social ni à aucun régulateur.</h1>
      <table>
        <tr><th>Instance</th><th>Nature</th><th>Membres</th><th>Rythme</th><th>Pouvoir réel</th></tr>
        <tr><td>Associé unique</td><td>Légale</td><td>Richard YI</td><td>Ad hoc</td><td>Statuts, comptes, transformation</td></tr>
        <tr><td>Président</td><td>Légale</td><td>Richard YI</td><td>Continu</td><td>Signature, représentation, veto</td></tr>
        <tr><td><strong>Comex IA</strong></td><td>Opérationnelle</td><td>7 agents + Président</td><td>Hebdo 90 min</td><td>AUTO + recommandations</td></tr>
        <tr><td>Comité Qualité &amp; IA</td><td>Réglementaire</td><td>CARE + Care humain + médecins</td><td>Mensuel</td><td>Protocoles, incidents, claims</td></tr>
        <tr><td>Comité Risques</td><td>Réglementaire</td><td>CFO + CARE + Président</td><td>Mensuel</td><td>Cash, HDS, AI Act, contrats</td></tr>
        <tr><td>Comité stratégique / Board</td><td>Fiduciaire</td><td>Humains (post-seed)</td><td>Trimestriel</td><td>Levée, stratégie 18–36 mois</td></tr>
        <tr><td>Fondation 1 %</td><td>Sociétale</td><td>Président</td><td>Annuel</td><td>1 % du résultat net</td></tr>
      </table>
      <p class="tiny" style="margin-top:10px">Les agents métier (APA, Bayon, RaaS-config, drones, IR, DPO) livrent aux sièges ; ils n'ont pas voix au Comex. Un DPO humain et un comité médical restent non substituables.</p>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">07  —  Architecture cible</div>
      <h1 class="action">Cinq couches, une intention : l'AGE traduit la volonté du Président ; jamais l'inverse.</h1>
      <div class="flow" style="height:92px;margin-bottom:12px">
        <div class="step" style="background:var(--navy);color:#F6F4EF"><strong>L0 Humains</strong><br><span class="tiny" style="color:#C5D0DA">Intention · veto · signature</span></div>
        <div class="arr">→</div>
        <div class="step" style="background:#0E8A80;color:white"><strong>L1 AGE-COMEX</strong><br><span class="tiny" style="color:#E7F4F2">Agenda · synthèse · A2A</span></div>
        <div class="arr">→</div>
        <div class="step"><strong>L2 Six sièges métier</strong><br><span class="tiny">PLAT CARE CFO GTM OPS STRAT</span></div>
        <div class="arr">→</div>
        <div class="step"><strong>L3 Agents métier</strong><br><span class="tiny">APA · Bayon · RaaS · IR · DPO</span></div>
        <div class="arr">→</div>
        <div class="step"><strong>L4 Systèmes</strong><br><span class="tiny">FHIR · HDS · site · data room</span></div>
      </div>
      <div class="grid g3">
        <div class="card">
          <h3>Alignement 4 piliers</h3>
          <p>PLAT = cerveau (FL, Bayon). GTM+APA = personnel numérique. OPS drones = logistique (hors chemin critique). OPS robots = RaaS 24/7. CARE = couche 1 Confiance (ZKP, consentement, AI Act).</p>
        </div>
        <div class="card">
          <h3>Contrats d'interface</h3>
          <p><strong>MCP</strong> : outils (Git, data room, CRM). <strong>A2A</strong> : l'AGE convoque, les sièges répondent en 1 page. <strong>WORM</strong> : décisions MANDATORY hashées, même standard que Bayon.</p>
        </div>
        <div class="card">
          <h3>SMCI (GEOVTC)</h3>
          <p><strong>Skills</strong> versionnées. <strong>Memory</strong> = ce dépôt. <strong>Context</strong> = pack de la semaine + OKR. <strong>Identity</strong> = fichier <em>comex/agents/*.md</em>. Transférable, auditable, sans lock-in.</p>
        </div>
      </div>
      {footer("Méthode AGE : Understand → Design → Build → Verify → Operate → Capitalize")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">08  —  Les 7 sièges</div>
      <h1 class="action">Chaque siège réduit une contrainte de scale-up — pas un titre pour occuper une case.</h1>
      <div class="grid g7">
        <div class="card seat navy"><div class="code" style="color:var(--gold)">AGE</div><h3 style="color:#fff">Orchestration</h3><p>Agenda, conflits d'interface, pack pyramidal. N'auto-valide jamais.</p></div>
        <div class="card seat"><div class="code">PLAT</div><h3>Produit</h3><p>Bayon, AGE Factory, FL, backlog APA. KPI : golden record, CI, skills réutilisées.</p></div>
        <div class="card seat"><div class="code">CARE</div><h3>Clinique</h3><p>HDS, AI Act, MDR, claims, incidents. Veto de facto sur le public. Sponsor : S. UM.</p></div>
        <div class="card seat"><div class="code">CFO</div><h3>Finance</h3><p>Runway, unit eco RaaS, data room, seuils CAPEX. Zéro ARR non contracté.</p></div>
        <div class="card seat"><div class="code">GTM</div><h3>Institutions</h3><p>Départements, LOI, APA GIR 1–4, pré-réservations. Playbook reproductible.</p></div>
        <div class="card seat"><div class="code">OPS</div><h3>Physique</h3><p>Flotte, SLA 24/7, opérateurs, runbook CD77. COGS réels vers CFO chaque semaine.</p></div>
        <div class="card seat"><div class="code">STRAT</div><h3>Scale-up</h3><p>12 sujets, stop-doing, Europe après PMF FR. Empêche la dispersion 4 piliers.</p></div>
      </div>
      <p class="tiny" style="margin-top:12px">Sponsor humain par défaut : Richard YI (AGE, PLAT, CFO, GTM, STRAT) · Sreypov UM (CARE, OPS). Les sièges sont des rôles ; un humain peut en tenir deux, un agent n'en tient qu'un.</p>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">09  —  Droits de décision</div>
      <h1 class="action">Le langage HITL de Bayon devient la constitution du Comex : trois niveaux, zéro zone grise.</h1>
      <table>
        <tr><th></th><th>AUTO <span class="pill p-auto">audit a posteriori</span></th><th>RECOMMENDED <span class="pill p-rec">oui sous 48 h</span></th><th>MANDATORY <span class="pill p-man">signature humaine</span></th></tr>
        <tr><td><strong>AGE</strong></td><td>CR, agenda, consolidation packs</td><td>Arbitrage d'interface entre sièges</td><td>Toute communication « au nom du Comex »</td></tr>
        <tr><td><strong>PLAT</strong></td><td>Backlog, CI, ADRs non breaking</td><td>Epic nouveau, dette vs feature</td><td>Branchement données de santé, claims produit</td></tr>
        <tr><td><strong>CARE</strong></td><td>Veille réglementaire, registre</td><td>Classification AI Act d'un flux</td><td>Protocole, DPA, incident P1, claim public</td></tr>
        <tr><td><strong>CFO</strong></td><td>Flash cash, MAJ modèle</td><td>Pricing hors grille, usage of proceeds</td><td>Term-sheet, CAPEX &gt; 10 k€, engagement &gt; 12 mois</td></tr>
        <tr><td><strong>GTM</strong></td><td>Relances, one-pagers, pipeline</td><td>Séquence d'un nouveau département</td><td>LOI, convention, tarifs opposables, presse</td></tr>
        <tr><td><strong>OPS</strong></td><td>Runbook, tickets, formation</td><td>Choix opérateur, n sites pilote</td><td>Go-live domicile, SLA contractuel</td></tr>
      </table>
      <div class="so"><strong>Règle d'or.</strong> Le silence n'est pas un accord. L'AGE n'auto-valide pas. En cas de conflit, 3 options — jamais une moyenne. Données de santé : hors Git, hors prompts Comex.</div>
      {footer("Calé sur Bayon : AUTO / RECOMMENDED / MANDATORY + journal WORM")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">10  —  Cadence</div>
      <h1 class="action">Une heure et demie par semaine suffit si chaque siège arrive avec une page, pas un récit.</h1>
      <div class="grid g2">
        <div>
          <table>
            <tr><th>Rituel</th><th>Durée</th><th>Owner</th><th>Livrable</th></tr>
            <tr><td>Standup ops</td><td>15 min / j</td><td>OPS</td><td>standup.md</td></tr>
            <tr><td><strong>Comex</strong></td><td>90 min / sem</td><td>AGE</td><td>packs/YYYY-Www.md</td></tr>
            <tr><td>Qualité &amp; IA</td><td>60 min / mois</td><td>CARE</td><td>quality/YYYY-MM.md</td></tr>
            <tr><td>Risques</td><td>60 min / mois</td><td>CFO</td><td>risk/YYYY-MM.md</td></tr>
            <tr><td>Stratégie</td><td>½ journée / trim.</td><td>STRAT</td><td>strategy/YYYY-Qn.md</td></tr>
          </table>
          <p class="tiny" style="margin-top:8px">Quorum Comex : AGE + 4 sièges + Président (async 24 h accepté). Pack J-1 obligatoire — pas de « je vous raconte ».</p>
        </div>
        <div class="card">
          <h3>Ordre du jour type (90 min)</h3>
          <ul class="tight">
            <li><strong>0–10</strong> Faits + 5 KPI flash</li>
            <li><strong>10–25</strong> PMF — APA, Bayon, pilote CD77</li>
            <li><strong>25–40</strong> GTM — pipeline, pré-réservations</li>
            <li><strong>40–55</strong> Trust — HDS, AI Act, incidents</li>
            <li><strong>55–70</strong> Capital — runway, data room, tour</li>
            <li><strong>70–80</strong> Décisions MANDATORY à signer</li>
            <li><strong>80–90</strong> OKR, risques, J+7</li>
          </ul>
          <p class="tiny" style="margin-top:8px">Parking lot pour tout hors des 12 sujets. Facilitation AGE : une recommandation par item.</p>
        </div>
      </div>
      {footer("Playbook : comex/playbooks/comex-hebdo.md")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">11  —  Agenda scale-up</div>
      <h1 class="action">Douze sujets MECE, quatre chantiers : si un thème n'entre pas ici, c'est un stop-doing jusqu'au PMF.</h1>
      <div class="grid g4">
        <div class="card navy"><h3>A · Product-market fit</h3>
          <p>1. Convertir la LOI CD77 en convention de pilote Q1 2027.<br>
          2. Industrialiser l'Agent APA HITL (GIR 1–4, 2026).<br>
          3. Brancher Bayon sur ≥ 1 source institutionnelle.</p></div>
        <div class="card teal"><h3>B · GTM institutionnel</h3>
          <p>4. Playbook département reproductible (cible : 5 LOI).<br>
          5. Verrouiller le modèle tripartite (actif / opérateur / APA).<br>
          6. Canal opérateurs SAD / EHPAD — sans cannibaliser 77.</p></div>
        <div class="card"><h3>C · Trust &amp; droit d'opérer</h3>
          <p>7. Lancer le dossier HDS (hébergeur, GAP, clés).<br>
          8. Registre AI Act vivant + evals documentées.<br>
          9. Comité médical + matériovigilance robots / OTA.</p></div>
        <div class="card"><h3>D · Capital &amp; organisation</h3>
          <p>10. Data room seed 5 M€, usage of proceeds 4 buckets.<br>
          11. Unit economics RaaS avec COGS réels (pas cibles).<br>
          12. Plan de hires humains post-traction — pas avant.</p></div>
      </div>
      <div class="so"><strong>Séquence.</strong> A débloque B. C débloque le B2G sérieux. D finance A+C. Les drones, l'EU et la Fondation sont des options Horizon 2 — STRAT les garde au parking jusqu'à go pilote.</div>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">12  —  Deep dive PMF</div>
      <h1 class="action">Le pilote Seine-et-Marne est la seule preuve qui convertit une thèse en contrat — tout le Comex lui est subordonné.</h1>
      <div class="grid g2">
        <div class="card">
          <h3>Chemin contractuel</h3>
          <div class="flow" style="margin-top:8px">
            <div class="step"><strong>LOI</strong><br><span class="tiny">Signée · CD77</span></div>
            <div class="arr">→</div>
            <div class="step"><strong>Convention</strong><br><span class="tiny">Périmètre, n sites, SLA</span></div>
            <div class="arr">→</div>
            <div class="step"><strong>Go-live Q1 27</strong><br><span class="tiny">HITL + incident 24/7</span></div>
            <div class="arr">→</div>
            <div class="step"><strong>ARR</strong><br><span class="tiny">Loyer APA + RAC</span></div>
          </div>
          <p style="margin-top:10px;font-size:13px">Kill-criteria J45 : pas de chemin contractuel identifiable → recentrer GTM et geler le narratif investisseur « pilote signé ».</p>
        </div>
        <div class="card">
          <h3>APA 2026 — plafonds à domicile (opposables)</h3>
          <table>
            <tr><th>GIR</th><th>Plafond mensuel</th><th>Implication RaaS</th></tr>
            <tr><td>1</td><td>2 080,33 €</td><td>Loyer 350–750 € tient dans le plan d'aide</td></tr>
            <tr><td>2</td><td>1 682,30 €</td><td>Idem, RAC famille à modéliser</td></tr>
            <tr><td>3</td><td>1 215,99 €</td><td>Arbitrage aide humaine vs RaaS</td></tr>
            <tr><td>4</td><td>811,52 €</td><td>RaaS entrée de gamme seulement</td></tr>
          </table>
          <p class="tiny" style="margin-top:6px">L'APA n'est pas un chèque robot : elle finance un plan d'aide AGGIR. GTM + CARE doivent écrire le libellé opposable avec le département.</p>
        </div>
      </div>
      {footer("Sources : CNSA tarifs APA 1er jan. 2026 ; medicalcity.ai (LOI CD77)")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">13  —  Deep dive capital</div>
      <h1 class="action">Le seed de 5 M€ achète 18 mois de PMF — pas l'industrialisation des quatre piliers.</h1>
      <div class="grid g2">
        <div>
          <table>
            <tr><th>Bucket</th><th>%</th><th>À quoi ça sert</th></tr>
            <tr><td>PMF produit (Bayon, APA, pilote)</td><td>40 %</td><td>Ingénierie, sites pilotes, AGE Factory</td></tr>
            <tr><td>Trust (HDS, AI Act, clinique)</td><td>20 %</td><td>Droit d'opérer B2G</td></tr>
            <tr><td>GTM départements + ops terrain</td><td>25 %</td><td>Playbook, opérateurs, flotte minimale</td></tr>
            <tr><td>Runway &amp; G&amp;A</td><td>15 %</td><td>Juridique, DPO, data room, 18 mois</td></tr>
          </table>
          <p class="tiny" style="margin-top:8px">Répartition indicative à valider par CFO — ordre de grandeur pour discipliner les demandes de chaque siège.</p>
        </div>
        <div class="card">
          <h3>Unit economics — hypothèses maison à éprouver</h3>
          <ul class="tight">
            <li>Loyer RaaS <strong>350–750 €/mois</strong> · 36–60 mois</li>
            <li>GM cible <strong>70–75 %</strong> après COGS opérateur</li>
            <li>Payback robot <strong>18–24 mois</strong> · LTV/CAC &gt; 5×</li>
            <li>Churn annuel cible <strong>&lt; 5 %</strong> (dépendance fonctionnelle)</li>
            <li>Comparatif : auxiliaire ~27 k€/an partiel vs RaaS 4,2–9 k€/an 24/7</li>
          </ul>
          <p class="tiny" style="margin-top:8px">CFO n'affiche un ARR que contracté. Les 205 pré-réservations sont un indicateur d'intérêt, pas un backlog de revenus.</p>
        </div>
      </div>
      <div class="so"><strong>Payeur public, à sourcer juste.</strong> Branche Autonomie CNSA 2026 : <strong>44,45 Md€</strong>. Concours aux départements : <strong>6,3 Md€</strong> (série 2024 : 5,4 Md€ — le chiffre site est la série, pas le budget 2026). Ne pas sur-vendre « 5,4 Md€ d'APA » à un investisseur.</div>
      {footer("Sources : CNSA Chiffres clés 2026 ; thèse medicalcity.ai")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">14  —  Feuille de route 18 mois</div>
      <h1 class="action">Trois horizons : gouverner maintenant, prouver au Q1 2027, n'industrialiser l'Europe qu'après.</h1>
      <table>
        <tr><th></th><th>H0 · 90 jours (nov. 2026)</th><th>H1 · Q1 2027 — PMF</th><th>H2 · S2 2027 — scale FR</th></tr>
        <tr><td><strong>Gouvernance</strong></td><td>Charte signée, 7 agents live, 12 Comex tenus</td><td>Comité médical + DPO humain</td><td>Board seed (3–5 humains)</td></tr>
        <tr><td><strong>Produit</strong></td><td>APA HITL documenté, plan Bayon</td><td>1 source FHIR live, Agent APA réel</td><td>FL v3.0 spécifié pour 1 cluster</td></tr>
        <tr><td><strong>GTM</strong></td><td>Convention CD77 rédigée, 5 one-pagers</td><td>Pilote live, 2 LOI de plus</td><td>5 départements, playbook figé</td></tr>
        <tr><td><strong>Ops</strong></td><td>Runbook, go/no-go, canal 24/7</td><td>n sites 77, uptime contractuel</td><td>Coût du site n ≪ site 1</td></tr>
        <tr><td><strong>Trust</strong></td><td>HDS lancé, registre AI Act</td><td>GAP HDS clos à 80 %, 0 P1 ouvert</td><td>HDS obtenu ou calendrier opposable</td></tr>
        <tr><td><strong>Capital</strong></td><td>Data room v1, unit eco versionnés</td><td>Term-sheet ou go/no-go tour</td><td>Seed clos, hires seniors</td></tr>
      </table>
      <p class="tiny" style="margin-top:10px">Hors scope H0–H1 : drones en production, expansion BE/LU/DE, Fondation opérationnelle, CA statutaire. STRAT tient la liste stop-doing à chaque Comex.</p>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">15  —  Plan 90 jours</div>
      <h1 class="action">J0 = signature de la charte. J90 = entreprise gouvernée, pilote contractable, seed racontable sans mensonge.</h1>
      <div class="grid g3">
        <div class="card navy">
          <h3>J0–J15 · Gouverner</h3>
          <p>Signer la charte. Instancier les 7 prompts. Premier Comex : valider les 12 sujets et le stop-doing drones. Ouvrir registres décisions / risques / qualité. LOI Comité médical (2–3 cliniciens).</p>
        </div>
        <div class="card teal">
          <h3>J16–J45 · Contractable</h3>
          <p>Projet de convention CD77. Runbook OPS go/no-go. Parcours APA HITL + mapping GIR. Plan de branchement Bayon. Data room sans donnée de santé. Kill-criteria : pas de chemin 77 → recentrer.</p>
        </div>
        <div class="card">
          <h3>J46–J90 · Finançable</h3>
          <p>Dossier HDS lancé. Registre AI Act vivant. 5 one-pagers départements. Narrative seed 4 buckets. Revue J90 : drones kill/continue, hires oui/non, go pilote.</p>
        </div>
      </div>
      <table style="margin-top:14px">
        <tr><th>Kill-criteria (arrêt ou recentrage)</th><th>Owner qui alerte</th></tr>
        <tr><td>Pas de chemin contractuel CD77 à J45</td><td>GTM + STRAT</td></tr>
        <tr><td>Unit economics non soutenables après COGS opérateurs réels</td><td>CFO + OPS</td></tr>
        <tr><td>Claim clinique non défendable devant un comité médical</td><td>CARE</td></tr>
        <tr><td>Runway &lt; 6 mois sans term-sheet</td><td>CFO</td></tr>
      </table>
      {footer("Détail : comex/playbooks/90-jours.md")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">16  —  Risques</div>
      <h1 class="action">Cinq risques peuvent tuer la thèse plus vite qu'un retard produit — le Comex les possède nommément.</h1>
      <table>
        <tr><th>#</th><th>Risque</th><th>Signal précoce</th><th>Mitigation Comex</th><th>Owner</th></tr>
        <tr><td>R1</td><td>Dispersion 4 piliers avant PMF</td><td>Backlog drones &gt; APA</td><td>Stop-doing STRAT, veto AGE</td><td>STRAT</td></tr>
        <tr><td>R2</td><td>Claim médical / device trop tôt</td><td>Copy site, LinkedIn, pitch</td><td>Veto CARE, Comité médical</td><td>CARE</td></tr>
        <tr><td>R3</td><td>LOI prise pour un contrat</td><td>Narratif investisseur en avance</td><td>CFO : ARR = contracté seulement</td><td>CFO</td></tr>
        <tr><td>R4</td><td>Donnée de santé dans un prompt</td><td>Pack Comex nominatif</td><td>Interdiction Git/prompts ; Bayon only</td><td>CARE</td></tr>
        <tr><td>R5</td><td>Agent « signe » ou parle en externe</td><td>Mail auto, tarif opposable</td><td>MANDATORY + identité claire non-humaine</td><td>AGE</td></tr>
      </table>
      <div class="grid g2" style="margin-top:12px">
        <div class="card"><h3>Risque juridique spécifique</h3><p>Un Comex d'IA n'exonère pas le Président. Responsabilité civile, pénale, AI Act (opérateur), RGPD (responsable de traitement) restent humains. La charte le dit en page 1 — à relire avant chaque claim « autonomous healthcare ».</p></div>
        <div class="card teal"><h3>Garde-fou opératoire</h3><p>Séparation des pouvoirs : l'AGE ne vérifie pas ses propres livrables. CARE peut bloquer GTM. CFO peut bloquer un go-live non financé. Le Président tranche les impasses, il ne les moyenne pas.</p></div>
      </div>
      {footer()}
    """))

    s.append(slide(f"""
      <div class="eyebrow">17  —  Comment l'instancier cette semaine</div>
      <h1 class="action">Le dépôt Git est déjà la salle du Comex : un prompt par siège, une mémoire partagée, un orchestrateur.</h1>
      <div class="grid g2">
        <div class="card">
          <h3>Mode opératoire recommandé (Cursor / Claude)</h3>
          <ul class="tight">
            <li>1 agent Cloud (ou Project) par siège, system prompt = <em>comex/agents/*.md</em></li>
            <li>AGE seul habilité à lancer les autres (A2A / @-mentions)</li>
            <li>Écriture limitée à <em>packs/</em>, <em>decisions/</em>, <em>risk/</em>, <em>quality/</em></li>
            <li>Modèle choisi par tâche (capacité, coût, souveraineté, résilience)</li>
            <li>Comex du vendredi : AGE consolide, Président commente, MANDATORY signés</li>
          </ul>
        </div>
        <div class="card navy">
          <h3>Les 10 décisions du Président — cette semaine</h3>
          <p>1. Adopter la charte v1.0.<br>
          2. Confirmer les 7 sièges (pas 10).<br>
          3. Nommer S. UM sponsor CARE+OPS.<br>
          4. Figer le stop-doing drones H0–H1.<br>
          5. Seuil MANDATORY CAPEX 10 k€.<br>
          6. Interdire la donnée de santé dans Git.<br>
          7. Calendrier Comex (créneau 90 min).<br>
          8. Cible n sites CD77 (hypothèse de travail).<br>
          9. Owner unique de la data room.<br>
          10. Date du Comité médical #1.</p>
        </div>
      </div>
      {footer("Fichiers : comex/CHARTE.md · comex/agents/ · comex/playbooks/")}
    """))

    s.append(slide(f"""
      <div class="eyebrow">18  —  Annexes</div>
      <h1 class="action">Le livrable n'est pas le PDF : c'est un système d'exploitation versionné, exécutable dès aujourd'hui.</h1>
      <div class="grid g2">
        <div class="card">
          <h3>Dans ce dépôt</h3>
          <table>
            <tr><th>Fichier</th><th>Usage</th></tr>
            <tr><td>comex/CHARTE.md</td><td>Constitution — à signer</td></tr>
            <tr><td>comex/architecture.yaml</td><td>Machine-readable (HITL, cadence, OKR)</td></tr>
            <tr><td>comex/agents/*.md</td><td>System prompts SMCI des 7 sièges</td></tr>
            <tr><td>comex/playbooks/comex-hebdo.md</td><td>Rituel 90 min</td></tr>
            <tr><td>comex/playbooks/90-jours.md</td><td>Checklist J0–J90</td></tr>
            <tr><td>comex/decisions/</td><td>Journal WORM des arbitrages</td></tr>
          </table>
        </div>
        <div class="card">
          <h3>Sources utilisées</h3>
          <ul class="tight">
            <li>medicalcity.ai — plateforme, agents, robots, studio (août 2026)</li>
            <li>Annonce légale SASU MEDICALCITY, 13/07/2026, RCS Paris</li>
            <li>CNSA, <em>Chiffres clés de l'aide à l'autonomie 2026</em> (44,45 Md€ / 6,3 Md€)</li>
            <li>CNSA, tarifs APA à domicile au 1er janvier 2026</li>
            <li>LinkedIn Richard YI — Bayon, 205 pré-réservations, wedge APA</li>
            <li>Instruction DNS/TS/DGCS n° 2026/91 — ESMS Numérique</li>
          </ul>
        </div>
      </div>
      <div class="so"><strong>Prochaine page blanche.</strong> Premier pack AGE à J+7. Si le pack n'existe pas, le Comex n'existe pas — le PDF non plus.</div>
      {footer("Document interne MedicalCity SASU — reproduction interdite")}
    """))

    s.append(slide(f"""
      <div style="height:80px"></div>
      <div style="font-size:13px;letter-spacing:.28em;color:var(--gold);font-weight:700">MEDICALCITY</div>
      <h1 class="action" style="font-size:36px;margin-top:14px">Le soin autonome se gouverne<br>avant de se scaler.</h1>
      <div class="rule"></div>
      <p style="font-size:18px;color:#C5D0DA;max-width:780px;line-height:1.45">
        Sept agents. Un Président. Douze sujets. Un pilote. Ensuite seulement, l'Europe.
      </p>
      <div class="cover-meta">
        medicalcity.ai  ·  richard.yi@medicalcity.ai  ·  66 avenue des Champs-Élysées, Paris<br>
        STRICTEMENT CONFIDENTIEL  ·  août 2026
      </div>
      {footer("Fin du document")}
    """, dark=True))

    return s


def main() -> None:
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    slides = "\n".join(build_slides())
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<title>MedicalCity — Comex IA &amp; scale-up · août 2026</title>
<style>{CSS}</style>
</head>
<body>
{slides}
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"HTML → {OUT_HTML}")

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUT_PDF}",
        OUT_HTML.as_uri(),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=90)
    except subprocess.TimeoutExpired:
        if not OUT_PDF.exists() or OUT_PDF.stat().st_size < 10_000:
            raise
        print("Chrome a dépassé le timeout ; PDF déjà écrit, on continue.")
    print(f"PDF  → {OUT_PDF}  ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
