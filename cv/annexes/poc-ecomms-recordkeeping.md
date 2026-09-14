# Note d'architecture — PoC E-Communications Recordkeeping & Reconciliation

**Objet :** ce que je proposerais de faire pendant les huit premières semaines, et comment je mesurerais que ça marche.
**Statut :** document de travail rédigé à partir de l'annonce. Les hypothèses marquées *(à confirmer)* dépendent du contexte réel du client — versions, licences, incumbent d'archivage, périmètre réglementaire.

Ce document a deux usages. Pour Richard : se mettre au niveau du sujet avant l'entretien. Pour le client : montrer, avant même d'être en poste, à quoi ressemble la pensée d'architecture qu'il achète. Il est joignable au CV, ou mieux, envoyé après le premier entretien.

---

## 1. Le problème n'est pas l'archivage, c'est la preuve de complétude

Une banque sait archiver. Ce qu'elle a du mal à prouver, c'est que **tout ce qui devait être capté l'a été** : la bonne population, sur tous les canaux autorisés, sans trou, avec les pièces jointes, et retrouvable à la demande. La vague de sanctions internationales sur les *off-channel communications* a déplacé l'exigence du stockage vers la démonstration ; c'est pour cette raison qu'un programme de recordkeeping recrute aujourd'hui un architecte **data et réconciliation**, pas un ingénieur stockage.

Trois questions gouvernent donc toute la conception :

1. **Qui** devait être enregistré, à quelle date, sur quels canaux ? *(populations)*
2. **Combien** de messages ont existé à la source, combien sont arrivés dans l'archive, et que valent les écarts ? *(complétude)*
3. **En combien de temps** puis-je ressortir un périmètre précis, complet, exportable, avec la preuve que rien n'a été altéré ? *(retrievability et piste d'audit)*

Tout ce qui ne sert pas à répondre à ces trois questions sort du PoC.

## 2. Périmètre du PoC

Volontairement étroit, mais complet **de bout en bout** — c'est la seule façon d'apprendre quelque chose de transposable.

| | Choix | Pourquoi |
|---|---|---|
| Population | Une population supervisée d'une entité, incluant des arrivées et des départs sur la fenêtre | La difficulté est dans les mouvements, pas dans le stock |
| Sources | Deux : Exchange/O365 **et** un canal instantané (Teams ou Bloomberg IB/MSG) | Un canal e-mail et un canal conversationnel n'ont ni la même granularité ni les mêmes pièges |
| Fenêtre | 90 jours glissants + 1 semaine de rejeu historique | Le rejeu révèle les hypothèses cachées sur l'ordre et l'idempotence |
| Cible | Archive existante *(à confirmer : incumbent ou bac à sable)* + zone immuable de contrôle | On ne remplace pas l'archive dans un PoC ; on l'instrumente |
| Hors périmètre | Voix, mobile, WhatsApp, supervision lexicale, e-discovery avancé | À cadrer ensuite, avec la même mécanique |

## 3. Chaîne cible en six étages

```
[0] Référentiels        RH, annuaire/AD, entitlements Bloomberg, licences O365,
                        liste supervisée tenue par Compliance
                        → construction du PÉRIMÈTRE ATTENDU, versionné par jour
        |
[1] Captation           journalisation Exchange/EXO · API d'export Teams · flux Bloomberg
                        → chaque source livre un lot horodaté + un décompte déclaré
        |
[2] Normalisation       modèle canonique de message, identités résolues, dédoublonnage,
                        horodatage UTC + décalage d'origine conservé, pièces jointes hachées
        |
[3] Réconciliation      3 niveaux (population / volumétrie / fidélité) + canaris de bout en bout
    & contrôles         → résultats de contrôle, écarts, exceptions avec cycle de vie
        |
[4] Archivage           remise à l'archive + accusé de prise en compte + stockage immuable (WORM)
    & immutabilité      des journaux et des packs de preuve
        |
[5] Restitution         recherche et export, reporting de couverture et de complétude,
    & reporting         pack de preuve auditeur, tableau des exceptions
```

Le point important : **l'étage [0] est le socle**. La plupart des programmes échouent parce qu'ils commencent à [1]. Sans périmètre attendu versionné par jour, la complétude n'a pas de dénominateur, et aucun chiffre produit ensuite n'est défendable.

## 4. Modèle de données minimal

Dix entités suffisent au PoC ; les nommer tôt évite trois mois de débat.

| Entité | Rôle | Clé |
|---|---|---|
| `Party` | La personne physique, indépendamment de ses comptes | identifiant RH |
| `Identity` | Un compte, une adresse, un terminal, un identifiant Bloomberg | identifiant technique + source |
| `PartyIdentity` | Rattachement daté d'une identité à une personne | (party, identity, valide du/au) |
| `SupervisionScope` | Qui est supervisé, sur quels canaux, du … au … | (party, canal, valide du/au) |
| `Channel` | Canal de communication et ses caractéristiques de captation | code canal |
| `Message` | Enregistrement canonique | hash de contenu + identifiant source |
| `Attachment` | Pièce jointe : nom, taille, hash, présence effective | (message, index) |
| `ArchiveReceipt` | Accusé de prise en compte par l'archive | (message, archive, horodatage) |
| `ControlResult` | Exécution d'un contrôle : périmètre, attendu, constaté, verdict | (contrôle, période, périmètre) |
| `Exception` | Écart qualifié, avec propriétaire, cause, SLA, statut | identifiant d'exception |

Deux règles de modélisation qui évitent les impasses : toutes les appartenances sont **datées** (une personne change de rôle, de terminal, d'entité — le périmètre d'hier doit rester reconstituable) ; et un message conserve **sa preuve de distribution** (destinataires, copies) même après dédoublonnage, sinon on perd l'information la plus utile en enquête.

## 5. Le modèle de réconciliation, à trois niveaux

C'est le cœur du poste. Trois niveaux indépendants, jamais confondus dans un même indicateur.

### Niveau 1 — Populations : *qui aurait dû être capté ?*

Rapprochement de quatre référentiels qui ne disent jamais la même chose : RH, annuaire/AD, entitlements (Bloomberg, licences O365), et liste des personnes supervisées tenue par Compliance. Sorties attendues :

- personnes supervisées **sans** captation active sur un canal autorisé → trou de couverture, gravité maximale ;
- comptes journalisés **sans** personne supervisée active → comptes orphelins, boîtes partagées, départs mal traités ;
- délai entre l'événement RH (arrivée, mobilité, départ) et la prise d'effet de la captation → c'est là que se logent la majorité des trous réels.

### Niveau 2 — Volumétrie : *tout ce qui a existé est-il arrivé ?*

Trois comptages, deux rapprochements, par jour, par canal, par population : **compté à la source** (rapport de journalisation, API, flux) → **ingéré** → **archivé et acquitté**. Aucun écart n'est « acceptable » : un écart est soit expliqué (rejeu, message hors périmètre, doublon identifié), soit une exception ouverte. Une tolérance non expliquée est une dette qui se paiera devant un auditeur.

À cela s'ajoute une mesure indépendante des sources, la plus utile en pratique : des **canaris**. Des comptes de test émettent chaque jour, sur chaque canal, des messages synthétiques (avec et sans pièce jointe, avec édition et suppression) ; on vérifie leur arrivée dans l'archive et le délai. Le canari mesure la chaîne réelle sans dépendre de la sincérité des décomptes de la source.

### Niveau 3 — Fidélité : *ce qui est arrivé est-il exploitable ?*

Pièces jointes présentes et intègres (nombre, taille, hash), fil et participants reconstituables, éditions et suppressions conservées **comme versions** et non comme écrasement, contenu lisible et indexable (le chiffrement de bout en bout produit des archives inutilisables si la question n'est pas traitée à l'ingestion), horodatage exploitable en UTC avec le décalage d'origine.

### Et le contrôle du contrôle

Un contrôle qui n'a pas tourné doit être aussi visible qu'un contrôle en échec. Le calendrier d'exécution est lui-même réconcilié : résultat manquant = exception.

## 6. Catalogue de contrôles du PoC

| Id | Contrôle | Question | Fréq. | Seuil | Propriétaire |
|---|---|---|---|---|---|
| C01 | Couverture population | Personne supervisée sans captation active | quotidien | 0 | Compliance IT |
| C02 | Comptes orphelins | Compte journalisé sans personne supervisée active | quotidien | 0 | IT / Ops |
| C03 | Entitlements | Détenteur de terminal Bloomberg hors périmètre de captation | quotidien | 0 | Ops marchés |
| C04 | Latence arrivées | Délai événement RH → captation effective | hebdo | ≤ 1 j ouvré | RH IT |
| C05 | Départs | Captation maintenue jusqu'à désactivation, rétention préservée après | hebdo | 0 écart | IT / Ops |
| C06 | Complétude source → ingestion | Décompte source vs ingéré | quotidien | 0 inexpliqué | Data Ops |
| C07 | Complétude ingestion → archive | Ingéré vs acquitté par l'archive | quotidien | 0 inexpliqué | Data Ops |
| C08 | Continuité temporelle | Intervalle anormal sans message sur un canal actif | quotidien | paramétré par canal | Data Ops |
| C09 | Pièces jointes | Attendues vs archivées, hash conforme | quotidien | 0 écart | Data Ops |
| C10 | Éditions / suppressions | Version conservée, pas d'écrasement | quotidien | 0 écart | Data Ops |
| C11 | Fraîcheur | Latence captation → archive vs SLA | quotidien | p95 < SLA | Data Ops |
| C12 | Lisibilité | Messages chiffrés non exploitables à l'ingestion | quotidien | 0 | IT sécurité |
| C13 | Intégrité de la preuve | Chaîne de hash vérifiée + relecture d'échantillon WORM | hebdo | 0 rupture | Architecture |
| C14 | Restitution | Tirage aléatoire retrouvé et exporté, délai mesuré | hebdo | 100 % / < SLA | Compliance |
| C15 | Contrôle du contrôle | Tous les contrôles ont-ils tourné et produit un résultat ? | quotidien | 0 manquant | Data Ops |

Chaque exception porte : cause présumée, périmètre impacté, propriétaire, échéance, statut, et **aging**. Un tableau d'exceptions sans aging ne sert à rien : c'est l'ancienneté des écarts, pas leur nombre, qui se voit en audit.

## 7. Piste d'audit et pack de preuve

Trois exigences, dans cet ordre :

1. **Append-only et hash-chaîné.** Chaque entrée du journal (réception d'un lot, résultat de contrôle, ouverture ou clôture d'exception, export) chaîne le hash de la précédente. Une modification silencieuse devient détectable sans faire confiance à l'exploitant.
2. **Immutabilité au stockage.** Verrouillage objet ou blob immuable pour les journaux et les packs de preuve, avec une durée de rétention alignée sur la politique réglementaire. Côté US, les amendements de 2022 à la règle SEC 17a-4(f) ont ouvert une alternative fondée sur une piste d'audit vérifiable au WORM strict — utile à connaître, car cela change les options d'architecture *(à confirmer selon les entités concernées)*.
3. **Reconstituable à froid.** Un pack de preuve pour une période donnée doit contenir les décomptes, les résultats de contrôle, les exceptions et leur résolution, **et la version des règles appliquées**. Sans le versionnage des règles, on ne sait pas rejouer l'histoire, et une piste d'audit qu'on ne peut pas rejouer n'est pas une preuve.

## 8. Retrievability : un protocole, pas une promesse

Le test que je ferais entrer dans le PoC, chaque semaine, à l'aveugle : Compliance tire un périmètre (une personne, une plage de dates, un mot-clé), l'équipe le restitue sans préparation. On mesure trois choses : **délai** jusqu'à l'export livré, **exhaustivité** contre un jeu de référence connu, **format** (lisible, avec métadonnées, fil reconstitué, pièces jointes attachées). On enregistre les résultats dans la piste d'audit. Trois répétitions suffisent pour savoir si la cible tient — et pour transformer un débat d'opinion en courbe.

## 9. Lineage : à quoi il sert ici

Le lineage n'est pas un poster pour le comité d'architecture. Sur ce programme il répond à une question précise, posée un jour par un auditeur : *« montrez-moi d'où vient ce chiffre »*. La chaîne à outiller est donc : **exigence réglementaire → règle de contrôle (version) → champ du modèle canonique → champ de la source → lot reçu**. Deux conséquences pratiques : le lineage doit être produit par la chaîne elle-même (déduit du code et des transformations, pas saisi à la main dans un catalogue), et il doit être **daté**, parce que les règles changent et que la question portera sur un état passé.

## 10. Les pièges, source par source

Ce sont eux qui font les six mois de retard. Les connaître avant de dessiner change le dessin.

**Exchange / Exchange Online.** La cible d'un journal ne peut pas être une boîte Exchange Online — Microsoft ne le supporte pas ; il faut un point de remise externe ou une extraction par API/substrat *(à confirmer selon la licence en place)*. Les copies par destinataire produisent des doublons qu'il faut dédoublonner **sans perdre** la preuve de distribution. Les règles de transport, DLP et le chiffrement de messages modifient ou protègent le contenu avant journalisation. Boîtes partagées et délégations cassent l'hypothèse « une boîte = une personne ».

**Teams.** Les messages sont **éditables et supprimables** : sans capture de versions, l'archive documente un état, pas une conversation. Les pièces jointes ne sont pas dans le message mais dans SharePoint/OneDrive : le record n'est pas auto-portant. Réactions, cartes, messages système, canaux privés, chats fédérés ou avec invités, et appels ont chacun leur régime. Côté extraction, les API d'export sont soumises à des quotas et à un modèle de licence à la volumétrie *(à confirmer)* — un coût qui doit entrer dans le dossier de décision, pas se découvrir en production.

**Bloomberg.** Tout est piloté par les **entitlements** : un départ retire l'accès au terminal, ce qui peut aussi supprimer la source de captation — d'où le contrôle C05. IB (conversations) et MSG (messagerie) sont deux flux distincts, avec leurs propres formats, horaires de coupure et pièces jointes. Le rapprochement personne ↔ identifiant Bloomberg ↔ identité RH est rarement automatique, et la moindre mobilité interne le casse.

**Transverse.** Décalages d'horloge et fuseaux (tout stocker en UTC en conservant le décalage d'origine) ; arrivées tardives et rejeux (idempotence obligatoire, sinon les décomptes deviennent faux au premier incident) ; volumétrie des pièces jointes ; tension RGPD entre durée de conservation réglementaire et minimisation, y compris les droits des collaborateurs et l'information des instances représentatives sur les dispositifs de surveillance ; dépendance à un archiveur tiers, qui relève de DORA — testabilité et plan de sortie compris.

## 11. Les huit semaines

| Sem. | Objet | Livrable de sortie |
|---|---|---|
| 1 | Cadrage : périmètre, liste supervisée, accès, décisions ouvertes | Note de cadrage + registre de décisions |
| 2 | Captation source A + décomptes déclarés | Lots ingérés, réconciliation N2 partielle |
| 3 | Captation source B + canaris sur les deux canaux | Premiers délais de bout en bout mesurés |
| 4 | Modèle canonique, résolution d'identité, dédoublonnage | Modèle figé + taux de rattachement |
| 5 | Réconciliation N1 (populations) et N2 (volumétrie) | Tableaux de couverture et de complétude |
| 6 | Contrôles, exceptions, piste d'audit hash-chaînée + WORM | Catalogue outillé + premier pack de preuve |
| 7 | Restitution, reporting, deux exercices à l'aveugle | Courbe délai / exhaustivité |
| 8 | Dossier de décision build | Résultats chiffrés, écarts, coût cible, trajectoire |

**Critères de sortie — chiffrés, pas argumentés.** Part de la population couverte, avec 100 % des écarts expliqués ; taux de complétude par canal, cause identifiée pour chaque écart ; délai médian et p95 de restitution sur les exercices à l'aveugle ; part des contrôles automatisés produisant une exception traçable ; coût par million de messages, licences comprises ; liste des dépendances bloquantes pour l'industrialisation. Si ces six chiffres existent à la semaine 8, la décision de build se prend en une réunion.

## 12. Ce qu'il faut décider avant d'écrire une ligne de code

Six questions à poser dès le premier atelier. Elles sont dans [`entretien.md`](entretien.md) sous forme de questions au client, parce qu'elles servent aussi à jauger la maturité du programme : qui **possède** la liste des personnes supervisées ; quelle est l'archive de référence et que sait-elle acquitter ; quel est le délai de restitution exigé et par qui ; quelles entités juridiques et donc quels régulateurs sont dans le périmètre ; quel outillage de contrôle et de lineage existe déjà et ne doit pas être redoublé ; qui tranche en cas de conflit entre exigence réglementaire et faisabilité.

## 13. Indicateurs à tenir après la mise en production

Couverture (part de la population supervisée effectivement captée) · complétude par canal · **ancienneté du plus vieil écart inexpliqué** — le meilleur indicateur unique du programme · aging des exceptions par propriétaire · délai de restitution p95 · taux d'exécution des contrôles · coût par million de messages.

## 14. Un prototype existe déjà

Le moteur décrit ici — trois niveaux de réconciliation, les quinze contrôles, la file d'exceptions avec propriétaire et aging, la piste d'audit hash-chaînée, les canaris et les tirages de restitution — est implémenté et exécutable sur données synthétiques : [`../../recon/`](../../recon/README.md). Le générateur y injecte des défauts qui portent chacun l'identifiant du contrôle censé les détecter, et les tests échouent si un contrôle cesse de trouver le sien.

Ce n'est pas une offre d'outil : c'est la démonstration que le raisonnement tient jusqu'au code, et une base de discussion pour le cadrage — notamment sur les deux partis pris qui font toute la différence, mesurer le rappel contre la source plutôt que contre l'archive, et disposer d'une mesure indépendante des décomptes de la source.

---

*Rédigé par Richard YI pour le programme E-Communications Recordkeeping & Reconciliation. Les affirmations réglementaires et produits sont données de bonne foi et à vérifier contre la documentation en vigueur et le contexte du client.*
