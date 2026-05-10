"""bequite — CLI entry point.

The thin Python wrapper that loads the SKILL.md + agents into a Claude API
call (out-of-host) for users who aren't running inside Claude Code / Cursor /
Codex / etc. The Skill is the source of truth; this CLI is one face of two
(the other being native invocation inside skill-aware hosts).

Subcommands map 1:1 to the slash commands in skill/commands/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

# Re-export stable imports for tests + integration.
from bequite import audit as audit_module
from bequite import freshness as freshness_module
from bequite import __version__


# ----------------------------------------------------------------------------
# Helper — load skill from the source of truth
# ----------------------------------------------------------------------------


def _resolve_skill_root(repo_root: Path) -> Path:
    """Find the BeQuite skill folder relative to a project."""
    candidates = [
        repo_root / "skill",
        repo_root / ".claude" / "skills" / "bequite",
        repo_root / ".cursor" / "skills" / "bequite",
        Path(__file__).resolve().parent.parent.parent / "skill",
    ]
    for c in candidates:
        if (c / "SKILL.md").exists():
            return c
    raise click.ClickException(
        "Could not locate skill/SKILL.md. Run from a BeQuite-managed project, "
        "or pass --skill-root <path>."
    )


# ----------------------------------------------------------------------------
# CLI — Click group
# ----------------------------------------------------------------------------


@click.group(
    name="bequite",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, prog_name="bequite")
def cli() -> None:
    """BeQuite — project harness for AI coding agents.

    19 commands map 1:1 to /bequite.<command> in skill-aware hosts. The
    Constitution + Memory Bank + state/ + receipts + evidence are the durable
    persistence; this CLI is one face of the same brain.

    Run `bequite doctor` first to verify the environment.
    """


# ----------------------------------------------------------------------------
# bequite version  (handled by --version above; explicit subcommand for scripts)
# ----------------------------------------------------------------------------


@cli.command()
def version() -> None:
    """Print the BeQuite CLI version."""
    click.echo(f"bequite {__version__}")


# ----------------------------------------------------------------------------
# bequite doctor  — environment check (master §17.2 — adapted)
# ----------------------------------------------------------------------------


@cli.command()
@click.option("--repo", default=".", help="Repo root to inspect.")
def doctor(repo: str) -> None:
    """Run environment + state-coherence checks."""
    from bequite.commands import run_doctor

    code = run_doctor(Path(repo).resolve())
    sys.exit(code)


# ----------------------------------------------------------------------------
# bequite init  — scaffold a new project
# ----------------------------------------------------------------------------


@cli.command()
@click.argument("name")
@click.option(
    "--doctrine",
    multiple=True,
    help="Active Doctrines (repeatable). Defaults to default-web-saas.",
)
@click.option(
    "--mode",
    type=click.Choice(["fast", "safe", "enterprise"], case_sensitive=False),
    default="safe",
    show_default=True,
)
@click.option(
    "--scale",
    "--scale-tier",
    "scale_tier",
    type=click.Choice(["solo", "small_saas", "mid_market", "country", "hyperscale", "library_tool"], case_sensitive=False),
    default="small_saas",
    show_default=True,
)
@click.option(
    "--audience",
    type=click.Choice(["engineer", "vibe-handoff"], case_sensitive=False),
    default="engineer",
    show_default=True,
)
def init(name: str, doctrine: tuple[str, ...], mode: str, scale_tier: str, audience: str) -> None:
    """Scaffold a fresh BeQuite-managed project at ./<name>/."""
    from bequite.commands import run_init

    code = run_init(
        project_name=name,
        doctrines=list(doctrine) or ["default-web-saas"],
        mode=mode.lower(),
        scale_tier=scale_tier.lower(),
        audience=audience.lower(),
    )
    sys.exit(code)


# ----------------------------------------------------------------------------
# bequite recover  — generate paste-able recovery prompt
# ----------------------------------------------------------------------------


@cli.command()
@click.option("--repo", default=".", help="Repo root.")
def recover(repo: str) -> None:
    """Generate a paste-able recovery prompt for a new session."""
    from bequite.commands import run_recover

    code = run_recover(Path(repo).resolve())
    sys.exit(code)


# ----------------------------------------------------------------------------
# bequite audit  — Constitution + Doctrine drift detector
# ----------------------------------------------------------------------------


@cli.command(name="audit")
@click.option("--repo", default=".")
@click.option("--rule", default=None, help="Run only rules matching this substring.")
@click.option("--doctrine", default=None, help="Scope to one Doctrine.")
@click.option("--ci", is_flag=True, help="CI mode (markdown output, exit 1 on block).")
@click.option("--json", "json_output", is_flag=True, help="JSON output.")
def audit_cmd(repo: str, rule: str | None, doctrine: str | None, ci: bool, json_output: bool) -> None:
    """Constitution + Doctrine drift detector."""
    args = [
        "--repo", repo,
    ]
    if rule:
        args += ["--rule", rule]
    if doctrine:
        args += ["--doctrine", doctrine]
    if ci:
        args.append("--ci")
    if json_output:
        args.append("--json")
    sys.exit(audit_module.main(args))


# ----------------------------------------------------------------------------
# bequite freshness  — knowledge probe
# ----------------------------------------------------------------------------


@cli.command(name="freshness")
@click.option("--repo", default=".")
@click.option("--package", default=None)
@click.option("--ecosystem", type=click.Choice(["npm", "pypi", "cargo"]))
@click.option("--all", "scan_all", is_flag=True, help="Probe every dep in manifests.")
@click.option("--max-age-months", type=int, default=6)
@click.option("--no-cache", is_flag=True)
@click.option("--json", "json_output", is_flag=True)
def freshness_cmd(
    repo: str,
    package: str | None,
    ecosystem: str | None,
    scan_all: bool,
    max_age_months: int,
    no_cache: bool,
    json_output: bool,
) -> None:
    """Knowledge probe — verify stack candidates aren't stale."""
    args = ["--repo", repo, "--max-age-months", str(max_age_months)]
    if package:
        args += ["--package", package]
    if ecosystem:
        args += ["--ecosystem", ecosystem]
    if scan_all:
        args.append("--all")
    if no_cache:
        args.append("--no-cache")
    if json_output:
        args.append("--json")
    sys.exit(freshness_module.main(args))


# ----------------------------------------------------------------------------
# bequite memory  — Memory Bank operations
# ----------------------------------------------------------------------------


@cli.group(name="memory")
def memory_group() -> None:
    """Memory Bank operations: show / validate / refresh / snapshot / diff."""


@memory_group.command("show")
@click.argument("target", required=False)
@click.option("--repo", default=".")
def memory_show(target: str | None, repo: str) -> None:
    """Print Memory Bank or specific file. `target` = projectbrief | productContext | systemPatterns | techContext | activeContext | progress | constitution | recovery | <doctrine>."""
    from bequite.commands import run_memory_show

    sys.exit(run_memory_show(Path(repo).resolve(), target))


@memory_group.command("validate")
@click.option("--repo", default=".")
def memory_validate(repo: str) -> None:
    """Schema-validate every Memory Bank + state file."""
    from bequite.commands import run_memory_validate

    sys.exit(run_memory_validate(Path(repo).resolve()))


# ----------------------------------------------------------------------------
# bequite skill install
# ----------------------------------------------------------------------------


@cli.group(name="skill")
def skill_group() -> None:
    """Skill operations: install / list."""


@skill_group.command("install")
@click.argument("host", type=click.Choice(["claude-code", "cursor", "codex", "gemini", "windsurf", "cline", "kilo", "continue", "aider"]))
@click.option("--repo", default=".")
def skill_install(host: str, repo: str) -> None:
    """Install BeQuite into the named host (per-host file layout)."""
    from bequite.commands import run_skill_install

    sys.exit(run_skill_install(host, Path(repo).resolve()))


# ----------------------------------------------------------------------------
# Skill-dispatching commands (thin wrappers — delegate to Claude API in v0.6.0+)
# ----------------------------------------------------------------------------


@cli.command()
@click.option("--repo", default=".")
def discover(repo: str) -> None:
    """P0 — product discovery interview (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("discover", Path(repo).resolve()))


@cli.command()
@click.argument("topic", required=False, default="")
@click.option("--repo", default=".")
def research(topic: str, repo: str) -> None:
    """P0 — research scan (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("research", Path(repo).resolve(), topic=topic))


@cli.command(name="decide-stack")
@click.option("--repo", default=".")
def decide_stack(repo: str) -> None:
    """P1 — stack ADR (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("decide-stack", Path(repo).resolve()))


@cli.command()
@click.option("--repo", default=".")
def plan(repo: str) -> None:
    """P2 — spec + plan + data-model + contracts (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("plan", Path(repo).resolve()))


@cli.command()
@click.option("--task", required=True, help="Task ID from state/task_index.json.")
@click.option("--repo", default=".")
def implement(task: str, repo: str) -> None:
    """P5 — implement one task (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("implement", Path(repo).resolve(), task=task))


@cli.command()
@click.option("--repo", default=".")
def review(repo: str) -> None:
    """P5 — code review (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("review", Path(repo).resolve()))


@cli.command()
@click.option("--repo", default=".")
def validate(repo: str) -> None:
    """P6 — validation mesh (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("validate", Path(repo).resolve()))


@cli.command()
@click.option("--repo", default=".")
def evidence(repo: str) -> None:
    """Surface evidence + receipts."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("evidence", Path(repo).resolve()))


@cli.command()
@click.option("--repo", default=".")
def release(repo: str) -> None:
    """P7 — handoff + release prep (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("release", Path(repo).resolve()))


@cli.command()
@click.option("--feature", required=True, help="Feature slug.")
@click.option("--max-cost-usd", type=int, default=20, show_default=True)
@click.option("--max-wall-clock-hours", type=int, default=6, show_default=True)
@click.option("--phases", default=None, help="Comma-separated subset (e.g. P5,P6).")
@click.option("--repo", default=".")
def auto(
    feature: str,
    max_cost_usd: int,
    max_wall_clock_hours: int,
    phases: str | None,
    repo: str,
) -> None:
    """One-click run-to-completion P0 → P7 with safety rails (skill dispatch)."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command(
        "auto",
        Path(repo).resolve(),
        feature=feature,
        max_cost_usd=max_cost_usd,
        max_wall_clock_hours=max_wall_clock_hours,
        phases=phases,
    ))


@cli.command()
@click.option("--repo", default=".")
def cost(repo: str) -> None:
    """Token + dollar receipts roll-up."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("cost", Path(repo).resolve()))


# ----------------------------------------------------------------------------
# bequite design <subcommand> — Impeccable command dispatch
# ----------------------------------------------------------------------------


@cli.group(name="design")
def design_group() -> None:
    """Design commands (Impeccable-loaded; frontend Doctrines only)."""


@design_group.command("audit")
@click.option("--repo", default=".")
def design_audit(repo: str) -> None:
    """Detect AI-looking UI."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command("design-audit", Path(repo).resolve()))


@design_group.command("craft")
@click.argument("impeccable_command", required=True)
@click.option("--repo", default=".")
def design_craft(impeccable_command: str, repo: str) -> None:
    """Apply a specific Impeccable command. See skill/skills-bundled/impeccable/ for the 23 commands."""
    from bequite.commands import run_skill_command

    sys.exit(run_skill_command(
        "impeccable-craft",
        Path(repo).resolve(),
        impeccable_command=impeccable_command,
    ))


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
