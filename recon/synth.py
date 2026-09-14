"""Générateur de monde synthétique : référentiels, sources, archive — et défauts injectés.

Aucune donnée réelle n'est utilisée : tout est produit à partir d'une graine, donc
reproductible. Les défauts injectés constituent la **vérité terrain** : chaque défaut
porte l'identifiant du contrôle censé le détecter, et les tests vérifient que le
contrôle le trouve. C'est ce couplage qui rend le prototype démonstratif plutôt
qu'illustratif.
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from .model import (
    ArchiveReceipt,
    Attachment,
    CaptureConfig,
    Channel,
    Defect,
    Identity,
    Message,
    Party,
    PartyIdentity,
    SourceBatch,
    SupervisionScope,
)

NOMS = [
    "Adam", "Bahri", "Costa", "Dubois", "Ehrlich", "Fontaine", "Girard", "Hoang",
    "Ibrahim", "Jaeger", "Klein", "Lambert", "Moreau", "Nakamura", "Okonkwo",
    "Perrin", "Quesnel", "Rossi", "Sabbagh", "Tanaka", "Ustinov", "Vidal",
    "Wallace", "Yamada", "Zhang", "Almeida",
]
ENTITES = ["Paris — Global Markets", "Paris — Corporate Banking", "Londres — Markets"]
SUJETS = [
    "RFQ EUR IRS 10Y", "confirmation trade", "pricing indicatif", "revue de position",
    "appel de marge", "documentation ISDA", "point client", "calendrier de règlement",
    "limite de contrepartie", "reporting quotidien",
]
MOTS = [
    "spread", "collatéral", "notionnel", "valorisation", "contrepartie", "échéance",
    "confirmation", "règlement", "limite", "exposition", "couverture", "liquidité",
]
SLA_MINUTES = 120


def _h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


@dataclass
class World:
    start: date
    end: date
    parties: list[Party] = field(default_factory=list)
    identities: list[Identity] = field(default_factory=list)
    links: list[PartyIdentity] = field(default_factory=list)
    scopes: list[SupervisionScope] = field(default_factory=list)
    captures: list[CaptureConfig] = field(default_factory=list)
    batches: list[SourceBatch] = field(default_factory=list)
    receipts: dict[str, ArchiveReceipt] = field(default_factory=dict)
    source_truth: list[Message] = field(default_factory=list)
    defects: list[Defect] = field(default_factory=list)
    sla_minutes: int = SLA_MINUTES
    seed: int = 0

    # ---------------------------------------------------------------- accès

    @property
    def days(self) -> list[date]:
        n = (self.end - self.start).days
        return [self.start + timedelta(days=i) for i in range(n + 1)]

    @property
    def channels(self) -> list[Channel]:
        return [Channel.EMAIL, Channel.TEAMS, Channel.BLOOMBERG]

    def party(self, party_id: str) -> Party:
        return next(p for p in self.parties if p.party_id == party_id)

    def identity(self, identity_id: str) -> Identity:
        return next(i for i in self.identities if i.identity_id == identity_id)

    def party_of(self, identity_id: str, day: date) -> str | None:
        for link in self.links:
            if link.identity_id == identity_id and link.active_on(day):
                return link.party_id
        return None

    def identities_of(self, party_id: str, channel: Channel, day: date) -> list[Identity]:
        ids = [
            link.identity_id
            for link in self.links
            if link.party_id == party_id and link.active_on(day)
        ]
        return [
            i for i in self.identities
            if i.identity_id in ids and i.channel is channel and i.active_on(day)
        ]

    def supervised(self, day: date, channel: Channel) -> set[str]:
        return {
            s.party_id for s in self.scopes
            if s.channel is channel and s.active_on(day) and self.party(s.party_id).active_on(day)
        }

    def captured_identities(self, day: date, channel: Channel) -> set[str]:
        return {c.identity_id for c in self.captures if c.channel is channel and c.active_on(day)}

    def ingested(self) -> list[Message]:
        return [m for batch in self.batches for m in batch.messages]

    def archived_keys(self) -> set[str]:
        return set(self.receipts)


# --------------------------------------------------------------------- génération


def build(seed: int = 7, n_parties: int = 24, window_days: int = 30) -> World:
    rng = random.Random(seed)
    end = date(2026, 6, 30)
    start = end - timedelta(days=window_days - 1)
    w = World(start=start, end=end, seed=seed)

    # --- 1. Personnes : un stock, trois arrivées et trois départs dans la fenêtre
    for i in range(n_parties):
        nom = NOMS[i % len(NOMS)]
        pid = f"P{i:03d}"
        hired = start - timedelta(days=rng.randint(200, 2000))
        term = None
        if i in (5, 9, 19):  # départs dans la fenêtre, dont un détenteur de terminal Bloomberg
            term = start + timedelta(days=rng.randint(8, window_days - 6))
        if i in (7, 13, 21):  # arrivées dans la fenêtre
            hired = start + timedelta(days=rng.randint(3, window_days - 12))
        w.parties.append(
            Party(party_id=pid, nom=nom, entite=ENTITES[i % len(ENTITES)], hired_on=hired, terminated_on=term)
        )

    # --- 2. Identités, rattachements, périmètre supervisé, captation
    bloomberg_holders = {p.party_id for i, p in enumerate(w.parties) if i % 3 == 0}
    for p in w.parties:
        canaux = [Channel.EMAIL, Channel.TEAMS]
        if p.party_id in bloomberg_holders:
            canaux.append(Channel.BLOOMBERG)
        for ch in canaux:
            iid = f"{p.party_id}-{ch.value}"
            handle = {
                Channel.EMAIL: f"{p.nom.lower()}@banque.example",
                Channel.TEAMS: f"{p.nom.lower()}#teams",
                Channel.BLOOMBERG: f"{p.nom.upper()[:4]}{p.party_id[-2:]}<GO>",
            }[ch]
            src = "bloomberg_entitlements" if ch is Channel.BLOOMBERG else "directory"
            w.identities.append(
                Identity(
                    identity_id=iid, channel=ch, handle=handle,
                    valid_from=p.hired_on, valid_to=p.terminated_on, source_ref=src,
                )
            )
            w.links.append(
                PartyIdentity(party_id=p.party_id, identity_id=iid,
                              valid_from=p.hired_on, valid_to=p.terminated_on)
            )
            w.scopes.append(
                SupervisionScope(party_id=p.party_id, channel=ch,
                                 valid_from=p.hired_on, valid_to=p.terminated_on)
            )
            # Cas nominal : la captation prend effet le lendemain de l'arrivée.
            w.captures.append(
                CaptureConfig(identity_id=iid, channel=ch,
                              valid_from=p.hired_on + timedelta(days=1),
                              valid_to=p.terminated_on)
            )

    _inject_population_defects(w, bloomberg_holders)

    # --- 3. Messages, lots, archive
    _generate_traffic(w, rng)
    _inject_flow_defects(w, rng)

    return w


# ----------------------------------------------------------- défauts population


def _replace_capture(w: World, identity_id: str, **changes) -> CaptureConfig | None:
    for idx, cap in enumerate(w.captures):
        if cap.identity_id == identity_id:
            new = CaptureConfig(
                identity_id=cap.identity_id,
                channel=cap.channel,
                valid_from=changes.get("valid_from", cap.valid_from),
                valid_to=changes.get("valid_to", cap.valid_to),
                mechanism=changes.get("mechanism", cap.mechanism),
            )
            w.captures[idx] = new
            return new
    return None


def _inject_population_defects(w: World, bloomberg_holders: set[str]) -> None:
    # C01 — personne supervisée sans captation active sur un canal autorisé.
    trou = "P004-teams"
    w.captures = [c for c in w.captures if c.identity_id != trou]
    w.defects.append(
        Defect("C01_trou_couverture", "C01", "P004/teams",
               "Personne supervisée sans journalisation Teams : aucun paramétrage n'a jamais existé.")
    )

    # C02 — compte orphelin : la captation survit au départ, la supervision non.
    leaver = next(p for p in w.parties if p.terminated_on is not None)
    _replace_capture(w, f"{leaver.party_id}-email", valid_to=leaver.terminated_on + timedelta(days=12))
    w.defects.append(
        Defect("C02_compte_orphelin", "C02", f"{leaver.party_id}/email",
               "Captation maintenue 12 jours après le départ : processus de sortie non appliqué côté IT.")
    )

    # C03 — détenteur de terminal Bloomberg absent de la liste supervisée.
    hors_liste = sorted(bloomberg_holders)[1]
    w.scopes = [
        s for s in w.scopes
        if not (s.party_id == hors_liste and s.channel is Channel.BLOOMBERG)
    ]
    _replace_capture(w, f"{hors_liste}-bloomberg", valid_from=w.end + timedelta(days=30))
    w.defects.append(
        Defect("C03_entitlement_hors_perimetre", "C03", f"{hors_liste}/bloomberg",
               "Terminal Bloomberg actif, personne absente de la liste supervisée et captation inactive : "
               "l'écart n'est visible que par les entitlements.")
    )

    # C04 — arrivée dont la captation ne prend effet qu'au bout de six jours.
    joiner = next(p for p in w.parties if p.hired_on > w.start)
    _replace_capture(w, f"{joiner.party_id}-email", valid_from=joiner.hired_on + timedelta(days=6))
    w.defects.append(
        Defect("C04_latence_arrivee", "C04", f"{joiner.party_id}/email",
               "Journalisation activée 6 jours après la date d'entrée RH : fenêtre non captée.")
    )

    # C05 — départ dont l'entitlement est retiré avant la date de sortie.
    leavers = [p for p in w.parties if p.terminated_on is not None and p.party_id in bloomberg_holders]
    if leavers:
        early = leavers[0]
        _replace_capture(w, f"{early.party_id}-bloomberg",
                         valid_to=early.terminated_on - timedelta(days=3))
        w.defects.append(
            Defect("C05_captation_coupee_avant_depart", "C05", f"{early.party_id}/bloomberg",
                   "Entitlement Bloomberg retiré 3 jours avant la sortie : trois jours de communications "
                   "potentiellement non captés, juste avant un départ — la fenêtre la plus sensible.")
        )


# ----------------------------------------------------------------- trafic


def _generate_traffic(w: World, rng: random.Random) -> None:
    volumes = {Channel.EMAIL: (2, 7), Channel.TEAMS: (1, 11), Channel.BLOOMBERG: (0, 5)}
    par_canal_jour: dict[tuple[Channel, date], list[Message]] = {}

    for day in w.days:
        for ch in w.channels:
            actives = sorted(w.captured_identities(day, ch))
            bucket = par_canal_jour.setdefault((ch, day), [])
            for iid in actives:
                lo, hi = volumes[ch]
                for k in range(rng.randint(lo, hi)):
                    autres = [x for x in actives if x != iid] or actives
                    dest = tuple(rng.sample(autres, k=min(len(autres), rng.randint(1, 3))))
                    sujet = rng.choice(SUJETS)
                    corps = " ".join(rng.choice(MOTS) for _ in range(rng.randint(8, 24)))
                    sent = datetime.combine(day, datetime.min.time()) + timedelta(
                        hours=rng.randint(7, 19), minutes=rng.randint(0, 59), seconds=rng.randint(0, 59)
                    )
                    sid = f"{ch.value}-{day.isoformat()}-{iid}-{k:02d}"
                    atts: tuple[Attachment, ...] = ()
                    if ch is Channel.EMAIL and rng.random() < 0.15:
                        nom = f"annexe-{rng.randint(100, 999)}.pdf"
                        atts = (Attachment(name=nom, size=rng.randint(20_000, 4_000_000), sha256=_h(sid + nom)),)
                    bucket.append(
                        Message(
                            source_id=sid, content_hash=_h(sid + corps), channel=ch,
                            sender_identity=iid, recipients=dest, sent_at=sent, day=day,
                            thread_id=f"T{_h(sujet)[:8]}", subject=sujet, body=corps,
                            attachments=atts,
                            ingested_at=sent + timedelta(minutes=rng.randint(4, 38)),
                        )
                    )
            # Canaris : mesure de bout en bout indépendante des décomptes de la source.
            sent = datetime.combine(day, datetime.min.time()) + timedelta(hours=6, minutes=30)
            sid = f"canary-{ch.value}-{day.isoformat()}"
            bucket.append(
                Message(
                    source_id=sid, content_hash=_h(sid), channel=ch,
                    sender_identity="CANARY", recipients=("CANARY-RX",), sent_at=sent, day=day,
                    thread_id="T-CANARY", subject="canari quotidien", body="canari",
                    is_canary=True, ingested_at=sent + timedelta(minutes=rng.randint(3, 20)),
                )
            )

    # Édition Teams : une v2 qui devra coexister avec sa v1 dans l'archive.
    for (ch, day), msgs in par_canal_jour.items():
        if ch is Channel.TEAMS and day == w.start + timedelta(days=9) and msgs:
            base = msgs[0]
            msgs.append(
                Message(
                    source_id=base.source_id, content_hash=_h(base.source_id + "v2"),
                    channel=ch, sender_identity=base.sender_identity, recipients=base.recipients,
                    sent_at=base.sent_at + timedelta(minutes=12), day=day, thread_id=base.thread_id,
                    subject=base.subject, body=base.body + " (corrigé)", version=2,
                    edited_from=base.source_id,
                    ingested_at=base.sent_at + timedelta(minutes=20),
                )
            )

    for (ch, day), msgs in sorted(par_canal_jour.items(), key=lambda kv: (kv[0][1], kv[0][0].value)):
        w.source_truth.extend(msgs)
        w.batches.append(
            SourceBatch(
                batch_id=f"B-{ch.value}-{day.isoformat()}", channel=ch, day=day,
                declared_count=len(msgs), messages=list(msgs),
                received_at=datetime.combine(day, datetime.min.time()) + timedelta(days=1, hours=2),
            )
        )


# --------------------------------------------------------------- défauts de flux


def _inject_flow_defects(w: World, rng: random.Random) -> None:
    by_key = {(b.channel, b.day): b for b in w.batches}

    # C06 — le lot livre moins de messages que la source n'en déclare.
    cible = by_key[(Channel.EMAIL, w.start + timedelta(days=4))]
    perdus = [m for m in cible.messages if not m.is_canary][:4]
    for m in perdus:
        cible.messages.remove(m)
    w.defects.append(
        Defect("C06_ecart_source_ingestion", "C06", f"email/{cible.day.isoformat()}",
               f"{len(perdus)} messages déclarés par la source mais absents du lot livré.")
    )

    # C15 — un lot jamais livré : le contrôle de complétude ne peut pas s'exécuter.
    manquant = by_key[(Channel.BLOOMBERG, w.start + timedelta(days=17))]
    w.batches.remove(manquant)
    w.defects.append(
        Defect("C15_lot_absent", "C15", f"bloomberg/{manquant.day.isoformat()}",
               "Aucun lot reçu : le contrôle de complétude n'a pas d'entrée pour cette journée. "
               "Un contrôle qui n'a pas tourné doit être aussi visible qu'un contrôle en échec.")
    )

    # C08 — journée sans aucun message pour une identité par ailleurs bavarde.
    silence_id = "P002-teams"
    silence_day = w.start + timedelta(days=21)
    lot = by_key[(Channel.TEAMS, silence_day)]
    lot.messages = [m for m in lot.messages if m.sender_identity != silence_id]
    lot.declared_count = len(lot.messages)
    w.defects.append(
        Defect("C08_silence_anormal", "C08", f"{silence_id}/{silence_day.isoformat()}",
               "Aucun message sur un canal habituellement actif : panne de collecteur silencieuse.")
    )

    # C12 — messages chiffrés non exploitables à l'ingestion.
    chiffres = [m for m in by_key[(Channel.EMAIL, w.start + timedelta(days=12))].messages if not m.is_canary][:2]
    for m in chiffres:
        m.encrypted = True
        m.readable = False
    w.defects.append(
        Defect("C12_chiffre_illisible", "C12", f"email/{chiffres[0].day.isoformat()}",
               f"{len(chiffres)} messages chiffrés archivés sans être déchiffrables : "
               "présents mais inexploitables en restitution.")
    )

    # C11 — latence anormale sur une journée entière.
    lent = by_key[(Channel.TEAMS, w.start + timedelta(days=25))]
    for m in lent.messages:
        m.ingested_at = m.sent_at + timedelta(hours=rng.randint(6, 9))
    w.defects.append(
        Defect("C11_latence_hors_sla", "C11", f"teams/{lent.day.isoformat()}",
               "Latence captation → archive de 6 à 9 h contre un SLA de 2 h.")
    )

    # --- Archive : accusés de prise en compte, avec trois défauts de fidélité.
    non_acquittes = {
        m.source_id for m in by_key[(Channel.EMAIL, w.start + timedelta(days=8))].messages
        if not m.is_canary
    }
    non_acquittes = set(sorted(non_acquittes)[:3])
    canari_perdu = f"canary-teams-{(w.start + timedelta(days=14)).isoformat()}"
    pj_tronquee: str | None = None
    hash_faux: str | None = None
    v1_ecrasee: str | None = None

    for batch in w.batches:
        for m in batch.messages:
            if m.source_id in non_acquittes or m.source_id == canari_perdu:
                continue
            att_count = len(m.attachments)
            stored = m.content_hash
            if pj_tronquee is None and m.attachments and m.channel is Channel.EMAIL:
                pj_tronquee, att_count = m.source_id, 0
            elif hash_faux is None and m.channel is Channel.EMAIL and not m.attachments and not m.is_canary:
                hash_faux, stored = m.source_id, _h(m.content_hash + "altéré")
            if m.edited_from is not None:
                v1_ecrasee = m.edited_from  # l'archive ne gardera que la v2
            w.receipts[m.key] = ArchiveReceipt(
                message_key=m.key, archive="ARCHIVE-REF",
                acknowledged_at=(m.ingested_at or m.sent_at) + timedelta(minutes=rng.randint(1, 9)),
                stored_hash=stored, attachment_count=att_count,
            )
    if v1_ecrasee:
        w.receipts.pop(f"{v1_ecrasee}#v1", None)

    w.defects += [
        Defect("C07_non_acquitte", "C07", f"email/{(w.start + timedelta(days=8)).isoformat()}",
               f"{len(non_acquittes)} messages ingérés sans accusé de l'archive."),
        Defect("C07_canari_perdu", "C07", f"teams/{(w.start + timedelta(days=14)).isoformat()}",
               "Canari quotidien jamais arrivé dans l'archive : preuve directe d'un trou de chaîne."),
        Defect("C09_piece_jointe_absente", "C09", pj_tronquee or "?",
               "Message archivé sans sa pièce jointe : le record n'est pas auto-portant."),
        Defect("C09_hash_divergent", "C09", hash_faux or "?",
               "Hash stocké différent du hash d'origine : altération ou re-encodage silencieux."),
        Defect("C10_version_ecrasee", "C10", v1_ecrasee or "?",
               "Message Teams édité dont la version initiale a été écrasée : l'archive documente "
               "un état, pas la conversation."),
    ]
