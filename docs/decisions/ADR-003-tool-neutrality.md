# ADR-003 — Tool neutrality

**Status:** Accepted
**Date:** 2026-05-11
**Supersedes:** none
**Superseded by:** none
**Related:** ADR-001 (lightweight skill pack), ADR-002 (mandatory workflow gates)

---

## Context

BeQuite v3.0.0-alpha.1 and -alpha.2 introduced 34 commands and 14 skills. Many of those files name specific tools (Drizzle, Vercel, shadcn/ui, Playwright, Better-Auth, Next.js 15, Inter font, etc.).

Two problems followed:

1. **The named tools risked becoming defaults.** A reader following the materials literally would adopt every named tool even when it doesn't fit their project.
2. **Stack choice was leading project understanding.** Skills sometimes recommended a tool before researching the project's actual domain, scale, and constraints.

The user's correction (2026-05-11) was explicit: every named tool is an example, not a mandatory choice. BeQuite must research the project first, choose tools second, and justify every pick.

## Decision

Adopt a **global tool neutrality principle** across BeQuite. Specifically:

1. Create `.bequite/principles/TOOL_NEUTRALITY.md` as the canonical source of truth.
2. Add a "Tool neutrality (global rule)" section to every tool-touching skill (11) and command (8).
3. Add the global principle to `CLAUDE.md` so it's surfaced on every session start.
4. Standardize the phrasing: replace "Use X." with "X is one candidate. Research and compare against other options. Use it only if it fits this project."
5. Codify the **10 decision questions** that every major tool pick must answer.
6. Codify the **decision section format** (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).
7. Codify the **do-not-auto-install defaults** (no dependencies, scraping tools, frontend libs, Docker, testing frameworks, deployment tools, monitoring, auth libs added by default).
8. Codify the **research-depth rule**: 11 dimensions of research, not just stack.
9. Project-level tool ADRs go to `.bequite/decisions/ADR-XXX-<tool>-choice.md` (per project, not framework-level).
10. BeQuite's own framework ADRs continue at `docs/decisions/` (this file lives there).

## Consequences

### Positive

- **No more hardcoded defaults.** Every named tool is explicitly framed as a candidate.
- **Project understanding leads tool choice.** /bq-research's 11 dimensions force domain + UX + scalability + security research before any tool is picked.
- **Decisions are documented.** Every major pick produces a decision section or ADR.
- **Consistent phrasing across all 34 commands + 14 skills + CLAUDE.md + every doctrine.**
- **Aligns with Article VI honest reporting** — recommendations are research-backed, not memory-backed.

### Negative

- **Heavier authoring overhead.** Every skill + command file gains a tool-neutrality block. Adds ~30 lines per file. Mitigation: standardized block; one canonical source in TOOL_NEUTRALITY.md.
- **Higher friction for prototypes.** Even quick spikes need a decision section. Mitigation: small projects can use a short inline section, not a full ADR.
- **Existing language in skills still uses "default X" phrasing in some places.** Mitigation: tool-neutrality block at the end of each file overrides; future passes will rewrite inline language. Tracked as follow-up.

### Neutral

- The 11-dimension research model already existed in `/bq-research`; this ADR formalizes its primacy over stack-first thinking.
- The 10 decision questions are new framing of long-existing senior-engineer practice; they don't add new work, they make existing thinking explicit.

## Alternatives considered

### A — Status quo (named tools as soft defaults)

Pros: simpler authoring. Cons: encourages cargo-culting; violates the user's explicit correction. **Rejected.**

### B — Remove every tool name from BeQuite materials

Pros: zero hardcoded defaults. Cons: loses concrete learning value; readers benefit from seeing examples to evaluate against. **Rejected — too sterile.**

### C — Mark every tool name with a "candidate" tag inline

Pros: every mention is contextually framed. Cons: massive rewrite; high error rate; noisy. **Deferred to future passes.**

### D — Standardized tool-neutrality block + canonical principle file + CLAUDE.md global

This ADR's choice. Each file appends a uniform block referencing TOOL_NEUTRALITY.md. Concrete examples remain in body text for learning value; the block at the end makes the framing explicit.

**Chosen: D.**

## Migration

For v3.0.0-alpha.1 / -alpha.2 projects:
- Re-run installer to copy `.bequite/principles/TOOL_NEUTRALITY.md` template
- Existing skills + commands gain the tool-neutrality block on next BeQuite update
- No existing project memory needs migration; the rule applies forward

For new projects:
- Installer creates `.bequite/principles/TOOL_NEUTRALITY.md` on `/bq-init`
- Every project-level tool ADR goes to `.bequite/decisions/`

## References

- User direction (2026-05-11): "Any tool, library, repo, framework, design system, workflow, or method mentioned in BeQuite is an example, not a fixed mandatory choice."
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth
- `BEQUITE_BOOTSTRAP_BRIEF.md` Article VII (Hallucination defense) — related; tool neutrality extends this with the "research before adopting" rule
- ADR-001 — lightweight skill pack direction
- ADR-002 — mandatory workflow gates
