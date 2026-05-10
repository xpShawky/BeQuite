"""Integration smoke test for cli/bequite/router.py + providers/ + cost_ledger.py (v0.8.0).

Runnable two ways:
    1. Direct: `PYTHONIOENCODING=utf-8 python tests/integration/router/test_router_smoke.py`
    2. Pytest: `PYTHONIOENCODING=utf-8 python -m pytest tests/integration/router/`

Tests use a TestProvider that returns canned Completions to keep the suite
hermetic (no network, no API keys required).
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import sys
import tempfile

# Make `bequite` importable from cli/ when run directly.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.cost_ledger import (  # noqa: E402
    DEFAULT_LEDGER_PATH,
    read,
    session_summary,
    update,
)
from bequite.providers import Completion, REGISTERED_PROVIDERS, get_provider  # noqa: E402
from bequite.providers.anthropic import AnthropicProvider  # noqa: E402
from bequite.providers.openai import OpenAIProvider  # noqa: E402
from bequite.router import (  # noqa: E402
    Route,
    _provider_for_model,
    dispatch,
    find_routing_path,
    select_route,
)


# --------------------------------------------------------------- TestProvider


@dataclasses.dataclass
class TestProvider:
    """Canned-response provider for hermetic tests."""

    name: str = "test"
    available: bool = True
    canned_text: str = "ok"
    canned_input_tokens: int = 100
    canned_output_tokens: int = 50
    canned_usd: float = 0.005

    def is_available(self) -> bool:
        return self.available

    def supports_model(self, model: str) -> bool:
        return True

    def estimate_cost_usd(self, model: str, in_tok: int, out_tok: int) -> float:
        return self.canned_usd

    def complete(self, *, model, prompt, system=None, max_input_tokens=100_000,
                 max_output_tokens=8_000, reasoning_effort="default", timeout_s=120.0):
        return Completion(
            text=self.canned_text,
            input_tokens=self.canned_input_tokens,
            output_tokens=self.canned_output_tokens,
            finish_reason="stop",
            model=model,
            provider=self.name,
            usd_cost=self.canned_usd,
        )


def _all_test_factory(provider: TestProvider):
    """Provider factory that always returns the same TestProvider regardless of name."""
    def factory(name: str):
        return dataclasses.replace(provider, name=name)
    return factory


# --------------------------------------------------------------- tests


def test_provider_registry_is_complete() -> None:
    assert set(REGISTERED_PROVIDERS) == {"anthropic", "openai", "google", "deepseek", "ollama"}


def test_each_provider_implements_protocol() -> None:
    for name in REGISTERED_PROVIDERS:
        p = get_provider(name)
        assert hasattr(p, "is_available")
        assert hasattr(p, "supports_model")
        assert hasattr(p, "estimate_cost_usd")
        assert hasattr(p, "complete")
        assert p.name == name


def test_provider_for_model_heuristics() -> None:
    assert _provider_for_model("claude-opus-4-7") == "anthropic"
    assert _provider_for_model("claude-sonnet-4-6") == "anthropic"
    assert _provider_for_model("gpt-5") == "openai"
    assert _provider_for_model("gpt-5-mini") == "openai"
    assert _provider_for_model("o3-mini") == "openai"
    assert _provider_for_model("gemini-2.5-pro") == "google"
    assert _provider_for_model("deepseek-coder") == "deepseek"
    assert _provider_for_model("llama-3.3-70b") == "ollama"
    assert _provider_for_model("mistral-large") == "ollama"


def test_select_route_phase_persona_exact() -> None:
    """P5 backend-engineer → claude-sonnet-4-6 medium."""
    route = select_route(phase="P5", persona="backend-engineer")
    assert route.model == "claude-sonnet-4-6"
    assert route.reasoning_effort == "medium"
    assert route.provider == "anthropic"
    assert route.fallback_model == "gpt-5-mini"


def test_select_route_reviewer_uses_opus_xhigh() -> None:
    """Aider architect-mode pattern: reviewer = frontier model + xhigh effort."""
    route = select_route(phase="P5", persona="reviewer")
    assert route.model == "claude-opus-4-7"
    assert route.reasoning_effort == "xhigh"


def test_select_route_skeptic_uses_any_boundary() -> None:
    """Skeptic uses phase='any-boundary'; matches via persona+special-phase rule."""
    route = select_route(phase="P3", persona="skeptic")
    assert route.persona == "skeptic"
    assert route.model == "claude-opus-4-7"


def test_select_route_unknown_falls_back_to_orchestrator() -> None:
    route = select_route(phase="nonexistent", persona="nonexistent-persona")
    assert route.model.startswith("claude-")  # safe default


def test_anthropic_pricing_estimates() -> None:
    p = AnthropicProvider()
    # opus: 1M in @ $15 + 100k out @ $75 = $15 + $7.5 = $22.5
    assert abs(p.estimate_cost_usd("claude-opus-4-7", 1_000_000, 100_000) - 22.5) < 1e-9
    # sonnet: 1M in @ $3 + 100k out @ $15 = $3 + $1.5 = $4.5
    assert abs(p.estimate_cost_usd("claude-sonnet-4-6", 1_000_000, 100_000) - 4.5) < 1e-9
    # haiku: 1M in @ $0.80 + 100k out @ $4.0 = $0.80 + $0.40 = $1.20
    assert abs(p.estimate_cost_usd("claude-haiku-4-5", 1_000_000, 100_000) - 1.20) < 1e-9


def test_openai_pricing_estimates() -> None:
    p = OpenAIProvider()
    # gpt-5: 1M in @ $12 + 100k out @ $50 = $12 + $5 = $17
    assert abs(p.estimate_cost_usd("gpt-5", 1_000_000, 100_000) - 17.0) < 1e-9


def test_dispatch_with_test_provider_returns_completion() -> None:
    tp = TestProvider(canned_text="hello world", canned_usd=0.123)
    completion, route = dispatch(
        phase="P5", persona="backend-engineer", prompt="write a hello world",
        provider_factory=_all_test_factory(tp),
        update_ledger=False,
    )
    assert completion.text == "hello world"
    assert completion.usd_cost == 0.123
    assert route.model == "claude-sonnet-4-6"


def test_dispatch_falls_back_when_primary_unavailable() -> None:
    """Primary unavailable → fallback model picked."""
    def factory(name: str):
        if name == "anthropic":
            return TestProvider(name="anthropic", available=False)
        # Fallback (openai for gpt-5-mini) is available.
        return TestProvider(name=name, available=True, canned_text="fallback-text")

    completion, route = dispatch(
        phase="P5", persona="backend-engineer", prompt="x",
        provider_factory=factory, update_ledger=False,
    )
    assert route.used_fallback is True
    assert route.model == "gpt-5-mini"
    assert route.provider == "openai"
    assert completion.text == "fallback-text"


def test_dispatch_returns_error_when_both_unavailable() -> None:
    def factory(name: str):
        return TestProvider(name=name, available=False)
    completion, route = dispatch(
        phase="P5", persona="backend-engineer", prompt="x",
        provider_factory=factory, update_ledger=False,
    )
    assert completion.finish_reason == "error"
    assert "unavailable" in (completion.error or "")


def test_cost_ledger_accumulates_across_calls() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        # Make 3 calls; check totals.
        for usd in (0.01, 0.02, 0.03):
            comp = Completion(
                text="x", input_tokens=100, output_tokens=50,
                finish_reason="stop", model="m", provider="test",
                usd_cost=usd,
            )
            update(repo_root=td, completion=comp, phase="P5", persona="backend-engineer")
        data = read(td)
        assert abs(data["session_total_usd"] - 0.06) < 1e-9
        assert data["session_total_tokens"] == 3 * 150
        assert data["calls_this_session"] == 3
        assert len(data["calls"]) == 3
        # Schema sanity: hook reads `session_total_usd` directly.
        assert "session_total_usd" in data


def test_cost_ledger_session_summary() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        comp = Completion(
            text="x", input_tokens=200, output_tokens=80,
            finish_reason="stop", model="m", provider="test",
            usd_cost=0.05,
        )
        update(repo_root=td, completion=comp, phase="P0", persona="research-analyst")
        s = session_summary(td)
        assert s["session_total_usd"] == 0.05
        assert s["session_total_tokens"] == 280
        assert s["calls_this_session"] == 1
        assert s["session_id"]


def test_dispatch_updates_ledger_when_enabled() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        tp = TestProvider(canned_usd=0.075)
        completion, route = dispatch(
            phase="P5", persona="backend-engineer", prompt="x",
            provider_factory=_all_test_factory(tp),
            repo_root=td,
            update_ledger=True,
        )
        ledger = read(td)
        assert abs(ledger["session_total_usd"] - 0.075) < 1e-9
        assert ledger["calls_this_session"] == 1


def _run_all() -> int:
    tests = [
        test_provider_registry_is_complete,
        test_each_provider_implements_protocol,
        test_provider_for_model_heuristics,
        test_select_route_phase_persona_exact,
        test_select_route_reviewer_uses_opus_xhigh,
        test_select_route_skeptic_uses_any_boundary,
        test_select_route_unknown_falls_back_to_orchestrator,
        test_anthropic_pricing_estimates,
        test_openai_pricing_estimates,
        test_dispatch_with_test_provider_returns_completion,
        test_dispatch_falls_back_when_primary_unavailable,
        test_dispatch_returns_error_when_both_unavailable,
        test_cost_ledger_accumulates_across_calls,
        test_cost_ledger_session_summary,
        test_dispatch_updates_ledger_when_enabled,
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
