"""Skill loader — assembles the dispatch payload for a /bequite.<command> call.

In v0.5.0 this is a stub that prints what would be loaded; v0.6.0 ships the
live Claude API call via the anthropic SDK. The contract this module commits
to is what v0.6.0 will satisfy.

The Skill is the source of truth (Constitution v1.0.1 Article I + Fork B
ratification). The CLI is one face of two — when invoked outside Claude Code
or Cursor or Codex, the CLI loads SKILL.md + the relevant agent persona +
prompt-pack into a Claude API call out-of-host.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PHASE_TO_COMMAND = {
    "discover": "P0",
    "research": "P0",
    "decide-stack": "P1",
    "plan": "P2",
    "phases": "P3",
    "tasks": "P4",
    "implement": "P5",
    "review": "P5",
    "validate": "P6",
    "evidence": "any",
    "release": "P7",
    "audit": "any",
    "freshness": "P1",
    "auto": "all",
    "memory": "any",
    "snapshot": "any",
    "cost": "any",
    "skill-install": "any",
    "design-audit": "P5/P6",
    "impeccable-craft": "P5",
    "recover": "any",
}


COMMAND_TO_PERSONA = {
    "discover": "product-owner",
    "research": "research-analyst",
    "decide-stack": "software-architect",
    "plan": "software-architect",
    "phases": "product-owner",
    "tasks": "product-owner",
    "implement": "backend-engineer",   # default; auto-mode selects per task scope
    "review": "software-architect",
    "validate": "qa-engineer",
    "evidence": "orchestrator",
    "release": "devops-engineer",
    "audit": "software-architect",
    "freshness": "research-analyst",
    "auto": "orchestrator",
    "memory": "orchestrator",
    "snapshot": "orchestrator",
    "cost": "token-economist",
    "skill-install": "devops-engineer",
    "design-audit": "frontend-designer",
    "impeccable-craft": "frontend-designer",
    "recover": "orchestrator",
}


def _find_skill_root(repo_root: Path) -> Path | None:
    """Find the skill folder relative to a project."""
    candidates = [
        repo_root / "skill",
        repo_root / ".claude" / "skills" / "bequite",
        repo_root / ".cursor" / "skills" / "bequite",
        Path(__file__).resolve().parent.parent.parent / "skill",
    ]
    for c in candidates:
        if (c / "SKILL.md").exists():
            return c
    return None


def _read_routing(skill_root: Path, persona: str) -> tuple[str | None, str | None]:
    """Read the routing.json entry for a persona."""
    routing_path = skill_root / "routing.json"
    if not routing_path.exists():
        return None, None
    try:
        data = json.loads(routing_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    for entry in data.get("phase_routing", []):
        if entry.get("persona") == persona:
            return entry.get("model"), entry.get("reasoning_effort")
    return None, None


def build_dispatch_payload(
    name: str,
    repo_root: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Build the payload that would be sent to the Claude API.

    Returns a dict with:
      - command: the slash-command name
      - phase: P0..P7 / any
      - persona: which agent persona to load
      - model: routing.json model
      - reasoning_effort: routing.json effort
      - input_files: list of paths the model is meant to read on entry
      - prompt_pack: the relevant prompts/<file>.md path
      - kwargs: passed-through user input
    """
    skill_root = _find_skill_root(repo_root)
    persona = COMMAND_TO_PERSONA.get(name, "orchestrator")

    model, effort = (None, None)
    if skill_root:
        model, effort = _read_routing(skill_root, persona)

    # Files the model is meant to read on entry (Article III + per-command spec).
    base_files = [
        ".bequite/memory/constitution.md",
        ".bequite/memory/projectbrief.md",
        ".bequite/memory/productContext.md",
        ".bequite/memory/systemPatterns.md",
        ".bequite/memory/techContext.md",
        ".bequite/memory/activeContext.md",
        ".bequite/memory/progress.md",
        "state/project.yaml",
        "state/current_phase.md",
        "state/recovery.md",
    ]

    # Per-command additions.
    extra: list[str] = []
    if name == "decide-stack":
        extra.extend([
            "docs/RESEARCH_SUMMARY.md",
            "docs/research/technical_options.md",
            "skill/references/stack-matrix.md",
            "skill/references/package-allowlist.md",
        ])
    elif name == "plan":
        extra.extend([
            ".bequite/memory/decisions/",
            "docs/PRODUCT_REQUIREMENTS.md",
            "docs/RESEARCH_SUMMARY.md",
        ])
    elif name == "implement":
        task = kwargs.get("task", "?")
        extra.append(f"specs/<feature>/phases/<phase>/tasks.md  # task: {task}")
    elif name == "validate":
        extra.extend([
            "tests/walkthroughs/admin-walk.md",
            "tests/walkthroughs/user-walk.md",
        ])

    prompt_pack_map = {
        "discover": "prompts/discovery_prompt.md",
        "research": "prompts/research_prompt.md",
        "decide-stack": "prompts/stack_decision_prompt.md",
        "plan": "prompts/stack_decision_prompt.md",
        "implement": "prompts/implementation_prompt.md",
        "review": "prompts/review_prompt.md",
        "recover": "prompts/recovery_prompt.md",
        "auto": "prompts/master_prompt.md",
    }
    prompt_pack = prompt_pack_map.get(name)

    return {
        "command": name,
        "phase": PHASE_TO_COMMAND.get(name, "any"),
        "persona": persona,
        "model": model or "claude-opus-4-7",
        "reasoning_effort": effort or "high",
        "input_files": base_files + extra,
        "prompt_pack": prompt_pack,
        "kwargs": kwargs,
    }
