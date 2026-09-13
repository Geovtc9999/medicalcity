# medicalcity

This repo is wired with [Graft](https://github.com/NanoNets/Graft) and [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) for Cursor.

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

