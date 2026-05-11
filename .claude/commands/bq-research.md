---
description: Gather verified evidence before deciding. Checks library freshness, deprecation, CVEs, alternatives. Writes .bequite/audits/RESEARCH_REPORT.md.
---

# /bq-research — verified evidence

You are doing **research before deciding**. The output is `.bequite/audits/RESEARCH_REPORT.md` — a cited list of options with freshness verdicts so the plan that follows is grounded in real 2026 data, not stale training-corpus assumptions.

## Step 1 — Read context

- `.bequite/state/OPEN_QUESTIONS.md` — the unresolved questions
- `.bequite/state/DECISIONS.md` — what's been decided
- `.bequite/audits/DISCOVERY_REPORT.md` — current stack

## Step 2 — Identify research targets

From OPEN_QUESTIONS + the user's clarify answers, pull out:

- Libraries / frameworks under consideration
- Stack choices (DB, auth, ORM, etc.)
- Vendor / service comparisons
- License / pricing checks
- Any "X vs Y" choice the plan will commit to

## Step 3 — Probe each target

Use WebFetch / WebSearch (and context7 if available) to verify:

For each library/framework:
- **npm / PyPI / crates.io**: last release date (< 6 months = fresh; 6-12 = warn; > 12 = stale)
- **GitHub**: stars, last commit, open issues vs closed
- **CVE / OSV scanner**: known vulnerabilities
- **License**: compatible with the project's intended license?
- **Maintainer**: active person / org / abandonware?
- **Bundle size** (for JS libs): bundlephobia or packagephobia
- **Type definitions**: TypeScript types shipped?

For each vendor/service:
- Pricing page — current rates (don't trust your training data)
- Free tier limits
- Geographic restrictions / data residency
- Status page — recent incidents
- T&C / acceptable-use policy gotchas

## Step 4 — Compare

For each "X vs Y" question, build a comparison table:

| Criterion | Option A | Option B |
|---|---|---|
| Stars | 12k | 8k |
| Last release | 2026-04 | 2024-11 ❌ |
| License | MIT | AGPL ⚠ (commercial closed-source blocker) |
| TS types | yes | no |
| Verdict | RECOMMENDED | reject — license incompatible |

## Step 5 — Write the report

`.bequite/audits/RESEARCH_REPORT.md`:

```markdown
# Research Report

**Generated:** <ISO 8601 UTC>
**Questions researched:** <count>

## 1. <Question 1 — short title>

**Context:** <one paragraph from OPEN_QUESTIONS.md>

**Candidates investigated:**

| Candidate | Last release | Stars | License | Risks | Verdict |
|---|---|---|---|---|---|
| ... |

**Recommendation:** <one candidate + reasoning>

**Sources:**
- <URL 1>
- <URL 2>

## 2. <Question 2>

...

## Summary

Recommendations for the plan:

1. <Question 1>: use <X>
2. <Question 2>: use <Y>
3. ...

Rejected / flagged for later:

- <Option Z>: <reason>
```

## Step 6 — Update state

- Append research conclusions to `.bequite/state/DECISIONS.md`
- Mark resolved items in `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/logs/AGENT_LOG.md` entry

## Step 7 — Report back

```
✓ Research complete

Questions researched: <count>
Recommendations:      <count>
Rejected options:     <count>

Full report: .bequite/audits/RESEARCH_REPORT.md

Next: /bq-scope (if findings expand the problem) or /bq-plan
```

## Rules

- **Cite every claim.** Each fact comes with a URL.
- **Recency matters.** If you can't verify a release date is < 12 months, mark it "stale — verify before adopting".
- **License-flag the AGPL / GPL surprises.** Many libraries that look great are GPL-encumbered (Firecrawl, Shannon, Wazuh, etc.). Note these.
- **No "should work" claims.** Either you verified it or you didn't — mark unverified items explicitly.
- **PhantomRaven defense:** treat any library NOT yet verified via npm/PyPI as potentially hallucinated. The agent must never `npm install <pkg>` until research confirms `<pkg>` exists.

## Memory files this command reads

- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/audits/DISCOVERY_REPORT.md`

## Memory files this command writes

- `.bequite/audits/RESEARCH_REPORT.md` (new)
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/OPEN_QUESTIONS.md` (resolved items marked)
- `.bequite/state/LAST_RUN.md` (updated)
- `.bequite/logs/AGENT_LOG.md` (appended)

## Usual next command

- `/bq-scope` if research surfaced new sub-questions
- `/bq-plan` otherwise
