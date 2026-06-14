# BeQuite Orchestration Map — source of truth (alpha.22 orchestration update)

**When confused, conflicted, or capability-missing: come HERE first.** This is the compact brain index — one-liners + pointers; details live in the canonical files named. Model doc: `docs/architecture/BEQUITE_ORCHESTRATION_MODEL.md`. Used by: bequite · suggest · discover · plan · auto · implement · review · verify · skill-audit (+ both routers on conflict).

## 1–5. Commands (60 active + 1 alias — full map: `.bequite/commands/COMMAND_ID_MAP.md`)

- **W0 setup:** bequite(menu) · init · discover · doctor · mode · new · existing
- **W1 framing:** clarify · research · scope(+from-interview,intake) · plan(+from-issues,migration,delegate) · spec · multi-plan
- **W2 build:** assign(+delegate) · implement · feature(+demo-data) · fix · uiux-variants(+style=) · live-edit
- **W3 quality:** test(+from-spec,fixtures) · audit(+client,a11y) · review(+delegate,persona) · red-team
- **W4 release:** verify(+regressions,drift) · release(+readiness,announce,proof,demo-video) · changelog
- **W5 memory:** memory · recover · handoff(+client)
- **N navigation:** now · help · explain · suggest(MAIN navigation assistant)
- **O orchestrators:** p0–p5 · auto(17 intents; 15-step sequence)
- **C capabilities:** presentation · writing-dna · reference · knowledge · course · pain-radar · integrate · proposal · job-finder · make-money · offer(C11) · automation(C12) · local-business(C13) · brand-kit(C14) · community(C15) · recording(C16) · start(C17) — C11-C17 built alpha.23/24, not live-tested
- **M maintenance:** update · skill-audit · hooks(M3, opt-in safety hooks: status/enable/disable/test) · **X:** add-feature(deprecated→feature)

**Near-miss boundaries (conflict killers):** audit=whole-project vs review=diff · spec=one-pager vs scope=boundaries vs plan=blueprint · now=1-line vs bequite=menu vs suggest=advisor · pain-radar=find problems vs make-money=find earning tracks · proposal=per-client pitch vs offer=standing productized package · verify="does it work" vs release readiness="should it ship".

## 6. Skills (31 — registry: `.bequite/skills/SKILL_REGISTRY.md`, router: `SKILL_ROUTER.md`)

orchestrator(this brain) · automation-engineer(tool-neutral automation+bots) · context-engineer(persisted context) · anti-hallucination(evidence-or-UNVERIFIED) · guard-pass(post-work AI-failure gates) · frontier-reasoning-coach(discipline for any model) · researcher(11-dim evidence) · project-architect(stack/ADR) · product-strategist(JTBD/MVP/pricing) · backend-architect · database-architect · security-reviewer(OWASP/supply-chain) · devops-cloud · testing-gate · release-gate · problem-solver(reproduce-first) · frontend-design-system(MASTER: Design DNA/continuity) · ux-ui-designer · frontend-quality(slop detection) · live-edit · localization-rtl(Arabic/MENA/RTL auto-attach) · scraping-automation(Article VIII, API-first) · presentation-builder · writing-dna · multi-model-planning · delegate-planner(strong plans/cheap implements/strong reviews) · workflow-advisor(suggest engine) · skill-auditor · updater · job-finder · make-money

## 7. Auto Mode rules → `.bequite/state/AUTO_MODE_RULES.md`
15-step anti-skip sequence; `Not applicable — reason:` / `Blocked — reason:` markings; 17 hard gates unchanged; stop/ask/continue/compact rules.

## 8. Command Router rules → `.bequite/commands/COMMAND_ROUTER.md`
Gate-aware spine + signal tables + journey routes; output = Required next + 2–6 set + accelerators + do-not-run-yet; auto reports `Internal workflow executed: <IDs>`.

## 9. Skill Router rules → `.bequite/skills/SKILL_ROUTER.md`
Domain map + mode sizing (fast=smallest safe · deep=broader · token-saver=lazy · delegate=pack-named); user never names skills; explicit user choice overrides.

## 10. Context compaction → `.bequite/state/CONTEXT_COMPACTION_RULES.md`
~40% summary · ~60% externalize · ~75% no new tasks · ~85% handoff; Context Compact format; facts live in files, never chat-only.

## 11. System design risk → `docs/architecture/SYSTEM_DESIGN_REASONING_STANDARD.md`
Mandatory block for payments/inventory/bookings/auth/permissions/db-writes/concurrency/queues/APIs/webhooks/uploads/UGC/admin/prod/security; domain risk libraries; risk-without-test = wish.

## 12. Missing capability detection
No fitting command/skill ⇒ emit `Missing Capability Detected:` block (needed · why existing isn't enough · workaround · recommended build · now-or-park · confidence) → log to OPEN_QUESTIONS/roadmap → workaround only if safe. Never pretend coverage.

## 13. Next-command recommendation rules
Contract step 12 (`COMMAND_EXECUTION_CONTRACT.md`); IDs are the shared vocabulary; capability suggestions only on task signals; gates never bypassed, blocked items appear under do-not-run-yet with the gate named.

## 15. Skills-first + execution profile + post-phase verify (alpha.25)
Every command (workflow + capability + maintenance; trivial reads exempt) announces its `Skill Selection:` block BEFORE acting. `/bq-plan` records skills per phase; `/bq-assign` records per task + an Execution Profile (recommended model+tier · effort · confidence — `docs/architecture/TASK_EXECUTION_PROFILE.md`). `/bq-discover`+`/bq-research` may recommend a VERIFIED external skill on a real gap (user-approved install only). After each phase/task: select verification skills + run tests/verify with evidence before advancing (failure → `/bq-fix`). BeQuite recommends models, never switches them.

**Maintainer rule:** command/skill/rule changes update this map in the same commit (drift-checked by `/bq-verify drift` + skill-audit).

## 14. Remaining-work source of truth

All "what remains / what's next / what's parked / what's alpha.23 / built-but-untested" questions are answered from `.bequite/tasks/REMAINING_WORK_MASTER.md` (sections: A built-untested · B maintenance · C alpha.23 /bq-offer · D V1 arguments · E V2 parked · F rejected · G recently completed). Never from memory alone. Wired into: bequite · now · suggest · recover · memory · skill-audit.
