"""Restitution : index de recherche sur l'archive et exercice de tirage à l'aveugle.

Le seul test qui compte est de retrouver et d'exporter un périmètre de communications
dans le délai imposé. Ici l'exhaustivité est mesurée contre la **vérité de la source**,
pas contre l'archive : comparer l'archive à elle-même est précisément le piège du
recordkeeping. Un message perdu en route ou archivé illisible fait donc chuter le
rappel, ce qui est le comportement attendu.
"""
from __future__ import annotations

import random
import re
import time
from collections import defaultdict
from datetime import date, timedelta

from .model import Message
from .synth import World

TOKEN = re.compile(r"[\wàâäéèêëîïôöùûüç'-]+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in TOKEN.findall(text)}


class RetrievalIndex:
    """Index de restitution : personne → jour → messages, plus un index de tokens.

    Ne contient que ce qui est **effectivement archivé et lisible** : c'est ce qu'un
    enquêteur pourra sortir, indépendamment de ce qui existait.
    """

    def __init__(self, world: World) -> None:
        self.w = world
        self.by_party: dict[str, dict[date, list[Message]]] = defaultdict(lambda: defaultdict(list))
        self.by_token: dict[str, set[str]] = defaultdict(set)
        self.size = 0
        for m in world.ingested():
            if m.key not in world.receipts or not m.readable or m.is_canary:
                continue
            self.size += 1
            for pid in self._parties_of(m):
                self.by_party[pid][m.day].append(m)
            for token in _tokens(f"{m.subject} {m.body}"):
                self.by_token[token].add(m.source_id)

    def _parties_of(self, m: Message) -> set[str]:
        parties = set()
        for iid in (m.sender_identity, *m.recipients):
            pid = self.w.party_of(iid, m.day)
            if pid:
                parties.add(pid)
        return parties

    def search(self, party_id: str, start: date, end: date, keyword: str | None = None) -> set[str]:
        hits: set[str] = set()
        jours = self.by_party.get(party_id, {})
        day = start
        while day <= end:
            for m in jours.get(day, ()):
                hits.add(m.source_id)
            day += timedelta(days=1)
        if keyword:
            hits &= self.by_token.get(keyword.lower(), set())
        return hits


def expected_set(world: World, party_id: str, start: date, end: date, keyword: str | None) -> set[str]:
    """Jeu de référence : ce qui a existé à la source pour ce périmètre."""
    wanted: set[str] = set()
    for m in world.source_truth:
        if m.is_canary or not (start <= m.day <= end):
            continue
        parties = set()
        for iid in (m.sender_identity, *m.recipients):
            pid = world.party_of(iid, m.day)
            if pid:
                parties.add(pid)
        if party_id not in parties:
            continue
        if keyword and keyword.lower() not in _tokens(f"{m.subject} {m.body}"):
            continue
        wanted.add(m.source_id)
    return wanted


def targeted_drill(world: World, index: RetrievalIndex, span: int = 6) -> dict | None:
    """Tirage ciblé sur la journée la plus abîmée, tel que Compliance le referait après un incident.

    Un exercice à l'aveugle a peu de chances de tomber sur la fenêtre défectueuse : c'est
    justement pourquoi il faut aussi rejouer la restitution là où l'on sait qu'il y a eu un trou.
    """
    indexes = {m.source_id for m in world.ingested() if m.key in world.receipts and m.readable}
    perdus_par_jour: dict[date, list[Message]] = defaultdict(list)
    for m in world.source_truth:
        if m.is_canary:
            continue
        if m.source_id not in indexes:
            perdus_par_jour[m.day].append(m)
    if not perdus_par_jour:
        return None
    jour = max(perdus_par_jour, key=lambda d: len(perdus_par_jour[d]))
    perdus = perdus_par_jour[jour]
    pid = next(
        (p for m in perdus for p in sorted(index._parties_of(m)) if p in index.by_party),
        None,
    )
    if pid is None:
        return None
    start = max(jour - timedelta(days=span // 2), world.start)
    end = min(start + timedelta(days=span - 1), world.end)
    attendu = expected_set(world, pid, start, end, None)
    if not attendu:
        return None
    t0 = time.perf_counter()
    trouve = index.search(pid, start, end, None)
    elapsed = (time.perf_counter() - t0) * 1000
    recouvre = attendu & trouve
    return {
        "scope": f"{pid} · tirage ciblé post-incident",
        "window": f"{start.isoformat()}..{end.isoformat()}",
        "expected": len(attendu),
        "found": len(recouvre),
        "extra": len(trouve - attendu),
        "recall": len(recouvre) / len(attendu),
        "elapsed_ms": elapsed,
        "manquants": sorted(attendu - trouve)[:5],
    }


def drill(world: World, index: RetrievalIndex, n: int = 3, seed: int = 0, span: int = 6) -> list[dict]:
    """Exercices à l'aveugle : Compliance tire un périmètre, l'équipe restitue sans préparation."""
    rng = random.Random(seed)
    mots = ["collatéral", "notionnel", "confirmation", "limite", "exposition", "règlement"]
    essais: list[dict] = []
    candidats = sorted(index.by_party)
    tentatives = 0
    while len(essais) < n and tentatives < 200:
        tentatives += 1
        pid = rng.choice(candidats)
        start = world.start + timedelta(days=rng.randint(0, max(len(world.days) - span - 1, 0)))
        end = start + timedelta(days=span - 1)
        keyword = rng.choice(mots) if rng.random() < 0.7 else None
        attendu = expected_set(world, pid, start, end, keyword)
        if len(attendu) < 3:
            continue
        t0 = time.perf_counter()
        trouve = index.search(pid, start, end, keyword)
        elapsed = (time.perf_counter() - t0) * 1000
        recouvre = attendu & trouve
        essais.append(
            {
                "scope": f"{pid}" + (f" · « {keyword} »" if keyword else " · tous messages"),
                "window": f"{start.isoformat()}..{end.isoformat()}",
                "expected": len(attendu),
                "found": len(recouvre),
                "extra": len(trouve - attendu),
                "recall": len(recouvre) / len(attendu),
                "elapsed_ms": elapsed,
                "manquants": sorted(attendu - trouve)[:5],
            }
        )
    return essais
