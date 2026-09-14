# Prototype — réconciliation e-comms

Moteur de réconciliation à trois niveaux pour un programme de *recordkeeping* de communications électroniques, sur données **entièrement synthétiques**. Écrit pour la candidature au poste de Lead Solution Architect (voir [`../cv/README.md`](../cv/README.md)) : c'est la preuve « hands-on » qui accompagne la [note d'architecture](../cv/annexes/poc-ecomms-recordkeeping.md).

Aucune dépendance hors bibliothèque standard, Python 3.11+.

```bash
python3 -m recon --verifie      # exécution + vérification de la détection des défauts injectés
python3 -m recon --falsifie     # altère le journal d'audit et montre que la chaîne le détecte
python3 -m unittest discover -s recon/tests -t .
```

## Ce que ça démontre

Un monde synthétique est généré à partir d'une graine : 24 personnes, trois canaux (Exchange/O365, Teams, Bloomberg), 30 jours, ~7 000 messages, avec des arrivées et des départs dans la fenêtre. Des **défauts sont injectés volontairement**, chacun portant l'identifiant du contrôle censé le détecter — c'est la vérité terrain des tests.

Puis les quinze contrôles du catalogue tournent : populations, volumétrie, fidélité, preuve, restitution, contrôle du contrôle. Sortie :

```
fenêtre            2026-06-01 → 2026-06-30  (6915 messages source)
couverture pop.    96.96%  (45 jours-personne-canal non couverts)
complétude         99.87%  (9 messages manquants)
canaris            88/90 arrivés
latence p95        44 min (SLA 120 min)
contrôles          283 résultats · 16 ko · 1 non exécutés
exceptions         29 ouvertes · plus vieil écart 30 j
restitution        3/4 tirages complets
piste d'audit      412 entrées chaînées, chaîne intègre
```

Trois artefacts sont écrits dans `recon/out/` (non versionné) : `rapport.md` (les six chiffres du dossier de décision, puis le détail), `audit.jsonl` (la piste d'audit hash-chaînée) et `exceptions.csv` (la file d'exceptions avec propriétaire et aging).

## Les défauts injectés

| Contrôle | Défaut | Ce qu'il représente dans la vraie vie |
|---|---|---|
| C01 | Personne supervisée sans journalisation Teams | Paramétrage jamais fait, invisible sans réconciliation de population |
| C02 | Captation active 12 jours après un départ | Processus de sortie non appliqué côté IT |
| C03 | Terminal Bloomberg actif hors liste supervisée | L'écart n'est visible que par les entitlements |
| C04 | Journalisation activée 6 jours après l'entrée RH | Latence joiners, la source la plus fréquente de trous |
| C05 | Entitlement Bloomberg retiré 3 jours avant la sortie | La fenêtre la plus sensible du programme |
| C06 | Lot livrant moins que le décompte déclaré | Un décompte de source est une déclaration, pas une vérité |
| C07 | Messages ingérés sans accusé de l'archive, dont un canari | Trou de chaîne prouvé indépendamment des sources |
| C08 | Journée sans message sur un canal actif | Panne de collecteur : elle se manifeste par du silence |
| C09 | Pièce jointe absente, hash divergent | Record non auto-portant, altération silencieuse |
| C10 | Édition Teams écrasant sa version initiale | L'archive documente un état, pas une conversation |
| C11 | Latence de 6 à 9 h pour un SLA de 2 h | Dérive de fraîcheur, invisible en moyenne, visible en p95 |
| C12 | Messages chiffrés non déchiffrables | Présent mais illisible = absent le jour de la restitution |
| C15 | Lot jamais reçu | Un contrôle qui n'a pas tourné doit être aussi visible qu'un contrôle en échec |

## Deux partis pris qui portent tout le reste

**Le rappel de restitution est mesuré contre la source, pas contre l'archive.** Comparer l'archive à elle-même donne toujours 100 % et ne prouve rien ; c'est le piège classique du recordkeeping. Ici, un message perdu en route ou archivé illisible fait chuter le rappel, ce qui est le comportement recherché.

**Les canaris sont la seule mesure indépendante.** Des messages synthétiques sont émis chaque jour sur chaque canal et leur arrivée dans l'archive est vérifiée. Quand la source déclare un décompte faux, les canaris le disent quand même.

## Organisation du code

| Fichier | Contenu |
|---|---|
| `model.py` | Dix entités, toutes les appartenances datées |
| `synth.py` | Générateur du monde et injection des défauts (vérité terrain) |
| `controls.py` | Les quinze contrôles, une méthode par contrôle |
| `retrieval.py` | Index de restitution, tirages à l'aveugle et tirage ciblé post-incident |
| `audit.py` | Journal append-only hash-chaîné, vérification, pack de preuve |
| `report.py` | Rapport de décision et résumé terminal |
| `cli.py` | Ligne de commande |
| `tests/` | 20 tests : détection de chaque défaut, intégrité de la chaîne, reproductibilité, idempotence du rejeu |

## Ce que ce prototype ne démontre pas

Les connecteurs réels (aucune API Microsoft ni flux Bloomberg n'est appelé), l'immutabilité au stockage (le journal est hash-chaîné, donc l'altération est *détectable* — pas *impossible* comme sur un support verrouillé), l'échelle (quelques milliers de messages en mémoire ; les décisions changent à plusieurs millions par jour) et le déchiffrement (détecté, pas traité). Ces limites sont répétées à la fin du rapport généré, à dessein : un prototype dont on ne sait pas dire les limites ne fait pas décider.
