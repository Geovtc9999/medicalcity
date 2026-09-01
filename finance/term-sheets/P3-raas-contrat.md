# P3 — Contrat RaaS client (spec)

**Parties :** OpCo (ou SASU H0) · bénéficiaire / mandataire SAD / payeur le cas échéant.

## Objet

Mise à disposition d’un robot de **veille / assistance** 24/7 + accès logiciel HITL.  
**Hors objet :** diagnostic, prescription, substitution d’un soignant.

## Économie

- Loyer : 350–750 € HT / mois · **TVA 20 %**  
- Durée : 36 mois ferme, reconduction 12 mois  
- Installation : forfait ou amortie dans le loyer (une ligne, pas les deux)  
- Indexation : ILC ou forfait 2 % / an (avocat)

## Payeurs (tripartite, clauses séparées)

1. Facture au **contractant** (famille ou SAD)  
2. Si APA : le client s’engage à **demander l’inscription** au plan d’aide — MedicalCity ne garantit ni le GIR ni le montant  
3. Mandat de prélèvement SEPA · impayé J+15 = suspension service après mise en demeure (sauf risque personne — protocole CARE)

## Crédit d’impôt / SAP

Clause : avantage fiscal **seulement** si l’organisme est déclaré/agréé à la date de facture. Sinon silence.

## Ops

- Substitution robot 72 h  
- SLA incidents : renvoyer au runbook OPS, pas un 99,99 % inventé  
- Fin de contrat : reprise matériel 10 j · données : politique conservation CARE (pas dans ce contrat au-delà d’un renvoi)

## Cession

Le client **accepte d’avance** la cession du loyer à un établissement de crédit / FleetCo (Dailly / nantissement) — **sans** céder de donnée de santé.
