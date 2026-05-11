# Using BeQuite commands — practical guide

This runbook walks through each command with real examples. For the full reference, run `/bq-help` inside Claude Code or read `.claude/commands/bq-help.md`.

---

## The mental model

BeQuite organizes work into **5 phases**:

| Phase | What you're doing | Time |
|---|---|---|
| 0 — Setup & Understanding | Learn what's there | minutes |
| 1 — Problem Framing | Decide what to build | minutes to hours |
| 2 — Build | Write the code | hours |
| 3 — Quality | Confirm it works | minutes |
| 4 — Ship | Release | minutes |
| 5 — Continue Later | Resume next time | seconds |

Each phase has 3-5 commands. You'll run most projects through all five.

---

## Phase 0 — Setup and Understanding

### `/bequite` — the menu

```
You: /bequite
```

Output:

```
BeQuite by xpShawky — lightweight project skill pack

Status:
  Project type:    existing repo (Next.js + Drizzle detected)
  BeQuite state:   initialized
  Current phase:   Phase 0
  Last run:        none

Recommended next 3 commands:
  1. /bq-discover     write DISCOVERY_REPORT.md
  2. /bq-doctor       environment health
  3. /bq-clarify      ask user 3-5 questions
```

Read-only. Never modifies anything. Use it as orientation any time.

### `/bq-help` — full reference

```
You: /bq-help
```

Shows every command grouped by phase + when to use + what it reads + what it writes + next.

### `/bq-init` — formal initialize

```
You: /bq-init
```

Creates `.bequite/state/`, baseline state files, appends a BeQuite section to `CLAUDE.md`. Only needed if `/bequite` shows "BeQuite state: fresh" — usually the installer already did this.

For brand-new empty projects:

```
You: /bq-init new
```

Skips the existing-repo discovery + jumps straight to `/bq-clarify`.

### `/bq-discover` — inspect the repo

```
You: /bq-discover
```

Writes `.bequite/audits/DISCOVERY_REPORT.md`. Includes:

- Detected stack (Next.js / Python / Rust / Go / etc.)
- Apps + entry points
- Ports used
- Package manager
- Tests
- CI
- Docs quality
- Risks + smells

Typical output time: ~30 seconds. The agent reads a few dozen files with Read + Glob + Grep.

### `/bq-doctor` — environment health

```
You: /bq-doctor
```

Probes `node`, `npm`, `python`, `docker`, `bun` on your PATH. Checks ports. Reads README usefulness. Writes `.bequite/audits/DOCTOR_REPORT.md`.

If anything is missing, prints clear install hints.

---

## Phase 1 — Problem Framing

### `/bq-clarify` — high-value questions only

```
You: /bq-clarify
```

The agent reads OPEN_QUESTIONS.md + DISCOVERY_REPORT.md, then asks **3-5 specific questions** with recommended defaults. You can:

- Answer specifically
- Say "default" or "yes" to accept the recommended default
- Say "skip" to skip that question
- Say "all defaults" to accept every default at once

Example:

```
Agent: Q1. What scale are you targeting for v1?
        Why it matters: Stack picks differ for 50 users vs 50,000.
        Recommended default: small_saas (50-5,000 MAU)

You:   default

Agent: Q2. PII / PHI / PCI involved?
        ...

You:   no

Agent: ... (3 more questions or fewer)

Agent: Recorded 3 answers to .bequite/state/OPEN_QUESTIONS.md.
       Next: /bq-plan
```

### `/bq-research` — verify libraries aren't deprecated

```
You: /bq-research
```

For each "X vs Y" question, the agent uses WebFetch to verify:

- Last release date
- Stars + commits
- CVEs (via OSV scanner)
- License (flags AGPL / GPL surprises)
- Pricing (current rates, not from memory)

Writes `.bequite/audits/RESEARCH_REPORT.md` with a verdict per option.

### `/bq-scope` — lock the boundaries

```
You: /bq-scope
```

Forces a commit to IN / OUT / NON-GOALS. The agent drafts the three lists; you confirm or move items.

Writes `.bequite/plans/SCOPE.md`. Critical — every later `/bq-add-feature` checks against this.

### `/bq-plan` — write the implementation plan

```
You: /bq-plan
```

The most important command. Writes `.bequite/plans/IMPLEMENTATION_PLAN.md` with:

1. Vision
2. Current context
3. Non-goals (from SCOPE.md)
4. Architecture diagram
5. Stack decision table
6. File plan (every file, NEW/MODIFIED/DELETED)
7. Phase plan (timeline + acceptance evidence)
8. Task plan (atomic ≤5min tasks)
9. Test plan
10. Risks + mitigations
11. Acceptance criteria
12. Rollback plan
13. Open questions

**No code written yet.** Pure planning. You approve the plan before any implementation.

### `/bq-multi-plan` — second opinion via manual paste

```
You: /bq-multi-plan
```

The agent writes two identical prompts (Claude + ChatGPT). You open both in your browser, paste each prompt, copy the responses back to BeQuite. BeQuite merges + identifies disagreements.

ToS-clean ($0 in API tokens — uses your subscriptions). Use for high-stakes decisions.

---

## Phase 2 — Build

### `/bq-assign` — break plan into tasks

```
You: /bq-assign
```

Reads `IMPLEMENTATION_PLAN.md`, writes `.bequite/tasks/TASK_LIST.md`:

```
- [ ] T-1.1 — Init Next.js 15 app
        Files: package.json, next.config.ts, tsconfig.json
        Acceptance: npm run dev returns HTTP 200 on /
        Depends on: none

- [ ] T-1.2 — Set up Drizzle + Supabase client
        ...
```

Every task is atomic (≤5 min) with one acceptance criterion.

### `/bq-implement` — workhorse

```
You: /bq-implement
```

Picks the next `[ ] pending` task. Reads files first. Makes minimal changes. Runs the test. Verifies the acceptance. Updates `[ ] → [x]`. Stops on blocker.

```
You: /bq-implement T-2.3
```

Force a specific task ID.

### `/bq-add-feature` — safer mini-cycle

```
You: /bq-add-feature "CSV export on the bookings page"
```

For features that don't need the full `/bq-plan` → `/bq-assign` cycle. Spec → impl → test atomically.

### `/bq-fix` — diagnose + repair a bug

```
You: /bq-fix
```

The agent asks for the symptom + reproduction. Then:

1. Reproduces (no fix without reproduction)
2. Finds root cause (5-whys)
3. Smallest safe patch
4. Adds test
5. Verifies symptom is gone

Writes the bug + cause + fix to `.bequite/logs/ERROR_LOG.md`.

---

## Phase 3 — Quality

### `/bq-test` — run + write tests

```
You: /bq-test
```

Detects framework (vitest / jest / pytest / cargo test). Runs them. Identifies coverage gaps in recently-changed source files. Asks if you want to write missing tests.

### `/bq-audit` — comprehensive product audit

```
You: /bq-audit
```

10-area audit across install / run / frontend / API / CLI / tests / docs / UX / security / release. Severity-tagged findings (Blocker / High / Medium / Low) with file:line + suggested fix.

Writes `.bequite/audits/FULL_PROJECT_AUDIT.md`.

### `/bq-review` — review current changes

```
You: /bq-review
```

Per-file commentary on uncommitted diff + recent commits. Verdict: Approved / Approved-with-comments / Blocked.

### `/bq-red-team` — adversarial Skeptic

```
You: /bq-red-team
```

8 attack angles. Severity-tagged findings. Kill-shot questions you must answer.

---

## Phase 4 — Ship

### `/bq-verify` — full gate matrix

```
You: /bq-verify
```

Runs every applicable gate (install / lint / typecheck / unit / integration / build / smoke / e2e). Writes `.bequite/audits/VERIFY_REPORT.md`. Either PASS or FAIL.

### `/bq-release` — release prep

```
You: /bq-release
```

Only proceeds if verify PASSED. Bumps version. Moves `[Unreleased]` → `[v<new>]` in CHANGELOG. Prints the git commands (you copy + run; nothing auto-pushed).

### `/bq-changelog` — keep CHANGELOG sharp

```
You: /bq-changelog
```

Categorizes recent commits into Added / Changed / Fixed / Deprecated / Removed / Security per Keep a Changelog v1.1.

---

## Phase 5 — Continue Later

### `/bq-memory` — see / snapshot memory

```
You: /bq-memory
You: /bq-memory show plans
You: /bq-memory snapshot
You: /bq-memory refresh
```

### `/bq-recover` — resume after a break

```
You: /bq-recover
```

Reads everything in `.bequite/`. Finds last green checkpoint. Tells you exactly what's safe to do next. The single most useful command after a session break.

### `/bq-handoff` — generate a handoff package

```
You: /bq-handoff
```

Writes `HANDOFF.md` at repo root. Two sections — engineer + non-engineer (vibe-handoff). Receiver checklist. Everything needed for a second engineer to pick up cold.

---

## When to break the rules

The workflow phases are a default; not a religion. You can:

- Skip `/bq-clarify` if the project is well-defined
- Skip `/bq-research` if you've already decided the stack
- Run `/bq-fix` without `/bq-implement` if you're just fixing a bug
- Run `/bq-audit` at any phase (not just Phase 3)
- Run `/bq-recover` at any time after a break

The point is **discipline + memory**, not the specific sequence.

---

## When BeQuite slows you down

If the workflow feels heavy for a small change:

- Skip ahead. Run `/bq-add-feature` directly without `/bq-plan` for tiny features.
- Don't run `/bq-verify` for trivial changes. Use `/bq-test` alone.
- For prototyping / spike work, run `/bequite` once for orientation, then ignore the rest.

BeQuite's discipline is meant for **changes that affect users**. Use it lightly for spikes.
