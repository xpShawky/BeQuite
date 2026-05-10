"""Integration smoke test for multi-model planning (BeQuite v0.10.5)."""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.multi_model import (  # noqa: E402
    compare_plans,
    parse_plan_sections,
    render_comparison_md,
    render_final_plan,
    render_judge_prompt,
    render_plan_prompt,
    scaffold_run,
    slug,
)
from bequite.providers.manual_paste import ManualPasteProvider, estimate_tokens  # noqa: E402


SAMPLE_PLAN_CLAUDE = """# Plan
## Vision
Build a bookings SaaS.

## Scope
Customer + admin flows.

## Stack
Next.js + Hono + Supabase + Better-Auth.

## Auth
Better-Auth.

## Security
Zod validation; RLS deny-by-default.
"""

SAMPLE_PLAN_GPT = """# Plan
## Vision
A bookings system.

## Scope
Customer + admin.

## Stack
Next.js + tRPC + Supabase + Clerk.

## Auth
Clerk.

## Risks
Vendor lock-in on Clerk.
"""


def test_render_plan_prompt_contains_role_and_brief() -> None:
    p = render_plan_prompt(
        model_name="claude-opus-4-7", role="lead-architect",
        brief="Build a bookings SaaS",
        doctrines=["default-web-saas"], constitution_version="1.2.0",
    )
    assert "lead-architect" in p
    assert "bookings SaaS" in p
    assert "default-web-saas" in p


def test_parse_plan_sections_extracts_known_sections() -> None:
    sections = parse_plan_sections(SAMPLE_PLAN_CLAUDE)
    assert "Vision" in sections
    assert "Scope" in sections
    assert "Stack" in sections
    assert "Auth" in sections
    assert "Better-Auth" in sections["Auth"]


def test_compare_plans_marks_disagreement_on_auth() -> None:
    cmp = compare_plans({"claude": SAMPLE_PLAN_CLAUDE, "gpt": SAMPLE_PLAN_GPT})
    auth_row = next(r for r in cmp["comparison"] if r["topic"] == "Auth")
    assert auth_row["agreement"] == "all-mention"
    assert "Better-Auth" in auth_row["per_model"]["claude"]
    assert "Clerk" in auth_row["per_model"]["gpt"]


def test_compare_plans_flags_omitted_section() -> None:
    cmp = compare_plans({"claude": SAMPLE_PLAN_CLAUDE, "gpt": SAMPLE_PLAN_GPT})
    # Neither plan has a "Phases" section.
    phases_row = next(r for r in cmp["comparison"] if r["topic"] == "Phases")
    assert phases_row["agreement"] == "all-omitted"


def test_render_comparison_md_writes_file() -> None:
    with tempfile.TemporaryDirectory() as td:
        run_dir = pathlib.Path(td)
        cmp = compare_plans({"claude": SAMPLE_PLAN_CLAUDE, "gpt": SAMPLE_PLAN_GPT})
        out = render_comparison_md(cmp, run_dir)
        assert out.exists()
        text = out.read_text(encoding="utf-8")
        assert "# Comparison" in text
        assert "claude" in text and "gpt" in text


def test_render_final_plan_with_user_decisions() -> None:
    cmp = compare_plans({"claude": SAMPLE_PLAN_CLAUDE, "gpt": SAMPLE_PLAN_GPT})
    final = render_final_plan(cmp, user_decisions={"Auth": "Better-Auth (chosen)"})
    assert "## Auth" in final
    assert "Better-Auth (chosen)" in final


def test_scaffold_run_creates_tree() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        run_dir = scaffold_run(
            repo_root=repo,
            brief="Build a bookings SaaS",
            models=[("claude-opus-4-7", "lead-architect"), ("gpt-5", "product-strategist")],
            doctrines=["default-web-saas"],
        )
        assert run_dir.exists()
        assert (run_dir / "input_brief.md").exists()
        assert (run_dir / "prompts" / "plan_claude-opus-4-7.md").exists()
        assert (run_dir / "prompts" / "plan_gpt-5.md").exists()
        state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
        assert state["mode"] == "parallel"
        assert len(state["models"]) == 2


def test_manual_paste_provider_protocol() -> None:
    p = ManualPasteProvider()
    assert p.is_available() is True
    assert p.supports_model("anything") is True
    assert p.estimate_cost_usd("anything", 1000, 500) == 0.0


def test_manual_paste_provider_async_returns_awaiting() -> None:
    with tempfile.TemporaryDirectory() as td:
        run_dir = pathlib.Path(td)
        (run_dir / "prompts").mkdir()
        p = ManualPasteProvider(run_dir=run_dir, async_mode=True)
        c = p.complete(model="claude-opus-4-7", prompt="test prompt")
        assert c.finish_reason == "awaiting_user"
        assert (run_dir / "prompts" / "plan_claude-opus-4-7.md").exists()


def test_render_judge_prompt() -> None:
    p = render_judge_prompt(
        judge_model="claude-opus-4-7", run_id="RUN-2026-05-10T12-00",
        peer_plans={"claude": SAMPLE_PLAN_CLAUDE, "gpt": SAMPLE_PLAN_GPT},
        comparison_table="| Topic | ... |\n",
    )
    assert "Final Judge" in p
    assert "claude" in p and "gpt" in p
    assert "self-attestation" in p


def test_estimate_tokens_is_proportional() -> None:
    assert estimate_tokens("a" * 4) == 1
    assert estimate_tokens("a" * 400) == 100


def test_slug_normalizes() -> None:
    assert slug("Claude-Opus-4.7") == "claude-opus-4-7"
    assert slug("GPT 5 Mini") == "gpt-5-mini"


def _run_all() -> int:
    tests = [
        test_render_plan_prompt_contains_role_and_brief,
        test_parse_plan_sections_extracts_known_sections,
        test_compare_plans_marks_disagreement_on_auth,
        test_compare_plans_flags_omitted_section,
        test_render_comparison_md_writes_file,
        test_render_final_plan_with_user_decisions,
        test_scaffold_run_creates_tree,
        test_manual_paste_provider_protocol,
        test_manual_paste_provider_async_returns_awaiting,
        test_render_judge_prompt,
        test_estimate_tokens_is_proportional,
        test_slug_normalizes,
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
