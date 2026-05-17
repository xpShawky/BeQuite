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

---

## New in v3.0.0-alpha.4 — scoped auto, UI variants, live edit

### `/bq-auto [intent] "task"` — scoped autonomous runner

Run a task end-to-end without per-step approval clicks. The agent parses the intent (17 types) and runs only the relevant scope. Pauses only at hard human gates (destructive ops, DB migrations, prod / VPS touches, secret rotations, etc.).

```
You: /bq-auto fix "Fix hidden text on dashboard"
You: /bq-auto uiux variants=5 "Create 5 dashboard concepts"
You: /bq-auto live-edit "Pricing cards less crowded"
You: /bq-auto new "Build pharmacy SaaS admin"
You: /bq-auto security "Audit + fix issues"
You: /bq-auto deploy "VPS deployment plan + execute"
```

Auto-mode continues by default. It does NOT ask "should I continue?" or "do you approve the plan?" unless a hard gate trips.

Full strategy: `docs/architecture/AUTO_MODE_STRATEGY.md`.

### `/bq-uiux-variants [N] "task"` — explore N design directions

Generate 1-10 **isolated** UI variants in parallel. Each is a different design direction (not a color tweak). Original UI stays intact. User picks winner; agent merges.

```
You: /bq-uiux-variants 3
You: /bq-uiux-variants 5 "five dashboard concepts"
You: /bq-uiux-variants 10 "ten landing page concepts"   # requires confirmation
```

Variants live at `/uiux/v1`, `/uiux/v2`, etc. (or `src/uiux-variants/Variant01/` if routing is harder). After user selects, winner merges into main UI; rejected variants archive at `.bequite/uiux/archive/`.

Full strategy: `docs/architecture/UIUX_VARIANTS_STRATEGY.md`.

### `/bq-live-edit "task"` — section-by-section frontend edits

Lightweight section-mapped editing of a running frontend. Maps visible sections to source files (`.bequite/uiux/SECTION_MAP.md`), applies the smallest possible edit, verifies via build + (optional) screenshots, logs to `.bequite/uiux/LIVE_EDIT_LOG.md`.

```
You: /bq-live-edit "Make pricing cards less crowded"
You: /bq-live-edit "Improve empty state on /dashboard"
You: /bq-live-edit "Fix mobile layout on hero"
```

**Lightweight.** No heavy Studio. No separate app. No Figma clone. **Does NOT auto-install Playwright** — uses code inspection if browser automation isn't already available.

Full strategy: `docs/architecture/LIVE_EDIT_STRATEGY.md`.

---

## Walkthroughs added in alpha.15

### Walkthrough — Operating modes (alpha.12)

BeQuite has **4 composable operating modes**: Deep / Fast / Token Saver (alias `lean`) / Delegate. All 17 hard human gates still apply regardless of mode.

#### Deep Mode — quality-critical work

```
/bq-auto deep "Build a SaaS dashboard for clinic booking"
/bq-research deep "Stack, security, deployment for medical SaaS in MENA region"
/bq-feature deep "Add booking automation module"
```

Full 11-dim research, multi-plan prompted, red-team mandatory at phase transitions, searches beyond obvious sources (Reddit / HN / Product Hunt / niche forums / non-English markets). Use for production, regulated work, new builds, security-critical changes.

#### Fast Mode — small scoped work

```
/bq-auto fast "Fix the dashboard text contrast"
/bq-fix fast "Install error on /bq-init"
/bq-feature fast "Add export button to reports table"
```

Shortcuts discovery if recent DISCOVERY_REPORT exists; 3-dim research (stack + security + scale); reuses memory; skips multi-plan + red-team. **Still tests + verifies + logs.** Not low-quality mode. Use for trivial scoped fixes, trusted stack, prototypes.

#### Token Saver Mode (alias `lean`)

```
/bq-auto token-saver "Update one config file"
/bq-auto lean "Same as above; shorter alias"
/bq-review token-saver "Review only current diff"
```

Reads core memory only; summaries before full files; reuses prior research; targeted greps over broad reads; compact reports. **Not the same as Fast.** Fast optimizes speed; Token Saver optimizes token cost. **Token-saving, NOT token-free.**

#### Delegate Mode — Architect Delegate pattern

Two-session workflow. Strong model architects + reviews; cheap model implements. 40–70% cost savings on large features.

Session 1 (strong model — Opus / GPT-5 class):

```
/bq-auto deep delegate "Build the e-commerce checkout module"
```

Writes `.bequite/tasks/DELEGATE_TASKS.md`, `DELEGATE_INSTRUCTIONS.md`, `DELEGATE_ACCEPTANCE_CRITERIA.md`, `DELEGATE_TEST_PLAN.md`.

Session 2 (cheap model — Sonnet / smaller, separate Claude Code session):

```
/bq-implement delegate
```

Executes per the task pack — no architectural decisions.

Session 3 (strong model — back):

```
/bq-review delegate
```

Writes `.bequite/audits/DELEGATE_REVIEW_REPORT.md` with per-task verdicts (✅ APPROVED / ⚠ APPROVED-WITH-COMMENTS / ❌ REJECTED). Strong model fixes or re-instructs.

Use for large features with clear shape + precise acceptance criteria. Don't use for tiny tasks or exploratory work.

#### Mode composition

```
/bq-auto fast token-saver "Quick small fix with low context"
/bq-auto deep token-saver "Thorough planning with compact output"
/bq-auto deep delegate "Strong model architects new feature"
/bq-auto fast delegate "Cheap impl of well-understood feature"
```

Conflicts (`fast` + `deep`): agent asks one question and defaults sanely. Mode tracking: every `/bq-auto` run appends to `.bequite/state/MODE_HISTORY.md`.

---

### Walkthrough — `/bq-presentation` (alpha.13)

Premium PPTX or HTML presentation builder. Natural language; quotes optional.

Common patterns:

```
/bq-presentation Create a lecture about infection control for doctors, 30 minutes, premium style

/bq-presentation format=pptx variants=3 topic=infection-control audience=doctors

/bq-presentation [format=both, variants=3, style=cinematic, audience=tech-executives] Create a keynote about AI agents

/bq-presentation strict=true source=folder ./course-materials Turn this material into slides

/bq-presentation creative=true Create a premium keynote-style deck about study skills

/bq-auto presentation format=both variants=5 deep "Create a premium lecture about AI agents"
```

What runs:

1. Parses natural language + options (`format` / `variants` / `source` / `strict` / `creative` / `audience` / `style` / `duration` / `language` / `brand`)
2. Reads core memory + source files
3. Writes 9 artifacts to `.bequite/presentations/` (BRIEF / OUTLINE / SLIDE_PLAN / DESIGN_BRIEF / MOTION_PLAN / SPEAKER_NOTES / REFERENCES / VARIANTS_REPORT / EXPORT_LOG)
4. When `variants>1`: pauses for user winner selection (hard human gate)
5. When user requests implementation: renders PPTX or HTML (tool-neutral — decision section required)

Strict vs Creative:

- `strict=true` — PDF / Word / scientific source preserved; don't invent facts; every claim traces to `REFERENCES.md`
- `creative=true` — Topic-only / keynote / marketing; may add hooks + story arcs; assumptions explicitly marked

PPTX vs HTML:

- PPTX — Institutional / lecture / offline / Office users / speaker recording
- HTML — Cinematic / responsive / product demo / interactive
- both — Same content; two renders for different audiences

Full reference: `.claude/commands/bq-presentation.md` and `.claude/skills/bequite-presentation-builder/SKILL.md`.

---

### Walkthrough — `/bq-auto` for everything (the umbrella)

`/bq-auto` is the most powerful command. Dispatches to the right workflow based on intent.

```
/bq-auto new "Build a SaaS bookings dashboard for clinics"
/bq-auto existing "Audit this repo for security gaps"
/bq-auto feature "Add user-export-to-CSV"
/bq-auto fix "Hidden text on /pricing"
/bq-auto uiux variants=5 "Redesign the marketing site"
/bq-auto security "Run security review + fix OWASP-A03 findings"
/bq-auto deploy "Plan VPS deployment with safety gates"
/bq-auto presentation format=both variants=3 "Premium lecture about AI agents"
```

Auto mode continues by default. Pauses only at the 17 hard human gates (destructive ops, DB migrations, prod / VPS / SSL, secrets, paid services, scope contradictions, variant winner selection, cost ceilings, repeated failures, etc.).

Full strategy: `docs/architecture/AUTO_MODE_STRATEGY.md`.

---

### The global feature-addition rule (alpha.14)

When working on BeQuite itself (or any project where BeQuite acts as the meta-system), every new feature must travel through the 15-step workflow defined in `docs/architecture/WORKFLOW_GATES.md` § "Feature-addition workflow (alpha.14 — global rule)":

1. Memory entry → 2. Research → 3. Scope → 4. Plan → 5. Tasks → 6. Implement → 7-13. Docs + logs + changelog → 14. `/bq-verify` → 15. Version bump

Even when the user provides a detailed spec inline, the agent must not shortcut to implementation. Exemptions: hotfixes + doc-only changes + skill additions activated only from existing commands can skip steps 2-5.

See `.bequite/audits/FEATURE_WORKFLOW_AUDIT.md` for the alpha.13 precedent that motivated this rule.
