# CV ciblé — Lead Solution Architect / Technical Lead

**Poste :** E-Communications Recordkeeping & Reconciliation — grande banque internationale, Paris, montée en charge à partir d'octobre 2026.
**Pour :** Richard YI.

## Point de départ, à lire d'abord

Aucun CV n'existait dans ce dépôt. Ce dossier n'est donc **pas** un CV adapté : c'est un CV **construit à la structure du poste**, dont tout le contenu vérifiable a été repris de tes documents internes (MedicalCity : golden record multi-sources, journal WORM hash-chaîné, paliers de décision HITL, cadre RGPD / HDS / AI Act), et dont tout ce qui relève de faits que je ne peux pas connaître — expérience bancaire, dates, diplômes, niveau d'anglais, TJM — est laissé en `[[trou]]` explicite.

Rien n'a été inventé. Aucune expérience, aucun employeur, aucune date, aucun chiffre n'a été fabriqué pour faire correspondre le dossier à l'annonce. C'est une contrainte, pas une timidité : sur ce type de mission, un dossier pris en défaut sur un point perd tous les autres.

**Pour finir le CV :** ouvre `data/cv-fr.yml`, remplace chaque `[[...]]` par un fait, relance le build. Le générateur refuse de produire une version « finale » tant qu'il en reste un.

## Contenu du dossier

| Fichier | À quoi ça sert |
|---|---|
| [`CV-RichardYI-FR.md`](CV-RichardYI-FR.md) | Le CV français, rendu lisible pour relecture (généré — ne pas éditer) |
| [`CV-RichardYI-EN.md`](CV-RichardYI-EN.md) | Idem, version anglaise (généré — ne pas éditer) |
| [`data/cv-fr.yml`](data/cv-fr.yml) · [`data/cv-en.yml`](data/cv-en.yml) | **La source de vérité. C'est ici qu'on écrit.** |
| [`poste/annonce.md`](poste/annonce.md) | L'annonce + ce qu'elle dit entre les lignes |
| [`poste/grille-exigences.md`](poste/grille-exigences.md) | Chaque exigence → la preuve attendue → où elle se trouve → statut |
| [`annexes/poc-ecomms-recordkeeping.md`](annexes/poc-ecomms-recordkeeping.md) | **La pièce qui différencie** : note d'architecture du PoC |
| [`annexes/deck-lecture-programme.yml`](annexes/deck-lecture-programme.yml) | Deck 5 slides « ma lecture du programme », pour l'entretien client |
| [`annexes/mots-cles-ats.md`](annexes/mots-cles-ats.md) | Mots-clés de l'annonce, lexique FR/EN, formulations qui portent |
| [`annexes/entretien.md`](annexes/entretien.md) | 10 questions probables, 12 questions à poser, 5 signaux d'alerte |
| [`lettres/reponse-recruteur-fr.md`](lettres/reponse-recruteur-fr.md) | Le mail de réponse, prêt à envoyer |
| [`lettres/cover-letter-en.md`](lettres/cover-letter-en.md) | Version anglaise, pour la boucle côté client |
| [`../recon/`](../recon/README.md) | **Prototype exécutable** du moteur de réconciliation à trois niveaux, sur données synthétiques |

## Générer les documents

```bash
python3 tools/build_cv.py                                        # CV FR + EN : Markdown, HTML, PDF A4
python3 tools/build_cv.py fr --png                               # une langue + un aperçu image
python3 tools/build_cv.py --strict                               # échoue tant qu'il reste un [[trou]]
python3 tools/build_doc.py cv/annexes/poc-ecomms-recordkeeping.md   # la note en PDF présentable
python3 tools/build_slides.py --png                              # le deck 16:9 en PDF
python3 -m recon --verifie                                       # le prototype + vérification des détections
```

Sortie dans `cv/build/` (non versionné) : PDF, HTML et aperçus PNG ; les `.md` du CV sont régénérés dans `cv/`.
Dépendances : Python 3, PyYAML, et Chrome / Chromium pour les PDF (sans Chrome, le Markdown et le HTML sont produits quand même). Le prototype, lui, n'utilise que la bibliothèque standard.

Tant qu'il reste un `[[trou]]`, le PDF porte un filigrane **BROUILLON** et un compteur en haut de page : c'est un garde-fou, pas une décoration — il rend impossible l'envoi accidentel d'un CV à trous.

## Règle de sincérité

Trois règles, dans l'ordre d'importance.

1. **Ne remplace jamais un `[[trou]]` par une approximation flatteuse.** Un trou honnêtement vide vaut mieux qu'une ligne fausse : le premier se comble en entretien, la seconde se paie au *reference check*.
2. **Toute ligne doit tenir vingt minutes de questions.** Relis le CV en te demandant, pour chaque ligne : *si l'entretien s'arrête ici, est-ce que je tiens ?* Sinon, la ligne sort. Cela s'applique particulièrement aux listes de technologies et d'outils : n'y laisse que ce que tu as utilisé.
3. **Ce que tu ne sais pas, dis-le avant qu'on te le demande.** Sur ce poste, l'annonce présente le recordkeeping e-comms comme « particulièrement apprécié », pas comme obligatoire. La bonne réponse n'est donc pas de faire semblant, c'est de montrer que tu maîtrises le raisonnement — d'où l'annexe PoC.

## L'ordre dans lequel avancer

1. **Lire [`poste/grille-exigences.md`](poste/grille-exigences.md)** — c'est le diagnostic : trois écarts à traiter, dont un seul est bloquant (l'expérience bancaire).
2. **Combler les `[[trous]]` de `data/cv-fr.yml`**, en priorité les blocs d'expérience bancaire, l'accroche et l'anglais. `python3 tools/build_cv.py --strict` te dit ce qui reste.
3. **Réordonner les expériences** : si tu as une expérience en banque ou marchés financiers, elle passe **avant** MedicalCity. Le filtre secteur se joue dans les six premières lignes.
4. **Reporter les mêmes faits dans `data/cv-en.yml`** puis relire le lexique de [`mots-cles-ats.md`](annexes/mots-cles-ats.md) § 2.
5. **Envoyer le mail** de [`lettres/reponse-recruteur-fr.md`](lettres/reponse-recruteur-fr.md), CV FR en pièce jointe, note PoC gardée pour le deuxième échange.
6. **Préparer l'entretien** avec [`annexes/entretien.md`](annexes/entretien.md) : deux récits chiffrés suffisent, un rapprochement difficile et un contrôle automatisé. Le deck 5 slides et le prototype sont là pour l'entretien client, pas pour le premier appel — sortir un prototype trop tôt donne l'impression d'avoir déjà décidé de l'architecture.

## Le point à arbitrer, qui n'est pas technique

Cette mission demande une présence à Paris et une montée en charge à partir d'octobre 2026, au moment où le calendrier MedicalCity prévoit le pilote départemental et la préparation du tour de financement. Les deux tiennent difficilement à plein temps. Avant d'envoyer le mail, décide — et écris-le dans le mail — combien de jours par semaine tu engages. Un architecte lead à deux jours par semaine sur un programme de remédiation, c'est un refus déguisé qui coûte trois semaines à tout le monde ; à quatre ou cinq jours, c'est MedicalCity qui absorbe le choc. C'est le seul arbitrage que ce dossier ne peut pas faire à ta place.
