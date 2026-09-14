"""Ligne de commande du prototype.

    python3 -m recon                 # exécution complète + rapport
    python3 -m recon --seed 12       # autre monde synthétique
    python3 -m recon --verifie       # vérifie que chaque défaut injecté est détecté
    python3 -m recon --falsifie      # altère le journal et montre que la chaîne le détecte
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from . import audit, controls, report, synth

OUT = Path(__file__).resolve().parent / "out"


def _exceptions_csv(run: controls.Run, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["exception_id", "control_id", "gravite", "perimetre", "proprietaire",
             "ouverte_le", "age_jours", "hors_delai", "statut", "cause"]
        )
        as_of = run.w.end
        for e in run.exceptions:
            writer.writerow([
                e.exception_id, e.control_id, e.severity.value, e.scope, e.owner,
                e.opened_on.isoformat(), e.age_days(as_of), "oui" if e.overdue(as_of) else "non",
                e.status.value, e.cause,
            ])


def _verifie_detection(world: synth.World, run: controls.Run) -> int:
    """La vérité terrain est la liste des défauts injectés : chacun porte l'identifiant
    du contrôle censé le trouver."""
    detectes = run.detected_controls()
    attendus = sorted({d.control_id for d in world.defects})
    manques = [cid for cid in attendus if cid not in detectes]
    print("\nDéfauts injectés et contrôle censé les détecter :\n")
    for d in world.defects:
        etat = "détecté" if d.control_id in detectes else "NON DÉTECTÉ"
        print(f"  {d.control_id}  {etat:<12} {d.scope:<28} {d.description}")
    print()
    if manques:
        print(f"échec : aucune exception ouverte pour {', '.join(manques)}")
        return 1
    print(f"{len(world.defects)} défauts injectés, {len(attendus)} contrôles concernés, tous ont produit "
          "au moins une exception.")
    return 0


def _falsifie(run: controls.Run) -> int:
    """Démonstration : une altération du journal est détectée sans faire confiance à personne."""
    journal = run.journal
    ok, message = journal.verify()
    print(f"avant   : {message}")
    entries = journal._entries  # noqa: SLF001 — accès assumé : on joue l'exploitant malveillant
    cible = next(
        (e for e in entries if e.kind == "control_result" and e.payload.get("verdict") == "ko"),
        entries[len(entries) // 2],
    )
    print(f"cible   : entrée {cible.seq} ({cible.kind}, {cible.payload.get('control_id')} "
          f"{cible.payload.get('period')}) — on maquille le verdict en « ok »")
    entries[cible.seq - 1] = type(cible)(
        seq=cible.seq, at=cible.at, kind=cible.kind,
        payload={**cible.payload, "verdict": "ok", "observed": cible.payload.get("expected")},
        prev_hash=cible.prev_hash, hash=cible.hash,
    )
    ok2, message2 = journal.verify()
    print(f"après   : {message2}")
    if ok and not ok2:
        print("\nla falsification d'une seule entrée invalide la chaîne : c'est ce que doit produire "
              "une piste d'audit opposable.")
        return 0
    print("\néchec : l'altération n'a pas été détectée")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=7, help="graine du monde synthétique")
    ap.add_argument("--personnes", type=int, default=24)
    ap.add_argument("--jours", type=int, default=30)
    ap.add_argument("--verifie", action="store_true", help="vérifier la détection des défauts injectés")
    ap.add_argument("--falsifie", action="store_true", help="démontrer la détection d'une altération")
    ap.add_argument("--out", type=Path, default=OUT, help="répertoire de sortie")
    args = ap.parse_args(argv)

    world = synth.build(seed=args.seed, n_parties=args.personnes, window_days=args.jours)
    run = controls.Run(world, audit.AuditJournal(rules_version="1.0.0")).run()

    print(report.console(world, run))

    args.out.mkdir(parents=True, exist_ok=True)
    rapport = args.out / "rapport.md"
    rapport.write_text(report.render(world, run), encoding="utf-8")
    journal_path = run.journal.write(args.out / "audit.jsonl")
    exceptions_path = args.out / "exceptions.csv"
    _exceptions_csv(run, exceptions_path)
    print(f"\nrapport            {rapport}")
    print(f"piste d'audit      {journal_path}")
    print(f"exceptions         {exceptions_path}")

    code = 0
    if args.verifie:
        code |= _verifie_detection(world, run)
    if args.falsifie:
        code |= _falsifie(run)
    return code
