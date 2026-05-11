"""Subcommand implementations for the BeQuite CLI.

Most commands are thin dispatchers — they prepare the context (Memory Bank,
state files, the relevant prompt-pack) and call out to a model via the skill
loader. The audit + freshness commands are fully local (no API call needed).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
err_console = Console(stderr=True)


# ----------------------------------------------------------------------------
# bequite doctor
# ----------------------------------------------------------------------------


def run_doctor(repo_root: Path) -> int:
    """Environment + state-coherence check (master §17.2 — adapted).

    v1.0.4: extended with a "Studio runtime" group that surfaces Node/Bun/Docker
    availability. These are optional for the CLI alone but required for the
    Studio (marketing + dashboard + API). Missing tools surface a clear install
    hint instead of a stack trace later.
    """
    checks: list[tuple[str, str, bool, str]] = []   # (group, name, ok, hint)

    # --- Tooling (required for CLI) ---
    for tool, hint in [
        ("git", "install git: https://git-scm.com"),
        ("python", "install Python 3.11+: https://python.org"),
        ("jq", "install jq for hook JSON parsing (optional for CLI; required for hooks)"),
    ]:
        ok = shutil.which(tool) is not None
        checks.append(("Tooling", tool, ok, hint if not ok else ""))

    # --- Studio runtime (required only if you want to run studio/) ---
    studio_tools = [
        ("node", ">=20", "install Node.js 20+: https://nodejs.org"),
        ("npm", ">=10", "ships with Node.js"),
        ("bun", ">=1.1", "powershell -c \"irm bun.sh/install.ps1 | iex\" | curl -fsSL https://bun.sh/install | bash"),
        ("docker", ">=24", "install Docker Desktop: https://www.docker.com/products/docker-desktop/"),
    ]
    for tool, _min, hint in studio_tools:
        ok = shutil.which(tool) is not None
        checks.append(("Studio runtime", tool, ok, hint if not ok else ""))

    # Docker daemon reachability (separate from binary presence)
    if shutil.which("docker"):
        try:
            r = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=4,
            )
            daemon_ok = r.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            daemon_ok = False
        checks.append((
            "Studio runtime", "docker daemon", daemon_ok,
            "start Docker Desktop and wait for 'Engine running'" if not daemon_ok else "",
        ))

    # --- Port availability (3000/3001/3002 for Studio) ---
    for port in (3000, 3001, 3002):
        ok = _port_is_free(port)
        checks.append((
            "Ports", f"localhost:{port}", ok,
            f"stop the process using :{port} OR run `docker compose down`" if not ok else "",
        ))

    # --- BeQuite scaffolding ---
    for path, hint in [
        (".bequite/memory/constitution.md", "run `bequite init <name>`"),
        (".bequite/memory/projectbrief.md", "Memory Bank missing"),
        (".bequite/memory/activeContext.md", "Memory Bank missing"),
        ("state/project.yaml", "state/ missing"),
        ("state/recovery.md", "state/ missing"),
        ("state/task_index.json", "state/ missing"),
        ("AGENTS.md", "universal entry missing"),
    ]:
        ok = (repo_root / path).exists()
        checks.append(("BeQuite scaffolding", path, ok, hint if not ok else ""))

    # --- Skill ---
    skill_locations = [
        repo_root / "skill" / "SKILL.md",
        repo_root / ".claude" / "skills" / "bequite" / "SKILL.md",
    ]
    skill_ok = any(p.exists() for p in skill_locations)
    checks.append(("Skill", "SKILL.md", skill_ok, "run `bequite skill install <host>`"))

    # --- Hooks ---
    hooks = [
        "skill/hooks/pretooluse-secret-scan.sh",
        "skill/hooks/pretooluse-block-destructive.sh",
        "skill/hooks/pretooluse-verify-package.sh",
        "skill/hooks/stop-verify-before-done.sh",
        "skill/hooks/sessionstart-load-memory.sh",
    ]
    for h in hooks:
        ok = (repo_root / h).exists()
        checks.append(("Hooks", h, ok, "skill/hooks/ missing"))

    # --- Render ---
    table = Table(title=f"bequite doctor — {repo_root}")
    table.add_column("Group")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Hint")
    for group, name, ok, hint in checks:
        status = "[green]OK[/green]" if ok else "[red]MISSING[/red]"
        table.add_row(group, name, status, hint)
    console.print(table)

    failures = [c for c in checks if not c[2]]
    if failures:
        err_console.print(f"\n[red]{len(failures)} check(s) failed.[/red]")
        return 1
    console.print("\n[green]All checks passed.[/green]")
    return 0


# ----------------------------------------------------------------------------
# bequite init
# ----------------------------------------------------------------------------


def run_init(
    project_name: str,
    doctrines: list[str],
    mode: str,
    scale_tier: str,
    audience: str,
) -> int:
    """Scaffold a fresh BeQuite-managed project at ./<project_name>/."""
    target = Path(project_name).resolve()
    if target.exists():
        err_console.print(f"[red]Target {target} already exists. Refusing to overwrite.[/red]")
        return 1

    # Locate the BeQuite source (where this CLI is installed from).
    bequite_src = _find_bequite_source()
    if not bequite_src:
        err_console.print(
            "[red]Could not locate the BeQuite source tree. "
            "Run from a BeQuite-developed checkout, or install via "
            "`uvx --from git+https://github.com/xpShawky/BeQuite bequite init <name>`.[/red]"
        )
        return 1

    template = bequite_src / "template"
    if not template.exists():
        err_console.print(f"[red]Template directory missing at {template}.[/red]")
        return 1

    # Copy template/ → target/
    shutil.copytree(template, target)

    # Copy active doctrines + skill into the new project.
    skills_target = target / ".claude" / "skills" / "bequite"
    skills_target.mkdir(parents=True, exist_ok=True)
    for path in [
        bequite_src / "skill" / "SKILL.md",
        bequite_src / "skill" / "routing.json",
    ]:
        if path.exists():
            shutil.copy(path, skills_target / path.name)
    for sub in ["agents", "commands", "hooks", "templates", "references"]:
        src_sub = bequite_src / "skill" / sub
        if src_sub.exists():
            shutil.copytree(src_sub, skills_target / sub, dirs_exist_ok=True)
    # Copy active doctrines only.
    doc_target = skills_target / "doctrines"
    doc_target.mkdir(parents=True, exist_ok=True)
    for d in doctrines:
        src_doc = bequite_src / "skill" / "doctrines" / f"{d}.md"
        if src_doc.exists():
            shutil.copy(src_doc, doc_target / src_doc.name)
    # Copy bundled skills only when the relevant Doctrine is loaded.
    bundled_target = skills_target / "skills-bundled"
    bundled_target.mkdir(parents=True, exist_ok=True)
    if "default-web-saas" in doctrines or "mena-bilingual" in doctrines:
        # Impeccable bundled snapshot (vendor pinned in v0.6.1+).
        impeccable_src = bequite_src / "skill" / "skills-bundled" / "impeccable"
        if impeccable_src.exists():
            shutil.copytree(impeccable_src, bundled_target / "impeccable", dirs_exist_ok=True)
    if "ai-automation" in doctrines:
        auto_src = bequite_src / "skill" / "skills-bundled" / "ai-automation"
        if auto_src.exists():
            shutil.copytree(auto_src, bundled_target / "ai-automation", dirs_exist_ok=True)

    # Render bequite.config.toml from the template.
    config_tpl = bequite_src / "skill" / "templates" / "bequite.config.toml.tpl"
    config_dest = target / ".bequite" / "bequite.config.toml"
    config_dest.parent.mkdir(parents=True, exist_ok=True)
    if config_tpl.exists():
        text = config_tpl.read_text(encoding="utf-8")
        slug = project_name.lower().replace(" ", "-")
        replacements = {
            "{{PROJECT_NAME}}": project_name,
            "{{PROJECT_SLUG}}": slug,
            "{{PROJECT_OWNER}}": "your-handle",
            "{{MAINTAINER_EMAIL}}": "you@example.com",
            "{{LICENSE}}": "MIT",
            "{{MODE}}": mode,
            "{{AUDIENCE}}": audience,
            "{{ACTIVE_DOCTRINES}}": ", ".join(f'"{d}"' for d in doctrines),
            "{{SCALE_TIER}}": scale_tier,
            "{{COMPLIANCE}}": "",
            "{{LOCALES}}": '"en-US"',
            "{{PRIMARY_HOST}}": "claude-code",
            "{{HOST_LIST}}": '"claude-code"',
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        config_dest.write_text(text, encoding="utf-8")

    # v0.7.1+: generate ed25519 keypair for receipt signing.
    keygen_status = "skipped (already present)"
    try:
        from bequite.receipts_signing import generate_keypair
        priv, pub = generate_keypair(target, overwrite=False)
        keygen_status = f"generated → {priv.relative_to(target)} + {pub.relative_to(target)}"
    except FileExistsError:
        keygen_status = "already present (kept)"
    except (ImportError, OSError) as e:
        keygen_status = f"FAILED ({e}) — run `bequite keygen` manually"

    # Append .bequite/.keys/ to .gitignore so the private key is never committed.
    # The template/.gitignore should already include this, but defend belt-and-braces.
    gitignore_path = target / ".gitignore"
    keys_pattern = ".bequite/.keys/\n.bequite/.keys/*\n"
    if gitignore_path.exists():
        existing = gitignore_path.read_text(encoding="utf-8")
        if ".bequite/.keys" not in existing:
            with gitignore_path.open("a", encoding="utf-8") as f:
                f.write("\n# v0.7.1 — never commit ed25519 private keys (Article IV).\n")
                f.write(keys_pattern)
    else:
        gitignore_path.write_text(
            "# v0.7.1 — never commit ed25519 private keys (Article IV).\n" + keys_pattern,
            encoding="utf-8",
        )

    console.print(Panel.fit(
        f"[green]Initialised {project_name} at {target}[/green]\n\n"
        f"  Mode:       {mode}\n"
        f"  Audience:   {audience}\n"
        f"  Scale tier: {scale_tier}\n"
        f"  Doctrines:  {', '.join(doctrines)}\n"
        f"  Keypair:    {keygen_status}\n\n"
        f"Next steps:\n"
        f"  cd {project_name}\n"
        f"  bequite doctor\n"
        f"  bequite discover            # P0 product discovery\n"
        f"  bequite research <topic>    # P0 research scan\n"
        f"  bequite decide-stack        # P1 stack ADR\n"
        f"  bequite verify-receipts     # validate signed receipts (v0.7.1+)\n",
        title="bequite init",
    ))
    return 0


def _find_bequite_source() -> Path | None:
    """Locate the BeQuite source tree (where skill/ + template/ live)."""
    here = Path(__file__).resolve()
    # Walk up from this file looking for a 'skill/SKILL.md'.
    for parent in [here.parent.parent.parent, *here.parents]:
        if (parent / "skill" / "SKILL.md").exists() and (parent / "template").exists():
            return parent
    return None


# ----------------------------------------------------------------------------
# bequite recover
# ----------------------------------------------------------------------------


def run_recover(repo_root: Path) -> int:
    """Generate the paste-able recovery prompt."""
    state_recovery = repo_root / "state" / "recovery.md"
    if not state_recovery.exists():
        err_console.print(f"[red]No state/recovery.md found at {repo_root}. Run `bequite init` first.[/red]")
        return 1

    # Read the recovery prompt template.
    prompt_path = repo_root / "prompts" / "recovery_prompt.md"
    if not prompt_path.exists():
        # Fallback to the bundled prompt.
        bequite_src = _find_bequite_source()
        if bequite_src:
            prompt_path = bequite_src / "prompts" / "recovery_prompt.md"
    if not prompt_path.exists():
        err_console.print("[red]No recovery prompt template found.[/red]")
        return 1

    template = prompt_path.read_text(encoding="utf-8")
    recovery_state = state_recovery.read_text(encoding="utf-8")

    # Compose the output.
    output = (
        "# bequite recover — paste-able prompt\n\n"
        "_Generated_: "
        f"{datetime.now(timezone.utc).isoformat()}\n\n"
        "---\n\n"
        f"{template}\n\n"
        "---\n\n"
        "## Current state/recovery.md\n\n"
        f"{recovery_state}\n"
    )
    console.print(output)
    return 0


# ----------------------------------------------------------------------------
# bequite memory
# ----------------------------------------------------------------------------


MEMORY_FILES = {
    "constitution": ".bequite/memory/constitution.md",
    "projectbrief": ".bequite/memory/projectbrief.md",
    "productContext": ".bequite/memory/productContext.md",
    "systemPatterns": ".bequite/memory/systemPatterns.md",
    "techContext": ".bequite/memory/techContext.md",
    "activeContext": ".bequite/memory/activeContext.md",
    "progress": ".bequite/memory/progress.md",
    "recovery": "state/recovery.md",
    "current_phase": "state/current_phase.md",
    "project_yaml": "state/project.yaml",
}


def run_memory_show(repo_root: Path, target: str | None) -> int:
    """Print Memory Bank or specific file."""
    if target is None:
        for key, path in MEMORY_FILES.items():
            full = repo_root / path
            console.print(f"\n[bold cyan]{path}[/bold cyan]\n" + "-" * 60)
            if full.exists():
                console.print(full.read_text(encoding="utf-8"))
            else:
                console.print(f"[yellow](missing)[/yellow]")
        return 0
    if target in MEMORY_FILES:
        full = repo_root / MEMORY_FILES[target]
        if full.exists():
            console.print(full.read_text(encoding="utf-8"))
            return 0
        err_console.print(f"[red]Missing: {full}[/red]")
        return 1
    # Try Doctrine.
    for d_path in [
        repo_root / "skill" / "doctrines" / f"{target}.md",
        repo_root / ".claude" / "skills" / "bequite" / "doctrines" / f"{target}.md",
    ]:
        if d_path.exists():
            console.print(d_path.read_text(encoding="utf-8"))
            return 0
    err_console.print(f"[red]Unknown target: {target}.[/red]")
    return 1


def run_memory_validate(repo_root: Path) -> int:
    """Schema-validate every Memory Bank + state file."""
    findings: list[tuple[str, str, str]] = []  # (file, severity, message)
    for key, path in MEMORY_FILES.items():
        full = repo_root / path
        if not full.exists():
            findings.append((path, "fail", "missing"))
            continue
        text = full.read_text(encoding="utf-8")
        if len(text.strip()) < 50:
            findings.append((path, "warn", "suspiciously short content"))

    table = Table(title="bequite memory validate")
    table.add_column("File")
    table.add_column("Status")
    table.add_column("Note")
    for f, sev, msg in findings:
        col = {"fail": "red", "warn": "yellow", "pass": "green"}.get(sev, "white")
        table.add_row(f, f"[{col}]{sev.upper()}[/{col}]", msg)
    if not findings:
        console.print("[green]All Memory Bank + state files present and non-empty.[/green]")
        return 0
    console.print(table)
    fails = [f for f in findings if f[1] == "fail"]
    return 1 if fails else 0


# ----------------------------------------------------------------------------
# bequite skill install (per-host)
# ----------------------------------------------------------------------------


def run_skill_install(host: str, repo_root: Path) -> int:
    """Install BeQuite into the named host's discovery path."""
    bequite_src = _find_bequite_source()
    if not bequite_src:
        err_console.print("[red]Could not locate BeQuite source.[/red]")
        return 1

    skill_src = bequite_src / "skill"
    if not skill_src.exists():
        err_console.print(f"[red]No skill source at {skill_src}.[/red]")
        return 1

    targets: list[Path] = {
        "claude-code": [repo_root / ".claude" / "skills" / "bequite"],
        "cursor": [repo_root / ".cursor" / "skills" / "bequite"],
        "codex": [repo_root / ".codex" / "skills" / "bequite"],
        "gemini": [repo_root / ".gemini" / "skills" / "bequite"],
        "windsurf": [repo_root / ".windsurf" / "skills" / "bequite"],
        "cline": [repo_root / ".cline" / "skills" / "bequite"],
        "kilo": [repo_root / ".kilocode" / "skills" / "bequite"],
        "continue": [repo_root / ".continue" / "skills" / "bequite"],
        "aider": [repo_root / ".aider" / "skills" / "bequite"],
    }.get(host, [])

    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        # Copy skill content.
        shutil.copy(skill_src / "SKILL.md", target / "SKILL.md")
        for sub in ["agents", "commands", "hooks", "templates", "doctrines", "references"]:
            src = skill_src / sub
            if src.exists():
                shutil.copytree(src, target / sub, dirs_exist_ok=True)
        if (skill_src / "routing.json").exists():
            shutil.copy(skill_src / "routing.json", target / "routing.json")
        bundled = skill_src / "skills-bundled"
        if bundled.exists():
            shutil.copytree(bundled, target / "skills-bundled", dirs_exist_ok=True)
        console.print(f"[green]Installed BeQuite skill at {target}[/green]")

    # Host-specific generation (AGENTS.md, .cursor/rules, etc.) deferred to v0.12.0.
    console.print(
        "[yellow]Note: host-specific adapter generation (AGENTS.md / .cursor/rules / "
        ".gemini config / etc.) lands in v0.12.0. The skill content is copied; per-host "
        "rule generation is a follow-up.[/yellow]"
    )
    return 0


# ----------------------------------------------------------------------------
# Skill-dispatching command (v0.5.0 stub — full Claude API dispatch in v0.6.0+)
# ----------------------------------------------------------------------------


def run_skill_command(name: str, repo_root: Path, **kwargs: Any) -> int:
    """Dispatch to the skill command via Claude API.

    v0.5.0 STUB: prints the prompt that *would* be sent + the inputs that would
    be loaded, without actually making the API call. v0.6.0 ships the live
    Claude API call via `skill_loader.py`. This lets users see the dispatch
    contract and verify their environment before turning on the API call.
    """
    from bequite.skill_loader import build_dispatch_payload

    payload = build_dispatch_payload(name, repo_root, **kwargs)
    console.print(Panel.fit(
        f"[bold]Skill command:[/bold] /{name}\n\n"
        f"[bold]Repo:[/bold] {repo_root}\n"
        f"[bold]Args:[/bold] {kwargs or '(none)'}\n\n"
        f"[bold]Inputs that would be loaded:[/bold]\n"
        + "\n".join(f"  - {p}" for p in payload.get("input_files", []))
        + f"\n\n[bold]Persona:[/bold] {payload.get('persona', '?')}\n"
        f"[bold]Model:[/bold] {payload.get('model', '?')} "
        f"({payload.get('reasoning_effort', '?')})\n\n"
        "[yellow]v0.5.0 STUB: dispatch contract surfaced; live API call lands in v0.6.0+.[/yellow]\n"
        "[yellow]To proceed manually: paste the relevant prompt-pack into your "
        "host (Claude Code / Cursor / Codex), and the skill will pick it up.[/yellow]",
        title=f"bequite {name}",
    ))
    return 0


# ----------------------------------------------------------------------------
# bequite dev — bring up the local Studio stack (v1.0.4+)
# ----------------------------------------------------------------------------


def run_dev(repo_root: Path, detach: bool = False) -> int:
    """Bring up the Studio stack (marketing + dashboard + api).

    Prefers Docker if the daemon is running. Falls back to instructions for
    native dev if Docker is missing.
    """
    docker_ok = False
    if shutil.which("docker"):
        try:
            r = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=4,
            )
            docker_ok = r.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            docker_ok = False

    if docker_ok and (repo_root / "docker-compose.yml").exists():
        console.print(Panel(
            "[green]Starting BeQuite Studio via Docker Compose[/green]\n"
            "[dim]docker compose up --build" + (" -d" if detach else "") + "[/dim]\n\n"
            "  http://localhost:3000   marketing\n"
            "  http://localhost:3001   dashboard\n"
            "  http://localhost:3002   api\n\n"
            "Stop with [bold]docker compose down[/bold] (or [bold]bequite dev --down[/bold]).",
            title="bequite dev",
        ))
        cmd = ["docker", "compose", "up", "--build"]
        if detach:
            cmd.append("-d")
        try:
            return subprocess.call(cmd, cwd=str(repo_root))
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Run `bequite dev --down` to stop containers.[/yellow]")
            return 130

    # Docker not available — print clear native-dev instructions.
    err_console.print(
        "[yellow]Docker daemon not reachable. Falling back to native instructions.[/yellow]\n"
    )
    console.print(Panel(
        "Run these in three separate terminals:\n\n"
        "[bold]Terminal 1[/bold] — API on :3002\n"
        "  [cyan]cd studio/api && bun run src/index.ts[/cyan]\n\n"
        "[bold]Terminal 2[/bold] — Dashboard on :3001 (HTTP mode)\n"
        "  Windows: [cyan]cd studio/dashboard; $env:BEQUITE_DASHBOARD_MODE='http'; npm run dev[/cyan]\n"
        "  Unix:    [cyan]cd studio/dashboard && BEQUITE_DASHBOARD_MODE=http npm run dev[/cyan]\n\n"
        "[bold]Terminal 3[/bold] — Marketing on :3000\n"
        "  [cyan]cd studio/marketing && npm run dev[/cyan]\n\n"
        "[dim]Bun install: https://bun.sh  |  Docker install: https://docker.com[/dim]",
        title="bequite dev — native mode",
    ))
    return 1


def run_dev_down(repo_root: Path) -> int:
    """Stop the Studio stack."""
    if shutil.which("docker") and (repo_root / "docker-compose.yml").exists():
        return subprocess.call(["docker", "compose", "down"], cwd=str(repo_root))
    err_console.print("[yellow]Docker not available; stop native dev servers with Ctrl+C in each terminal.[/yellow]")
    return 1


# ----------------------------------------------------------------------------
# bequite status — quick health probe (v1.0.4+)
# ----------------------------------------------------------------------------


def run_status(repo_root: Path) -> int:
    """Probe the three Studio services + report up/down for each."""
    import urllib.request
    import urllib.error

    targets = [
        ("api",       "http://localhost:3002/healthz",         200),
        ("dashboard", "http://localhost:3001/",                200),
        ("marketing", "http://localhost:3000/",                200),
    ]

    table = Table(title="bequite status — Studio service probes")
    table.add_column("Service")
    table.add_column("URL")
    table.add_column("Status")
    table.add_column("Notes")

    any_down = False
    for name, url, expected in targets:
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                code = r.status
                if code == expected:
                    table.add_row(name, url, "[green]UP[/green]", f"HTTP {code}")
                else:
                    table.add_row(name, url, "[yellow]ODD[/yellow]", f"got HTTP {code}")
                    any_down = True
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            table.add_row(name, url, "[red]DOWN[/red]", reason[:50])
            any_down = True
        except Exception as e:
            table.add_row(name, url, "[red]ERR[/red]", str(e)[:50])
            any_down = True

    console.print(table)
    if any_down:
        err_console.print(
            "\n[yellow]Some services are down. Try `bequite dev` to bring them up.[/yellow]"
        )
        return 1
    console.print("\n[green]All Studio services up.[/green]")
    return 0


def _port_is_free(port: int) -> bool:
    """Return True if nothing is listening on localhost:<port>."""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex(("127.0.0.1", port))
    except OSError:
        return True
    finally:
        s.close()
    # connect_ex returns 0 on success (port IS bound). Non-zero = free.
    return result != 0
