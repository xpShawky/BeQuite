# Prompt Engineering Standard (alpha.19)

> How BeQuite writes prompts — both the prompts INSIDE command/skill files and the prompts BeQuite GENERATES (multi-plan packets, delegate task packs, research queries). Skeletons live in `.bequite/prompts/PROMPT_PATTERNS.md`; authoring depth in `HARNESS_AND_PROMPT_QUALITY.md`.

**Status:** active · **Adopted:** alpha.19 (Fable Strengthening Pass)

---

## The base shape (every non-trivial prompt)

**Role + Goal + Constraints + Sources + Output format.** Never bare "improve this" instructions. Facts and assumptions are separated explicitly (facts cite sources; assumptions are labeled `[Assumption]`). Questions to the user: maximum one, highest-value only, with a recommended default.

## The four prompt classes

| Class | Used by | Properties |
|---|---|---|
| **Complete** | Deep Mode, new builds, regulated | Full role/goal/constraints/sources/format · all relevant DNA + research cited · acceptance criteria embedded |
| **Compact** | Token Saver Mode, follow-ups | Same 5 parts, minimum words · references cached artifacts by path instead of inlining · no restating known context |
| **Neutral** | `/bq-multi-plan` external packets · Delegate task packs | **Zero bias from Claude's prior conclusions.** External models get the same raw briefing Claude got — never Claude's plan to critique. Delegate INSTRUCTIONS state verified constraints as constraints and opinions as `[Architect's preference]`, so the cheap model doesn't inherit unverified assumptions as facts |
| **Strict** | source-fidelity work — `/bq-presentation strict=true`, Writing DNA academic mode, `/bq-spec` from user docs | Every claim traces to a source line · no additions beyond source · `UNVERIFIED:` forced-fork for anything unconfirmed · no invented citations, ever |

## Mode → class mapping

deep → Complete · fast → Compact (with full safety constraints) · token-saver → Compact · delegate → Neutral (pack) + Complete (review phase) · strict/creative flags select Strict vs Complete for content work.

## Anti-patterns (reject on sight)

- Vague verbs without acceptance criteria ("polish", "improve", "make better")
- Repeating research already in `.bequite/research/` instead of citing it
- Biasing packets: "Claude thinks X — do you agree?" (destroys independence)
- Burying the key constraint mid-prompt (most important instructions go FIRST)
- Asking 5 questions when 1 high-value question + defaults would do
- Stating assumptions as facts in any pack another model will consume
