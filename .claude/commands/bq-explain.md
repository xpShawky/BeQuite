---
description: Explain a file / function / decision / concept in plain English. Useful for onboarding, vibe-handoff prep, understanding inherited code, or learning what BeQuite did during /bq-auto. Read-only.
---

# /bq-explain — plain-English explainer

## Purpose

Take a piece of code / a file / a decision / a concept and explain it in **plain English** — no jargon, no implementation reasoning, just what it DOES and why it matters.

For vibe coders, non-engineer stakeholders, future-you returning to inherited code, or anyone who wants to understand what's there without reading every line.

## When to use it

- Returning to AI-generated code you don't fully understand
- Onboarding a new engineer / vibe coder to the project
- Preparing a handoff (`/bq-handoff` uses `/bq-explain` outputs)
- Explaining a `DECISIONS.md` entry to a stakeholder
- Understanding a chunk of inherited code in an existing project
- Understanding what BeQuite did during `/bq-auto`

## When NOT to use it

- Writing new code (use `/bq-feature` or `/bq-implement`)
- Fixing a bug (use `/bq-fix` — needs reproduction discipline, not explanation)
- Designing UI (use `/bq-uiux-variants` or `/bq-live-edit`)
- A full project tour (use `/bq-discover` + `/bq-handoff`)

## Syntax

```
/bq-explain "<target>"
```

`<target>` can be:
- A file path: `"app/api/bookings/route.ts"`
- A function name: `"computeMonthlyTotal in lib/billing.ts"`
- A concept: `"how auth works in this project"`
- A decision: `"why we chose Drizzle over Prisma"`
- A BeQuite artifact: `".bequite/audits/RESEARCH_REPORT.md"` or `"the IMPLEMENTATION_PLAN"`
- A command output: `"what /bq-auto did in the last run"`

Examples:
- `/bq-explain "lib/auth.ts"`
- `/bq-explain "the PricingCards component"`
- `/bq-explain "how the rate limiter works"`
- `/bq-explain "ADR-002"`
- `/bq-explain "what /bq-auto changed last run"`

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- None (read-only)

## Files to read

- The target file(s) — derived from the argument
- Related files the target imports / depends on (1-2 hops max)
- `.bequite/state/DECISIONS.md` (if target is a decision)
- `.bequite/audits/*.md` (if target is an artifact)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (for context)

## Files to write

None. `/bq-explain` is strictly read-only.

## Steps

### 1. Parse the target

If `/bq-explain` invoked alone → ask:
> "What do you want explained? File, function, concept, decision, or BeQuite artifact?"

If argument provided → identify target type:
- Path-like with extension → file
- "X in Y" pattern → function in file
- Starts with "how" / "why" / "what" → concept
- Mentions "decision" / "ADR" → decision
- Mentions "/bq-" → command output

### 2. Read the target + neighbors

For a file:
- Read the file
- Read 1-2 files it imports (just enough for context)
- Read the test file if one exists alongside

For a function:
- Read the function + its file
- Read the test file
- Read its callers (1-hop)

For a concept:
- Identify 2-3 relevant files
- Read them
- Read related ADR if exists

For a decision:
- Read the relevant `DECISIONS.md` entry
- Read the related ADR if exists
- Read the affected code (1-2 files)

For a BeQuite artifact:
- Read the artifact
- Skim related state files for context

### 3. Write the explanation

The explanation has 4 sections — kept SHORT (this is a summary, not a tutorial):

```
## What it is

(1-2 sentences. Plain English. No jargon. What would you say to a non-engineer?)

## What it does

(2-4 sentences. The behavior, not the implementation. Inputs → outputs. User-visible effects.)

## Why it matters

(1-2 sentences. What changes for users / the system / the team if this is broken or removed?)

## Things to be careful of

(0-3 bullets. Edge cases, gotchas, known issues, "if you change this, also change that".)
```

For files, also include:
```
## Related files

- `<path>` — <one-line reason it's related>
- `<path>` — <one-line reason it's related>
```

### 4. Print to chat

Print the 4-section explanation directly. No file written. No state change.

If user wants the explanation saved (e.g. for handoff), suggest:
> "Save this to `.bequite/handoff/explain-<target-slug>.md`? (y/N)"

If yes → write the file. Otherwise → chat-only.

### 5. Suggest next steps

```
Want to dig deeper? Try:
  /bq-explain "<related file>"        — explain something this references
  /bq-handoff                          — generate full handoff with /bq-explain outputs
  /bq-audit                            — full project audit if you want concerns surfaced
```

## Output format

The 4-section explanation in chat. Concise. No code blocks dumped verbatim. No re-reading the file at the user — they could do that themselves; the value of `/bq-explain` is the SYNTHESIS.

## Quality gate

- Plain English (no jargon — or if used, defined inline)
- Concrete (cites file:line where relevant)
- Honest (if you don't understand a part, say so — don't bluff)
- 4 sections present (What it is / What it does / Why it matters / Things to be careful of)
- "Why it matters" actually answers the question (not "it does X" again)
- No banned weasel words

## Failure behavior

- Target unclear → ask ONE clarifying question; then proceed
- Target file unreadable / not found → say so + suggest similar paths
- Target is too large (e.g. "explain the whole codebase") → narrow with user; suggest 1-2 file targets instead
- Concept requires too much context → cite the relevant docs (e.g. ADR-002, IMPLEMENTATION_PLAN §11) + give a 1-paragraph summary; don't try to fully explain inside chat

## Memory updates

None by default. If user opts to save the explanation, writes to `.bequite/handoff/explain-<target-slug>.md`.

## Log updates

None by default (read-only navigation). If saved, append to `AGENT_LOG.md`.

## Tool neutrality (global rule)

`/bq-explain` doesn't pick tools. Read-only. Nothing to install.

But: the explanations themselves should respect tool neutrality. When explaining a tool choice (e.g. "why Drizzle?"), surface the decision section rationale rather than implying Drizzle is universally correct.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Vibe-handoff use case

When preparing a project for someone non-technical to inherit (a "vibe-coder" or non-engineer stakeholder):

1. Run `/bq-explain` on every top-level component / page
2. Run `/bq-explain` on every ADR
3. Run `/bq-explain` on the overall architecture
4. Save each output to `.bequite/handoff/`
5. Run `/bq-handoff` — it'll pick up the saved explanations and bundle them

Result: a HANDOFF.md that an inheritor can read without writing code first.

## Usual next command

- `/bq-explain "<another target>"` — keep exploring
- `/bq-handoff` — if you're preparing handoff and need the explanations bundled
- `/bq-audit` — if explanation surfaced concerns worth investigating
