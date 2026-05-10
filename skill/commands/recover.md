---
name: bequite.recover
description: Generate recovery prompt for a new session. Reads state/recovery.md + state/task_index.json + Memory Bank + last receipts; produces a paste-able prompt that resumes from the next safe task without requiring chat history (master §25). Works in any host that loads AGENTS.md.
phase: any
persona: orchestrator (this SKILL)
prompt_pack: prompts/recovery_prompt.md
---

# /bequite.recover

When invoked (or `bequite recover`):

## Step 1 — Gather

Read in order:

- `AGENTS.md`, `CLAUDE.md`
- `.bequite/memory/constitution.md`
- All six Memory Bank files
- All accepted ADRs at `.bequite/memory/decisions/`
- `state/project.yaml`, `state/current_phase.md`, `state/recovery.md`
- `state/task_index.json` — find `pending` + `in_progress` items
- `state/decision_index.json`
- `state/evidence_index.json`
- Most recent receipt at `.bequite/receipts/` (v0.7.0+)
- Last 5 entries from `git log --oneline`

## Step 2 — Compute the seven answers (master §25)

1. **What is complete?** — list every sub-version + tag from `git tag -l`. Cross-reference `state/evidence_index.json`.
2. **What is incomplete?** — pending + in_progress tasks.
3. **What failed last?** — `state/recovery.md::What failed last`.
4. **What evidence exists?** — list `evidence/<phase>/<task>/` directories; note which carry receipts.
5. **What is the next safe task?** — `state/recovery.md::What is the next safe task`.
6. **What commands should run first?** — `state/recovery.md::Commands to run first`.
7. **What files must not be touched?** — `state/recovery.md::Files to NOT touch`.

## Step 3 — Render

Produce a paste-able prompt using the template at `prompts/recovery_prompt.md`. The prompt:

- Opens with the seven instructions to read.
- Lists the seven questions to answer.
- Reaffirms the seven Iron Laws.
- Names the binding Mode (Fast / Safe / Enterprise).
- Ends with "Resume only from the next safe task" + "Do not restart the whole project."

## Step 4 — Update state

Refresh `state/recovery.md` with the latest computed values.

## Stop condition

- Recovery prompt rendered to stdout (or to `.bequite/recovery-prompts/<timestamp>.md`).
- `state/recovery.md` refreshed.
- Iron Laws + Mode + active Doctrines surfaced in the rendered prompt.

## Anti-patterns

- Generating recovery from chat history (defeats the purpose — recovery exists *because* chat history may be lost).
- Surfacing only "what's complete" without "next safe task" (incomplete prompt).
- Glossing over failures — list them concretely with file paths + commands to investigate.

## Related

- `state/recovery.md` — the human-readable resume document.
- `prompts/recovery_prompt.md` — the prompt pack template.
- `/bequite.evidence` — list evidence artefacts referenced by the recovery prompt.
