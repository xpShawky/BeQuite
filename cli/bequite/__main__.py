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

# Force UTF-8 on stdout/stderr so help text + receipts + log lines containing
# Unicode (→, ✓, ・, RTL Arabic) render correctly on Windows consoles that
# default to cp1252. Python 3.7+ exposes reconfigure(); the try/except keeps
# us safe on stdout-redirected-to-pipe contexts where reconfigure may fail.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:
            pass

import click

# Re-export stable imports for tests + integration.
from bequite import audit as audit_module
from bequite import freshness as freshness_module
from bequite import pricing as pricing_module
from bequite import receipts as receipts_module
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
# bequite quickstart  — friendly onboarding for first-time users
# ----------------------------------------------------------------------------


@cli.command()
def quickstart() -> None:
    """Show a first-time onboarding guide for new users."""
    click.secho("", nl=True)
    click.secho("  BeQuite quickstart", fg="yellow", bold=True)
    click.secho("  Build it right the first time. No chatter. No debug spirals.", fg="bright_black")
    click.secho("", nl=True)
    click.secho(f"  Installed: bequite v{__version__}", fg="green")
    click.secho("", nl=True)

    click.secho("  What BeQuite does", fg="cyan", bold=True)
    click.echo("    Runs the 7-phase workflow (Research -> Stack -> Plan -> Phases ->")
    click.echo("    Tasks -> Implement -> Verify -> Handoff) with deterministic gates")
    click.echo("    so AI agents ship real software instead of broken half-builds.")
    click.secho("", nl=True)

    click.secho("  Try these commands (in order)", fg="cyan", bold=True)
    click.echo("")
    click.secho("    1. Diagnose your environment", fg="bright_yellow")
    click.echo("       bequite doctor")
    click.echo("")
    click.secho("    2. Scaffold a new project", fg="bright_yellow")
    click.echo("       bequite init my-app --doctrine default-web-saas")
    click.echo("       cd my-app")
    click.echo("")
    click.secho("    3. Run the full 7-phase workflow with safety rails", fg="bright_yellow")
    click.echo('       bequite auto --feature "add health endpoint" --max-cost-usd 10')
    click.echo("")
    click.secho("    4. Or run each phase manually", fg="bright_yellow")
    click.echo('       bequite research "what library should I use for X?"')
    click.echo("       bequite stack")
    click.echo("       bequite plan")
    click.echo("       bequite verify")
    click.echo("")

    click.secho("  Useful background", fg="cyan", bold=True)
    click.echo("    bequite --help                  list all 19+ commands")
    click.echo("    bequite memory show             read the Memory Bank")
    click.echo("    bequite receipts list           list signed reproducibility receipts")
    click.echo("    bequite route providers         model routing status (Anthropic/OpenAI/etc.)")
    click.echo("    bequite freshness --all         knowledge probe (catches deprecated packages)")
    click.echo("")

    click.secho("  Studio (optional visual surface)", fg="cyan", bold=True)
    click.echo("    The dashboard + marketing site + API live in studio/. Run three terminals:")
    click.echo("      cd studio/api       && bun run src/index.ts       # :3002")
    click.echo("      cd studio/dashboard && npm run dev                # :3001")
    click.echo("      cd studio/marketing && npm run dev                # :3000")
    click.echo("")

    click.secho("  Docs", fg="cyan", bold=True)
    click.echo("    Install guide:     docs/INSTALL.md")
    click.echo("    Release notes:     docs/RELEASES/v1.0.0.md")
    click.echo("    Constitution:      .bequite/memory/constitution.md")
    click.echo("    GitHub:            https://github.com/xpShawky/BeQuite")
    click.echo("")


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
@click.option("--by", default="session", type=click.Choice(["session", "phase", "day"]))
@click.option("--since", default=None, help="Filter receipts emitted on or after this date (YYYY-MM-DD).")
def cost(repo: str, by: str, since: str | None) -> None:
    """Token + dollar receipts roll-up.

    Local-first: walks .bequite/receipts/ and rolls up. Falls through to the
    skill-command dispatch only when no receipts exist (offline-friendly per
    Article III). For roll-ups across multiple projects, use the receipts CLI
    directly.
    """
    import json

    repo_path = Path(repo).resolve()
    receipts_dir = repo_path / ".bequite" / "receipts"

    if not receipts_dir.exists():
        click.echo(f"(no receipts at {receipts_dir} — receipts begin in v0.7.0+)")
        click.echo("Falling through to skill-dispatch ...")
        from bequite.commands import run_skill_command
        sys.exit(run_skill_command("cost", repo_path))

    store = receipts_module.ReceiptStore(str(receipts_dir))
    receipts = store.list_all()
    if since:
        receipts = [r for r in receipts if r.timestamp_utc >= since]

    if not receipts:
        click.echo(f"(no receipts after {since})" if since else f"(no receipts in {receipts_dir})")
        sys.exit(0)

    if by == "session":
        rollup = receipts_module.roll_up_by_session(receipts)
    elif by == "phase":
        rollup = receipts_module.roll_up_by_phase(receipts)
    else:
        rollup = receipts_module.roll_up_by_day(receipts)

    click.echo(json.dumps(rollup, indent=2, sort_keys=True, default=str))


# ----------------------------------------------------------------------------
# bequite receipts <subcommand> — direct receipts ops
# ----------------------------------------------------------------------------


@cli.group(name="receipts")
def receipts_group() -> None:
    """Reproducibility receipts (v0.7.0+)."""


@receipts_group.command("list")
@click.option("--repo", default=".")
def receipts_list(repo: str) -> None:
    """List all receipts in chain order."""
    sys.exit(receipts_module.main(["--storage-dir", str(Path(repo).resolve() / ".bequite" / "receipts"), "list"]))


@receipts_group.command("show")
@click.argument("sha")
@click.option("--repo", default=".")
def receipts_show(sha: str, repo: str) -> None:
    """Show a single receipt's JSON."""
    sys.exit(receipts_module.main(["--storage-dir", str(Path(repo).resolve() / ".bequite" / "receipts"), "show", sha]))


@receipts_group.command("validate-chain")
@click.option("--repo", default=".")
def receipts_validate_chain(repo: str) -> None:
    """Walk parent_receipt links; report any missing or out-of-order."""
    sys.exit(receipts_module.main(["--storage-dir", str(Path(repo).resolve() / ".bequite" / "receipts"), "validate-chain"]))


@receipts_group.command("roll-up")
@click.option("--repo", default=".")
@click.option("--by", default="session", type=click.Choice(["session", "phase", "day"]))
def receipts_rollup(repo: str, by: str) -> None:
    """Cost / token roll-up by session, phase, or day."""
    sys.exit(receipts_module.main(["--storage-dir", str(Path(repo).resolve() / ".bequite" / "receipts"), "roll-up", "--by", by]))


# ----------------------------------------------------------------------------
# bequite verify-receipts (v0.7.1) — ed25519 chain validation
# ----------------------------------------------------------------------------


@cli.command(name="verify-receipts")
@click.option("--repo", default=".")
@click.option("--strict", is_flag=True, default=False, help="Reject unsigned receipts (recommended for v0.7.1+ projects).")
def verify_receipts(repo: str, strict: bool) -> None:
    """Validate signatures + chain on every receipt in the project (v0.7.1+).

    Checks for: missing-parent links, causality violations, cycles, signature
    invalid (tampered receipt), unsigned receipts (in strict mode).
    """
    from bequite.receipts_signing import (
        load_public_key,
        verify_receipts_directory,
        DEFAULT_PUBLIC_KEY,
    )

    project = Path(repo).resolve()
    receipts_dir = project / ".bequite" / "receipts"
    pub_path = project / DEFAULT_PUBLIC_KEY

    # 1. Public key present?
    if not pub_path.exists():
        click.echo(f"error: no public key at {pub_path}.", err=True)
        click.echo("       run `bequite init` (which generates a keypair) or `bequite keygen`.", err=True)
        sys.exit(2)

    # 2. Signatures
    pub = load_public_key(pub_path)
    sig_ok, sig_issues, counts = verify_receipts_directory(receipts_dir, pub, strict=strict)
    click.echo(
        f"signature check: total={counts['total']} signed_valid={counts['signed_valid']} "
        f"signed_invalid={counts['signed_invalid']} unsigned={counts['unsigned']}"
    )
    for i in sig_issues:
        click.echo(f"  ! {i}", err=True)

    # 3. Chain
    store = receipts_module.ReceiptStore(str(receipts_dir))
    receipts = store.list_all()
    chain_ok, chain_issues = receipts_module.validate_chain(receipts)
    click.echo(f"chain check:     {len(receipts)} receipt(s); {'OK' if chain_ok else 'FAIL'}")
    for i in chain_issues:
        click.echo(f"  ! {i}", err=True)

    if sig_ok and chain_ok:
        sys.exit(0)
    sys.exit(1)


# ----------------------------------------------------------------------------
# bequite keygen (v0.7.1) — direct keypair generation (also called from init)
# ----------------------------------------------------------------------------


@cli.command()
@click.option("--repo", default=".")
@click.option("--overwrite", is_flag=True, default=False, help="Replace an existing keypair (WILL invalidate previous receipt signatures).")
def keygen(repo: str, overwrite: bool) -> None:
    """Generate a per-project ed25519 keypair for receipt signing (v0.7.1+)."""
    from bequite.receipts_signing import generate_keypair

    project = Path(repo).resolve()
    try:
        priv, pub = generate_keypair(project, overwrite=overwrite)
    except FileExistsError as e:
        click.echo(f"error: {e}", err=True)
        click.echo("       Pass --overwrite to regenerate (this WILL invalidate previous signatures).", err=True)
        sys.exit(2)
    click.echo("generated keypair:")
    click.echo(f"  private: {priv}  (chmod 0600; gitignored)")
    click.echo(f"  public:  {pub}   (chmod 0644; commit this)")
    click.echo("")
    click.echo("Reminders (auto-handled by `bequite init`; manual when running keygen standalone):")
    click.echo("  - Add '.bequite/.keys/' to .gitignore (private key MUST NEVER be committed).")
    click.echo("  - Commit '.bequite/keys/public.pem' so receipt signatures stay verifiable.")


# ----------------------------------------------------------------------------
# bequite route <subcommand> — multi-model routing inspection (v0.8.0)
# ----------------------------------------------------------------------------


@cli.group(name="route")
def route_group() -> None:
    """Inspect / probe the multi-model routing matrix (v0.8.0+)."""


@route_group.command("show")
@click.option("--phase", required=True, help="P0..P7 / any / any-boundary / always-on / orchestrator.")
@click.option("--persona", required=True, help="One of the 17 personas in skill/agents/.")
@click.option("--repo", default=".")
def route_show(phase: str, persona: str, repo: str) -> None:
    """Print the route a (phase, persona) pair would resolve to."""
    import json
    from bequite.router import select_route
    repo_path = Path(repo).resolve()
    route = select_route(phase=phase, persona=persona, repo_root=repo_path)
    click.echo(json.dumps({
        "phase": route.phase,
        "persona": route.persona,
        "model": route.model,
        "reasoning_effort": route.reasoning_effort,
        "fallback_model": route.fallback_model,
        "max_input_tokens": route.max_input_tokens,
        "max_output_tokens": route.max_output_tokens,
        "provider": route.provider,
        "note": route.note,
    }, indent=2, sort_keys=True))


@route_group.command("list")
@click.option("--repo", default=".")
def route_list(repo: str) -> None:
    """List every routing row in skill/routing.json."""
    import json
    from bequite.router import find_routing_path
    repo_path = Path(repo).resolve()
    path = find_routing_path(repo_path)
    if not path:
        click.echo("error: no routing.json found", err=True)
        sys.exit(2)
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("phase_routing", [])
    click.echo(f"{'phase':18s} {'persona':22s} {'model':22s} {'effort':8s} {'fallback':16s}")
    click.echo("-" * 90)
    for row in rows:
        click.echo(
            f"{row.get('phase', ''):18s} {row.get('persona', ''):22s} "
            f"{row.get('model', ''):22s} {row.get('reasoning_effort', ''):8s} "
            f"{(row.get('fallback_model') or ''):16s}"
        )


@route_group.command("providers")
def route_providers() -> None:
    """Probe each provider for availability (SDK + API key)."""
    from bequite.providers import REGISTERED_PROVIDERS, get_provider
    click.echo(f"{'provider':12s} {'available':12s}")
    click.echo("-" * 28)
    for name in REGISTERED_PROVIDERS:
        p = get_provider(name)
        status = "yes" if p.is_available() else "no"
        click.echo(f"{name:12s} {status:12s}")


# ----------------------------------------------------------------------------
# bequite ledger show — current session cost ledger
# ----------------------------------------------------------------------------


@cli.group(name="ledger")
def ledger_group() -> None:
    """Inspect / reset the session cost ledger (v0.8.0+)."""


@ledger_group.command("show")
@click.option("--repo", default=".")
def ledger_show(repo: str) -> None:
    """Display the current session's ledger summary."""
    import json
    from bequite.cost_ledger import session_summary
    s = session_summary(Path(repo).resolve())
    if not s.get("session_id"):
        click.echo("(no ledger yet — make at least one model call to populate)")
        return
    click.echo(json.dumps(s, indent=2, sort_keys=True))


@ledger_group.command("reset")
@click.option("--repo", default=".")
def ledger_reset(repo: str) -> None:
    """Reset session totals (keeps the call history)."""
    from bequite.cost_ledger import reset_session
    reset_session(Path(repo).resolve())
    click.echo("session ledger reset (call history preserved)")


# ----------------------------------------------------------------------------
# bequite pricing <subcommand> — live pricing fetch + cache (v0.8.1)
# ----------------------------------------------------------------------------


@cli.group(name="pricing")
def pricing_group() -> None:
    """Live model pricing fetch + cache (v0.8.1+)."""


@pricing_group.command("show")
@click.argument("model")
@click.option("--repo", default=".")
@click.option("--ttl-hours", type=int, default=24)
def pricing_show(model: str, repo: str, ttl_hours: int) -> None:
    """Show pricing for a single model (cache → fallback)."""
    sys.exit(pricing_module.main(["--repo", repo, "show", model, "--ttl-hours", str(ttl_hours)]))


@pricing_group.command("list")
@click.option("--repo", default=".")
def pricing_list(repo: str) -> None:
    """List all known models with cache + fallback rates."""
    sys.exit(pricing_module.main(["--repo", repo, "list"]))


@pricing_group.command("refresh")
@click.option("--repo", default=".")
@click.option("--provider", type=click.Choice(["anthropic", "openai", "google", "deepseek"]), default=None)
@click.option("--ttl-hours", type=int, default=24)
def pricing_refresh(repo: str, provider: str | None, ttl_hours: int) -> None:
    """Fetch live pricing and update the cache (best-effort)."""
    args = ["--repo", repo, "refresh", "--ttl-hours", str(ttl_hours)]
    if provider:
        args.extend(["--provider", provider])
    sys.exit(pricing_module.main(args))


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
