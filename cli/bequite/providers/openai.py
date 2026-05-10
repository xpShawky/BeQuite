"""OpenAI provider adapter — planner alt + DeepSeek base (v0.8.0).

Maps `gpt-5`, `gpt-5-mini`, `gpt-4.1`, `o3` family to the OpenAI SDK's
Responses / Chat Completions API. Same adapter is reused by DeepseekProvider
with `base_url` overridden — DeepSeek's API is OpenAI-compatible.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from bequite.providers import Completion


# May-2026 pricing per 1M tokens (input/output) — static fallback.
_OPENAI_PRICING = {
    "gpt-5":         {"input": 12.00, "output": 50.00},
    "gpt-5-mini":    {"input":  0.50, "output":  2.00},
    "gpt-4.1":       {"input":  3.00, "output": 12.00},
    "gpt-4.1-mini":  {"input":  0.40, "output":  1.60},
    "o3":            {"input": 10.00, "output": 40.00},
    "o3-mini":       {"input":  1.50, "output":  6.00},
}


class OpenAIProvider:
    name = "openai"

    def __init__(
        self,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key_env = api_key_env
        self.base_url = base_url

    def is_available(self) -> bool:
        if not os.environ.get(self.api_key_env):
            return False
        try:
            import openai  # noqa: F401
        except ImportError:
            return False
        return True

    def supports_model(self, model: str) -> bool:
        return model in _OPENAI_PRICING or model.startswith(("gpt-", "o3", "o4"))

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        # v0.8.1: consult live pricing cache first; fall back to hard-coded table.
        try:
            from bequite.pricing import pricing_for
            rates, _source = pricing_for(model)
            if rates:
                return (input_tokens / 1_000_000) * rates["input"] + (output_tokens / 1_000_000) * rates["output"]
        except ImportError:
            pass
        tier = _OPENAI_PRICING.get(model)
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
                error=f"openai SDK or {self.api_key_env} not present",
            )

        import openai

        kwargs: dict[str, Any] = {"api_key": os.environ[self.api_key_env]}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        client = openai.OpenAI(**kwargs)

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        if reasoning_effort != "default":
            # For o3-class models the SDK supports `reasoning_effort` directly;
            # for gpt-5 family it's an extension. Pass through as a header
            # hint when supported; otherwise prepend to system.
            messages.append({"role": "system", "content": f"Reasoning effort: {reasoning_effort}."})
        messages.append({"role": "user", "content": prompt})

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_output_tokens,
                timeout=timeout_s,
            )
        except Exception as e:  # noqa: BLE001
            return Completion(
                text="",
                input_tokens=0, output_tokens=0,
                finish_reason="error",
                model=model, provider=self.name,
                error=f"{type(e).__name__}: {e}",
            )

        choice = (resp.choices or [None])[0]
        text = ""
        finish = "stop"
        if choice is not None:
            text = (choice.message.content or "") if getattr(choice, "message", None) else ""
            finish = getattr(choice, "finish_reason", "stop") or "stop"

        usage = getattr(resp, "usage", None)
        in_tok = getattr(usage, "prompt_tokens", 0) if usage else 0
        out_tok = getattr(usage, "completion_tokens", 0) if usage else 0

        return Completion(
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            finish_reason=finish,
            model=model,
            provider=self.name,
            usd_cost=self.estimate_cost_usd(model, in_tok, out_tok),
            raw_response={"id": getattr(resp, "id", None), "finish_reason": finish},
        )
