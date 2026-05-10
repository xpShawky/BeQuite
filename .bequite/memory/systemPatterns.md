# System Patterns: BeQuite

> The architecture, the recurring design patterns, and the ADR index. Updated whenever a pattern emerges or an ADR lands. Linked from `plan.md` per feature.

---

## 1. The high-level shape

```
                        ┌─────────────────────────────────────────┐
USER  ──prompt──▶       │   ENTRY ROUTER (skill / CLI / IDE)      │
                        └──────────────┬──────────────────────────┘
                                       │ loads
                ┌──────────────────────┼──────────────────────┐
                ▼                      ▼                      ▼
    .bequite/memory/constitution  .bequite/memory/*    AGENTS.md / CLAUDE.md
       (Iron Laws + Doctrines)     (six Bank files)    .cursor/rules/*.mdc
                │                      │                      │
                └──────────────────────┴──────────────────────┘
                                       │
                              ┌────────▼────────┐
                              │ ORCHESTRATOR    │  (planner: Opus 4.7 high
                              │  "Tech-Lead"    │   reasoning effort)
                              └────────┬────────┘
                                       │ delegates by phase
   ┌────────┬────────┬────────┬────────┼────────┬────────┬────────┐
   ▼        ▼        ▼        ▼        ▼        ▼        ▼        ▼
  P0       P1       P2       P3       P4       P5       P6       P7
Research Stack    Plan    Phases   Tasks  Implement Verify   Handoff
                                       │
                              ┌────────▼────────┐
                              │ EXECUTOR POOL   │  (Sonnet 4.5,
                              │  forked context │   Haiku 4.5)
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │ SKEPTIC GATE    │  adversarial twin —
                              │ at every phase  │  one kill-shot question
                              │ boundary        │  per phase exit
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │ DETERMINISTIC   │  hooks: secret-scan,
                              │ GATES (hooks)   │  block-destructive,
                              │  exit code 2    │  verify-package,
                              │  blocks tool    │  verify-before-stop,
                              │                 │  cost-budget
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │ RECEIPT CHAIN   │  signed JSON per
                              │ (.bequite/      │  phase; ed25519;
                              │  receipts/)     │  parent-hash chain
                              └─────────────────┘
```

## 2. The seams

| Seam | Contract location | Owner | Policy |
|---|---|---|---|
| Skill ↔ host | `skill/SKILL.md` (Anthropic Skills frontmatter schema) | BeQuite skill maintainer | semver-strict; new fields additive |
| CLI ↔ skill | `cli/bequite/skill_loader.py` (Claude API call with beta headers) | BeQuite CLI maintainer | beta-headers logged in receipts; on header deprecation, doctor command surfaces |
| Hooks ↔ tool calls | `skill/hooks/*.sh` (exit codes per Claude Code hook contract) | BeQuite hooks maintainer | block = exit 2; warn = exit 0 with message; never bypass |
| Receipts ↔ audit | `cli/bequite/receipts.py` Pydantic schema; ed25519 chain | BeQuite receipts maintainer | parent-hash chain unbroken; tamper = chain invalid |
| Constitution ↔ Doctrines | `skill/templates/constitution.md.tpl` + `skill/doctrines/*.md` schema | xpShawky | Iron Laws beat Doctrines; ADR-only amendment |
| Memory Bank ↔ session | `.bequite/memory/{6 files}` read on `SessionStart`; written on task end | every agent | Article III binding |

## 3. Recurring design patterns

- **Pattern: persona separation.** Each phase has a named persona (Researcher, Architect, ScrumMaster, Implementer, Reviewer, Skeptic, QA, TechWriter, FrontendDesign). Personas live in `skill/agents/<name>.md` and load on demand. Rationale: routing matrix can target each persona to the cheapest viable model. Anti-pattern: collapsing personas into one mega-prompt loses the routing leverage.
- **Pattern: gate-by-default.** Hooks are deny-by-default for destructive operations (`pretooluse-block-destructive.sh`). Allowing a destructive op requires an explicit ADR. Rationale: Article IV. Anti-pattern: hook bypass flags.
- **Pattern: ADR for one-way doors.** Stack picks, security boundaries, scale-tier choices, framework swaps. Rationale: Bezos-style — reversible decisions move fast; one-way doors get an ADR. Anti-pattern: silent stack drift.
- **Pattern: layered Constitution.** Iron Laws (universal) + Doctrines (per-project). Rationale: a CLI tool doesn't need an Inter font ban; a fintech app does need PCI rules. Anti-pattern: monolithic universal-feeling rules that don't fit.
- **Pattern: receipt-per-phase.** Every phase commits its receipt JSON. Rationale: SBOM-but-for-AI; auditable; replay-able. Anti-pattern: single end-of-project receipt that captures nothing about the journey.
- **Pattern: Skeptic at boundaries (not inside).** Per AkitaOnRails 2026: forced multi-model on coupled tasks loses to solo frontier. Skeptic runs *at phase exit*, not during the phase. Rationale: empirical. Anti-pattern: forced reviewer on every line.
- **Pattern: vendored peer skills, pinned commits.** Impeccable, Memory Bank pattern, Spec-Kit grammar — all vendored at known-good commits, never live-pulled. Rationale: upstream churn cannot break BeQuite. Anti-pattern: live `git submodule` to a moving target.

## 4. State management

- **System of record for project intent:** `.bequite/memory/projectbrief.md`.
- **System of record for code state:** the git repo + receipts.
- **System of record for "what's happening now":** `.bequite/memory/activeContext.md` (refreshed every task; auto-mode heartbeats every 5 minutes).
- **Caches:** freshness-probe responses (24h TTL, keyed on `pkg@version`) and pricing-table fetches (24h TTL).
- **Background jobs:** none in BeQuite-itself. Doctrines for downstream projects recommend BullMQ / Inngest / Trigger.dev based on scale tier.

## 5. Cross-cutting concerns

| Concern | Strategy | Where it lives |
|---|---|---|
| Auth (BeQuite-itself) | none — no service to protect | n/a |
| Logging | structured JSON to stdout; receipts as audit trail | `cli/bequite/__main__.py` |
| Tracing / observability | opt-in telemetry (ADR-002 pending) | future |
| Errors | exit code 2 for hook blocks; exit 1 for runtime errors; rich tracebacks via `rich` | `cli/bequite/__main__.py` |
| Rate limiting (Claude API) | per-session cost ceiling + wall-clock ceiling | `cli/bequite/auto.py` (v0.10.0) |
| Feature flags | none — sub-versions are the unit of release | `CHANGELOG.md` |
| i18n | Constitution + skill prompts: English. User-facing CLI text: English + Arabic. | `cli/bequite/i18n/` (v0.11.0) |

## 6. The ADR index

Every architectural decision lives at `.bequite/memory/decisions/`.

| ADR | Title | Status | Touches Iron Law(s) | Touches Doctrine(s) |
|---|---|---|---|---|
| ADR-001-stack | BeQuite's own stack: Python CLI + Markdown skill + bash hooks | proposed (drafting in v0.5.0) | I, V, VII | library-package, cli-tool |
| ADR-002-telemetry | Receipt-only opt-in telemetry, never code or prompts | proposed (drafting in v0.7.0) | IV, VI | library-package |
| ADR-003-doctrine-distribution | Community Doctrines via separate `bequite-doctrines` org | proposed (drafting in v0.12.0) | I | library-package |

## 7. The receipts

Every implementation phase emits a signed receipt at `.bequite/receipts/<sha>-<phase>.json`. The chain proves the project's history is reproducible.

- **Latest receipt:** (none yet — receipts begin emitting in v0.7.0)
- **Receipt count:** 0
- **Verification:** `bequite verify-receipts` (ships v0.7.1)

## 8. Known sharp edges

- **The freshness probe is brittle.** Vendor pricing pages and registry APIs change. v0.4.3 ships best-effort with 24h cache and offline fallback. Tuning continues into v1.x.
- **API skills cannot install packages.** Anthropic Skills loaded via `/v1/skills` have no network and no package install. We ship two skill modes: `claude-code-full` (filesystem + scripts) and `api-portable` (offline-only). Documented in `docs/HOSTS.md`.
- **AkitaOnRails 2026 cuts both ways.** Routing reflects empirical reality — Skeptic is at *boundaries*, not inside coupled tasks. Tuning the routing.json based on real auto-mode runs is a v1.x activity.
- **Single-maintainer bundled skill.** Impeccable is by Paul Bakaus alone (~26.6k stars). We vendor pinned; an upstream breakage requires a manual snapshot bump in `skill/skills-bundled/impeccable/.pinned-commit`.
- **MENA verification needs a native reviewer.** Auto-mode pauses for Ahmed's review on first MENA-locale walks. Limitations are flagged.
- **Receipts can be lost via `git clean -fd`.** They are *not* gitignored. Documented in HANDOFF.md.
