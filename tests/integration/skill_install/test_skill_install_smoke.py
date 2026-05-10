"""Integration smoke test for cli/bequite/skill_install.py (BeQuite v0.12.0)."""

from __future__ import annotations

import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.skill_install import HOSTS, _content_for_host, detect_hosts, install_host  # noqa: E402


def test_hosts_table_complete() -> None:
    expected = {"claude-code", "cursor", "codex", "cline", "kilo", "continue", "aider", "windsurf", "gemini"}
    assert set(HOSTS.keys()) == expected


def test_detect_no_hosts() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        assert detect_hosts(repo) == []


def test_detect_claude_code() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        (repo / "CLAUDE.md").write_text("# claude", encoding="utf-8")
        hosts = detect_hosts(repo)
        assert "claude-code" in hosts


def test_detect_cursor() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        (repo / ".cursor").mkdir()
        hosts = detect_hosts(repo)
        assert "cursor" in hosts


def test_detect_codex_and_cline() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        (repo / ".codex").mkdir()
        (repo / ".clinerules").mkdir()
        hosts = detect_hosts(repo)
        assert "codex" in hosts
        assert "cline" in hosts


def test_install_host_writes_file() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        path, status = install_host(repo, "cursor")
        assert path.exists()
        assert status == "installed"
        text = path.read_text(encoding="utf-8")
        assert "BeQuite" in text


def test_install_host_idempotent() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        install_host(repo, "claude-code")
        path, status = install_host(repo, "claude-code")
        assert status == "already-present"


def test_install_unknown_host_raises() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        try:
            install_host(repo, "not-a-real-host")
        except ValueError:
            return
        raise AssertionError("expected ValueError")


def test_content_for_host_includes_banned_words() -> None:
    for host in HOSTS:
        text = _content_for_host(host)
        assert "should" in text  # in the banned-words list
        assert "BeQuite" in text


def _run_all() -> int:
    tests = [
        test_hosts_table_complete,
        test_detect_no_hosts,
        test_detect_claude_code,
        test_detect_cursor,
        test_detect_codex_and_cline,
        test_install_host_writes_file,
        test_install_host_idempotent,
        test_install_unknown_host_raises,
        test_content_for_host_includes_banned_words,
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
