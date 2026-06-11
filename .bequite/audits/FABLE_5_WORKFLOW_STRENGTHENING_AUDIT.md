# BeQuite — Fable 5 Workflow Strengthening Audit

**Audit run:** 2026-06-11
**Auditor:** Claude Fable 5 (strongest available model — confirmed active) · Deep Mode · `/bq-auto`-style full pass
**Repo state at audit:** v3.0.0-alpha.18 (commit `bcd7511` on main; clean tree)
**Direction check:** lightweight preserved — no Studio / heavy CLI / dashboard / Docker / runtime deps found in active surface ✅

---

## 0. The most important finding first

**A large share of this strengthening request is already shipped.** Alpha.17 (Frontend Design Continuity) and alpha.18 (Harness, Hooks & Context-Engineering) — both released 2026-06-04 — delivered the context-engineering, harness, hooks, design-continuity, and game-changer-discovery targets. This audit therefore does two things: (a) **verifies** what exists and whether it actually holds together, and (b) isolates the **genuine gaps** so this pass strengthens instead of duplicating. Duplicating existing docs under new filenames would itself be a context-engineering failure (two sources of truth = drift).

---

## 1. Current workflow state

- **Version:** v3.0.0-alpha.18 · previous alpha.17 · both shipped 2026-06-04
- **Mode:** none selected (template state — this repo uses /bq-auto passes, mode set per run)
- **Phase:** P0 template state
- **Gate ledger:** template state for installed projects; BeQuite-itself runs are tracked via LAST_RUN + AGENT_LOG
- **Last run:** alpha.18 ship; next-suggested was "live verification of hooks OR alpha.19 game-changer build" — this Fable pass supersedes that suggestion with a strengthening pass

## 2. Current command structure (45 files)

1 root menu (`bequite.md`) + 43 active `bq-*` + 1 deprecated alias (`bq-add-feature` → `bq-feature`).
Categories: Root/orientation (4) · P0 (6) · P1 (6) · P2 (4+alias) · P3 (4) · P4 (3) · P5 (3) · Orchestrators (7) · UI (2) · Opportunity (3) · Creative+Content (1) · Maintenance (1).
All have YAML frontmatter; alpha.15 added gate-check + memory preflight + writeback to the 16 that lacked them; alpha.18 upgraded review/verify/discover/fix/feature/plan/assign/auto with reliability discipline.

## 3. Current skill structure (24 skills)

7 baseline + 7 specialist + live-edit + 3 opportunity + updater + delegate-planner + presentation-builder + **frontend-design-system (master, alpha.17)** + **context-engineer (alpha.18)** + **anti-hallucination (alpha.18)** + workflow-advisor.
All 24 have valid frontmatter + When NOT to use + Quality gate (alpha.15/16 repairs verified still present). `frontend-design-system` is the first **master/coordinator** skill — a useful new architectural tier.

## 4. Current memory structure

`.bequite/state/` (15 files incl. PROJECT_DNA, WORKING_NOTES, FRONTEND_CONTEXT_SUMMARY, MODE_HISTORY, MISTAKE_MEMORY — seeded with 10 `[fe][design]` rules) · `logs/` · `audits/` · `plans/` (incl. FILE_RESPONSIBILITY_MAP) · `design/` (DESIGN_DNA, FRONTEND_SKILL_MAP, DESIGN_CONTINUITY_REPORT) · `presentations/` (9 templates) · `jobs/` `money/` `uiux/` `research/` `prompts/` `principles/` `decisions/` `backups/` + `MEMORY_INDEX.md`.
**Missing:** `.bequite/writing/` (no Writing DNA memory) · `CONTEXT_SUMMARY.md` (generic, non-frontend compact summary) · `EVIDENCE_LOG.md` (alpha.18's anti-hallucination skill demands evidence-over-claims but gives it no dedicated ledger file).

## 5. Current docs structure

`docs/architecture/` 16 files — incl. alpha.18's CONTEXT_ENGINEERING.md, HARNESS_AND_PROMPT_QUALITY.md, CLAUDE_CODE_HOOKS_STRATEGY.md and alpha.17's DESIGN_CONTINUITY_GATE.md, FRONTEND_CONTEXT_ENGINEERING.md. `docs/specs/` 5 files incl. GAME_CHANGER_FEATURES.md + CAPABILITY_FEATURE_IDEAS.md. 5 ADRs (ADR-005 now **Accepted — implemented opt-in alpha.18**). `docs/legacy/` archive intact.

## 6. Current workflow gate state

23 workflow gates + 17 hard human gates + Design Continuity Gate (alpha.17: `DESIGN_DNA_LOCKED`, `DESIGN_CONTINUITY_PASS`, `VISUAL_QA_DONE` wired into 9 commands) + opt-in machine-enforcement hooks (alpha.18: destructive-op block, secret scan, weasel-word stop — NOT active by default, RCE-vector review model).

---

## 7. Weakness findings

### 7a. Context engineering weaknesses (remaining)

| # | Weakness | Evidence | Fix in this pass |
|---|---|---|---|
| C1 | No **generic** compact context summary — alpha.17 added FRONTEND_CONTEXT_SUMMARY but backend/db/long multi-domain work has no equivalent | `.bequite/state/` listing | Create `CONTEXT_SUMMARY.md` template + wire into context-engineer skill flow |
| C2 | **No evidence ledger.** `bequite-anti-hallucination` demands "paste command + exit code + output" but there's no durable file to accumulate evidence across a long run — it lives in chat and dies at compaction | anti-hallucination SKILL has no memory target for evidence | Create `.bequite/research/EVIDENCE_LOG.md` |
| C3 | **No-research-repeat rule** is implied (token-saver "reuse cached research") but never stated as a hard rule with a lookup step | RESEARCH_DEPTH_STRATEGY has no "check .bequite/research/ first" step | State the rule in CONTEXT_ENGINEERING_STRATEGY + execution contract step 5 |
| C4 | **Context packs** are ad-hoc — frontend has one (DESIGN_DNA + SECTION_MAP + FRONTEND_CONTEXT_SUMMARY); presentation has one (9 templates); but there's no named pattern telling a new feature WHICH files form its pack | implicit only | Name the "context pack" pattern in CONTEXT_ENGINEERING_STRATEGY with the 4 existing packs as instances |
| C5 | Writing has **no DNA** — the third DNA pillar (project / design / writing) is missing entirely | no `.bequite/writing/` | Build Writing DNA feature (this pass) |

### 7b. Prompt engineering weaknesses

| # | Weakness | Fix |
|---|---|---|
| P1 | HARNESS_AND_PROMPT_QUALITY.md covers prompt quality but there's **no reusable pattern file** — commands re-derive prompt shapes instead of referencing named patterns | Create `.bequite/prompts/PROMPT_PATTERNS.md` (role+goal+constraints+sources+output-format skeletons per mode) |
| P2 | No single standard distinguishing **compact prompts (token-saver) vs complete prompts (deep) vs neutral prompts (multi-plan) vs strict prompts (source fidelity)** in one reference | Create `PROMPT_ENGINEERING_STANDARD.md` indexing the four prompt classes |
| P3 | Multi-plan neutrality (zero Claude-bias in external prompts) is documented in bq-multi-plan but not generalized to delegate-mode task packs | Note in standard: delegate INSTRUCTIONS must also avoid biasing the cheap model with unverified architectural opinions stated as facts |

### 7c. Harness engineering weaknesses

| # | Weakness | Fix |
|---|---|---|
| H1 | The 11-step execution contract exists **in fragments** (alpha.15 preflight/writeback blocks + alpha.18 reliability rules) but no single contract doc a command can cite in one line | Create `COMMAND_EXECUTION_CONTRACT.md` — canonical 11 steps |
| H2 | Strategy discoverability: harness knowledge is split across HARNESS_AND_PROMPT_QUALITY + CLAUDE_CODE_HOOKS_STRATEGY + MEMORY_FIRST_BEHAVIOR + per-command blocks. New contributor can't find the index | Create `HARNESS_ENGINEERING_STRATEGY.md` as the thin index; same for `CONTEXT_ENGINEERING_STRATEGY.md` |
| H3 | **File-edit safety gap:** hooks block destructive *shell* ops + secret strings, but risky *file edits* (auth middleware, migrations, nginx, CI/CD, payment code, RLS) pass through with no risk classification | Create FILE_RISK_CLASSIFICATION.md + FILE_RISK_RULES.md; reference from AUTO_MODE_STRATEGY + hooks strategy |
| H4 | Auto-mode "uncertain scope" is gate 10 (scope contradiction) only when SCOPE.md exists — **a vague task with no SCOPE.md sails through on the agent's own assumptions** | Add explicit "uncertain scope" hard-gate language to AUTO_MODE_STRATEGY |

### 7d. Places where BeQuite may lose context / skip steps / assume

- Long multi-domain runs lose mid-conversation facts after compaction → C1/C2 fixes + existing compaction-survival rule (CLAUDE.md rule 16)
- Auto mode with vague intent + missing upstream artifacts "runs the prerequisite command then continues" — correct behavior, but the prerequisite output is generated by the agent itself → assumption stacking. Mitigation: execution-contract step 3 (scope detection) requires marking assumption-derived scope in ASSUMPTIONS.md + uncertain-scope gate (H4)
- Memory writeback is specified everywhere now, but CHANGELOG `[Unreleased]` updates are still the most-skipped step in practice (AGENT_LOG review of alpha runs) → contract step 10 lists it explicitly; weasel-word Stop hook indirectly helps

### 7e. Skill size/quality findings

- **Too large:** `bequite-frontend-design-system` (master + 9 references + 3 examples) is intentionally large as a master skill — acceptable, but its references must stay progressive-disclosure (verified: references are separate files, loaded on demand) ✅
- **Largest single SKILL.md files:** presentation-builder (~385 lines), delegate-planner (~370) — at the upper bound; fine for now; `/bq-skill-audit` (new, this pass) institutionalizes monitoring
- **Too shallow:** none placeholder-thin; weakest depth is `bequite-problem-solver` (could use a worked example) — flag for first `/bq-skill-audit` run
- **Duplicate risk:** `context-engineer` ↔ `MEMORY_FIRST_BEHAVIOR.md` overlap (skill vs doc — acceptable: doc is strategy, skill is execution); `frontend-quality` ↔ `frontend-design-system` (resolved in alpha.17: quality = slop detection, design-system = coordinator) ✅
- **Merge candidates:** none this pass; job-finder/make-money share intake machinery but serve distinct user intents — keep separate

### 7f. Command overlap / docs disagreement

- No new overlaps since alpha.14 clutter review; `/bq-add-feature` remains the only deprecated alias
- **Docs-vs-reality drift found:** README/commands.md badge counts will be stale after this pass (44→46 commands, 24→26 skills) — update in step 12
- "Professional Expert Mode" appears in user requirements but **does not exist** in the repo — never scoped, never built. Decision: do NOT silently add a 5th operating mode; the capability ≈ `deep` + `bequite-anti-hallucination` + regulated doctrine. Proposed properly in GAME_CHANGER_FEATURE_DISCOVERY.md instead, with a recommended composition alias documented there
- `MULTI_MODEL_PLANNING_STRATEGY.md` still carries some v0.x phasing language in its body (header fixed in alpha.16) — minor; flagged for skill-audit backlog

### 7g. Outdated implementation spots

- `CLI_AUTHENTICATION_STRATEGY.md` is heavy-direction residue still in active `docs/architecture/` — flag to move to `docs/legacy/` (done this pass)
- Installer scripts predate writing/ dir — updated this pass

---

## 8. Already-covered request items (verified, no rework)

| Requested | Delivered in | Evidence |
|---|---|---|
| Hooks (destructive / secret / weasel) | alpha.18 | `.claude/hooks/*.{sh,ps1}` ×6 + README + 2 settings examples; ADR-005 Accepted |
| Context engineering core (PROJECT_DNA, WORKING_NOTES, compaction survival, session orientation, sub-agent isolation) | alpha.18 | `CONTEXT_ENGINEERING.md` + `bequite-context-engineer` |
| Harness + prompt quality authoring standard | alpha.18 | `HARNESS_AND_PROMPT_QUALITY.md` |
| Design Continuity Gate + DESIGN_DNA + visual QA + section-by-section loop | alpha.17 | 9-command wiring; `.bequite/design/`; master skill |
| Game-changer discovery report | alpha.18 + `bcd7511` | `docs/specs/GAME_CHANGER_FEATURES.md` + `CAPABILITY_FEATURE_IDEAS.md` |
| Anti-hallucination / evidence-over-claims / UNVERIFIED fork | alpha.18 | `bequite-anti-hallucination` skill + CLAUDE.md rule 16 |
| Mode definitions (when/when-not/scope/memory/research/verification/output/safety/examples) | alpha.12/15 | commands.md §Operating Modes + USING walkthroughs — re-verified complete for all 4 modes |
| Presentation builder capabilities (PPTX/HTML/both/variants/strict/creative/refs/notes/brand/motion/morph) | alpha.13 | command + skill + 9 templates — re-verified complete; only the consolidating strategy DOC was missing |

## 9. Final strengthening plan (this pass = v3.0.0-alpha.19 "Fable Strengthening Pass")

**New features (2):** Writing DNA (`/bq-writing-dna` + skill + 5 memory templates) · Skill Audit (`/bq-skill-audit` + skill + report seed)
**New strategy docs (6):** COMMAND_EXECUTION_CONTRACT · HARNESS_ENGINEERING_STRATEGY (index) · CONTEXT_ENGINEERING_STRATEGY (index + deltas) · PROMPT_ENGINEERING_STANDARD · FILE_RISK_CLASSIFICATION · PRESENTATION_BUILDER_STRATEGY
**New memory (4):** CONTEXT_SUMMARY.md · EVIDENCE_LOG.md · FILE_RISK_RULES.md · PROMPT_PATTERNS.md
**New plan:** GAME_CHANGER_FEATURE_DISCOVERY.md (decision tracker over the alpha.18 report; includes Professional Expert Mode proposal)
**Hardening:** AUTO_MODE_STRATEGY uncertain-scope gate + file-edit-risk gate reference
**Hygiene:** CLI_AUTHENTICATION_STRATEGY → legacy
**Docs:** README · commands.md · CLAUDE.md · /bequite · /bq-help · /bq-suggest · COMMAND_CATALOG · workflow-advisor · installer (writing templates + counts)
**Version:** alpha.18 → **alpha.19** (next sequential; user suggested alpha.20 assuming the report commit was a release — it wasn't versioned, so 19 is correct)
