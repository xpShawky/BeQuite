# BeQuite Orchestration Map — source of truth (alpha.22 orchestration update)

**When confused, conflicted, or capability-missing: come HERE first.** This is the compact brain index — one-liners + pointers; details live in the canonical files named. Model doc: `docs/architecture/BEQUITE_ORCHESTRATION_MODEL.md`. Used by: bequite · suggest · discover · plan · auto · implement · review · verify · skill-audit (+ both routers on conflict).

## 1–5. Commands (52 active + 1 alias — full map: `.bequite/commands/COMMAND_ID_MAP.md`)

- **W0 setup:** bequite(menu) · init · discover · doctor · mode · new · existing
- **W1 framing:** clarify · research · scope(+from-interview,intake) · plan(+from-issues,migration,delegate) · spec · multi-plan
- **W2 build:** assign(+delegate) · implement · feature(+demo-data) · fix · uiux-variants(+style=) · live-edit
- **W3 quality:** test(+from-spec,fixtures) · audit(+client,a11y) · review(+delegate,persona) · red-team
- **W4 release:** verify(+regressions,drift) · release(+readiness,announce,proof,demo-video) · changelog
- **W5 memory:** memory · recover · handoff(+client)
- **N navigation:** now · help · explain · suggest(MAIN navigation assistant)
- **O orchestrators:** p0–p5 · auto(17 intents; 15-step sequence)
- **C capabilities:** presentation · writing-dna · reference · knowledge · course · pain-radar · integrate · proposal · job-finder · make-money (C11 offer = queued, NOT built)
- **M maintenance:** update · skill-audit · **X:** add-feature(deprecated→feature)

**Near-miss boundaries (conflict killers):** audit=whole-project vs review=diff · spec=one-pager vs scope=boundaries vs plan=blueprint · now=1-line vs bequite=menu vs suggest=advisor · pain-radar=find problems vs make-money=find earning tracks · proposal=per-client vs offer(future)=standing package · verify="does it work" vs release readiness="should it ship".

## 6. Skills (30 — registry: `.bequite/skills/SKILL_REGISTRY.md`, router: `SKILL_ROUTER.md`)

orchestrator(this brain) · context-engineer(persisted context) · anti-hallucination(evidence-or-UNVERIFIED) · guard-pass(post-work AI-failure gates) · frontier-reasoning-coach(discipline for any model) · researcher(11-dim evidence) · project-architect(stack/ADR) · product-strategist(JTBD/MVP/pricing) · backend-architect · database-architect · security-reviewer(OWASP/supply-chain) · devops-cloud · testing-gate · release-gate · problem-solver(reproduce-first) · frontend-design-system(MASTER: Design DNA/continuity) · ux-ui-designer · frontend-quality(slop detection) · live-edit · localization-rtl(Arabic/MENA/RTL auto-attach) · scraping-automation(Article VIII, API-first) · presentation-builder · writing-dna · multi-model-planning · delegate-planner(strong plans/cheap implements/strong reviews) · workflow-advisor(suggest engine) · skill-auditor · updater · job-finder · make-money

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

**Maintainer rule:** command/skill/rule changes update this map in the same commit (drift-checked by `/bq-verify drift` + skill-audit).
