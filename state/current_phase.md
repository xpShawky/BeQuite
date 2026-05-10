# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-3` — Reproducibility + economics (v0.7.0 + v0.7.1 done; v0.8.x next).
- **Sub-version:** Just tagged `v0.7.1`. Next: **`v0.8.0`** (Multi-model routing — cost-aware).
- **Last green sub-version:** `v0.7.1` (Signed receipts — ed25519 keypair on init + sign-at-emission + `bequite verify-receipts` + 9-test signing integration suite all passing; combined receipts+signing 19/19 green on Python 3.14).
- **Mode:** Safe Mode (master §4)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0)
- **Constitution version:** `v1.2.0` (9 Iron Laws; Modes; 12 Doctrines; Definition-of-done)

## What this sub-version (just tagged) shipped

`v0.7.1` is **Signed receipts** — ed25519 sign-and-verify on top of v0.7.0's chain-hashed receipts.

Completed:
- ✅ `cli/bequite/receipts_signing.py` — ed25519 sign-and-verify layer:
  - `generate_keypair(project_dir, overwrite=False)` — creates per-project keypair via `cryptography.hazmat.primitives.asymmetric.ed25519`. Private at `<project>/.bequite/.keys/private.pem` (mode 0600 best-effort on POSIX; gitignored). Public at `<project>/.bequite/keys/public.pem` (mode 0644; committed). Refuses overwrite by default; `overwrite=True` regenerates with explicit warning.
  - `load_private_key/load_public_key` — typed PEM loaders.
  - `sign_dict(receipt_dict, private_key)` — returns copy with `signature` (base64-ed25519) added. Signs over canonical-JSON-without-signature (sidesteps chicken-and-egg).
  - `verify_dict(receipt_dict, public_key)` — recovers signature, recomputes payload, verifies. Returns `(ok, reason)`.
  - `verify_receipts_directory(receipts_dir, public_key, strict)` — walks `*.json`; reports counts (total / signed_valid / signed_invalid / unsigned). Strict mode rejects unsigned.
  - CLI: `python -m bequite.receipts_signing {keygen,sign,verify}`.
- ✅ `Receipt` schema additive bump — optional `signature: Optional[str] = None` field (last position; backward-compatible).
- ✅ `ReceiptStore.write(receipt, sign_with=None)` — opt-in signing at write-time. Filename remains v0.7.0 deterministic-from-inputs (allows key rotation without breaking chain pointers).
- ✅ `bequite verify-receipts [--strict]` Click command — signature + chain validation; refuses without public key (suggests `bequite init` or `bequite keygen`).
- ✅ `bequite keygen [--overwrite]` Click command — direct keypair generation with gitignore + commit reminders.
- ✅ `bequite init` extension — auto-calls `generate_keypair` on scaffold; appends `.bequite/.keys/` patterns to project's `.gitignore`. Init summary now shows keypair status.
- ✅ `tests/integration/receipts/test_signing_smoke.py` — 9-test integration suite covering: keygen creates files / refuses overwrite / overwrites when explicit; sign-verify roundtrip; tampered-body rejected; unsigned-strict-fails; unsigned-lenient-tolerated; ReceiptStore.write(sign_with=) emits signed; cross-paste-signature mismatch detected. All 9 pass on Python 3.14.
- ✅ Combined receipts + signing test suite: 19/19 green.
- ✅ `cli/bequite/__init__.py::__version__` → `0.7.1`. `cli/pyproject.toml::version` → `0.7.1`.
- ✅ `CHANGELOG.md` — v0.7.1 entry added.

## Next sub-version

After `v0.7.1`: **`v0.8.0` — Multi-model routing (cost-aware)**.

Tasks for v0.8.0:
1. Refresh `skill/routing.json` schema with cost-aware fields (model + reasoning_effort + fallback_model + max_input_tokens + max_output_tokens per phase × persona).
2. Provider adapters in `cli/bequite/providers/`:
   - `anthropic.py` (primary; `anthropic` SDK already in deps)
   - `openai.py` (planner alt; `bequite[openai]` extra already declared)
   - `google.py` (Gemini for free-tier doc gen; `bequite[google]` extra)
   - `deepseek.py` (cheap implementer; OpenAI-compatible API)
   - `ollama.py` (offline mode; HTTP localhost)
3. `skill_loader.py` reads routing → picks model per call.
4. Wire `stop-cost-budget.sh` for `bequite.config.toml::cost.session_max_usd` ceiling enforcement.
5. Receipts emit per model invocation (chain + signing already operational).
6. Routing-test fixture: Sonnet for implementer + Opus for reviewer.
7. Cost-ceiling test: synthetic receipts summing past threshold trips stop hook.
8. Bumps: `__init__.py` + `pyproject.toml` → `0.8.0`; CHANGELOG; activeContext + progress + recovery; commit + tag.

After v0.8.0: v0.8.1 (live pricing) → v0.9.0 (3 examples) → v0.9.1 (e2e harness) → v0.10.0 (auto-mode) → v0.10.1 (auto-hardening) → v0.11.0 (MENA) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0** (final). **11 sub-versions remain.**

## Open questions (none blocking)

- E1 — GitHub org / repo: `xpShawky/BeQuite` confirmed (Ahmed created; remote configured `origin = https://github.com/xpShawky/BeQuite.git`; NOT pushed).
- E2 — PyPI package name + ownership — blocks v0.5.0 PyPI release / v1.0.0 final.
- E3 — Studio (v2.0.0+) timing — after v1.0.0 ships.
- E4 — Telemetry policy — off entirely; receipts stay local-first by default.
- E5 — Doctrine distribution model (community fork org) — pending in v0.12.0.
- E6 — MENA bilingual Researcher seeds — Ahmed seeds list at v0.11.0.
- E7 — Codex 5.5 review-mode role — review-only default; pending v0.8.0.
- E8 — Strict-mode default for receipt signing — flip to default in v0.10.0 when auto-mode wires emit-with-signing as the only path.

None of these block v0.8.0+ progress.

## Cost / wall-clock telemetry (this session)

Receipts (v0.7.0) + signing (v0.7.1) operational; auto-emit-on-phase-transition lands v0.10.0.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
