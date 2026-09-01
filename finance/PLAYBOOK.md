# Playbook financier MedicalCity

**Version 1.0 · 1er septembre 2026 · STRICTEMENT CONFIDENTIEL**  
**Auteur :** CFO (siège Comex) · **Signataire :** Président  
**Objet :** architecture financière pour **vendre MedicalCity comme un produit financier** — pas comme un récit tech.

Complète : rail cash GTM (`gtm/`), levée AIR/JEI (`capital/`), Comex HITL.  
N’ouvre **pas** de rail token / CLARITY.

Point d’entrée 8 minutes : [`BRIEF.md`](BRIEF.md).

---

## 0. Verdict CFO

MedicalCity n’est **pas un produit**. C’est une **usine à trois produits**, chacun avec un acheteur, une horloge, un rendement, et un régulateur.

| Produit | Ce que l’acheteur achète | Acheteur | Horloge 1er euro |
|---|---|---|---|
| **P1 — Equity HoldCo** | Option sur la plateforme (Bayon + agents) | BA, family, VC santé | AIR 2–6 sem. · seed 4–9 mois |
| **P2 — Créances logicielles** | Factures AUDIT / APA / Bayon / MC-77 | Banque (Dailly) | Dès 1re facture |
| **P3 — Contrat RaaS** | Usage 36–60 mois, 350–750 €/mois | Famille, SAD, département | Q1 2027 (pas avant go-live OPS) |
| **P4 — Facility flotte** | Actif robot + loyer cédé | Bailleur / warehouse / note privée | Après 50 unités *performing* |

L’erreur fatale : financer la **flotte** avec de l’**equity** et vendre le **seed** comme un **yield**.  
L’equity paie l’incertitude (PMF, Trust, GTM). La dette paie le fer une fois que le loyer existe.  
**CFO n’affiche un ARR RaaS que contracté, livrable, et assurable.**

---

## 1. Doctrine — « Siemens, pas un token »

Les fabricants d’imagerie ne portent pas 100 % du parc. Ils **originent** le contrat, un **bailleur** (Verso Healthcare, BPCE Lease, DLL, SGEF) **possède** l’actif, l’exploitant **sert**. MedicalCity doit faire la même chose pour le robot.

| On copie | On ne copie pas |
|---|---|
| Vendor program + HoldCo/FleetCo | SPV offshore (tue HDS + CD77) |
| Cession Dailly des factures logicielles | ABS public an 1 |
| Note privée H2, after seasoning | CLARITY / jeton / « 5 M$ SEC » |
| Granularité + réserve + DSCR | « APA = AAA, 0 défaut » |

Souveraineté : toutes les entités **France**, comptes France, pas de donnée de santé dans un FleetCo (uniquement IDs contrat, montants, statut performing).

---

## 2. Architecture juridique — trois strates, pas quatre sociétés demain

Capital social actuel : **1 299 €**. Aucun bailleur ne finance une flotte là-dessus. L’architecture se **déplie** avec le cash, elle ne précède pas le cash.

```
                    ┌─────────────────────────────┐
                    │  HOLDCO  MedicalCity SASU   │  P1 Equity
                    │  IP Bayon, AGE, marque      │
                    └──────┬──────────────┬───────┘
                           │              │
              ┌────────────▼──┐    ┌──────▼──────────────┐
              │ OPCO  (même   │    │ FLEETCO  (H1)       │
              │ SASU en H0,   │    │ Robots + loyers     │
              │ filiale H1)   │    │ cédés au bailleur   │
              │ Logiciel, HITL│    │ = P4                │
              │ SLA, DPA, GTM │    └──────────┬──────────┘
              │ = P2 + service│               │
              └──────┬────────┘               │ lease / warehouse
                     │ P3 contrat client      ▼
                     │                 BAILLEUR / NOTE
                     ▼
              Client (famille / SAD / CD)
```

### H0 — maintenant (0–90 j, 1 personne morale)

Une seule SASU. **Trois axes analytiques** (plan comptable, pas Kbis) :

| Axe | Compte | Produit |
|---|---|---|
| `PLAT` | Logiciel, R&D, HDS, wages produit | P1 + P2 |
| `FLEET` | CAPEX robots, assurances, résiduels — **reste à 0** | P4 (préparé, pas allumé) |
| `CARE` | Qualité, incidents, comité médical | Coût Trust (non productisé) |

Règle : tout euro seed est **tagué**. Un robot acheté sur `PLAT` est une faute CFO.

### H1 — post-seed ou 1ers 50 robots (Q1–Q2 2027)

- **FleetCo SAS** 100 % HoldCo. Objet : acquérir / donner en location les robots. **Aucun salarié, aucune donnée de santé.**
- **Vendor program** signé avec 1 bailleur FR. HoldCo = originator + servicer. FleetCo = emprunteur / locataire-bailleur.
- OpCo (HoldCo ou filiale) facture le **service** (SLA, HITL, logiciel embarqué). FleetCo / bailleur facture le **loyer actif**.

### H2 — ≥ 200 unités performing 12 mois

- **Warehouse** revolving (banque / fonds dette) sur pool cédé Dailly + nantissement robots.
- **Note privée** (placement < 150 personnes, pas d’offre au public AMF) si le pool est granulaire. Pas de cotation, pas de token.

**Kill-criteria structure :** créer FleetCo **avant** un BC robot ou un vendor term-sheet = dépenses avocat sans actif. Interdit.

---

## 3. Les quatre produits — spec vendeur

### P1 — Equity HoldCo (« croissance »)

| Champ | Spec |
|---|---|
| Instrument | BSA-AIR puis actions (seed 5 M€) |
| Ce qu’on vend | IP, Bayon, agents, option flotte **sans porter le fer** |
| Ticket | AIR 50–250 k€ · seed 0,5–2 M€ / fonds |
| Usage of proceeds | 40 % PMF produit · 20 % Trust · 25 % GTM + *equity slice* flotte (apport) · 15 % G&A |
| Multiple mental | SaaS / infra santé, **pas** un yield 8 % |
| Closer | Président. Data room sans donnée de santé |
| Interdit | Promettre un coupon, un ARR robot, une valo token |

Phrase : *« Vous achetez la plateforme. Le robot se finance tout seul dès qu’il loue. »*

### P2 — Créances logicielles (« working capital »)

| Champ | Spec |
|---|---|
| Sous-jacent | Factures MC-AUDIT, MC-APA, MC-BAYON, MC-77 |
| Instrument | Bordereau **Dailly** (C. mon. fin. L. 313-23) |
| Advance | 70–80 % HT des factures B2B notifiées · B2G Chorus Pro plus lent (60–70 %) |
| Coût | ~0,5–1,5 % + intérêt · à négocier **après** 2 factures encaissées au réel |
| Pourquoi | Capital 1 299 € : on ne finance pas le BFR avec de l’equity |
| Interdit | Céder une facture non émise, une LOI, une pré-réservation |

### P3 — Contrat RaaS client (« usage »)

C’est le **produit financier vendu au terrain**, pas au fonds.

| Champ | Spec (hypothèses maison — à éprouver pilote) |
|---|---|
| Loyer | 350–750 € HT / mois · TVA **20 %** (téléassistance = 20 %, pas 10 %) |
| Durée | 36 mois ferme + 12–24 option · alignée payback 18–24 mois |
| Payeurs | (1) APA si **inscrit** au plan d’aide (2) reste à charge (3) SAD mandataire |
| Crédit d’impôt 50 % | **Uniquement** si agrément/déclaration SAP — **ne pas vendre avant** |
| Résiliation | Préavis + indemnité dégressive · substitution robot sous 72 h |
| Claims | Veille / assistance, **pas** diagnostic médical |

L’APA n’est **pas** un chèque. GIR 4 plafond 811,52 € (2026) : seul le bas de grille RaaS tient **avec** de l’aide humaine. GIR 1–2 : 350–750 € tient dans le plan, RAC selon ressources. Modéliser **trois** sous-jacents de crédit : département, famille, SAD.

### P4 — Facility flotte (« yield / infra »)

| Champ | Spec cible H1 (pas un engagement) |
|---|---|
| Sous-jacent | Robot (propriété bailleur ou FleetCo) + loyer cédé |
| Advance rate | 55 % du fer **unseasoned** · 70 % après 6 mois performing |
| Durée actif | 48 mois · résiduel 10–20 % (tech risk — haircut bailleur) |
| DSCR | ≥ 1,40× (loyer net COGS ops / dette) |
| Réserve | 4 mois de service de dette, cash trap si DSCR < 1,25× |
| Concentration | ≤ 35 % un département tant que < 4 CD · ≤ 1,5 % un bénéficiaire |
| Servicer | OpCo, fee 8–12 % des encaissements (logiciel + SLA) |
| Backup servicer | Nommé H1 (SAD partenaire ou bailleur) |
| Yield parleur FO | **Ne pas promettre un taux.** Dire : *underwriting après 50 unités* |

Phrase bailleur : *« Vous financez 50 numéros de série, pas une startup. On sert, on substitue, on assure. »*

---

## 4. Unit economics — grille d’underwriting

**Statut : hypothèses internes, pas des comptes.** Toute cellule rouge = pas de P4.

Loyer mixte illustratif : **550 € HT / mois**.

| Poste | € / mois | Commentaire |
|---|---:|---|
| Loyer P3 | 550 | Milieu de grille 350–750 |
| COGS ops (opérateur, connectivity, SAV) | (155) | Cible GM cash ~72 % **hors fer** |
| Assurance + maintenance | (40) | Obligatoire pour P4 |
| **Contribution avant fer** | **355** | Ce qui sert le lease + plateforme |
| Dont servicer OpCo (10 %) | 55 | Logiciel / HITL / incidents |
| Dont disponible fer + HoldCo | 300 | 3 600 € / an |

| Fer | Hypothèse | Test |
|---|---:|---|
| Coût robot + mise en service | 8 000 € (fourchette 6–12 k€ **à sourcer OPS**) | Si > 12 k€, loyer min ou durée + |
| Payback fer @ 300 €/mois | **27 mois** | Hors cible 18–24 → **remonter loyer ou baisser fer** |
| Payback @ 396 €/mois (si COGS ops 154 et pas de split servicer) | **20 mois** | Compatible thèse site 18–24 |
| LTV/CAC | Interdit tant que CAC départemental non mesuré | Cible Comex > 5× **après** 1er canal 77 |

**Règle d’or :** le seed ne subsidie pas le loyer. Si le payback fer > 24 mois au COGS **réel** du pilote, on **ne scale pas** la flotte — on change le prix ou le hardware.

Sensibilité APA :

| GIR | Plafond 2026 | RaaS 550 € | Commentaire crédit |
|---|---:|---:|---|
| 1 | 2 080 € | Tient | RAC selon ressources |
| 2 | 1 682 € | Tient | Idem |
| 3 | 1 216 € | Tient si peu d’aide humaine | Risque d’arbitrage |
| 4 | 812 € | **Serré** | Grille 350 € ou mix SAD |

CFO refuse un pool P4 à > 25 % GIR 4 tant que le RAC n’est pas encaissé 6 mois.

---

## 5. Waterfall cash — qui est payé dans quel ordre

### Logiciel (P2) — H0

```
Client → OpCo (facture) → [option Dailly banque]
OpCo paie : Trust, produit, G&A, Président
```

Acompte 30–50 % **avant** kickoff (playbook GTM). Sinon tu es la banque du client avec 1 299 €.

### RaaS (P3/P4) — H1

```
1. Encaissement loyer (famille et/ou APA et/ou SAD)
2. Taxe / TVA collectée
3. Réserve DSCR (si facility)
4. Dette / loyer bailleur (FleetCo)
5. COGS ops + assurance
6. Servicer fee OpCo
7. Excess spread → HoldCo (equity)
```

Défaut bénéficiaire : substitution **contrat** (autre GIR éligible) sous 45 j ou **reprise robot** + réserve. Pas de recapitalisation HoldCo automatique — le P4 vit tout seul ou on arrête d’originer.

### Interdiction de commingling

Comptes dédiés : `MC-PLAT`, `MC-FLEET`, `MC-TAX`. Un loyer RaaS qui paie un salaire produit = **covenant breach** interne dès H1 (et breach réel dès qu’un bailleur est là).

---

## 6. Stack de capital — qui met quel euro

```
H0                          H1                         H2
────────                    ──                         ──
AIR / IR-PME                Seed 5 M€                  Growth / dette
Dailly factures logicielles Vendor lease flotte        Warehouse + note privée
BPI (prêt / garantie)       Equity slice 25–40 % fer   Infra FO (yield)
                            BPI / Réseau Entreprendre
```

| Source | Rôle | Dilution | Sûreté |
|---|---|---|---|
| BSA-AIR | Pont 0,5–1,5 M€ | Différée (cap/floor) | Aucune — equity |
| Seed VC | PMF + Trust + GTM | Oui | Aucune |
| Dailly | BFR logiciel | Non | Créances |
| Bailleur | 55–70 % du fer | Non | Robot + loyer |
| BPI | Quasi-equity / garantie | Faible | Variable |
| Note privée | Scale flotte | Non | Pool + réserve |
| Token | **Interdit H0–H1** | — | — |

**Ratio cible H1 (50 robots × 8 k€ = 400 k€ fer) :** 30 % equity HoldCo (120 k€ du seed) + 70 % bailleur (280 k€). L’equity **n’achète pas** 400 k€ de fer.

---

## 7. Comment vendre — trois pitchs, zéro mélange

### 7.1 Family office / BA (P1)

Durée 12 min. Support : 8 slides max.

1. Droit : APA + choc démographique (sans « 5,4 Md€ » faux)  
2. Wedge : LOI 77 + Bayon en prod + SKU cash  
3. Architecture : *vous n’achetez pas le fer*  
4. Usage 5 M€ · 18 mois  
5. Cap table SASU · AIR termes  
6. Risques : Trust, CD77, payback fer  
7. Ask : 150 k€ AIR, cap à discuter avocat  
8. Ce que vous ne financez pas : drones, token, Fondation  

### 7.2 Bailleur / lease (P4)

Durée 20 min. Dossier crédit, pas un deck vision.

- 50 numéros de série, coût unitaire sourcé  
- Contrat P3 type + assurance  
- Historique **performing** (même N=10 du pilote)  
- Concentration, DSCR, réserve, servicer  
- Backup, substitution, reprise  
- KYC HoldCo post-seed (fonds propres ≠ 1 299 €)

### 7.3 Fonds santé seed (P1)

Idem BA + data room. **Preuve cash** (facture AUDIT/77) > LOI.  
Ils achètent le multiple plateforme. Si tu parles yield flotte trop tôt, tu es **mal pricé** (on te file un 8× cash flow au lieu d’un 12–15× SaaS).

**Règle closer :** un rendez-vous = **un produit**. Jamais P1 et P4 dans la même salle le même jour.

---

## 8. Credit box & covenants (à coller dans tout term-sheet P4)

**Eligibilité d’un contrat dans le pool**

- Contrat écrit ≥ 36 mois  
- Loyer ≥ 350 € HT  
- Robot assuré, n° de série, localisation France  
- Performing : 2 échéances encaissées, 0 impayé > 30 j  
- Pas de donnée de santé dans le dossier bailleur  
- Intended use non médical (CARE)

**Covenants HoldCo / FleetCo**

| Covenant | Seuil | Breach |
|---|---|---|
| DSCR | 1,40× | Cash trap + stop origination |
| Concentration CD | 35 % | Haircut advance |
| Impayés > 30 j | < 4 % du pool | Marge + |
| Fonds propres HoldCo | Post-seed ≥ 1 M€ cash | Pas de tire bailleur |
| Claims cliniques | 0 non signé | Cross-default réputation (clause)

---

## 9. Fiscalité — ce que le closer n’invente pas

| Sujet | Position CFO H0 |
|---|---|
| TVA logiciel | 20 % |
| TVA RaaS / téléassistance-like | **20 %** (CGI : téléassistance hors taux réduits SAP) |
| TVA 5,5 / 10 % SAP | Seulement gestes essentiels **après** qualification avocat |
| Crédit d’impôt 50 % | Après déclaration/agrément SAP · **jamais** en argument GTM avant |
| IR-PME / JEI | Dossier **cette semaine** · 30 % JEI à la **conversion** actions, pas à l’AIR |
| IS HoldCo | Déficitaire H0–H1 : normal · ne pas vendre un « yield net d’IS » |
| Prix de transfert H1 | Loyer interne OpCo ↔ FleetCo = marché (dossier) |

---

## 10. Data room — deux armoires, une IP

**Armoire Equity (P1)** — fonds / BA  
Index : Kbis, statuts, cap table, AIR, LOI 77, SKU GTM, CI Bayon (sans data), politique qualité, registre AI Act (schéma), modèle UE **hypothèses**, 13-week cash, usage of proceeds.  
**Zéro** dossier patient, **zéro** nom aidant.

**Armoire Crédit (P2/P4)** — banque / bailleur  
Index : CGV, factures, Chorus Pro, contrats P3 type, polices d’assurance, n° série, tapis performing, concentration, DSCR, DPA *mentionné* pas joint s’il contient de la santé.

Un data room unique « tout pour tout le monde » = tu donnes trop au VC et trop peu au bailleur. **Deux liens.**

---

## 11. 90 jours — plan comptable du CFO

Aligné GTM J0 = 24 août 2026 ; ici **J0 = signature de ce playbook**.

### J0–J15

- [ ] Axes `PLAT` / `FLEET` / `CARE` dans la compta  
- [ ] 13-week cash réel (pas un deck)  
- [ ] Dossier **JEI** envoyé  
- [ ] Mandat avocat AIR (cap, floor, décote)  
- [ ] Trois banques : Dailly **après** 1re facture, pas avant  
- [ ] Liste 3 bailleurs FR (Verso, BPCE Lease, un 3ᵉ) — **prise de contact info**, pas un term-sheet

### J16–J45

- [ ] 1re facture P2 dans l’armoire equity  
- [ ] Polices RC pro + cyber (prérequis P4 *et* CD77)  
- [ ] Sourcer **coût fer unitaire** (OPS) — tuer l’hypothèse 8 k€ ou la valider  
- [ ] Contrat P3 v0 (CARE + avocat) : durée, RAC, substitution, claims  

### J46–J90

- [ ] Term-sheet vendor **non signé** si 0 robot — dossier prêt  
- [ ] Décision go/no-go FleetCo : uniquement si go pilote **et** fer payback ≤ 24 mois  
- [ ] Data room P1 complète pour seed  

---

## 12. KPI CFO (ligne huddle)

En plus des 8 chiffres Président :

| KPI | Rouge |
|---|---|
| Cash / runway semaines | < 16 sem. sans AIR/seed |
| Facturé vs encaissé P2 | DSO > 45 j B2B · > 75 j B2G |
| Mix axes PLAT vs FLEET | FLEET > 0 € avant go-live |
| Payback fer (modèle) | > 24 mois au COGS réel |
| ARR RaaS affiché | Toute ligne non contractée |

---

## 13. Interdits (constitution financière)

1. Token, CLARITY, Regulation Crypto, « on est un digital commodity ».  
2. ARR robot dans un deck.  
3. « APA paie 100 % » · crédit d’impôt 50 % avant SAP.  
4. Acheter le parc sur l’equity seed au-delà de l’apport 25–40 %.  
5. SPV hors France.  
6. CA GEOVTC.  
7. Commingling loyer / opex produit.  
8. Créer FleetCo pour faire joli.  
9. Un yield promis à un FO avant 50 unités performing.  
10. Donnée de santé dans un dossier bailleur.

---

## Adoption

Ce playbook entre en vigueur à la signature du Président. Révision trimestrielle (même cadence que la revue risques Comex). Toute dérogation = MANDATORY.

**Richard YI — Président, MedicalCity SASU**
