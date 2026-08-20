# Cibles 14 jours — qui a un budget cette année

Ne pas diluer : **20 noms, pas 200**. GTM tient le fichier ; le Président n’appelle que les A.

Priorité A = closer cette semaine. B = semaine 2–3. C = parking jusqu’à CA > 40 k€.

---

## A1 — Le contrat qui transforme la LOI (SKU MC-77)

| Cible | SKU | Pourquoi maintenant |
|---|---|---|
| CD77 — DGA Solidarités / directeur autonomie | MC-77 | LOI déjà signée ; marché < 60 k€ = 1re facture publique |
| CD77 — DSI / chef de projet SI APA | MC-77 + MC-BAYON | L’outillage se vend à la DSI, la LOI se vend à l’élu |
| CD77 — finances / commande publique | MC-77 | Ils tiennent le seuil 60 k€ et Chorus Pro |

Next step : un créneau **unique** « devis outillage instruction APA, 48–58 k€ HT, sans robot ».

---

## A2 — SAD / SPASAD Île-de-France (SKU MC-AUDIT → MC-APA)

Critère : volume dossiers APA, douleur administrative, SIRET, décideur = directeur / DAF, pas l’infirmière coordinatrice seule.

Pistes de sourcing (à nommer dans le CRM, pas à laisser en catégorie) :

- SAD du **77** déjà dans le périmètre LOI (ils seront le canal ops du pilote — les payer en logiciel **avant** le robot)
- Têtes de réseau : **ADMR, UNA, Domicile à domicile / FNAAFP-CSF, Croix-Rouge autonomie, AMPA**
- 5 SAD privés / associatifs 75-78-91-92-93-94 avec > 200 bénéficiaires APA

Message : cycle time dossier, pas « IA de soin ».

---

## A3 — DSI / innovation EHPAD (SKU MC-AUDIT ou MC-BAYON)

- Groupes : un **directeur innovation / DSI régional**, pas le siège national (trop lent). Viser une **région IDF** d’un groupe (Clariane, DomusVi, Colisée, Korian residual, associatifs type Fondation Partage & Vie).
- EHPAD isolés du 77 : MC-AUDIT 8,5 k€ = ticket digérable en budget établissement.

Message : golden record, pas robot en chambre (claim + MDR).

---

## B — Multiplicateurs (après 1re facture)

| Cible | SKU | Note |
|---|---|---|
| Autre département IDF (78, 91, 92, 93, 94) | MC-AUDIT puis marché < 60 k€ | Playbook 77 recopié ; **pas** de 2ᵉ RaaS |
| MDPH / PCH (même DGA souvent) | MC-AUDIT | Même douleur d’instruction, autre code |
| Éditeur SI médico-social | MC-BAYON | OEM / connecteur — cycle plus long, gros ticket |
| Mutuelle / CARSAT (conférence des financeurs) | Parking | Utile au scale, lent au cash |

---

## C — Les 205 pré-réservations (canal, pas CA robot)

Traitement **J3** :

1. Segment : famille / EHPAD / presse / investisseur / autre (champ formulaire site).
2. Famille : mail honnête — robot **Q1 2027**, 0 € maintenant, option : être rattachés à un SAD partenaire (le SAD, lui, achète MC-APA).
3. EHPAD / médecin : bascule A3.
4. Investisseur : bascule data room, pas GTM cash.
5. Aucun acompte robot.

Si un aidant demande à payer : **liste d’attente prioritaire gratuite**, pas un SKU famille tant que SAP / flotte absents.

---

## Fichier minimum (une ligne par cible)

`gtm/pipeline.csv` à créer J1 (hors Git si nominatif — **initiales + orga seulement** dans Git) :

`orga | type | sku | € | étape | next_step_date | owner`

Étapes : cible → RDV → devis → verbal → BC → facturé → encaissé.
