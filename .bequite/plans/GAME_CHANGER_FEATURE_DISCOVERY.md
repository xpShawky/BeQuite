# Game Changer Feature Discovery (decision tracker)

> The **decision ledger** over BeQuite's game-changer candidates. Full analyses live in `docs/specs/GAME_CHANGER_FEATURES.md` (alpha.18 report) + `docs/specs/CAPABILITY_FEATURE_IDEAS.md` (2026 demand ranking) — this file tracks KEEP / REJECT / BUILT decisions so they aren't re-litigated. **Proposals only become builds via the 15-step feature-addition workflow.**

**Updated:** 2026-06-11 (alpha.19 Fable pass)

---

## Already built (graduated from this list)

| Feature | Built in | Command/skill |
|---|---|---|
| Live UI edit | alpha.4 | /bq-live-edit |
| UI variants | alpha.4 | /bq-uiux-variants |
| Opportunity radar (jobs + money) | alpha.8/10 | /bq-job-finder, /bq-make-money |
| Presentation builder | alpha.13 | /bq-presentation |
| Design continuity (visual proof) | alpha.17 | Design Continuity Gate + VISUAL_QA_REPORT |
| Machine-enforcement hooks | alpha.18 | .claude/hooks/* (opt-in) |
| **Writing DNA** | **alpha.19** | **/bq-writing-dna + bequite-writing-dna** |
| **Skill generator quality loop** | **alpha.19** | **/bq-skill-audit + bequite-skill-auditor** |

## KEEP — proposed, awaiting approval (ranked)

| # | Feature | What it does | Why different | Pain | Output | Shape | Lightweight fit | Deps | Risk | Safety gate | Stage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Regression ledger** | Append-only ledger of every fixed bug + its guard test; /bq-verify replays guards | Fixes stop silently un-fixing | "it broke again" | REGRESSION_LEDGER.md + guard list | extend /bq-fix + /bq-verify | ✅ markdown only | none | low | none needed | MVP next |
| 2 | **Drift detector** | Periodic check: docs/counts/gates vs reality (the alpha.14 audit, automated) | Self-audits today are heroic, not routine | silent doc rot | DRIFT_REPORT.md | /bq-drift or fold into /bq-skill-audit | ✅ | none | low | report-only | MVP next |
| 3 | ~~Confidence surfacing~~ → **BUILT in alpha.21** as the Confidence Forecast system (banded % + evidence levels + calibration loop; integrated into 9 commands) | | | | | | | | | | graduated |
| 4 | **Ship-readiness scorecard** | One-page go/no-go: gates+tests+security+docs+rollback | Last-mile shipping is scattered across P3/P4 | "are we actually ready?" | SHIP_READINESS.md | extend /bq-verify or /bq-release | ✅ | none | low | release gate stands | V1 |
| 5 | ~~Professional Expert Mode (alias)~~ → **DOCUMENTED in alpha.21** as the `expert` composition alias (deep + strict evidence + safety scope + domain checklist) per FEATURE_TYPE_TAXONOMY ruling — NOT a 5th mode | | | | | | | | | | graduated |
| 6 | **Workflow export** | Export a project's .bequite/ learnings as a reusable pack | Team reuse of project memory | restarting discipline per project | export bundle | /bq-export | ✅ | none | medium (secrets scrub needed) | secret-scan before export | V2 |
| 7 | **Automation/bot builder** | Guided n8n/Make/Zapier-class automation with Article VIII discipline | Roadmap since alpha.5 | automation w/o engineering | automation spec + impl | /bq-automation family | ⚠ per-project deps | tool-neutral picks | medium | paid-service + deploy gates | V2 |
| 8 | **Data-to-product builder** | CSV/API → dashboard/report product scaffold | Common upwork-style demand | data sitting unused | scaffold + product | intent under /bq-auto | ⚠ | per-project | medium | scope gate | V2 |
| 9 | **AI service business builder** | Combines make-money + product-strategist + ship-readiness into a "launch a service" path | End-to-end earner journey | from skill to income | business plan + assets | orchestration of existing cmds | ✅ | none | medium (overpromise risk) | trust checks | V2 |
| 10 | **3D/animated site builder** | Cinematic/3D site workflows (R3F/GSAP-class candidates) | High-wow frontend demand | premium sites | site + motion plan | extend frontend-design-system refs | ⚠ heavy per-project deps | tool-neutral | high (deps+perf) | design + dep gates | V2 |
| 11 | **Product movie generator** | Product demo video planning (script/storyboard/capture plan) | Marketing last-mile | demo videos are hard | MOVIE_PLAN.md + assets | possible /bq-presentation extension | ⚠ render tooling | per-project | high | publishing gate | V2 |
| 12 | **Agent pack generator** | Generate a domain skill-pack from a project's patterns | Meta-capability | every team rebuilds packs | new SKILL.md set | /bq-skill-audit sibling | ✅ | none | medium (quality control) | report+approve | V2 |

## REJECT (with reasons — don't re-propose without new evidence)

| Feature | Reason |
|---|---|
| Secure-launch daemon / monitoring service | requires runtime — ADR-004 |
| AI-detector evasion (any framing) | ethics line — Writing DNA explicitly excludes |
| Auto-publishing pipelines (social/slides/store) | external-publishing hard gate; human stays in the loop |
| Full visual-QA CI with browser farm | default heavy dep; optional-browser tier model stands |

## Decision rule

A KEEP item graduates only when: user approves → 15-step workflow runs (research → scope → plan → tasks → impl → docs → verify) → entry moves to "Already built". This file is the memory that prevents both re-litigating rejects and forgetting approved intents.

---

## alpha.22 status update (Older V1 Candidate Review — full table in APPROVED_CAPABILITY_SHAPE_DECISIONS.md)

Built+verified: #3 Confidence Surfacing (alpha.21) · #5 Expert alias (alpha.21). Absorbed as arguments this pass: #1 Regression Ledger → `/bq-verify regressions` · #2 Drift Detector → `/bq-verify drift` · #4 Ship-readiness → `/bq-release readiness` · #11 Product Movie → `/bq-release demo-video` · #10 3D Site → `/bq-reference style=cinematic-3d` + `/bq-uiux-variants style=3d`. Parked V2: #6 Workflow Export (secret-scan design first) · #7 Automation/Bot Builder (strongest parked candidate; spec first) · #8 Data-to-Product (merge-watch with C7) · #9 AI Service Business Builder (orchestrator; after C5/C6/C8 stabilize) · #12 Agent Pack Generator (prefer `/bq-skill-audit generate-pack`; after Guard Pass matures). Zero new commands from V1.
