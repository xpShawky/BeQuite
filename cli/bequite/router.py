"""bequite.router — read routing.json + select provider+model+effort (v0.8.0).

The single entry-point the rest of BeQuite uses to actually call a model:

    from bequite.router import dispatch
    completion, route = dispatch(phase="P5", persona="backend-engineer", prompt=...)

Behaviour:
1. Reads `skill/routing.json` (or `.bequite/routing-overrides.json` if present).
2. Picks the row matching `(phase, persona)` — falls back to `phase="any"` or
   `persona="orchestrator"` if no exact match.
3. Determines provider from the model name (claude-* → anthropic, gpt-* / o3 →
   openai, gemini-* → google, deepseek-* → deepseek; others assumed ollama).
4. Checks `is_available()`; if not, tries `fallback_model` from the same row.
5. Calls `complete()` and returns the `Completion` plus a `Route` summary.
6. Updates `.bequite/cache/cost-ledger.json` so `stop-cost-budget.sh` can
   enforce the session ceiling.

For tests, `dispatch()` accepts a `provider_factory` injection — a callable
mapping provider-name → AiProvider. Default is `bequite.providers.get_provider`.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
from typing import Any, Callable, Optional

from bequite.providers import AiProvider, Completion, get_provider


# --------------------------------------------------------------------- routing


@dataclasses.dataclass
class Route:
    phase: str
    persona: str
    model: str
    reasoning_effort: str
    fallback_model: Optional[str]
    max_input_tokens: int
    max_output_tokens: int
    provider: str
    used_fallback: bool = False
    note: Optional[str] = None


def _provider_for_model(model: str) -> str:
    if model.startswith("claude-"):
        return "anthropic"
    if model.startswith(("gpt-", "o3", "o4")):
        return "openai"
    if model.startswith("gemini-"):
        return "google"
    if model.startswith("deepseek-"):
        return "deepseek"
    if model.startswith(("llama", "mistral", "qwen", "phi", "gemma")):
        return "ollama"
    # Unknown — assume ollama (local model, user has pulled it).
    return "ollama"


def find_routing_path(repo_root: pathlib.Path) -> Optional[pathlib.Path]:
    candidates = [
        repo_root / ".bequite" / "routing-overrides.json",
        repo_root / "skill" / "routing.json",
        repo_root / ".claude" / "skills" / "bequite" / "routing.json",
    ]
    # Walk up if not found at repo_root.
    here = pathlib.Path(__file__).resolve()
    for parent in here.parents:
        candidates.append(parent / "skill" / "routing.json")
    for c in candidates:
        if c.exists():
            return c
    return None


def select_route(
    *,
    phase: str,
    persona: str,
    routing_path: Optional[pathlib.Path] = None,
    repo_root: Optional[pathlib.Path] = None,
) -> Route:
    """Pick the best routing row for (phase, persona).

    Match priority:
    1. exact phase + exact persona
    2. exact persona + phase=="any" or "any-boundary" or "always-on"
    3. exact phase + persona=="orchestrator"
    4. catch-all defaults.
    """
    if routing_path is None:
        routing_path = find_routing_path(repo_root or pathlib.Path.cwd())

    if routing_path is None or not routing_path.exists():
        # No routing.json — return safe default (Anthropic Opus, high effort).
        return Route(
            phase=phase, persona=persona,
            model="claude-opus-4-7", reasoning_effort="high",
            fallback_model="gpt-5",
            max_input_tokens=100_000, max_output_tokens=12_000,
            provider="anthropic",
            note="no routing.json found; using safe defaults",
        )

    data = json.loads(routing_path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = data.get("phase_routing", [])

    def make_route(row: dict[str, Any]) -> Route:
        model = row.get("model") or "claude-opus-4-7"
        return Route(
            phase=row.get("phase", phase),
            persona=row.get("persona", persona),
            model=model,
            reasoning_effort=row.get("reasoning_effort", "high"),
            fallback_model=row.get("fallback_model"),
            max_input_tokens=int(row.get("max_input_tokens", 100_000)),
            max_output_tokens=int(row.get("max_output_tokens", 12_000)),
            provider=_provider_for_model(model),
            note=row.get("note"),
        )

    # 1. Exact phase + persona.
    for row in rows:
        if row.get("phase") == phase and row.get("persona") == persona:
            return make_route(row)
    # 2. persona + special phase (any / any-boundary / always-on / any-mode).
    for row in rows:
        if row.get("persona") == persona and row.get("phase") in ("any", "any-boundary", "always-on", "any-mode"):
            return make_route(row)
    # 3. Phase + orchestrator.
    for row in rows:
        if row.get("phase") == phase and row.get("persona") == "orchestrator":
            return make_route(row)
    # 4. Catch-all: orchestrator row.
    for row in rows:
        if row.get("phase") == "orchestrator" and row.get("persona") == "orchestrator":
            return make_route(row)

    # Final fallback.
    return Route(
        phase=phase, persona=persona,
        model="claude-opus-4-7", reasoning_effort="high",
        fallback_model="gpt-5",
        max_input_tokens=100_000, max_output_tokens=12_000,
        provider="anthropic",
        note=f"no row for ({phase}, {persona}); using catch-all defaults",
    )


# --------------------------------------------------------------------- dispatch


ProviderFactory = Callable[[str], AiProvider]


def dispatch(
    *,
    phase: str,
    persona: str,
    prompt: str,
    system: Optional[str] = None,
    routing_path: Optional[pathlib.Path] = None,
    repo_root: Optional[pathlib.Path] = None,
    provider_factory: ProviderFactory = get_provider,
    update_ledger: bool = True,
) -> tuple[Completion, Route]:
    """Run a single completion using the route picked from routing.json.

    On primary provider unavailability, tries `fallback_model`. Updates
    `.bequite/cache/cost-ledger.json` (unless `update_ledger=False`, which
    tests use to keep state isolated).
    """
    route = select_route(
        phase=phase, persona=persona,
        routing_path=routing_path, repo_root=repo_root,
    )

    primary = provider_factory(route.provider)
    if primary.is_available() and primary.supports_model(route.model):
        completion = primary.complete(
            model=route.model, prompt=prompt, system=system,
            max_input_tokens=route.max_input_tokens,
            max_output_tokens=route.max_output_tokens,
            reasoning_effort=route.reasoning_effort,
        )
    else:
        # Try fallback.
        if route.fallback_model:
            fb_provider_name = _provider_for_model(route.fallback_model)
            fb = provider_factory(fb_provider_name)
            if fb.is_available() and fb.supports_model(route.fallback_model):
                route = dataclasses.replace(
                    route,
                    model=route.fallback_model,
                    provider=fb_provider_name,
                    used_fallback=True,
                )
                completion = fb.complete(
                    model=route.model, prompt=prompt, system=system,
                    max_input_tokens=route.max_input_tokens,
                    max_output_tokens=route.max_output_tokens,
                    reasoning_effort=route.reasoning_effort,
                )
            else:
                completion = Completion(
                    text="", input_tokens=0, output_tokens=0,
                    finish_reason="error", model=route.model, provider=route.provider,
                    error=f"primary {route.provider} and fallback {fb_provider_name} both unavailable",
                )
        else:
            completion = Completion(
                text="", input_tokens=0, output_tokens=0,
                finish_reason="error", model=route.model, provider=route.provider,
                error=f"primary {route.provider} unavailable; no fallback configured",
            )

    if update_ledger:
        from bequite.cost_ledger import update as ledger_update
        try:
            ledger_update(
                repo_root=repo_root or pathlib.Path.cwd(),
                completion=completion,
                phase=phase,
                persona=persona,
            )
        except Exception:  # noqa: BLE001
            # Don't let ledger failures crash the dispatch.
            pass

    return completion, route
