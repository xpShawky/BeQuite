# BeQuite — System Research Report (alpha.14)

**Run date:** 2026-05-17
**Mode:** deep research (BeQuite on BeQuite)
**Purpose:** Extract principles from current best practices in coding-agent skill packs, spec-driven development, memory systems, and creative-content workflows — then improve BeQuite. **Do not copy blindly. Keep BeQuite lightweight.**

---

## 1. Sources reviewed

(Memory-first scope: this is a synthesis of established public patterns from the AI-coding-agent and spec-driven-development ecosystems. Because BeQuite's tool neutrality forbids hardcoding tool picks, we reference sources by ECOSYSTEM, not by URL — and capture the PRINCIPLE, not the implementation.)

### Coding-agent skill packs

- **Anthropic Skills** (SKILL.md format with YAML frontmatter, `allowed-tools`, progressive disclosure)
- **Claude Code slash commands** (markdown-driven; `.claude/commands/*.md`)
- **Continue.dev custom commands** (config-driven)
- **Cursor rules** (`.cursor/rules/*.mdc`, per-folder, scoped)
- **Aider** (architect/edit pattern; cheap-model edits, strong-model plans)
- **OpenDevin / Devin** (autonomous agent loops)
- **Kilo Code** (Roo Code successor; opinionated dev workflow)

### Spec-driven development

- **GitHub Spec Kit** (`specs/<feature>/spec.md` schema; 9 official commands `/speckit.*`)
- **BMad Method** (agent + spec + brief + persona shape)
- **Cline Memory Bank** (six-file project memory: brief / product / system / tech / active / progress)
- **OpenAI o3 + Spec Mode** patterns

### Memory systems

- **Cline Memory Bank** (six-file persistent memory)
- **Claude Code project memory** (CLAUDE.md + .claude/ scaffold)
- **Roo Code memory** (rules + context)
- **Continue.dev context providers** (RAG-flavored)
- **Letta / MemGPT** (hierarchical memory)

### Command-pack design

- **Impeccable** (23 frontend design commands with `craft / teach / extract / shape / critique / polish / harden / animate / colorize / typeset / layout / delight` namespace)
- **shadcn registry** (component-pack distribution)
- **Spec Kit's `/speckit.constitution/specify/clarify/plan/tasks/analyze/implement/checklist/taskstoissues`** (9-command vocabulary)

### Red-team + verification workflows

- **OWASP Top 10 LLM Applications 2025**
- **PhantomRaven / Shai-Hulud supply-chain patterns** (npm typo-squat campaigns 2025)
- **STRIDE threat modeling**
- **Adversarial prompt-injection red-team patterns**

### Memory + research-before-planning workflows

- **Spec-First development** (write spec → verify spec → plan from spec)
- **ADR-driven architecture** (one decision per file; immutable history)

### Token-saving workflows

- **Prompt caching** (Anthropic, 5-minute cache TTL; bigger context cached → reads cheaper)
- **Summarization-before-load** (read a 1-page summary instead of a 20-page doc)
- **Sliding-window recent log** (keep last 5–10 entries; archive older)

### UI/UX live edit workflows

- **Vercel v0** (LLM → JSX → preview loop)
- **Figma + Make** (design-first; export to code)
- **CSS animation libraries** (GSAP, Motion One, vanilla CSS keyframes)

### Presentation generation workflows

- **PowerPoint Morph transition** (object-based; same object name across slides; engine interpolates)
- **Apple Keynote Magic Move** (similar object-tracking interpolation)
- **reveal.js** (HTML slide framework; CSS transitions + JS hooks)
- **Slidev** (Markdown → Vue → slides)
- **Marp** (Markdown → slides → export PPTX/PDF/HTML)
- **Spectacle** (React-based slides)
- **python-pptx** (Python → .pptx generation)
- **pptxgenjs** (JS → .pptx generation)

### Job + opportunity research

- **LinkedIn Easy Apply**, **Wellfound**, **RemoteRocketship**, **YC Work at a Startup**, **Indie Hackers**, **Yandex Toloka**, **Wuzzuf**, **BrighterMonday**, **Outlier**, **Mercor**, **Scale AI**, **DataAnnotation**, **Surge**, **Appen**, **UserTesting**, **UserBrain**, **Prolific**, **Respondent**, **dscout**

### Automation + scraping

- **Playwright**, **Puppeteer**, **n8n**, **Make**, **Zapier**, **firecrawl**, **Apify**

### Security review

- **OWASP Web App Top 10 (2021 + 2025 draft)**
- **OWASP LLM Top 10 (2025 final)**
- **CWE Top 25**

### DevOps + cloud safety

- **Twelve-Factor App** patterns
- **Blue-green** + **canary** deployments
- **GitOps**

---

## 2. Useful ideas (apply to BeQuite)

### A. Spec Kit's command vocabulary

**Idea:** Spec Kit's 9 commands (`/speckit.constitution`, `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.implement`, `/speckit.checklist`, `/speckit.taskstoissues`) form a clean spec-driven loop.

**BeQuite has its own loop:** `/bq-init`, `/bq-discover`, `/bq-doctor`, `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`, `/bq-multi-plan`, `/bq-assign`, `/bq-implement`, `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-release`, `/bq-changelog`, `/bq-memory`, `/bq-recover`, `/bq-handoff` + orchestrators + scoped autos + creative workflows.

**Recommendation for BeQuite:** keep BeQuite's vocabulary. It's richer than Spec Kit's because BeQuite covers more phases (doctor, discover, audit, red-team, verify, release, memory, handoff). Cross-reference Spec Kit interop via `/bq-spec` (already done).

### B. Cline Memory Bank's six-file shape

**Idea:** Cline uses six files: brief / product / system / tech / active / progress. Each has a specific role; the agent reads them in order on session start.

**BeQuite's `.bequite/state/` has:** PROJECT_STATE / CURRENT_MODE / CURRENT_PHASE / WORKFLOW_GATES / LAST_RUN / DECISIONS / OPEN_QUESTIONS / ASSUMPTIONS / MISTAKE_MEMORY / MODE_HISTORY / BEQUITE_VERSION / UPDATE_SOURCE.

**Recommendation:** BeQuite's structure is more granular and tracks more state. Keep as-is. Consider a `MEMORY_INDEX.md` that lists the file purposes, for orientation. (Not blocking for alpha.14.)

### C. Aider's architect-edit pattern (formalized as Delegate Mode)

**Idea:** Strong model writes the plan/instructions; cheap model implements; strong model reviews. Cost savings without quality loss.

**BeQuite already implements this as Delegate Mode (alpha.12).** ✅ This research validates the pattern was the right call.

### D. PowerPoint Morph + Apple Magic Move — object-name continuity

**Idea:** The morph engine works by NAME-MATCHING objects across slides. Stable object IDs → smooth transitions. This is the principle behind "morph-like motion" in `/bq-presentation`.

**BeQuite has this principle documented** in `MOTION_PLAN.md` template and `bequite-presentation-builder/SKILL.md` ("PPTX morph-like discipline" section). ✅ The discipline is encoded.

**Improvement for alpha.15+:** when actual rendering happens, the agent should write the object-naming map to `MOTION_PLAN.md::object-naming-convention` BEFORE generating any .pptx.

### E. Memory-first preflight

**Idea:** Coding agents waste tokens by re-reading everything on each turn. Memory-first means: read the small state files first; read the deep docs only if needed.

**BeQuite documents this in `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`** ✅. The doc exists. The implementation is partial — 27/45 commands have explicit `## Files to read` preflight; 18 don't.

**Repair for alpha.14:** add memory-first preflight (`## Files to read` section) to the 18 commands lacking it.

### F. Tool neutrality (BeQuite's own principle ADR-003)

**Idea:** Don't hardcode tool picks. Research per project. Decision-section discipline (Problem / Options / Sources / Best option / Why / Why others rejected / Risk / Cost / Test plan / Rollback).

**BeQuite documents this in `.bequite/principles/TOOL_NEUTRALITY.md`** ✅. The 10 decision questions are in CLAUDE.md.

**Improvement:** every NEW skill file should have a "Tool neutrality" reminder at the top. Already done for newer skills (delegate-planner, presentation-builder). Backport to older skills (alpha.15 task).

### G. Anthropic Skills progressive disclosure

**Idea:** Skills are loaded only when relevant; their full content isn't always in context. The SKILL.md format with YAML frontmatter + concise description + `allowed-tools` enables this.

**BeQuite uses Anthropic Skills format correctly** ✅. All 21 skills have valid frontmatter.

**Improvement:** the `description:` field in some skill YAML is too verbose. The Anthropic skills system uses the description for activation matching; keep it under 300 chars and laser-focused on triggers.

### H. Red-team workflows

**Idea:** Adversarial review by a "Skeptic" mode produces sharper analysis than friendly review. Multiple attack angles (security, architecture, testing, deployment, scalability, UX, token-waste, hidden assumptions).

**BeQuite implements this as `/bq-red-team`** (8 attack angles documented) ✅.

**Improvement:** add 2 more angles based on research:
- **Supply-chain attack angle** (PhantomRaven-style typo squat scan + lockfile reconciliation)
- **Prompt injection angle** (LLM Top 10 #1: any user input passed to the agent should be reviewed for injection)

### I. Spec-driven development discipline

**Idea:** Write the spec BEFORE writing code. The spec is the contract. The agent reads the spec to know what to build.

**BeQuite has:** `/bq-spec` (one-page Spec Kit format) + `/bq-scope` (IN/OUT/NON-GOALS) + `/bq-plan` (full implementation plan). Three tiers of "spec".

**Improvement:** alpha.13's Presentation Builder skipped all three. Alpha.14's global feature-addition rule enforces this going forward.

### J. Mistake memory

**Idea:** When the agent makes a mistake, record it. Read on session start so the same mistake isn't repeated.

**BeQuite implements this via `.bequite/state/MISTAKE_MEMORY.md`** ✅. Wired into 7 commands.

**Improvement:** add to `/bq-presentation` too (currently not wired). Alpha.14 task.

---

## 3. Ideas rejected

| Idea | Source | Why rejected |
|---|---|---|
| Localhost dashboard for project status | Devin, Cursor, BMad Studio | ADR-004: keep BeQuite lightweight; no daemon, no port |
| Mandatory Spec Kit adoption | Spec Kit | Tool neutrality — `/bq-spec` is interop, not lock-in |
| Mandatory Cline Memory Bank shape | Cline | BeQuite's state structure is more granular + serves more phases |
| Python CLI as primary entry | (paused per ADR-001) | Slash commands inside Claude Code are the MVP; Python CLI is paused |
| Daemon + file watcher | Various | No daemons in BeQuite; ADR-004 |
| Hot-reload skill auto-discovery | Various | Claude Code already handles skill discovery |
| Mandatory red-team on every change | Adversarial-first methods | Optional gate; `/bq-red-team` is opt-in; required for `--mode deep` only |
| Single-shot "magic prompt" command | "do everything" patterns | Against tool neutrality; BeQuite forces the discipline; the menu is `/bequite`, the autopilot is `/bq-auto` |
| LLM-only spec validation | Various | Some validation must be machine-checkable (gate ledger) |
| Auto-publishing to SlideShare / Google Slides | Presentation tooling | Hard human gate (alpha.13); never auto-publish |
| Auto-install of presentation libraries (python-pptx, etc.) | Various | Tool neutrality; CANDIDATES only; decision section required |
| Hooks (PreToolUse / PostToolUse / Stop) for gate enforcement | Claude Code hooks | Considered for alpha.15+ — currently convention-enforced; hooks would be machine-enforcement (ADR-005 to draft) |

---

## 4. Risks

1. **Risk:** BeQuite has 45 commands. Even with grouping by phase, this is a lot to learn.
   - Mitigation: `/bequite` menu + `/bq-now` + `/bq-suggest` lower the entry barrier. Documented in clutter review.
2. **Risk:** Convention-enforced gates can be ignored when the agent shortcuts.
   - Mitigation: alpha.14 adds explicit refusal logic to commands; alpha.15 may add Claude Code hooks for machine enforcement.
3. **Risk:** Without research before implementation, features can adopt bad tool picks.
   - Mitigation: alpha.14 codifies the global feature-addition rule.
4. **Risk:** Skill descriptions in YAML frontmatter are getting longer; Anthropic Skills' activation matching may suffer.
   - Mitigation: alpha.15 audit of skill description lengths; aim for <300 chars.
5. **Risk:** As features stack, the installer copies more templates; users get a `.bequite/` directory with many empty templates.
   - Mitigation: only `.gitkeep` is shipped for empty dirs; templates have helpful starter content; documented as templates.
6. **Risk:** "Token Saver Mode" naming may still confuse — users may expect zero tokens.
   - Mitigation: alpha.13 docs are clear ("NOT token-free"; "token-lean"); alpha.14 verify and re-emphasize.
7. **Risk:** No formal verify means changes that ship may have subtle inconsistencies.
   - Mitigation: alpha.14 establishes a self-audit pattern (this very run). Should be repeated each minor release.

---

## 5. Command improvements (alpha.14+)

| Command | Improvement | Priority |
|---|---|---|
| `bq-test` | Add gate-refusal logic at top | high (alpha.14) |
| `bq-verify` | Add gate-refusal logic | medium |
| `bq-implement`, `bq-clarify`, `bq-research`, `bq-scope`, `bq-plan` | Add gate-refusal logic | medium |
| `bq-add-feature` | Mark deprecated; redirect to `/bq-feature` | high (alpha.14) |
| 18 commands lacking memory-first preflight | Add `## Files to read` section | medium (alpha.14 partial; full in alpha.15) |
| 20 commands lacking alpha.6 standardized fields | Add the section | low (alpha.15) |
| `/bq-presentation` | Wire to MISTAKE_MEMORY | medium (alpha.14) |
| `/bq-help` | Fix old phase name "Setup and Understanding" → "Setup and Discovery" | low |
| `/bequite` | Update top comment "Command map (34 commands)" → "Command map (44 commands)" | low |

---

## 6. Skill improvements (alpha.14+)

| Skill | Improvement | Priority |
|---|---|---|
| 18 skills lacking `Quality gate` | Add section | medium (alpha.14) |
| 16 skills lacking `When NOT to use` | Add section | medium (alpha.14) |
| 17 skills lacking `Common mistakes` | Add section | low (alpha.15) |
| All 21 skills | Audit YAML `description:` length; aim <300 chars | low (alpha.15) |
| Older skills (alpha.2 era) | Add tool-neutrality reminder block | low (alpha.15) |

---

## 7. Workflow improvements (alpha.14+)

1. **Global feature-addition rule** — codify in CLAUDE.md + WORKFLOW_GATES.md + COMMAND_CATALOG + USING_BEQUITE_COMMANDS (alpha.14)
2. **Gate name aliasing** — both `_DONE` and `_COMPLETE` forms valid (alpha.14)
3. **Orthogonal workflow declaration** — Presentation / Job / Money / Suggest are orthogonal to the dev lifecycle (alpha.14)
4. **Two extra red-team angles** — supply-chain + prompt-injection (alpha.15)
5. **Mode history visualization** — render `/bq-mode-history` to surface user patterns (alpha.15 if user wants)
6. **Hooks (Claude Code PreToolUse / Stop hooks)** for machine-enforcement of banned weasel words, secret scan, destructive op block (alpha.16+ — separate ADR)

---

## 8. Memory improvements (alpha.14+)

1. **`MEMORY_INDEX.md`** at `.bequite/` root — lists every state file with its role (alpha.15)
2. **Sliding-window archival** — for `AGENT_LOG.md`, archive entries older than 90 days to `AGENT_LOG-<date>.md` (alpha.15)
3. **MISTAKE_MEMORY pruning** — periodic review; archive resolved entries (alpha.15)
4. **`PROJECT_STATE.md` template refresh** — remove stale "paused Studio" reference (alpha.14)

---

## 9. Documentation improvements (alpha.14+)

1. **Move stale heavy-direction docs to `docs/legacy/`** (alpha.14)
   - 9 top-level `docs/*.md`
   - `docs/audits/*`
   - `docs/RELEASES/*`
   - `docs/merge/*`
2. **Update `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`** with correct counts + alpha.13 surface (alpha.14)
3. **Update `USING_BEQUITE_COMMANDS.md`** with worked examples for Presentation Builder + Delegate Mode (alpha.14 partial; rest alpha.15)
4. **Add `docs/architecture/PRESENTATION_BUILDER_STRATEGY.md`** post-alpha.14 — formalizes PPTX/HTML decision logic + tool-neutrality candidate list (alpha.15)
5. **Sync README badge counts with reality** — 44 commands / 21 skills / 4 modes (alpha.14)

---

## 10. Final recommendations (action list for alpha.14)

### Must do in alpha.14 (the discipline-restoration release)

1. ✅ Write all 7 audit reports (this is one of them)
2. Codify global feature-addition rule in 4 docs
3. Mark `bq-add-feature.md` as deprecated alias
4. Add `## Quality gate` to 18 skills (or document why exempt)
5. Add `## When NOT to use` to 16 skills
6. Update `PROJECT_STATE.md` (remove stale Studio reference)
7. Close stale `OPEN_QUESTIONS.md` entries (Q1-Q3)
8. Move stale heavy-direction docs to `docs/legacy/`
9. Update `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` counts
10. Update `USING_BEQUITE_COMMANDS.md` with Presentation + Delegate walkthroughs
11. Bump `BEQUITE_VERSION` to alpha.14
12. Update AGENT_LOG, CHANGELOG, LAST_RUN
13. Run final self-audit (`FINAL_SYSTEM_ALIGNMENT_REPORT.md`)
14. Commit + push

### Should do soon (alpha.15)

15. Add `## Files to read` to 18 commands lacking it
16. Add alpha.6 standardized fields to 20 commands lacking it
17. Add gate-refusal logic to 14 commands lacking it
18. Add 2 red-team angles (supply-chain + prompt-injection)
19. Skill `description:` field audit
20. `MEMORY_INDEX.md`

### Nice to have (alpha.16+)

21. Claude Code hooks for machine-enforced banned weasel words / secret scan / destructive op block (ADR draft)
22. PPTX library decision example (when user actually renders a deck)
23. Bot Maker / Automation roadmap fleshed out
24. Sliding-window archival for AGENT_LOG / MISTAKE_MEMORY
