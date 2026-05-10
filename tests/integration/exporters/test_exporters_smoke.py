"""Integration smoke test for cli/bequite/exporters.py (BeQuite v0.13.0)."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import zipfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.exporters import (  # noqa: E402
    REQUIRED_FRONTMATTER_KEYS,
    export_claude_skill,
    export_spec_kit_zip,
    parse_frontmatter,
    validate_artifact,
)


def test_parse_frontmatter_basic() -> None:
    text = "---\nfeature: x\nversion: 1.0\nstatus: draft\n---\n\n# Heading\n"
    fm = parse_frontmatter(text)
    assert fm == {"feature": "x", "version": "1.0", "status": "draft"}


def test_parse_frontmatter_no_block_returns_empty() -> None:
    assert parse_frontmatter("# Just a heading\n") == {}


def test_validate_artifact_complete_spec_md() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "spec.md"
        p.write_text("---\nfeature: x\nversion: 1\nstatus: draft\n---\n", encoding="utf-8")
        ok, missing = validate_artifact(p)
        assert ok is True
        assert missing == []


def test_validate_artifact_missing_keys() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "spec.md"
        p.write_text("---\nfeature: x\n---\n", encoding="utf-8")
        ok, missing = validate_artifact(p)
        assert ok is False
        assert "version" in missing
        assert "status" in missing


def test_validate_artifact_unknown_filename_passes() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "random.md"
        p.write_text("# X", encoding="utf-8")
        ok, missing = validate_artifact(p)
        assert ok is True


def test_export_spec_kit_zip_creates_file() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        (repo / "specs" / "feat-x").mkdir(parents=True)
        (repo / "specs" / "feat-x" / "spec.md").write_text("---\nfeature: x\nversion: 1\nstatus: draft\n---\n", encoding="utf-8")
        (repo / ".bequite" / "memory").mkdir(parents=True)
        (repo / ".bequite" / "memory" / "constitution.md").write_text("# Iron Laws", encoding="utf-8")
        target = export_spec_kit_zip(repo)
        assert target.exists()
        with zipfile.ZipFile(target) as zf:
            names = zf.namelist()
            assert "manifest.json" in names
            assert any("specs/feat-x/spec.md" in n for n in names)
            assert any(".bequite/memory/constitution.md" in n for n in names)


def test_export_claude_skill_creates_file() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        skill = repo / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Skill", encoding="utf-8")
        (skill / "agents").mkdir()
        (skill / "agents" / "demo.md").write_text("agent", encoding="utf-8")
        target = export_claude_skill(repo)
        assert target.exists()
        with zipfile.ZipFile(target) as zf:
            names = zf.namelist()
            assert "manifest.json" in names
            assert "skill/SKILL.md" in names
            assert "skill/agents/demo.md" in names


def test_required_frontmatter_keys_complete() -> None:
    assert "spec.md" in REQUIRED_FRONTMATTER_KEYS
    assert "plan.md" in REQUIRED_FRONTMATTER_KEYS
    assert "tasks.md" in REQUIRED_FRONTMATTER_KEYS
    assert "phases.md" in REQUIRED_FRONTMATTER_KEYS


def _run_all() -> int:
    tests = [
        test_parse_frontmatter_basic,
        test_parse_frontmatter_no_block_returns_empty,
        test_validate_artifact_complete_spec_md,
        test_validate_artifact_missing_keys,
        test_validate_artifact_unknown_filename_passes,
        test_export_spec_kit_zip_creates_file,
        test_export_claude_skill_creates_file,
        test_required_frontmatter_keys_complete,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures += 1
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_run_all())
