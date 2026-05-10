# Multi-Model Planning Strategy

> Architectural strategy doc that fleshes out ADR-012. Operational reference for engineers implementing v0.10.5+ manual-paste mode and v0.11.x+ direct-API mode.
>
> **Status:** Phase-1 (docs-only). Implementation lands v0.10.5+.

---

## 1. Goal

Get two or more AI models to think through a project plan **independently**, then have BeQuite compare + merge their outputs into a single, stronger plan that the user can approve, edit, or send for another round.

## 2. Non-goals

- Multi-agent **execution** (running multiple models against code simultaneously). That's auto-mode (v0.10.0) + parallel-task fan-out (v0.10.1) — not this feature.
- Browser-session reuse of consumer subscriptions (Claude Pro, ChatGPT Plus). ToS-grey + brittle. See ADR-012 §Part 3.
- Real-time streaming model-vs-model debate. v2 enhancement post-v1.0.0.

## 3. Why multi-model planning exists

Single-model planning fails predictably:

1. **Confirmation bias** — once a model commits to a stack or pattern, it rarely contradicts itself within the same plan.
2. **Per-model blind spots** — Claude over-engineers edge cases; GPT-5 under-engineers security; Gemini over-trusts user intent. Each model has signature failure modes.
3. **Veracode 2025: ~45% of AI-generated code has OWASP Top-10 issues.** Many of those are plan-stage decisions (e.g. "store passwords in DB" vs "use Better-Auth"). A second model reviewing catches a meaningful share.

A second model reading the first's plan exposes assumptions the first didn't realize it made. Merging the two preserves what they agree on + surfaces what they disagree on for human resolution.

## 4. MVP — manual-paste mode

The Phase-3 (v0.10.5) implementation only requires:

1. A prompt-template renderer (`cli/bequite/multi_model.py::render_prompt`).
2. A comparison engine (`cli/bequite/multi_model.py::compare`).
3. A merge-report writer (`cli/bequite/multi_model.py::merge`).

**Workflow:**

```
1. bequite plan --multi-model "Build a bookings SaaS with admin + customer roles"
   → BeQuite scaffolds:
     docs/planning_runs/RUN-2026-05-10T15-30/input_brief.md
     docs/planning_runs/RUN-2026-05-10T15-30/prompts/plan_claude.md
     docs/planning_runs/RUN-2026-05-10T15-30/prompts/plan_chatgpt.md

2. User opens Claude (Pro / Code / Web) → pastes plan_claude.md → saves
   response to docs/planning_runs/RUN-.../claude_plan.md

3. User opens ChatGPT (Plus / Web) → pastes plan_chatgpt.md → saves
   response to docs/planning_runs/RUN-.../chatgpt_plan.md

4. bequite models compare
   → produces RUN-.../comparison.md (decision table)

5. bequite models merge --judge claude
   → BeQuite scaffolds RUN-.../prompts/merge_judge.md (the judge prompt)
   → user pastes it into Claude → saves response to RUN-.../merge_report.md
   → bequite extracts final_plan.md from merge_report.md

6. User reviews final_plan.md → confirms with bequite models merge --confirm
   → BeQuite copies final_plan.md to specs/<feature>/plan.md
   → links the planning run as the spec's provenance
```

**Why this works on day-1 of v0.10.5:**

- Zero provider auth complexity. Subscription users use their existing tools.
- ToS-clean (no driving of provider endpoints from CLI sessions).
- Validates the workflow before committing to direct-API.
- Works with any model — Claude, GPT, Gemini, Mistral, DeepSeek, local Ollama, even Perplexity if the user wants to reality-check claims.

## 5. Future direct-API mode (v0.11.x+)

After manual-paste matures, direct-API reuses v0.8.0 provider infrastructure:

```python
# Direct-API path (v0.11.x+):
from bequite.router import dispatch
from bequite.multi_model import render_prompt, save_output

claude_prompt = render_prompt(brief, model="claude-opus-4-7")
claude_completion, _ = dispatch(
    phase="P2", persona="multi-model-planning-orchestrator",
    prompt=claude_prompt,
)
save_output(run_dir, "claude_plan.md", claude_completion.text)

# (same for ChatGPT, then compare + merge)
```

**Two new failure paths to handle in direct-API:**

1. Provider unavailable (no API key) → fall back to manual-paste for that model.
2. Cost ceiling reached mid-run → pause + prompt user (per v0.8.0 stop-cost-budget hook).

## 6. Provider adapter architecture

Multi-model planning **does not introduce new provider adapters.** It uses the existing v0.8.0 `AiProvider` Protocol:

```python
class AiProvider(Protocol):
    name: str
    def is_available(self) -> bool: ...
    def supports_model(self, model: str) -> bool: ...
    def estimate_cost_usd(self, model, in_tokens, out_tokens) -> float: ...
    def complete(self, *, model, prompt, ...) -> Completion: ...
```

What's new:

- **ManualPasteProvider** (v0.10.5) — implements `AiProvider` but `is_available()` always returns True; `complete()` writes the prompt to a file + waits for the user to drop the response into a sibling file. The "wait" can be:
  - Synchronous (CLI blocks until file appears) — good for single-shot.
  - Asynchronous (CLI exits + leaves a `READY:` marker) — good for "paste later" workflows.

```python
class ManualPasteProvider:
    name = "manual-paste"

    def is_available(self) -> bool:
        return True  # always

    def supports_model(self, model: str) -> bool:
        return True  # any user-named model

    def estimate_cost_usd(self, model, in_tokens, out_tokens) -> float:
        return 0.0  # human cost, not API cost

    def complete(self, *, model, prompt, run_dir: pathlib.Path, async_mode=False, ...) -> Completion:
        prompt_file = run_dir / "prompts" / f"plan_{slug(model)}.md"
        prompt_file.write_text(prompt)
        response_file = run_dir / f"{slug(model)}_plan.md"
        if async_mode:
            return Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="awaiting_user", model=model, provider=self.name,
            )
        # synchronous: poll for file appearance
        while not response_file.exists():
            time.sleep(2)
            print(f"Waiting for {response_file.name} ... (Ctrl-C to abort)")
        return Completion(
            text=response_file.read_text(),
            input_tokens=estimate_tokens(prompt),
            output_tokens=estimate_tokens(response_file.read_text()),
            finish_reason="user_provided", model=model, provider=self.name,
        )
```

## 7. Role system — 12 roles

Each role can be assigned to any model. Default assignments below; users override via `bequite.config.toml::multi_model.role_assignments`.

| Role | Default Model | What it does |
|---|---|---|
| Lead Architect | Claude Opus 4.7 | Owns overall architecture + cross-cutting decisions. |
| Product Strategist | GPT-5 | Owns product scope, user value, competitive positioning. |
| Frontend Architect | Claude Sonnet 4.6 | UI / state management / component sourcing. |
| Backend Architect | Claude Sonnet 4.6 | API design / data flow / integration boundaries. |
| Database Architect | Claude Opus 4.7 | Data model / RLS / indexing / migration discipline. |
| Security Reviewer | Claude Opus 4.7 (xhigh effort) | OWASP Top 10 / Article IV compliance / secrets discipline. |
| Testing Architect | Claude Sonnet 4.6 | Test pyramid / Playwright walks / coverage strategy. |
| DevOps Architect | Claude Sonnet 4.6 | CI / deployment / observability / cost discipline. |
| UX/UI Reviewer | GPT-5 + Impeccable bundled skill | Anti-patterns walk / accessibility / copy. |
| Scraping/Automation Architect | Claude Opus 4.7 | If Doctrine `ai-automation` loaded; n8n / Make patterns. |
| Cost & Token Optimizer | Claude Haiku 4.5 | Reads receipts; recommends cost reductions. |
| Final Judge | Configurable (default Opus) | Reviews all role outputs; produces final plan. |

Most planning runs use a subset (typically Lead Architect + Product Strategist + Security Reviewer for an MVP project).

## 8. Five collaboration modes

### Mode 1 — Parallel Planning (default for MVP)

- All selected models receive the **same brief**.
- Each produces a complete, independent plan.
- BeQuite compares + identifies agreements / disagreements / gaps.
- User picks final via `bequite models merge`.

**Best for:** early project design when no single model has prior context. Most ToS-clean (no model sees another's output).

### Mode 2 — Specialist Split

- Each model gets a domain-specific brief.
- Example: Claude → Lead Architect + Backend; GPT → Product Strategist + UX; Gemini → Database; Haiku → Cost Optimizer.
- BeQuite stitches the domain plans into a single doc.

**Best for:** larger projects where domain depth matters more than cross-domain consistency. Slightly higher merge complexity (handling domain overlaps).

### Mode 3 — Debate and Merge

- Round 1: each model drafts a plan (parallel).
- Round 2: each model receives the **other model's plan** + asked to: identify agreement, disagreement, missing points, risky assumptions, better alternatives, final recommendation.
- BeQuite produces final based on debate outputs.

**Best for:** contested / high-stakes decisions where an independent stress-test is worth the extra round.

### Mode 4 — Judge Mode

- Models produce parallel plans (Mode 1).
- One model is designated **Final Judge** — reviews all plans + selects best ideas + rejects weak assumptions + writes final plan.
- Final plan must explain (per topic) why each decision was accepted or rejected.

**Best for:** when the user trusts one specific model's judgment most.

### Mode 5 — Red-Team Review

- Models produce a plan (any of Modes 1-4).
- A red-team model attacks: security gaps, architecture gaps, testing gaps, deployment gaps, scalability gaps, UX gaps, token waste, hidden assumptions.
- Output: `red_team_review.md` — every gap with severity (block / warn / nit) + remediation suggestion.

**Best for:** vibe-defense and gov-fedramp Doctrines where adversarial review is mandatory before implementation.

## 9. Plan merge algorithm

Given N independent plans + an optional judge model:

```
1. Parse each plan into structured sections (Vision / Scope / Stack / Phases / etc.).
   - If a plan is missing a section, that's a finding ("Plan A omitted Testing strategy").
2. For each section, build a comparison table:
   - Topic (e.g. "Auth provider")
   - Per-model recommendation
   - Agreement level: full | partial | conflict | only-one-mentioned
   - Risk: low | medium | high (heuristic — e.g. security topics default to medium+)
3. Apply Iron Law / Doctrine / freshness filter (see §10 Conflict resolution).
4. For each non-blocking conflict, mark `requires_user_decision: true`.
5. If a judge model is configured:
   a. Render `merge_judge.md` prompt template.
   b. Send to judge (manual-paste or direct-API).
   c. Judge produces `merge_report.md` with per-topic final + reason.
6. Else:
   a. BeQuite produces `comparison.md` only.
   b. User runs `bequite models merge --confirm` after editing `user_decisions.md`.
7. Generate `final_plan.md` from merge_report + user_decisions.
8. Emit receipts (one per model invocation; one for the merge operation).
```

## 10. Conflict resolution rules (priority order)

1. **Iron Law beats anything.** A model recommendation that violates an Article (e.g. "use SQLite for write-heavy multi-tenant" violates Article V) is rejected on sight, no matter who proposed it. Reason: "Violates Constitution Article V scale honesty."
2. **Doctrine beats convenience.** A model recommendation that violates a loaded Doctrine rule (e.g. hardcoded purple-blue gradient violates default-web-saas Rule 1) is rejected. Reason: "Violates loaded Doctrine `default-web-saas` Rule 1."
3. **Active session evidence beats memory.** If `bequite freshness` shows a fact, the freshness evidence wins over any model's memory.
4. **Skeptic kill-shot must be answered.** Every contested topic gets one Skeptic question — answer recorded.
5. **User picks final.** When all of the above clear and a tradeoff remains, user marks the final in `user_decisions.md`.

## 11. User decision points

The user must explicitly approve / decide:

- ✅ Topic flagged `requires_user_decision: true`.
- ✅ Stack selection (per Article I — spec sup remacy).
- ✅ Final plan before it's written to `specs/<feature>/plan.md`.
- ✅ Cost / wall-clock ceiling overrides.
- ✅ Doctrine activation.

## 12. Logging model contributions

Every multi-model planning run produces a `merge_report.md` with:

```markdown
## Model contributions

| Model | Role | Plan path | Receipt | Cost (USD) | Notes |
|---|---|---|---|---|---|
| claude-opus-4-7 | Lead Architect | claude_plan.md | sha256:... | $0.083 | manual-paste mode |
| gpt-5 | Product Strategist | chatgpt_plan.md | sha256:... | $0.041 | manual-paste mode |
| claude-opus-4-7 | Final Judge | merge_report.md | sha256:... | $0.150 | manual-paste mode |

## Decisions accepted

- Auth provider: Better-Auth (both models agreed; doctrine-aligned).
- ...

## Decisions rejected

- "Roll-our-own JWT auth" (Claude proposed; rejected per Doctrine `default-web-saas` Rule 9).
- ...

## Decisions deferred to user

- State manager: Zustand (Claude) vs Redux Toolkit (GPT). User picked Zustand in user_decisions.md.
- ...
```

## 13. Token saving strategy

- **Manual-paste mode = $0 of API cost** (the user pays subscription cost, not BeQuite-incurred).
- **Direct-API mode** runs each model **once** (Mode 1) or twice (Mode 3 debate). Cost is bounded by `bequite.config.toml::cost.session_max_usd`.
- Token economist persona (existing v0.2.0) reads receipts after every multi-model run + produces `cost_optimization.md` recommending cheaper models for next run if the project type doesn't need frontier reasoning.

## 14. Failure handling

| Failure | Recovery |
|---|---|
| User pastes wrong file (claude_plan into chatgpt_plan slot) | Compare detects model-name mismatch in plan content + asks user to confirm. |
| One model's plan is empty | Re-prompt with reminder of brief; if still empty, drop that model from the run + flag in merge report. |
| Models violently disagree on a stack pick | Skeptic asked for kill-shot per option; user picks final via `user_decisions.md`. |
| Judge produces incoherent merge | User reruns with `--judge none`; falls back to comparison-only mode. |
| Cost ceiling hit mid-direct-API | Stop-cost-budget hook pauses; user approves continuation or cancels. |
| Provider unavailable (no API key) | Direct-API mode falls back to manual-paste for that model; rest of run continues. |

## 15. Testing strategy

- Unit tests at `cli/tests/test_multi_model.py`:
  - Prompt template rendering.
  - Comparison-table generator (synthetic plan inputs).
  - Merge-report generator.
- Integration tests at `tests/integration/multi_model/`:
  - End-to-end manual-paste workflow with mocked file writes.
  - End-to-end direct-API workflow with TestProvider.
  - Conflict resolution: Iron Law violation → auto-rejected.
  - Conflict resolution: Doctrine violation → auto-rejected.
  - Conflict resolution: User decision deferred → flagged correctly.
- E2E test at `tests/integration/e2e/test_multi_model_smoke.py`:
  - `bequite plan --multi-model` scaffolds run dir.
  - `bequite models compare` produces comparison.md.
  - `bequite models merge` produces final_plan.md.

## 16. Security and privacy concerns

- **No prompt content leaked across models** — each model sees only its own prompt + (in Debate mode) the other model's output. Session content stays in the user's chat windows.
- **No API key crossover** — Anthropic key is used only for Anthropic provider; OpenAI key for OpenAI; etc. Per-provider env vars enforced via v0.8.0 ProvidersConfig.
- **Receipts redact prompts** — receipt's `input.prompt_hash` is sha256, not plaintext (v0.7.0 schema). Plaintext stays in `docs/planning_runs/<run>/prompts/` (gitignored if the brief contains private info).
- **Manual-paste workflow** — the user is responsible for what they paste into subscription web UIs. BeQuite does not auto-redact PII.

## 17. Cost concerns

- Manual-paste mode = $0 BeQuite-incurred cost.
- Direct-API mode (Mode 1, two models) ≈ $0.05-$0.30 per planning run depending on model + brief size.
- Mode 3 (Debate) ≈ 1.5-2× Mode 1 cost.
- Mode 4 (Judge) ≈ Mode 1 + 1 judge call.
- Mode 5 (Red-Team) ≈ +1 red-team-model call.

Cost ceiling default: `$5 per planning run` (configurable). Hit → pause for user approval.

## 18. Example workflows

### Example A — Solo developer, manual-paste, two-model parallel

```bash
$ bequite plan --multi-model "Build a bookings SaaS"
Created run: docs/planning_runs/RUN-2026-05-10T15-30/
Prompt files:
  → prompts/plan_claude.md  (paste into Claude)
  → prompts/plan_chatgpt.md (paste into ChatGPT)
Save responses to:
  → claude_plan.md
  → chatgpt_plan.md
Then run: bequite models compare && bequite models merge --judge claude

$ # ... user pastes prompts into their chat windows; saves responses ...

$ bequite models compare
Generated: comparison.md  (8 topics; 2 conflicts; 1 user decision pending)

$ bequite models merge --judge claude
Generated merge prompt: prompts/merge_judge.md
After Claude's response, save to: merge_report.md
Then run: bequite models merge --confirm

$ # ... user pastes merge_judge.md into Claude; saves merge_report.md ...

$ bequite models merge --confirm
Generated: final_plan.md
Linked: specs/bookings/plan.md → docs/planning_runs/RUN-.../final_plan.md
```

### Example B — Team, direct-API, debate-and-merge

```bash
$ ANTHROPIC_API_KEY=... OPENAI_API_KEY=... \
  bequite plan --multi-model "Add SMS notifications to bookings" \
    --models claude-opus-4-7,gpt-5 \
    --mode debate \
    --judge claude-opus-4-7 \
    --direct-api

[1/4] Claude drafting plan ........................... ✓ (12s, $0.054)
[2/4] GPT-5 drafting plan ............................ ✓ ( 9s, $0.041)
[3/4] Claude reviewing GPT's plan .................... ✓ ( 8s, $0.039)
[4/4] GPT-5 reviewing Claude's plan .................. ✓ ( 7s, $0.033)
[5/5] Claude as judge producing final ................ ✓ (15s, $0.072)

Total: 5 calls, $0.239, 51 seconds
Receipts: docs/planning_runs/RUN-.../receipts/  (5 receipts, signed)
Final plan: docs/planning_runs/RUN-.../final_plan.md
Linked: specs/bookings-sms/plan.md
```

### Example C — Vibe-defense, red-team review

```bash
$ bequite plan --multi-model "Production launch checklist" \
    --models claude-opus-4-7 \
    --mode red-team
```

The red-team model attacks the existing plan. Produces `red_team_review.md` with severity-tagged findings.

## 19. Cross-references

- ADR: `.bequite/memory/decisions/ADR-012-multi-model-planning.md`
- Requirements: `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md`
- Constitution: `.bequite/memory/constitution.md` (Articles I, VI, VII)
- Existing routing: `skill/routing.json` (v0.2.0; v0.8.0 wired)
- Provider adapters: `cli/bequite/providers/` (v0.8.0)
- Cost ledger: `cli/bequite/cost_ledger.py` (v0.8.0)
- Receipts: `cli/bequite/receipts.py` (v0.7.0)
- New personas:
  - `skill/agents/multi-model-planning-orchestrator.md`
  - `skill/agents/model-judge.md`
  - `skill/agents/red-team-reviewer.md`
