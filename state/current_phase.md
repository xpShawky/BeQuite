# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-3` — Reproducibility + economics (v0.7.0 + v0.7.1 + v0.8.0 done; v0.8.1 + v0.9.x next).
- **Sub-version:** Just tagged `v0.8.0`. Next: **`v0.8.1`** (Live pricing fetch — best-effort).
- **Last green sub-version:** `v0.8.0` (Multi-model routing live — 5 provider adapters + router + cost ledger + 15-test integration suite all passing on Python 3.14; combined receipts+signing+router 34/34 green).
- **Mode:** Safe Mode (master §4)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0)
- **Constitution version:** `v1.2.0` (9 Iron Laws; Modes; 12 Doctrines; Definition-of-done)

## What this sub-version (just tagged) shipped

`v0.8.0` is **Multi-model routing live** — the `routing.json` schema authored in v0.2.0 becomes operational.

Completed:
- ✅ `cli/bequite/providers/__init__.py` — `AiProvider` Protocol (4 methods: is_available / supports_model / estimate_cost_usd / complete) + `Completion` dataclass + `REGISTERED_PROVIDERS` tuple + `get_provider(name)` lazy-import factory.
- ✅ 5 thin adapters in `cli/bequite/providers/`:
  - `anthropic.py` — Claude family; pricing $15/$3/$0.80 per 1M (opus/sonnet/haiku).
  - `openai.py` — GPT-5 / o3 family; pricing $12/$0.50/$10. Reusable as DeepSeek base (OpenAI-compatible API).
  - `google.py` — Gemini via `google-genai` SDK; pricing $1.25/$0.30 (pro/flash).
  - `deepseek.py` — Subclasses OpenAIProvider with `base_url=https://api.deepseek.com/v1`; pricing $0.27/$0.55.
  - `ollama.py` — HTTP localhost (`http://localhost:11434`) via httpx; **no vendor SDK required**; cost always $0.00.
  - **Graceful degradation:** every adapter is importable WITHOUT its vendor SDK; `is_available()` returns False instead of raising.
- ✅ `cli/bequite/router.py`:
  - `Route` dataclass.
  - `_provider_for_model()` heuristic.
  - `find_routing_path()` (project-local override at `.bequite/routing-overrides.json` first, then `skill/routing.json`).
  - `select_route()` with match priority: exact (phase, persona) → (persona, special-phase: any/any-boundary/always-on/any-mode) → (phase, orchestrator) → orchestrator catch-all → safe defaults.
  - `dispatch()` with auto-fallback to `fallback_model` on primary unavailability; calls `cost_ledger.update()` on every call.
- ✅ `cli/bequite/cost_ledger.py` — feeds `.bequite/cache/cost-ledger.json` so `stop-cost-budget.sh` (v0.3.0 hook) is operational. Methods: `update`, `read`, `session_summary`, `reset_session`. Per-process session_id auto-resets totals.
- ✅ `bequite route show --phase <P> --persona <X>` Click command — JSON of resolved route.
- ✅ `bequite route list` — every row in routing.json (table format).
- ✅ `bequite route providers` — availability probe per provider.
- ✅ `bequite ledger show` — current session summary.
- ✅ `bequite ledger reset` — reset session totals.
- ✅ `tests/integration/router/test_router_smoke.py` — 15-test integration suite covering: provider Protocol conformance, model heuristics, route selection (exact + special-phase + fallback + catch-all), pricing estimates per provider, dispatch with TestProvider, dispatch fallback when primary unavailable, dispatch error when both unavailable, cost ledger accumulation across calls, ledger session_summary surface, dispatch updates ledger when enabled. All 15 pass on Python 3.14.
- ✅ Combined integration suite: receipts (10) + signing (9) + router (15) = **34/34 green**.
- ✅ `cli/bequite/__init__.py::__version__` → `0.8.0`. `cli/pyproject.toml::version` → `0.8.0`.
- ✅ `CHANGELOG.md` — v0.8.0 entry added.

## Next sub-version

After `v0.8.0`: **`v0.8.1` — Live pricing fetch (best-effort)**.

Tasks for v0.8.1:
1. `cli/bequite/pricing.py` — WebFetch vendor pricing pages; 24h cache; offline fallback.
2. Surface pricing-changed warnings in `bequite stack` + `bequite cost`.
3. Provider adapters' `estimate_cost_usd()` consult live cache before hard-coded fallback.
4. Pricing-fetch unit test (4+ providers).
5. Offline-mode graceful fallback test.
6. Bumps: `__init__.py` + `pyproject.toml` → `0.8.1`. CHANGELOG. State. Commit + tag.

After v0.8.1: v0.9.0 (3 examples) → v0.9.1 (e2e harness) → v0.10.0 (auto-mode) → v0.10.1 (auto-hardening) → v0.11.0 (MENA) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0**. **10 sub-versions remain.**

## Open questions (none blocking)

- E1 — GitHub org / repo: `xpShawky/BeQuite` confirmed; remote configured; NOT pushed.
- E2 — PyPI package name + ownership — blocks v1.0.0 final.
- E3 — Studio (v2.0.0+) timing — after v1.0.0.
- E4 — Telemetry policy — off by default; receipts stay local-first.
- E5 — Doctrine distribution model — pending in v0.12.0.
- E6 — MENA bilingual Researcher seeds — Ahmed seeds list at v0.11.0.
- E7 — Codex 5.5 review-mode role — review-only default; pending v0.8.0+.
- E8 — Strict-mode default for receipt signing — flip in v0.10.0 when auto-mode wires emit-with-signing.

None of these block v0.8.1+ progress.

## Cost / wall-clock telemetry (this session)

Receipts (v0.7.0) + signing (v0.7.1) operational. Multi-model routing + cost ledger (v0.8.0) operational — `bequite ledger show` displays the current session's cost. `stop-cost-budget.sh` (v0.3.0 hook) reads the ledger now that it's populated.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
