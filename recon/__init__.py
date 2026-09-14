"""Prototype de réconciliation e-comms — recordkeeping bancaire.

Trois niveaux de réconciliation (populations, volumétrie, fidélité), quinze contrôles
avec file d'exceptions, piste d'audit hash-chaînée et exercice de restitution, sur des
données entièrement synthétiques. Aucune dépendance hors bibliothèque standard.

    python3 -m recon --verifie
"""

__all__ = ["audit", "cli", "controls", "model", "report", "retrieval", "synth"]
