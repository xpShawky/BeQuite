"""DeepSeek provider adapter (v0.8.0).

DeepSeek's API is OpenAI-compatible — this adapter is the OpenAIProvider
configured with `base_url=https://api.deepseek.com/v1`. Useful for cheap
parallel implementation tasks (per AkitaOnRails 2026: split only when
genuinely parallel; otherwise solo frontier wins).
"""

from __future__ import annotations

from bequite.providers.openai import OpenAIProvider


# Pricing per 1M tokens — May 2026.
_DEEPSEEK_PRICING = {
    "deepseek-chat":   {"input": 0.27, "output": 1.10},
    "deepseek-coder":  {"input": 0.27, "output": 1.10},
    "deepseek-reasoner":{"input": 0.55, "output": 2.19},
}


class DeepseekProvider(OpenAIProvider):
    """OpenAI-compatible adapter pointed at DeepSeek's endpoint."""

    name = "deepseek"

    def __init__(
        self,
        api_key_env: str = "DEEPSEEK_API_KEY",
        base_url: str = "https://api.deepseek.com/v1",
    ) -> None:
        super().__init__(api_key_env=api_key_env, base_url=base_url)

    def supports_model(self, model: str) -> bool:
        return model in _DEEPSEEK_PRICING or model.startswith("deepseek-")

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        tier = _DEEPSEEK_PRICING.get(model)
        if not tier:
            return 0.0
        return (input_tokens / 1_000_000) * tier["input"] + (output_tokens / 1_000_000) * tier["output"]
