---
description: Gather verified evidence across 11 dimensions — stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation. WebFetch live data — no memory-based claims. Writes RESEARCH_REPORT.md.
---

# /bq-research — 11-dimension verified evidence

## Purpose

Replace your training-corpus assumptions with **verified, dated, cited 2026 evidence** before you commit to a plan. The output is `.bequite/audits/RESEARCH_REPORT.md` — a structured report across 11 dimensions, each with sources, freshness verdicts, and "use this / reject this" recommendations.

This is the single most important Phase 1 command. A bad plan is usually a plan built on stale research.

## When to use it

- After `/bq-clarify` (you know the questions; now find answers)
- Before `/bq-scope` or `/bq-plan`
- Whenever a stack pick or vendor pick will lock you in for months

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅` (mode-specific dimensions are emphasized differently)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`
- `CLARIFY_DONE` (recommended — research is sharper when questions are crisp)

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/audits/DISCOVERY_REPORT.md` (if exists)
- `.bequite/plans/SCOPE.md` (if exists)

## Files to write

- `.bequite/audits/RESEARCH_REPORT.md` (new — 11 dimensions)
- `.bequite/state/DECISIONS.md` (research conclusions appended)
- `.bequite/state/OPEN_QUESTIONS.md` (resolved items marked)
- `.bequite/state/WORKFLOW_GATES.md` (`RESEARCH_DONE ✅`)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## The 11 dimensions

Every research session covers all 11 unless explicitly skipped (and skips are logged). Some dimensions are mode-specific in emphasis:

| # | Dimension | New | Existing | Feature | Fix | Research-only | Release |
|---|---|---|---|---|---|---|---|
| 1 | **Stack** — runtimes, frameworks, libraries | heavy | medium | medium | light | medium | light |
| 2 | **Product** — what exists, what's needed | heavy | light | medium | n/a | heavy | n/a |
| 3 | **Competitors** — who else does this | heavy | medium | medium | n/a | heavy | n/a |
| 4 | **Failures** — what failed (prior art, your own logs, similar products) | medium | heavy | light | heavy | heavy | medium |
| 5 | **Success** — what worked (patterns, repos, case studies) | heavy | medium | medium | medium | heavy | light |
| 6 | **User journey** — what the end-user actually does | heavy | light | medium | n/a | heavy | n/a |
| 7 | **UX/UI** — design references + accessibility | heavy (if UI) | medium | medium (if UI) | n/a | heavy | n/a |
| 8 | **Security** — threat model, OWASP, CVEs | heavy | heavy | medium | heavy | medium | heavy |
| 9 | **Scalability** — load patterns, scale-tier evidence | heavy | medium | light | n/a | medium | heavy |
| 10 | **Deployment** — hosting options, CI/CD, costs | heavy | medium | light | n/a | medium | heavy |
| 11 | **Differentiation** — why pick this over alternatives | heavy | light | medium | n/a | heavy | n/a |

`heavy` = at least 3-5 sources, comparison tables. `medium` = 1-3 sources, summary. `light` = quick verification. `n/a` = skip.

## Steps

### 1. Identify research targets per dimension

From OPEN_QUESTIONS + SCOPE + mode, derive concrete sub-questions per dimension:

- **Stack**: every library/framework under consideration → freshness probe
- **Product**: what does this product DO that's not already done? Two paragraphs from user, then verify against market
- **Competitors**: 3-5 named products that solve the same problem
- **Failures**: prior projects that tried this + failed. Search for postmortems
- **Success**: 3-5 projects that succeeded. What did they do right?
- **User journey**: end-to-end flow the user walks through (sign up → first task → daily use)
- **UX/UI**: 3-5 design references for the same pattern (e.g. "good admin dashboard 2026")
- **Security**: OWASP Top 10 (LLM + Web App) coverage map; recent CVEs in chosen libs
- **Scalability**: scale-tier evidence — what does 50 / 5K / 50K / 500K users look like?
- **Deployment**: Vercel / Fly / Render / Railway / self-host comparison for this stack
- **Differentiation**: "why us, not them" — concrete answer or flag as unclear

### 2. Probe each target with live data

**Use WebFetch + WebSearch (and context7 if available) — not memory.**

For each library / framework:
- npm / PyPI / crates.io: last release date (< 6 months = fresh; 6-12 = warn; > 12 = stale)
- GitHub: stars, last commit, open issues vs closed
- CVE / OSV scanner: known vulnerabilities
- License: compatible with project's intended license?
- Maintainer: active person / org / abandonware?
- Bundle size (JS): bundlephobia / packagephobia
- Type definitions: TypeScript types shipped?

For each vendor / service:
- Pricing page — current 2026 rates (memory will be wrong)
- Free tier limits
- Geographic restrictions / data residency
- Status page — recent incidents
- Acceptable-use policy gotchas

For each design reference:
- Screenshot URLs (Pinterest / Dribbble / Mobbin / real site)
- What works: hierarchy, density, typography
- What to avoid: AI-slop patterns

For each security item:
- OWASP Top 10 (2021 stable + 2025 draft) coverage
- OWASP Top 10 for LLM Applications 2025 (if AI involved)
- Recent supply-chain attacks (PhantomRaven, Shai-Hulud, ...) — does your dep tree expose you?

### 3. Write the report (structured)

`.bequite/audits/RESEARCH_REPORT.md`:

```markdown
# Research Report — 11 Dimensions

**Generated:** <ISO 8601 UTC>
**Mode:** <mode>
**Questions researched:** <count>

---

## Dimension 1 — Stack

### Candidates investigated

| Candidate | Last release | Stars | License | CVEs | Verdict |
|---|---|---|---|---|---|
| ... | | | | | |

### Recommendation

<which library/framework + why, with concrete reasoning>

### Sources

- <URL with date accessed>

### Rejected / flagged

- <library>: <reason — e.g. AGPL surprise, unmaintained, deprecated>

---

## Dimension 2 — Product

### What exists today

(market scan, 2-3 paragraphs)

### What's needed

(gap the project fills)

### Sources

- <URLs>

---

## Dimension 3 — Competitors

| Product | URL | Pricing | Key feature | Notable gap |
|---|---|---|---|---|

### Sources

- <URLs>

---

## Dimension 4 — Failures (what failed before)

(prior attempts, postmortems, abandoned repos)

### Key lessons

- <one-liner each>

### Sources

- <URLs>

---

## Dimension 5 — Success (what worked)

(case studies, repos, articles)

### Patterns to copy

- <one-liner each>

### Sources

- <URLs>

---

## Dimension 6 — User journey

```
<step-by-step flow from user POV — sign up → first action → daily use>
```

### Friction points to avoid

- <list>

### Sources

- <user research / competitor walkthroughs>

---

## Dimension 7 — UX/UI

### Design references

| Reference | URL | What works | What to avoid |
|---|---|---|---|

### Accessibility baseline

- WCAG 2.1 AA target
- axe-core gate in CI
- Keyboard nav, screen-reader, color contrast specifics

---

## Dimension 8 — Security

### Threat model

(2-3 paragraphs)

### OWASP Top 10 coverage

| OWASP item | How we address |
|---|---|

### Recent CVEs in chosen libs

| Lib | CVE | Severity | Fix version |
|---|---|---|---|

### Supply-chain considerations

(PhantomRaven, dep tree audit, lockfile discipline)

---

## Dimension 9 — Scalability

### Scale tier evidence

| Tier | Users | Architecture | Cost/mo (est) |
|---|---|---|---|
| Solo | 1-50 | Single VPS | $5-20 |
| Small | 50-5K | Managed DB + CDN | $20-200 |
| Growth | 5K-50K | Read replicas + cache | $200-2K |
| Scale | 50K-500K | Sharded + queue | $2K-20K |

### Recommended tier for v1

<tier + reasoning>

---

## Dimension 10 — Deployment

| Host | Pricing 2026 | Cold start | Region | Verdict |
|---|---|---|---|---|

### Recommended

<host + reasoning>

### CI/CD

(GitHub Actions / GitLab / etc.)

---

## Dimension 11 — Differentiation

### Why this product wins

(2-3 concrete reasons — speed, price, focus, UX, regional fit)

### What we're NOT trying to be

(explicit non-goals)

---

## Cross-dimension summary

### Recommendations rolled up

1. Stack: use <X>
2. Hosting: use <Y>
3. Auth: use <Z>
4. ...

### Rejected / flagged

- <items>

### Open questions still unresolved

- <list — these feed back to OPEN_QUESTIONS.md>
```

### 4. Update state

- Append research conclusions to `DECISIONS.md`
- Mark resolved items in `OPEN_QUESTIONS.md`
- Mark `RESEARCH_DONE ✅` in `WORKFLOW_GATES.md`
- `LAST_RUN.md` updated
- `AGENT_LOG.md` appended

### 5. Report back

```
✓ Research complete — 11 dimensions covered

Mode:                 <mode>
Sources cited:        <count>
Recommendations:      <count>
Rejected options:     <count>
Open questions left:  <count>

Full report: .bequite/audits/RESEARCH_REPORT.md

Next: /bq-scope (lock IN/OUT) or /bq-plan (write the plan)
```

## Output format

Print a short summary in chat (see above). Full evidence goes in the report file.

## Quality gate

- All applicable dimensions covered (per mode emphasis table)
- Every claim has a cited URL with date accessed
- No "should work" / "is probably fine" / "I think" — verified or marked unverified
- Freshness verdicts attached to every library / vendor
- AGPL / GPL surprises flagged explicitly
- PhantomRaven defense applied (no package recommended without registry verification)

## Failure behavior

- WebFetch fails / rate-limited → degrade gracefully; mark items as "unverified — needs manual check"
- No suitable candidate found in a dimension → write "no clear winner; flagging for `/bq-multi-plan` second opinion"
- Critical finding (deprecated central dep) → write the finding to the report and **pause** before scope-lock

## Rules

- **Cite every claim.** Each fact comes with a URL + date accessed.
- **Recency matters.** Mark anything > 12 months old as "stale — verify before adopting".
- **License-flag the AGPL / GPL surprises.** Many libraries that look great are GPL-encumbered (Firecrawl, Shannon, Wazuh, etc.).
- **No "should work" claims.** Either verified or marked unverified.
- **PhantomRaven defense:** never recommend a library NOT verified via npm/PyPI/crates this session.

## Skills activated

- `bequite-project-architect` (for stack architecture)
- `bequite-security-reviewer` (for dimension 8)
- `bequite-ux-ui-designer` (for dimension 7, when UI involved)
- `bequite-scraping-automation` (only if scraping is in scope)

## Usual next command

- `/bq-scope` if research surfaced new sub-questions
- `/bq-plan` otherwise
- `/bq-multi-plan` if research left a tie on a high-stakes decision

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow this command surfaces during research is an EXAMPLE, not a mandatory default.**

Research produces **candidates**, not commitments. The plan that follows decides which candidate fits.

**Do not write in the RESEARCH_REPORT:** "Use X."
**Write:** "X is one candidate. Compare against alternatives. Adopt only if it fits this project's type, scale, constraints, and existing stack."

The 10 decision questions every research summary must enable:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Every recommendation in RESEARCH_REPORT.md must enable a decision section: Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan.

Research depth covers 11 dimensions — not just stack. Project domain, user needs, competitors, failure modes, success patterns, UX, security, scalability, deployment, differentiation. **Tool choice comes after project understanding, never before.**

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
