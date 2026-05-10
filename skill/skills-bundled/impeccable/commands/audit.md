# `audit` — comprehensive design scan

> The diagnostic command. Walks the 15 anti-patterns + the 10 principles against a target page or component. Emits findings; does not fix. Pair with `craft` / `polish` / `harden` for remediation.

## When to use

- Before a P5 → P6 transition (the `design-audit` slash command invokes this).
- After a `craft` pass to confirm nothing regressed.
- On a periodic basis ("design hygiene week") as a debt-tracking pass.

## When NOT to use

- For sub-component-level critique (use `critique`).
- For documentation generation (use `document`).
- When you intend to fix immediately without a checkpoint (use `craft` directly).

## Inputs

- Target — single page, component, or "the active feature."
- Active Doctrine — must be a frontend Doctrine.
- Optional: previous audit delta to diff against.

## Steps

1. **Take a screenshot** of the rendered target at viewport 360 + 1440 + (if mena-bilingual loaded) `ar-*`.
2. **Walk the 15 anti-patterns** from `references/anti-patterns.md`:
   - Generic SaaS template look
   - Bad spacing
   - Weak typography
   - Purple-blue gradient overuse
   - Card nesting
   - Fake dashboard charts
   - Weak empty states
   - Bad mobile behavior
   - Poor contrast
   - Missing focus states
   - Repeated icon tiles
   - Poor UX copy
   - Wrong hierarchy
   - Over-rounded components
   - Unclear actions
3. **Walk the 10 principles** from `references/principles.md`. Mark each as observed / partially observed / violated.
4. **Run axe-core** if available (Playwright + axe-playwright). Capture violations.
5. **Run tokens-only check** via `bequite audit` rule pack. Capture violations.
6. **Compose findings report** at `evidence/<phase>/<task>/design-audit-<YYYY-MM-DD>.md`:
   ```markdown
   # Design audit — <target> — <date>
   
   ## Summary
   - Anti-patterns found: <N> (block: <X>, warn: <Y>, nit: <Z>)
   - Principles violated: <N>
   - axe-core violations: <N>
   - Tokens-only violations: <N>
   
   ## Findings
   - **<file:line>** — <anti-pattern> [block] — <description>. Recommended: `bequite design <command>`.
   ...
   
   ## Recommended remediation order
   1. ...
   2. ...
   
   ## Skeptic kill-shot
   "<one question that hits the most-likely-to-rot finding>"
   ```
7. **Cross-link** to the screenshots taken in step 1.
8. **Update `state/recovery.md`** with audit completion + finding count.

## Outputs

- Findings report Markdown.
- Screenshots dir with viewport variants.
- Audit summary line in `evidence/<phase>/<task>/summary.md`.
- Suggested remediation queue (which `bequite design <command>` to run, in what order).

## Severity levels

- **block** — must fix before P5 → P6 transition. Doctrine `default-web-saas` Rules 1, 4, 5, 6, 7, 10, 11, 13 are block-class.
- **warn** — should fix, but can be tracked in `docs/risks.md` for follow-up.
- **nit** — pure design-craft taste; track if you wish, ignore if you must.

## Skeptic kill-shot per audit

Always frame at least one question in the report: *"Which finding is most likely to be ignored by a future contributor who doesn't share this design sense?"* The answer informs what gets `harden`-ed into `tokens.css` or pushed into a CI rule.

## Stop conditions

- Findings report file exists + has content per the schema.
- Screenshots saved at all required viewports.
- All `block`-severity findings have a recommended remediation command.
- Skeptic kill-shot included.

## Anti-patterns in this command's own behavior

- Auditing without screenshots (the report has nothing to point at).
- Auditing without running the app (paper audits miss real issues like contrast on actual rendered pages).
- Auto-fixing as you audit (this command surfaces; remediation commands fix).
- Skipping principles when listing only anti-patterns (the principles tell *why*; the anti-patterns are the *what*).

## Cross-reference

- `references/anti-patterns.md` — the 15 to walk.
- `references/principles.md` — the 10 to check.
- `craft.md`, `polish.md`, `harden.md`, `colorize.md`, `typeset.md` — common remediations.
- `skill/commands/design-audit.md` — the BeQuite slash command that wraps this.
