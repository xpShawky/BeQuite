---
name: bequite.design-audit
description: Detect AI-looking frontend output. Loads frontend-designer (Impeccable-loaded). Walks the 15 anti-patterns per master §7.9. Active only when a frontend Doctrine is loaded. Returns findings + per-finding remediation suggestions.
phase: P5 | P6
persona: frontend-designer
loaded_skill: skill/skills-bundled/impeccable/
---

# /bequite.design-audit

When invoked (or `bequite design audit`):

## Step 1 — Confirm context

Active only when `state/project.yaml::active_doctrines` includes `default-web-saas` or a frontend-doctrine fork. For pure CLI / library / ML / automation projects without a UI, refuse — there's no UI to audit.

## Step 2 — Load frontend-designer

Switch to `skill/agents/frontend-designer.md`. Load the bundled Impeccable skill at `skill/skills-bundled/impeccable/` (pinned snapshot, attributed to Paul Bakaus, MIT).

## Step 3 — Walk the 15 anti-patterns (master §7.9)

For each rendered page / component:

1. Generic SaaS template look — page layout indistinguishable from a Lovable / v0 default.
2. Bad spacing — inconsistent / non-tokenised values; cramped or excessive whitespace.
3. Weak typography — unrecorded font choice; mismatched line heights; orphan headings.
4. Purple-blue gradient overuse — the AI-slop tell. Doctrine `default-web-saas` Rule 1.
5. Card nesting — `.card` inside `.card`. Doctrine Rule 4. Block.
6. Fake dashboard charts — placeholder data; lorem-ipsum metrics; no real insight.
7. Weak empty states — "Nothing to show" without next-action CTA. Doctrine `default-web-saas` Rule 7.
8. Bad mobile behavior — viewport 360 broken; touch targets <44px.
9. Poor contrast — gray-on-color (Doctrine Rule 5); axe-core fail.
10. Missing focus states — keyboard navigation invisible.
11. Repeated icon tiles — every action has the same generic icon.
12. Poor UX copy — vague labels ("Submit" instead of "Send invoice"); error messages that don't explain.
13. Wrong hierarchy — H1/H2/H3 misused; visual weight doesn't match importance.
14. Over-rounded components — 24px+ radius on everything; the "Bolt-app" look.
15. Unclear actions — primary CTA indistinguishable from secondary; destructive button looks like cancel.

## Step 4 — Cross-reference Impeccable

Run Impeccable's `/audit` + `/critique` commands (loaded skill). Their findings layered on top of the 15-anti-pattern walk.

## Step 5 — Produce report

`evidence/<phase>/design-audit-<YYYY-MM-DD>.md`:

- Per anti-pattern: found / not-found / N/A.
- For each "found": file:line, severity (block / warn / nit), suggested remediation.
- Screenshots (before) at `evidence/<phase>/screenshots/before/`.
- Recommended Impeccable command(s) to apply (`craft`, `polish`, `bolder`, `quieter`, etc.).

## Step 6 — Optionally apply remediations

If user accepts: invoke `/bequite.impeccable-craft` per finding. Save after-screenshots; re-run audit; confirm clean.

## Stop condition

- Report at `evidence/<phase>/design-audit-<YYYY-MM-DD>.md` exists + populated.
- Skeptic kill-shot answered ("which anti-pattern is the most-likely-to-rot if a future contributor doesn't share the same design sense?").
- For each `block`-severity finding: filed as a new task or accepted in `docs/risks.md`.

## Anti-patterns (in this command's own behaviour)

- Auditing without screenshots (the only evidence of "what looked wrong").
- Auditing without running the app (paper audits miss real issues).
- Auto-fixing without user confirmation (this command surfaces; `/bequite.impeccable-craft` fixes).

## Related

- `/bequite.impeccable-craft` — apply Impeccable commands to remediate.
- `/bequite.validate` — full Phase 6 validation including a11y.
