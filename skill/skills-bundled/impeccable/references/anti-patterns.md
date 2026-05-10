# Impeccable anti-pattern catalog (the AI-slop tells)

> 15 patterns that mark a UI as AI-default. The `design-audit` slash command walks all 15 against every rendered page; findings drive `impeccable-craft` remediations.

## 1. Generic SaaS template look

**Tell:** Page layout is indistinguishable from a Lovable / v0 / Bolt default. Sidebar-left, top-bar with logo + user-menu, three-card hero, generic "Welcome back" heading.

**Fix:** Throw away the template-shaped structure. Start from the user's primary task. Lay out the *task*, not a generic dashboard.

## 2. Bad spacing

**Tell:** Inconsistent / non-tokenised values (13px, 27px, 41px). Cramped or excessive whitespace.

**Fix:** Apply the 4/8/12/16/24/32/48/64/96/128 scale. Use the `polish` command to walk a screen and normalise.

## 3. Weak typography

**Tell:** Unrecorded font choice. Mismatched line-heights. Orphan headings (a single H3 with nothing under it). Headings that are larger than they need to be.

**Fix:** Apply `typeset`. Record the font-choice reason in `tokens.css`. Use a 4-step type scale at most (display / heading / body / caption), not 7 sizes.

## 4. Purple-blue gradient overuse

**Tell:** The classic AI-default gradient. `from-purple-500 to-blue-500` on every CTA + hero + every card.

**Fix:** Pick a single brand color. Use it sparingly (the primary CTA, occasionally an accent badge). If the brand calls for a gradient, use *one* per screen, in *one* place.

## 5. Card nesting (`.card` inside `.card`)

**Tell:** A bordered/shadowed card containing another bordered/shadowed card. Sometimes three deep.

**Fix:** One card per visual group. Use sections, dividers, or layout grids for sub-grouping. Doctrine Rule 4 blocks this.

## 6. Fake dashboard charts

**Tell:** Placeholder data ("$1,234.56", "42 widgets"). Lorem-ipsum metrics. No real insight; just chart-shaped decoration.

**Fix:** Either show real data (even if seeded) or show a real empty state with a real CTA. Never ship lorem-ipsum charts.

## 7. Weak empty states

**Tell:** "Nothing to show." "No data." That's it.

**Fix:** Apply `harden`. Empty states explain *why* it's empty, offer *what's next*, and (when relevant) link to docs / examples.

## 8. Bad mobile behaviour

**Tell:** Viewport 360 broken. Touch targets < 44px. Horizontal scrolls.

**Fix:** Apply `adapt`. Test on viewport 360 always. Touch targets stay ≥ 44 × 44 px.

## 9. Poor contrast

**Tell:** Gray text on coloured background. Light-gray text on white background. Buttons whose label fades into their fill.

**Fix:** axe-core gate (WCAG AA: ≥ 4.5:1 body, ≥ 3:1 large). Doctrine Rule 5 blocks this. Apply `polish` or `colorize`.

## 10. Missing focus states

**Tell:** Tab through the page; nothing visible changes.

**Fix:** Every interactive element has a visible focus ring (offset, 2px, brand-color or system-default). Apply `harden` to add focus states.

## 11. Repeated icon tiles

**Tell:** Every action card has the same generic icon (or worse, the same emoji). Or: the icons exist but they're all stacked-rectangles or three-bars.

**Fix:** Either pick an icon set with semantic variety (Lucide, Phosphor, Tabler) and use distinct icons, or *don't use icons* for the action tiles — use a clear text label and structure.

## 12. Poor UX copy

**Tell:** Vague labels ("Submit"). Error messages that don't explain ("Something went wrong"). Headings that don't tell you what page you're on.

**Fix:** Apply `clarify`. CTAs are verb-noun ("Send invoice", not "Submit"). Errors say *what* failed and *what to do*. Headings name the page in user-language.

## 13. Wrong hierarchy

**Tell:** H1 used three times on a page. H2 same size as body. Visual weight doesn't match importance.

**Fix:** One H1 per page. Three levels max in admin views. Apply `bolder` / `quieter` to balance.

## 14. Over-rounded components

**Tell:** Every card, button, input has 24px+ border-radius. The "Bolt-app look."

**Fix:** Apply `shape`. Pick one rounding scale (e.g. 4 / 8 / 12 px) and stick with it. Heroic rounding is a design choice, not a default.

## 15. Unclear actions

**Tell:** Primary CTA indistinguishable from secondary. Destructive button (delete, cancel-subscription) looks the same as a benign cancel.

**Fix:** Apply `harden`. Primary = filled brand-color; secondary = outline; destructive = filled red (or red border + red text). Confirmation modal for destructive.

## How `design-audit` walks these

The `skill/commands/design-audit.md` slash command runs through this list for every rendered page. Each finding includes: file:line, severity (block / warn / nit), suggested remediation command (which Impeccable command to apply).

For projects loaded with `default-web-saas` Doctrine, **all `block`-severity findings must clear before P5 → P6 transition.** Warns + nits are tracked in `docs/risks.md` for follow-up.
