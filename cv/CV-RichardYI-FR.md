# Richard YI

**Lead Solution Architect — Data, Recordkeeping & Réconciliation**

*Candidature — Lead Solution Architect / Technical Lead, programme E-Communications Recordkeeping & Reconciliation (Paris, oct. 2026)*

Paris, France — disponible sur site · [[À COMPLÉTER : téléphone]] · [[À COMPLÉTER : e-mail]] · [[À COMPLÉTER : LinkedIn]] · Français (natif) · Anglais [[À COMPLÉTER : niveau + contexte]]

> **BROUILLON — 40 trous à combler.** Chaque `[[...]]` est un fait que seul Richard peut fournir. Voir `cv/README.md`.

## Profil

Architecte de solutions data, hands-on. Je conçois et je fais atterrir des chaînes de données réglementées de bout en bout : captation multi-sources, normalisation, rapprochement, contrôles automatisés, piste d'audit inaltérable, restitution à la demande. [[À COMPLÉTER : X ans d'expérience, dont Y en banque / marchés financiers — nommer ici les deux institutions les plus fortes de ton parcours, c'est la ligne que le recruteur lit en premier]]. Je prototype moi-même, je documente le lineage de ce que je livre, et je tiens le sujet devant une DSI comme devant des équipes Operations, Risk et Compliance.

## Ce que j'apporte sur ce programme

- **Cohérence end-to-end, pas une collection de connecteurs.** Un modèle de données unique des sources (Exchange/O365, Teams, Bloomberg IB & MSG, voix, mobile) jusqu'aux systèmes d'archivage, et un contrat d'interface explicite par source : format, clés, horodatage, complétude attendue, comportement en cas de retard ou de rejeu.
- **Complétude démontrable à trois niveaux.** Réconciliation des populations (RH / annuaire / entitlements contre comptes réellement journalisés), des volumétries (compté à la source contre ingéré contre archivé) et de la fidélité (pièces jointes, éditions, suppressions, fils, participants). Chaque écart est daté, imputé, expliqué.
- **Des contrôles qui produisent des exceptions traçables.** Chaque contrôle a un propriétaire, un seuil, une fréquence, une file d'exceptions et un SLA. Une exception est un objet de données avec un cycle de vie, pas un e-mail de relance.
- **Une piste d'audit qui tient sans la bonne foi de l'exploitant.** Journal append-only hash-chaîné, stockage immuable (WORM), pack de preuve reconstituable à froid : ce qui a été capté, par quel chemin, quand, avec quelle règle dans quelle version.
- **La retrievability se mesure, elle ne se promet pas.** Le seul test qui compte est de retrouver et d'exporter un périmètre de communications dans le délai imposé, à l'aveugle, en enregistrant le temps et l'exhaustivité. Je fais entrer ce test dans le PoC.
- **Un PoC conçu pour être promu ou jeté.** Périmètre réduit — une population, deux sources — mais mêmes contrats d'interface, mêmes contrôles et mêmes critères de sortie que la cible, afin que la décision de build ne se prenne pas sur une démo.

## Compétences clés

**Architecture & intégration de données** — Architecture cible et trajectoire · contrats d'interface et modélisation · ingestion batch et quasi-temps réel, CDC, event streaming · orchestration et ordonnancement · idempotence, rejeu, reprise sur incident, backfill · gestion des arrivées tardives et de l'ordre des événements · documentation d'architecture (C4, ADR) [[À COMPLÉTER : garder les technologies que tu maîtrises réellement — Kafka, Spark, dbt, Airflow, Control-M, SQL, Python, cloud Azure/AWS/GCP — et supprimer les autres]]

**Matching & réconciliation** — Rapprochement déterministe et probabiliste · résolution d'identité (personne ↔ comptes ↔ terminaux ↔ population supervisée) · définition des clés, tolérances et règles de bris · réconciliation de complétude et de volumétrie · break management, requalification, aging des écarts · contrôle du contrôle (réconciliation de la réconciliation)

**Data quality & automatisation des contrôles** — Dimensions complétude, exactitude, unicité, fraîcheur, conformité de format · contrôles embarqués dans le pipeline plutôt qu'en aval · seuils, scoring, tendance · automatisation des contrôles de niveau 1 et production de la preuve pour le niveau 2 · tableaux de contrôle pour Operations et Compliance

**Data lineage & gouvernance** — Lineage technique et fonctionnel · traçabilité exigence réglementaire → règle → champ → source · versioning des règles et rejouabilité de l'historique · dictionnaire de données et propriété · catalogage et cartographie [[À COMPLÉTER : Collibra, Informatica, Solidatus, OpenMetadata, DataHub — ne garder que le vécu]]

**Recordkeeping & archivage des communications électroniques** — Journalisation Exchange / Exchange Online · Teams (API d'export Graph, Purview, pièces jointes déportées) · Bloomberg IB et MSG, entitlements, Vault · rétention, légal hold, politiques de conservation · immutabilité WORM (Object Lock, blob immuable) · indexation, recherche et export e-discovery · dédoublonnage et conservation de la preuve de distribution

**Réglementaire traduit en exigences techniques** — MiFID II art. 16(7) et règlement délégué (UE) 2017/565 art. 76 (conservation 5 ans, 7 sur demande de l'autorité) · SEC 17a-4(f) et l'alternative « audit trail » ouverte par les amendements de 2022 · FINRA 3110 / 4511, CFTC 1.31 et 1.35 · RGPD : minimisation, durées, droits des collaborateurs, doctrine CNIL · DORA : dépendance à un archiveur tiers, testabilité, plan de sortie

**Delivery & interlocuteurs** — Cadrage et conception de PoC · build, plan de recette, UAT, bascule en production · animation d'ateliers et comitologie · interface IT / Operations / Risk / Compliance · arbitrage entre exigence réglementaire, faisabilité et délai · conduite en anglais professionnel

## Expérience

### [[À COMPLÉTER : intitulé — ex. Solution Architect Data / Tech Lead]] — [[À COMPLÉTER : banque ou institution financière]]

*[[À COMPLÉTER : ville]] · [[À COMPLÉTER : période]]*

[[À COMPLÉTER : en une phrase — quel domaine (marchés, risque, conformité, back-office), quel périmètre de données, combien de sources, quelle volumétrie, quelle taille d'équipe.]]

- [[À COMPLÉTER : le rapprochement le plus difficile que tu as conçu. Deux sources censées dire la même chose, les clés retenues, le taux de match atteint, ce que tu as fait des bris.]]
- [[À COMPLÉTER : un contrôle manuel que tu as automatisé. Avant : combien de temps, par qui, avec quel taux d'erreur. Après : la même mesure.]]
- [[À COMPLÉTER : une exigence réglementaire que tu as transformée en exigence technique testable, et comment tu as prouvé qu'elle était tenue.]]
- [[À COMPLÉTER : le passage en production. Ce que tu as porté jusqu'à l'UAT, la bascule, ce qui a cassé et comment tu l'as tenu.]]

Stack : [[À COMPLÉTER : technologies réellement utilisées]]

### [[À COMPLÉTER : intitulé]] — [[À COMPLÉTER : organisation — banque, marchés, ou environnement réglementé]]

*[[À COMPLÉTER : ville]] · [[À COMPLÉTER : période]]*

[[À COMPLÉTER : même logique. Si le poste est ancien, deux puces suffisent — garde la place pour ce qui est le plus proche de la réconciliation, du lineage et de la data quality.]]

- [[À COMPLÉTER : réalisation 1, chiffrée]]
- [[À COMPLÉTER : réalisation 2, chiffrée]]

Stack : [[À COMPLÉTER : technologies]]

### Président — architecte de la plateforme — MedicalCity SASU

*Paris · [[À COMPLÉTER : mois]] 2026 — aujourd'hui*

Infrastructure data en environnement fortement réglementé (données de santé) : conception et réalisation de la plateforme, du cadre de conformité et de la trajectoire technique. Rôle d'architecte hands-on autant que de dirigeant.

- **Golden record multi-sources (Bayon).** Chaîne d'ingestion, mapping vers un modèle canonique normalisé FHIR R4, résolution d'identité et constitution d'un enregistrement de référence en moins de 30 s ; livrée en PoC forfaitaire de 8 semaines avec jalons de recette contractuels (40 % commande / 40 % mi-parcours / 20 % recette).
- **Piste d'audit inaltérable.** Journal append-only hash-chaîné et journalisation WORM de chaque décision automatisée : rejouer à froid ce qui a été décidé, par quelle règle et sur quelle donnée.
- **Automatisation des contrôles avec gestion des exceptions.** Paliers de décision explicites — AUTO, RECOMMENDED, MANDATORY — le dernier imposant une validation humaine tracée. Le silence n'est pas un accord : une recommandation non signée sous 48 h est un refus. C'est un modèle de contrôle de niveau 1 automatisé avec file d'exceptions et séparation des rôles.
- **Exigences réglementaires traduites en contraintes d'architecture.** Hébergement en France, contrats de sous-traitance (DPA), interdiction stricte de données sensibles dans le dépôt de code, dossier d'hébergement de données de santé, registre AI Act tenu à jour — chaque exigence convertie en règle vérifiable dans la chaîne de livraison plutôt qu'en engagement déclaratif.
- **Interface avec des fonctions de contrôle.** Conception et animation d'une comitologie hebdomadaire séparant l'exécution des décisions réservées (contrats, données de santé, engagements), sur le modèle d'un comité de risque.

Stack : [[À COMPLÉTER : stack réelle de la plateforme — langages, ingestion, stockage, CI, cloud]]

### [[À COMPLÉTER : rôle chez GEOVTC]] — GEOVTC

*[[À COMPLÉTER : ville]] · [[À COMPLÉTER : période]]*

[[À VÉRIFIER — reconstitué à partir de tes documents internes : offre d'« IA factory » et de diagnostic court pour ETI. Corrige ou supprime ce bloc s'il ne correspond pas.]]

- [[À COMPLÉTER : ce que tu as construit et pour quels volumes / clients]]
- [[À COMPLÉTER : ce qui est transposable au poste — intégration de données, automatisation de contrôles, industrialisation]]

Stack : [[À COMPLÉTER : technologies]]

## Pièce joignable

Note d'architecture de 3 pages — « PoC E-Communications Recordkeeping & Reconciliation : périmètre, modèle de réconciliation, catalogue de contrôles, critères de sortie » — rédigée pour ce programme et disponible sur demande.

## Formation

- [[À COMPLÉTER : diplôme, établissement, année]]
- [[À COMPLÉTER : diplôme ou certification complémentaire — les certifications cloud / architecture / data governance comptent ici]]

## Langues

- Français — langue maternelle
- Anglais — [[À COMPLÉTER : niveau. Ne pas écrire « courant » sans preuve : nomme la situation réelle (comitologie en anglais, équipe offshore, client anglophone, mission à l'étranger). C'est éliminatoire sur ce poste.]]
- [[À COMPLÉTER ou supprimer : autre langue]]

## Disponibilité & modalités

- Paris et Île-de-France, présence sur site
- Démarrage compatible avec une montée en charge progressive à partir d'octobre 2026
- [[À COMPLÉTER : statut de facturation — société, portage, salarié]]
- [[À COMPLÉTER : TJM cible et nombre de jours par semaine]]
