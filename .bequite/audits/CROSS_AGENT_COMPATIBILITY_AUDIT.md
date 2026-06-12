# Cross-Agent Compatibility Audit (alpha.22 stabilization)

**Run:** 2026-06-12 · question: how Claude-coupled is BeQuite today, and what was needed to make it usable elsewhere? (Documentation pass only — no adapters built, no live cross-agent trial run; all "works with X" statements are design-level, marked accordingly.)

## Findings

| # | Finding | Evidence | Action |
|---|---|---|---|
| 1 | The only hard Claude couplings are: slash invocation (`.claude/commands/` filename mechanism), skill auto-attach, hooks runtime, automatic CLAUDE.md load | strategy doc §1 table | documented; everything else verified plain-markdown |
| 2 | Command files were already playbook-readable — each contains a self-contained procedure (syntax → steps → writes → routing) with no Claude-only steps inside the procedure bodies | spot-checked bq-fix / bq-course / bq-verify / bq-plan | maintainer rule added (strategy §5): keep it that way |
| 3 | `.bequite/` memory contract has zero Claude dependencies (plain files; state/logs/gates all readable+writable by any file-capable agent) | dir inspection | no change needed |
| 4 | The FRONTIER_REASONING_SUMMARY 10-rule card already solves "make any model follow BeQuite discipline" — it predates this pass and is the natural cross-agent briefing | `.bequite/state/FRONTIER_REASONING_SUMMARY.md` | promoted in the outside-Claude runbook |
| 5 | Skill selection outside Claude Code needs a manual path | SKILL_ROUTER.md domain map is human-readable | runbook step 4 documents manual selection |
| 6 | No cross-agent docs existed before this pass | — | created: CROSS_AGENT_COMPATIBILITY_STRATEGY.md · USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md · AGENT_COMPATIBILITY_MATRIX.md; README gains a compatibility section |
| 7 | Hooks are the one safety layer with no portable equivalent | hooks = Claude Code runtime | documented as a known loss + mitigation (instruct + review more) |

## What was NOT done (deliberately)

No universal app · no CLI wrapper · no provider APIs · no AGENTS.md auto-generation (recorded as roadmap candidates: `bq` prompt-assembly script, AGENTS.md generator argument, Cursor rules-file template — see strategy §4 + matrix rightmost column). **UNVERIFIED:** actual behavior of each third-party agent against this repo — no live cross-agent trial has been run; the matrix carries a verify-before-relying caveat.

## Verdict

BeQuite is ~85% portable by construction (memory, gates, playbooks, IDs, evidence rules); the remaining 15% (invocation sugar, auto-attach, hooks) is now explicitly documented with mitigations. Compatibility is a documentation feature today and an adapter feature later — in line with the lightweight charter.
