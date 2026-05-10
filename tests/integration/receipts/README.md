# tests/integration/receipts/

> Integration tests for `cli/bequite/receipts.py` (v0.7.0+). Exercise the full emit → list → validate-chain → replay → roll-up roundtrip.

## What's covered

- **Receipt construction.** `make_receipt()` produces a Receipt with valid sha256 hashes for prompt + memory snapshot + diff; UUID session_id; ISO 8601 timestamp.
- **Storage roundtrip.** `ReceiptStore.write()` writes canonical JSON; `list_all()` deserializes back to identical Receipts.
- **Chain validation.** Causally-ordered chain validates; missing-parent detected; out-of-order timestamp detected.
- **Replay.** Original prompt + memory directory hash matches recorded hashes; tampered prompt fails replay.
- **Roll-ups.** Per-session / per-phase / per-day roll-ups sum to expected totals.

## Running locally

From `cli/` directory:

```bash
PYTHONIOENCODING=utf-8 python -m pytest ../tests/integration/receipts/ -v
```

(Pytest config lands in `cli/pyproject.toml::[tool.pytest.ini_options]` per v0.5.0.)

## Smoke-test (no pytest required)

The test in `test_receipts_smoke.py` is also runnable directly:

```bash
PYTHONIOENCODING=utf-8 python ../tests/integration/receipts/test_receipts_smoke.py
```

## Future coverage (v0.7.1+)

- ed25519 signature on emission.
- ed25519 verification via `bequite verify-receipts`.
- Tampered receipt body — chain still validates content_hash but signature fails.
- Per-project keypair generation on `bequite init`.

## Cross-references

- Module: `cli/bequite/receipts.py`
- CLI: `bequite cost` + `bequite receipts {list,show,validate-chain,roll-up}`
- Schema doc (cross-ref): `skill/references/playwright-walks.md::5. Receipt schema`
- Plan: `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md` v0.7.0 row
