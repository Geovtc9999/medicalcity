# medicalcity

Infrastructure IA-native de la santé autonome — [medicalcity.ai](https://medicalcity.ai)

## Comex d'agents IA exécutifs

Ce dépôt contient le **système d'exploitation du Comex** : charte, architecture, prompts des 7 sièges, playbooks, et le livrable de travail Président.

| Livrable | Chemin |
|---|---|
| **Deck McKinsey (PDF)** | [`docs/comex/MedicalCity-Comex-IA-ScaleUp.pdf`](docs/comex/MedicalCity-Comex-IA-ScaleUp.pdf) |
| Deck source (HTML) | [`docs/comex/deck.html`](docs/comex/deck.html) |
| Charte de gouvernance | [`comex/CHARTE.md`](comex/CHARTE.md) |
| Architecture YAML | [`comex/architecture.yaml`](comex/architecture.yaml) |
| Prompts des 7 sièges | [`comex/agents/`](comex/agents/) |
| Playbook Comex 90 min | [`comex/playbooks/comex-hebdo.md`](comex/playbooks/comex-hebdo.md) |
| Plan 90 jours | [`comex/playbooks/90-jours.md`](comex/playbooks/90-jours.md) |

### Instancier un siège

Le fichier `comex/agents/<siege>.md` est le system prompt (SMCI). Mémoire partagée = ce dépôt. L'orchestrateur `age-comex` est le seul à convoquer les autres.

### Rebuild du PDF

```bash
python3 tools/build_deck.py
```

Produit `docs/comex/deck.html` puis imprime le PDF via Chrome headless.
