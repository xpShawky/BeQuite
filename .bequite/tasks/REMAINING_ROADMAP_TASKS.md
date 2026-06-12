# Remaining Roadmap Tasks (post-alpha.22 stabilization, 2026-06-12)

> **SUPERSEDED (2026-06-12):** the canonical remaining-work source is now `.bequite/tasks/REMAINING_WORK_MASTER.md` (sections A-G, queryable via bequite/now/suggest/recover/memory/skill-audit). This file is preserved as history; do not update it.

The single ledger separating done / pending / parked / alpha.23 / future. Statuses: each item lists current status · reason · dependencies · what must be true before building · confidence · next action. Companion: `ALPHA_22_TASK_CHECKLIST.md` (the shipped-pass ledger). **No live trial has been run on any alpha.22 capability — nothing below claims runtime validation.**

## A. Keep as-is until live trial (built, untested against real input)

| Item | Status | Must be true before changing | Conf. | Next action |
|---|---|---|---|---|
| /bq-course · /bq-knowledge · /bq-reference · /bq-pain-radar · /bq-integrate · /bq-proposal | BUILT (alpha.22 skeletons + specs); **UNTRIED live** | one real run each; gaps logged to MISTAKE_MEMORY | 80–86% per shape decisions | user runs one on a real task when ready (C5 or C3 recommended first) |

## B. Maintenance next (cheap, safe, do before alpha.23)

| Item | Status | Reason | Next action |
|---|---|---|---|
| /bq-skill-audit baseline for localization-rtl + guard-pass | pending | registry marks them provisional ✓ | run M2 once; update registry Q column |
| /bq-verify drift run | pending | stabilization fixed 7 doc findings; drift arg should confirm zero remain | run after this pass lands |
| Install docs verification | **DONE this pass** | INSTALL counts re-verified 52/29; pointer to canonical counts present | — |
| Stale count check | **DONE this pass** | README 39/42/18-era counts fixed; repo-wide sweep clean | re-run inside every release verify |
| USING_BEQUITE_COMMANDS full walkthrough refresh | pending (pointer added; walkthroughs current to alpha.14) | append-only doc, low risk | refresh when a capability command gets its first live walkthrough |

## C. alpha.23 candidate (queued, approved direction, NOT built)

| Item | Status | Dependencies | Must be true first | Conf. | Next action |
|---|---|---|---|---|---|
| **/bq-offer (C11)** — sellable-offer builder | queued; ID reserved; output spec sketched in forgotten-candidate review | C8 proposal + C6 pain-radar in usable shape (they are; live trial preferred) | explicit user go → 15-step feature workflow → taxonomy check | 85% | user approval is the only blocker |

## D. V1 argument candidates (approved shapes, documented, build-on-demand)

All shaped as arguments in alpha.22/addendum — each is buildable in its owning command whenever first needed; none blocks anything:
`/bq-feature demo-data` (80%) · `/bq-review persona` (78%) · `/bq-scope intake` (80%) · `/bq-proposal price` (75%) · `/bq-plan migration` (82%) · `/bq-job-finder interview-prep` (80%) · `/bq-feature landing` (80%) · `/bq-writing-dna repurpose` (78%) · `/bq-writing-dna seo-brief` (75%) · `/bq-proposal sow` (70%) · `/bq-audit a11y` (75%) · `/bq-explain diagram` (72%) · `/bq-job-finder resume` (70%).
**Next action for all:** implement the argument's procedure block on first real demand (each is a doc-level addition to an existing command — no new files needed beyond outputs).

## E. V2 / parked (explicit promotion conditions)

| Item | Status · reason | Must be true before building | Conf. |
|---|---|---|---|
| /bq-automation (or /bq-bot) | parked — strongest V2 candidate; scope not yet crisp | tool-neutral spec written + one real automation use-case from pain-radar; stays n8n/Activepieces/Make/cron/Playwright-neutral | 70% |
| /bq-data-product | parked — merge-watch with C7 | C7 sees real use; then decide merge vs standalone | 60% |
| AI Service Business Builder | parked — orchestrator over C5/C6/C8/C10 + offer | underlying commands live-proven + /bq-offer built | 68% |
| Workflow export | parked | secret-scan design first (hard requirement) | 65% |
| Agent pack generator | parked — prefer `/bq-skill-audit generate-pack` | Guard Pass + skill audit mature one more cycle | 62% |
| /bq-release template | parked V2 | secret-scan discipline + launch-kit args proven | 72% |
| Local business digitizer | parked — template/route first | one real pain-radar → feature run in a local-business niche | 75% |
| Brand kit generator | parked | C3 reference matures | 62% |
| Community pack | parked | course adoption signal | 65% |
| App store launch kit | parked V2 | a real mobile launch need | 68% |
| Recording-to-assets (/bq-recording) | parked V2 | researched lightweight frame-extraction path + real demand | 55% |
| Cross-agent adapters (`bq` wrapper · AGENTS.md generator · Cursor rules template) | roadmap — manual per-agent setup now documented in `INSTALL_FOR_OTHER_AGENTS.md` (orchestration update); adapters would automate what is already copy-paste-doable | real cross-agent usage demand; stays a thin script, never an app | 70% |
| bequite-course-architect skill | deferred candidate (new this pass) | one real /bq-course run proves which pedagogy knowledge deserves a reusable SKILL.md | 72% |

**Maintainer rule:** when an item moves buckets, update this file + LAST_RUN in the same commit. Promotion always goes through the 15-step feature workflow + shape taxonomy.
