# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-3` — Reproducibility + economics (covers v0.7.0 + v0.7.1 + v0.8.x).
- **Sub-version:** Just tagged `v0.7.0`. Next: **`v0.7.1`** (Signed receipts — ed25519).
- **Last green sub-version:** `v0.7.0` (Reproducibility receipts — `cli/bequite/receipts.py` + chain-hashed schema + `bequite cost` local-first + `bequite receipts {list,show,validate-chain,roll-up}` Click group + 10-test integration suite all passing on Python 3.14).
- **Mode:** Safe Mode (master §4)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0)
- **Constitution version:** `v1.2.0` (9 Iron Laws; Modes; 12 Doctrines; Definition-of-done)

## What this sub-version (just tagged) shipped

`v0.7.0` is **Reproducibility receipts** — the auditable record per phase transition.

Completed:
- ✅ `cli/bequite/receipts.py` (~510 lines, dataclass-based, stdlib-only runtime — no pydantic dependency at receipt-time):
  - Schema v1: `version` + `session_id` (UUID) + `phase` (P0..P7) + `timestamp_utc` (ISO 8601) + `model{name, reasoning_effort, fallback_model}` + `input{prompt_hash sha256, memory_snapshot_hash sha256}` + `output{diff_hash sha256, files_touched}` + `tools_invoked[{name, args_hash, exit}]` + `tests{command, exit, stdout_hash}` + `cost{input_tokens, output_tokens, usd}` + `doctrine[]` + `constitution_version` + `parent_receipt` (sha256 chain pointer).
  - `make_receipt()` — constructor; computes hashes (sha256 of prompt; sha256-of-files-and-paths for memory snapshot dir, skipping `.git/__pycache__/.venv/node_modules/.pytest_cache/.mypy_cache`; `git diff` for output + files-touched); generates UUID session_id; UTC timestamp.
  - `Receipt.content_hash()` — deterministic sha256 of canonical-JSON encoding (sorted keys, no whitespace, None-stripped).
  - `ReceiptStore` — local filesystem store at `.bequite/receipts/<sha>-<phase>.json`. Methods: `write` / `list_all` / `get`.
  - `validate_chain()` — checks missing-parent + causality (parent.ts ≤ child.ts) + cycle.
  - `replay_check()` — re-derives hashes; reports prompt or memory mismatches.
  - `roll_up_by_session/phase/day()` — token + USD aggregations with first/last timestamps + active doctrines.
  - CLI: `python -m bequite.receipts {emit,list,show,validate-chain,roll-up}` with full subcommand args.
- ✅ `cli/bequite/__main__.py` — `bequite cost` reads local receipts first (offline-first per Article III) with skill-dispatch fallback only when no receipts. New `bequite receipts {list,show,validate-chain,roll-up}` Click group.
- ✅ `tests/integration/receipts/test_receipts_smoke.py` — 10-test integration suite (emit + list roundtrip; chain validation valid/missing-parent; replay pass/tamper-rejection; roll-ups by session/phase/day; content-hash determinism; full Receipt round-trip). All 10 tests pass.
- ✅ `tests/integration/receipts/README.md` — explains coverage + run modes + future v0.7.1 (signing) coverage path.
- ✅ `cli/bequite/__init__.py::__version__` → `0.7.0`. `cli/pyproject.toml::version` → `0.7.0`.
- ✅ `CHANGELOG.md` — v0.7.0 entry added.

## Next sub-version

After `v0.7.0`: **`v0.7.1` — Signed receipts (ed25519)**.

Tasks for v0.7.1:
1. `cli/bequite/receipts_signing.py` — keypair generation (cryptography lib already in deps); sign + verify primitives.
2. Refresh `Receipt` schema with optional `signature` field (additive, backward-compatible).
3. Wire `bequite init` to call `generate_keypair`.
4. Add `bequite verify-receipts` command — validates signature + chain.
5. Append `.bequite/.keys/` to `.gitignore`.
6. 3 integration tests: signing roundtrip; tampered-body rejected; unsigned-in-strict-mode rejected.
7. Bumps: `__init__.py` + `pyproject.toml` → `0.7.1`; CHANGELOG entry; activeContext + progress + recovery; commit + tag.

After v0.7.1: v0.8.0 (multi-model live: AiProvider adapters for Anthropic + OpenAI + Google + DeepSeek + Ollama with cost ceiling enforcement) → v0.8.1 (live pricing + 24h cache + offline fallback) → v0.9.0 (3 example projects) → v0.9.1 (e2e harness) → v0.10.0 (auto-mode state machine + safety rails + heartbeat) → v0.10.1 (auto-mode hardening) → v0.11.0 (MENA bilingual) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0** (final). **12 sub-versions remain.**

## Open questions (none blocking)

- E1 — GitHub org / repo: `xpShawky/BeQuite` confirmed (Ahmed created; remote configured `origin = https://github.com/xpShawky/BeQuite.git`; NOT pushed).
- E2 — PyPI package name + ownership — blocks v0.5.0 PyPI release / v1.0.0 final.
- E3 — Studio (v2.0.0+) timing — after v1.0.0 ships.
- E4 — Telemetry policy — off entirely; pending ADR-002 in v0.7.0 (was deferred; receipts stay local-first by default).
- E5 — Doctrine distribution model (community fork org) — pending in v0.12.0.
- E6 — MENA bilingual Researcher seeds — Ahmed seeds list at v0.11.0.
- E7 — Codex 5.5 review-mode role — review-only default; pending v0.8.0.

None of these block v0.7.1+ progress.

## Cost / wall-clock telemetry (this session)

Receipts are now emittable but not yet auto-emitted (auto-mode lands v0.10.0). Manual emission via `bequite receipts emit` works.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
