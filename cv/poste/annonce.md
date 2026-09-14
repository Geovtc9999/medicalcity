# Annonce — Lead Solution Architect / Technical Lead

| | |
|---|---|
| **Intitulé** | Lead Solution Architect / Technical Lead |
| **Programme** | E-Communications Recordkeeping & Reconciliation |
| **Client final** | Grande banque internationale (via cabinet / ESN) |
| **Lieu** | Paris (principalement) |
| **Démarrage** | Montée en charge progressive à partir d'octobre 2026 |
| **Langue** | Français + anglais professionnel **indispensable** (contexte international) |
| **Reçu le** | Approche directe recruteur, adressée à Richard YI |

## Texte reçu (verbatim)

> Bonjour Richard,
>
> J'espère que vous allez bien.
>
> Je me permets de vous contacter car je recherche actuellement un **Lead Solution Architect / Technical Lead** pour intervenir chez l'un de nos clients, grande banque internationale, sur un programme stratégique autour du **E-Communications Recordkeeping & Reconciliation**.
>
> Le rôle consiste à porter la **cohérence technique end-to-end** de la solution, depuis les différentes **sources et populations** jusqu'aux **systèmes d'archivage** : architecture et intégration data, **data lineage**, **matching & reconciliation**, **data quality**, **contrôles et gestion des exceptions**, **audit trail**, **reporting et retrievability**. Le Lead Architect interviendra également sur la **conception du PoC**, puis accompagnera le **build jusqu'à l'UAT et la mise en production**.
>
> Nous recherchons un profil **senior** disposant d'une solide expérience en **architecture et intégration de données dans des environnements bancaires / marchés financiers**, avec une expérience concrète en **data reconciliation, data lineage, data quality ou control automation**. Une connaissance des problématiques de **recordkeeping, journalization ou archiving des communications électroniques** serait particulièrement appréciée, notamment dans des environnements **Microsoft Exchange/O365, Teams et/ou Bloomberg**.
>
> Au-delà de l'expertise technique, nous recherchons quelqu'un de **hands-on**, capable de **prototyper**, de traduire des besoins fonctionnels et réglementaires en solutions implémentables et d'interagir avec des équipes **IT, Operations, Risk et Compliance**. Le contexte étant international, un **anglais professionnel solide** est indispensable.
>
> La mission est principalement basée à **Paris**, avec une montée en charge progressive à partir d'**octobre 2026**.

## Lecture entre les lignes

1. **« Reconciliation » est le cœur du sujet, pas l'archivage.** Une banque qui recrute un architecte pour rapprocher *sources et populations* avec *systèmes d'archivage* cherche à prouver la **complétude** de sa captation : qui devait être journalisé, qui l'a été, quels messages manquent, depuis quand, et pourquoi. C'est un chantier de preuve, pas un chantier de stockage.
2. **Le mot « populations » est le signal fort.** Il ne s'agit pas seulement de messages mais de **périmètre de personnes** (personnes supervisées, joiners/movers/leavers, prestataires, comptes partagés, délégations). La difficulté est là : le référentiel RH, l'annuaire, les entitlements Bloomberg et les licences O365 ne disent jamais la même chose.
3. **« Retrievability » = test de restitution.** L'attendu implicite : retrouver et exporter un jeu de communications dans le délai imposé par un régulateur ou un enquêteur, de façon reproductible et documentée.
4. **Contexte réglementaire probable.** MiFID II art. 16(7) et règlement délégué (UE) 2017/565 art. 76 côté UE ; pour une banque internationale avec entités US, SEC 17a-4 / FINRA / CFTC — la vague de sanctions « off-channel communications » (2021-2024) a mis ces programmes en haut des priorités de nombreuses banques. À faire confirmer en entretien plutôt qu'à supposer.
5. **PoC → UAT → production dans le même rôle.** Le client veut quelqu'un qui reste responsable de ce qu'il a dessiné. C'est un point à jouer : l'architecte qui écrit ses propres requêtes de rapprochement et qui tient l'UAT.
6. **Ce que le recruteur va chercher dans le CV** : les mots exacts de son annonce. Voir [`../annexes/mots-cles-ats.md`](../annexes/mots-cles-ats.md).
