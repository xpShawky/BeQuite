# BeQuite Orchestration Map: source of truth (v1)

**When confused, conflicted, or a capability is missing: come here first.** A compact index of one-liners and pointers; details live in the files named. Model doc: `.claude/bequite/docs/architecture/BEQUITE_ORCHESTRATION_MODEL.md`. Used by: bequite, suggest, discover, plan, auto, implement, review, verify, skill-audit (and both routers on a conflict).

## 1-5. Commands (51 in three packs; full map: `.bequite/commands/COMMAND_ID_MAP.md`)

- **W0 setup:** bequite (update check + menu) · init · discover · doctor · mode · new · existing · work
- **W1 framing:** clarify · research · scope (+from-interview, intake) · plan (+from-issues, delegate) · spec · multi-plan
- **W2 build:** assign (+delegate) · implement · feature (+demo-data) · fix · uiux-variants · live-edit
- **W3 quality:** test (+from-spec, fixtures) · audit (+client) · review (+delegate, persona) · red-team
- **W4 release:** verify (+regressions, drift) · release (+readiness, announce, proof, demo-video) · changelog
- **W5 memory:** memory · recover · handoff (+client)
- **N navigation:** help · explain · suggest (main navigation assistant)
- **O orchestrator:** auto (intents incl. `motion`; `phase=P0..P5`)
- **C core capabilities:** writing-dna · knowledge (build, ask, rag-plan, export, recording, reference, integrate, automation) · team (command center) · operator (Telegram)
- **C studio:** presentation · motion · content (radar, study, script, produce, package, queue, from-work, brand-kit, community, course) · watch · dna
- **C business:** offer (offer, proposal, local-business, pain-radar, business-system) · make-money · job-finder · start · productize
- **M maintenance:** update (also automatic at every command) · skill-audit · hooks

**Near-miss boundaries (conflict killers):** audit = whole project vs review = a diff · spec = one page vs scope = boundaries vs plan = blueprint · bequite = menu vs suggest = advisor · offer pain-radar = find problems vs make-money = find earning routes · offer proposal = one client vs offer = a standing package · content = one piece vs team = a standing team · watch = one video vs dna = a niche's format · verify = does it work vs release readiness = should it ship.

## 6. Skills (38 in three packs; registry: `.bequite/skills/SKILL_REGISTRY.md`, router: `SKILL_ROUTER.md`)

**core:** orchestrator (routes, operating card, subagent cost rule) · context-engineer · anti-hallucination · guard-pass · researcher · project-architect · product-strategist · backend-architect · database-architect · security-reviewer · devops-cloud · testing-gate · release-gate · problem-solver · frontend-design-system (master) · ux-ui-designer · frontend-quality · live-edit · localization-rtl (auto-attach) · automation (official API first, Scrapling default) · delegation (strong plans, cheap builds, second plans) · writing-dna · human-taste (reference-first, the human test) · agent-team · skill-auditor · updater
**studio:** motion-director · kinetic-type (BQ Kinetic engine) · sound-voice · render-pipeline · presentation-builder · video-intel · trend-radar · format-dna · hooks-and-copy · publish-prep
**business:** make-money · job-finder

## 7. Auto Mode rules → `.bequite/state/AUTO_MODE_RULES.md`
15-step anti-skip sequence; `Not applicable — reason:` / `Blocked — reason:` markings; 17 hard gates unchanged; stop/ask/continue/compact rules.

## 8. Command Router rules → `.bequite/commands/COMMAND_ROUTER.md`
Gate-aware spine + signal tables + journey routes; output = Required next + 2–6 set + accelerators + do-not-run-yet; auto reports `Internal workflow executed: <IDs>`.

## 9. Skill Router rules → `.bequite/skills/SKILL_ROUTER.md`
Domain map + mode sizing (fast=smallest safe · deep=broader · token-saver=lazy · delegate=pack-named); user never names skills; explicit user choice overrides.

## 10. Context compaction → `.bequite/state/CONTEXT_COMPACTION_RULES.md`
~40% summary · ~60% externalize · ~75% no new tasks · ~85% handoff; Context Compact format; facts live in files, never chat-only.

## 11. System design risk → `.claude/bequite/docs/architecture/SYSTEM_DESIGN_REASONING_STANDARD.md`
Mandatory block for payments/inventory/bookings/auth/permissions/db-writes/concurrency/queues/APIs/webhooks/uploads/UGC/admin/prod/security; domain risk libraries; risk-without-test = wish.

## 12. Missing capability detection
No fitting command/skill ⇒ emit `Missing Capability Detected:` block (needed · why existing isn't enough · workaround · recommended build · now-or-park · confidence) → log to OPEN_QUESTIONS/roadmap → workaround only if safe. Never pretend coverage.

## 13. Next-command recommendation rules
Contract step 12 (`COMMAND_EXECUTION_CONTRACT.md`); IDs are the shared vocabulary; capability suggestions only on task signals; gates never bypassed, blocked items appear under do-not-run-yet with the gate named.

## 16. Work folders + motion (v4)
Every piece of work lives in `.bequite/work/NNNN-slug/` (brief · research · spec · plan · tasks · gates · evidence · review · verify · log); `ACTIVE.md` points at it; gates are per work; `/bq-work close` converges, merges spec deltas into `.bequite/specs/` and archives. Spec: `.claude/bequite/docs/architecture/WORK_FOLDERS.md`. Video/film requests route to C18 `/bq-motion` (skills motion-director + kinetic-type + sound-voice + render-pipeline); website motion routes to frontend-design-system `web-motion.md` (PERF_BUDGET_PASS). Creative work is plan-first even in auto mode.

## 15. Skills-first + execution profile + post-phase verify (alpha.25)
Every command (workflow + capability + maintenance; trivial reads exempt) announces its `Skill Selection:` block BEFORE acting. `/bq-plan` records skills per phase; `/bq-assign` records per task + an Execution Profile (recommended model+tier · effort · confidence — `.claude/bequite/docs/architecture/TASK_EXECUTION_PROFILE.md`). `/bq-discover`+`/bq-research` may recommend a VERIFIED external skill on a real gap (user-approved install only). After each phase/task: select verification skills + run tests/verify with evidence before advancing (failure → `/bq-fix`). BeQuite recommends models, never switches them.

**Maintainer rule:** command/skill/rule changes update this map in the same commit (drift-checked by `/bq-verify drift` + skill-audit).

## 14. Remaining-work source of truth

All "what remains / what's next / what's parked / what's alpha.23 / built-but-untested" questions are answered from `.bequite/tasks/REMAINING_WORK_MASTER.md` (sections: A built-untested · B maintenance · C alpha.23 /bq-offer · D V1 arguments · E V2 parked · F rejected · G recently completed). Never from memory alone. Wired into: bequite · now · suggest · recover · memory · skill-audit.
