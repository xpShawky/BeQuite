# `harden` — add edge-case states

> The state-completeness command. Materializes the four canonical states every interactive component must have: **loading**, **error**, **empty**, **disabled**. Use after a component "works on the happy path."

## Why this command exists

The single biggest gap in AI-generated UIs is missing states. Components render correctly with full data; they fall apart when data is loading, the API is down, the list is empty, or the user lacks permission. `harden` fills those gaps with deliberate, recovery-oriented states.

## When to use

- Right after a component's happy path is implemented and visually approved.
- During `design-audit` review, when "weak empty states" or "missing focus states" findings appear.
- When the spec calls for offline / degraded states (PWA, mobile-first, MENA low-bandwidth contexts).

## When NOT to use

- For pure presentational components (a static logo doesn't need an error state).
- For components whose states are already complete (run `audit` first to confirm).
- As a substitute for backend error handling — `harden` adds the *UI* representation; the backend must surface the right errors.

## Inputs

- Target component file(s).
- Backend contract — what errors can this surface raise? (Read the relevant API spec or schema.)
- User context — is the user authenticated? What permissions do they have? What viewport?

## The four canonical states

### Loading

- Use **skeletons matched to the future content's shape**, not generic spinners. A skeleton for a list-of-3-cards looks like 3 card-shaped placeholder rectangles; not a spinner over the whole region.
- For sub-second loads, no loading state at all (premature spinner = perceived slowness).
- For long loads (>3s), add a status message ("Loading large dataset…") or a progress indicator if you have real progress data.
- Skeletons match `tokens.css::--color-skeleton-bg` (use a subtle gray that respects the active theme).

### Error

- Show **what failed** in user-language ("Couldn't load your bookings"), not technical jargon ("HTTP 500").
- Show **what to do** — primary action is "Try again" or "Refresh" or "Go back."
- Show **why it might have failed** — for sophisticated audiences, a one-line technical hint ("Your session expired"). For consumer audiences, omit.
- Provide a way to **see logs / contact support** for debugging — usually a small subtle link.
- Color: red token (`--color-danger`), but text on the red surface must hit WCAG AA.

### Empty

- The hardest state to do well.
- One-line **explanation of why it's empty** ("You haven't created any bookings yet").
- One **clear next-action CTA** ("Create your first booking" — primary button).
- Optional: link to docs / examples / sample data.
- Optional: illustration (only if brand has illustration assets — no stock illustrations).
- Empty ≠ "Nothing to show." Empty *teaches* the user what this section is for.

### Disabled

- A disabled element must communicate **why** it's disabled.
- Hover tooltip on the disabled control: "Your subscription doesn't include this. Upgrade to Pro." or "Wait for the upload to finish."
- Disabled visual: lower opacity (0.5–0.6) + cursor not-allowed.
- Disabled state must still be **focusable** (so keyboard + screen reader users can discover it; the tooltip is read aloud).

## Steps

1. **Read the component.** Identify which states it currently handles.
2. **Read the backend contract.** What errors / loading-times / empty conditions can occur?
3. **Plan the four states.** Sketch what each looks like (text, icon, CTA, color).
4. **Save before-screenshot** of the happy-path version.
5. **Implement loading state.** Match skeleton shape to content shape.
6. **Implement error state.** Real failure-mode wording; recovery action.
7. **Implement empty state.** Real explanation; real next-action CTA.
8. **Implement disabled state.** Real reason in tooltip.
9. **Save after-screenshots** — one per state.
10. **Verify each state via Playwright** — mock the backend to force each state; capture screenshot.
11. **Run `bequite design audit`** — confirm "weak empty states" / "missing focus states" findings cleared.
12. **Suggest commit.** `feat(<task>): harden <component> with loading + error + empty + disabled states`.

## Outputs

- Updated component file with all four states.
- 4–5 screenshots (happy + 4 states).
- Storybook / preview file (if `live` was previously run on this component).
- Audit delta showing finding reduction.

## Skeptic kill-shot

- *"What happens when the API returns 401 on a previously-authenticated session? Does the user get a clear path back?"*
- *"What happens at viewport 360 in each state?"*
- *"Is the empty state's CTA the right one for a brand-new user — or just for a user who deleted their last item?"*

## Stop conditions

- All four states implemented.
- All four states screenshotted.
- All four states verified via Playwright (mock-driven).
- axe-core passes for each state (focus visible, contrast hit, ARIA correct).
- Skeptic kill-shots answered.

## Anti-patterns this command must NOT introduce

- Generic spinner for loading (use skeletons).
- "Something went wrong" error wording (be specific).
- "Nothing to show" empty wording (explain + CTA).
- Disabled-without-tooltip (the user has no recourse).
- Missing focus state on disabled (keyboard users can't discover it).

## Cross-reference

- `references/anti-patterns.md` — items 7, 9, 10, 12, 15.
- `references/principles.md` — principle 6.
- `polish.md` — light edits to existing states.
- `clarify.md` — when the wording is the issue.
- `live.md` — generate a preview that exercises all states.
