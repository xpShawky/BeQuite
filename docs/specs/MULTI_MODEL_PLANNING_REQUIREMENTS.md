# Multi-Model Planning — Requirements

> Concrete, testable requirements for the multi-model planning module. Pairs with `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md` (the "what / why") — this doc is the "must do / must not do" contract.
>
> **Status:** Phase-1 docs (v0.9.2). Implementation lands v0.10.5+.

---

## 1. Functional requirements

### F-1. Generate per-model prompts

`bequite plan --multi-model "<brief>"` MUST:

- F-1.1 Create a fresh run directory at `docs/planning_runs/RUN-<YYYY-MM-DDTHH-MM>/`.
- F-1.2 Write `input_brief.md` containing the literal user-provided brief + active doctrines + project metadata (mode, scale tier, audience).
- F-1.3 Render one prompt file per selected model under `<run-dir>/prompts/plan_<model-slug>.md`.
- F-1.4 Each prompt MUST be **independent** — no model sees another model's output at this stage.
- F-1.5 Each prompt MUST embed: the brief verbatim + the active Constitution version + the active Doctrines + the model's assigned role.
- F-1.6 Prompts MUST NOT embed API keys, tokens, or any secret-shaped content (PreToolUse secret-scan hook validates).

### F-2. Accept model outputs

After the user pastes responses into their chat tools, BeQuite MUST:

- F-2.1 Detect new files at `<run-dir>/<model-slug>_plan.md`.
- F-2.2 Validate each response is non-empty + parseable (heading-structured Markdown).
- F-2.3 Surface a friendly error if a response slot is empty after a configurable wait (default 60 minutes for synchronous mode).
- F-2.4 Optionally support `--async` mode where CLI exits + leaves a `READY:` marker for later processing.

### F-3. Compare model outputs

`bequite models compare` MUST:

- F-3.1 Parse each plan into structured sections (Vision / Scope / Stack / Phases / Risks / etc.).
- F-3.2 For each section, build a comparison row in `comparison.md`:
  - Topic
  - Per-model recommendation
  - Agreement level: full / partial / conflict / only-one-mentioned
  - Risk: low / medium / high
  - Better option (auto-recommended where Iron Law / Doctrine / freshness gives a clear winner)
  - Final decision (`pending` until merge)
  - Reason
- F-3.3 Apply Iron Law / Doctrine / freshness filters per ADR-012 §10.
- F-3.4 Auto-mark `requires_user_decision: true` for non-blocking conflicts.
- F-3.5 Flag any section that all models omitted as a coverage gap.

### F-4. Merge model outputs

`bequite models merge [--judge <model>] [--confirm]` MUST:

- F-4.1 Without `--judge`: scaffold `prompts/merge_judge.md` only when the user passes `--judge <model>`. With no judge, build `final_plan.md` directly from `comparison.md` + `user_decisions.md`.
- F-4.2 With `--judge`: render judge prompt; wait for judge response at `<run-dir>/merge_report.md`; extract `final_plan.md` from merge_report.
- F-4.3 Without `--confirm`: leave `final_plan.md` as a draft; do not write to `specs/<feature>/plan.md`.
- F-4.4 With `--confirm`: copy `final_plan.md` to `specs/<feature>/plan.md`; link the planning run as the spec's provenance.
- F-4.5 Emit one receipt per model invocation (manual-paste = $0 cost; direct-API = actual cost).

### F-5. Role assignment

Users MUST be able to:

- F-5.1 Assign roles via CLI: `bequite plan --models claude=lead-architect,gpt=product-strategist`.
- F-5.2 Assign roles via config: `bequite.config.toml::multi_model.role_assignments`.
- F-5.3 List available roles: `bequite models roles`.
- F-5.4 Each role MUST have a default model recommendation that the user can override.

### F-6. Five collaboration modes

The CLI MUST support `--mode <mode>`:

- F-6.1 `parallel` (default) — all models receive same brief; independent plans.
- F-6.2 `specialist` — domain-split per role assignment.
- F-6.3 `debate` — two rounds; round 2 sees other model's output.
- F-6.4 `judge` — judge model decides between peer outputs.
- F-6.5 `red-team` — one model attacks an existing plan.

### F-7. Provider adapters

Multi-model planning MUST:

- F-7.1 Use `bequite.providers.AiProvider` Protocol for all providers.
- F-7.2 Default to **manual-paste** mode unless `--direct-api` flag is set.
- F-7.3 With `--direct-api`, gracefully fall back to manual-paste for any provider whose `is_available()` returns False.
- F-7.4 Never reuse consumer-subscription session cookies (Claude Pro / ChatGPT Plus). Documented in ADR-012 §Part 3.
- F-7.5 Add `ManualPasteProvider` to `cli/bequite/providers/` (v0.10.5).

### F-8. Iron Law + Doctrine enforcement

For every model recommendation, the merge engine MUST:

- F-8.1 Check against active Iron Laws (Articles I-IX). Auto-reject violations with reason: "Violates Article <N>".
- F-8.2 Check against loaded Doctrine rules. Auto-reject violations with reason: "Violates Doctrine `<name>` Rule <N>".
- F-8.3 Check against `bequite freshness` cache. Flag stale claims with reason: "Stale claim — freshness probe says ...".

### F-9. Skeptic kill-shots

For every contested topic, the merge engine MUST:

- F-9.1 Generate at least one Skeptic kill-shot question.
- F-9.2 Record the kill-shot + answer in `comparison.md::Reason` column.
- F-9.3 Refuse to write `final_plan.md` if any block-class topic has no recorded answer.

### F-10. Receipts

Multi-model planning MUST:

- F-10.1 Emit a v0.7.0+ receipt per model invocation.
- F-10.2 Sign each receipt (v0.7.1+) when public key is present.
- F-10.3 Link receipts to the planning run via `<run-dir>/receipts/<sha>-<phase>.json`.
- F-10.4 Update `.bequite/cache/cost-ledger.json` per direct-API call (per v0.8.0).

## 2. Non-functional requirements

### NFR-1. Performance

- NFR-1.1 Manual-paste mode: latency dominated by user paste-time (BeQuite waits asynchronously).
- NFR-1.2 Direct-API mode: total wall-clock ≤ 90 seconds for 2-model parallel (assumes typical model latency 30s + overhead).
- NFR-1.3 Comparison engine: `bequite models compare` completes in < 5s on 8-section plans.

### NFR-2. Cost

- NFR-2.1 Manual-paste: $0 BeQuite-incurred cost.
- NFR-2.2 Direct-API: bounded by `bequite.config.toml::multi_model.max_run_cost_usd` (default $5).
- NFR-2.3 Cost overrun → pause + user approval (uses v0.8.0 `stop-cost-budget.sh` hook).

### NFR-3. Privacy

- NFR-3.1 No prompt content sent to providers other than the assigned model.
- NFR-3.2 Receipts redact prompts (sha256 only).
- NFR-3.3 `<run-dir>/prompts/*.md` is `.gitignore`-able per project (advisory; not enforced — some runs are intentionally committed for archival).
- NFR-3.4 Manual-paste mode: user is responsible for what they paste into provider chat UIs; BeQuite does not auto-redact PII.

### NFR-4. Reliability

- NFR-4.1 Idempotent reruns: `bequite models compare` re-run on same run-dir produces identical output.
- NFR-4.2 Partial failures: one model's response empty → run continues with remaining models + flags gap.
- NFR-4.3 Resume: a run interrupted at any phase resumes via `bequite plan --multi-model --resume RUN-...`.

### NFR-5. Compatibility

- NFR-5.1 Backward-compatible with v0.7.0+ receipts schema (additive fields only).
- NFR-5.2 Works without `BEQUITE_API_KEY` (manual-paste mode is default).
- NFR-5.3 Works without auth (Phase-2 / Phase-3 of ADR-011).

## 3. CLI commands

| Command | Purpose | Phase |
|---|---|---|
| `bequite plan --multi-model "<brief>"` | Start a planning run | v0.10.5 |
| `bequite plan --multi-model --models claude,gpt` | Specify models | v0.10.5 |
| `bequite plan --multi-model --mode <mode>` | Specify collaboration mode | v0.10.5 |
| `bequite plan --multi-model --judge <model>` | Specify judge | v0.10.5 |
| `bequite plan --multi-model --direct-api` | Use API keys instead of manual-paste | v0.11.x |
| `bequite plan --multi-model --resume RUN-...` | Resume an interrupted run | v0.10.5 |
| `bequite models list` | List available providers + models | v0.10.5 |
| `bequite models configure` | Interactive setup of roles + providers | v0.10.5 |
| `bequite models roles` | List 12 roles + default model per role | v0.10.5 |
| `bequite models compare` | Generate comparison.md from plans | v0.10.5 |
| `bequite models merge [--judge X] [--confirm]` | Generate final plan | v0.10.5 |

## 4. Slash commands

| Slash | CLI equivalent |
|---|---|
| `/bequite.plan --multi-model` | `bequite plan --multi-model` |
| `/bequite.models.list` | `bequite models list` |
| `/bequite.models.configure` | `bequite models configure` |
| `/bequite.models.roles` | `bequite models roles` |
| `/bequite.models.compare` | `bequite models compare` |
| `/bequite.models.merge` | `bequite models merge` |

## 5. Data model

### Run directory

```
docs/planning_runs/
  RUN-2026-05-10T15-30/
    input_brief.md            # what the user described
    prompts/
      plan_claude.md          # Claude's prompt (or any model's per role)
      plan_chatgpt.md         # GPT's prompt
      review_security.md      # specialist prompt (specialist mode)
      merge_judge.md          # judge prompt (judge mode)
      red_team.md             # red-team prompt (red-team mode)
    claude_plan.md            # Claude's response (manual-paste user-saved)
    chatgpt_plan.md           # GPT's response
    comparison.md             # comparison table
    merge_report.md           # judge's output
    final_plan.md             # final merged plan
    user_decisions.md         # any human-in-the-loop selections
    receipts/                 # per-model receipts
      <sha>-P2-claude.json
      <sha>-P2-gpt.json
      <sha>-P2-judge.json
    state.json                # run state (mode, models, status per phase)
```

### Run state file (`state.json`)

```json
{
  "version": "1",
  "run_id": "RUN-2026-05-10T15-30",
  "started_utc": "2026-05-10T15:30:00Z",
  "mode": "parallel",
  "judge_model": "claude-opus-4-7",
  "models": [
    {"name": "claude-opus-4-7", "role": "lead-architect", "provider": "manual-paste", "status": "complete"},
    {"name": "gpt-5", "role": "product-strategist", "provider": "manual-paste", "status": "complete"}
  ],
  "phase": "merged",
  "comparison_topics": 8,
  "conflicts": 2,
  "user_decisions_pending": 1,
  "final_plan_committed": false,
  "specs_target": "specs/bookings/plan.md"
}
```

## 6. State files

```
state/
  model_sessions/
    <run-id>/                  # mirrors docs/planning_runs/<run-id>/state.json
  planning_runs/
    active.json                # currently-active run pointer
  merge_reports/
    <run-id>-summary.md        # short summary; full report stays in docs/
```

## 7. Prompt templates (lands v0.10.5)

```
skill/templates/prompts/multi_model/
  plan_claude.md.tpl           # Claude-flavored brief template
  plan_chatgpt.md.tpl          # GPT-flavored brief template
  review_security.md.tpl       # Security Reviewer specialist
  review_frontend.md.tpl       # Frontend Reviewer specialist
  review_backend.md.tpl        # Backend Reviewer specialist
  review_database.md.tpl       # Database Architect specialist
  review_testing.md.tpl        # Testing Architect specialist
  review_devops.md.tpl         # DevOps Architect specialist
  review_ux.md.tpl             # UX/UI Reviewer specialist
  review_scraping.md.tpl       # Scraping/Automation specialist
  review_cost.md.tpl           # Cost Optimizer specialist
  merge_judge.md.tpl           # Judge prompt template
  red_team.md.tpl              # Red-team prompt template
```

Each template variable (per Doctrine + freshness conventions):
- `{{BRIEF}}` — user-provided brief.
- `{{ACTIVE_DOCTRINES}}` — comma-separated list of loaded Doctrines.
- `{{CONSTITUTION_VERSION}}` — e.g. "1.2.0".
- `{{MODEL_NAME}}` — for self-identification.
- `{{ROLE}}` — assigned role.
- `{{OTHER_MODEL_OUTPUTS}}` — only set in debate mode.
- `{{PRIOR_PLAN}}` — only set in red-team mode.

## 8. Output files

Per the Run directory layout above. All Markdown.

## 9. Logs

- Per-run log at `<run-dir>/run.log` — Click logger output for the run.
- Aggregated log at `state/merge_reports/<run-id>-summary.md` — short summary for `bequite memory show planning-run <run-id>`.

## 10. Acceptance criteria (v0.10.5)

For v0.10.5 to ship:

- ✅ ADR-012 accepted (this Phase-1 deliverable).
- ✅ `cli/bequite/multi_model.py` with: `render_prompt`, `compare`, `merge`, `extract_final_plan`.
- ✅ `cli/bequite/providers/manual_paste.py` (new provider conforming to AiProvider Protocol).
- ✅ `bequite plan --multi-model` Click command + `bequite models {list,configure,roles,compare,merge}` Click group.
- ✅ Prompt templates at `skill/templates/prompts/multi_model/*.md.tpl` (≥4 templates: plan_claude, plan_chatgpt, merge_judge, red_team).
- ✅ Integration test suite at `tests/integration/multi_model/` (≥10 tests covering: prompt render, file detection, comparison build, merge with judge / without judge, conflict resolution Iron Law / Doctrine / freshness, receipts emit, run state persistence, idempotent rerun).
- ✅ Combined integration suite green: receipts (10) + signing (9) + router (15) + pricing (14) + e2e (16) + multi-model (10) = 74/74 tests on Python 3.14.
- ✅ Updated CHANGELOG, activeContext, progress, recovery, current_phase.
- ✅ One end-to-end manual-paste run on the `examples/01-bookings-saas` example (proof-of-life screenshot in evidence dir).

## 11. Open questions (deferred to v0.10.5 implementation phase)

| Question | Default decision | Override path |
|---|---|---|
| Should manual-paste mode poll the filesystem or watch via inotify/fsevents? | Polling (simplest; cross-platform) | Override per OS later |
| Should comparison-table be HTML or Markdown? | Markdown (consistent with rest of BeQuite) | HTML export in v0.13.0 (vibe-handoff) |
| Should models see each other's output in Mode 1 (Parallel)? | NO — independence is the point of Parallel | Mode 3 (Debate) is the "see each other" mode |
| Default judge model when `--judge` omitted? | Claude Opus 4.7 (analytical) | User config in `bequite.config.toml::multi_model.default_judge` |
| What happens if user runs `bequite plan` (without `--multi-model`)? | Single-model mode (existing behavior) | Documented in `docs/HOW-IT-WORKS.md` (v0.14.0) |

## 12. Cross-references

- ADR: `.bequite/memory/decisions/ADR-012-multi-model-planning.md`
- Strategy: `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`
- Constitution: `.bequite/memory/constitution.md`
- Provider adapters: `cli/bequite/providers/` (v0.8.0)
- Routing: `skill/routing.json` (v0.2.0; v0.8.0 wired)
- Receipts: `cli/bequite/receipts.py` (v0.7.0)
- Signing: `cli/bequite/receipts_signing.py` (v0.7.1)
- Cost ledger: `cli/bequite/cost_ledger.py` (v0.8.0)
- Pricing: `cli/bequite/pricing.py` (v0.8.1)
- New personas: `skill/agents/{multi-model-planning-orchestrator,model-judge,red-team-reviewer}.md`
