"""bequite.providers — AiProvider adapters (v0.8.0).

Cost-aware multi-model routing per `skill/routing.json`. Each provider is a
thin adapter conforming to the `AiProvider` Protocol; the `router` module
picks one based on phase + persona + availability + ceiling.

Per AkitaOnRails 2026: forced multi-model on cohesive tasks loses to solo
frontier. Auto-mode default routing reflects that — Skeptic runs at boundaries
(`any-boundary` row in routing.json), not inside coupled implementation tasks.

Providers (BeQuite v1):
- anthropic   — primary; Claude family.
- openai      — planner alt; GPT-5 family.
- google      — Gemini family; free-tier doc gen.
- deepseek    — cheap implementer; OpenAI-compatible API.
- ollama      — offline / air-gapped (HTTP localhost).

Each adapter MUST:
1. Be importable WITHOUT its vendor SDK installed (graceful degradation —
   `is_available()` returns False instead of import-erroring).
2. Read API key from the env var declared in `bequite.config.toml::providers`.
3. Return a `Completion` dataclass with at minimum: text, input_tokens,
   output_tokens, finish_reason, raw_response (provider-specific dict).
4. Estimate USD cost (best-effort; v0.8.1 brings live pricing).

Test seam: any adapter can be replaced with a `TestProvider` that returns
canned responses for routing/cost-ceiling tests without touching the network.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Optional, Protocol, runtime_checkable


@dataclasses.dataclass
class Completion:
    """Vendor-neutral completion result. Producers of receipts read this."""

    text: str
    input_tokens: int
    output_tokens: int
    finish_reason: str  # "stop" | "length" | "tool_use" | "content_filter" | "error"
    model: str
    provider: str
    usd_cost: float = 0.0
    raw_response: Optional[dict[str, Any]] = None
    error: Optional[str] = None


@runtime_checkable
class AiProvider(Protocol):
    """Vendor-neutral AI provider Protocol.

    Adapters implement this protocol implicitly via duck-typing. The router
    only needs the four methods below; adapters are free to expose more.
    """

    name: str  # "anthropic" / "openai" / etc.

    def is_available(self) -> bool:
        """Return True if the SDK is importable AND the API key is present."""
        ...

    def supports_model(self, model: str) -> bool:
        """Return True if this provider can serve `model`."""
        ...

    def estimate_cost_usd(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Best-effort USD estimate. v0.8.1 wires live pricing fetch."""
        ...

    def complete(
        self,
        *,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        max_input_tokens: int = 100_000,
        max_output_tokens: int = 8_000,
        reasoning_effort: str = "default",
        timeout_s: float = 120.0,
    ) -> Completion:
        """Run a single completion. Raises on transport-level errors."""
        ...


# Provider names registered with the router.
REGISTERED_PROVIDERS = ("anthropic", "openai", "google", "deepseek", "ollama")


def get_provider(name: str) -> AiProvider:
    """Lazy-import + return a provider adapter by name.

    Raises ValueError on unknown provider; adapters that fail to import (their
    SDK is missing) still return — the caller checks `is_available()`.
    """
    if name == "anthropic":
        from bequite.providers.anthropic import AnthropicProvider
        return AnthropicProvider()
    if name == "openai":
        from bequite.providers.openai import OpenAIProvider
        return OpenAIProvider()
    if name == "google":
        from bequite.providers.google import GoogleProvider
        return GoogleProvider()
    if name == "deepseek":
        from bequite.providers.deepseek import DeepseekProvider
        return DeepseekProvider()
    if name == "ollama":
        from bequite.providers.ollama import OllamaProvider
        return OllamaProvider()
    raise ValueError(f"Unknown provider {name!r}; choose from {REGISTERED_PROVIDERS}")
