# Vocabulaire et mots-clés

Deux usages : passer les filtres (le recruteur cherche ses propres mots) et parler juste (rien n'expose plus vite qu'un mot employé de travers).

## 1. Les mots exacts de l'annonce — à retrouver dans le CV

Le CV les contient déjà, sauf mention contraire. À vérifier après chaque modification.

| Terme de l'annonce | Présent | Où |
|---|---|---|
| Lead Solution Architect / Technical Lead | oui | Titre |
| E-Communications Recordkeeping | oui | Titre de candidature, compétences |
| Reconciliation / réconciliation | oui | Compétences, apport, expériences |
| Data lineage | oui | Compétences |
| Data quality | oui | Compétences |
| Matching | oui | Compétences |
| Control automation / automatisation des contrôles | oui | Compétences, MedicalCity |
| Exception management / gestion des exceptions | oui | Apport, MedicalCity |
| Audit trail / piste d'audit | oui | Apport, MedicalCity |
| Reporting | oui | Compétences delivery, apport |
| Retrievability | oui | Apport |
| Journalization / journalisation | oui | Compétences recordkeeping |
| Archiving / archivage | oui | Compétences recordkeeping |
| Microsoft Exchange / O365 | oui | Compétences recordkeeping |
| Teams | oui | Compétences recordkeeping |
| Bloomberg | oui | Compétences recordkeeping |
| Data integration / intégration de données | oui | Compétences architecture |
| PoC | oui | Apport, MedicalCity |
| UAT | oui | Compétences delivery |
| Banking / marchés financiers | **à compléter** | Bloc expérience bancaire |
| Hands-on | oui | Profil |
| IT / Operations / Risk / Compliance | oui | Compétences delivery |
| Anglais professionnel | **à compléter** | Langues |

## 2. Correspondances FR ⇄ EN

Utile pour la version anglaise et pour l'entretien en anglais, qui aura lieu si le client est international.

| Français | English |
|---|---|
| rapprochement, réconciliation | reconciliation, matching |
| écart | break, discrepancy, gap |
| gestion des écarts | break management |
| ancienneté des écarts | ageing |
| complétude | completeness |
| exactitude | accuracy |
| fraîcheur | timeliness, freshness |
| piste d'audit | audit trail |
| inaltérable, non réinscriptible | tamper-evident, WORM (write once read many) |
| conservation, durée de conservation | retention, retention period |
| conservation à titre probatoire | legal hold |
| restitution, recherche et export | retrievability, retrieval, e-discovery export |
| journalisation | journalling (UK) / journaling (US) |
| population supervisée | supervised population, in-scope population |
| habilitations, droits d'accès | entitlements |
| arrivées / mobilités / départs | joiners, movers, leavers (JML) |
| contrôle de niveau 1 / 2 | first line / second line control |
| séparation des tâches | segregation of duties |
| lignage, traçabilité des données | data lineage |
| dictionnaire de données | data dictionary, business glossary |
| propriétaire de la donnée | data owner / data steward |
| recette, recette utilisateur | testing, UAT |
| bascule, mise en production | cut-over, go-live |
| reprise sur incident, rejeu | recovery, replay |
| arrivée tardive | late-arriving data |
| exigence réglementaire | regulatory requirement |
| dossier de preuve | evidence pack |

## 3. Formulations qui portent (et leurs versions faibles)

| À éviter | À dire |
|---|---|
| « J'ai participé à la mise en place d'un outil de réconciliation » | « J'ai conçu le rapprochement entre X et Y : clés retenues, tolérances, taux de match de N %, et j'ai tenu la file d'écarts jusqu'à l'audit » |
| « Je connais la data quality » | « J'ai embarqué N contrôles dans le pipeline, avec seuils et propriétaires, dont M automatisés à partir d'un contrôle manuel » |
| « Bonne connaissance du réglementaire » | « J'ai traduit l'exigence de conservation en règle testable : durée, immutabilité, preuve de restitution, et je sais montrer le test » |
| « Je suis hands-on » | « Le prototype est de moi ; voici comment il gère le rejeu et l'arrivée tardive » |
| « Anglais courant » | « Comitologie hebdomadaire en anglais avec l'équipe de Londres et l'archiveur » — nommer la situation |
| « Architecte end-to-end » | « J'ai porté la même chaîne de la captation à la restitution, avec un contrat d'interface par source » |

## 4. Cinq mots à ne pas employer à la légère

- **WORM** : ne dis pas WORM si tu veux dire « sauvegarde ». WORM signifie non réinscriptible pendant la durée de rétention, verrouillé au niveau du stockage.
- **Immuable** : une base append-only n'est pas immuable si l'administrateur peut supprimer la table. L'immutabilité se prouve au niveau du support et de la politique de rétention.
- **Journalisation** : côté Microsoft, c'est un mécanisme précis (règle de journal, point de remise), pas « on garde les logs ».
- **Lineage** : si tu ne peux pas répondre à « d'où vient ce chiffre » en remontant jusqu'au lot reçu, ce n'est pas du lineage, c'est un schéma.
- **Réconciliation** : rapprocher deux extractions de la même base n'est pas une réconciliation. Il faut deux sources indépendantes — c'est exactement le piège du recordkeeping, où l'on est tenté de comparer l'archive à elle-même.
