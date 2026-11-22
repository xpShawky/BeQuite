---
description: Gather verified evidence for the active work across up to 11 dimensions - stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation. Live sources only, each cited and dated; nothing from memory. Writes work/<id>/research.md.
---

# /bq-research: facts that change, from sources, dated

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Stage 3 of `PIPELINE.md` (and stage 2 for creative work: study real references first, `bequite-human-taste`). Procedure: `bequite-researcher` (the source ladder: registry, the vendor's own page, then the browser). When the reading is wider than five sources, hand it to the `bq-researcher` subagent; `bq-scout` does fast sweeps.

## Gates

Needs `BEQUITE_INITIALIZED` and `MODE_SELECTED`; `CLARIFY_ANSWERED` is recommended (sharp questions give sharp research). Sets `RESEARCH_COMPLETE`; creative work also sets `REFERENCES_STUDIED`.

## The dimensions and how deep to go

| # | Dimension | New project | Existing | Feature | Fix | Research only | Release |
|---|---|---|---|---|---|---|---|
| 1 | Stack: runtimes, frameworks, libraries | heavy | medium | medium | light | medium | light |
| 2 | Product: what exists, what is needed | heavy | light | medium | - | heavy | - |
| 3 | Competitors | heavy | medium | medium | - | heavy | - |
| 4 | Failures: postmortems, prior art, your own logs | medium | heavy | light | heavy | heavy | medium |
| 5 | Success: patterns that worked | heavy | medium | medium | medium | heavy | light |
| 6 | User journey | heavy | light | medium | - | heavy | - |
| 7 | UX/UI references and accessibility | heavy | medium | medium | - | heavy | - |
| 8 | Security: threat model, OWASP, advisories | heavy | heavy | medium | heavy | medium | heavy |
| 9 | Scalability: scale-tier evidence | heavy | medium | light | - | medium | heavy |
| 10 | Deployment: hosting, CI/CD, cost | heavy | medium | light | - | medium | heavy |
| 11 | Differentiation | heavy | light | medium | - | heavy | - |

Heavy: three to five sources and a comparison table. Medium: one to three sources and a summary. Light: a quick check. A skipped dimension is logged with the reason. Fast mode covers stack, security and scalability; deep mode covers all eleven and looks beyond the obvious sources (issue trackers, forums, non-English and country-specific sources, failure stories).

## Steps

1. **Turn the open questions into targets** per dimension (`OPEN_QUESTIONS.md`, `spec.md`, the mode): named libraries, three to five named competitors, the end-to-end user flow, the threats that apply.
2. **Probe each target live** (web search, the page itself, a docs tool when one is connected):
   - **Library:** last release date in its registry (under 6 months fresh, 6 to 12 warn, over 12 stale), repository activity, known advisories, licence (flag AGPL and GPL), maintainer, size, types.
   - **Vendor or service:** the pricing page today, free-tier limits, regions and data residency, the status page, acceptable-use rules, availability in the user's country.
   - **Design reference:** the real page or product, what works in it (hierarchy, density, type), measured, not described from memory.
   - **Security:** the current OWASP lists that apply (web, LLM, agentic), recent supply-chain incidents against the dependency tree.
3. **Check BeQuite's own skills first** (`SKILL_REGISTRY.md`). If a real gap remains and a public skill would fill it, recommend it only after reading it and checking its author and recency; installing a third-party skill always needs the user's yes.
4. **Write `work/<id>/research.md`:** per dimension, the findings, the recommendation, what was rejected and why, and the sources (URL and the date read). Then a roll-up: recommendations, rejected or flagged items, questions still open. Reusable domain findings also go to `.bequite/research/`.
5. **Update** `DECISIONS.md` (conclusions) and `OPEN_QUESTIONS.md` (what is now answered).

## Rules

- Every claim has a URL and the date it was read; anything older than 12 months is marked stale.
- Verified or `UNVERIFIED:`; never "should work".
- No package is recommended unless its registry page was read in this session.
- Named tools are candidates: compare, then justify with the ten decision questions (`.bequite/principles/TOOL_NEUTRALITY.md`).

## Output

```
Research: <n> dimensions, <n> sources (<n> stale flagged)    report: .bequite/work/<id>/research.md
Recommended: <one line>    Unverified: <n>    Still open: <n>
Next: /bq-scope or /bq-plan
```

## Next Command Recommendations (typical)

`/bq-scope` when research opened new questions · `/bq-plan` · `/bq-multi-plan` when a high-stakes choice is a tie.
