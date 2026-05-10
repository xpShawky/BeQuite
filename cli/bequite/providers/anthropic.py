"""Anthropic provider adapter — primary BeQuite provider (v0.8.0).

Maps `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5` to the
`anthropic` SDK's Messages API. Reasoning effort is passed via the SDK's
extended-thinking parameter; for SDK versions that don't expose it, the
adapter falls back to a system-prompt prefix ("You are operating in <effort>
reasoning mode.").
"""

from __future__ import annotations

import os
from typing import Any, Optional

from bequite.providers import Completion


# Pricing tier as of May 2026 — best-effort static fallback (v0.8.1 fetches live).
# USD per 1M tokens (input / output).
_ANTHROPIC_PRICING = {
    "claude-opus-4-7":  {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":{"input":  3.00, "output": 15.00},
    "claude-haiku-4-5": {"input":  0.80, "output":  4.00},
}


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key_env: str = "ANTHROPIC_API_KEY") -> None:
        self.api_key_env = api_key_env

    def is_available(self) -> bool:
        if not os.environ.get(self.api_key_env):
            return False
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return False
        return True

    def supports_model(self, model: str) -> bool:
        return model in _ANTHROPIC_PRICING or model.startswith("claude-")

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        # v0.8.1: consult live pricing cache first; fall back to hard-coded table.
        try:
            from bequite.pricing import pricing_for
            rates, _source = pricing_for(model)
            if rates:
                return (input_tokens / 1_000_000) * rates["input"] + (output_tokens / 1_000_000) * rates["output"]
        except ImportError:
            pass
        tier = _ANTHROPIC_PRICING.get(model)
        if not tier:
            return 0.0
        return (input_tokens / 1_000_000) * tier["input"] + (output_tokens / 1_000_000) * tier["output"]

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
        if not self.is_available():
            return Completion(
                text="",
                input_tokens=0, output_tokens=0,
                finish_reason="error",
                model=model, provider=self.name,
                error=f"anthropic SDK or {self.api_key_env} not present",
            )

        import anthropic

        client = anthropic.Anthropic(api_key=os.environ[self.api_key_env])

        system_blocks: list[Any] = []
        if system:
            system_blocks.append({"type": "text", "text": system})
        if reasoning_effort != "default":
            system_blocks.append({"type": "text", "text": f"Reasoning effort: {reasoning_effort}."})

        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_output_tokens,
                system=system_blocks if system_blocks else None,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout_s,
            )
        except Exception as e:  # noqa: BLE001 — adapter boundary
            return Completion(
                text="",
                input_tokens=0, output_tokens=0,
                finish_reason="error",
                model=model, provider=self.name,
                error=f"{type(e).__name__}: {e}",
            )

        # Extract text from content blocks (newer SDK shape).
        text_parts = []
        for block in getattr(resp, "content", []) or []:
            if getattr(block, "type", None) == "text":
                text_parts.append(getattr(block, "text", ""))
        text = "".join(text_parts)

        usage = getattr(resp, "usage", None)
        in_tok = getattr(usage, "input_tokens", 0) if usage else 0
        out_tok = getattr(usage, "output_tokens", 0) if usage else 0

        return Completion(
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            finish_reason=getattr(resp, "stop_reason", "stop") or "stop",
            model=model,
            provider=self.name,
            usd_cost=self.estimate_cost_usd(model, in_tok, out_tok),
            raw_response={"id": getattr(resp, "id", None), "stop_reason": getattr(resp, "stop_reason", None)},
        )
