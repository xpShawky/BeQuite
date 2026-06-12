# Using BeQuite with Smaller / Cheaper / Local Models

BeQuite makes weaker models perform better by forcing structure: memory, checklists, decomposition, evidence, and gates. **It narrows the gap — it does not make a small model a frontier model.** Strategy: `docs/architecture/LOW_COST_MODEL_EXECUTION_STRATEGY.md` · rules card: `.bequite/state/LOW_COST_MODEL_RULES.md` · agent setup: `INSTALL_FOR_OTHER_AGENTS.md`.

## The recipe (any Tier B/C model)

1. **Decompose first (Tier A or you):** run `/bq-plan delegate` + `/bq-assign delegate` (or write the pack by hand) so each task has: exact file paths · files NOT to touch · steps · edge cases · test commands · acceptance criteria · common mistakes · rollback notes.
2. **Brief the model per task, not per project:** paste ONE task + the orientation block (read `CLAUDE.md` rules, `.bequite/state/CONTEXT_SUMMARY.md`, the task file) + the relevant SKILL.md sections **as text** (small models get checklists, not auto-attach) + the 10-rule frontier card (`.bequite/state/FRONTIER_REASONING_SUMMARY.md`).
3. **Demand evidence per step:** command + exit code + output after every change; assumption ⇒ written to `ASSUMPTIONS.md`; unknown ⇒ `UNVERIFIED`, never improvised.
4. **Gate the output:** run the Guard Pass checklists over everything produced (hallucinated APIs · hardcoded success · over-mocking · doc drift are exactly small-model failure modes); risky tasks get a stronger-model review (`/bq-review delegate`).
5. **Verify before accepting:** `/bq-verify` (or its playbook) with the task's test commands; treat the small model's own confidence as a claim to check.

## Per-target notes

- **Cheaper Claude models (Haiku-class) in Claude Code:** everything works natively (skills auto-attach); still apply task-chunking + delegate review for risky work.
- **Codex/ChatGPT workflows:** orientation block in AGENTS.md; one task per session; paste skill checklists.
- **Cursor (cheaper model selected):** task pack in context + rules file; keep diffs small; review with a stronger model before applying broadly.
- **Ollama / local models (Tier C):** smallest chunks; drafts/boilerplate/demo-data/summaries only; exact paths; expect to iterate; never the hard-list items (security, migrations, auth, payments, destructive/broad edits, release approval).
- **Hermes/OpenClaw-style autonomous harnesses:** wire the 15-step sequence (`AUTO_MODE_RULES.md`) as the loop; hard gates = harness approvals; Guard Pass mandatory before any auto-merge.

## What never goes to small models

Production security decisions · DB migrations · auth changes · payment logic · destructive edits · broad refactors · final release approval — same list as `LOW_COST_MODEL_RULES.md`, aligned with the 17 hard gates and R3 file tiers.
