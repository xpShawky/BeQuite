"""bequite.exporters — Vibe-handoff exporters (v0.13.0).

Two formats:
- spec-kit-zip: zip artifacts in Spec-Kit-compatible format (specs/ + memory/ + decisions/).
- claude-code-skill: export `.bequite/` as a Claude Skill bundle (SKILL.md + agents/ + commands/).

Plus JSON-schema validation for spec.md / plan.md / tasks.md / phases.md headers.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import io
import json
import pathlib
import re
import sys
import zipfile
from typing import Optional


REQUIRED_FRONTMATTER_KEYS = {
    "spec.md": {"feature", "version", "status"},
    "plan.md": {"feature", "scale_tier", "stack_decided"},
    "tasks.md": {"feature", "phase", "task_count"},
    "phases.md": {"feature", "phase_count"},
}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML frontmatter (between leading --- markers). Returns dict."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def validate_artifact(path: pathlib.Path) -> tuple[bool, list[str]]:
    """Validate frontmatter of one artifact. Returns (ok, missing_keys)."""
    name = path.name
    required = REQUIRED_FRONTMATTER_KEYS.get(name)
    if required is None:
        return (True, [])
    if not path.exists():
        return (False, [f"file not found: {path}"])
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    missing = sorted(required - set(fm.keys()))
    return (not missing, missing)


# ---------------------------------------------------------------------- spec-kit-zip


def export_spec_kit_zip(repo_root: pathlib.Path, output: Optional[pathlib.Path] = None) -> pathlib.Path:
    """Bundle specs/ + .bequite/memory/ into a zip per Spec-Kit conventions."""
    if output is None:
        ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H-%M")
        output = repo_root / "dist" / f"spec-kit-export-{ts}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)

    paths_to_include = [
        repo_root / "specs",
        repo_root / ".bequite" / "memory",
        repo_root / "AGENTS.md",
        repo_root / "CLAUDE.md",
    ]

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        manifest = {
            "format": "spec-kit-zip",
            "version": "1",
            "exported_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            "source": "bequite",
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
        for src in paths_to_include:
            if not src.exists():
                continue
            if src.is_file():
                zf.write(src, arcname=src.relative_to(repo_root).as_posix())
            else:
                for f in src.rglob("*"):
                    if f.is_file() and not any(seg in (".git", "__pycache__", ".venv") for seg in f.parts):
                        zf.write(f, arcname=f.relative_to(repo_root).as_posix())
    return output


# ---------------------------------------------------------------------- claude-code-skill


def export_claude_skill(repo_root: pathlib.Path, output: Optional[pathlib.Path] = None) -> pathlib.Path:
    """Export `.bequite/` + skill/ + active doctrines as a Claude-Code skill bundle."""
    if output is None:
        ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H-%M")
        output = repo_root / "dist" / f"claude-skill-{ts}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)

    skill_root = repo_root / "skill"
    if not skill_root.exists():
        # Fallback: walk up to find BeQuite source root.
        cand = repo_root
        for _ in range(5):
            cand = cand.parent
            if (cand / "skill" / "SKILL.md").exists():
                skill_root = cand / "skill"
                break

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        manifest = {
            "format": "claude-code-skill",
            "version": "1",
            "exported_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            "source": "bequite",
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
        if skill_root.exists():
            for f in skill_root.rglob("*"):
                if f.is_file() and not any(seg in (".git", "__pycache__", ".venv") for seg in f.parts):
                    zf.write(f, arcname=("skill/" + f.relative_to(skill_root).as_posix()))
        for extra in ("AGENTS.md", "CLAUDE.md"):
            ep = repo_root / extra
            if ep.exists():
                zf.write(ep, arcname=extra)
    return output


# ---------------------------------------------------------------------- CLI


def _validate_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    artifacts = list(repo.glob("specs/**/spec.md")) + list(repo.glob("specs/**/plan.md")) \
        + list(repo.glob("specs/**/tasks.md")) + list(repo.glob("specs/**/phases.md"))
    if not artifacts:
        print("(no specs/ artifacts found)")
        return 0
    overall_ok = True
    for a in artifacts:
        ok, missing = validate_artifact(a)
        status = "OK" if ok else f"MISSING: {missing}"
        print(f"  {a.relative_to(repo)}: {status}")
        overall_ok = overall_ok and ok
    return 0 if overall_ok else 1


def _spec_kit_zip_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    out = pathlib.Path(args.output).resolve() if args.output else None
    target = export_spec_kit_zip(repo, out)
    print(f"exported spec-kit-zip → {target}")
    return 0


def _claude_skill_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    out = pathlib.Path(args.output).resolve() if args.output else None
    target = export_claude_skill(repo, out)
    print(f"exported claude-code-skill → {target}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-export", description="Vibe-handoff exporters (v0.13.0).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate spec/plan/tasks/phases frontmatter.")
    v.set_defaults(fn=_validate_cmd)

    sk = sub.add_parser("spec-kit-zip", help="Export specs/ + memory/ as Spec-Kit-compatible zip.")
    sk.add_argument("--output", default=None)
    sk.set_defaults(fn=_spec_kit_zip_cmd)

    cs = sub.add_parser("claude-skill", help="Export skill/ + AGENTS.md + CLAUDE.md as a Claude Skill bundle.")
    cs.add_argument("--output", default=None)
    cs.set_defaults(fn=_claude_skill_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
