"""Pydantic models for bequite.config.toml + state/project.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

# tomllib in Python 3.11+ stdlib
try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]


Mode = Literal["fast", "safe", "enterprise"]
Audience = Literal["engineer", "vibe-handoff"]
ScaleTier = Literal["solo", "small_saas", "mid_market", "country", "hyperscale", "library_tool"]


class SafetyRails(BaseModel):
    cost_ceiling_usd: int = 20
    wall_clock_ceiling_hours: int = 6
    consecutive_failure_threshold: int = 3
    heartbeat_minutes: int = 5
    banned_completion_phrases: list[str] = Field(default_factory=lambda: [
        "should", "probably", "seems to", "appears to",
        "I think it works", "might work", "hopefully", "in theory",
    ])
    pause_on: list[str] = Field(default_factory=lambda: [
        "cost_ceiling_reached",
        "wall_clock_ceiling_reached",
        "three_consecutive_failures",
        "banned_phrase_detected",
        "hook_block",
        "stack_adr_sign_off",
        "first_handoff_generation",
        "tier_3_command",
        "publish_to_pypi",
        "publish_to_npm",
        "git_push_to_main",
        "git_push_force",
        "terraform_apply",
        "shared_db_migration",
    ])


class FreshnessConfig(BaseModel):
    cache_ttl_hours: int = 24
    check_pricing_pages: bool = True
    check_osv: bool = True
    check_github_last_commit: bool = True
    github_last_commit_max_age_months: int = 6
    fail_stack_adr_on_stale: bool = True


class ReceiptsConfig(BaseModel):
    emit_per_phase: bool = True
    sign_with_ed25519: bool = True
    chain_parent_hash: bool = True
    storage_dir: str = ".bequite/receipts"


class EvidenceConfig(BaseModel):
    storage_dir: str = "evidence"
    require_screenshot_for_ui: bool = True
    require_test_output_for_implement: bool = True
    require_lint_output_for_implement: bool = True
    require_typecheck_output_for_implement: bool = True


class MemoryConfig(BaseModel):
    memory_bank_dir: str = ".bequite/memory"
    state_dir: str = "state"
    prompts_dir: str = "prompts"


class ProvidersConfig(BaseModel):
    anthropic: dict = Field(default_factory=lambda: {"api_key_env": "ANTHROPIC_API_KEY"})
    openai: dict = Field(default_factory=lambda: {"api_key_env": "OPENAI_API_KEY"})
    google: dict = Field(default_factory=lambda: {"api_key_env": "GOOGLE_API_KEY"})
    deepseek: dict = Field(default_factory=lambda: {"api_key_env": "DEEPSEEK_API_KEY"})


class TelemetryConfig(BaseModel):
    enabled: bool = False
    mode: Literal["off", "receipts_only", "full"] = "off"
    endpoint: str = ""


class AiAutomationConfig(BaseModel):
    cost_alarm_daily_ops_per_scenario: int = 10000
    cost_alarm_daily_executions_per_workflow: int = 5000
    cost_alarm_daily_tasks_per_zap: int = 500
    cost_alarm_daily_runs_per_function: int = 5000
    cost_alarm_daily_actions_per_workflow: int = 1000
    error_routing: dict = Field(default_factory=lambda: {
        "slack_channel": "#automation-alerts",
        "sentry_project": "automation",
        "pagerduty_service_id": "",
    })
    agent_max_iterations_default: int = 10
    agent_max_cost_usd_per_run_default: float = 1.00
    agent_circuit_breaker_consecutive_failures: int = 3


class ProjectConfig(BaseModel):
    name: str
    slug: str = ""
    owner: str = "xpShawky"
    maintainer: str = "noreply@bequite.dev"
    license: str = "MIT"
    constitution_version: str = "1.0.1"
    mode: Mode = "safe"
    audience: Audience = "engineer"
    doctrines: list[str] = Field(default_factory=list)
    scale_tier: ScaleTier = "small_saas"
    compliance: list[str] = Field(default_factory=list)
    locales: list[str] = Field(default_factory=lambda: ["en-US"])


class BequiteConfig(BaseModel):
    """Full bequite.config.toml shape."""

    project: ProjectConfig
    safety_rails: SafetyRails = Field(default_factory=SafetyRails)
    freshness: FreshnessConfig = Field(default_factory=FreshnessConfig)
    receipts: ReceiptsConfig = Field(default_factory=ReceiptsConfig)
    evidence: EvidenceConfig = Field(default_factory=EvidenceConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
    telemetry: TelemetryConfig = Field(default_factory=TelemetryConfig)
    ai_automation: AiAutomationConfig | None = None


def load_config(repo_root: Path) -> BequiteConfig | None:
    """Load bequite.config.toml from .bequite/ at repo root. Returns None if missing."""
    path = repo_root / ".bequite" / "bequite.config.toml"
    if not path.exists():
        return None
    with path.open("rb") as f:
        data = tomllib.load(f)
    project_raw = data.get("project", {})
    if "name" not in project_raw:
        project_raw["name"] = repo_root.name
    if "slug" not in project_raw or not project_raw["slug"]:
        project_raw["slug"] = repo_root.name.lower().replace(" ", "-")
    return BequiteConfig.model_validate({"project": project_raw, **{k: v for k, v in data.items() if k != "project"}})
