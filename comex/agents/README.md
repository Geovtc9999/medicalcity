# Agents du Comex MedicalCity

Chaque fichier est le **contrat d’identité** d’un siège (framework SMCI : Skills, Memory, Context, Identity).

À instancier comme :

- agent Cursor Cloud (un run par siège, mémoire = ce dépôt) ;
- Custom GPT / Claude Project / skill ;
- nœud MCP + A2A derrière l’AGE.

## Règles d’instanciation

1. Coller le fichier `*.md` comme system prompt.
2. Donner accès en lecture à `comex/` et `docs/comex/`.
3. Écriture limitée à `comex/packs/`, `comex/risk/`, `comex/quality/`, `comex/decisions/`.
4. Toute donnée de santé reste hors de ces agents (passerelle Bayon uniquement, HITL).
5. L’agent `age-comex` est le seul à convoquer les autres (protocole A2A).

## Carte

```
Président (humain)
        │ intention / veto
        ▼
   age-comex
     ├── plat  ── apa, bayon
     ├── care  ── dpo
     ├── cfo   ── ir
     ├── gtm
     ├── ops   ── raas-config, drones
     └── strat
```
