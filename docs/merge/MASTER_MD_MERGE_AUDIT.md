# MASTER_MD_MERGE_AUDIT.md

> Merge audit reconciling `BeQuite_MASTER_PROJECT.md` (introduced 2026-05-10 mid-session, after v0.1.1 had been written and tagged) with the existing project plan ratified via ExitPlanMode.
>
> **Status:** Adopted (Ahmed authorised "merge anything useful and continue work" 2026-05-10).
>
> **Output sub-version:** v0.1.2 (this commit).

---

## 0. Context

Two sources of truth arrived in this session:

1. **Original brief** (`BEQUITE_BOOTSTRAP_BRIEF.md`, 545 lines) — Ahmed's first input. Framed BeQuite as a Skill + CLI + repo template. Used by the approved plan.
2. **Approved plan** (`.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`) — ratified via ExitPlanMode. Resolved four forks: engineer-first / skill-first / layered Constitution + Doctrines / full-power v1 with autonomous execution.
3. **Master file** (`BeQuite_MASTER_PROJECT.md`, 2858 lines) — introduced after v0.1.1 was already written + tagged. Substantially wider scope: prescribes a TypeScript pnpm + Turborepo monorepo with Next.js dashboard, NestJS API, Postgres + Prisma, Redis + BullMQ, Docker Compose, etc. Frames BeQuite as a full-stack SaaS product (with web UI), not just a Skill + CLI + template.

The two are not strictly contradictory but they describe different *implementations* of the same idea ("project harness for AI coding agents"). The master is more ambitious in surface area, less host-portable.

This audit is the senior-architect call on what to merge, what to keep current, and what to defer.

---

## 1. The strategic call: two layers, one brain

I am **not** discarding the v0.1.0 + v0.1.1 work to switch to the master's monorepo stack. Reasons:

- Ahmed's prior decisions (skill-first distribution; CLI as thin Python wrapper; Iron Laws + Doctrines layered Constitution) are honoured. Discarding them would break the contract under which v0.1.0 + v0.1.1 shipped.
- The master's monorepo stack is a 6+ month build. Ahmed's stated timeline + autonomous-execution authorisation align with the harness-first plan.
- The harness (Skill + CLI + template) is portable across 25+ hosts (Claude Code, Cursor, Codex, Cline, Kilo, Continue, Aider, Windsurf, …). A hosted SaaS reaches one website. The wedge is portability.

I am **also not** rejecting the master. Most of the master's additions are *complementary* to the harness, not replacements. The right call is **two layers, one brain**:

| Layer | Surface | Stack | Sub-versions | Relationship |
|---|---|---|---|---|
| **Layer 1 — Harness (current)** | SKILL.md + Python CLI + repo template | Markdown + Python 3.11+ + bash hooks | v0.1.0 → v1.0.0 | Source of truth. Writes `.bequite/`, `state/`, `evidence/`, `receipts/`. |
| **Layer 2 — Studio (master's stack)** | Next.js dashboard + NestJS API + Worker + Postgres | TypeScript pnpm + Turborepo | v2.0.0+ | Reads what Layer 1 writes. Adds visual phase board, project wizard, evidence viewer, recovery screen. |

Both layers share:
- The same Constitution (Iron Laws + Doctrines) at `.bequite/memory/constitution.md`.
- The same Memory Bank (six files) at `.bequite/memory/`.
- The same `state/` files (master pattern; adopted in v0.1.2).
- The same `evidence/` directory.
- The same `prompts/` directory.
- The same persona names (master's named roles + my Skeptic + my token-economist).
- The same slash command names (master's simpler names + my unique `/audit`, `/freshness`, `/auto`).
- The same Phase 0–7 lifecycle for BeQuite-managed projects.

Layer 2 v2.0.0 is a **view of Layer 1's filesystem state**, indexed into Postgres for searchability and rendered in Next.js. The CLI writes the truth; the dashboard displays it.

**This honours the master's ambition without abandoning the wedge.**

---

## 2. The merge ledger — every distinct master claim, classified

### Bucket A — **MASTER WINS, ADOPT IN v0.1.2**

Items that are clean wins for the harness; adopted now.

| # | Master claim | Where | Why it wins | How adopted in v0.1.2 |
|---|---|---|---|---|
| A1 | Three modes: Fast / Safe / Enterprise | §4 | Clearer than "Slow/Fast/Auto"; maps to project complexity tier (not execution speed). Names match how teams already think. | Constitution amendment v1.0.0 → v1.0.1 references modes. Doctrines declare which modes they support. Auto-mode (v0.10.0) reads mode from `state/project.yaml`. |
| A2 | Root `CLAUDE.md` + root `AGENTS.md` | §6, §11, §12 | Master's pattern matches industry convention. AGENTS.md is a Linux Foundation standard now. | Both written this commit; reference `.bequite/memory/constitution.md` + `state/recovery.md`. |
| A3 | `state/` files (project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json) | §10.2, §6 | Operational state. Lighter-weight than Memory Bank. Master's recovery prompt requires them. | Created this commit. Memory Bank stays as durable cross-session brain; state/ as current working state. |
| A4 | `prompts/` directory with master/discovery/research/stack/implementation/review/recovery prompts | §6, §10.4 | Reusable prompt packs separate from `.claude/commands/`. | Created this commit. Aligns with .bequite/memory/prompts/v<N>/ for versioned snapshots. |
| A5 | `evidence/<phase>/<task>/` filesystem pattern | §3.6, §10.3, §21 | Complementary to my receipts. Receipts = signed JSON chain (auditability); evidence = filesystem artifacts (test outputs, screenshots, logs). Both. | `evidence/` directory created this commit; receipts schema (v0.7.0) emits parallel artifacts. |
| A6 | Recovery prompt template | §25 | Copy-paste-able recovery for new sessions. Operational discipline win. | Adopted into `prompts/recovery_prompt.md` (this commit) and exposed via `/recover` and `bequite recover` (v0.4.1). |
| A7 | Persona names: product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist | §8 | More familiar than my (Researcher / Architect / ScrumMaster / Implementer / Reviewer / QA / TechWriter / FrontendDesign). Especially: **token-economist as first-class** is a cost-discipline win. | Adopted in v0.2.0 (skill orchestrator). Plus my Skeptic kept as #11 (adversarial twin distinct from reviewer). |
| A8 | Slash commands: `/discover`, `/research`, `/decide-stack`, `/plan`, `/implement`, `/review`, `/validate`, `/recover`, `/design-audit`, `/impeccable-craft`, `/evidence`, `/release` | §7 | Simpler than my Spec-Kit-extends + BeQuite-adds split. | Adopted in v0.4.0 (renamed). My unique commands kept: `/audit`, `/freshness`, `/auto`. |
| A9 | Provider adapter interface (`AiProvider` TypeScript interface) | §16.5 | Clean boundary for multi-model. Useful even in Python land — translate to a Pydantic `AiProvider` ABC. | Adopted in v0.5.0 (CLI thin wrapper). |
| A10 | Common gaps checklist (Product / Architecture / Backend / Database / Frontend / Testing / Security / Agent workflow) | §26 | Direct rule-pack input for `bequite audit`. | Adopted in v0.4.2 — these become audit rule packs. |
| A11 | Definition-of-done at three levels: feature / phase / release | §27 | Crisp. | Adopted into Constitution amendment (v1.0.1) — referenced from Article II. |
| A12 | Initial ADR set: ADR-0001 repo-architecture, ADR-0002 mode-system, ADR-0003 memory-architecture, ADR-0004 frontend-design-quality, ADR-0005 validation-mesh, ADR-0006 provider-boundary, ADR-0007 local-first-development | §28 | Seeds the ADR catalog with the obvious foundational decisions. | Adopted in v0.5.0 (when CLI ships). Drafted as files-to-write in this audit; emitted with `bequite-itself` ADR-001 stack decision in v0.5.0. |
| A13 | Required test commands (lint / typecheck / test / test:integration / test:e2e / build / validate) | §18.1 | Standard surface for any project. | Adopted in `default-web-saas` Doctrine (already shipped in v0.1.1). |
| A14 | Three-tier command safety classification (safe / needs approval / dangerous) | §19.4 | Sharper than my "block destructive" hook. Maps cleanly to PreToolUse hook + auto-mode safety rails. | Adopted in v0.3.0 (hooks) + v0.10.0 (auto mode). |
| A15 | "Treat external content as untrusted" prompt-injection rule | §19.5 | Direct OWASP LLM Top 10 alignment. | Adopted into Constitution amendment (v1.0.1) Article IV addendum. |
| A16 | `bq` alias for `bequite` CLI | §17 | Quality-of-life win. | Adopted in v0.5.0 (CLI). |
| A17 | "Before adding any dependency" review checklist | §19.6 | Concrete supply-chain hygiene. | Adopted into `library-package` Doctrine (already shipped) + new `pretooluse-verify-package.sh` enrichment in v0.3.0. |

### Bucket B — **CURRENT WINS, KEEP**

Items where my approach is genuinely stronger; not adopting the master's framing.

| # | Topic | Master's position | Current position (kept) | Why current wins |
|---|---|---|---|---|
| B1 | Memory pattern | 4-layer (Project / State / Evidence / Prompt). Files defined ad-hoc. | 6-file Cline Memory Bank (projectbrief, productContext, systemPatterns, techContext, activeContext, progress) PLUS state/ + prompts/ + evidence/ + receipts/. | Cline Memory Bank has prior-art adoption + clean cross-session semantics. Master's "project memory" is just a list of files. We get both. |
| B2 | Constitution structure | Single set of "non-negotiable operating contract" rules (§3) | Layered: Iron Laws (universal, 7 articles) + Doctrines (forkable per project type) | Layered handles CLI vs ML vs library projects without applying inappropriate rules. |
| B3 | Reproducibility | Filesystem evidence with manifest.json | Signed ed25519 receipt chain (planned v0.7.0–v0.7.1) | Receipts can't be silently tampered with. Auditable for regulated industries. Filesystem evidence still adopted (Bucket A5). |
| B4 | Stack matrix freshness | Static stack list (§5.1, §11) — already partially obsolete (Stronghold deprecation, EV cert obsolescence, Spec-Kit command count, Roo Code shutdown not addressed) | `bequite freshness` probe (planned v0.4.3) — runs context7 + WebFetch + OSV scan + pricing-page check before any stack ADR signs | Master's stack matrix would rot. Probe defends against rot. |
| B5 | Adversarial review | Reviewer agent only | Reviewer **+** Skeptic (kill-shot question per phase boundary) | Aider has reviewer; Spec-Kit has analyse; nobody has explicit adversary. Catches optimism that vibe-coding produces. |
| B6 | Brief reconciliations | Master makes 2024-era assumptions: Stronghold mandated, EV cert required, mentions Roo Code as living host, "126 packages" un-attributed, etc. | Plan §2 codified 10 surgical updates: Aider direction reversed, Stronghold deprecated, EV cert obsolete, Roo Code shutting down 2026-05-15, PhantomRaven attribution, Veracode "14/MVP" dropped, Clerk MAU updated, Vercel timeout, Supavisor, etc. | These are factual corrections. Adopting the master without them ships 2024 advice in 2026. |
| B7 | MENA / Arabic | No locale support | `mena-bilingual` Doctrine (v0.11.0) — Arabic + Egyptian dialect, RTL-by-default, Tajawal/Cairo/Readex Pro fonts, bilingual Researcher | Single most differentiated competitive feature. No coding agent ships Arabic-first. |
| B8 | Vibe-to-handoff wedge | Treats BeQuite as engineer-only | Engineer-first v1 with vibe-handoff seeded into artifact discipline; Studio v2.0.0+ becomes the vibe-coder UI on top | Reaches the Lovable/v0/Bolt audience the original brief explicitly targeted. |
| B9 | Cost ceiling | "Token economist" as a persona only (§8.10) | Token economist persona **+** hard `max-cost-usd` ceiling enforced by Stop hook + cost roll-up via receipts (v0.8.0) | Persona without enforcement is theatre. Hooks make it real. |
| B10 | Project lifecycle | Phase 0–7 (Foundation → Core → DB+API → Web → Agent files → Validation mesh → Research engine → Release) — describes building BeQuite-itself | P0–P7 (Research → Stack → Plan → Phases → Tasks → Implement → Verify → Handoff) — describes lifecycle of any BeQuite-managed project | These are different things. Master's Phase 0–7 = how-to-build-BeQuite. My P0–P7 = how-BeQuite-runs-projects. **Both kept**, with naming clarified. |
| B11 | Audience flag | Implicit (master is for engineers / agency operators) | Explicit `audience = engineer | vibe-handoff` in `bequite.config.toml` | Allows the v2 vibe surface to drive the same harness without rewriting v1. |

### Bucket C — **MERGE BOTH, BOTH USEFUL**

Items where master and current are complementary; both adopted.

| # | Topic | Master | Current | Merged |
|---|---|---|---|---|
| C1 | Documentation directory | `docs/PROJECT_BRIEF.md`, `docs/PRODUCT_REQUIREMENTS.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md`, etc. | `.bequite/memory/projectbrief.md`, `.bequite/memory/systemPatterns.md`, etc. | `docs/` becomes the human-facing presentation layer (READMEs, architecture, runbooks); `.bequite/memory/` is the agent-facing durable brain. `docs/architecture/SYSTEM_OVERVIEW.md` cross-references `.bequite/memory/systemPatterns.md`. Same content, two views. |
| C2 | Slash commands | Master's 12 (§7) | Mine: 9 spec-kit-extends + 9 bequite-adds + audit + freshness + auto = ~21 | Adopt master's 12 names; my unique extras (`/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`) layered on top. Total: ~19 commands. |
| C3 | Subagents | Master's 10 named roles | Mine: 9 personas (incl. Skeptic) | Adopt master's 10 + add my Skeptic + my FrontendDesign (Impeccable-loaded). Total: 12 personas. |
| C4 | Phase roadmap (BeQuite-itself) | Phase 0 → Phase 7 (master §23) | v0.1.0 → v1.0.0 (15 sub-versions, my plan §4) | Map: master's Phase 0 ≈ my v0.1.0–v0.1.x; Phase 1 ≈ v0.2.0–v0.5.0; Phase 2 ≈ deferred to v2.0.0 (Studio); Phase 3 ≈ deferred to v2.0.0; Phase 4 ≈ v0.4.0–v0.4.1, v0.12.0; Phase 5 ≈ v0.6.0; Phase 6 ≈ v0.10.0; Phase 7 ≈ v0.15.0. Both kept; my sub-version granularity preserved. |
| C5 | Evidence vs receipts | Filesystem evidence (master §21) | Signed JSON receipts (mine, v0.7.x) | Both. Evidence = artifacts of validation runs (test outputs, screenshots, logs). Receipts = cryptographic proof of model + prompt + input + output. Co-exist. |
| C6 | Validation surface | Master's `pnpm lint / typecheck / test / build / validate` (§18.1) | Mine: Playwright walks + smoke + secret-scan + audit + freshness + receipts | Master's set = the universal CI gate; mine = the project-specific gates. `bequite verify` runs both. |
| C7 | Provider adapter interface | TypeScript `AiProvider` interface (master §16.5) | My `routing.json` + `skill_loader.py` Claude API caller | Both. Interface defined as Pydantic `AiProvider` ABC in `cli/bequite/providers/__init__.py` (v0.5.0); routing.json maps phase + persona → provider. |

### Bucket D — **MASTER'S SCOPE, DEFERRED TO v2.0.0 (Studio)**

Items that require the full TypeScript monorepo stack. Layer 2.

| # | Master claim | Where | Deferred to |
|---|---|---|---|
| D1 | pnpm + Turborepo monorepo | §5.1, §6 | v2.0.0 (Studio bootstrap) |
| D2 | Next.js web dashboard | §5.1, §15 | v2.0.0 |
| D3 | NestJS or Fastify API | §5.1, §16 | v2.0.0 |
| D4 | Node worker process | §5.1 | v2.0.0 |
| D5 | PostgreSQL + Prisma + migrations + seeds | §5.1, §14 | v2.0.0 (DB indexes filesystem state) |
| D6 | Redis + BullMQ | §5.1 | v2.0.0 |
| D7 | Docker Compose | §5.1, §6 | v2.0.0 |
| D8 | Required UI screens (project wizard, phase board, task detail, evidence viewer, recovery screen, settings, skills, model routing, design audit) | §15 | v2.0.0 (each is a major sub-version inside v2.x) |
| D9 | Storybook | §5.1 | v2.0.0 |
| D10 | k6 load tests | §5.1, §18.7 | v2.0.0 |
| D11 | OpenTelemetry traces | §5.1 | v2.0.0 |
| D12 | API modules (Auth, Users, Projects, Discovery, Research, Decisions, Phases, Tasks, Evidence, Prompts, Skills, Runs, Recovery, Settings) | §16.1 | v2.0.0 |
| D13 | Role permissions matrix (owner/admin/builder/reviewer/viewer) | §19.3 | v2.0.0 (Studio auth) |

A separate `docs/STUDIO_PLAN.md` will outline v2.0.0+ work after v1.0.0 ships.

### Bucket E — **OPEN ITEMS REQUIRING AHMED'S INPUT**

Decisions I cannot make unilaterally; flagged for Ahmed.

| # | Decision | My current default | When it blocks |
|---|---|---|---|
| E1 | GitHub org / repo name | `xpShawky/BeQuite` | Before first remote push (no remote configured yet — non-blocking) |
| E2 | PyPI package name + ownership | `bequite` (assume Ahmed creates) | v0.5.0 release (CLI ships) |
| E3 | Studio (v2.0.0+) timing — start after v1.0.0 ships, or immediately as parallel track? | After v1.0.0 ships | v1.0.0 release |
| E4 | Telemetry policy — opt-in only? Receipt-only (no code/prompts)? Off entirely? | Off entirely until ADR-002 lands; receipts are local-only | v0.7.0 (receipts ship) |
| E5 | Doctrine distribution — community Doctrines via separate `bequite-doctrines` GitHub org, or in main repo `skill/doctrines/community/`? | Separate org for scale; main repo for shipped defaults | v0.12.0 |
| E6 | MENA bilingual Researcher seeds — which X/Twitter accounts and Telegram channels seed the bilingual Researcher? | Empty seed list; Ahmed adds | v0.11.0 |
| E7 | Codex 5.5 review mode — invoke Codex as review-only after Claude Code primary, or fully alternate? | Review-only (cheaper, less divergence) | v0.8.0 (multi-model routing) |

None block v0.1.2 work. Will surface again at the relevant sub-version.

---

## 3. What changes in v0.1.2 (this commit)

**Files added (this commit):**

- `docs/merge/MASTER_MD_MERGE_AUDIT.md` (this file)
- `CLAUDE.md` (root) — adapted from master §11
- `AGENTS.md` (root) — adapted from master §12
- `state/project.yaml`
- `state/current_phase.md`
- `state/recovery.md`
- `state/task_index.json`
- `state/decision_index.json`
- `state/evidence_index.json`
- `prompts/master_prompt.md`
- `prompts/discovery_prompt.md`
- `prompts/research_prompt.md`
- `prompts/stack_decision_prompt.md`
- `prompts/implementation_prompt.md`
- `prompts/review_prompt.md`
- `prompts/recovery_prompt.md`
- `evidence/README.md`
- `BeQuite_MASTER_PROJECT.md` (now tracked — it's the source artifact for this audit)

**Files amended (this commit):**

- `skill/templates/constitution.md.tpl` — bumps to v1.0.1 — adds: Modes section (Fast/Safe/Enterprise), command-safety classification (master §19.4), prompt-injection rule (master §19.5), three-level definition-of-done (master §27), reference to `state/` files for `SessionStart` reads.
- `.bequite/memory/constitution.md` — same amendment applied to BeQuite-itself's Constitution.
- `README.md` — adds two-layer architecture section + master file reference.
- `CHANGELOG.md` — adds v0.1.1 + v0.1.2 entries.
- `.bequite/memory/activeContext.md` — current state updated.
- `.bequite/memory/progress.md` — evolution log updated with the merge.

**Files NOT touched (preserved):**

- All eight Doctrines under `skill/doctrines/` (v0.1.1 work).
- All seven `skill/templates/*.md.tpl` (v0.1.0 work).
- `template/.bequite/memory/*` (v0.1.0 work).
- The original `BEQUITE_BOOTSTRAP_BRIEF.md` (history).
- The plan + brief snapshots in `.bequite/memory/prompts/v1/` (history).

---

## 4. What this audit does NOT do

- It does not start v2.0.0 (Studio) work. That's a separate plan after v1.0.0 ships.
- It does not delete, rewrite, or invalidate any v0.1.0 / v0.1.1 work.
- It does not change Ahmed's four ratified fork answers (engineer-first / skill-first / layered Constitution / full-power v1).
- It does not commit to PyPI, GitHub remote, or any one-way-door action.

## 5. Resumption plan after v0.1.2

After this commit, v0.2.0 (Skill orchestrator) resumes per the original plan, with the merged additions baked in:

- Personas use master's named roles + Skeptic + token-economist (12 total).
- Slash commands use master's 12 names + my unique extras (≈19 total).
- Skill orchestrator reads from `state/` (master pattern) and `.bequite/memory/` (Cline pattern); both are sources, no conflict.
- Constitution v1.0.1 (post-amendment) is the new ratified rules; the v1.0.0 → v1.0.1 diff is recorded as ADR-008 (drafted in v0.5.0).

Sub-version granularity stays as planned (v0.2.0 → v0.15.0 → v1.0.0). v2.0.0+ Studio work begins only after v1.0.0 ships and Ahmed authorises.

---

## Appendix A — Verbatim master sections marked for direct adoption

For traceability, the following master sections were adopted **verbatim or near-verbatim**:

- §3.6 "Never say done without evidence" — reflected in Constitution Article II
- §3.7 "Never restart the whole project to fix one bug" — reflected in Constitution amendment v1.0.1
- §3.8 "Never lose context" — reflected in Constitution Article III + new state/ files
- §11 CLAUDE.md template body — adapted to BeQuite's actual paths
- §12 AGENTS.md template body — adapted to BeQuite's actual commands
- §19.4 command-safety three-tier classification — adopted in hooks (v0.3.0)
- §19.5 prompt-injection rule — adopted in Constitution amendment v1.0.1
- §25 recovery prompt template — adopted at `prompts/recovery_prompt.md`
- §27 definition-of-done three levels — adopted in Constitution amendment v1.0.1

## Appendix B — Items in master with no direct counterpart yet (future-track)

- ResearchSource authority levels (master §14.3) — useful schema for v0.4.1 `research.md` command output.
- Run states (`queued/running/succeeded/failed/cancelled/needs_review`) (master §16.4) — useful for v0.10.0 auto-mode state machine.
- Branch protection guidance (master §20.4) — adopted into `library-package` Doctrine (already shipped).
- Load test scenarios (master §18.7) — adopted into `default-web-saas` Doctrine for downstream projects.
- Visual checks per UI feature (master §18.5) — adopted into `default-web-saas` Doctrine.

## Appendix C — Token-saving rationale

The merge is shaped to minimise token waste:

- No mass rewriting of v0.1.0 / v0.1.1 (8000+ lines preserved).
- Constitution amendment is a patch bump (v1.0.0 → v1.0.1), not a rewrite.
- New files in v0.1.2 are concise (state/ files are < 200 lines combined; prompts are < 100 lines each).
- Bucket-D items (Studio) are a future plan, not present-day code, so no monorepo bootstrap drag.

Total v0.1.2 cost: ~25 new files, 6 amended files, 1 commit. Estimated diff size: ~3000 lines of new content + ~200 lines of amendments. Well within Article III + the cost-ceiling discipline.
