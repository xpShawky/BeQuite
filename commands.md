# BeQuite commands (v1)

55 commands in three packs (core, studio, business). Each command is a markdown playbook in `.claude/commands/`; run it in Claude Code as `/<name>`. Catalog IDs: `.bequite/commands/COMMAND_ID_MAP.md` (in the BeQuite repo: `templates/bequite/commands/COMMAND_ID_MAP.md`).

## How every command behaves

Every action command follows the same contract (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):

1. **Up to date:** it first runs the update check (`.claude/bequite/bin/bq-update.sh`, at most once an hour) and updates BeQuite when a newer version is published.
2. **Skills first:** it announces the skills it selected and why, before doing anything.
3. **Resolve the work:** it uses the active work folder (`.bequite/ACTIVE.md` → `.bequite/work/<id>/`) or creates a new one for new work.
4. **Gates:** project gates (`.bequite/state/WORKFLOW_GATES.md`) and work gates (`work/<id>/gates.md`); a missing gate stops the command and names the prerequisite.
5. **Plan first:** non-trivial work gets a plan you approve before output. Hard human gates (destructive ops, production, secrets, paid services, releases, and for films the script / style / render plan) always wait for your yes.
6. **Evidence:** every check is recorded with command + exit code + output, or marked `UNVERIFIED:`.
7. **Write back** to the work log and project memory, then **recommend the next commands**.

## Operating modes (any command)

| Mode | Use when | Research | Testing | Output |
|---|---|---|---|---|
| `deep` | quality matters most (new products, regulated, production-bound) | full 11 dimensions + red-team | full | full reports |
| `fast` | small, well-understood changes | 3 dimensions, reuse memory | still runs existing tests and verify | short |
| `token-saver` (alias `lean`) | long sessions, context cost matters | reuse cached research | targeted | compact |
| `delegate` | a strong model plans and reviews, a cheaper model implements | per task pack | strong-model review of the diff | task pack + review report |

Combine them (`/bq-auto deep delegate "..."`). If two conflict (deep + fast), BeQuite explains and picks deep for quality-critical work, fast for small scoped work. Modes never skip hard gates.

---

## W0 Setup

| ID | Command | What it does |
|---|---|---|
| W0.1 | `/bequite` · `/bequite short` | menu: state, active work, gates, next recommended commands · `short` = one line |
| W0.2 | `/bq-init` | create the `.bequite/` memory in this project |
| W0.3 | `/bq-discover` | inspect the repo → `DISCOVERY_REPORT.md` |
| W0.4 | `/bq-doctor` | environment health check |
| W0.5 | `/bq-mode` | pick a workflow mode (New Project, Existing Audit, Add Feature, Fix, Research Only, Release Readiness) |
| W0.6 | `/bq-new` | start a new project |
| W0.7 | `/bq-existing` | start an existing-project audit |
| W0.8 | `/bq-work new "<title>" [type=…]` · `list` · `switch <id>` · `status` · `close` | work folders; `close` = converge → merge spec deltas → archive |

## W1 Framing

| ID | Command | What it does |
|---|---|---|
| W1.1 | `/bq-clarify` | 3–5 high-value questions → the work's `brief.md` |
| W1.2 | `/bq-research [deep\|fast]` | verified research with sources → `research.md` |
| W1.3 | `/bq-scope` (`from-interview`, `intake`) | lock in / out / non-goals → `spec.md` |
| W1.4 | `/bq-plan` (`from-issues`, `migration`, `delegate`) | the plan + file-responsibility map + per-phase profile → `plan.md` |
| W1.5 | `/bq-spec "<idea>" [export=speckit]` | one-page spec in the work (optional Spec Kit export) |
| W1.6 | `/bq-multi-plan` | independent plans from other models (manual paste), merged |

## W2 Build

| ID | Command | What it does |
|---|---|---|
| W2.1 | `/bq-assign` (`delegate`) | atomic tasks with waves, skills, model / effort / confidence → `tasks.md` |
| W2.2 | `/bq-implement` | one task at a time, verified before the next |
| W2.3 | `/bq-feature "<title>"` (`demo-data`, `landing`) | add-feature mini-cycle in its own work folder |
| W2.4 | `/bq-fix "<symptom>"` | reproduce → root cause → smallest patch → regression test |
| W2.5 | `/bq-uiux-variants [N] "<task>"` | 1–10 isolated design directions; you pick the winner |
| W2.6 | `/bq-live-edit "<task>"` | section-by-section UI edits with browser checks (built-in browser pane → your browser → scripted → computer use) |

## W3 Quality

| ID | Command | What it does |
|---|---|---|
| W3.1 | `/bq-test` (`from-spec`, `fixtures`) | run and write tests |
| W3.2 | `/bq-audit` (`client`, `a11y`) | full project audit |
| W3.3 | `/bq-review` (`delegate`, `persona`) | spec compliance first, then quality, plus Guard Pass |
| W3.4 | `/bq-red-team` | adversarial review |

## W4 Release

| ID | Command | What it does |
|---|---|---|
| W4.1 | `/bq-verify` (`regressions`, `drift`) | full verification + converge check (incl. design continuity and web performance when relevant) |
| W4.2 | `/bq-release` (`readiness`, `announce`, `proof`, `demo-video`, `template`) | release prep; prints git commands, never pushes |
| W4.3 | `/bq-changelog` | changelog entry from recent work |

## W5 Memory

| ID | Command | What it does |
|---|---|---|
| W5.1 | `/bq-memory` | inspect or snapshot memory |
| W5.2 | `/bq-recover` | resume after a break |
| W5.3 | `/bq-handoff` (`client`, `workflow-export`) | handoff package |

## N Navigation · O Orchestrator

| ID | Command | What it does |
|---|---|---|
| N2 | `/bq-help` | full reference |
| N3 | `/bq-explain "<target>"` | plain-English explanation of a file, decision or artifact |
| N4 | `/bq-suggest "<situation>"` | the navigation assistant: which commands, skills and mode fit your goal |
| O7 | `/bq-auto [intent] [mode] "<task>"` · `/bq-auto phase=P0..P5` | autonomous runner (18 intents incl. `motion`); stops only at hard gates; creative work stops at the plan |

`/bq-auto` intents: `new` `existing` `feature` `fix` `uiux` `frontend` `backend` `database` `security` `testing` `devops` `scraping` `automation` `deploy` `live-edit` `variants` `release` `motion`.

## C Capabilities

Folded in v1: the ten small capability commands are now modes of `/bq-knowledge`, `/bq-content` and `/bq-offer` (the old names move to `.bequite/backups/` on update).

### core

| ID | Command | What it does |
|---|---|---|
| C2 | `/bq-writing-dna <request>` | a voice learned from real samples; write in it, checked by a blind pick |
| C4 | `/bq-knowledge build\|ask\|rag-plan\|export "<docs>"` | knowledge pack, FAQ, grounded Q&A, retrieval blueprint |
| C3 | `/bq-knowledge reference screenshot\|url\|flow "<goal>"` | design extraction + an original, clone-safe rebuild blueprint |
| C7 | `/bq-knowledge integrate "<API docs>"` | integration blueprint (auth, endpoints, errors, retries, tests) |
| C12 | `/bq-knowledge automation "<workflow>"` · `bot` · `workflow` | tool-neutral automation blueprint (official API first) |
| C16 | `/bq-knowledge recording "<video \| transcript>"` | a long video or meeting into structured knowledge |
| C23 | `/bq-team init\|ask\|beat\|board\|approve\|decline\|schedule\|status` | command center in a folder: role agents on heartbeats, budgets, an editor that can reject, approvals before any post or spend |
| C24 | `/bq-operator options\|setup\|check\|start\|audit` | text your own computer from Telegram: allow-listed bot, read-only runs, Approve/Decline for changes, audit log |

### studio

| ID | Command | What it does |
|---|---|---|
| C1 | `/bq-presentation <request>` (`format=pptx\|html\|both`, `variants=N`, `strict=true`) | decks from studied references |
| C18 | `/bq-motion "<idea>"` · `M<n>` · `study <path>` · `lab <technique>` · `recut <platform>` · `post` · `status` | direct a film: references, script, style, render plan, build, sound, QC, recuts, posts |
| C19 | `/bq-content radar\|study\|script\|produce\|package\|queue\|from-work` | the content studio: from what is moving to a packaged draft that waits for your yes |
| C5 | `/bq-content course "<idea>"` (`validate`, `curriculum`, `launch`) | a course from validation to launch |
| C14 | `/bq-content brand-kit "<niche + audience>"` | a non-generic brand identity |
| C15 | `/bq-content community "<who + purpose>"` | a community plan |
| C20 | `/bq-watch "<video>"` (`breakdown`, `steps`, `claims`, `measure`, `test`) | watch a video at the lowest cost that answers the question |
| C21 | `/bq-dna "<niche>"` (`shorts`, `reels`, `tiktok`, `long`) | the format sheet of a niche's top five outliers |

### business

| ID | Command | What it does |
|---|---|---|
| C11 | `/bq-offer "<idea>"` (`refine`, `business-system`, `agency`, `service-business`) | an honest, sellable offer pack |
| C6 | `/bq-offer pain-radar "<niche>" [country=…]` | public pain into ranked opportunities |
| C8 | `/bq-offer proposal "<job post>"` | a tailored, honest proposal |
| C13 | `/bq-offer local-business "<business>"` | a minimum digital system for an offline business |
| C9 | `/bq-job-finder [worldwide_hidden=true]` | real work opportunities, scam-checked |
| C10 | `/bq-make-money [track=…]` | legitimate earning routes checked for your country |
| C17 | `/bq-start "<what you want to start>"` | choose how to start |
| C22 | `/bq-productize <work-id>` | finished work into a sellable asset, built from its own evidence |

## M Maintenance

| ID | Command | What it does |
|---|---|---|
| M1 | `/bq-update` (`check`, `source=local path=…`) | update BeQuite by hand; every command already checks automatically; never touches project memory |
| M2 | `/bq-skill-audit` | skill-pack quality audit |
| M3 | `/bq-hooks status\|enable\|disable\|test` | opt-in safety hooks (off by default) |
| M4 | `/bq-budget set\|status\|log\|report` | a credit budget per work; stops at the ceiling |
| M5 | `/bq-taste review\|add\|list` | your corrections become DNA rules (saved only on your yes) |
| M6 | `/bq-forge propose\|use\|status\|promote` | a proven procedure becomes a skill after three evidenced uses |
| M7 | `/bq-eval run\|add\|list\|compare` | scenarios per skill; a regression blocks the release |
