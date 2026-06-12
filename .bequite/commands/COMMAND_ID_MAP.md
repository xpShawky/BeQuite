# BeQuite Command ID Map (canonical) — alpha.22

Display-only catalog IDs (Option A — files never renamed). Strategy: `docs/architecture/COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md`.
**53 active commands + 1 deprecated alias.** Shapes: WF = workflow · CAP = capability · NAV = navigation · ORC = orchestrator · MNT = maintenance · ARG noted where argument workflows exist.

| ID | Command | Category | Phase | Purpose | Usually follows | Usually next | Auto-run? | Hidden? | Shape |
|---|---|---|---|---|---|---|---|---|---|
| W0.1 | `/bequite` | setup/entry | P0 | gate-aware menu + next 3 | (entry) | per menu | yes | no | NAV/WF |
| W0.2 | `/bq-init` | setup | P0 | initialize memory | /bequite | W0.5 mode / W0.3 | yes | no | WF |
| W0.3 | `/bq-discover` | setup | P0 | inspect repo | init | W0.4 doctor | yes | no | WF |
| W0.4 | `/bq-doctor` | setup | P0 | env health check | discover | W1.1 clarify | yes | no | WF |
| W0.5 | `/bq-mode` | setup | P0 | select workflow mode | init | per mode | yes | no | WF |
| W0.6 | `/bq-new` | setup | P0 | start new project | init | W0.3 | yes | no | WF |
| W0.7 | `/bq-existing` | setup | P0 | start existing-audit | init | W0.3 | yes | no | WF |
| W1.1 | `/bq-clarify` | framing | P1 | 3–5 high-value questions | doctor | W1.2 research | no (needs user) | no | WF |
| W1.2 | `/bq-research` | framing | P1 | 11-dim verified evidence | clarify | W1.3 scope | yes | no | WF |
| W1.3 | `/bq-scope` | framing | P1 | lock in/out/non-goals | research | W1.4 plan | yes | no | WF · ARG `from-interview`, `intake` |
| W1.4 | `/bq-plan` | framing | P1 | implementation plan + file map | scope | W2.1 assign | yes | no | WF · ARG `from-issues`, `delegate` |
| W1.5 | `/bq-spec` | framing | P1 | one-page Spec Kit spec | scope | W1.4 plan | yes | no | WF |
| W1.6 | `/bq-multi-plan` | framing | P1 | multi-model planning (paste) | plan | W2.1 | no (manual paste) | no | WF |
| W2.1 | `/bq-assign` | build | P2 | atomic task list | plan | W2.2 implement | yes | no | WF · ARG `delegate` |
| W2.2 | `/bq-implement` | build | P2 | one task at a time | assign | W3.1 test | yes | no | WF |
| W2.3 | `/bq-feature` | build | P2 | add-feature mini-cycle | plan | W3.1 test | yes | no | WF · ARG `demo-data` |
| W2.4 | `/bq-fix` | build | P2 | reproduce-first fix | (bug) | W4.1 verify | yes | no | WF |
| W2.5 | `/bq-uiux-variants` | build/UI | P2 | 1–10 design directions | plan | gate-16 winner pick | partial (gate 16) | no | WF |
| W2.6 | `/bq-live-edit` | build/UI | P2 | section-by-section UI edits | (running FE) | W4.1 verify | yes | no | WF |
| W3.1 | `/bq-test` | quality | P3 | run + write tests | implement | W3.3 review | yes | no | WF · ARG `from-spec`, `fixtures` |
| W3.2 | `/bq-audit` | quality | P3 | full project audit | discover/test | W3.3 review | yes | no | WF · ARG `client` |
| W3.3 | `/bq-review` | quality | P3 | spec-then-quality diff review | test | W4.1 verify | yes | no | WF · ARG `delegate`, `persona` |
| W3.4 | `/bq-red-team` | quality | P3 | 10-angle adversarial review | review | W4.1 verify | yes | no | WF |
| W4.1 | `/bq-verify` | release | P4 | full local verification | review | W4.2 release | yes | no | WF · ARG `regressions`, `drift` |
| W4.2 | `/bq-release` | release | P4 | release prep (never pushes) | verify | W4.3 + user push (gate 17) | partial (gate 17) | no | WF · ARG `readiness`, `announce`, `proof`, `demo-video` (launch-video/demo-script profiles); `template` approved V2 |
| W4.3 | `/bq-changelog` | release | P4 | changelog entry | verify | W4.2 | yes | no | WF |
| W5.1 | `/bq-memory` | memory | P5 | snapshot / inspect memory | release | W5.3 handoff | yes | no | WF |
| W5.2 | `/bq-recover` | memory | P5 | resume after break | (new session) | per checkpoint | yes | no | WF |
| W5.3 | `/bq-handoff` | memory | P5 | handoff package | memory | done | yes | no | WF · ARG `client` |
| N1 | `/bq-now` | navigation | any | one-line status | any | per status | yes | no | NAV |
| N2 | `/bq-help` | navigation | any | full reference | any | per need | yes | no | NAV |
| N3 | `/bq-explain` | navigation | any | plain-English explainer | any | — | yes | no | NAV |
| N4 | `/bq-suggest` | navigation | any | **main navigation assistant** (commands + skills + mode + gates + confidence) | any | per advice | yes | no | NAV |
| O1–O6 | `/bq-p0`…`/bq-p5` | orchestrator | P0–P5 | walk one phase in order | prior phase | next phase | yes (per-phase gates) | no | ORC |
| O7 | `/bq-auto` | orchestrator | all | scoped autonomous runner (17 intents) | any | per intent | yes (17 hard gates) | no | ORC |
| C1 | `/bq-presentation` | capability | any | premium PPTX/HTML decks | (content need) | W4.1 if built | yes (variant gate) | no | CAP |
| C2 | `/bq-writing-dna` | capability | any | reusable writing profile | (writing need) | C1 / C5 / C8 | yes | no | CAP |
| C3 | `/bq-reference` | capability | any | inspiration → design extraction + clone-safe rebuild blueprint | (visual ref) | W2.5 / W2.3 | yes | no | CAP (alpha.22) |
| C4 | `/bq-knowledge` | capability | any | docs → knowledge pack / FAQ / RAG blueprint | (docs exist) | C5 / export | yes | no | CAP (alpha.22) · modes `build/ask/rag-plan/export` |
| C5 | `/bq-course` | capability | any | Course Engine — validation → curriculum → launch | (course idea) | C1 slides / C4 | yes | no | CAP (alpha.22) |
| C6 | `/bq-pain-radar` | capability | any | public pain mining → product/service/course ideas | (niche idea) | C10 / C8 / C5 | yes | no | CAP (alpha.22) |
| C7 | `/bq-integrate` | capability | any | API docs → integration blueprint | (API need) | W2.3 feature | yes | no | CAP (alpha.22) |
| C8 | `/bq-proposal` | capability | any | job post → honest tailored proposal | C9 / C6 | (user sends) | yes | no | CAP (alpha.22) |
| C9 | `/bq-job-finder` | capability | any | real work opportunities | (profile) | C8 proposal | yes | no | CAP |
| C10 | `/bq-make-money` | capability | any | legitimate earning tracks | (profile) | C6 / C8 | yes | no | CAP |
| C11 | `/bq-offer` | capability | any | idea/niche/pain → sellable productized offer (12-file pack; no overpromise, no fake income claims) | C6 / C10 / C8 / C5 / user idea | C8 proposal / W4.2 proof / C1 / C2 / W1.3 intake / W2.3 landing | yes | no | CAP (alpha.23) · ARG `refine`, `lang=` |
| M1 | `/bq-update` | maintenance | any | self-update from source | (new release) | W0.4 doctor | yes (backup-gated) | no | MNT |
| M2 | `/bq-skill-audit` | maintenance | any | skill-pack quality audit | (drift sign) | fixes on approval | yes (report-only) | no | MNT |
| X1 | `/bq-add-feature` | deprecated | — | alias → W2.3 `/bq-feature` | — | — | — | listed as deprecated | alias |

**Proposed only (not built):** `/bq-localize` — localization/RTL is skill-first (`bequite-localization-rtl`, auto-attached); command added only if demand proves it.
