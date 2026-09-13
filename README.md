# medicalcity

This repo is wired with [Graft](https://github.com/NanoNets/Graft), [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), and [Verdent AI](https://www.verdent.ai/) for Cursor.

## Graft

Local context graph of the code. After cloning, generate it (no API key required):

```bash
npx @nanonets/graft build
```

## BMAD

Agile AI-driven development skills live in `.agents/skills/` (29 skills, including `bmad-help`, `bmad-prd`, `bmad-build`, and the analyst / PM / UX / architect / developer agents).

After cloning:

1. Install [uv](https://docs.astral.sh/uv/) — required by `bmad-build` and `bmad-build-auto`.
2. Restart Cursor so the BMAD skills load.
3. Start with `/bmad-help`.

## Verdent AI

Verdent is a Cursor/VS Code coding agent (extension `verdentai.verdent`), not a project skill. This repo recommends it in `.vscode/extensions.json`.

In Cursor:

1. Open Extensions (`Cmd+Shift+X` / `Ctrl+Shift+X`)
2. Search for **Verdent** by Verdent AI
3. Install, then sign in (account required; 7-day trial available)
4. Open the Verdent sidebar (`Cmd+L` / `Ctrl+L`)

Desktop app (macOS/Windows): [verdent.ai/download](https://www.verdent.ai/download). Linux uses the editor extension.

