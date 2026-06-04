---
name: bequite-context-engineer
description: Use when any task spans multiple steps, files, or sessions — keeps the agent grounded in persisted context instead of fading chat memory; prevents context rot, amnesia, and off-convention drift. Master context skill; generalizes the frontend DNA + section-map + compact-summary + continuity-gate pattern to ALL workflows (backend / API / db / security / devops / testing). Loaded alongside bq-plan / bq-implement / bq-auto / bq-recover and the domain specialists.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-context-engineer — persist context, don't remember it

**Core principle (Anthropic effective-context-engineering):** find *the smallest set of high-signal tokens* that produce the right action. Context is a scarce, finite resource — attention is roughly n² in token count, and every model loses focus past some length. More context is not better; the *right* context is. Persist what matters to files; keep the live window small and sharp.

**The failure this prevents:** the same drift the frontend skill fixes for design — but for every workflow. A backend, migration, security fix, or deploy starts grounded, then the architectural decision / reproduced bug / chosen convention scrolls out of the live window, and the model falls back to the statistical average → spaghetti, re-introduced bugs, off-convention code, lost progress between sessions.

## The 3 primitives every long task uses at boundaries (effective-context-engineering + effective-harnesses)

| Primitive | What it does | Keep / preserve | Bias |
|---|---|---|---|
| **COMPACT** | Summarize the window + reinitialize a fresh one | architectural decisions · unresolved bugs · modified files · test/run commands · open questions | **recall > precision** (keep more, lose nothing critical) |
| **CLEAR tool-results** | Drop stale tool output (cheaper than compact) | last 4–6 results live; **keep the `tool_use` record** (the call happened) | drop re-fetchable content first |
| **EXTERNALIZE to files** | Write state/notes/decisions to disk | anything that must survive a reset | durable over in-window |

### Diagnostic: symptom → primitive

| Symptom | Primitive |
|---|---|
| Window growing unbounded, slowing down | **COMPACT** |
| Old re-fetchable tool output piled up (file reads, greps, builds) | **CLEAR tool-results** |
| Facts lost between sessions / after a break | **EXTERNALIZE to memory files** |
| Recall degrading mid-task (model "forgets" what it just did) | **CLEAR + COMPACT** |

## Context rot is real, measurable, and universal — never trust the middle

- Measured across 18 models (Chroma context-rot study): accuracy drops as input grows even when the task is trivial. "Lost-in-the-middle" is a ~15–20pp drop for facts sitting in the **middle** of a long context vs the start/end.
- **Rule:** put must-use facts at the **TOP or BOTTOM** of any prompt, file, or summary — **never the middle**.
- **Rule:** never trust a fact buried mid-conversation. If it matters, **re-read it from a file** before acting on it. "I think we decided X" is a drift in progress — go read the decision.

## Compaction-survival rule (Claude Code memory/context docs)

After a `/compact` (or auto-compact), **only the project-root `CLAUDE.md` + auto-memory are re-injected.** Path-scoped / nested rules and skill bodies are NOT guaranteed back — skill bodies are capped (~5k tokens/skill, ~25k total) and **truncated keeping the START**. Therefore:

1. Anything that must-not-be-forgotten lives in **project-root `CLAUDE.md`** or **auto-memory** — not only in a skill body or a nested rule.
2. The most important instructions go at the **TOP of every file** (truncation eats the end; long context buries the middle).
3. Treat skill bodies as *reloadable reference*, not *persistent state*. State goes to `.bequite/`.

## Machine-read state → JSON. Human narrative → Markdown.

Gates, task status, mode, phase, counters — anything a program (or the agent at session start) parses — belong in **overwrite-resistant JSON**: "the model is less likely to inappropriately change JSON." Audits, notes, decisions, narratives stay **Markdown** (human-first). When both exist, JSON is the source of truth for machine state; Markdown explains *why*.

## PROJECT DNA — the universal generalization of Design DNA

The frontend skill persists a **Design DNA** so new UI matches the established identity. This skill persists a **PROJECT DNA** so new *code* matches the established codebase instead of drifting into spaghetti.

- **Lives in:** `.bequite/state/PROJECT_DNA.md`.
- **Records:** conventions · architecture / layering · naming · error-handling pattern · validation pattern · test style + runner · dependency direction (what may import what) · logging/observability pattern · config/secrets pattern · the "house style" of this repo.
- **Read it BEFORE any implementation** (backend, db, security, devops, testing — same as FE reads Design DNA before UI code).
- The **Consistency check** judges new code against the DNA: does this match the repo's patterns, or did it freestyle? Off-DNA code is a drift to fix while cheap.
- If `PROJECT_DNA.md` is missing/placeholder, fill + lock it from the existing code before writing new code. For frontend work, the Design DNA (`.bequite/design/DESIGN_DNA.md`) is the UI-specific sibling — read both for UI tasks.

## WORKING_NOTES — the universal scratchpad

`.bequite/state/WORKING_NOTES.md` is the generic cousin of the frontend section map. **Every** workflow (backend / db / security / devops / testing) appends the **same 4-line shape** per step:

```
## <step / task id> — <timestamp>
- what I tried:
- what I learned:
- what's pending:
- what to re-read next:
```

This is the externalized scratchpad that survives compaction and session breaks — `/bq-recover` reads it to know where you were.

## Path-scoped rules keep always-on context small

Put domain rules in `.claude/rules/*.md` with a `paths:` frontmatter glob so they load **only when matching files are touched** (e.g. an API-error-handling rule that loads on `src/api/**`). This keeps the always-on context lean — high-signal rules appear exactly when relevant instead of bloating every turn. (Per the compaction-survival rule above, these can be dropped after `/compact`, so duplicate any *must-not-forget* line into root `CLAUDE.md`.)

## Session-orientation ritual (effective-harnesses) — do this BEFORE implementing

1. Re-read state: `PROJECT_DNA.md` · `WORKING_NOTES.md` · `WORKFLOW_GATES.md` · `CURRENT_PHASE.md` · `LAST_RUN.md` + recent `git log`.
2. Pick the **single highest-priority** item.
3. Run a **basic end-to-end check** (install / build / smoke) to confirm a known-good baseline.
4. **One task at a time.** Finish + verify before starting the next.
5. **Never delete or edit a test to make it pass.** Fix the code or fix the test for the right reason, then say why.

## Compact-summary discipline (token-saver friendly)

Keep a **1-screen digest** the agent reads every task — the generic cousin of `FRONTEND_CONTEXT_SUMMARY.md`. It holds: DNA gist · active task · touched files · open risks · last verify result · what-to-re-read. Escalate to the full files (`PROJECT_DNA.md`, plan, prior reports) **only when the digest is insufficient**. Re-reading the whole `.bequite/` tree every micro-step is the opposite failure — it wastes context and pushes other facts out.

## Sub-agent context isolation (effective-harnesses)

Spin a sub-agent in a **fresh window** for read-heavy work; have it return only a **1–2k-token distilled conclusion**, not its raw transcript. Multi-agent runs cost **~15× the tokens** of a single agent — use isolation for **research / discovery / audit** (read-heavy, parallelizable), **NOT** for tightly-coupled implementation where one agent must hold the whole thread.

## When this skill activates

Any multi-step / multi-file / multi-session task. Invoked alongside `/bq-plan`, `/bq-implement`, `/bq-auto`, `/bq-recover`, and the domain specialists (backend / database / security / devops / testing). For UI work it defers to the frontend cousin — see below.

## Effort awareness (`${CLAUDE_EFFORT}` / Ultracode)

- **low / medium** — compact-only: read the 1-screen digest; compact at boundaries; minimal externalization.
- **high** — full primitives: compact + clear + externalize at every boundary; read `PROJECT_DNA.md` + `WORKING_NOTES.md` per task; run the Consistency check.
- **xhigh / max / Ultracode** — full externalization + **per-step re-read**: re-orient before each step, persist a note after each step, JSON-track machine state, isolate read-heavy work to sub-agents.

If effort is unavailable, infer from operating mode: `deep`→high+, `fast`→compact, `token-saver`→digest + JSON state only, `delegate`→strong model writes DNA + notes shape, cheap model fills, strong model verifies.

## Cross-references

- `docs/architecture/CONTEXT_ENGINEERING.md` — the full doctrine (this skill is its operational front end).
- `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md` + `bequite-frontend-design-system` — the **frontend cousin**; this skill is the generalization. For UI tasks, that pair owns Design DNA + section map; this skill owns the generic PROJECT DNA + working notes.
- `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` — the read-before-act rule this skill operationalizes.

## Tool neutrality (global rule)

Every tool / mechanism named here (`/compact`, JSON state, path-scoped rules, sub-agents) is the **Claude Code mechanism**, not a project dependency — they install nothing. The *principles* (smallest high-signal set, persist-don't-remember, never-trust-the-middle, JSON-for-machine-state) are universal. Don't auto-install anything. See `.bequite/principles/TOOL_NEUTRALITY.md`.

## When NOT to use this skill

- A single-shot, single-file change that finishes in one turn → no context engineering needed; just do it.
- Pure UI continuity across sections → use `bequite-frontend-design-system` (this skill defers to it for design identity).
- Read-only orientation only → `/bq-now` or `/bq-recover` already apply the relevant slice.
- The task fits entirely in one short window with no decisions worth persisting → skip the ceremony.

## Quality gate

Before claiming this skill's work complete:

- [ ] `PROJECT_DNA.md` exists + read before implementation; new code passed the Consistency check
- [ ] `WORKING_NOTES.md` updated with the 4-line shape for each step taken
- [ ] Machine state (gates / task status / mode / phase) lives in JSON, not buried in prose
- [ ] Must-not-forget facts are in root `CLAUDE.md` / auto-memory (survive `/compact`), not only in a skill body or nested rule
- [ ] No critical fact relied on from the middle of the conversation — re-read from file
- [ ] Compact summary kept to ~1 screen and current
- [ ] Sub-agents (if used) returned distilled 1–2k-token conclusions, not raw transcripts
- [ ] No banned weasel words; no auto-installed dependency
- [ ] `AGENT_LOG.md` + state files updated

If any item fails, report PARTIAL with the specific gap — do not claim done.
