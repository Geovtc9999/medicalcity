"""Tests du prototype de réconciliation.

    python3 -m unittest discover -s recon/tests -t .

Le test central est `test_chaque_defaut_injecte_est_detecte` : la vérité terrain est la
liste des défauts que le générateur a introduits, chacun portant l'identifiant du
contrôle censé le trouver. Un contrôle qui cesse de détecter son défaut fait échouer la
suite — c'est ce couplage qui empêche le prototype de devenir décoratif.
"""
from __future__ import annotations

import unittest
from datetime import timedelta

from recon import controls, report, retrieval, synth
from recon.audit import AuditJournal
from recon.model import Channel


def build_run(seed: int = 7):
    world = synth.build(seed=seed)
    run = controls.Run(world, AuditJournal(rules_version="test")).run()
    return world, run


class TestDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.world, cls.execution = build_run()

    def test_chaque_defaut_injecte_est_detecte(self) -> None:
        detectes = self.execution.detected_controls()
        for defect in self.world.defects:
            with self.subTest(defect=defect.code):
                self.assertIn(
                    defect.control_id, detectes,
                    f"{defect.control_id} n'a ouvert aucune exception pour {defect.code}",
                )

    def test_tous_les_controles_du_catalogue_produisent_un_resultat(self) -> None:
        joues = {r.control_id for r in self.execution.results}
        self.assertEqual(set(controls.CATALOGUE), joues)

    def test_un_lot_absent_rend_le_controle_non_execute_et_visible(self) -> None:
        non_executes = [r for r in self.execution.results if r.verdict == "non exécuté"]
        self.assertTrue(non_executes, "le lot manquant devrait produire un contrôle non exécuté")
        self.assertTrue(
            any(e.control_id == "C15" for e in self.execution.exceptions),
            "un contrôle non exécuté doit ouvrir une exception C15",
        )

    def test_le_canari_perdu_est_vu_par_la_completude(self) -> None:
        causes = [e.cause for e in self.execution.exceptions if e.control_id == "C07"]
        self.assertTrue(any("canari" in c for c in causes))

    def test_exceptions_toutes_attribuees_et_datees(self) -> None:
        for e in self.execution.exceptions:
            with self.subTest(exception=e.exception_id):
                self.assertTrue(e.owner)
                self.assertTrue(e.scope)
                self.assertGreaterEqual(e.age_days(self.world.end + timedelta(days=1)), 0)

    def test_le_plus_vieil_ecart_ouvert_est_positif(self) -> None:
        self.assertGreater(self.execution.oldest_open_gap(), 0)


class TestPisteAudit(unittest.TestCase):
    def setUp(self) -> None:
        self.world, self.execution = build_run()

    def test_chaine_intacte_apres_execution(self) -> None:
        ok, message = self.execution.journal.verify()
        self.assertTrue(ok, message)

    def test_alteration_de_contenu_detectee(self) -> None:
        journal = self.execution.journal
        entries = journal._entries  # noqa: SLF001
        cible = next(e for e in entries if e.kind == "control_result")
        entries[cible.seq - 1] = type(cible)(
            seq=cible.seq, at=cible.at, kind=cible.kind,
            payload={**cible.payload, "verdict": "maquillé"},
            prev_hash=cible.prev_hash, hash=cible.hash,
        )
        ok, message = journal.verify()
        self.assertFalse(ok)
        self.assertIn("contenu modifié", message)

    def test_suppression_d_entree_detectee(self) -> None:
        journal = self.execution.journal
        del journal._entries[10]  # noqa: SLF001
        ok, message = journal.verify()
        self.assertFalse(ok)

    def test_pack_de_preuve_porte_la_version_des_regles(self) -> None:
        pack = self.execution.journal.evidence_pack(kinds=("control_result",))
        self.assertTrue(pack)
        self.assertTrue(all(entry["rules_version"] == "test" for entry in pack))

    def test_persistance_et_relecture(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = self.execution.journal.write(Path(tmp) / "audit.jsonl")
            relu = AuditJournal.read(path)
            self.assertEqual(len(relu), len(self.execution.journal))
            self.assertTrue(relu.verify()[0])


class TestReproductibilite(unittest.TestCase):
    def test_meme_graine_memes_resultats(self) -> None:
        a_world, a_run = build_run(seed=21)
        b_world, b_run = build_run(seed=21)
        self.assertEqual(len(a_world.source_truth), len(b_world.source_truth))
        self.assertEqual(
            [(r.control_id, r.period, r.verdict, r.observed) for r in a_run.results],
            [(r.control_id, r.period, r.verdict, r.observed) for r in b_run.results],
        )

    def test_graines_differentes_mondes_differents(self) -> None:
        a_world, _ = build_run(seed=21)
        b_world, _ = build_run(seed=22)
        self.assertNotEqual(len(a_world.source_truth), len(b_world.source_truth))

    def test_rejeu_du_meme_lot_est_idempotent(self) -> None:
        """Rejouer un lot déjà ingéré ne doit pas gonfler les compteurs : sans idempotence,
        les décomptes deviennent faux au premier incident."""
        world = synth.build(seed=9)
        avant = len(world.ingested())
        cle_avant = {m.key for m in world.ingested()}
        rejoue = world.batches[3]
        rejoue.messages.extend(list(rejoue.messages))
        dedoublonne = {m.key: m for m in world.ingested()}
        self.assertEqual(len(dedoublonne), avant)
        self.assertEqual(set(dedoublonne), cle_avant)


class TestRestitution(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.world, cls.execution = build_run()

    def test_index_ne_contient_que_l_archive_lisible(self) -> None:
        archives_lisibles = sum(
            1 for m in self.world.ingested()
            if m.key in self.world.receipts and m.readable and not m.is_canary
        )
        self.assertEqual(self.execution.index.size, archives_lisibles)

    def test_rappel_mesure_contre_la_source_et_non_contre_l_archive(self) -> None:
        cible = retrieval.targeted_drill(self.world, self.execution.index)
        self.assertIsNotNone(cible)
        self.assertLess(cible["recall"], 1.0, "le tirage ciblé doit révéler la perte")

    def test_un_tirage_a_l_aveugle_reste_exploitable(self) -> None:
        essais = retrieval.drill(self.world, self.execution.index, n=2, seed=3)
        self.assertEqual(len(essais), 2)
        for essai in essais:
            self.assertGreaterEqual(essai["expected"], 3)
            self.assertLess(essai["elapsed_ms"], 3000)


class TestRapport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.world, cls.execution = build_run()

    def test_statistiques_coherentes(self) -> None:
        s = report.compute(self.world, self.execution)
        for ch in self.world.channels:
            self.assertLessEqual(s.couverts.get(ch, 0), s.attendus.get(ch, 0))
            self.assertLessEqual(s.archives.get(ch, 0), s.declares.get(ch, 0))
        self.assertLess(s.canaris_archives, s.canaris_emis, "un canari perdu est injecté")

    def test_le_rapport_expose_les_six_chiffres_et_ses_limites(self) -> None:
        texte = report.render(self.world, self.execution)
        for attendu in (
            "Couverture de la population",
            "Complétude source → archive",
            "Ancienneté du plus vieil écart ouvert",
            "Coût par million de messages",
            "Ce que ce prototype ne démontre pas",
        ):
            self.assertIn(attendu, texte)

    def test_bloomberg_a_moins_de_population_que_email(self) -> None:
        s = report.compute(self.world, self.execution)
        self.assertLess(s.attendus[Channel.BLOOMBERG], s.attendus[Channel.EMAIL])


if __name__ == "__main__":
    unittest.main(verbosity=2)
