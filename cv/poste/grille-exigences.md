# Grille exigences → preuves

Une ligne par exigence de l'annonce. La colonne **Preuve** est ce qui doit exister *dans le CV ou dans ta bouche en entretien* : un fait daté, chiffré, défendable pendant cinq minutes de questions. La colonne **Statut** est à tenir à jour au fur et à mesure que tu remplaces les `[[À COMPLÉTER]]`.

Statuts : `couvert` (le CV le prouve déjà) · `à compléter` (le CV a un emplacement, il te manque le fait) · `à décider` (choix de positionnement) · `risque` (exigence que tu ne peux pas prouver — voir la stratégie en bas).

## 1. Exigences techniques

| # | Exigence de l'annonce | Preuve attendue | Où dans le CV | Statut |
|---|---|---|---|---|
| 1 | Cohérence technique end-to-end sources → archivage | Une architecture cible que tu as portée seul de la captation à la restitution, avec les contrats d'interface | Accroche + « Ce que j'apporte » + annexe PoC | couvert (via Bayon) + `à compléter` (échelle bancaire) |
| 2 | Architecture et intégration de données | Volumétrie, nombre de sources, mode d'ingestion, mécanismes de reprise | Expériences : lignes « Stack » et « Volumes » | à compléter |
| 3 | Data lineage | Lineage règle → champ → source, outillé ou documenté ; qui s'en sert et pour quoi | Compétences § Lineage + expérience bancaire | à compléter |
| 4 | Matching & reconciliation | Un rapprochement réel : clés, tolérances, taux de match, gestion des bris | Expériences + annexe PoC § modèle de réconciliation | à compléter (fort enjeu) |
| 5 | Data quality | Contrôles DQ automatisés en pipeline, dimensions couvertes, seuils | Compétences § DQ + MedicalCity | couvert partiellement |
| 6 | Contrôles et gestion des exceptions | Une file d'exceptions avec propriétaire, SLA, escalade — pas un fichier Excel | MedicalCity (paliers HITL) + annexe PoC § catalogue de contrôles | couvert |
| 7 | Audit trail | Journal inaltérable : append-only, hash-chaîné, WORM, pack de preuve | MedicalCity (journal WORM, audit hash-chaîné) | couvert |
| 8 | Reporting & retrievability | Un test de restitution mesuré (délai, exhaustivité, format d'export) | Annexe PoC § retrievability | à décider (à mesurer en PoC) |
| 9 | Conception de PoC | Un PoC que tu as cadré, chiffré, livré, avec critères de sortie | MedicalCity (POC forfaitaires 8 semaines, jalons de recette) | couvert |
| 10 | Build → UAT → mise en production | Un passage en production dont tu étais responsable, plan de recette, bascule | Expérience bancaire | à compléter |
| 11 | Environnement bancaire / marchés financiers | Nom des institutions, périmètre métier, durée | Bloc « Expérience — Banque & marchés financiers » | **à compléter — priorité 1** |
| 12 | Control automation | Un contrôle manuel que tu as automatisé, avec l'avant/après | Expériences | à compléter |
| 13 | Recordkeeping / journalization / archiving e-comms | Connaissance des mécanismes de journalisation et des pièges ; à défaut d'expérience directe, maîtrise démontrée | Compétences § Recordkeeping + annexe PoC | couvert en connaissance, `risque` en expérience |
| 14 | Exchange/O365, Teams, Bloomberg | Savoir ce que chaque source sait et ne sait pas produire | Annexe PoC § sources et pièges | couvert en connaissance |
| 15 | Hands-on / prototypage | Du code que tu as écrit toi-même, récemment | MedicalCity + annexe PoC (le PoC est ton échantillon) | couvert |
| 16 | Traduire besoins réglementaires en solutions | Une exigence réglementaire transformée en exigence technique testable | Compétences § Réglementaire + MedicalCity (HDS, AI Act, RGPD) | couvert |
| 17 | Interaction IT / Operations / Risk / Compliance | Comitologie, ateliers, arbitrages tenus face à des fonctions de contrôle | Expériences + « Ce que j'apporte » | à compléter |

## 2. Exigences non techniques

| # | Exigence | Preuve attendue | Statut |
|---|---|---|---|
| 18 | Séniorité | Années d'expérience, taille des équipes influencées, budget des programmes | à compléter |
| 19 | Anglais professionnel solide | Un contexte international vécu, pas une auto-évaluation. Nomme la situation : comitologie en anglais, équipe offshore, client anglophone | **à compléter — priorité 2** |
| 20 | Paris | Présence sur site, pas de sujet | couvert |
| 21 | Démarrage octobre 2026, montée en charge progressive | Compatible avec ton agenda MedicalCity — à arbitrer explicitement | **à décider** |
| 22 | Statut et tarif | Statut de facturation, TJM, jours par semaine | à compléter |

## 3. Les trois écarts à traiter avant d'envoyer

1. **L'expérience bancaire (ligne 11).** C'est le premier filtre du recruteur : il doit lire un nom d'institution financière dans les six premières lignes. Si tu as cette expérience, elle passe *avant* MedicalCity dans le CV — quitte à ce que MedicalCity devienne la dernière ligne. Si tu ne l'as pas, ne la fabrique pas : repositionne le dossier sur « architecte data en environnement réglementé » et accepte que ce poste-là soit un coup à 30 %, en jouant l'annexe PoC comme différenciateur.

2. **Le recordkeeping e-comms (ligne 13).** Personne n'exige une expérience préalable : l'annonce dit « serait particulièrement appréciée ». Ce qui est éliminatoire, c'est de découvrir les pièges en entretien. L'annexe [`poc-ecomms-recordkeeping.md`](../annexes/poc-ecomms-recordkeeping.md) existe pour ça : elle te met au niveau d'un architecte qui a déjà vécu le sujet, à condition que tu la lises comme un document de travail et pas comme un argumentaire.

3. **La réconciliation (ligne 4).** Si aucune de tes expériences n'affiche un rapprochement chiffré, le CV a un trou au centre de la cible. Cherche dans ton parcours tout ce qui rapproche deux sources censées dire la même chose — facturation vs relevés, référentiel RH vs annuaire, stock vs comptabilité, journaux vs base : c'est de la réconciliation, même sans le mot. Puis nomme-le avec le mot.

## 4. Règle de sincérité

Avant envoi, relis chaque ligne du CV et pose la question : *si l'entretien s'arrête vingt minutes sur cette ligne, est-ce que je tiens ?* Si non, la ligne sort. Un CV amputé d'une ligne reste crédible ; un CV pris en défaut sur une ligne perd les autres.
