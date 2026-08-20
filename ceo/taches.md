# Catalogue des tâches du Président

Toute tâche MedicalCity tombe dans une des trois colonnes.  
Si elle n’y est pas, STRAT l’ajoute ou la classe **stop-doing**.

Légende HITL : **M** mandatory · **R** recommended · **A** auto (audit a posteriori).

---

## A. CEO-only — tu ne délègues pas l’accountability

Même si un agent ou un conseil prépare 95 % du dossier.

### A1. Organe social & signature

| Tâche | HITL | Cadence | Préparé par |
|---|---|---|---|
| Représentation légale SASU, Kbis, banques, assurances | M | Ad hoc | CFO |
| Contrats, LOI, avenants, NDA institutionnels | M | Ad hoc | GTM + CFO |
| Term-sheet, data room investisseur, usage of proceeds | M | Semaine pendant levée | CFO |
| CAPEX > 10 k€ ou engagement > 12 mois | M | Ad hoc | CFO |
| Nomination comité médical, DPO humain, PRRC (quand MDR) | M | H0–H1 | CARE |
| Politique qualité (1 page) et objectifs qualité mesurables | M | Trimestriel | CARE |
| Management review SMQ (présence + décisions) | M | Trimestriel (mensuel si pré-audit) | CARE |
| Réponses autorité (CNIL, ARS, ANSM, DGCCRF, Tracfin) | M | Ad hoc | CARE + CFO |

### A2. Visage institutionnel

| Tâche | HITL | Cadence | Préparé par |
|---|---|---|---|
| Closer CD77 / départements (tu es dans la salle) | M | Hebdo tant que non signé | GTM |
| Récit seed 5 M€ — tu le dis, tu ne le lis pas | M | 4–8 calls / mois en levée | CFO + STRAT |
| Presse, claims médicaux, prises de parole | M | Ad hoc | CARE (claims) + contenu |
| Relations CNSA / ARS / payeur public | M | Mensuel | GTM |
| Rounding terrain (voir OS §6) | R | 1 / semaine | OPS + CARE |

### A3. Intention & arbitrage

| Tâche | HITL | Cadence | Préparé par |
|---|---|---|---|
| 3–5 priorités de la semaine + time-blocking | M | Dimanche 18h | Toi (AGE propose un draft) |
| Trancher les conflits d’agents (3 options max, pas de moyenne) | M | Comex | AGE |
| Stop-doing : tuer un sujet hors des 12 | M | Comex | STRAT |
| Go / no-go pilote Q1 2027 | M | J90 + freeze H1 | OPS + CARE + GTM |
| Recrutements humains seniors (post-traction seulement) | M | Après go pilote | STRAT |

---

## B. CEO-in-the-loop — tu décides, tu n’exécutes pas

| Tâche | HITL | Toi fais | Toi ne fais pas |
|---|---|---|---|
| Parcours HITL APA (GIR 1–4) | R | Valider le protocole et les cas limites | Mapper les codes, cliquer les dossiers |
| Branchement Bayon / FHIR | R | Trancher la 1re source institutionnelle | Intégrer, déboguer |
| Pricing RaaS hors grille 350–750 € | R | Oui/non sous 48 h | Construire le modèle |
| Séquence GTM d’un nouveau département | R | Autoriser le 1er contact | Rédiger les one-pagers |
| Backlog produit vs 12 sujets | R | Arbitrer 15 min en Comex | Gérer Jira |
| JD + short-list | R | Choisir qui on voit | Sourcer |
| Incidents P1 — revue 72 h | M si P0/P1 personne ou data | Être briefé, allouer, communiquer | Mener le RCA |
| Pack Comex | A | Annoter, signer les MANDATORY | Réécrire |

---

## C. Interdit au Président (H0–H1)

Faire ces tâches, c’est voler les 3–5 priorités.

- Rédiger les packs, CR, veilles, relances hors institutionnel
- Coder une feature « vite fait » (y compris Bayon)
- Négocier en solo un département **sans** brief GTM écrit
- Produire du contenu LinkedIn au fil de l’eau (Sreypov + CARE ; toi tu valides les claims)
- Explorer drones / UE / Fondation
- Recruter un organigramme fantôme (CMO, VP Sales, Board) avant traction
- Stocker ou coller une donnée de santé dans un prompt, un Git, un Slack
- Répondre à chaud à un journaliste
- « Aider » un agent en réécrivant son livrable au lieu de renvoyer le pack

---

## D. Tâches des 90 jours — backlog personnel

Aligné sur `comex/playbooks/90-jours.md`. Owner = Président. Exécution = sièges.

### J0–J15 — Gouverner

- [ ] Signer `comex/CHARTE.md`
- [ ] Signer `ceo/BRIEF.md` (adoption de cet OS)
- [ ] Instancier les 7 agents + 1er huddle 15 min
- [ ] 1er Comex : figer 12 sujets + stop-doing drones
- [ ] Nommer 2–3 cliniciens en LOI comité médical
- [ ] Écrire et signer la politique qualité 1 page

### J16–J45 — Pilote contractable

- [ ] Être dans la salle pour convertir LOI CD77 → projet de convention
- [ ] Trancher n sites, go/no-go, canal incident (OPS)
- [ ] Valider le parcours APA HITL documenté
- [ ] Trancher la 1re source Bayon
- [ ] Ouvrir data room seed (index, unit economics, **zéro donnée de santé**)

### J46–J90 — Finançable

- [ ] Lancer dossier HDS (périmètre + hébergeur)
- [ ] Voir le registre AI Act vivant (pas un slide)
- [ ] 5 one-pagers départements — tu closes 2 rendez-vous
- [ ] Narrative seed 5 M€ tenu à l’oral sans notes
- [ ] Revue J90 : kill/continue drones, hires oui/non, go pilote

---

## E. Matrice RACI condensée (Président)

| Décision | R | A (toi) | C | I |
|---|---|---|---|---|
| Convention pilote CD77 | GTM | Président | CARE, CFO, OPS | STRAT |
| Classification AI Act / intended use | CARE | Président | PLAT | GTM |
| Hébergeur HDS | CARE | Président | CFO, PLAT | — |
| Term-sheet | CFO | Président | STRAT | GTM |
| Claim public « soin / diagnostic / autonomie » | CARE | Président | GTM | OPS |
| OTA robot / matériovigilance | OPS | Président | CARE | PLAT |
| Recrutement senior | STRAT | Président | siège concerné | — |

R = exécute · A = accountable (une seule personne : toi) · C = consulté · I = informé
