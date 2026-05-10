"""bequite.multi_model — Multi-Model Planning module (v0.10.5).

Manual-paste mode is the v0.10.5 MVP. Direct-API mode reuses v0.8.0 router
in v0.11.x+.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import re
import sys
from typing import Optional


def now_run_id() -> str:
    return "RUN-" + _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H-%M")


def slug(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


# ----------------------------------------------------------------------- prompt rendering


PLAN_TEMPLATE = """# Planning brief — {model_name} ({role})

You are operating as the **{role}** for this BeQuite-managed project. Produce a complete, technology-grounded implementation plan based on the brief below.

## Brief

{brief}

## Project context

- Active doctrines: {doctrines}
- Constitution version: {constitution_version}
- Project mode: {mode}
- Audience: {audience}

## What to produce

A complete plan covering:

1. Vision (1-2 sentences)
2. Scope (in)
3. Non-goals (out)
4. Architecture (high-level)
5. Stack (per layer; cite reasoning)
6. Data model
7. Frontend strategy (if applicable)
8. Backend strategy
9. Auth strategy
10. Security strategy
11. Testing strategy
12. Deployment strategy
13. Phases (P0..P7 decomposition)
14. Tasks (atomic, ≤5 min each)
15. Acceptance criteria (per phase)
16. Risks
17. Open questions

## Independence

Do not reference any other model's output. Plan independently. Be opinionated but principled — every recommendation must cite a reason (Doctrine rule, scale-honesty, freshness, recorded preference).

## Output format

Markdown. Headings per the 17 sections above. Be concrete; avoid hedging language ("should", "probably", "I think it works" — Article II violation in BeQuite).
"""


JUDGE_TEMPLATE = """# Final-judge prompt — {judge_model}

You are the **Final Judge** for planning run {run_id}. Synthesize the {n} peer plans below into one coherent final plan.

## Peer plans

{peer_plans_section}

## Comparison table (already auto-generated)

{comparison_table}

## Your job

For each contested topic in the comparison table:
1. Pick a final decision.
2. Explain why each peer recommendation was accepted or rejected.
3. Cite the violated Article / Doctrine rule / freshness fact when rejecting.
4. Mark `requires_user_decision: true` for pure-preference tradeoffs (do NOT pick for the user).
5. Generate a Skeptic kill-shot per accepted decision; record the answer.

## Self-attestation block (mandatory at end)

End the response with the model-judge persona's mandatory self-attestation block per `skill/agents/model-judge.md`.

## Output

Markdown. Sections: Decisions accepted / Decisions rejected / Decisions deferred to user / Self-attestation.
"""


def render_plan_prompt(
    *,
    model_name: str,
    role: str,
    brief: str,
    doctrines: list[str],
    constitution_version: str = "1.2.0",
    mode: str = "safe",
    audience: str = "engineer",
) -> str:
    return PLAN_TEMPLATE.format(
        model_name=model_name,
        role=role,
        brief=brief,
        doctrines=", ".join(doctrines) if doctrines else "(none active)",
        constitution_version=constitution_version,
        mode=mode,
        audience=audience,
    )


def render_judge_prompt(
    *,
    judge_model: str,
    run_id: str,
    peer_plans: dict[str, str],  # model_name -> plan_text
    comparison_table: str,
) -> str:
    peer_plans_section = "\n\n".join(
        f"### {model}\n\n{text}\n" for model, text in peer_plans.items()
    )
    return JUDGE_TEMPLATE.format(
        judge_model=judge_model,
        run_id=run_id,
        n=len(peer_plans),
        peer_plans_section=peer_plans_section,
        comparison_table=comparison_table,
    )


# ----------------------------------------------------------------------- run scaffolding


def scaffold_run(
    *,
    repo_root: pathlib.Path,
    brief: str,
    models: list[tuple[str, str]],  # [(model, role), ...]
    mode: str = "parallel",
    judge: Optional[str] = None,
    doctrines: Optional[list[str]] = None,
    constitution_version: str = "1.2.0",
) -> pathlib.Path:
    """Create docs/planning_runs/RUN-<datetime>/ with input + per-model prompts + state.json."""
    run_id = now_run_id()
    run_dir = repo_root / "docs" / "planning_runs" / run_id
    (run_dir / "prompts").mkdir(parents=True, exist_ok=True)
    (run_dir / "receipts").mkdir(parents=True, exist_ok=True)

    (run_dir / "input_brief.md").write_text(
        f"# Planning brief\n\n{brief}\n\n## Metadata\n\n- run_id: {run_id}\n- mode: {mode}\n- judge: {judge or '(none)'}\n- doctrines: {doctrines or []}\n- constitution: {constitution_version}\n",
        encoding="utf-8",
    )

    for (model, role) in models:
        prompt_text = render_plan_prompt(
            model_name=model, role=role, brief=brief,
            doctrines=doctrines or [], constitution_version=constitution_version,
        )
        (run_dir / "prompts" / f"plan_{slug(model)}.md").write_text(prompt_text, encoding="utf-8")

    state = {
        "version": "1",
        "run_id": run_id,
        "started_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "mode": mode,
        "judge_model": judge,
        "models": [
            {"name": m, "role": r, "provider": "manual-paste", "status": "scaffolded"}
            for (m, r) in models
        ],
        "phase": "scaffolded",
        "doctrines": doctrines or [],
        "constitution_version": constitution_version,
    }
    (run_dir / "state.json").write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    return run_dir


# ----------------------------------------------------------------------- comparison


SECTION_HEADERS = (
    "Vision", "Scope", "Non-goals", "Architecture", "Stack", "Data model",
    "Frontend", "Backend", "Auth", "Security", "Testing", "Deployment",
    "Phases", "Tasks", "Acceptance", "Risks", "Open questions",
)


def parse_plan_sections(text: str) -> dict[str, str]:
    """Coarse parse: returns {section_keyword: content_until_next_section}."""
    out: dict[str, str] = {}
    lines = text.split("\n")
    current_section: Optional[str] = None
    buf: list[str] = []
    for line in lines:
        # Match "## Foo" or "### 5. Stack".
        m = re.match(r"^#{2,3}\s+(?:\d+\.\s+)?(\w[\w\s/-]+)", line)
        if m:
            if current_section is not None:
                out[current_section] = "\n".join(buf).strip()
            heading = m.group(1).strip().lower()
            current_section = next((s for s in SECTION_HEADERS if s.lower() in heading), None)
            buf = []
        else:
            buf.append(line)
    if current_section is not None:
        out[current_section] = "\n".join(buf).strip()
    return out


def compare_plans(plans: dict[str, str]) -> dict:
    """Build a comparison structure from {model_name: plan_text} dict."""
    parsed = {model: parse_plan_sections(text) for model, text in plans.items()}
    comparison: list[dict] = []
    for section in SECTION_HEADERS:
        per_model = {model: parsed.get(model, {}).get(section, "") for model in plans}
        present_count = sum(1 for v in per_model.values() if v.strip())
        if present_count == 0:
            agreement = "all-omitted"
        elif present_count == len(plans):
            agreement = "all-mention"  # detailed agreement requires NLP; coarse for v0.10.5
        else:
            agreement = "partial"
        comparison.append({
            "topic": section,
            "per_model": per_model,
            "agreement": agreement,
            "risk": "medium" if section in ("Security", "Auth", "Risks") else "low",
            "final": "pending",
            "reason": "",
            "requires_user_decision": agreement != "all-omitted",
        })
    return {"plans": list(plans.keys()), "comparison": comparison}


def render_comparison_md(comparison: dict, run_dir: pathlib.Path) -> pathlib.Path:
    """Write comparison.md to run_dir."""
    lines = ["# Comparison\n", f"Models compared: {', '.join(comparison['plans'])}\n", ""]
    lines.append("| Topic | Agreement | Risk | Final | Reason |")
    lines.append("|---|---|---|---|---|")
    for row in comparison["comparison"]:
        final = row["final"]
        if row["agreement"] == "all-omitted":
            final = "GAP — re-prompt or accept omission"
        lines.append(f"| {row['topic']} | {row['agreement']} | {row['risk']} | {final} | {row['reason'] or '(pending)'} |")
    lines.append("")
    lines.append("## Per-section detail\n")
    for row in comparison["comparison"]:
        lines.append(f"### {row['topic']}\n")
        for model, content in row["per_model"].items():
            preview = (content[:300] + "...") if len(content) > 300 else content
            lines.append(f"**{model}:**\n```\n{preview or '(omitted)'}\n```\n")
    out = run_dir / "comparison.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ----------------------------------------------------------------------- merge


def render_final_plan(
    comparison: dict,
    user_decisions: Optional[dict[str, str]] = None,
    judge_report: Optional[str] = None,
) -> str:
    """Build final_plan.md content from comparison + (optional) user decisions + (optional) judge report."""
    lines = ["# Final plan\n"]
    lines.append("> Synthesized from multi-model planning run.\n")
    user_decisions = user_decisions or {}
    for row in comparison["comparison"]:
        topic = row["topic"]
        final = user_decisions.get(topic, row.get("final", "pending"))
        lines.append(f"## {topic}\n")
        if final == "pending" or final == "":
            lines.append("(decision pending; user must edit)\n")
        else:
            lines.append(f"{final}\n")
    if judge_report:
        lines.append("\n## Judge report\n")
        lines.append(judge_report)
    return "\n".join(lines)


# ----------------------------------------------------------------------- CLI


def _scaffold_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    models_pairs = []
    for spec in (args.models or "claude-opus-4-7=lead-architect,gpt-5=product-strategist").split(","):
        if "=" in spec:
            m, r = spec.split("=", 1)
        else:
            m, r = spec, "lead-architect"
        models_pairs.append((m.strip(), r.strip()))
    run_dir = scaffold_run(
        repo_root=repo, brief=args.brief, models=models_pairs,
        mode=args.mode, judge=args.judge,
        doctrines=(args.doctrines or "").split(",") if args.doctrines else None,
    )
    print(f"scaffolded run: {run_dir.relative_to(repo)}")
    print("paste prompts into your chat tools; save responses to:")
    for (m, _) in models_pairs:
        print(f"  → {(run_dir / f'{slug(m)}_plan.md').relative_to(repo)}")
    print(f"then: bequite-multi-model compare --run-dir {run_dir.relative_to(repo)}")
    return 0


def _compare_cmd(args: argparse.Namespace) -> int:
    run_dir = pathlib.Path(args.run_dir).resolve()
    state_file = run_dir / "state.json"
    if not state_file.exists():
        print(f"error: {state_file} not found", file=sys.stderr)
        return 2
    state = json.loads(state_file.read_text(encoding="utf-8"))
    plans: dict[str, str] = {}
    for m in state["models"]:
        path = run_dir / f"{slug(m['name'])}_plan.md"
        if path.exists():
            plans[m["name"]] = path.read_text(encoding="utf-8")
    if not plans:
        print("error: no plan files found in run-dir", file=sys.stderr)
        return 2
    comp = compare_plans(plans)
    out = render_comparison_md(comp, run_dir)
    state["phase"] = "compared"
    state_file.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    print(f"comparison: {out.relative_to(run_dir.parent.parent.parent)}")
    return 0


def _merge_cmd(args: argparse.Namespace) -> int:
    run_dir = pathlib.Path(args.run_dir).resolve()
    state_file = run_dir / "state.json"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    plans: dict[str, str] = {}
    for m in state["models"]:
        path = run_dir / f"{slug(m['name'])}_plan.md"
        if path.exists():
            plans[m["name"]] = path.read_text(encoding="utf-8")
    comparison = compare_plans(plans)
    user_decisions: dict[str, str] = {}
    udec_file = run_dir / "user_decisions.md"
    if udec_file.exists():
        # Coarse parse: lines like "Topic: decision"
        for line in udec_file.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                topic, decision = line.split(":", 1)
                user_decisions[topic.strip()] = decision.strip()
    judge_report = None
    if args.judge:
        report_file = run_dir / "merge_report.md"
        if report_file.exists():
            judge_report = report_file.read_text(encoding="utf-8")
    final = render_final_plan(comparison, user_decisions, judge_report)
    out = run_dir / "final_plan.md"
    out.write_text(final, encoding="utf-8")
    state["phase"] = "merged"
    state_file.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    print(f"final_plan: {out.relative_to(run_dir.parent.parent.parent)}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-multi-model", description="Multi-Model Planning (v0.10.5).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)

    sc = sub.add_parser("scaffold", help="Start a new multi-model planning run.")
    sc.add_argument("--brief", required=True)
    sc.add_argument("--models", default=None, help="comma-separated model=role pairs")
    sc.add_argument("--mode", default="parallel", choices=["parallel", "specialist", "debate", "judge", "red-team"])
    sc.add_argument("--judge", default=None)
    sc.add_argument("--doctrines", default=None)
    sc.set_defaults(fn=_scaffold_cmd)

    cmp = sub.add_parser("compare", help="Build comparison.md from saved plans.")
    cmp.add_argument("--run-dir", required=True)
    cmp.set_defaults(fn=_compare_cmd)

    mg = sub.add_parser("merge", help="Build final_plan.md from comparison + user_decisions + (opt) judge.")
    mg.add_argument("--run-dir", required=True)
    mg.add_argument("--judge", default=None)
    mg.set_defaults(fn=_merge_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
