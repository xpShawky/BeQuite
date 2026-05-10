# `polish` — small refinements (contrast, spacing, alignment)

> The light-touch command. Use when a section is *almost right* and needs surface-level adjustments — tightening contrast, normalizing spacing, fixing small alignment issues. Lower-risk than `craft`.

## When to use

- After `craft` has done the heavy lift, but the section still feels slightly off.
- When `audit` flagged a few `warn`-class items but no `block`-class.
- For edges and corners (date pickers, popovers, hover states) that need a final pass.
- When applying a brand designer's specific feedback ("can the spacing tighten by half?").

## When NOT to use

- For a comprehensive section pass (use `craft`).
- For introducing new states (use `harden`).
- For typography overhauls (use `typeset`).
- For structural changes (use `layout` or `extract`).

## Inputs

- Target — file(s) or specific selectors within a file.
- Optional: specific feedback ("the contrast on the badge is too low", "the button padding feels cramped").

## Steps

1. **Read the target.** Map the small things that look slightly off.
2. **Save before-screenshot** at viewport 360 + 1440.
3. **Walk a checklist:**
   - **Spacing** — any `mt-[27px]` or `gap-3.5` style arbitrary values? Move to scale.
   - **Contrast** — any text/background pair that's borderline? Bump to clearly-passing.
   - **Alignment** — items that should align but don't (off by 1–2px). Fix.
   - **Border radius** — within the chosen scale (4 / 8 / 12 / 16)?
   - **Shadows** — using `--shadow-*` tokens, not arbitrary `shadow-[0_4px_8px_...]`?
   - **Hover states** — visible enough? Subtle but discoverable?
   - **Focus rings** — visible at 100% zoom + at viewport 360?
4. **Apply edits.** Each edit should be defensible in one sentence.
5. **Save after-screenshot.**
6. **Run `bequite design audit`** lightweight — confirm no regressions.
7. **Suggest commit.** `style(<task>): polish <component>`.

## Outputs

- Edited target file(s) — typically a small diff (5–30 lines).
- Before/after screenshots.
- Brief summary in `evidence/<phase>/<task>/polish-notes.md` — what was tweaked + why.

## Skeptic kill-shot

- *"Did any of these tweaks cross from 'polish' into 'craft'? If yes, revert and re-do as `craft`."*
- *"Did any tweak touch state-bearing logic (like onClick handlers, conditionals)? If yes, this isn't a polish — revert and split into a polish PR + a refactor PR."*

## Stop conditions

- Edits applied.
- Before/after screenshots exist.
- Audit shows no regression (and ideally a small improvement).
- Skeptic kill-shot answered.

## Anti-patterns this command must NOT introduce

- Touching component logic (this is a *visual* polish; if logic needs work, it's a different command or task).
- Adding new tokens (token additions are deliberate decisions, not polish).
- Cross-component touches (a `polish` pass scopes to one component or one section; cross-cutting changes belong in a `craft` or refactor task).

## Cross-reference

- `craft.md` — when polish isn't enough.
- `audit.md` — what to polish against.
- `principles.md` — principles 1, 4, 9 are the most-frequently invoked here.
