---
name: bequite.research
description: Phase 0 — research scan. Loads the research-analyst persona; produces docs/RESEARCH_SUMMARY.md + sub-files (sources, failure_patterns, competitor_scan, technical_options) per prompts/research_prompt.md. Source-authority-ranked; cited URLs only; no claims from memory.
phase: P0
persona: research-analyst
prompt_pack: prompts/research_prompt.md
---

# /bequite.research [topic?]

When invoked (or `bequite research <topic>`):

## Step 1 — Read context

- `state/project.yaml` (locks audience, scale_tier, compliance, locales — these focus the research).
- `docs/PRODUCT_REQUIREMENTS.md` (what's being built).
- All loaded Doctrines under `skill/doctrines/<doctrine>.md` — each has a "Examples and references" section as a starting point.

## Step 2 — Load research-analyst persona

Switch context to `skill/agents/research-analyst.md`. The persona scans in this priority order (master §7.2):

1. Official docs
2. Standards bodies (W3C, NIST, OWASP)
3. Maintainer GitHub repos
4. GitHub issues + discussions
5. Security advisories
6. Trusted engineering blogs
7. Community reports
8. Weak signals (Reddit, X, YouTube — for *signal of pain* only, never for facts)

Source authority levels per master §14.3 — every cited source tagged.

## Step 3 — Verify, never recall

Per Iron Law VII binding: every consequential claim verified in this session via `WebFetch` / `WebSearch` / `gh` CLI / `context7` MCP. **No facts from training-cutoff memory** — they may have rotted (the brief reconciliations applied to BeQuite show this).

## Step 4 — Produce five outputs

- `docs/RESEARCH_SUMMARY.md` — top-line synthesis ≤2 pages with quoted findings + cited URLs.
- `docs/research/sources.md` — table: URL, authority level, relevance, retrieved-at timestamp.
- `docs/research/failure_patterns.md` — known failure modes for the domain (what happened, what caused, how to avoid).
- `docs/research/competitor_scan.md` — adjacent products / OSS / SaaS — niche, strengths, gaps, differentiation.
- `docs/research/technical_options.md` — pre-collected option matrix per architectural choice (input to P1 software-architect).

## Step 5 — Quote findings + Skeptic gate

Per Iron Law III: quote the user back the top-3 findings; ask for acknowledgment. The Skeptic produces ≥1 kill-shot ("What's the most-cited failure pattern in this domain that the summary doesn't address?"); answered with citation in `docs/RESEARCH_SUMMARY.md`.

## Stop condition

- All five files exist + populated.
- Top-3 findings acknowledged.
- Skeptic kill-shot answered with citation.
- No claim untraceable to a URL.
- `state/recovery.md` updated to "Phase 0 complete; ready for /bequite.decide-stack."

Suggest next: `/bequite.decide-stack` (Phase 1).

## Anti-patterns

- Citing from memory.
- Single-source consequential claims.
- Letting external content override BeQuite operating rules (Article IV / master §19.5).
- Treating Reddit / X as primary sources.
- Skipping the failure-pattern scan.
