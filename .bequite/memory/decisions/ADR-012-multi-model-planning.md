---
adr_id: ADR-012-multi-model-planning
title: Multi-Model Planning — manual-paste MVP, parallel-mode default, role system, judge mode
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
superseded_by: null
constitution_version: 1.2.0
related_articles: [I, II, III, VI, VII]
related_doctrines: [default-web-saas, ai-automation, cli-tool, mena-bilingual]
implementation_target: v0.9.2 phase-1 docs / v0.10.5 phase-2 stubs / v0.10.6 phase-3 manual-paste working / v0.11.x phase-4 direct-API for two providers / post-v1.0.0 phase-5 specialist + debate + red-team modes
---

# ADR-012: Multi-Model Planning and Role Collaboration

> Status: **accepted (Phase-1 docs only — implementation lands v0.10.5+)** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

Single-model planning has two failure modes:

1. **Confirmation bias** — a model asked to plan a feature will rarely contradict its earlier output. Plans drift toward whatever the model first committed to.
2. **Blind spots** — Claude tends to over-engineer edge cases; GPT-5 tends to under-engineer security; Gemini tends to over-trust user intent. Each has signature failures different planning sessions struggle to surface alone.

Veracode 2025 reports ~45% of AI-generated code hits OWASP Top-10 issues; PhantomRaven (Koi Security 2025) shipped 126 npm packages exploiting AI-hallucinated names. Both problems are *plan-stage* failures: the model committed to a stack or pattern at planning time that an adversary can exploit at implementation time. A second model reviewing the first's plan catches a meaningful share of these before code is written.

BeQuite already has multi-model **routing** (v0.8.0 — pick the right model per phase × persona). What's missing is multi-model **planning** — getting two or more models to think through a project independently, then comparing their outputs.

Ahmed's request:

> Two or more models should think together before implementation. Example: ChatGPT 5.5 creates a plan, Claude Opus 4.7 creates a plan, BeQuite compares both, extracts common decisions, identifies missing parts, identifies contradictions, creates a merged stronger plan, one selected model acts as final judge or lead architect, user can approve, edit, or ask for another round.

## Decision

Add **Multi-Model Planning** as a first-class BeQuite capability. The decision has six parts:

### Part 1 — MVP path: manual-paste mode

For v0.10.5+ Phase-3, BeQuite ships **manual-paste mode** as the only working implementation:

1. User runs `bequite plan --multi-model` with a project brief.
2. BeQuite generates two prompts: `prompts/multi_model/plan_claude.md` (Claude-flavored) and `plan_chatgpt.md` (GPT-flavored).
3. User pastes each prompt into Claude Code / Claude.ai / ChatGPT subscription web UI.
4. User saves each model's response to `docs/planning_runs/RUN-<datetime>/{claude_plan.md,chatgpt_plan.md}`.
5. User runs `bequite models compare` — BeQuite analyzes both, produces `comparison.md` + `merge_report.md`.
6. User runs `bequite models merge --judge claude` — BeQuite (or the user's chosen judge model, run via the same manual-paste loop) produces `final_plan.md`.

**Why manual-paste first:**
- **No provider auth complexity.** Works the day BeQuite ships v0.10.5.
- **No billing complexity.** User uses their existing Claude Pro / ChatGPT Plus subscriptions.
- **ToS-clean.** The user is a human reading + typing; no driving of provider endpoints from a CLI session cookie.
- **Validates the workflow first.** Direct-API mode is a v2 enhancement once we know the UX is right.
- **Works with any model the user has access to.** Add Gemini, DeepSeek, Mistral, local models — no adapter required at MVP.

### Part 2 — Direct-API mode (v0.11.x+)

After manual-paste validates the workflow, direct-API mode reuses the v0.8.0 provider adapters:

1. `bequite plan --multi-model --direct-api` calls `cli/bequite/router.py::dispatch()` once per model.
2. Each call uses the v0.8.0 routing logic (pick model + reasoning_effort + fallback) plus a per-call cost guard against the v0.8.0 cost ledger.
3. Receipts emit per model invocation (v0.7.0 + v0.7.1 already operational).
4. Provider availability checked via `is_available()` — if a provider is unconfigured, BeQuite gracefully falls back to manual-paste mode for that one model.

### Part 3 — Browser-session reuse (consumer subscriptions) — NOT recommended

Ahmed asked specifically about driving consumer subscriptions (Claude Pro, ChatGPT Plus) from BeQuite. The technically-possible-but-not-recommended path is reusing the user's authenticated browser session — BeQuite would scrape session cookies + drive the web UI's API endpoints.

**This is not the recommended path.** Reasons:

1. **ToS violation.** Both Anthropic and OpenAI ToS prohibit non-API access to their endpoints. The "API access" has its own auth path (API keys, paid per-token). Subscription-session reuse is grey-to-black.
2. **Brittle.** Session cookies rotate; CSRF tokens regenerate; the UI changes structure. Maintenance burden is high.
3. **Rate limited differently than the API.** Subscription tiers throttle generously for human use, harshly for automation. Detection-and-throttling will hit BeQuite users.
4. **Detection fingerprinting.** Anthropic and OpenAI both run anti-automation systems. A flagged user could lose their subscription.

**Manual-paste mode is the ToS-clean way to use a subscription.** The user opens the chat UI, pastes BeQuite's prompt, saves the response. Zero automation; zero ToS surface. **Done.**

If a user wants automation against their consumer subscription, they should subscribe to API access separately (Claude API + OpenAI API) and use direct-API mode.

### Part 4 — Default collaboration mode = Parallel Planning

Five collaboration modes are documented in the strategy doc:

1. **Parallel Planning** — each model drafts an independent plan; BeQuite compares + merges.
2. **Specialist Split** — each model owns a domain (architecture / security / UX / cost).
3. **Debate and Merge** — models review each other's drafts.
4. **Judge Mode** — one model is final judge over peers.
5. **Red-Team Review** — one model attacks the plan (security, scalability, UX gaps).

**Default for v0.10.5 MVP: Parallel Planning.** It's the simplest mode, the most useful for early-project design, and the most ToS-clean (each model sees only the brief, not the other model's output — which is what subscription users naturally do).

**v2 default after manual-paste matures: Debate and Merge.**

### Part 5 — Default judge model

The judge model is **configurable per project**. BeQuite recommends:

- **Claude Opus 4.7** as default judge for analytical / architectural / code-quality work (its current frontier on those tasks per AkitaOnRails 2026 benchmarks).
- **GPT-5** as alternative judge for product-strategy / UX / customer-flow work.
- User can override via `--judge claude` or `--judge gpt` or `--judge none` (no judge; user picks final from comparison).

When auto-mode (v0.10.0) integrates multi-model planning, the judge defaults to whatever the project's `bequite.config.toml::routing` declares for the orchestrator persona — usually Opus 4.7 with reasoning_effort=high.

### Part 6 — Conflict resolution

When models disagree, BeQuite produces a **comparison table** in `comparison.md`:

| Topic | Claude says | GPT says | Agreement | Risk | Better option | Final | Reason |
|---|---|---|---|---|---|---|---|
| Auth provider | Better-Auth | Clerk | partial | low | Better-Auth (ownership) | Better-Auth | Aligned with Doctrine Rule 9 + ownership preference. |
| State manager | Zustand | Redux Toolkit | conflict | low | Zustand | Zustand | Smaller; matches doctrine. |
| ... | ... | ... | ... | ... | ... | ... | ... |

Resolution rules (priority order):

1. **Iron Law beats anything.** A model recommendation that violates an Article (e.g. "use SQLite for write-heavy multi-tenant" violates Article V scale honesty) is rejected on sight, no matter who proposed it.
2. **Doctrine beats convenience.** A model recommendation that violates a loaded Doctrine rule (e.g. "use bg-purple-500 hardcoded" violates default-web-saas Rule 1) is rejected.
3. **Active session evidence beats memory.** If a model claims "Vercel timeout is 300s" and `bequite freshness` shows Vercel Pro has been 800s since 2025, the freshness evidence wins.
4. **Skeptic kill-shot must be answered.** Every contested topic gets one Skeptic question — the answer is recorded in `comparison.md::Reason`.
5. **User picks final.** When all of the above clear and a genuine tradeoff remains (e.g. Better-Auth vs Clerk), the user marks the final decision in `user_decisions.md` and confirms with `bequite models merge --confirm`.

### Storage layout

Per Ahmed's spec:

```
docs/planning_runs/
  RUN-2026-05-10T15-30/
    input_brief.md            # what the user described
    claude_plan.md            # Claude's independent plan
    chatgpt_plan.md           # GPT's independent plan
    comparison.md             # side-by-side table + per-topic resolution
    merge_report.md           # what was merged + why
    final_plan.md             # the merged plan, ready for /bequite.plan
    user_decisions.md         # any human-in-the-loop selections
    receipts/                 # per-model receipts (v0.7.0+)
```

```
prompts/multi_model/
  plan_claude.md              # Claude-flavored brief template
  plan_chatgpt.md             # GPT-flavored brief template
  review_security.md          # Security Reviewer specialist prompt
  review_frontend.md          # Frontend Reviewer specialist prompt
  review_backend.md           # Backend Reviewer specialist prompt
  merge_judge.md              # Judge prompt template
  red_team.md                 # Red-team prompt template
```

```
state/
  model_sessions/             # per-model handles + paste history
  planning_runs/              # active run tracking
  merge_reports/              # historical merges
```

### CLI commands

```
bequite plan --multi-model [--mode parallel|debate|specialist|red-team|judge]
bequite plan --models claude,gpt[,gemini,deepseek]
bequite plan --judge claude|gpt|none
bequite models list           # available providers + roles
bequite models configure      # interactive setup
bequite models roles          # list 12 roles + which models cover them
bequite models compare        # produce comparison.md from Run dir
bequite models merge [--judge <model>] [--confirm]
```

Slash commands:

```
/bequite.plan --multi-model
/bequite.models.list
/bequite.models.configure
/bequite.models.roles
/bequite.models.compare
/bequite.models.merge
```

### Three new personas

This ADR introduces three personas alongside the existing 17:

1. **multi-model-planning-orchestrator** — owns the multi-model loop. Generates per-model prompts. Receives outputs. Builds comparison + merge reports. Asks Skeptic kill-shots.
2. **model-judge** — when judge-mode is active, this persona reviews all plans + selects best ideas + rejects weak assumptions + writes final plan.
3. **red-team-reviewer** — when red-team mode is active, attacks the plan from security / scalability / UX / deployment / token-waste / hidden-assumptions angles.

Authored alongside this ADR; total persona count → 20.

## Constitution amendment status

**No new Iron Law required.** Article I (Specification supremacy) covers the planning artifact discipline; Article VII (Hallucination defense) governs evidence-checking; Article VI (Honest reporting) is operational here ("what was written / what was tested / what remains / what is uncertain" applies to multi-model plans too).

## Status: accepted (Phase-1 docs only; 2026-05-10)

Phase 2-5 land per the implementation_target field. v0.10.5 ships the manual-paste workflow.

## Cross-references

- Strategy doc: `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`
- Requirements doc: `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md`
- Constitution Articles I + VI + VII: `.bequite/memory/constitution.md`
- Existing routing matrix: `skill/routing.json` (v0.2.0; v0.8.0 wired)
- Existing provider adapters: `cli/bequite/providers/` (v0.8.0)
- Existing cost ledger: `cli/bequite/cost_ledger.py` (v0.8.0)
- Receipts: `cli/bequite/receipts.py` + `cli/bequite/receipts_signing.py` (v0.7.0 + v0.7.1)
