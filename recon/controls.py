"""Les quinze contrôles du PoC, dans l'ordre du catalogue de la note d'architecture.

Trois niveaux indépendants, jamais confondus dans un même indicateur :

- **niveau 1, populations** (C01–C05) : qui aurait dû être capté ?
- **niveau 2, volumétrie** (C06–C08) : tout ce qui a existé est-il arrivé ?
- **niveau 3, fidélité** (C09–C12) : ce qui est arrivé est-il exploitable ?

Puis la preuve elle-même (C13), la restitution (C14) et le contrôle du contrôle (C15).
Chaque contrôle produit un `ControlResult` — y compris quand il ne peut pas s'exécuter,
ce qui est la seule façon de rendre visible un contrôle qui n'a pas tourné.
"""
from __future__ import annotations

import statistics
from collections import defaultdict
from datetime import date, timedelta

from .audit import AuditJournal
from .model import Channel, ControlResult, Exception_, Severity
from .retrieval import RetrievalIndex, drill, targeted_drill
from .synth import World

CATALOGUE: dict[str, tuple[str, str, Severity]] = {
    "C01": ("Couverture population", "Compliance IT", Severity.CRITIQUE),
    "C02": ("Comptes orphelins", "IT / Ops", Severity.MAJEURE),
    "C03": ("Entitlements hors périmètre", "Ops marchés", Severity.CRITIQUE),
    "C04": ("Latence des arrivées", "RH IT", Severity.MAJEURE),
    "C05": ("Départs et continuité", "IT / Ops", Severity.CRITIQUE),
    "C06": ("Complétude source → ingestion", "Data Ops", Severity.CRITIQUE),
    "C07": ("Complétude ingestion → archive", "Data Ops", Severity.CRITIQUE),
    "C08": ("Continuité temporelle", "Data Ops", Severity.MAJEURE),
    "C09": ("Pièces jointes et intégrité de contenu", "Data Ops", Severity.MAJEURE),
    "C10": ("Éditions et suppressions", "Data Ops", Severity.MAJEURE),
    "C11": ("Fraîcheur", "Data Ops", Severity.MINEURE),
    "C12": ("Lisibilité", "IT sécurité", Severity.MAJEURE),
    "C13": ("Intégrité de la preuve", "Architecture", Severity.CRITIQUE),
    "C14": ("Restitution (retrievability)", "Compliance", Severity.CRITIQUE),
    "C15": ("Contrôle du contrôle", "Data Ops", Severity.MAJEURE),
}

RETRIEVAL_SLA_MS = 3000.0


class Run:
    """Exécution complète du catalogue sur un monde donné."""

    def __init__(self, world: World, journal: AuditJournal | None = None) -> None:
        self.w = world
        # `journal or AuditJournal()` serait un piège : un journal vide est falsy (__len__).
        self.journal = journal if journal is not None else AuditJournal()
        self.results: list[ControlResult] = []
        self.exceptions: list[Exception_] = []
        self.index = RetrievalIndex(world)
        self.drills: list[dict] = []
        self._seq = 0

    # ------------------------------------------------------------------ outils

    def _result(self, cid: str, scope: str, period: str, expected, observed, verdict: str, detail: str = "") -> None:
        res = ControlResult(
            control_id=cid, libelle=CATALOGUE[cid][0], scope=scope, period=period,
            expected=expected, observed=observed, verdict=verdict, detail=detail,
        )
        self.results.append(res)
        self.journal.append(
            "control_result", control_id=cid, scope=scope, period=period,
            expected=expected, observed=observed, verdict=verdict,
        )

    def _exception(self, cid: str, scope: str, cause: str, opened_on: date, due: int = 5) -> Exception_:
        self._seq += 1
        _, owner, severity = CATALOGUE[cid]
        exc = Exception_(
            exception_id=f"E{self._seq:04d}", control_id=cid, severity=severity,
            scope=scope, cause=cause, owner=owner, opened_on=opened_on, due_in_days=due,
        )
        self.exceptions.append(exc)
        self.journal.append(
            "exception_opened", exception_id=exc.exception_id, control_id=cid,
            scope=scope, severity=severity.value, owner=owner, opened_on=opened_on.isoformat(),
        )
        return exc

    # ---------------------------------------------------------- niveau 1 : populations

    def c01_couverture(self) -> None:
        """Personne supervisée sans captation active : gravité maximale, c'est le trou de couverture."""
        manques: dict[tuple[str, Channel], list[date]] = defaultdict(list)
        attendus = couverts = 0
        for day in self.w.days:
            for ch in self.w.channels:
                for pid in sorted(self.w.supervised(day, ch)):
                    attendus += 1
                    ids = self.w.identities_of(pid, ch, day)
                    captes = self.w.captured_identities(day, ch)
                    if any(i.identity_id in captes for i in ids):
                        couverts += 1
                    else:
                        manques[(pid, ch)].append(day)
        for (pid, ch), jours in sorted(manques.items(), key=lambda kv: (kv[0][0], kv[0][1].value)):
            self._exception(
                "C01", f"{pid}/{ch.value}",
                f"{len(jours)} jour(s) supervisé(s) sans journalisation active "
                f"(du {jours[0].isoformat()} au {jours[-1].isoformat()})",
                opened_on=jours[0],
            )
        taux = couverts / attendus if attendus else 1.0
        self._result(
            "C01", "toutes populations", "fenêtre", 0, attendus - couverts,
            "ok" if attendus == couverts else "ko",
            f"couverture {taux:.2%} sur {attendus} jours-personne-canal attendus",
        )

    def c02_orphelins(self) -> None:
        """Captation active alors que personne de supervisée ne l'est : sortie mal traitée."""
        orphelins: dict[tuple[str, Channel], list[date]] = defaultdict(list)
        for day in self.w.days:
            for ch in self.w.channels:
                supervisees = self.w.supervised(day, ch)
                for iid in sorted(self.w.captured_identities(day, ch)):
                    pid = self.w.party_of(iid, day)
                    if pid is None or pid not in supervisees:
                        orphelins[(iid, ch)].append(day)
        for (iid, ch), jours in sorted(orphelins.items(), key=lambda kv: kv[0][0]):
            self._exception(
                "C02", f"{iid}",
                f"captation active {len(jours)} jour(s) sans personne supervisée rattachée "
                f"(du {jours[0].isoformat()} au {jours[-1].isoformat()})",
                opened_on=jours[0],
            )
        self._result("C02", "tous comptes", "fenêtre", 0, len(orphelins),
                     "ok" if not orphelins else "ko",
                     f"{len(orphelins)} compte(s) journalisé(s) hors périmètre supervisé")

    def c03_entitlements(self) -> None:
        """Un terminal Bloomberg actif est une source de communications : il doit être
        dans le périmètre, que la liste supervisée le sache ou non."""
        ecarts = 0
        for ident in sorted(
            (i for i in self.w.identities if i.source_ref == "bloomberg_entitlements"),
            key=lambda i: i.identity_id,
        ):
            for day in self.w.days:
                if not ident.active_on(day):
                    continue
                pid = self.w.party_of(ident.identity_id, day)
                if pid is None or not self.w.party(pid).active_on(day):
                    continue
                supervise = pid in self.w.supervised(day, Channel.BLOOMBERG)
                capte = ident.identity_id in self.w.captured_identities(day, Channel.BLOOMBERG)
                if not supervise or not capte:
                    ecarts += 1
                    self._exception(
                        "C03", f"{pid}/bloomberg",
                        "terminal Bloomberg actif "
                        + ("hors liste supervisée" if not supervise else "sans captation active")
                        + f" à partir du {day.isoformat()}",
                        opened_on=day,
                    )
                    break  # une exception par détenteur suffit
        self._result("C03", "entitlements Bloomberg", "fenêtre", 0, ecarts,
                     "ok" if not ecarts else "ko",
                     f"{ecarts} détenteur(s) de terminal hors périmètre de captation")

    def c04_latence_arrivees(self, seuil_jours: int = 1) -> None:
        """Délai entre l'événement RH et la prise d'effet de la journalisation :
        c'est là que se logent la majorité des trous réels."""
        pires: list[tuple[str, int]] = []
        for p in self.w.parties:
            if p.hired_on < self.w.start:
                continue
            for cap in self.w.captures:
                pid = self.w.party_of(cap.identity_id, cap.valid_from)
                if pid != p.party_id:
                    continue
                delta = (cap.valid_from - p.hired_on).days
                if delta > seuil_jours:
                    pires.append((cap.identity_id, delta))
                    self._exception(
                        "C04", cap.identity_id,
                        f"journalisation activée {delta} jours après la date d'entrée RH "
                        f"({p.hired_on.isoformat()})",
                        opened_on=p.hired_on,
                    )
        observed = max((d for _, d in pires), default=0)
        self._result("C04", "arrivées de la fenêtre", "fenêtre", seuil_jours, observed,
                     "ok" if not pires else "ko",
                     f"{len(pires)} arrivée(s) hors seuil, pire délai {observed} j")

    def c05_departs(self) -> None:
        """La captation doit durer jusqu'à la désactivation, et la rétention survivre au départ.
        Les jours qui précèdent une sortie sont la fenêtre la plus sensible du programme."""
        ecarts = 0
        for p in self.w.parties:
            if p.terminated_on is None or not (self.w.start <= p.terminated_on <= self.w.end):
                continue
            for cap in self.w.captures:
                if self.w.party_of(cap.identity_id, p.terminated_on) != p.party_id:
                    continue
                if cap.valid_to is not None and cap.valid_to < p.terminated_on:
                    ecarts += 1
                    trou = (p.terminated_on - cap.valid_to).days
                    self._exception(
                        "C05", cap.identity_id,
                        f"captation arrêtée {trou} jour(s) avant la sortie du {p.terminated_on.isoformat()}",
                        opened_on=cap.valid_to,
                    )
            # Rétention : les messages archivés avant le départ doivent rester lisibles après.
            conserves = sum(
                1 for m in self.w.source_truth
                if m.day <= p.terminated_on
                and self.w.party_of(m.sender_identity, m.day) == p.party_id
                and m.key in self.w.receipts
            )
            self.journal.append("retention_check", party=p.party_id, archived_messages=conserves)
        self._result("C05", "départs de la fenêtre", "fenêtre", 0, ecarts,
                     "ok" if not ecarts else "ko",
                     f"{ecarts} départ(s) avec captation interrompue trop tôt")

    # ---------------------------------------------------------- niveau 2 : volumétrie

    def c06_source_vers_ingestion(self) -> None:
        """Décompte déclaré par la source contre contenu réellement livré.
        Un décompte de source est une déclaration : il n'est jamais la vérité."""
        lots = {(b.channel, b.day): b for b in self.w.batches}
        for day in self.w.days:
            for ch in self.w.channels:
                if not self.w.captured_identities(day, ch):
                    continue
                batch = lots.get((ch, day))
                if batch is None:
                    self._result("C06", ch.value, day.isoformat(), None, None, "non exécuté",
                                 "aucun lot reçu : pas d'entrée pour ce contrôle")
                    continue
                livres = len(batch.messages)
                canaris = sum(1 for m in batch.messages if m.is_canary)
                ecart = batch.declared_count - livres
                verdict = "ok" if ecart == 0 else "ko"
                self._result("C06", ch.value, day.isoformat(), batch.declared_count, livres, verdict,
                             f"écart {ecart}, canaris livrés {canaris}")
                if ecart:
                    self._exception(
                        "C06", f"{ch.value}/{day.isoformat()}",
                        f"{ecart} message(s) déclaré(s) par la source et absent(s) du lot livré",
                        opened_on=day,
                    )

    def c07_ingestion_vers_archive(self) -> None:
        """Ingéré contre acquitté par l'archive. Sans accusé opposable, ce niveau est
        bancal par construction — d'où les canaris comme mesure indépendante."""
        par_jour: dict[tuple[Channel, date], list] = defaultdict(list)
        for m in self.w.ingested():
            par_jour[(m.channel, m.day)].append(m)
        canaris_perdus = 0
        for (ch, day), msgs in sorted(par_jour.items(), key=lambda kv: (kv[0][1], kv[0][0].value)):
            acquittes = [m for m in msgs if m.key in self.w.receipts]
            manquants = [m for m in msgs if m.key not in self.w.receipts]
            verdict = "ok" if not manquants else "ko"
            canaris = [m for m in manquants if m.is_canary]
            canaris_perdus += len(canaris)
            self._result("C07", ch.value, day.isoformat(), len(msgs), len(acquittes), verdict,
                         f"{len(manquants)} sans accusé" + (f", dont {len(canaris)} canari(s)" if canaris else ""))
            if manquants:
                cause = f"{len(manquants)} message(s) ingéré(s) sans accusé de l'archive"
                if canaris:
                    cause += " — dont le canari quotidien, preuve directe d'un trou de chaîne"
                self._exception("C07", f"{ch.value}/{day.isoformat()}", cause, opened_on=day, due=2)
        self.journal.append("canary_summary", lost=canaris_perdus)

    def c08_continuite(self, mediane_min: int = 4) -> None:
        """Journée sans aucun message sur un canal habituellement actif : c'est ainsi
        qu'une panne de collecteur se manifeste — par du silence, pas par une erreur."""
        compte: dict[tuple[str, Channel, date], int] = defaultdict(int)
        for m in self.w.ingested():
            if not m.is_canary:
                compte[(m.sender_identity, m.channel, m.day)] += 1
        suspects = 0
        for ident in sorted(self.w.identities, key=lambda i: i.identity_id):
            jours = [d for d in self.w.days if ident.identity_id in self.w.captured_identities(d, ident.channel)]
            if len(jours) < 5:
                continue
            volumes = [compte[(ident.identity_id, ident.channel, d)] for d in jours]
            if statistics.median(volumes) < mediane_min:
                continue
            for d, v in zip(jours, volumes):
                if v == 0:
                    suspects += 1
                    self._exception(
                        "C08", f"{ident.identity_id}/{d.isoformat()}",
                        f"aucun message le {d.isoformat()} alors que la médiane quotidienne "
                        f"est de {statistics.median(volumes):.0f}",
                        opened_on=d,
                    )
        self._result("C08", "toutes identités", "fenêtre", 0, suspects,
                     "ok" if not suspects else "ko",
                     f"{suspects} journée(s) de silence anormal")

    # ---------------------------------------------------------- niveau 3 : fidélité

    def c09_pieces_jointes(self) -> None:
        """Pièces jointes présentes et intègres. Un message archivé sans sa pièce jointe
        n'est pas un enregistrement complet : le record doit être auto-portant."""
        pj_manquantes = hash_divergents = controles = 0
        for m in self.w.ingested():
            receipt = self.w.receipts.get(m.key)
            if receipt is None:
                continue
            controles += 1
            if receipt.attachment_count != len(m.attachments):
                pj_manquantes += 1
                self._exception(
                    "C09", m.source_id,
                    f"{len(m.attachments)} pièce(s) jointe(s) attendue(s), "
                    f"{receipt.attachment_count} archivée(s)",
                    opened_on=m.day,
                )
            if receipt.stored_hash != m.content_hash:
                hash_divergents += 1
                self._exception(
                    "C09", m.source_id,
                    "hash stocké différent du hash d'origine : altération ou re-encodage",
                    opened_on=m.day, due=2,
                )
        total = pj_manquantes + hash_divergents
        self._result("C09", "messages archivés", "fenêtre", 0, total,
                     "ok" if not total else "ko",
                     f"{controles} messages vérifiés, {pj_manquantes} pièce(s) jointe(s) manquante(s), "
                     f"{hash_divergents} hash divergent(s)")

    def c10_editions(self) -> None:
        """Un message édité doit produire une version, pas un écrasement : sinon l'archive
        documente un état et non une conversation."""
        ecrasees = 0
        for m in self.w.ingested():
            if m.edited_from is None:
                continue
            v1 = f"{m.edited_from}#v1"
            if v1 not in self.w.receipts:
                ecrasees += 1
                self._exception(
                    "C10", m.source_id,
                    f"version initiale {v1} absente de l'archive alors que la v{m.version} y est : "
                    "édition traitée comme un écrasement",
                    opened_on=m.day,
                )
        self._result("C10", "messages édités", "fenêtre", 0, ecrasees,
                     "ok" if not ecrasees else "ko",
                     f"{ecrasees} version(s) initiale(s) perdue(s)")

    def c11_fraicheur(self) -> None:
        """Latence captation → archive contre SLA, en p95 et non en moyenne :
        la moyenne cache exactement les incidents qu'on cherche."""
        par_jour: dict[tuple[Channel, date], list[float]] = defaultdict(list)
        for m in self.w.ingested():
            receipt = self.w.receipts.get(m.key)
            if receipt is None:
                continue
            par_jour[(m.channel, m.day)].append((receipt.acknowledged_at - m.sent_at).total_seconds() / 60)
        globales: list[float] = []
        for (ch, day), latences in sorted(par_jour.items(), key=lambda kv: (kv[0][1], kv[0][0].value)):
            globales += latences
            p95 = _p95(latences)
            verdict = "ok" if p95 <= self.w.sla_minutes else "ko"
            self._result("C11", ch.value, day.isoformat(), self.w.sla_minutes, round(p95, 1), verdict,
                         f"{len(latences)} messages, médiane {statistics.median(latences):.0f} min")
            if verdict == "ko":
                self._exception(
                    "C11", f"{ch.value}/{day.isoformat()}",
                    f"p95 de latence {p95:.0f} min pour un SLA de {self.w.sla_minutes} min",
                    opened_on=day, due=10,
                )
        self.journal.append("latency_summary", p95_global=round(_p95(globales), 1), n=len(globales))

    def c12_lisibilite(self) -> None:
        """Présent mais illisible équivaut à absent le jour de la restitution."""
        illisibles = [m for m in self.w.ingested() if not m.readable]
        for m in illisibles:
            self._exception(
                "C12", m.source_id,
                "message chiffré archivé sans être déchiffrable : inexploitable en restitution",
                opened_on=m.day,
            )
        self._result("C12", "messages archivés", "fenêtre", 0, len(illisibles),
                     "ok" if not illisibles else "ko",
                     f"{len(illisibles)} message(s) chiffré(s) non exploitable(s)")

    # --------------------------------------------------------- preuve et restitution

    def c13_integrite_preuve(self, echantillon: int = 60) -> None:
        """Chaîne de hash vérifiée, plus relecture d'un échantillon comme on relirait
        un support WORM. C'est le contrôle qui rend la preuve opposable."""
        intacte, explication = self.journal.verify()
        archives = sorted(self.w.receipts.values(), key=lambda r: r.message_key)[:echantillon]
        par_cle = {m.key: m for m in self.w.ingested()}
        divergences = sum(
            1 for r in archives
            if r.message_key in par_cle and par_cle[r.message_key].content_hash != r.stored_hash
        )
        verdict = "ok" if intacte and not divergences else "ko"
        if not intacte:
            self._exception("C13", "journal d'audit", explication, opened_on=self.w.end, due=0)
        if divergences:
            self._exception(
                "C13", "relecture WORM",
                f"{divergences} divergence(s) de hash sur un échantillon de {len(archives)}",
                opened_on=self.w.end, due=2,
            )
        self._result("C13", "piste d'audit + archive", "fenêtre", 0, divergences, verdict,
                     f"{explication}, {len(archives)} enregistrements relus")

    def c14_restitution(self, tirages: int = 3) -> None:
        """Tirage à l'aveugle : délai jusqu'à l'export, exhaustivité contre un jeu de
        référence connu. Trois répétitions suffisent à transformer un débat en courbe."""
        essais = drill(self.w, self.index, n=tirages, seed=self.w.seed + 11)
        cible = targeted_drill(self.w, self.index)
        if cible is not None:
            essais.append(cible)
        for essai in essais:
            self.drills.append(essai)
            verdict = "ok" if essai["recall"] >= 1.0 and essai["elapsed_ms"] <= RETRIEVAL_SLA_MS else "ko"
            self._result(
                "C14", essai["scope"], essai["window"], 1.0, round(essai["recall"], 4), verdict,
                f"{essai['found']}/{essai['expected']} retrouvés en {essai['elapsed_ms']:.0f} ms",
            )
            if verdict == "ko":
                self._exception(
                    "C14", essai["scope"],
                    f"restitution incomplète : {essai['found']}/{essai['expected']} messages "
                    f"({essai['recall']:.1%}) sur {essai['window']}",
                    opened_on=self.w.end, due=1,
                )
            self.journal.append(
                "retrieval_drill", scope=essai["scope"], window=essai["window"],
                expected=essai["expected"], found=essai["found"],
                recall=round(essai["recall"], 4), elapsed_ms=round(essai["elapsed_ms"], 1),
            )

    def c15_controle_du_controle(self) -> None:
        """Un contrôle qui n'a pas tourné doit être aussi visible qu'un contrôle en échec."""
        non_executes = [r for r in self.results if r.verdict == "non exécuté"]
        joues = {r.control_id for r in self.results}
        absents = [cid for cid in CATALOGUE if cid not in joues and cid != "C15"]
        for r in non_executes:
            self._exception(
                "C15", f"{r.control_id}/{r.scope}/{r.period}",
                f"contrôle {r.control_id} sans résultat pour {r.period} : {r.detail}",
                opened_on=date.fromisoformat(r.period) if _is_iso(r.period) else self.w.end,
                due=1,
            )
        for cid in absents:
            self._exception("C15", cid, f"contrôle {cid} jamais exécuté sur la fenêtre",
                            opened_on=self.w.end, due=1)
        total = len(non_executes) + len(absents)
        self._result("C15", "catalogue", "fenêtre", 0, total,
                     "ok" if not total else "ko",
                     f"{len(self.results)} résultats produits, {len(non_executes)} non exécuté(s), "
                     f"{len(absents)} contrôle(s) absent(s)")

    # ------------------------------------------------------------------ exécution

    def run(self) -> "Run":
        self.journal.append(
            "run_started", window=f"{self.w.start.isoformat()}..{self.w.end.isoformat()}",
            seed=self.w.seed, parties=len(self.w.parties), batches=len(self.w.batches),
        )
        for batch in self.w.batches:
            self.journal.append(
                "batch_received", batch_id=batch.batch_id, channel=batch.channel.value,
                day=batch.day.isoformat(), declared=batch.declared_count, delivered=len(batch.messages),
            )
        self.c01_couverture()
        self.c02_orphelins()
        self.c03_entitlements()
        self.c04_latence_arrivees()
        self.c05_departs()
        self.c06_source_vers_ingestion()
        self.c07_ingestion_vers_archive()
        self.c08_continuite()
        self.c09_pieces_jointes()
        self.c10_editions()
        self.c11_fraicheur()
        self.c12_lisibilite()
        self.c14_restitution()
        self.c15_controle_du_controle()
        self.c13_integrite_preuve()  # en dernier : il vérifie le journal qui précède
        self.journal.append(
            "run_finished", results=len(self.results), exceptions=len(self.exceptions),
            ko=sum(1 for r in self.results if r.verdict == "ko"),
        )
        return self

    # ------------------------------------------------------------------ synthèse

    def oldest_open_gap(self, as_of: date | None = None) -> int:
        """Ancienneté du plus vieil écart ouvert — le meilleur indicateur unique du programme."""
        as_of = as_of or (self.w.end + timedelta(days=1))
        ouvertes = [e for e in self.exceptions if e.status.value == "ouverte"]
        return max((e.age_days(as_of) for e in ouvertes), default=0)

    def detected_controls(self) -> set[str]:
        return {e.control_id for e in self.exceptions}


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(int(round(0.95 * (len(ordered) - 1))), len(ordered) - 1)
    return ordered[idx]


def _is_iso(text: str) -> bool:
    try:
        date.fromisoformat(text)
        return True
    except ValueError:
        return False
