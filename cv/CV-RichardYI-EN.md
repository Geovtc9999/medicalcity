# Richard YI

**Lead Solution Architect — Data, Recordkeeping & Reconciliation**

*Application — Lead Solution Architect / Technical Lead, E-Communications Recordkeeping & Reconciliation programme (Paris, from Oct. 2026)*

Paris, France — available on site · [[TO COMPLETE: phone]] · [[TO COMPLETE: email]] · [[TO COMPLETE: LinkedIn]] · French (native) · English [[TO COMPLETE: level + context]]

> **DRAFT — 40 gaps to fill.** Chaque `[[...]]` est un fait que seul Richard peut fournir. Voir `cv/README.md`.

## Profile

Hands-on data solution architect. I design and land regulated end-to-end data chains: multi-source capture, normalisation, matching, automated controls, tamper-evident audit trail, on-demand retrieval. [[TO COMPLETE: X years of experience, of which Y in banking / capital markets — name your two strongest institutions here; this is the line the reader scans first]]. I prototype myself, I document the lineage of what I deliver, and I hold the subject in front of IT as well as Operations, Risk and Compliance.

## What I bring to this programme

- **End-to-end coherence, not a collection of connectors.** One canonical data model from the sources (Exchange/O365, Teams, Bloomberg IB & MSG, voice, mobile) through to the archiving systems, and an explicit interface contract per source: format, keys, timestamps, expected completeness, behaviour on late arrival and replay.
- **Completeness that can be demonstrated at three levels.** Population reconciliation (HR / directory / entitlements against accounts actually journalled), volume reconciliation (counted at source vs ingested vs archived) and fidelity reconciliation (attachments, edits, deletions, threads, participants). Every gap is dated, attributed, explained.
- **Controls that produce traceable exceptions.** Each control has an owner, a threshold, a frequency, an exception queue and an SLA. An exception is a data object with a lifecycle, not a chaser email.
- **An audit trail that stands without trusting the operator.** Append-only hash-chained journal, immutable (WORM) storage, and an evidence pack that can be rebuilt cold: what was captured, through which path, when, under which version of which rule.
- **Retrievability is measured, not promised.** The only test that counts is retrieving and exporting a defined scope of communications within the mandated window, blind, with elapsed time and completeness recorded. I put that test inside the PoC.
- **A PoC designed to be promoted or thrown away.** Narrow scope — one population, two sources — but the same interface contracts, controls and exit criteria as the target, so the build decision is not taken on the strength of a demo.

## Core skills

**Data architecture & integration** — Target architecture and roadmap · interface contracts and data modelling · batch and near-real-time ingestion, CDC, event streaming · orchestration and scheduling · idempotency, replay, failure recovery, backfill · late-arriving data and event ordering · architecture documentation (C4, ADR) [[TO COMPLETE: keep only the technologies you genuinely master — Kafka, Spark, dbt, Airflow, Control-M, SQL, Python, Azure/AWS/GCP]]

**Matching & reconciliation** — Deterministic and probabilistic matching · identity resolution (person ↔ accounts ↔ terminals ↔ supervised population) · key, tolerance and break-rule design · completeness and volume reconciliation · break management, requalification, ageing · control-on-the-control (reconciling the reconciliation)

**Data quality & control automation** — Completeness, accuracy, uniqueness, timeliness and format-conformity dimensions · controls embedded in the pipeline rather than bolted on downstream · thresholds, scoring, trend · level-1 control automation and evidence production for level 2 · control dashboards for Operations and Compliance

**Data lineage & governance** — Technical and business lineage · traceability from regulatory requirement → rule → field → source · rule versioning and replayability of history · data dictionary and ownership · cataloguing and mapping [[TO COMPLETE: Collibra, Informatica, Solidatus, OpenMetadata, DataHub — keep only what you have used]]

**E-communications recordkeeping & archiving** — Exchange / Exchange Online journalling · Teams (Graph export APIs, Purview, attachments held outside the message) · Bloomberg IB and MSG, entitlements, Vault · retention, legal hold, retention policies · WORM immutability (Object Lock, immutable blob) · indexing, search and e-discovery export · de-duplication while preserving proof of distribution

**Regulation translated into technical requirements** — MiFID II art. 16(7) and Delegated Regulation (EU) 2017/565 art. 76 (5-year retention, 7 on request of the competent authority) · SEC 17a-4(f) and the audit-trail alternative introduced by the 2022 amendments · FINRA 3110 / 4511, CFTC 1.31 and 1.35 · GDPR: minimisation, retention periods, employee rights, CNIL guidance · DORA: reliance on a third-party archive, testability, exit plan

**Delivery & stakeholders** — PoC framing and design · build, test strategy, UAT, production cut-over · workshop facilitation and governance forums · IT / Operations / Risk / Compliance interface · trade-offs between regulatory requirement, feasibility and deadline · delivery in professional English

## Experience

### [[TO COMPLETE: title — e.g. Data Solution Architect / Tech Lead]] — [[TO COMPLETE: bank or financial institution]]

*[[TO COMPLETE: city]] · [[TO COMPLETE: period]]*

[[TO COMPLETE: one sentence — business domain (markets, risk, compliance, back office), data scope, number of sources, volumes, team size.]]

- [[TO COMPLETE: the hardest reconciliation you designed. Two sources meant to agree, the keys you chose, the match rate reached, what you did with the breaks.]]
- [[TO COMPLETE: a manual control you automated. Before: how long, by whom, with what error rate. After: the same measure.]]
- [[TO COMPLETE: a regulatory requirement you turned into a testable technical requirement, and how you evidenced it.]]
- [[TO COMPLETE: the production release. What you carried to UAT, the cut-over, what broke and how you held it.]]

Stack : [[TO COMPLETE: technologies actually used]]

### [[TO COMPLETE: title]] — [[TO COMPLETE: organisation]]

*[[TO COMPLETE: city]] · [[TO COMPLETE: period]]*

[[TO COMPLETE: same logic; two bullets are enough for older roles.]]

- [[TO COMPLETE: quantified achievement 1]]
- [[TO COMPLETE: quantified achievement 2]]

Stack : [[TO COMPLETE: technologies]]

### Founder & President — platform architect — MedicalCity SASU

*Paris · [[TO COMPLETE: month]] 2026 — present*

Data infrastructure in a heavily regulated environment (health data): platform design and build, compliance framework and technical roadmap. Hands-on architect as much as executive.

- **Multi-source golden record (Bayon).** Ingestion chain, mapping to a canonical FHIR R4 model, identity resolution and construction of a reference record in under 30 s; delivered as a fixed-price 8-week PoC with contractual acceptance milestones (40 % order / 40 % mid-point / 20 % acceptance).
- **Tamper-evident audit trail.** Append-only hash-chained journal and WORM logging of every automated decision: replay cold what was decided, under which rule, on which data.
- **Control automation with exception management.** Explicit decision tiers — AUTO, RECOMMENDED, MANDATORY — the latter requiring recorded human sign-off. Silence is not consent: an unsigned recommendation lapses to a refusal after 48 h. This is an automated level-1 control model with an exception queue and segregation of duties.
- **Regulatory requirements translated into architectural constraints.** France-based hosting, processor agreements, a hard ban on sensitive data in the code repository, health-data hosting certification file, a live AI Act register — each requirement converted into a rule verifiable in the delivery chain rather than a declarative commitment.
- **Working with control functions.** Designed and ran a weekly governance forum separating execution from reserved decisions (contracts, health data, commitments), on the model of a risk committee.

Stack : [[TO COMPLETE: actual platform stack — languages, ingestion, storage, CI, cloud]]

### [[TO COMPLETE: role at GEOVTC]] — GEOVTC

*[[TO COMPLETE: city]] · [[TO COMPLETE: period]]*

[[TO VERIFY — reconstructed from your internal documents: an "AI factory" and short-diagnostic offering for mid-caps. Correct or delete this block if inaccurate.]]

- [[TO COMPLETE: what you built, for which volumes / clients]]
- [[TO COMPLETE: what transfers to this role — data integration, control automation, industrialisation]]

Stack : [[TO COMPLETE: technologies]]

## Available on request

A 3-page architecture note — "PoC for E-Communications Recordkeeping & Reconciliation: scope, reconciliation model, control catalogue, exit criteria" — written for this programme.

## Education

- [[TO COMPLETE: degree, institution, year]]
- [[TO COMPLETE: further degree or certification — cloud / architecture / data governance certifications belong here]]

## Languages

- French — native
- English — [[TO COMPLETE: level. Do not write "fluent" without evidence: name the real situation (governance forums in English, offshore team, English-speaking client, assignment abroad). This is a knock-out criterion for this role.]]
- [[TO COMPLETE or delete: other language]]

## Availability

- Paris and Île-de-France, on site
- Start compatible with a progressive ramp-up from October 2026
- [[TO COMPLETE: contracting status]]
- [[TO COMPLETE: target day rate and days per week]]
