# BeQuite Command ID Map (canonical, v5)

Display-only catalog IDs (files are never renamed). Strategy: `.claude/bequite/docs/architecture/COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md`.
**53 commands** in three packs: core 43 · studio 5 · business 5. Shapes: WF workflow · CAP capability · NAV navigation · ORC orchestrator · MNT maintenance; ARG marks argument modes. Folded commands live on as modes (rows with a `·` after the parent).

| ID | Command | Pack | Category | Phase | Purpose | Usually next | Auto-run? | Shape |
|---|---|---|---|---|---|---|---|---|
| W0.1 | `/bequite` | core | setup/entry | P0 | update check + gate-aware menu + next 3 | per menu | yes | NAV/WF |
| W0.2 | `/bq-init` | core | setup | P0 | initialize memory | W0.5 mode | yes | WF |
| W0.3 | `/bq-discover` | core | setup | P0 | inspect repo | W0.4 doctor | yes | WF |
| W0.4 | `/bq-doctor` | core | setup | P0 | environment health check | W1.1 clarify | yes | WF |
| W0.5 | `/bq-mode` | core | setup | P0 | select workflow mode | per mode | yes | WF |
| W0.8 | `/bq-work` | core | setup | any | work folders: new / list / switch / status / close | W1.1 / C18 | yes | WF |
| W1.1 | `/bq-clarify` | core | framing | P1 | 3-5 high-value questions | W1.2 research | no (needs user) | WF |
| W1.2 | `/bq-research` | core | framing | P1 | verified evidence | W1.3 scope | yes | WF |
| W1.3 | `/bq-scope` | core | framing | P1 | lock in / out / non-goals | W1.4 plan | yes | WF · ARG `from-interview`, `intake` |
| W1.4 | `/bq-plan` | core | framing | P1 | implementation plan + file map | W2.1 assign | yes | WF · ARG `from-issues`, `delegate` |
| W1.5 | `/bq-spec` | core | framing | P1 | one-page spec | W1.4 plan | yes | WF |
| W1.6 | `/bq-multi-plan` | core | framing | P1 | independent plans from other models (paste) | W2.1 | no (manual paste) | WF |
| W2.1 | `/bq-assign` | core | build | P2 | atomic task list | W2.2 implement | yes | WF · ARG `delegate` |
| W2.2 | `/bq-implement` | core | build | P2 | one task at a time | W3.1 test | yes | WF |
| W2.3 | `/bq-feature` | core | build | P2 | add-feature mini-cycle | W3.1 test | yes | WF · ARG `demo-data` |
| W2.4 | `/bq-fix` | core | build | P2 | reproduce-first fix | W4.1 verify | yes | WF |
| W2.5 | `/bq-uiux-variants` | core | build/UI | P2 | 1-10 design directions | winner pick (gate) | partial | WF |
| W2.6 | `/bq-live-edit` | core | build/UI | P2 | measured section edits in a real browser | W4.1 verify | yes | WF |
| W3.1 | `/bq-test` | core | quality | P3 | run + write tests | W3.3 review | yes | WF · ARG `from-spec`, `fixtures` |
| W3.2 | `/bq-audit` | core | quality | P3 | full project audit | W3.3 review | yes | WF · ARG `client` |
| W3.3 | `/bq-review` | core | quality | P3 | spec-then-quality diff review | W4.1 verify | yes | WF · ARG `delegate`, `persona` |
| W3.4 | `/bq-red-team` | core | quality | P3 | adversarial review | W4.1 verify | yes | WF |
| W4.1 | `/bq-verify` | core | release | P4 | full local verification | W4.2 release | yes | WF · ARG `regressions`, `drift` |
| W4.2 | `/bq-release` | core | release | P4 | release prep (never pushes) | user push (gate) | partial | WF · ARG `readiness`, `announce`, `proof`, `demo-video` |
| W4.3 | `/bq-changelog` | core | release | P4 | changelog entry | W4.2 | yes | WF |
| W5.1 | `/bq-memory` | core | memory | P5 | snapshot / inspect memory | W5.3 handoff | yes | WF |
| W5.2 | `/bq-recover` | core | memory | P5 | resume after a break | per checkpoint | yes | WF |
| W5.3 | `/bq-handoff` | core | memory | P5 | hand-off package | done | yes | WF · ARG `client` |
| N2 | `/bq-help` | core | navigation | any | full reference | per need | yes | NAV |
| N3 | `/bq-explain` | core | navigation | any | plain-language explainer | - | yes | NAV |
| N4 | `/bq-suggest` | core | navigation | any | main navigation assistant (orchestrator skill) | per advice | yes | NAV |
| O7 | `/bq-auto` | core | orchestrator | all | scoped autonomous runner | per intent | yes (hard gates stop it) | ORC |
| C2 | `/bq-writing-dna` | core | capability | any | a voice learned from real samples | C19 / C11 | yes | CAP |
| C4 | `/bq-knowledge` | core | capability | any | sources into knowledge and blueprints | per mode | yes | CAP · modes `build/ask/rag-plan/export` |
| C3 | · `/bq-knowledge reference` | core | mode | any | screenshot / URL / flow into a clone-safe design blueprint | W2.5 / W2.3 | yes | mode |
| C7 | · `/bq-knowledge integrate` | core | mode | any | API docs into an integration blueprint | W2.3 feature | yes | mode |
| C12 | · `/bq-knowledge automation` | core | mode | any | workflow or bot into a tool-neutral automation blueprint | W1.4 / W2.3 | yes | mode · ARG `bot`, `workflow` |
| C16 | · `/bq-knowledge recording` | core | mode | any | a recording into structured knowledge (transcript first) | C4 / C19 course | yes | mode |
| C23 | `/bq-team` | core | capability | any | command center in a folder: roles, heartbeats, budgets, editor, approvals | approvals | partial (owner approves publish and spend) | CAP (v5) · modes `init/ask/beat/board/approve/decline/schedule/status` |
| C24 | `/bq-operator` | core | capability | any | text your own computer from Telegram (allow-listed, read-only runs, approvals) | - | no (owner creates the bot) | CAP (v5) · modes `options/setup/check/start/audit` |
| M1 | `/bq-update` | core | maintenance | any | update BeQuite (also automatic at every command) | W0.4 doctor | yes (backup first) | MNT |
| M2 | `/bq-skill-audit` | core | maintenance | any | skill-pack quality audit | fixes on approval | yes (report only) | MNT |
| M3 | `/bq-hooks` | core | maintenance | any | manage the safety hooks | reload + test | partial | MNT |
| M4 | `/bq-budget` | core | harness | any | a credit budget per work: ceiling, model role per stage, stop at 100% | per stage | yes (raising the ceiling needs a yes) | MNT (v5) · modes `set/status/log/report` |
| M5 | `/bq-taste` | core | harness | any | the user's corrections into DNA rules, saved only on a yes | review | partial | MNT (v5) · modes `review/add/list` |
| M6 | `/bq-forge` | core | harness | any | a closing work's proven procedure into a skill candidate; promoted after 3 evidenced uses | skill-audit | partial | MNT (v5) · modes `propose/use/status/promote` |
| M7 | `/bq-eval` | core | harness | any | scenarios per skill (scripted + fast model); a regression blocks release | release | yes | MNT (v5) · modes `run/add/list/compare` |
| C1 | `/bq-presentation` | studio | capability | any | PPTX / HTML decks from references | W4.1 if built | yes (variant gate) | CAP |
| C18 | `/bq-motion` | studio | capability | any | direct a film: references, script, style, render plan, build, sound, QC, recuts | C19 package | partial (plan, credits, final render, posting) | CAP |
| C19 | `/bq-content` | studio | capability | any | the content studio: radar, study, script, produce, package, queue, from-work | approval per post | partial (owner approves each post) | CAP (v5) |
| C5 | · `/bq-content course` | studio | mode | any | a course from validation to launch | C1 slides / C4 | yes | mode · ARG `validate`, `curriculum`, `launch` |
| C14 | · `/bq-content brand-kit` | studio | mode | any | a non-generic brand identity from the niche | C3 / W2.3 landing | yes | mode |
| C15 | · `/bq-content community` | studio | mode | any | a community plan | C2 / C12 | yes | mode |
| C20 | `/bq-watch` | studio | capability | any | watch a video at the lowest cost that answers the question | C21 / C19 | yes | CAP (v5) · modes `breakdown/steps/claims/measure/test` |
| C21 | `/bq-dna` | studio | capability | any | the format sheet of a niche's top five outliers | C19 script | yes | CAP (v5) |
| C11 | `/bq-offer` | business | capability | any | an honest, sellable offer pack | C8 proposal | yes | CAP · ARG `refine`, `lang=`, `business-system`, `agency`, `service-business` |
| C6 | · `/bq-offer pain-radar` | business | mode | any | public pain into opportunities | C10 / C8 | yes | mode · ARG `from-exports` |
| C8 | · `/bq-offer proposal` | business | mode | any | a tailored, honest proposal for one client | (user sends) | yes | mode |
| C13 | · `/bq-offer local-business` | business | mode | any | an offline business into a minimum digital system | C11 / W2.3 | yes | mode |
| C9 | `/bq-job-finder` | business | capability | any | real work opportunities, scam-checked | C8 proposal | yes | CAP |
| C10 | `/bq-make-money` | business | capability | any | legitimate earning routes checked for the country | C6 / C11 | yes | CAP |
| C17 | `/bq-start` | business | capability | any | choose how to start (profile, brand, platforms, niche, career) | C14 / C5 / C11 / C9 | yes | CAP |
| C22 | `/bq-productize` | business | capability | any | finished work into a sellable asset with its evidence | C11 / C19 | yes | CAP (v5) |

Folded in v5 (modes now; the old files move to `.bequite/backups/` on update): `/bq-knowledge reference`, `integrate`, `automation`, `recording`; `/bq-content course`, `brand-kit`, `community`; `/bq-offer pain-radar`, `proposal`, `local-business`. Removed in v1: the seven phase redirects (`/bequite short` and `/bq-auto phase=P0..P5` replace them).
