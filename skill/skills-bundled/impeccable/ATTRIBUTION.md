# Attribution — Impeccable

This bundled skill is a **vendored snapshot** of Paul Bakaus's [Impeccable](https://github.com/pbakaus/impeccable) project, integrated into BeQuite as a sub-skill of the `frontend-designer` persona.

## Original work

- **Author:** Paul Bakaus ([@pbakaus](https://github.com/pbakaus))
- **Project:** Impeccable
- **Repository:** https://github.com/pbakaus/impeccable
- **License:** MIT (see `LICENSE` in upstream repo)
- **Stars at vendor time:** ~26,600 (May 2026)
- **Commands at vendor time:** 23 (`craft, teach, document, extract, shape, critique, audit, polish, bolder, quieter, distill, harden, onboard, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, live`)

## What we vendored

- The 23-command interface (one Markdown stub per command in `commands/`).
- The design-language principles distilled into `references/principles.md`.
- The opinions and the philosophy: how to reason about UI craft, what makes interfaces "AI-default-looking" and how to fix them.

## What we DIDN'T vendor

- Upstream Impeccable's prompt internals (those are Paul's IP and we use them via reference, not duplication).
- Upstream tests, examples, or contributor docs (they live upstream; readers should consult them directly).

## Why we vendored at all (instead of fetching live)

- **Reproducibility** (Iron Law III). A pinned snapshot means a project tagged today renders identically a year from now, even if upstream evolves.
- **Offline mode**. BeQuite's `api-portable` skill mode (Anthropic API hosts that can't shell out to `git clone`) needs the bundle in-tree.
- **PhantomRaven defense**. Pulling code at install time is a supply-chain risk surface; vendored + pinned + reviewable diffs is the safer pattern.

## How we honor the MIT license

- This `ATTRIBUTION.md` file plus the upstream repo link in the README and the pinned-commit file (`.pinned-commit`).
- The bundled stubs preserve Paul's command names, ordering, and philosophy (no rebranding).
- If Paul prefers BeQuite stop bundling Impeccable and instead require users to `git clone` upstream, we'll honor that request — the modular design at `skill/skills-bundled/<name>/` makes removal a single-PR change.

## Update protocol

See `.pinned-commit` in this directory.

## Contact

- Bundling questions: Ahmed Shawky / xpShawky (BeQuite maintainer)
- Upstream Impeccable questions: Paul Bakaus (please direct to the upstream repo's issues / discussions)
