---
description: Write a one-page product / feature spec in Spec Kit-compatible format. Lightweight bridge between BeQuite's research + plan + scope and the broader Spec Kit ecosystem. Writes specs/<feature>/spec.md.
---

# /bq-spec — one-page Spec Kit-compatible spec

## Purpose

Write a focused one-page specification for a product or feature in **Spec Kit-compatible format** (`specs/<feature>/spec.md`). Bridges BeQuite to the Spec Kit ecosystem so projects can mix both tools without format drift.

Lightweight: not a full IMPLEMENTATION_PLAN (use `/bq-plan` for that). Not a feature mini-spec (use `/bq-feature` for that). This is the **technology-agnostic, user-and-outcome-focused spec** that Spec Kit's `/specify` workflow produces.

## When to use it

- You want a portable spec that works in both BeQuite and Spec Kit
- You're documenting a feature for stakeholders (PM, design, ops) before engineering
- You're sharing a feature definition with another team or repo
- You want a tighter, narrative-style spec than IMPLEMENTATION_PLAN.md

## When NOT to use it

- Full project planning with stack + file plan + tasks — use `/bq-plan`
- Add Feature mini-cycle — use `/bq-feature` (12-type router)
- Quick fix — use `/bq-fix`
- Just exploring (no commitment yet) — use `/bq-clarify` + `/bq-research`

## Syntax

```
/bq-spec "<feature or product idea in one sentence>"
```

Examples:
- `/bq-spec "Add CSV export to the bookings page"`
- `/bq-spec "Patient intake form for the clinic SaaS"`
- `/bq-spec "Lead capture landing page with newsletter signup"`
- `/bq-spec "Multi-tenant org switching"`

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED` (recommended; not strictly required)

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/plans/SCOPE.md` (if exists)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists)
- `.bequite/audits/RESEARCH_REPORT.md` (if exists; for persona / market context)

## Files to write

- `specs/<feature-slug>/spec.md` — the spec (Spec Kit-compatible path)
- `.bequite/plans/spec-<feature-slug>.md` — link / copy in BeQuite memory
- `.bequite/state/DECISIONS.md` — append "Spec written for <feature>"
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. Get the spec subject

If user invoked `/bq-spec` alone, ask:
> "What feature or product idea? (one sentence)"

If user passed an argument like `/bq-spec "..."` → use that.

Derive the slug: `kebab-case` of the idea (e.g. "patient intake form" → `patient-intake-form`).

### 2. Detect Spec Kit presence (optional)

Check if the project already uses Spec Kit:
- `specs/` directory at root
- `.specify/` or similar Spec Kit config

If yes → follow Spec Kit's conventions (path, naming).
If no → still write to `specs/<slug>/spec.md` (this becomes the seed for adopting Spec Kit later if desired).

### 3. Draft the spec

Write `specs/<slug>/spec.md`:

```markdown
# Feature: <Name>

**Status:** Draft
**Author:** <user>
**Created:** <ISO 8601 UTC>
**BeQuite mode:** <current mode>
**BeQuite phase:** <current phase>

---

## What

(2-3 sentences. The feature in plain English. No jargon. No stack mention.)

## Why

(2-4 sentences. The user value + business value. Why does this matter? What changes for the user after this ships?)

## Who

**Primary user(s):** <persona — concrete role, not "everyone">
**Secondary users:** <if any>
**Stakeholders:** <PM / design / ops / etc.>

## What changes for the user

(Step-by-step from the user's POV. Before/after. The journey, not the implementation.)

Example:
- **Before:** User exports bookings by selecting each row and copying into Excel.
- **After:** User clicks "Export CSV" → downloads a complete bookings.csv with date-range filter applied.

## Acceptance criteria

(Concrete, testable. Each item is a specific observable user-visible behavior.)

- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>
- [ ] No banned weasel words in error messages
- [ ] Works on mobile (360px) and desktop (1440px)
- [ ] Accessible (WCAG 2.1 AA where applicable)

## Out of scope

(Explicit non-goals. What this spec is NOT.)

- ...
- ...

## Constraints

- **Privacy / compliance:** <PII? GDPR? PDPL? HIPAA? PCI?>
- **Performance:** <p95 target if relevant>
- **Existing system:** <what must NOT break>
- **Budget:** <cost ceiling if relevant>

## Open questions

(Items requiring decisions before implementation. Routed to `OPEN_QUESTIONS.md`.)

- [ ] <question 1>
- [ ] <question 2>

## Success metric

(ONE number that tells you the feature shipped successfully. Not "users love it" — a specific measurable.)

Example: "10% of active users export at least once in the first month."

## How (high-level)

(Optional. 2-3 paragraphs of approach. NOT a full design — that's `/bq-plan`. Just enough so a reviewer can sanity-check the spec.)

## Related

- BeQuite scope: `.bequite/plans/SCOPE.md`
- BeQuite plan: `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists)
- Related ADRs: <list>
```

### 4. Save the BeQuite memory copy

Write `.bequite/plans/spec-<slug>.md` as a copy / symlink to `specs/<slug>/spec.md`.

### 5. Update state

- Append "Spec written: <feature>" to `DECISIONS.md`
- Append unresolved questions from §"Open questions" to `OPEN_QUESTIONS.md`
- Update `LAST_RUN.md`
- Append `AGENT_LOG.md`

### 6. Report back

```
✓ Spec written — <feature name>

Path:         specs/<slug>/spec.md
BeQuite copy: .bequite/plans/spec-<slug>.md
Status:       Draft
Open questions: <count>

Next:
  /bq-plan        — turn this spec into a full implementation plan
  /bq-feature     — Add Feature mini-cycle (if the spec is small enough)
  /bq-clarify     — resolve open questions before planning
  /bq-multi-plan  — second-opinion on the spec via another model
```

## Output format

Narrate the steps. Print the final report.

## Quality gate

- `specs/<slug>/spec.md` exists with all required sections
- "What", "Why", "Who", "Acceptance criteria" are concrete (no weasel words)
- "Out of scope" is explicit (at least 1 item)
- Open questions are real (not placeholder "TBD")
- Path matches Spec Kit convention so Spec Kit's `/speckit.plan` could pick it up
- User confirmed the spec is accurate

## Failure behavior

- User can't articulate "Why" → escalate to `/bq-clarify` or `bequite-product-strategist` skill (JTBD framework)
- "Acceptance criteria" are vague — return to user with one targeted question per vague item
- Spec contradicts locked `SCOPE.md` — surface the conflict; do not advance until resolved

## Memory updates

- `specs/<slug>/spec.md` (new)
- `.bequite/plans/spec-<slug>.md` (new — BeQuite-side copy)
- `DECISIONS.md` — append spec record
- `OPEN_QUESTIONS.md` — append unresolved items

## Log updates

- `AGENT_LOG.md` — entry "Spec written: <feature>"

## Tool neutrality (global rule)

⚠ **Spec Kit is named here as an interop target — it is NOT a mandatory dependency.** BeQuite works fine without Spec Kit installed. `/bq-spec` produces a spec that's **compatible** with Spec Kit if you choose to adopt it.

Alternatives (also compatible candidates):
- ProductBoard / Linear / Notion spec docs (different but equally valid)
- Google Docs / Markdown wiki specs

Per the 10 decision questions, pick the spec tool that fits your team's workflow. `/bq-spec` produces the markdown; where you put it (Spec Kit, repo `specs/`, wiki) is your decision.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Usual next command

- `/bq-plan` — turn the spec into a full implementation plan
- `/bq-feature "<name>"` — Add Feature mini-cycle (if scope is small)
- `/bq-clarify` — resolve open questions surfaced by the spec
- `/bq-multi-plan` — get a second opinion from another model before locking
