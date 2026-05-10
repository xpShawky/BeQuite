"""Ollama provider adapter — offline / air-gapped (v0.8.0).

Talks to a locally-running Ollama daemon at `http://localhost:11434/api/chat`
by default. No vendor SDK required (uses httpx, already in deps).

Cost is always 0.0 USD (local compute). Useful for:
- Air-gapped projects (Doctrine `gov-fedramp` with high-side data).
- Cost-zero parallel exploration.
- Offline-first development on planes / trains / etc.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from bequite.providers import Completion


class OllamaProvider:
    name = "ollama"

    def __init__(
        self,
        base_url_env: str = "OLLAMA_BASE_URL",
        default_base_url: str = "http://localhost:11434",
    ) -> None:
        self.base_url = os.environ.get(base_url_env, default_base_url)

    def is_available(self) -> bool:
        try:
            import httpx
        except ImportError:
            return False
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:  # noqa: BLE001
            return False

    def supports_model(self, model: str) -> bool:
        # Ollama supports any model the user has pulled locally; we don't
        # gate on a static list.
        return True

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        return 0.0  # local compute

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
        try:
            import httpx
        except ImportError:
            return Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=model, provider=self.name,
                error="httpx not installed",
            )

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        if reasoning_effort != "default":
            messages.append({"role": "system", "content": f"Reasoning effort: {reasoning_effort}."})
        messages.append({"role": "user", "content": prompt})

        try:
            with httpx.Client(timeout=timeout_s) as client:
                resp = client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "stream": False,
                        "options": {"num_predict": max_output_tokens},
                    },
                )
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
        except Exception as e:  # noqa: BLE001
            return Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=model, provider=self.name,
                error=f"{type(e).__name__}: {e}",
            )

        # Ollama returns: {message: {content: ...}, prompt_eval_count: N, eval_count: M, done_reason: "stop"}
        text = ((data.get("message") or {}).get("content")) or ""
        in_tok = int(data.get("prompt_eval_count") or 0)
        out_tok = int(data.get("eval_count") or 0)
        finish = data.get("done_reason") or "stop"

        return Completion(
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            finish_reason=finish,
            model=model,
            provider=self.name,
            usd_cost=0.0,
            raw_response={"done_reason": finish},
        )
