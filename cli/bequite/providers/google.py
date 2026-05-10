"""Google (Gemini) provider adapter (v0.8.0).

Maps `gemini-2.5-pro` and `gemini-2.5-flash` to the `google-genai` SDK
(`bequite[google]` extra). Notably useful for free-tier doc generation
(token-economist + tech-writer personas).
"""

from __future__ import annotations

import os
from typing import Any, Optional

from bequite.providers import Completion


_GOOGLE_PRICING = {
    "gemini-2.5-pro":   {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.30, "output":  2.50},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
}


class GoogleProvider:
    name = "google"

    def __init__(self, api_key_env: str = "GOOGLE_API_KEY") -> None:
        self.api_key_env = api_key_env

    def is_available(self) -> bool:
        if not os.environ.get(self.api_key_env):
            return False
        try:
            import google.genai  # noqa: F401
        except ImportError:
            return False
        return True

    def supports_model(self, model: str) -> bool:
        return model in _GOOGLE_PRICING or model.startswith("gemini-")

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        # v0.8.1: consult live pricing cache first; fall back to hard-coded table.
        try:
            from bequite.pricing import pricing_for
            rates, _source = pricing_for(model)
            if rates:
                return (input_tokens / 1_000_000) * rates["input"] + (output_tokens / 1_000_000) * rates["output"]
        except ImportError:
            pass
        tier = _GOOGLE_PRICING.get(model)
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
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=model, provider=self.name,
                error=f"google-genai SDK or {self.api_key_env} not present",
            )

        from google import genai
        from google.genai import types

        client = genai.Client(api_key=os.environ[self.api_key_env])

        contents: list[Any] = []
        if system:
            contents.append({"role": "user", "parts": [{"text": f"System: {system}"}]})
        if reasoning_effort != "default":
            contents.append({"role": "user", "parts": [{"text": f"Reasoning effort: {reasoning_effort}."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        try:
            resp = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_output_tokens,
                ),
            )
        except Exception as e:  # noqa: BLE001
            return Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=model, provider=self.name,
                error=f"{type(e).__name__}: {e}",
            )

        # Extract text — Gemini packs it into resp.text in newer SDK.
        text = getattr(resp, "text", None) or ""
        usage = getattr(resp, "usage_metadata", None)
        in_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
        out_tok = getattr(usage, "candidates_token_count", 0) if usage else 0

        return Completion(
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            finish_reason="stop",
            model=model,
            provider=self.name,
            usd_cost=self.estimate_cost_usd(model, in_tok, out_tok),
            raw_response={"finish_reason": "stop"},
        )
