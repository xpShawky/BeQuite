# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-3` complete (Reproducibility + economics: v0.7.0 + v0.7.1 + v0.8.0 + v0.8.1). Next phase: `phase-4` (Examples + e2e harness; v0.9.0 + v0.9.1).
- **Sub-version:** Just tagged `v0.8.1`. Next: **`v0.9.0`** (Three example projects).
- **Last green sub-version:** `v0.8.1` (Live pricing fetch — `cli/bequite/pricing.py` + cache + vendored fallback + adapter wiring + 14-test integration suite all passing on Python 3.14; combined receipts+signing+router+pricing 48/48 green).
- **Mode:** Safe Mode (master §4)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0)
- **Constitution version:** `v1.2.0` (9 Iron Laws; Modes; 12 Doctrines; Definition-of-done)

## What this sub-version (just tagged) shipped

`v0.8.1` is **Live pricing fetch (best-effort)** — completes the cost-aware multi-model routing started in v0.8.0.

Completed:
- ✅ `cli/bequite/pricing.py` (~330 lines) — vendor pricing fetch + cache + fallback infrastructure:
  - Cache shape at `.bequite/cache/pricing.json` with `fetched_utc` + `ttl_hours` + `models{model: {input, output, source}}` + `warnings`.
  - `fetch_pricing(provider=None)` best-effort GET with httpx (User-Agent `bequite-pricing-probe/0.8.1`, follow_redirects, 10s timeout). Returns partial dict on parse failure rather than raising.
  - `extract_prices_from_html(html)` regex-based paragraph parser. Pairs nearest model + 2 prices.
  - `pricing_for(model)` returns `(rates, source)` where source ∈ {live, stale, fallback, unknown}.
  - `estimate_cost_usd(model, in_tokens, out_tokens)` convenience wrapper.
  - CLI `python -m bequite.pricing {refresh,show,list}`.
- ✅ `skill/references/pricing-table.md` — vendored May-2026 snapshot (5 model providers + hosting + auth + database tiers).
- ✅ Provider adapters (`anthropic.py`, `openai.py`, `google.py`, `deepseek.py`) updated: `estimate_cost_usd()` consults `pricing.pricing_for()` first; soft-import preserves graceful degradation.
- ✅ `bequite pricing {show,list,refresh}` Click group.
- ✅ `tests/integration/pricing/test_pricing_smoke.py` — 14 tests covering fallback / cache freshness / stale-marking / unknown handling / regex extraction / adapter wiring. All 14 pass on Python 3.14.
- ✅ Combined integration suite: receipts (10) + signing (9) + router (15) + pricing (14) = **48/48 green**.
- ✅ `cli/bequite/__init__.py::__version__` → `0.8.1`. `cli/pyproject.toml::version` → `0.8.1`.
- ✅ `CHANGELOG.md` — v0.8.1 entry added.

## Next sub-version

After `v0.8.1`: **`v0.9.0` — Three example projects**.

Tasks for v0.9.0:
1. `examples/01-bookings-saas/` — Next.js + Hono + Supabase + Clerk + Vercel; Doctrine `default-web-saas`; bookings flow with admin + customer.
2. `examples/02-ai-tool-wrapper/` — Python CLI + Anthropic SDK; Doctrine `cli-tool`; markdown summariser.
3. `examples/03-tauri-note-app/` — Tauri v2 + SvelteKit + SQLite; Doctrine `desktop-tauri`; local-first notes with OS keychain.
4. Each ships full `.bequite/` tree + specs + receipts + HANDOFF.md.
5. Acceptance: `bequite verify` green per example; HANDOFF hand-runnable.
6. Bumps: `__init__.py` + `pyproject.toml` → `0.9.0`. CHANGELOG. State. Commit + tag.

After v0.9.0: v0.9.1 (e2e harness) → v0.10.0 (auto-mode state machine + safety rails + heartbeat) → v0.10.1 (auto-hardening) → v0.11.0 (MENA) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0**. **9 sub-versions remain.**

## Open questions (none blocking)

- E1 — GitHub org / repo: `xpShawky/BeQuite` confirmed; remote configured; NOT pushed.
- E2 — PyPI package name + ownership — blocks v1.0.0 final.
- E3 — Studio (v2.0.0+) timing — after v1.0.0.
- E4 — Telemetry policy — off by default; receipts stay local-first.
- E5 — Doctrine distribution model — pending in v0.12.0.
- E6 — MENA bilingual Researcher seeds — Ahmed seeds list at v0.11.0.
- E7 — Codex 5.5 review-mode role — review-only default; pending v0.10.x.
- E8 — Strict-mode default for receipt signing — flip in v0.10.0 when auto-mode wires emit-with-signing.

None of these block v0.9.0+ progress.

## Cost / wall-clock telemetry (this session)

Receipts (v0.7.0) + signing (v0.7.1) + multi-model routing (v0.8.0) + cost ledger (v0.8.0) + live pricing (v0.8.1) all operational. The full economics stack is in place — `bequite ledger show` displays the running session cost; `bequite pricing list` shows per-model rates with source.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
