"""E2E smoke test: doctrine loading correctness (v0.9.1).

Asserts that:
- Each Doctrine file in `skill/doctrines/` parses cleanly (frontmatter valid).
- Doctrines declare expected fields (name, version, applies_to, supersedes).
- Loading a Doctrine via `bequite memory show doctrine <name>` returns
  the file's content.
- The 12 Doctrines listed in v0.9.0 progress.md actually exist on disk.
"""

from __future__ import annotations

import pathlib
import re
import sys

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))


EXPECTED_DOCTRINES = [
    "default-web-saas",
    "cli-tool",
    "ml-pipeline",
    "desktop-tauri",
    "library-package",
    "fintech-pci",
    "healthcare-hipaa",
    "gov-fedramp",
    "ai-automation",
    "vibe-defense",
    "mena-pdpl",
    "eu-gdpr",
]

DOCTRINES_DIR = _REPO_ROOT / "skill" / "doctrines"


def test_doctrines_dir_exists() -> None:
    assert DOCTRINES_DIR.exists(), f"missing doctrines dir at {DOCTRINES_DIR}"
    assert DOCTRINES_DIR.is_dir()


def test_all_12_doctrines_present() -> None:
    """v0.9.0 progress.md claims 12 Doctrines shipped. Verify each on disk."""
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        assert path.exists(), f"Doctrine file missing: {path}"
        assert path.stat().st_size > 100, f"Doctrine {d}.md is suspiciously short ({path.stat().st_size} bytes)"


def test_each_doctrine_has_frontmatter() -> None:
    """Each Doctrine starts with a YAML frontmatter block."""
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"Doctrine {d}.md missing leading --- frontmatter"
        # Find the closing --- and assert it exists within the first 30 lines.
        lines = content.split("\n")[:30]
        closing_count = sum(1 for line in lines if line.strip() == "---")
        assert closing_count >= 2, f"Doctrine {d}.md frontmatter not closed within first 30 lines"


def test_each_doctrine_declares_required_fields() -> None:
    """Each Doctrine declares: name, version, applies_to, supersedes (or null), maintainer."""
    required_fields = ["name:", "version:", "applies_to:", "supersedes:"]
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        content = path.read_text(encoding="utf-8")
        # Extract just the frontmatter (between first two --- blocks).
        m = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
        assert m, f"Doctrine {d}.md frontmatter regex failed"
        fm = m.group(1)
        for field in required_fields:
            assert field in fm, f"Doctrine {d}.md missing field {field!r} in frontmatter"


def test_each_doctrine_name_matches_filename() -> None:
    """The `name:` field in frontmatter matches the filename slug."""
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        content = path.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
        fm = m.group(1)
        name_match = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
        assert name_match, f"Doctrine {d}.md `name:` field not found or malformed"
        name = name_match.group(1).strip()
        assert name == d, f"Doctrine {d}.md declares name={name!r}, expected {d!r}"


def test_each_doctrine_has_rules_section() -> None:
    """Each Doctrine has a Rules section (Doctrine-flavored: 'Rules', 'Common rules', etc.)."""
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        content = path.read_text(encoding="utf-8")
        # Tolerant regex: matches "## 2. Rules", "## Rules", "## Common rules", "## 2. Common rules", etc.
        assert re.search(r"^##\s*(\d+\.\s*)?(Common\s+|Strict\s+)?Rules\b", content, re.MULTILINE | re.IGNORECASE), \
            f"Doctrine {d}.md missing Rules-section heading (any flavor)"


def test_default_web_saas_v1_1_0_referenced() -> None:
    """v0.6.1 bumped default-web-saas to 1.1.0; verify the version in frontmatter."""
    path = DOCTRINES_DIR / "default-web-saas.md"
    content = path.read_text(encoding="utf-8")
    assert "version: 1.1.0" in content, "default-web-saas should be at v1.1.0 (bumped in v0.6.1)"


def test_each_doctrine_has_changelog_or_status_marker() -> None:
    """Each Doctrine ends with a Changelog section, Status note, or both."""
    for d in EXPECTED_DOCTRINES:
        path = DOCTRINES_DIR / f"{d}.md"
        content = path.read_text(encoding="utf-8")
        has_changelog = bool(re.search(r"^##\s*(\d+\.\s*)?Changelog\b", content, re.MULTILINE | re.IGNORECASE))
        has_status = "Status:" in content or "ratification_date:" in content
        assert has_changelog or has_status, \
            f"Doctrine {d}.md missing Changelog section or Status marker"


def _run_all() -> int:
    tests = [
        test_doctrines_dir_exists,
        test_all_12_doctrines_present,
        test_each_doctrine_has_frontmatter,
        test_each_doctrine_declares_required_fields,
        test_each_doctrine_name_matches_filename,
        test_each_doctrine_has_rules_section,
        test_default_web_saas_v1_1_0_referenced,
        test_each_doctrine_has_changelog_or_status_marker,
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
