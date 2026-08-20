# Processus à monitorer

**32 processus, 6 domaines.** Tu ne les opères pas. Tu les **vois** au rythme indiqué.  
Owner = siège Comex. Escalade = huddle 15 min ou Comex 90 min.

Inspirations : huddles Cleveland Clinic / Intermountain (qualité d’abord, escalade en 15 min) ; Qualiscope Ramsay (référentiel interne plus dur que l’audit) ; clinic weekly ops rhythm (10–15 KPI, pas 80) ; ISO 13485 management review ; AI Act art. 14 (human oversight).

Seuil **rouge** = tu t’en occupes **ce jour-là**. Orange = ligne Comex. Vert = AUTO.

---

## 1. Sécurité des personnes & incidents (hôpital d’abord)

Les PDG de Cleveland Clinic ouvrent chaque jour par : infections, événements graves, capacité. Toi tu n’as pas de lits. Tu as des **agents, des robots, des dossiers APA, des données**.

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 1.1 | Notification d’incident grave | Tout P0 (personne, robot, data, presse) au Président **le jour même** | Temps réel | OPS + CARE | Non notifié J0 |
| 1.2 | Triage P0 / P1 / P2 | Taxonomie unique, un owner, une horloge | Quotidien | OPS | P1 sans owner 4 h |
| 1.3 | Clôture / CAPA | P1 clos ou plan daté **< 72 h** | Quotidien | CARE | P1 ouvert > 72 h |
| 1.4 | RCA2 (analyse systémique) | 1 RCA pour tout P0, thèmes capitalisés | 7 jours | CARE | P0 sans RCA J+7 |
| 1.5 | Materiovigilance / OTA robots | Incidents dispositif, rollback OTA, traçabilité flotte | Hebdo (quotidien si flotte live) | OPS | OTA sans journal WORM |
| 1.6 | Sécurité aidant / bénéficiaire (pilote) | Chutes, non-réponse, fausse alerte, escalade humaine | Quotidien dès go-live | OPS | Escalade humaine > SLA |

**Rituel CEO :** huddle item 1 = file incidents. Zéro incident ≠ skip : on dit « zéro », c’est une donnée.

---

## 2. Trust, droit d’opérer, qualité (MedTech + Ramsay)

Ramsay pilote HAS + Qualiscope interne. Doctolib : « zéro compromis vie privée ». ISO 13485 : le DG *possède* le SMQ.

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 2.1 | HITL Bayon (AUTO / RECOMMENDED / MANDATORY) | Taux d’override, files d’attente, décisions sans log | Quotidien | PLAT | Décision sans hash WORM |
| 2.2 | Audit trail WORM | Chaîne de hash intacte, rétention | Hebdo | PLAT | Trou dans la chaîne |
| 2.3 | Classification AI Act + registre | Intended use, risque, logs, evals, art. 14 oversight | Hebdo | CARE | Système en prod hors registre |
| 2.4 | Drift / evals agents métier | Jeu de tests APA & clinique, score vs baseline | Hebdo | PLAT + CARE | Baisse eval > 5 pts ou hallucination documentée |
| 2.5 | RGPD / base légale / DPA | Registre des traitements, DPA hébergeur, DPIA APA | Mensuel | CARE (DPO quand nommé) | Traitement sans base légale |
| 2.6 | HDS | GAP, hébergeur, clés, périmètre, jalons | Hebdo pendant dossier | CARE | Jalon HDS glissé > 14 j |
| 2.7 | Claims cliniques | Toute phrase publique vs intended use | Ad hoc + Comex | CARE | Claim non signé Président |
| 2.8 | Comité médical / matériovigilance | Présence, avis, veto protocole | Mensuel | CARE | Protocole live sans avis |
| 2.9 | Management review SMQ | Inputs 13485 : audits, CAPA, PMS, fournisseurs, réglementaire | Trimestriel | CARE + Président | Revue sautée ou sans décision |
| 2.10 | Souveraineté data | Données de santé **France**, rien dans Git/prompts | Quotidien | PLAT | Donnée de santé hors HDS-ready |

---

## 3. Product-market fit (wedge APA / Bayon / CD77)

Alan : preuve avant récit. Doctolib : rester collé à l’utilisateur réel.

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 3.1 | Conversion LOI CD77 → convention | Jalons juridiques, blockers nommés | Hebdo | GTM | Aucun chemin contractuel à J45 |
| 3.2 | Agent APA bout-en-bout | Dossiers instruits HITL, cycle time, taux retour | Hebdo | PLAT | 0 dossier réel à J90 sans plan |
| 3.3 | Mapping GIR 1–4 / barème 2026 | Couverture codes, écarts | Hebdo | PLAT + CARE | Mapping non versionné |
| 3.4 | Golden record FHIR R4 | Latence source → record (cible < 30 s), 1 source institutionnelle | Hebdo | PLAT | Latence p95 > 60 s ou 0 source à J90 |
| 3.5 | Qualité plateforme | CI verts, 55 E2E, régressions | Quotidien | PLAT | Main rouge > 24 h |
| 3.6 | Go / no-go pilote Q1 2027 | Critères écrits (n sites, SLA, canal incident) | Mensuel puis hebdo H1 | OPS | Critères absents à J45 |

---

## 4. GTM institutionnel & ops physiques

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 4.1 | Pipeline départements | Étapes : cible → one-pager → 1er RDV → LOI → convention | Hebdo | GTM | Pipeline < 5 noms actifs |
| 4.2 | Pré-réservations robots | Stock 205 → cible 400 ; qualité du lead | Hebdo | GTM | Conversion inbound morte 14 j |
| 4.3 | Conversion LOI → contrat | Taux > 30 % (OKR 18 mois) | Mensuel | GTM | Taux < 15 % sur n ≥ 5 |
| 4.4 | Modèle tripartite | Actif / opérateur / APA — clauses, qui facture | Hebdo | GTM + CFO | Clause payeur floue |
| 4.5 | Canal SAD / EHPAD | 1 canal, sans cannibaliser 77 | Hebdo | GTM | 2e département avant 77 signé, sans feu vert |
| 4.6 | Flotte RaaS & SLA 24/7 | Disponibilité, MTTR, n sites, opérateurs | Quotidien dès pilote | OPS | Dispo < SLA écrit |
| 4.7 | NPS aidants / opérateurs | Pulse post-contact | Mensuel (hebdo en pilote) | OPS | NPS < 30 ou plainte grave |

---

## 5. Capital, cash, unit economics

Le cash est un incident de sécurité. Les PDG d’hôpitaux regardent le revenue cycle chaque semaine ; toi tu regardes **runway + COGS réels**.

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 5.1 | Trésorerie / runway | Jours de cash, 13-week rolling | **Lundi huddle** | CFO | Runway < 6 mois sans term-sheet |
| 5.2 | Burn vs plan | Écart MTD | Hebdo | CFO | Burn > plan +20 % |
| 5.3 | Unit economics RaaS | LTV/CAC, COGS opérateurs **réels** (pas cibles 70–75 %) | Hebdo | CFO | LTV/CAC < 3× ou COGS inconnus |
| 5.4 | Data room seed | Index, dates, pas de donnée de santé | Hebdo en levée | CFO | Doc > 14 j ou donnée de santé |
| 5.5 | Pipeline investisseur | Funnel, next step daté | Hebdo en levée | CFO | Next step absent > 7 j sur un chaud |
| 5.6 | Engagements > 12 mois / CAPEX | File MANDATORY | Ad hoc | CFO | Engagement signé hors file |

---

## 6. Gouvernance, personnes, calendrier du Président

Intermountain : on mesure si le huddle a eu lieu. Alan : transparence interne, ownership distribué.

| # | Processus | KPI / signal | Cadence | Owner | Rouge |
|---|---|---|---|---|---|
| 6.1 | Packs Comex | 7 pages sièges J-1, pack pyramidal ≤ 4 p. | Hebdo | AGE | < 5 sièges packés |
| 6.2 | Décisions HITL | RECOMMENDED < 48 h ; MANDATORY journalisées | Quotidien | AGE | Reco hors SLA |
| 6.3 | Stop-doing | Heures drones / UE / Fondation | Hebdo | STRAT | > 2 h Président |
| 6.4 | OS Président | Blocs stratégiques tenus, huddles, rounding | Vendredi | AGE | < 3 blocs tenus |
| 6.5 | Charge Sreypov | Priorités Care vs contenu vs terrain | Hebdo | CARE | 3 chantiers P1 simultanés |
| 6.6 | Qualité agents (evals SMCI) | Drift de consigne, hallucinations de pack | Hebdo | AGE | Pack sans reco unique |

---

## Vue huddle — les 8 chiffres du matin

Pas 32. **Huit.** Le reste vit dans le pack hebdo.

1. Incidents P0/P1 ouverts  
2. Décisions HITL hors SLA  
3. CI / Bayon (vert/rouge)  
4. Runway (jours)  
5. Blocker #1 CD77  
6. File APA (dossiers en attente humaine)  
7. Dispo flotte (N/A tant que pas live)  
8. Blocs Président du jour (tenus hier oui/non)

Modèle : `checklists/huddle-15min.md` + `scorecard.yaml`.

---

## Ce que tu ne monitores pas (volontairement)

- Vanity (followers, impressions) sauf si GTM en fait un canal mesuré
- Roadmap drones / Europe
- Benchmarks HAS hospitaliers (infections nosocomiales, DMS) — hors scope jusqu’à dispositif de soin régulé
- Organigramme à 30 personnes
- Compte d’exploitation « type clinique 200 lits »

Ramsay surveille IQSS et NPS parce qu’ils opèrent des établissements. Toi tu surveilles **droit d’opérer + wedge + cash**. Le jour où un robot est un dispositif médical en service, la colonne 1 s’épaissit — on n’attend pas ce jour-là pour ouvrir 1.1 à 1.6.
