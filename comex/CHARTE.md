# Charte du Comex IA — MedicalCity

**Version 1.0 · 20 août 2026 · STRICTEMENT CONFIDENTIEL**  
**Statut :** document de travail Président — à adopter en premier Comex.

## 1. Objet

Cette charte organise le **comité exécutif (Comex)** de MedicalCity, composé d’agents IA exécutifs sous supervision humaine. Elle distingue clairement :

| Instance | Nature | Rôle |
|---|---|---|
| **Associé unique / Président** | Légale (SASU) | Seul organe social. Signature, représentation, responsabilité. |
| **Comex IA** | Opérationnelle | Exécution, packs, recommandations, AUTO. |
| **Comité Qualité & IA** | Réglementaire | Protocoles, incidents, AI Act, MDR. |
| **Comité Risques** | Réglementaire | Cash, HDS, contrats, réputation. |
| **Comité stratégique / Board** | Fiduciaire (post-seed) | Levée, stratégie 18–36 mois, nomination humains. |

MedicalCity est une SASU. **Il n’y a pas de conseil d’administration** tant que les statuts ne le prévoient pas. Le « CA d’agents » est un **Comex opérationnel**, pas un organe social. Créer un CA formel trop tôt dilue la responsabilité du Président sans apporter de protection juridique.

## 2. Principes non négociables

1. **Pouvoir de signer ≠ pouvoir d’exécuter.** Les agents préparent, chiffrent, rédigent, orchestrent. L’humain signe.
2. **Séparation des pouvoirs.** L’AGE n’auto-valide jamais un livrable critique (indépendant verifier).
3. **HITL par criticité** — identique à Bayon : `AUTO` / `RECOMMENDED` / `MANDATORY`.
4. **Un siège = un mandat MECE** = un pack hebdomadaire = un owner de KPI.
5. **Mémoire unique.** Décisions, risques, OKR et packs vivent dans ce dépôt (Git), hashés, horodatés.
6. **Multi-vendor.** Choix de modèle par tâche (capacité, coût, souveraineté, résilience). Pas de lock-in.
7. **Souveraineté sanitaire.** Données de santé en France, HDS-ready, RGPD by design, AI Act documenté.

## 3. Composition du Comex (7 sièges)

| # | Siège | Agent | Mandat en une phrase | Sponsor humain |
|---|---|---|---|---|
| 0 | Président | — | Intention, veto, signature | Richard YI |
| 1 | Orchestration | `age-comex` | Agenda, synthèse pyramidale, arbitrage d’interfaces | Richard YI |
| 2 | Produit & Plateforme | `plat` | Bayon, AGE Factory, apprentissage fédéré, agents métier | Richard YI |
| 3 | Clinique & Conformité | `care` | Protocoles, HDS, AI Act, MDR/ANSM, qualité | Sreypov UM |
| 4 | Finance & Capital | `cfo` | Runway, unit economics, data room, tour seed | Richard YI |
| 5 | Commercial & Institutions | `gtm` | Départements, APA, EHPAD/SAD, conversion LOI | Richard YI |
| 6 | Opérations physiques | `ops` | Flotte RaaS, drones, SLA 24/7, déploiement terrain | Sreypov UM |
| 7 | Stratégie & Scale-up | `strat` | OKR 18 mois, concurrence, Europe, chantiers Comex | Richard YI |

Les agents métier (`apa`, `bayon`, `raas-config`, `drones`, `ir`, `dpo`) **ne votent pas**. Ils livrent au siège Comex de rattachement.

## 4. Quorum et décisions

- **Comex hebdomadaire** : 90 minutes. Quorum = AGE + 4 sièges sur 6 + Président (async possible via pack commenté sous 24 h).
- **AUTO** : l’agent exécute, le Comex audite a posteriori.
- **RECOMMENDED** : accord Président ou délégué sous 48 h. Le silence n’est **pas** un accord.
- **MANDATORY** : veto humain obligatoire. Journal WORM (même standard que Bayon).
- En cas de conflit d’agents : l’AGE formalise les options (max 3), le Président tranche. Interdiction de « moyenne » entre recommandations contradictoires.

## 5. Ce que le Comex ne fait pas

- Ne remplace pas un médecin, un DPO humain, un commissaire aux comptes, un avocat.
- Ne produit pas de claims cliniques publics sans Comité médical.
- Ne négocie pas en son nom avec un département, un investisseur ou un journaliste.
- Ne stocke pas de données de santé dans les prompts ou dans Git.

## 6. Adoption

Cette charte entre en vigueur à la signature du Président. Révision trimestrielle par `strat`, validation MANDATORY.

**Richard YI — Président, MedicalCity SASU**
