# BeQuite v1.0.0 — Full-Power Build Plan (autonomous-execution branch)

> Final plan after Ahmed's four answers. Scope: ship full BeQuite v1.0.0 with every feature in the brief, broken into 15 micro-versions (v0.1.0 → v1.0.0), each with detailed tasks and acceptance criteria. Includes a one-click `bequite auto` mode. After `ExitPlanMode`, I will execute these phases autonomously per the Memory Bank discipline (Article III), pausing only at the safety-rail boundaries defined in §7.

---

## 1. Context

Ahmed (xpShawky) wants BeQuite shipped at full power on day one — every artifact, every phase, every gate from `BEQUITE_BOOTSTRAP_BRIEF.md`, plus the additions surfaced in research (audit, freshness, Skeptic, MENA, vibe-to-handoff). He has authorized me to drive execution autonomously through v1.0.0 with phase-by-phase commits and clear safety rails. This document is both my marching orders and Ahmed's contract for what "v1.0.0 done" means.

This plan resolves the four forks Ahmed answered:

- **Audience:** engineer-first v1 with vibe-to-handoff artifact discipline so v2 can drive the same brain from a vibe-coder UI.
- **Distribution:** SKILL.md is the source of truth. CLI is a thin Python wrapper that loads the skill out-of-host via Claude API for non-Claude-Code hosts.
- **Constitution:** layered. Six "Iron Laws" + forkable "Doctrines." Impeccable bundled as the default Doctrine for frontend projects (pinned snapshot, attributed to Paul Bakaus).
- **Scope:** **full v1 from day 1.** Detailed sub-versions. One-click autonomous mode. I drive.

---

## 2. Brief reconciliations (apply once, in v0.1.0)

The brief is structurally right. Ten facts have rotted. Apply these surgical fixes when writing the Constitution and templates so we don't ship 2024 advice in 2026:

| In the brief | What it should say |
|---|---|
| Aider architect: "cheap writes, frontier reviews" | Aider architect: **frontier reasoner plans, cheap editor emits diffs.** Cite the cost-savings story for the right reason. |
| Tauri Stronghold for license storage | **OS keychain plugins** (`tauri-plugin-keyring`); Stronghold is deprecated and removed in Tauri v3. |
| Windows: OV/EV cert + AKV + `relic` | OV cert + **AzureSignTool (vcsjones)**; EV no longer gives SmartScreen reputation boost (MS removed EV-specific OIDs Aug 2024). Note AKV cert validity capped at 1 year since Feb 2026. |
| macOS: `altool` for notarization | `xcrun notarytool submit` (replaced altool in Xcode 13+). |
| Spec-Kit ships 16 commands | Spec-Kit ships 9 commands today (`/speckit.*`); BeQuite **extends** with 7 (`init, research, stack, phases, verify, review, handoff, resume, doctor`) plus 2 of our own (`audit, freshness`). Frame as extension, not replacement. |
| Roo Code as supported host | **Roo Code is shutting down May 15, 2026.** Replace with Kilo Code in the host list. |
| shadcn registry MCP (third-party) | Built into shadcn CLI v3+; use the official `shadcn registry:build` + MCP. |
| Clerk free tier is small | Clerk free tier is **50k MAU** in 2026; Pro from $20/mo. |
| Vercel "300s function cap" | Hobby hard 300s. **Pro/Enterprise default 300s, configurable to 800s.** |
| PgBouncer transaction-mode | "PgBouncer (or **Supavisor** on Supabase)." |
| "126 malicious npm packages" | Cite the **PhantomRaven** campaign (Koi Security, Aug–Oct 2025) by name. Mention Shai-Hulud (~700 pkg) as broader 2025 supply-chain pattern. |
| Veracode 2025: ~14 vulns/MVP | **Drop the "~14/MVP" number** (not in report). Keep the 45% OWASP figure (verified). |
| OWASP Top-10 (Article V, ambiguous) | Reference both **OWASP Top 10 for LLM Applications 2025** (final) and OWASP Web App Top 10 (2021 stable / 2025 draft). |
| Impeccable: 19k stars, 18 commands | ~26.6k stars, 23 commands. Update count; namespace `craft`/`extract` correctly; include `teach, document, shape, onboard, live`. |

These corrections are baked into Constitution v1.0.0 and the stack-matrix template authored in v0.1.0.

---

## 3. Architecture (the file tree v1.0.0 ships with)

```
bequite/                              ← the BeQuite repo
├── skill/                            ← THE source of truth (all hosts read this)
│   ├── SKILL.md                      ← orchestrator persona, 7-phase router, mode selector
│   ├── agents/
│   │   ├── researcher.md             ← P0
│   │   ├── architect.md              ← P1, P2
│   │   ├── scrum-master.md           ← P3, P4
│   │   ├── implementer.md            ← P5
│   │   ├── reviewer.md               ← P5 review
│   │   ├── skeptic.md                ← adversarial twin (every phase boundary)
│   │   ├── qa.md                     ← P6
│   │   ├── tech-writer.md            ← P7
│   │   └── frontend-design.md        ← Impeccable-loaded sub-persona
│   ├── commands/
│   │   ├── speckit-extends/          ← 9 commands wrapping Spec-Kit primitives
│   │   │   ├── constitution.md
│   │   │   ├── specify.md
│   │   │   ├── clarify.md
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── analyze.md
│   │   │   ├── implement.md
│   │   │   ├── checklist.md
│   │   │   └── taskstoissues.md
│   │   ├── bequite-adds/             ← 9 commands BeQuite contributes
│   │   │   ├── init.md
│   │   │   ├── research.md
│   │   │   ├── stack.md
│   │   │   ├── phases.md
│   │   │   ├── verify.md
│   │   │   ├── review.md
│   │   │   ├── handoff.md
│   │   │   ├── resume.md
│   │   │   └── doctor.md
│   │   ├── audit.md                  ← Constitution drift detector
│   │   ├── freshness.md              ← Knowledge probe
│   │   ├── auto.md                   ← One-click autonomous mode
│   │   ├── memory.md                 ← Memory-Bank ops
│   │   ├── snapshot.md               ← Versioned prompt/spec snapshots
│   │   ├── cost.md                   ← Token + dollar receipts
│   │   └── skill-install.md          ← Install BeQuite into a host
│   ├── hooks/
│   │   ├── pretooluse-secret-scan.sh
│   │   ├── pretooluse-block-destructive.sh
│   │   ├── pretooluse-verify-package.sh   ← PhantomRaven defense
│   │   ├── posttooluse-format.sh
│   │   ├── posttooluse-lint.sh
│   │   ├── stop-verify-before-done.sh
│   │   ├── sessionstart-load-memory.sh
│   │   └── sessionstart-cost-budget.sh
│   ├── templates/
│   │   ├── constitution.md.tpl
│   │   ├── doctrine.md.tpl
│   │   ├── adr.md.tpl
│   │   ├── spec.md.tpl
│   │   ├── plan.md.tpl
│   │   ├── tasks.md.tpl
│   │   ├── phases.md.tpl
│   │   ├── research.md.tpl
│   │   ├── handoff.md.tpl
│   │   ├── security.md.tpl
│   │   └── tokens.css.tpl
│   ├── doctrines/                    ← forkable industry/profile doctrines
│   │   ├── default-web-saas.md       ← shipped default
│   │   ├── cli-tool.md
│   │   ├── ml-pipeline.md
│   │   ├── desktop-tauri.md
│   │   ├── library-package.md
│   │   ├── mena-bilingual.md         ← Arabic + RTL (v0.11.0)
│   │   ├── fintech-pci.md
│   │   ├── healthcare-hipaa.md
│   │   └── gov-fedramp.md
│   ├── references/
│   │   ├── stack-matrix.md           ← scale-tier → stack mapping (post-corrections)
│   │   ├── frontend-stack.md
│   │   ├── backend-stack.md
│   │   ├── database-stack.md
│   │   ├── auth-stack.md
│   │   ├── hosting-stack.md
│   │   ├── desktop-stack.md
│   │   ├── security-checklist.md
│   │   ├── verification-checklist.md
│   │   └── package-allowlist.md      ← seeds the freshness probe
│   ├── skills-bundled/               ← vendored peer skills
│   │   └── impeccable/               ← pinned snapshot of pbakaus/impeccable
│   └── routing.json                  ← multi-model routing matrix
├── cli/
│   ├── pyproject.toml                ← hatchling, distributable via uvx/pipx
│   ├── README.md
│   └── bequite/
│       ├── __init__.py
│       ├── __main__.py
│       ├── commands.py               ← dispatches each /bequite.X to the skill
│       ├── skill_loader.py           ← loads SKILL.md + agents into a Claude API call
│       ├── auto.py                   ← `bequite auto` orchestrator
│       ├── config.py                 ← reads .bequite/bequite.config.toml
│       ├── receipts.py               ← reproducibility receipts
│       ├── freshness.py              ← package + tier + CVE probe
│       ├── audit.py                  ← Constitution drift scan
│       └── hooks.py                  ← shells out to skill/hooks/
├── template/                         ← `gh repo create --template` source
│   ├── .bequite/
│   │   ├── memory/
│   │   │   ├── constitution.md       ← copied from skill/templates
│   │   │   ├── projectbrief.md
│   │   │   ├── productContext.md
│   │   │   ├── systemPatterns.md
│   │   │   ├── techContext.md
│   │   │   ├── activeContext.md
│   │   │   ├── progress.md
│   │   │   ├── decisions/
│   │   │   ├── prompts/
│   │   │   └── logs/
│   │   ├── skills/                   ← symlinks/copies of bundled skills
│   │   ├── agents/
│   │   ├── commands/
│   │   ├── templates/
│   │   ├── scripts/
│   │   ├── hooks/
│   │   ├── receipts/                 ← signed JSON receipts per phase
│   │   └── bequite.config.toml
│   ├── specs/
│   ├── apps/
│   ├── packages/
│   ├── tests/
│   ├── infra/
│   ├── .claude/
│   │   ├── skills/                   ← symlinks
│   │   ├── agents/
│   │   ├── commands/
│   │   └── settings.json             ← hooks wired
│   ├── .cursor/rules/
│   ├── .codex/
│   ├── .gemini/
│   ├── .windsurf/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── README.md
│   ├── HANDOFF.md
│   ├── SECURITY.md
│   └── LICENSE
├── examples/
│   ├── 01-bookings-saas/             ← worked example (web SaaS doctrine)
│   ├── 02-ai-tool-wrapper/           ← worked example (CLI tool doctrine)
│   └── 03-tauri-note-app/            ← worked example (desktop doctrine)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│       ├── seven-phase-walk.test.ts
│       ├── auto-mode.test.ts
│       └── doctrine-loading.test.ts
├── docs/
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── HOW-IT-WORKS.md
│   ├── DOCTRINE-AUTHORING.md
│   ├── HOSTS.md                      ← per-host install: Claude Code, Cursor, Codex, etc.
│   ├── AUTONOMOUS-MODE.md
│   └── SECURITY.md
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── release.yml
│   │   └── examples-e2e.yml
│   └── ISSUE_TEMPLATE/
├── CHANGELOG.md
├── LICENSE
└── README.md
```

**Personas (the agents/ folder):**

| Agent | Role | Phase(s) | Default model |
|---|---|---|---|
| Researcher | Phase 0 — find prior art, evidence | P0 | Opus 4.7 (high) |
| Architect | Phase 1–2 — stack ADR, plan, contracts | P1, P2 | Opus 4.7 (high) |
| ScrumMaster | Phase 3–4 — phase + atomic-task breakdown | P3, P4 | Sonnet 4.5 |
| Implementer | Phase 5 — code | P5 | Sonnet 4.5 |
| Reviewer | Phase 5 — diff review | P5 | Opus 4.7 (xhigh) |
| **Skeptic** | Adversarial — every phase boundary | P0–P7 | Opus 4.7 (xhigh) |
| QA | Phase 6 — Playwright walks, smoke tests | P6 | Sonnet 4.5 + Playwright MCP |
| TechWriter | Phase 7 — HANDOFF | P7 | Haiku 4.5 |
| FrontendDesign | Sub-persona, loaded with Impeccable | P5 (UI) | Sonnet 4.5 |

---

## 4. Sub-version roadmap (v0.1.0 → v1.0.0)

Each sub-version is an atomic, committable unit. Each ends with a tagged release on the BeQuite repo. Acceptance is binary: tests pass or the sub-version doesn't ship. Tasks marked `[parallel]` can run concurrently within a sub-version; everything else is sequential within its sub-version.

### v0.1.0 — Foundation & Constitution

**Goal:** the `.bequite/` tree, Constitution v1.0.0, Memory Bank scaffolding. Repo initialised, license, README skeleton.

**Tasks:**
1. Create the BeQuite repo skeleton (root `README.md`, `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`).
2. Author `skill/templates/constitution.md.tpl` — Iron Laws v1.0.0:
   - Article I — Specification supremacy
   - Article II — Verification before completion
   - Article III — Memory discipline
   - Article IV — Security & destruction discipline
   - Article V — Scale honesty
   - Article VI — Honest reporting
   - Article VII — Hallucination defense
   - Doctrines reference (`@doctrines/<active>.md` block)
3. Author `skill/templates/doctrine.md.tpl` — Doctrine schema (frontmatter: `name, applies_to, version, supersedes`).
4. Author six Memory-Bank templates (`projectbrief.md.tpl`, `productContext.md.tpl`, `systemPatterns.md.tpl`, `techContext.md.tpl`, `activeContext.md.tpl`, `progress.md.tpl`).
5. Author `skill/templates/adr.md.tpl` (semver-versioned ADR with status field: proposed/accepted/superseded).
6. Author `template/.bequite/memory/` instances of the six files for a fresh project.
7. Wire root README with the BeQuite vision pitch + 90-second elevator.

**Acceptance:** `cat skill/templates/constitution.md.tpl | grep "Article I"` returns the expected line; `tree template/.bequite/` shows the full memory tree; CI passes structural lint.

**Tag:** `v0.1.0`.

### v0.1.1 — Doctrines pack

**Goal:** ship the default doctrines that drive Constitution behaviour per project type.

**Tasks:** [parallel]
1. `doctrines/default-web-saas.md` — UI rules (no AI-default Inter without recorded reason; no purple-blue gradients; no nested cards; no gray-on-color text), shadcn/ui order, tokens.css required, axe-core gate, Playwright walk required.
2. `doctrines/cli-tool.md` — no UI doctrine; man-page generation; semver discipline; bash completions.
3. `doctrines/ml-pipeline.md` — reproducible training, dataset versioning, experiment tracking, GPU-cost discipline.
4. `doctrines/desktop-tauri.md` — Tauri v2 + OS keychain (NOT Stronghold) + Apple notarytool + AzureSignTool + Keygen for licensing.
5. `doctrines/library-package.md` — public API freezing, semver-strict, changelog discipline, no telemetry without opt-in.
6. `doctrines/fintech-pci.md` — PCI DSS controls, audit log retention, cardholder data segregation.
7. `doctrines/healthcare-hipaa.md` — PHI handling, BAA list, audit trail.
8. `doctrines/gov-fedramp.md` — FedRAMP control families, FIPS-validated crypto.

**Acceptance:** all doctrines load via `bequite memory show doctrine <name>`; doctrine schema validation passes.

**Tag:** `v0.1.1`.

### v0.2.0 — Skill orchestrator (the brain)

**Goal:** SKILL.md exists, the 7-phase router works, every persona loads on demand.

**Tasks:**
1. Author `skill/SKILL.md` — frontmatter (name `bequite`, description ≤1024 chars, allowed-tools list per Anthropic Skills schema). Body = orchestrator persona + 7-phase router + mode selector (Slow / Fast / Auto).
2. Author each persona file in `skill/agents/`:
   - `researcher.md`, `architect.md`, `scrum-master.md`, `implementer.md`, `reviewer.md`, `skeptic.md`, `qa.md`, `tech-writer.md`, `frontend-design.md`
3. Author `skill/routing.json` — default routing matrix (post brief reconciliation #3).
4. Author `bequite.config.toml.tpl` — mode, model routing overrides, scale tier, providers, cost ceiling, audience flag (engineer/vibe-handoff).
5. Wire skill into `template/.claude/skills/bequite/` (symlink target for fresh projects).

**Acceptance:** Claude Code loads `skill/SKILL.md`; `/bequite` lists the available 7-phase commands; routing.json validates against schema.

**Tag:** `v0.2.0`.

### v0.3.0 — Hooks (deterministic gates)

**Goal:** every hook in §13 of the brief works, blocks bad behaviour, and is host-portable.

**Tasks:** [some parallel]
1. `pretooluse-secret-scan.sh` — regex for `(api|secret|password|token|jwt)[-_]?(key|token)?` + AWS access patterns. Exit 2 on match.
2. `pretooluse-block-destructive.sh` — block `rm -rf` outside `/tmp`, `terraform destroy`, `DROP DATABASE`, `git push -f` to protected branches, `:force-with-lease` to main.
3. `pretooluse-verify-package.sh` — diff `package.json`/`pyproject.toml`/`Cargo.toml`; for each new import run `npm view <pkg>` / `pip index versions <pkg>` / `cargo search <pkg>` + cross-check against `references/package-allowlist.md`. Exit 2 if package missing or in known-bad list.
4. `posttooluse-format.sh` — biome / prettier / black / ruff / clippy by language detection.
5. `posttooluse-lint.sh` — eslint / ruff / clippy. Warn-only.
6. `stop-verify-before-done.sh` — re-runs failing tests; if any task incomplete or completion message contains banned words (`should/probably/seems to/appears to/I think it works`), exit 2 with reason.
7. `sessionstart-load-memory.sh` — reads all six Memory Bank files + active ADRs into context.
8. `sessionstart-cost-budget.sh` — loads cost ceiling from config.
9. Wire into `template/.claude/settings.json` and `template/.bequite/hooks/` shell-script copies for non-Claude hosts.

**Acceptance:** test fixtures in `tests/integration/hooks/` verify each hook returns the expected exit code on planted violations. CI runs the suite.

**Tag:** `v0.3.0`.

### v0.4.0 — Slash commands wave 1: Spec-Kit-extends (9 commands)

**Goal:** commands that wrap Spec-Kit primitives. Each is one Markdown file with the command's persona prompt + tools list.

**Tasks:** [parallel]
1. `constitution.md` — generate / amend `.bequite/memory/constitution.md`.
2. `specify.md` — generate `specs/<feature>/spec.md` (technology-agnostic).
3. `clarify.md` — Skeptic-driven clarifying questions.
4. `plan.md` — generate `specs/<feature>/plan.md` (implementation, stack-bound).
5. `tasks.md` — atomic task list (≤5 min each), dependency-ordered.
6. `analyze.md` — adversarial pre-implementation review (Skeptic owns).
7. `implement.md` — write code, TDD discipline, per-task commit.
8. `checklist.md` — verification checklist tied to phase.
9. `taskstoissues.md` — exporter for GitHub Issues / Linear.

**Acceptance:** `/bequite.constitution` generates a valid Constitution; `/bequite.specify` generates a valid spec; full pipeline `init → constitution → specify → plan → tasks → implement` runs on a 1-line feature ("add a /health endpoint").

**Tag:** `v0.4.0`.

### v0.4.1 — Slash commands wave 2: BeQuite-adds (9 commands)

**Tasks:** [parallel]
1. `init.md` — scaffolding command. Prompts: scale tier, audience, doctrine pack, hosts to wire. Writes `.bequite/` tree.
2. `research.md` — Phase 0. WebSearch + WebFetch + context7. Quotes findings back, requires user ack.
3. `stack.md` — Phase 1. Educational stack ADR. Cross-checks against `references/stack-matrix.md` and the freshness probe (forward-deps to v0.4.3).
4. `phases.md` — Phase 3. Decompose plan into phase markdowns under `specs/<feature>/phases/`.
5. `verify.md` — Phase 6. Playwright walks + smoke + secret scan + receipts. (Surface defined here; Playwright integration lands in v0.6.0.)
6. `review.md` — code review pass (separate from analyse).
7. `handoff.md` — Phase 7. Generate HANDOFF.md + screencast checklist.
8. `resume.md` — load memory + last activeContext + replay from last green phase.
9. `doctor.md` — diagnostic: missing files, broken hooks, stale dependencies.

**Acceptance:** `bequite init my-app --doctrine web-saas --scale 5000` produces the full tree; `bequite resume` correctly reloads memory after `git stash && git checkout main && git checkout -`.

**Tag:** `v0.4.1`.

### v0.4.2 — `bequite audit` (Constitution drift detector)

**Goal:** the unique feature — continuous Constitution + Doctrine enforcement.

**Tasks:**
1. `cli/bequite/audit.py` — scan rules engine. For each Iron Law and active Doctrine, emit a finding with file:line + suggested fix.
2. Rule packs:
   - Article I: code paths without a corresponding spec ID in commit message.
   - Article III: missing `activeContext.md` updates after a code commit.
   - Article V (security): `.env*` reads in code; secrets-shaped strings in source.
   - Article V (destruction): destructive ops outside ADR-approved scripts.
   - Article V scale-honesty: synchronous in-process job patterns above scale tier 50K.
   - Article VII hallucination: imports not in lockfile + not in allowlist.
   - Doctrine web-saas: hardcoded `font-family: Inter` outside `tokens.css`; gray-on-color contrast violations.
3. CI workflow `audit.yml` — runs on every PR, posts violations as inline comments.
4. PostToolUse hook `posttooluse-audit.sh` — runs lightweight subset on every Edit/Write.

**Acceptance:** test fixtures with planted violations all surface; clean fixtures emit zero findings.

**Tag:** `v0.4.2`.

### v0.4.3 — `bequite freshness` (knowledge probe)

**Goal:** before stack picks, verify candidates haven't rotted (the exact bug we caught in §2).

**Tasks:**
1. `cli/bequite/freshness.py` — probe runner.
2. Per-candidate checks:
   - `npm view <pkg> time.modified` < 6 months ago
   - `pip index versions <pkg>` returns a fresh release
   - GitHub repo last commit < 6 months
   - context7 has the library indexed at the version requested
   - OSV scanner reports zero unfixed criticals
   - Pricing-tier probe: WebFetch the vendor's pricing page; LLM-extract the tier the brief assumed; flag mismatch
3. Caching: 24h TTL keyed on package@version.
4. Report format: `freshness.md` per stack ADR with verdict per candidate.
5. Wire into `bequite stack` so a stale candidate blocks the ADR from being signed.

**Acceptance:** seeded test with `tauri-plugin-stronghold` correctly flags as deprecated; seeded test with current `better-auth` passes; pricing-mismatch on a stale Clerk MAU figure is caught.

**Tag:** `v0.4.3`.

### v0.5.0 — CLI thin wrapper

**Goal:** `uvx bequite` works on any machine with Python ≥3.11. CLI dispatches to skill via Claude API for non-Claude-Code users; falls through to running locally inside Claude Code if invoked there.

**Tasks:**
1. `cli/pyproject.toml` — hatchling, entry point `bequite = bequite.__main__:main`, deps `anthropic`, `tomli`, `click`, `rich`, `httpx`, `pydantic`.
2. `cli/bequite/__main__.py` — Click app. Subcommands: every command from v0.4.0 + v0.4.1 + audit + freshness + auto + doctor + memory + snapshot + cost + skill-install.
3. `skill_loader.py` — reads `skill/SKILL.md` + linked agents into a Claude API request with the right beta headers (`code-execution-2025-08-25, skills-2025-10-02, files-api-2025-04-14`).
4. `config.py` — Pydantic model for `bequite.config.toml`.
5. `hooks.py` — invokes `skill/hooks/*.sh` from non-Claude hosts.
6. CI: build sdist + wheel, smoke-test `uvx --from . bequite --version`.

**Acceptance:** `uvx --from git+...bequite init demo` from a clean machine produces the full tree without a Claude Code installation. `uvx bequite specify "add a /health endpoint"` produces a valid spec via Claude API.

**Tag:** `v0.5.0`.

### v0.6.0 — Verification gates (Playwright + smoke + walks)

**Goal:** P6 actually works. App boots, every route walked admin + user, zero console errors, secret scan green.

**Tasks:**
1. Wire Playwright MCP via `npx @playwright/mcp@latest`.
2. `qa.md` persona: planner → spec writer → generator → healer pattern.
3. Templates:
   - `tests/walkthroughs/admin-walk.md.tpl`
   - `tests/walkthroughs/user-walk.md.tpl`
   - `tests/seed.spec.ts.tpl`
4. Self-walk script `scripts/self-walk.sh` — boots app, logs in admin then user, traverses sitemap, captures console errors + 4xx/5xx.
5. Smoke test runner `scripts/smoke.sh` — curl every public endpoint, expect 200/401 per spec.
6. Receipt emission: `verify` outputs `receipts/<phase>-verify.json` (see v0.7.0 for the schema).
7. Acceptance-evidence check: `verify` enforces every task's acceptance evidence has been executed in this session.

**Acceptance:** on the bookings-saas example, `bequite verify` catches a planted broken redirect; the same command on a clean run reports green with receipt.

**Tag:** `v0.6.0`.

### v0.6.1 — Frontend Quality Module (Impeccable + shadcn + Magic + context7)

**Goal:** every web SaaS project ships with the design discipline the brief demanded.

**Tasks:**
1. Vendor `pbakaus/impeccable` at a pinned commit (recorded in `skill/skills-bundled/impeccable/.pinned-commit`). Attribute Paul Bakaus in `skills-bundled/impeccable/ATTRIBUTION.md` (MIT-license-respecting).
2. Wire 23 Impeccable commands as `bequite design <command>` aliases (`craft, teach, document, extract, shape, critique, audit, polish, bolder, quieter, distill, harden, onboard, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, live`).
3. shadcn registry MCP wiring (built-in to shadcn CLI v3+).
4. 21st.dev Magic MCP wiring (`@21st-dev/magic`); document API-key requirement.
5. context7 MCP wiring.
6. tweakcn link in stack-matrix; theme JSON template.
7. `templates/tokens.css.tpl` — design tokens with named, deliberate font choice.
8. axe-core gate in CI.
9. Doctrine `default-web-saas.md` updated to reference all of the above.

**Acceptance:** `bequite design audit` runs on a fresh shadcn-based project; tokens.css presence is enforced; axe-core gate fails a planted gray-on-color violation.

**Tag:** `v0.6.1`.

### v0.7.0 — Reproducibility receipts (JSON)

**Goal:** every implement / verify run produces an auditable receipt.

**Tasks:**
1. `cli/bequite/receipts.py` — receipt emitter.
2. Schema (Pydantic):
   ```
   {
     "version": "1",
     "session_id": "uuid",
     "phase": "P5",
     "timestamp_utc": "...",
     "model": {"name": "claude-opus-4-7", "reasoning_effort": "high"},
     "input": {"prompt_hash": "sha256:...", "memory_snapshot_hash": "sha256:..."},
     "output": {"diff_hash": "sha256:...", "files_touched": [...]},
     "tools_invoked": [{"name": "Edit", "args_hash": "sha256:...", "exit": 0}],
     "tests": {"command": "...", "exit": 0, "stdout_hash": "sha256:..."},
     "cost": {"input_tokens": ..., "output_tokens": ..., "usd": ...},
     "doctrine": ["default-web-saas"],
     "constitution_version": "1.0.0",
     "parent_receipt": "sha256:..."  // chain
   }
   ```
3. Storage at `.bequite/receipts/<sha>-<phase>.json`.
4. `bequite cost` reads receipts and rolls up.

**Acceptance:** receipts emitted on every phase transition; `bequite cost --since v0.6.0` returns a roll-up; receipt-replay test reconstructs prompt + memory state from receipt content.

**Tag:** `v0.7.0`.

### v0.7.1 — Signed receipts (ed25519)

**Tasks:**
1. Generate per-project keypair on `bequite init` (private in `.bequite/.keys/`, public in `.bequite/keys/public.pem`, gitignore the private).
2. Sign each receipt at emission.
3. `bequite verify-receipts` validates the chain.

**Acceptance:** tampered receipt is rejected; fresh receipt validates.

**Tag:** `v0.7.1`.

### v0.8.0 — Multi-model routing (cost-aware)

**Goal:** the §14 routing matrix actually drives model selection.

**Tasks:**
1. `routing.json` schema: `{ phase, persona, model, reasoning_effort, fallback_model, max_input_tokens, max_output_tokens }`.
2. `skill_loader.py` reads routing → picks model per call.
3. Cost ceiling: `bequite.config.toml::cost.session_max_usd` enforced via `stop-cost-budget.sh`. Stop hook fires when ceiling reached and asks Ahmed before continuing.
4. Provider list in v1: Anthropic (primary), OpenAI (planner alt), Google (Gemini for free-tier doc gen), DeepSeek (cheap implementer), Ollama (offline mode).
5. Provider auth via env vars / Doppler / Infisical references.

**Acceptance:** routing-test fixture forces Sonnet for implementer + Opus for reviewer; receipts confirm. Cost-ceiling test stops correctly.

**Tag:** `v0.8.0`.

### v0.8.1 — Live pricing fetch (best-effort)

**Tasks:**
1. WebFetch vendor pricing pages on `bequite stack` and `bequite cost`.
2. Cache 24h.
3. Surface a warning when vendor pricing changed since last cache.
4. Failure mode: if WebFetch fails, fall back to vendored `references/pricing-table.md` with a "stale" warning.

**Acceptance:** pricing-fetch unit test passes for Vercel + Supabase + Clerk + Anthropic; offline mode falls back gracefully.

**Tag:** `v0.8.1`.

### v0.9.0 — Three example projects

**Goal:** prove the seven-phase loop on three domain types. Examples are validation harnesses, not just docs.

**Tasks:** [parallel]
1. `examples/01-bookings-saas/` — Next.js + Hono + Supabase + Clerk + Vercel. Doctrine: `default-web-saas`. Scale: 5K. Bookings flow with admin + customer roles.
2. `examples/02-ai-tool-wrapper/` — Python CLI + Anthropic SDK + click. Doctrine: `cli-tool`. Scale: solo. CLI that summarises markdown.
3. `examples/03-tauri-note-app/` — Tauri v2 + SvelteKit + SQLite. Doctrine: `desktop-tauri`. Local-first note app with OS keychain secrets.

Each example ships with: full `.bequite/` tree, all seven phases run end-to-end, receipts archived, HANDOFF.md, screencast (`docs/screencasts/<example>.mp4`).

**Acceptance:** each example's `bequite verify` returns green; HANDOFF.md is hand-runnable by a second engineer.

**Tag:** `v0.9.0`.

### v0.9.1 — End-to-end test harness

**Tasks:**
1. `tests/e2e/seven-phase-walk.test.ts` — drives a fresh project from `bequite init` to `bequite handoff`; asserts artifacts at every phase.
2. `tests/e2e/auto-mode.test.ts` — drives `bequite auto` to completion; asserts safety rails.
3. `tests/e2e/doctrine-loading.test.ts` — fresh init with each doctrine; asserts correct rules loaded.
4. CI workflow `examples-e2e.yml` — runs the three example projects on every PR.

**Acceptance:** all three e2e tests pass on CI; nightly cron runs them on `main`.

**Tag:** `v0.9.1`.

### v0.10.0 — Auto mode (one-click run-to-completion)

**Goal:** `bequite auto --feature <name>` runs P0 → P7 sequentially with safety rails.

**Tasks:**
1. `cli/bequite/auto.py` — orchestrator with state machine: `P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → DONE` with explicit `BLOCKED`, `FAILED`, `PAUSED` states.
2. Per-phase commit (atomic): each phase exit creates a single commit with the receipt + artifacts; any phase reverts cleanly.
3. Skeptic gate at every phase boundary: must produce ≥1 kill-shot question whose answer is recorded in the phase's `analysis.md`.
4. Safety rails:
   - **Hard cost ceiling** (default $20/session, configurable). Exceeding pauses with prompt.
   - **Hard wall-clock ceiling** (default 6h). Exceeding pauses.
   - **Failure threshold:** 3 consecutive Implementer failures on a single task → `BLOCKED`, ask for human input.
   - **Banned-word check:** any completion message containing `should/probably/seems to/appears to/I think it works` → `BLOCKED`, ask for restate.
   - **Destructive op check:** any tool call hitting a `pretooluse-block-destructive` exit → `BLOCKED`, refuses to override.
5. Failure replay: on `BLOCKED` or `FAILED`, capture state to `.bequite/replays/<timestamp>/` and surface a single resume command.
6. Heartbeat: write `activeContext.md` every 5 minutes during long phases.
7. CLI flags: `--feature`, `--max-cost-usd`, `--max-wall-clock-hours`, `--phases <subset>`, `--mode slow|fast|auto`, `--on-failure pause|abort|continue-with-warning`, `--no-skeptic` (debug only).

**Acceptance:** `bequite auto --feature add-health-endpoint --max-cost-usd 5` runs to DONE on the bookings-saas example; cost stays under $5; receipts emitted at every phase. Planted Article-V violation correctly trips `BLOCKED`.

**Tag:** `v0.10.0`.

### v0.10.1 — Auto-mode resilience hardening

**Tasks:**
1. Resume from `BLOCKED`: `bequite auto resume <session>` re-loads receipts + memory + last green phase.
2. Parallel-task detection: ScrumMaster marks tasks as `parallel: true` in `tasks.md`; Implementer fans out via subagents, joins on completion. (Per AkitaOnRails: only when *genuinely* parallel — apply same change to many files, generate similar CRUD endpoints.)
3. Idempotent reruns: `bequite auto` can be run twice on the same feature without double-committing.
4. State persistence: `.bequite/auto-state/<session>.json`.

**Acceptance:** mid-run `Ctrl-C`, then `bequite auto resume <session>`, finishes correctly. Idempotency test passes.

**Tag:** `v0.10.1`.

### v0.11.0 — MENA bilingual module (the differentiated feature)

**Goal:** ship the only AI tech-lead with first-class Arabic + RTL support.

**Tasks:**
1. `doctrines/mena-bilingual.md` finalised (locale `ar-EG` default; Arabic + Egyptian dialect transcription; RTL layout; Arabic-friendly font set: Tajawal, Cairo, Readex Pro — none banned).
2. Researcher persona — bilingual mode: queries in Arabic AND English, scrapes Twitter/X MENA accounts + Telegram channels (config-listed), summarises in both.
3. Templates: `tokens.css.tpl` includes RTL-friendly font stack; `apps/web/` template wires `dir="rtl"` when locale is `ar-*`.
4. Verifier: Playwright walks include `?locale=ar` admin + user walks; visual diff catches LTR-only assumptions.
5. Audit rule: web-saas + mena-bilingual together → require RTL test fixture.

**Acceptance:** `bequite init demo --doctrine mena-bilingual,default-web-saas` produces a project that boots in Arabic, RTL, with passing walks at both locales.

**Tag:** `v0.11.0`.

### v0.12.0 — Universal entry (AGENTS.md + per-host adapters)

**Goal:** BeQuite-managed projects work in every coding agent that reads AGENTS.md (~25 hosts), not just Claude Code.

**Tasks:**
1. `template/AGENTS.md` — per Linux Foundation Agentic AI Foundation schema. Points at `.bequite/memory/constitution.md` + `CLAUDE.md` for Claude-specific extensions.
2. `template/CLAUDE.md` — Claude-Code extension; same content discoverable through AGENTS.md as primary.
3. `.cursor/rules/*.mdc` — per-folder rules ≤100 lines each.
4. `.codex/` — Codex skills + AGENTS.md fallback.
5. `.gemini/` — Gemini CLI memory.
6. `.windsurf/` — Cascade rules.
7. `bequite skill install` — installs the BeQuite skill into a host. Detects host (Claude Code / Cursor / Codex / Gemini / Windsurf / Cline / Kilo / Continue) and writes the right files.

**Acceptance:** smoke test: install BeQuite into a fresh Cursor project; verify `.cursor/rules/` populated; Cursor agent can read the Constitution. Same for Codex (`AGENTS.md` discovery test).

**Tag:** `v0.12.0`.

### v0.13.0 — Vibe-to-handoff artifact discipline

**Goal:** lock in the wedge. Every artifact is portable to vibe-coder UIs in v2.

**Tasks:**
1. JSON-schema validation for `spec.md` / `plan.md` / `tasks.md` / `phases.md` headers.
2. `bequite export --format spec-kit-zip` — zip artifacts in Spec-Kit-compatible format.
3. `bequite export --format claude-code-skill` — exports a project's `.bequite/` as a Claude Skill bundle.
4. Handoff readiness check: `bequite handoff --target <claude-code|cursor|codex|aider>` validates the project would load in that target.
5. CLI flag `bequite init --vibe-handoff` — adds an extra layer of artifact polish (more user-facing comments, more readable tasks.md, structured HANDOFF for non-engineers).

**Acceptance:** a project initialised with `--vibe-handoff` is loadable by Claude Code, Cursor, and Codex without modification (smoke-tested in CI).

**Tag:** `v0.13.0`.

### v0.14.0 — Documentation

**Tasks:** [parallel]
1. `docs/README.md` — vision, what BeQuite is, quickstart link.
2. `docs/QUICKSTART.md` — 5-minute path: `uvx bequite init demo --doctrine web-saas → bequite auto --feature health-endpoint → done`.
3. `docs/HOW-IT-WORKS.md` — architecture, the seven phases, hooks, receipts, auto mode.
4. `docs/DOCTRINE-AUTHORING.md` — how to fork doctrines; industry doctrine pattern.
5. `docs/HOSTS.md` — per-host install guide (Claude Code, Cursor, Codex, Gemini, Windsurf, Cline, Kilo).
6. `docs/AUTONOMOUS-MODE.md` — auto-mode safety rails, cost ceilings, failure modes.
7. `docs/SECURITY.md` — threat model, hooks reference, OWASP Top 10 (LLM 2025 + Web App) coverage map.
8. `template/README.md.tpl` — generated per-project README.
9. `template/HANDOFF.md.tpl` — handoff template for engineers + handoff-for-non-engineers section.

**Acceptance:** docs build clean (markdownlint + linkcheck); a non-Ahmed reader follows QUICKSTART end-to-end without external help.

**Tag:** `v0.14.0`.

### v0.15.0 — Release engineering

**Tasks:**
1. Semver discipline: every release tagged; `CHANGELOG.md` auto-generated from commit subjects (Conventional Commits).
2. CI workflows:
   - `ci.yml` — lint + unit + integration on every push.
   - `examples-e2e.yml` — full e2e on every PR + nightly.
   - `release.yml` — on tag, publish to PyPI (`pip install bequite`), npm (`@xpshawky/bequite` thin shell), and GitHub Release with attached signed receipts.
3. PyPI account setup checklist (`docs/MAINTAINER.md`) — *flagged for Ahmed*: I can prepare the workflow but PyPI account creation is one-way-door. We do this together.
4. Code-signing keys for the npm shell (deferred to v1.0.0 release prep — also Ahmed-supervised).
5. License audit: `osv-scanner` + `license-checker` on every release.

**Acceptance:** dry-run release on a fork tags + builds + creates a Release without publishing.

**Tag:** `v0.15.0`.

### v1.0.0 — Full release

**Goal:** v1.0.0 ships; the world can `uvx bequite`.

**Tasks:**
1. Final e2e on all three examples.
2. Final audit across the whole repo (BeQuite eats its own food).
3. Final freshness sweep on the stack matrix and references.
4. Tag `v1.0.0`. Publish to PyPI. Publish thin npm shell.
5. Release notes blog post (English + Arabic) — *will require Ahmed's review before publishing*.
6. Submit to AGENTS.md ecosystem registry.
7. Open source announcement to: HN, X, Reddit r/ChatGPTCoding, Arab Net, MENA tech press.

**Acceptance:** `uvx bequite --version` returns `1.0.0`; install works on a clean Win/Mac/Linux box; the bookings-saas example clones-and-builds in under 10 minutes by a second engineer.

**Tag:** `v1.0.0`.

---

## 5. The auto-mode design (one-click run-to-completion)

### State machine

```
INIT → P0_RESEARCH → P1_STACK → P2_PLAN → P3_PHASES → P4_TASKS →
       P5_IMPLEMENT (per-task loop) → P6_VERIFY → P7_HANDOFF → DONE

Any phase can exit to: BLOCKED (needs human), FAILED (gate trip), PAUSED (rail trip).
```

### Per-phase contract

Every phase enters with **memory + receipts + previous-phase-output**, and exits only when:

1. The phase's artifact exists and validates against its schema.
2. The Skeptic produces ≥1 kill-shot question and the primary answers it.
3. The phase's gate (Article II verification) passes.
4. The receipt is emitted and signed.
5. A commit lands tagged `bequite-auto/<feature>/P<n>`.

### Safety-rail boundaries (when auto-mode pauses for Ahmed)

Even in `--mode auto`, I pause at:

- **Cost ceiling reached** (`max-cost-usd` exceeded — default $20/session).
- **Wall-clock ceiling reached** (`max-wall-clock-hours` exceeded — default 6h).
- **3 consecutive Implementer failures on the same task.**
- **Banned-word check trips** (completion message contains `should/probably/seems to/appears to/I think it works`).
- **Hook block** (`pretooluse-*` exit 2 — never auto-override; always pause).
- **Stack ADR sign-off** is a one-way-door — pause unless `--auto-sign-stack` flag is passed (default off).
- **First HANDOFF generation** — pause for human review of the engineer-handoff doc.
- **One-way-door operations** never auto-run: PyPI publish, npm publish, git push to main, force push, `terraform apply`, DB migrations against shared DBs.

### What auto-mode does NOT do

- Does not skip Phase 0 research.
- Does not silently change doctrines mid-run.
- Does not bypass hooks under any flag (the brief is explicit; I keep that contract).
- Does not generate marketing or press content without a pause.

---

## 6. Verification (how we prove v1.0.0 actually works)

End-to-end across all three examples:

1. Fresh machine. `uvx --from git+...bequite init e2e-bookings --doctrine default-web-saas --scale 5000`.
2. Assert tree: `.bequite/memory/{constitution,projectbrief,…}.md`, `specs/`, `apps/`, `tests/`, AGENTS.md, CLAUDE.md.
3. `bequite auto --feature add-confirmation-flow --max-cost-usd 10`.
4. Auto-mode runs P0 → P7 with phase commits.
5. Receipts at every phase, signature chain valid.
6. `bequite verify` green: Playwright admin-walk + user-walk + smoke + secret-scan + audit + freshness.
7. Plant a Constitution violation — `bequite audit` catches it.
8. Plant a deprecated package — `bequite freshness` catches it.
9. Run the same auto-mode on `02-ai-tool-wrapper` (CLI doctrine) and `03-tauri-note-app` (desktop doctrine).
10. Run `bequite skill install` into a fresh Cursor / Codex / Gemini project; smoke-test that each host loads BeQuite.
11. Run `bequite export --format spec-kit-zip`; verify the export loads in vanilla Spec-Kit.
12. Hand the bookings-saas folder + HANDOFF.md to a second engineer; they install + boot + deploy from docs alone.

If any of those 12 steps fail, v1.0.0 does not ship.

---

## 7. Honest scope assessment

This is a **6–10 week project of focused, autonomous work** at full pace, given the scope Ahmed approved. Each sub-version maps to roughly 0.5–1.5 days of focused execution including the verification loop. Realistic constraints:

- Some sub-versions (v0.6.0 Playwright, v0.10.0 auto mode, v0.11.0 MENA, v0.12.0 host adapters) are larger and span multiple sessions.
- One-way-door operations (PyPI publish, code-signing keys, npm shell, MENA-language voice/transcription accuracy) require Ahmed's oversight and will pause auto-execution.
- Freshness probe is brittle by nature — vendor pricing pages and package APIs change. v0.4.3 ships best-effort; ongoing tuning into v1.x.
- AkitaOnRails 2026 finding cuts both ways: even with Skeptic-as-adversary, solo Opus 4.7 on cohesive tasks beats forced delegation. Auto-mode default routing reflects that — Skeptic runs at *boundaries*, not inside coupled implementation tasks.
- The brief's "no should/probably" rule is respected here. Where I would otherwise hedge, I'm calling out a concrete risk and a concrete mitigation.

## 8. Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Auto-mode burns cost on a stuck loop | Medium | Hard ceiling + 3-failure threshold + receipt cost roll-up |
| Vendor pricing / API drift breaks freshness probe | High | 24h cache + offline fallback + best-effort tag + ongoing v1.x tuning |
| Impeccable upstream breaks BeQuite | Medium | Pinned snapshot vendored; not live-pulled |
| Roo Code / Stronghold / EV cert advice rotates again | High | `bequite freshness` runs on the BeQuite repo itself in CI; stale references trip the audit |
| Skill format constraints (API skills can't run packages) limit BeQuite features | Medium | Two skill modes — `claude-code-full` (filesystem + scripts) and `api-portable` (offline-only). Documented in HOSTS.md |
| MENA module is hard to verify without an Arabic-native reviewer | Medium | Pause for Ahmed's review on first MENA-locale walks; flag known limitations |
| Anthropic deprecates a beta header BeQuite uses | Low | Receipts log the header version; on deprecation, doctor command surfaces it; switch to GA when available |
| User loses receipts via `git clean -fd` | Low | `.bequite/receipts/` not gitignored; documented |
| Per-project ed25519 key compromised | Low | Keys per-project; rotation command in v1.x; never committed |

## 9. Files to be created (master list, in build order)

This is the complete checklist. Numbered lines map to sub-versions.

```
v0.1.0
  /README.md                                          (root)
  /LICENSE                                            (MIT)
  /CHANGELOG.md
  /.gitignore
  /skill/templates/constitution.md.tpl
  /skill/templates/doctrine.md.tpl
  /skill/templates/{projectbrief,productContext,systemPatterns,techContext,activeContext,progress}.md.tpl
  /skill/templates/adr.md.tpl
  /template/.bequite/memory/{constitution,projectbrief,productContext,systemPatterns,techContext,activeContext,progress}.md
  /template/.bequite/memory/decisions/.gitkeep
  /template/.bequite/memory/prompts/.gitkeep
  /template/.bequite/memory/logs/.gitkeep

v0.1.1
  /skill/doctrines/{default-web-saas,cli-tool,ml-pipeline,desktop-tauri,library-package,fintech-pci,healthcare-hipaa,gov-fedramp}.md
  (mena-bilingual.md is created in v0.11.0)

v0.2.0
  /skill/SKILL.md
  /skill/agents/{researcher,architect,scrum-master,implementer,reviewer,skeptic,qa,tech-writer,frontend-design}.md
  /skill/routing.json
  /skill/templates/bequite.config.toml.tpl
  /template/.claude/skills/bequite/                   (symlink target)

v0.3.0
  /skill/hooks/{pretooluse-secret-scan,pretooluse-block-destructive,pretooluse-verify-package,
                 posttooluse-format,posttooluse-lint,stop-verify-before-done,
                 sessionstart-load-memory,sessionstart-cost-budget}.sh
  /tests/integration/hooks/

v0.4.0
  /skill/commands/speckit-extends/{constitution,specify,clarify,plan,tasks,analyze,implement,checklist,taskstoissues}.md

v0.4.1
  /skill/commands/bequite-adds/{init,research,stack,phases,verify,review,handoff,resume,doctor}.md

v0.4.2
  /skill/commands/audit.md
  /cli/bequite/audit.py
  /.github/workflows/audit.yml
  /skill/hooks/posttooluse-audit.sh

v0.4.3
  /skill/commands/freshness.md
  /cli/bequite/freshness.py
  /skill/references/package-allowlist.md

v0.5.0
  /cli/pyproject.toml
  /cli/README.md
  /cli/bequite/{__init__,__main__,commands,skill_loader,config,hooks}.py

v0.6.0
  /skill/templates/{tests/walkthroughs/admin-walk,tests/walkthroughs/user-walk,tests/seed.spec.ts}.tpl
  /template/scripts/{self-walk,smoke}.sh

v0.6.1
  /skill/skills-bundled/impeccable/                   (vendored snapshot)
  /skill/skills-bundled/impeccable/{ATTRIBUTION,.pinned-commit}.md
  /skill/templates/tokens.css.tpl

v0.7.0
  /cli/bequite/receipts.py
  (schema embedded in receipts.py)

v0.7.1
  /cli/bequite/receipts_signing.py

v0.8.0
  (no new files; routing.json + cost guardrail in config)
  /skill/hooks/stop-cost-budget.sh

v0.8.1
  /cli/bequite/pricing.py
  /skill/references/pricing-table.md

v0.9.0
  /examples/01-bookings-saas/
  /examples/02-ai-tool-wrapper/
  /examples/03-tauri-note-app/

v0.9.1
  /tests/e2e/{seven-phase-walk,auto-mode,doctrine-loading}.test.ts
  /.github/workflows/examples-e2e.yml

v0.10.0
  /skill/commands/auto.md
  /cli/bequite/auto.py

v0.10.1
  /cli/bequite/auto_state.py

v0.11.0
  /skill/doctrines/mena-bilingual.md
  /skill/templates/tokens.css.tpl                     (RTL-aware)
  /skill/agents/researcher.md                          (extended for bilingual)

v0.12.0
  /template/AGENTS.md.tpl
  /template/CLAUDE.md.tpl
  /template/.cursor/rules/*.mdc.tpl
  /template/.codex/, .gemini/, .windsurf/             (host-specific)
  /skill/commands/skill-install.md

v0.13.0
  /cli/bequite/exporters/{spec_kit,claude_skill}.py
  /docs/VIBE-HANDOFF.md

v0.14.0
  /docs/{README,QUICKSTART,HOW-IT-WORKS,DOCTRINE-AUTHORING,HOSTS,AUTONOMOUS-MODE,SECURITY,MAINTAINER}.md
  /template/README.md.tpl
  /template/HANDOFF.md.tpl
  /template/SECURITY.md.tpl

v0.15.0
  /.github/workflows/{ci,release}.yml

v1.0.0
  (release prep, no new code; tagging, publishing, announcements)
```

---

## 10. Reused, not built fresh

- **Cline Memory Bank pattern** (six files) — verbatim, attribute Cline (https://docs.cline.bot/features/memory-bank).
- **Spec-Kit's command grammar** — adopt `/speckit.<command>` namespace; we add `/bequite.<command>` for our 9 + audit + freshness + auto.
- **AGENTS.md schema** — Linux Foundation Agentic AI Foundation standard.
- **Anthropic SKILL.md frontmatter** — official schema, three-level loading.
- **Impeccable** — pinned snapshot at `skill/skills-bundled/impeccable/`, attributed to Paul Bakaus, MIT-license-respecting.
- **Playwright MCP** — `npx @playwright/mcp@latest`, by Microsoft.
- **shadcn registry MCP** — built into shadcn CLI v3+.
- **21st.dev Magic MCP** — `@21st-dev/magic`.
- **context7** — Upstash, version-pinned docs.
- **tweakcn** — visual theme editor with code export.
- **Better-Auth, Clerk, Keygen, Supavisor, AzureSignTool, notarytool** — recommended in the corrected stack matrix.

## 11. What this plan authorises

By exiting plan mode, Ahmed authorises me to:

- Create the BeQuite repo locally (`C:\Ahmed Shawky\Antigravity projects\BeQuite\` is the working directory; I'll use `bequite/` as the source root, leaving `BEQUITE_BOOTSTRAP_BRIEF.md` untouched).
- Initialise git, commit per sub-version with tagged releases.
- Write all files listed in §9.
- Run local tests, `uvx`, `npm`, `npx` for tooling that builds on the local box.
- Pause autonomously at any safety-rail boundary defined in §5.
- Not push to GitHub, not publish to PyPI/npm, not run any one-way-door operation without Ahmed's explicit approval.

## 12. What this plan does NOT authorise

- Pushing the BeQuite repo to a public remote (Ahmed creates the GitHub org / repo; I supply the local commits).
- Creating PyPI / npm accounts, publishing packages.
- Generating press / blog content for publication.
- Scraping Twitter/X / Telegram MENA channels (config-listed only — Ahmed seeds the list).
- Spending more than the configured `max-cost-usd` per session without re-approval.
- Reading `.env`, generating secrets, or committing keys.
- Any action that breaks an Iron Law of the Constitution.

---

## 13. Immediate next actions (after `ExitPlanMode` is approved)

1. Snapshot this plan to `.bequite/memory/prompts/v1/2026-05-10T<UTC>_initial-plan.md`.
2. Begin v0.1.0: create the repo skeleton + Constitution v1.0.0.
3. Commit + tag `v0.1.0`.
4. Update `activeContext.md` and `progress.md` per Article III.
5. Continue to v0.1.1 unless a safety rail trips or Ahmed pauses.

I'll keep going phase by phase until v1.0.0 is shipped or a rail trips. Memory bank discipline means each session resumes cleanly from the last green sub-version.
