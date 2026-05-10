"""bequite.skill_install — Per-host adapter installer (v0.12.0).

Detects the active host(s) in a project and writes per-host config files:

- Claude Code: CLAUDE.md (extends AGENTS.md).
- Cursor: .cursor/rules/*.mdc.
- Codex CLI: .codex/AGENTS.md (symlink to root AGENTS.md).
- Cline: .clinerules/bequite.md.
- Kilo Code: .kilocode/bequite.md.
- Continue.dev: .continuerules/bequite.md.
- Aider: .aider/AGENTS.md.
- Windsurf: .windsurf/cascades/bequite.md.
- Gemini CLI: .gemini/memory.md.

CLI: `python -m bequite.skill_install detect|install [--host <name>]`.

The hosts above all read AGENTS.md first (Linux Foundation Agentic AI
Foundation schema); host-specific files extend.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Optional


HOSTS = {
    "claude-code": "CLAUDE.md",
    "cursor": ".cursor/rules/bequite-constitution.mdc",
    "codex": ".codex/AGENTS.md",
    "cline": ".clinerules/bequite.md",
    "kilo": ".kilocode/bequite.md",
    "continue": ".continuerules/bequite.md",
    "aider": ".aider/AGENTS.md",
    "windsurf": ".windsurf/cascades/bequite.md",
    "gemini": ".gemini/memory.md",
}


def detect_hosts(repo_root: pathlib.Path) -> list[str]:
    """Return the list of hosts already present in the project."""
    out: list[str] = []
    indicators = {
        "claude-code": ["CLAUDE.md", ".claude/"],
        "cursor": [".cursor/"],
        "codex": [".codex/"],
        "cline": [".clinerules/", ".cline/"],
        "kilo": [".kilocode/"],
        "continue": [".continuerules/", ".continue/"],
        "aider": [".aider/", ".aider.conf.yml"],
        "windsurf": [".windsurf/"],
        "gemini": [".gemini/"],
    }
    for host, paths in indicators.items():
        if any((repo_root / p).exists() for p in paths):
            out.append(host)
    return out


def install_host(repo_root: pathlib.Path, host: str) -> tuple[pathlib.Path, str]:
    """Install BeQuite config for one host. Returns (path, status)."""
    if host not in HOSTS:
        raise ValueError(f"unknown host {host!r}; choose from {list(HOSTS)}")
    target = repo_root / HOSTS[host]
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return (target, "already-present")
    # Stub content; specifics per-host below.
    content = _content_for_host(host)
    target.write_text(content, encoding="utf-8")
    return (target, "installed")


def _content_for_host(host: str) -> str:
    common = (
        "# BeQuite-managed project — host extension\n\n"
        "Read AGENTS.md first (universal entry per Linux Foundation Agentic AI Foundation schema).\n"
        "Read .bequite/memory/constitution.md for Iron Laws.\n\n"
        "Banned weasel words: should, probably, seems to, appears to, I think it works.\n\n"
    )
    if host == "claude-code":
        return common + "\nClaude Code reads this file as a session-start memory pin. "
    if host == "cursor":
        return (
            "---\n"
            "description: BeQuite operating contract\n"
            'globs: ["**/*"]\n'
            "alwaysApply: true\n"
            "---\n\n" + common
        )
    if host == "codex":
        return common + "\nCodex CLI uses AGENTS.md discovery; this file is for codex-specific overrides.\n"
    if host == "cline":
        return common + "\nCline reads `.clinerules/` files as system-prompt context.\n"
    if host == "kilo":
        return common + "\nKilo Code reads `.kilocode/` files as system context.\n"
    if host == "continue":
        return common + "\nContinue.dev reads `.continuerules/` files.\n"
    if host == "aider":
        return common + "\nAider reads AGENTS.md from this folder; no separate Aider config needed.\n"
    if host == "windsurf":
        return common + "\nWindsurf Cascades read `.windsurf/cascades/` folder.\n"
    if host == "gemini":
        return common + "\nGemini CLI reads `.gemini/memory.md` as a memory pin.\n"
    return common


def install_all_detected(repo_root: pathlib.Path) -> list[tuple[str, pathlib.Path, str]]:
    """Detect + install for every host found."""
    hosts = detect_hosts(repo_root)
    return [(h, *install_host(repo_root, h)) for h in hosts]


# ---------------------------------------------------------------------- CLI


def _detect_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    hosts = detect_hosts(repo)
    if not hosts:
        print("no hosts detected (no .claude/ or .cursor/ or .codex/ etc. found)")
        return 0
    print("detected hosts:")
    for h in hosts:
        print(f"  - {h:14s} target: {HOSTS[h]}")
    return 0


def _install_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    if args.host:
        if args.host not in HOSTS:
            print(f"error: unknown host {args.host!r}; choose from {list(HOSTS)}", file=sys.stderr)
            return 2
        path, status = install_host(repo, args.host)
        print(f"{args.host:14s} -> {path.relative_to(repo)} ({status})")
        return 0
    results = install_all_detected(repo)
    if not results:
        print("no hosts detected; pass --host <name> to install for a specific host")
        return 0
    for h, path, status in results:
        print(f"{h:14s} -> {path.relative_to(repo)} ({status})")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-skill-install", description="Per-host adapter installer (v0.12.0).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect", help="Detect which hosts are present in this project.")
    d.set_defaults(fn=_detect_cmd)
    i = sub.add_parser("install", help="Install BeQuite config for detected hosts (or one specific host).")
    i.add_argument("--host", default=None, choices=list(HOSTS))
    i.set_defaults(fn=_install_cmd)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
