"""ManualPasteProvider — v0.10.5.

Conforms to AiProvider Protocol. complete() writes the prompt to a file and
either polls for the response (sync) or returns awaiting-user (async).
"""

from __future__ import annotations

import pathlib
import time
from typing import Optional

from bequite.providers import Completion


def slug(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def estimate_tokens(text: str) -> int:
    """Coarse ~4-chars-per-token estimate."""
    return max(1, len(text) // 4)


class ManualPasteProvider:
    name = "manual-paste"

    def __init__(self, run_dir: Optional[pathlib.Path] = None, async_mode: bool = False, poll_interval_s: float = 2.0, timeout_s: float = 3600.0) -> None:
        self.run_dir = run_dir
        self.async_mode = async_mode
        self.poll_interval_s = poll_interval_s
        self.timeout_s = timeout_s

    def is_available(self) -> bool:
        return True  # always

    def supports_model(self, model: str) -> bool:
        return True  # any user-named model

    def estimate_cost_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        return 0.0  # human cost via subscription, not API spend

    def complete(
        self,
        *,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        max_input_tokens: int = 100_000,
        max_output_tokens: int = 8_000,
        reasoning_effort: str = "default",
        timeout_s: float = 3600.0,
    ) -> Completion:
        if self.run_dir is None:
            return Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=model, provider=self.name,
                error="ManualPasteProvider requires run_dir to be set",
            )
        prompts_dir = self.run_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = prompts_dir / f"plan_{slug(model)}.md"
        response_file = self.run_dir / f"{slug(model)}_plan.md"
        prompt_file.write_text(prompt, encoding="utf-8")

        if self.async_mode:
            return Completion(
                text="", input_tokens=estimate_tokens(prompt), output_tokens=0,
                finish_reason="awaiting_user", model=model, provider=self.name,
            )

        # Synchronous: poll for the file.
        elapsed = 0.0
        while not response_file.exists():
            if elapsed >= self.timeout_s:
                return Completion(
                    text="", input_tokens=estimate_tokens(prompt), output_tokens=0,
                    finish_reason="error", model=model, provider=self.name,
                    error=f"timeout after {self.timeout_s}s waiting for {response_file.name}",
                )
            time.sleep(self.poll_interval_s)
            elapsed += self.poll_interval_s
        text = response_file.read_text(encoding="utf-8")
        return Completion(
            text=text,
            input_tokens=estimate_tokens(prompt),
            output_tokens=estimate_tokens(text),
            finish_reason="user_provided",
            model=model,
            provider=self.name,
            usd_cost=0.0,
        )
