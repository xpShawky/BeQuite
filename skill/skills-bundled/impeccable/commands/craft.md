# `craft` — apply Impeccable's design language to a section

> The marquee command. Section-scoped pass that addresses hierarchy, spacing, typography, and color in one go. Use when starting a new feature's UI from a working-but-rough state.

## When to use

- A new feature's UI is functionally complete but visually generic ("AI-default look").
- A section was hand-coded without consulting tokens / scale / hierarchy.
- The user explicitly asks "make this look good."

## When NOT to use

- For tiny tweaks (use `polish`).
- For a single dimension (use `colorize` / `typeset` / `layout` / `shape`).
- When the underlying component is wrong (refactor first; then `craft`).
- When tokens.css doesn't exist yet (author tokens first; then `craft`).

## Inputs

- Target file(s) — the JSX/TSX/Svelte/Vue component file(s).
- Doctrine context — `default-web-saas` (or fork) must be loaded.
- Screenshots — viewport 360 + 1440, plus `ar-*` if mena-bilingual loaded.

## Steps

1. **Read the target.** Map the component tree; identify hierarchy levels, color usage, typography, spacing, motion.
2. **Read tokens.css.** Inventory: which tokens exist? which are used? which are missing?
3. **Identify the primary action.** There must be exactly one. If two compete, ask the user which is primary.
4. **Apply hierarchy.** Primary gets the heaviest weight (size + font-weight + color contrast). Secondaries recede.
5. **Normalize spacing.** Move arbitrary values to scale-aligned values (4/8/12/16/24/32/48/64/96/128).
6. **Apply tokens-only.** Remove hardcoded colors / fonts / shadows. If a token is missing, propose a token, but don't auto-add (token additions are decisions, not refactors).
7. **Recheck contrast.** Run axe-core mentally; visualize. If any pair < WCAG AA, fix.
8. **Recheck mobile.** Mentally render at viewport 360. If anything overflows, the spacing or breakpoint is wrong; fix.
9. **Save before-screenshots.** Capture at viewport 360 + 1440 (+ `ar-*` if mena-bilingual).
10. **Apply edits.** One file or one section per craft pass.
11. **Save after-screenshots.**
12. **Run `bequite design audit`** (lightweight) on the touched section. Confirm anti-patterns reduced.
13. **Run `posttooluse-audit.sh`.** Tokens-only + axe-core checks. If red, fix or revert.
14. **Suggest commit.** Conventional Commit: `style(<task>): craft <component-name>`.

## Outputs

- Edited target file(s).
- Before/after screenshots saved.
- Optional: proposed token additions in `evidence/<phase>/<task>/proposed-tokens.md`.
- Audit delta in `evidence/<phase>/<task>/audit-delta.md` (anti-patterns before vs after).
- Suggested commit message.

## Skeptic kill-shot

Before commit: *"Looking at this section, what would a senior frontend designer at Linear / Vercel / Stripe say is wrong?"*

If there's a real answer, fix it before commit. If there isn't, ship.

## Stop conditions

- Before/after screenshots exist.
- Audit delta shows reduction (or no regression).
- Tokens-only check green.
- axe-core green.
- Skeptic kill-shot answered.

## Anti-patterns this command must NOT introduce

- Card nesting (Doctrine Rule 4).
- Gray-on-color (Doctrine Rule 5).
- Bounce / elastic motion (Doctrine Rule 6).
- Hardcoded values (Doctrine Rule 1).
- Unrecorded font choice (Doctrine Rule 2).

## Cross-reference

- `principles.md` — the philosophy.
- `anti-patterns.md` — what `craft` is reducing.
- `aesthetic-targets.md` — what good looks like.
- `polish.md` — when `craft` is too heavy a hand.
- `audit.md` — the post-craft check.
