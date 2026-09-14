"""Rapport de réconciliation : les six chiffres du dossier de décision, puis le détail.

Un PoC qui ne produit que des captures d'écran ne fait pas décider. Ce module produit
les chiffres sur lesquels un comité peut trancher, et il dit explicitement ce que le
prototype ne démontre pas.
"""
from __future__ import annotations

import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta

from .controls import CATALOGUE, Run, _p95
from .model import Channel
from .synth import World


@dataclass
class Stats:
    attendus: dict[Channel, int]
    couverts: dict[Channel, int]
    declares: dict[Channel, int]
    livres: dict[Channel, int]
    archives: dict[Channel, int]
    canaris_emis: int
    canaris_archives: int
    p95_latence: float
    mediane_latence: float
    illisibles: int
    index_size: int
    source_total: int


def compute(world: World, run: Run) -> Stats:
    attendus: dict[Channel, int] = defaultdict(int)
    couverts: dict[Channel, int] = defaultdict(int)
    for day in world.days:
        for ch in world.channels:
            captes = world.captured_identities(day, ch)
            for pid in world.supervised(day, ch):
                attendus[ch] += 1
                if any(i.identity_id in captes for i in world.identities_of(pid, ch, day)):
                    couverts[ch] += 1

    declares: dict[Channel, int] = defaultdict(int)
    livres: dict[Channel, int] = defaultdict(int)
    archives: dict[Channel, int] = defaultdict(int)
    for batch in world.batches:
        declares[batch.channel] += batch.declared_count
        livres[batch.channel] += len(batch.messages)
        archives[batch.channel] += sum(1 for m in batch.messages if m.key in world.receipts)

    canaris = [m for m in world.source_truth if m.is_canary]
    latences = [
        (world.receipts[m.key].acknowledged_at - m.sent_at).total_seconds() / 60
        for m in world.ingested() if m.key in world.receipts
    ]
    return Stats(
        attendus=dict(attendus), couverts=dict(couverts),
        declares=dict(declares), livres=dict(livres), archives=dict(archives),
        canaris_emis=len(canaris),
        canaris_archives=sum(1 for m in canaris if m.key in world.receipts),
        p95_latence=_p95(latences), mediane_latence=statistics.median(latences) if latences else 0.0,
        illisibles=sum(1 for m in world.ingested() if not m.readable),
        index_size=run.index.size, source_total=len(world.source_truth),
    )


def _pct(num: int, den: int) -> str:
    return f"{num / den:.2%}" if den else "—"


def render(world: World, run: Run) -> str:
    s = compute(world, run)
    as_of = world.end + timedelta(days=1)
    ouvertes = [e for e in run.exceptions if e.status.value == "ouverte"]
    en_retard = [e for e in ouvertes if e.overdue(as_of)]
    ko = [r for r in run.results if r.verdict == "ko"]
    non_exec = [r for r in run.results if r.verdict == "non exécuté"]
    intacte, chaine = run.journal.verify()

    total_attendus = sum(s.attendus.values())
    total_couverts = sum(s.couverts.values())
    total_declares = sum(s.declares.values())
    total_archives = sum(s.archives.values())
    drills_ok = [d for d in run.drills if d["recall"] >= 1.0]
    p95_restitution = _p95([d["elapsed_ms"] for d in run.drills])

    out: list[str] = []
    a = out.append

    a("# Rapport de réconciliation e-comms — prototype")
    a("")
    a(f"Fenêtre **{world.start.isoformat()} → {world.end.isoformat()}** · "
      f"{len(world.parties)} personnes · {len(world.channels)} canaux · "
      f"{s.source_total} messages à la source · graine `{world.seed}`.")
    a("")
    a("> Données entièrement synthétiques. Les défauts sont **injectés volontairement** : "
      "le rapport vaut par le fait que les contrôles les retrouvent, pas par ses chiffres.")
    a("")

    a("## 1. Les six chiffres du dossier de décision")
    a("")
    a("| # | Indicateur | Valeur |")
    a("|---|---|---|")
    a(f"| 1 | Couverture de la population supervisée | **{_pct(total_couverts, total_attendus)}** "
      f"({total_attendus - total_couverts} jours-personne-canal non couverts) |")
    a(f"| 2 | Complétude source → archive | **{_pct(total_archives, total_declares)}** "
      f"({total_declares - total_archives} messages manquants) |")
    a(f"| 3 | Restitution : rappel et délai p95 | **{len(drills_ok)}/{len(run.drills)} tirages complets**, "
      f"p95 {p95_restitution:.1f} ms |")
    a(f"| 4 | Contrôles automatisés, et traçabilité des écarts | "
      f"**{len(CATALOGUE)}/{len(CATALOGUE)}** automatisés, "
      f"**{len(run.detected_controls())}** ont ouvert une exception traçable |")
    a(f"| 5 | Ancienneté du plus vieil écart ouvert | **{run.oldest_open_gap(as_of)} jours** |")
    a("| 6 | Coût par million de messages | *non mesurable sur données synthétiques — "
      "à instruire avec les licences réelles (extraction Teams, archive, stockage)* |")
    a("")
    a(f"Chaîne d'audit : **{chaine}**. Exceptions ouvertes : **{len(ouvertes)}**, dont "
      f"**{len(en_retard)}** hors délai. Contrôles en échec : **{len(ko)}**, non exécutés : "
      f"**{len(non_exec)}**.")
    a("")

    a("## 2. Niveau 1 — populations : qui aurait dû être capté ?")
    a("")
    a("| Canal | Jours-personne attendus | Couverts | Couverture |")
    a("|---|---:|---:|---:|")
    for ch in world.channels:
        a(f"| {ch.label} | {s.attendus.get(ch, 0)} | {s.couverts.get(ch, 0)} | "
          f"{_pct(s.couverts.get(ch, 0), s.attendus.get(ch, 0))} |")
    a("")

    a("## 3. Niveau 2 — volumétrie : tout ce qui a existé est-il arrivé ?")
    a("")
    a("| Canal | Déclaré source | Livré | Archivé et acquitté | Perte |")
    a("|---|---:|---:|---:|---:|")
    for ch in world.channels:
        d, l, ar = s.declares.get(ch, 0), s.livres.get(ch, 0), s.archives.get(ch, 0)
        a(f"| {ch.label} | {d} | {l} | {ar} | {d - ar} |")
    a("")
    a(f"Canaris : **{s.canaris_archives}/{s.canaris_emis}** arrivés dans l'archive. "
      "Le canari est la seule mesure qui ne dépende pas de la sincérité des décomptes de la source.")
    a("")

    a("## 4. Niveau 3 — fidélité : ce qui est arrivé est-il exploitable ?")
    a("")
    a(f"- Messages indexables et restituables : **{s.index_size}** sur {s.source_total} existants à la source.")
    a(f"- Messages chiffrés non exploitables : **{s.illisibles}**.")
    a(f"- Latence captation → archive : médiane **{s.mediane_latence:.0f} min**, "
      f"p95 **{s.p95_latence:.0f} min** pour un SLA de {world.sla_minutes} min.")
    a("")

    a("## 5. Catalogue de contrôles")
    a("")
    a("| Id | Contrôle | Propriétaire | Résultats | ok | ko | non exécuté | Exceptions |")
    a("|---|---|---|---:|---:|---:|---:|---:|")
    for cid, (libelle, owner, _sev) in CATALOGUE.items():
        res = [r for r in run.results if r.control_id == cid]
        exc = [e for e in run.exceptions if e.control_id == cid]
        a(f"| {cid} | {libelle} | {owner} | {len(res)} | "
          f"{sum(1 for r in res if r.verdict == 'ok')} | "
          f"{sum(1 for r in res if r.verdict == 'ko')} | "
          f"{sum(1 for r in res if r.verdict == 'non exécuté')} | {len(exc)} |")
    a("")

    a("## 6. Exceptions — l'aging compte plus que le nombre")
    a("")
    par_owner: dict[str, list] = defaultdict(list)
    for e in ouvertes:
        par_owner[e.owner].append(e)
    a("| Propriétaire | Ouvertes | Hors délai | Plus ancienne (j) |")
    a("|---|---:|---:|---:|")
    for owner in sorted(par_owner):
        lot = par_owner[owner]
        a(f"| {owner} | {len(lot)} | {sum(1 for e in lot if e.overdue(as_of))} | "
          f"{max(e.age_days(as_of) for e in lot)} |")
    a("")
    a("Dix exceptions les plus anciennes :")
    a("")
    a("| Id | Contrôle | Gravité | Périmètre | Ouverte le | Âge (j) | Cause |")
    a("|---|---|---|---|---|---:|---|")
    for e in sorted(ouvertes, key=lambda x: (x.opened_on, x.exception_id))[:10]:
        a(f"| {e.exception_id} | {e.control_id} | {e.severity.value} | {e.scope} | "
          f"{e.opened_on.isoformat()} | {e.age_days(as_of)} | {e.cause} |")
    a("")

    a("## 7. Restitution — exercices à l'aveugle")
    a("")
    a("| Périmètre | Fenêtre | Attendus | Retrouvés | Rappel | Délai |")
    a("|---|---|---:|---:|---:|---:|")
    for d in run.drills:
        a(f"| {d['scope']} | {d['window']} | {d['expected']} | {d['found']} | "
          f"{d['recall']:.1%} | {d['elapsed_ms']:.1f} ms |")
    a("")
    if any(d["recall"] < 1.0 for d in run.drills):
        a("Le rappel est mesuré contre **la vérité de la source**, pas contre l'archive : un message "
          "perdu en route ou archivé illisible fait donc chuter le rappel. C'est le comportement "
          "recherché — comparer l'archive à elle-même donnerait 100 % et ne prouverait rien.")
        a("")

    a("## 8. Piste d'audit")
    a("")
    a(f"- {len(run.journal)} entrées chaînées ; vérification : **{chaine}**.")
    a("- Types d'entrées : réception de lot, résultat de contrôle, ouverture d'exception, "
      "exercice de restitution, début et fin d'exécution.")
    a("- Chaque entrée porte la version des règles appliquées : sans ce versionnage, "
      "l'historique n'est pas rejouable, et une piste d'audit non rejouable n'est pas une preuve.")
    a("")

    a("## 9. Ce que ce prototype ne démontre pas")
    a("")
    a("- **Les connecteurs réels.** Aucune API Microsoft ni flux Bloomberg n'est appelé : les sources "
      "sont simulées, avec leurs pièges (décompte déclaré ≠ livré, édition Teams, entitlement retiré "
      "avant la sortie), mais pas leurs modalités d'accès, leurs quotas ni leur coût de licence.")
    a("- **L'immutabilité au stockage.** Le journal est hash-chaîné, ce qui rend une altération "
      "détectable ; il n'est pas posé sur un support verrouillé (Object Lock, blob immuable), "
      "ce qui seul rend l'altération impossible.")
    a("- **L'échelle.** Quelques milliers de messages en mémoire. Les décisions d'architecture "
      "changent à partir de plusieurs millions par jour : partitionnement, index, coût du rejeu.")
    a("- **Le déchiffrement.** Les messages chiffrés sont détectés, pas traités : la stratégie de clés "
      "est une décision de sécurité, pas d'architecture data.")
    a("")
    a("*Prototype écrit pour la candidature au poste de Lead Solution Architect — "
      "E-Communications Recordkeeping & Reconciliation. Aucune donnée réelle.*")
    return "\n".join(out) + "\n"


def console(world: World, run: Run) -> str:
    """Résumé court pour le terminal."""
    s = compute(world, run)
    as_of = world.end + timedelta(days=1)
    intacte, chaine = run.journal.verify()
    total_attendus = sum(s.attendus.values())
    total_couverts = sum(s.couverts.values())
    total_declares = sum(s.declares.values())
    total_archives = sum(s.archives.values())
    lignes = [
        f"fenêtre            {world.start} → {world.end}  ({s.source_total} messages source)",
        f"couverture pop.    {_pct(total_couverts, total_attendus)}  "
        f"({total_attendus - total_couverts} jours-personne-canal non couverts)",
        f"complétude         {_pct(total_archives, total_declares)}  "
        f"({total_declares - total_archives} messages manquants)",
        f"canaris            {s.canaris_archives}/{s.canaris_emis} arrivés",
        f"latence p95        {s.p95_latence:.0f} min (SLA {world.sla_minutes} min)",
        f"contrôles          {len(run.results)} résultats · "
        f"{sum(1 for r in run.results if r.verdict == 'ko')} ko · "
        f"{sum(1 for r in run.results if r.verdict == 'non exécuté')} non exécutés",
        f"exceptions         {len(run.exceptions)} ouvertes · "
        f"plus vieil écart {run.oldest_open_gap(as_of)} j",
        f"restitution        {sum(1 for d in run.drills if d['recall'] >= 1.0)}/{len(run.drills)} "
        f"tirages complets",
        f"piste d'audit      {chaine}",
    ]
    return "\n".join(lignes)
