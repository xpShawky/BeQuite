# Research depth strategy

**Status:** active
**Adopted:** 2026-05-11 (alpha.2 expanded /bq-research from 1 dim → 11 dims)
**Reference:** TOOL_NEUTRALITY.md, `.claude/commands/bq-research.md`, `.claude/skills/bequite-researcher/SKILL.md`

**Related strategies (alpha.16 cross-refs):**
- `AUTO_MODE_STRATEGY.md` §11 "Operating modes" — **Deep Mode** activates the full 11-dim research; **Fast Mode** scopes to 3 dims (stack / security / scale)
- `MEMORY_FIRST_BEHAVIOR.md` — research outputs live in `.bequite/research/` and are reused by Token Saver / Delegate flows
- `MULTI_MODEL_PLANNING_STRATEGY.md` + `bequite-delegate-planner` skill — Delegate Mode's Phase 1 starts with deep research (often the strong-model output becomes the cached evidence the cheap model reads later)
- `WORKFLOW_GATES.md` § "Feature-addition workflow (alpha.14)" — step 2 is "Run targeted research"; this doc defines the depth ladder

---

## The principle

Tool choice comes AFTER project understanding, not before.

Before any major tool / library / architecture pick, BeQuite must research across 11 dimensions. Stack is one of them. The other 10 are equally important.

Sources must be live (WebFetch / WebSearch / context7) — not memory. Memory is a guess; sources are evidence.

---

## The 11 research dimensions

| # | Dimension | What to investigate |
|---|---|---|
| 1 | **Stack** | Runtimes, frameworks, libraries — freshness, license, CVEs, bundle size |
| 2 | **Product** | What it is, who it's for, what it replaces |
| 3 | **Competitors** | 3-5 direct competitors; pricing; trajectory; gaps |
| 4 | **Failures** | Prior attempts that failed; postmortems; abandoned repos |
| 5 | **Success** | 3-5 reference implementations; patterns to copy |
| 6 | **User journey** | End-to-end flow from user POV; friction points |
| 7 | **UX/UI** | Design references; AI-slop anti-patterns; accessibility |
| 8 | **Security** | OWASP Top 10 (Web + LLM); supply-chain; recent CVEs |
| 9 | **Scalability** | Scale-tier table; load patterns; sharding triggers |
| 10 | **Deployment** | Hosting candidates; cold-start; pricing 2026; regions |
| 11 | **Differentiation** | Why pick this over named competitors; concrete answer |

## Emphasis per mode

Not every dimension carries equal weight per mode:

| Dimension | New | Existing | Feature | Fix | Research-only | Release |
|---|---|---|---|---|---|---|
| Stack | heavy | medium | medium | light | medium | light |
| Product | heavy | light | medium | n/a | heavy | n/a |
| Competitors | heavy | medium | medium | n/a | heavy | n/a |
| Failures | medium | heavy | light | heavy | heavy | medium |
| Success | heavy | medium | medium | medium | heavy | light |
| User journey | heavy | light | medium | n/a | heavy | n/a |
| UX/UI | heavy (UI) | medium | medium (UI) | n/a | heavy | n/a |
| Security | heavy | heavy | medium | heavy | medium | heavy |
| Scalability | heavy | medium | light | n/a | medium | heavy |
| Deployment | heavy | medium | light | n/a | medium | heavy |
| Differentiation | heavy | light | medium | n/a | heavy | n/a |

`heavy` = at least 3-5 sources, comparison tables.
`medium` = 1-3 sources, summary.
`light` = quick verification.
`n/a` = skip.

## Output discipline

Every claim in `RESEARCH_REPORT.md` has:
- URL (with date accessed)
- Quote or paraphrase supporting it
- Verdict (fresh / warn / stale / unverified)

No claim without a source. No source without a date.

## Anti-hallucination defenses

- **PhantomRaven** (Aug-Oct 2025 npm campaign): never recommend a package without WebFetch-verifying it exists in the registry
- **Shai-Hulud** (broader 2025): pin to exact versions for security-critical deps; commit lockfile; Dependabot/Renovate with auto-merge OFF
- **Memory-based pricing claims**: never quote pricing from memory; always WebFetch within 24h

## Tool neutrality intersection

Per TOOL_NEUTRALITY.md, every named tool in `RESEARCH_REPORT.md` is a **candidate**, not a default. The research enables decisions; it doesn't make them.

After research, `/bq-plan` produces decision sections (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan) before adopting anything.

## Failure modes

| Failure | Recovery |
|---|---|
| WebFetch rate-limited | Mark items unverified; document as gap |
| Library doesn't exist in registry | Flag as hallucination risk; do NOT recommend |
| Pricing page paywalled | Mark unverified; note alternatives |
| Two reputable sources disagree | Cite both; prefer more recent |
| Research finds blocker (e.g. deprecated central dep) | Pause; surface to user before scope-lock |

## See also

- `.claude/commands/bq-research.md` — the command spec
- `.claude/skills/bequite-researcher/SKILL.md` — deep procedures per dimension
- TOOL_NEUTRALITY.md — the candidate-not-default rule
- MULTI_MODEL_PLANNING_STRATEGY.md — when research leaves a tie
