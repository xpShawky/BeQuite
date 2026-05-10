"""Integration smoke test for cli/bequite/pricing.py (BeQuite v0.8.1).

Hermetic: no live network calls. The fetch path is exercised via a stubbed
`fetch_pricing` only when explicitly tested. Cache + fallback paths are
exercised against tempdirs.

Runnable two ways:
    1. Direct: `PYTHONIOENCODING=utf-8 python tests/integration/pricing/test_pricing_smoke.py`
    2. Pytest: `PYTHONIOENCODING=utf-8 python -m pytest tests/integration/pricing/`
"""

from __future__ import annotations

import datetime as _dt
import json
import pathlib
import sys
import tempfile

# Make `bequite` importable from cli/ when run directly.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.pricing import (  # noqa: E402
    DEFAULT_TTL_HOURS,
    cache_age_hours,
    estimate_cost_usd,
    extract_prices_from_html,
    fallback_pricing,
    is_cache_fresh,
    pricing_for,
    read_cache,
    write_cache,
)


def test_fallback_pricing_known_models() -> None:
    p = fallback_pricing("claude-opus-4-7")
    assert p == {"input": 15.00, "output": 75.00}
    p = fallback_pricing("gpt-5-mini")
    assert p == {"input": 0.50, "output": 2.00}
    p = fallback_pricing("gemini-2.5-flash")
    assert p == {"input": 0.30, "output": 2.50}
    p = fallback_pricing("deepseek-coder")
    assert p == {"input": 0.27, "output": 1.10}


def test_fallback_pricing_unknown_returns_none() -> None:
    assert fallback_pricing("definitely-not-a-real-model") is None


def test_pricing_for_falls_back_when_cache_empty() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        rates, source = pricing_for("claude-opus-4-7", repo_root=td)
        assert source == "fallback"
        assert rates == {"input": 15.00, "output": 75.00}


def test_pricing_for_unknown_model_returns_unknown() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        rates, source = pricing_for("not-a-model", repo_root=td)
        assert rates is None
        assert source == "unknown"


def test_pricing_for_uses_fresh_cache() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        cache_path = td / ".bequite" / "cache" / "pricing.json"
        # Seed cache with fresh fetched_utc + a custom rate.
        now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
        write_cache(cache_path, {
            "fetched_utc": now,
            "ttl_hours": 24,
            "models": {"claude-opus-4-7": {"input": 99.99, "output": 199.99, "source": "live"}},
        })
        rates, source = pricing_for("claude-opus-4-7", repo_root=td)
        assert source == "live"
        assert rates["input"] == 99.99
        assert rates["output"] == 199.99


def test_pricing_for_marks_stale_when_cache_old() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        cache_path = td / ".bequite" / "cache" / "pricing.json"
        # Seed cache with fetched_utc 100h ago.
        old = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=100)).isoformat(timespec="seconds")
        write_cache(cache_path, {
            "fetched_utc": old,
            "ttl_hours": 24,
            "models": {"claude-opus-4-7": {"input": 12.34, "output": 56.78, "source": "live"}},
        })
        rates, source = pricing_for("claude-opus-4-7", repo_root=td)
        assert source == "stale"
        assert rates["input"] == 12.34


def test_pricing_for_unknown_in_cache_falls_back_to_fallback_table() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        cache_path = td / ".bequite" / "cache" / "pricing.json"
        now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
        write_cache(cache_path, {
            "fetched_utc": now,
            "ttl_hours": 24,
            "models": {"claude-opus-4-7": {"input": 50, "output": 100, "source": "live"}},
        })
        # gpt-5 not in cache → should fall back to hard-coded.
        rates, source = pricing_for("gpt-5", repo_root=td)
        assert source == "fallback"
        assert rates == {"input": 12.00, "output": 50.00}


def test_estimate_cost_usd_uses_pricing_for() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        # 1M input + 100k output @ opus = 15 + 7.5 = 22.5
        usd, source = estimate_cost_usd("claude-opus-4-7", 1_000_000, 100_000, repo_root=td)
        assert abs(usd - 22.5) < 1e-9
        assert source == "fallback"


def test_estimate_cost_usd_unknown_returns_zero() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        usd, source = estimate_cost_usd("not-a-model", 100, 50, repo_root=td)
        assert usd == 0.0
        assert source == "unknown"


def test_cache_age_hours_missing_returns_inf() -> None:
    assert cache_age_hours({}) == float("inf")
    assert cache_age_hours({"fetched_utc": "not-an-iso"}) == float("inf")


def test_is_cache_fresh_under_ttl() -> None:
    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    assert is_cache_fresh({"fetched_utc": now}, ttl_hours=24)


def test_is_cache_fresh_over_ttl() -> None:
    old = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=48)).isoformat(timespec="seconds")
    assert not is_cache_fresh({"fetched_utc": old}, ttl_hours=24)


def test_extract_prices_from_html_finds_paired_model_and_prices() -> None:
    html = """
    <html><body>
    <p>claude-opus-4-7 costs $15.00 / 1M input tokens and $75.00 / 1M output tokens.</p>
    <p>gpt-5-mini is $0.50 per 1M input and $2.00 per 1M output.</p>
    </body></html>
    """
    out = extract_prices_from_html(html)
    assert "claude-opus-4-7" in out
    assert out["claude-opus-4-7"]["input"] == 15.00
    assert out["claude-opus-4-7"]["output"] == 75.00
    assert "gpt-5-mini" in out
    assert out["gpt-5-mini"]["input"] == 0.50
    assert out["gpt-5-mini"]["output"] == 2.00


def test_adapter_estimate_cost_usd_consults_pricing_module() -> None:
    """When pricing module is importable, AnthropicProvider.estimate_cost_usd uses pricing_for."""
    from bequite.providers.anthropic import AnthropicProvider
    p = AnthropicProvider()
    # Without a temp cache, it falls back to vendored — same answer either way.
    usd = p.estimate_cost_usd("claude-opus-4-7", 1_000_000, 100_000)
    assert abs(usd - 22.5) < 1e-9


def _run_all() -> int:
    tests = [
        test_fallback_pricing_known_models,
        test_fallback_pricing_unknown_returns_none,
        test_pricing_for_falls_back_when_cache_empty,
        test_pricing_for_unknown_model_returns_unknown,
        test_pricing_for_uses_fresh_cache,
        test_pricing_for_marks_stale_when_cache_old,
        test_pricing_for_unknown_in_cache_falls_back_to_fallback_table,
        test_estimate_cost_usd_uses_pricing_for,
        test_estimate_cost_usd_unknown_returns_zero,
        test_cache_age_hours_missing_returns_inf,
        test_is_cache_fresh_under_ttl,
        test_is_cache_fresh_over_ttl,
        test_extract_prices_from_html_finds_paired_model_and_prices,
        test_adapter_estimate_cost_usd_consults_pricing_module,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures += 1
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_run_all())
