# Skill Registry (v1)

> **The compact routing index over all BeQuite skills.** The Skill Router reads this first; a full SKILL.md loads only after selection. Each skill's own file is the source of truth for when to use it, its procedure and its sources; this registry holds routing metadata only.
>
> **Refreshed:** 2026-11-21 (v1 integration) · **38 skills** in three packs: core 26 · studio 10 · business 2. Refreshed by `/bq-skill-audit`; adding or removing a skill without updating this file in the same commit is a drift violation.

Legend: **Cost** (weight when loaded): L under 80 lines · M 80-150 · H has `references/` or scripts. **Risk**: L docs and advice · M writes project files · H touches security, production or money.

## Routing table

| Skill | Pack | Domains | Trigger keywords / intents | Usual commands | Pairs with | Cost | Risk |
|---|---|---|---|---|---|---|---|
| `orchestrator` | core | routing, conflicts, missing capability, subagent cost | which command, where to start, conflict, nothing fits | bequite, suggest, auto, plan, discover, implement, review, verify, skill-audit | context-engineer, all | M | L |
| `context-engineer` | core | context, memory, long tasks | multi-step, resume, compaction, lost context | plan, implement, auto, recover | all | M | L |
| `anti-hallucination` | core | evidence, claims | verify, prove, is this true, done claims, package check | review, verify, audit, red-team | all | M | L |
| `guard-pass` | core | second pass on generated work | after implementation or tests, before verify or release | implement, feature, fix, test, review, verify, release | anti-hallucination, testing-gate | M | L |
| `researcher` | core | research, sources | research, compare, what's best, competitors, versions, prices | research, plan, knowledge | all | H | L |
| `project-architect` | core | architecture, stack | stack choice, ADR, options board, scale tier | plan, research, scope | all specialists | M | M |
| `product-strategist` | core | product, scope, price | MVP, persona, job to be done, differentiation, pricing | clarify, scope, plan, offer | project-architect | M | L |
| `backend-architect` | core | server code | API, errors, retries, queues, idempotency, webhooks | plan, feature, fix, knowledge integrate | database-architect, security-reviewer | M | M |
| `database-architect` | core | data | schema, migration, index, N+1, transactions, pooling | plan, feature, fix | backend-architect | M | H |
| `security-reviewer` | core | security, agents, supply chain | auth, input, secrets, OWASP, prompt injection, MCP, CI | plan, feature, fix, audit, review, red-team | devops-cloud, anti-hallucination | M | H |
| `devops-cloud` | core | CI, deploy, infra | CI, deploy, env vars, secrets, VPS, rollback | plan, feature, verify, release | release-gate, security-reviewer | M | H |
| `testing-gate` | core | tests | test, coverage, regression, flaky, fail-first | test, feature, fix | all build skills | M | L |
| `release-gate` | core | release | version, tag, changelog, publish, ready to ship | verify, release, changelog | devops-cloud, testing-gate | M | M |
| `problem-solver` | core | debugging | bug, error, crash, regression, bisect, root cause | fix | testing-gate | M | L |
| `frontend-design-system` | core | multi-section UI | page, landing, app screen, redesign, AI-looking | feature, fix, auto, uiux-variants, live-edit, audit | ux-ui-designer, frontend-quality, live-edit | H | M |
| `ux-ui-designer` | core | design tokens | type scale, colour, spacing, states, motion, tokens | plan, feature, audit | frontend-design-system | M | L |
| `frontend-quality` | core | UI checks | AI tells, WCAG, Web Vitals, dead buttons, fake data | audit, review, verify | frontend-design-system | H | L |
| `live-edit` | core | measured UI edits | fix this section, spacing, button does nothing | live-edit, auto live-edit | frontend-design-system | M | M |
| `localization-rtl` | core | Arabic, MENA, RTL | Arabic, Egypt, RTL, bilingual | any (auto-attach) | writing-dna, human-taste | M | L |
| `automation` | core | scraping, bots, workflows | scrape, crawl, bot, webhook, schedule, n8n, Telegram | knowledge automation, offer local-business, feature | backend-architect, security-reviewer | M | M |
| `delegation` | core | strong plans, cheap builds, second plans | delegate, task pack, second opinion, parallel tracks | auto/plan/assign/review delegate, multi-plan | orchestrator | H | M |
| `writing-dna` | core | voice | write like me, posts, captions, human writing | writing-dna, content script, offer, presentation notes | human-taste, localization-rtl | H | L |
| `human-taste` | core | reference-first, the human test | not AI-looking, from references, taste | every creative command | writing-dna, frontend-design-system, motion-director | M | L |
| `agent-team` | core | standing agent team, phone operator | team, heartbeat, budget per agent, approvals, Telegram | team, operator | publish-prep, writing-dna | H | M |
| `skill-auditor` | core | pack health | skill audit, stale skills, sources | skill-audit | anti-hallucination | M | L |
| `updater` | core | BeQuite updates | update BeQuite | update | - | M | M |
| `motion-director` | studio | films, promos, ads, reels | video, film, promo, ad, reel, trailer, like the Apple ad | motion, auto motion | kinetic-type, sound-voice, render-pipeline | H | M |
| `kinetic-type` | studio | moving type; BQ Kinetic engine | kinetic typography, text animation, captions, chat-directed AE film | motion | motion-director, render-pipeline | H | L |
| `sound-voice` | studio | voice-over, music, mix | voice-over, TTS, music, SFX, loudness | motion, knowledge recording | motion-director | H | M |
| `render-pipeline` | studio | engines, render, QC, delivery | After Effects, aerender, Remotion, Blender, Resolve, ffmpeg | motion | motion-director | H | M |
| `presentation-builder` | studio | decks | slides, deck, PPTX, keynote | presentation, content course | ux-ui-designer, writing-dna | H | M |
| `video-intel` | studio | understanding videos | watch, YouTube, TikTok, Reels, transcript, breakdown | watch, dna, content study, motion | format-dna, trend-radar | H | L |
| `trend-radar` | studio | what is moving in a niche | trend, trending, radar, outlier, what to post | content radar | video-intel, format-dna | H | L |
| `format-dna` | studio | the form of winning videos | format, top videos, shorts format, what works | dna, content study | video-intel | H | L |
| `hooks-and-copy` | studio | openings, titles, captions | hook, first 3 seconds, title, caption, script beats | content script | writing-dna | H | L |
| `publish-prep` | studio | packages and approvals | post, publish, schedule, package, can we auto-post | content package, content queue | agent-team | H | M |
| `make-money` | business | earning routes | make money, income, which platform pays in Egypt | make-money, offer | job-finder, product-strategist | M | L |
| `job-finder` | business | jobs, freelance | job, freelance, remote work | job-finder | make-money | M | L |

## Memory-write hotspots

- frontend-design-system: `design/DESIGN_DNA.md`, continuity and visual QA reports · writing-dna: `writing/WRITING_DNA.md` · presentation-builder: `presentations/`
- guard-pass: `audits/GUARD_PASS_REPORT.md` · researcher: `research/` · anti-hallucination: evidence entries
- job-finder / make-money: `jobs/`, `money/` · skill-auditor: `audits/` and this registry · context-engineer: `state/{PROJECT_DNA,WORKING_NOTES,CONTEXT_SUMMARY}.md`
- agent-team: the team folder (`.bequite/team/` by default) · publish-prep: `work/<id>/package/` and `APPROVAL.md`

## Retired in v1

delegate-planner and multi-model-planning became `delegation`; scraping-automation and automation-engineer became `automation`; frontier-reasoning-coach and workflow-advisor folded into `orchestrator`. Updates move the old folders to `.bequite/backups/`.
