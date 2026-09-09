# medicalcity

This project uses [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) (v6.12.0) for agile AI-driven development.

## Prerequisites

- Node.js 20+
- [uv](https://docs.astral.sh/uv/) (required for `bmad-build` and `bmad-build-auto`)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Using BMad in Cursor

Skills are installed under `.agents/skills/`. Start with **bmad-help** and ask what to do next.

Typical flow:

1. `bmad-help` — see where you are and the next step
2. Planning: `bmad-brainstorming` → `bmad-product-brief` → `bmad-prd` → `bmad-architecture`
3. Delivery: `bmad-create-epics-and-stories` → `bmad-sprint-planning` → `bmad-dev` / `bmad-build`

Reinstall or update:

```bash
npx bmad-method install --directory . --modules bmm --tools cursor --yes
```
