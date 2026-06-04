# Superpowers — researched reference notes

**Source:** Jesse Vincent (obra) — https://github.com/obra/superpowers. Launch post: https://blog.fsck.com/2025/10/09/superpowers/ . Verified against the repo README + raw `skills/<name>/SKILL.md` files (alpha.17 research pass).

> Reference, not a dependency. BeQuite ports the *methodology* (plan → checkpoint → verify; concise skills) — it already has its own gate system.

## What it is

"An agentic skills framework & software development methodology." A library of `skills/<name>/SKILL.md` files, grouped: Testing/Debugging, Collaboration/Workflow, Meta. Key skills: `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `test-driven-development`, `verification-before-completion`, `writing-skills`, `using-superpowers`.

## Methodology ported into BeQuite's frontend discipline

1. **Plan before code (committed spec gate).** Brainstorming HARD-GATE: no implementation until a written, self-reviewed, user-approved design exists. → maps to BeQuite persisting `DESIGN_DNA.md` before any UI code (`DESIGN_DNA_LOCKED`) and the section map before building.
2. **Topic-by-topic / section-by-section approval checkpoints.** "Ask after each section whether it looks right." → the heart of BeQuite's section-by-section loop: build section → check section → continue.
3. **Verify-before-done with fresh evidence.** `verification-before-completion`: *"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE."* 5-step gate: identify the proof command → run fresh → read full output + exit codes → confirm it supports the claim → only then claim. Banned language: "should work / probably / seems to." → reinforces BeQuite Iron Law #2 + banned weasel words + the Visual QA "render it, don't trust code inspection" rule.
4. **Concise skills + on-demand reference files.** `writing-skills` word budgets: frequently-loaded <200 words, others <500; **split reference docs when 100+ lines** (load on demand, not inline). Frontmatter: only `name` + `description` mandatory, ≤1024 chars; **descriptions start with "Use when…" and state triggers only, never the workflow** (CSO rule — the model may follow the description instead of reading the skill). → BeQuite's master SKILL.md is concise and pushes heavy material to `references/`.
5. **TDD-for-skills / TDD-for-docs.** "If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing." Baseline fail → minimal fix → re-test. → fold into the feature-addition workflow ("watch it fail first").
6. **Subagent-driven execution + two-stage review.** Fresh subagent per task with isolated context, given the **full task text** (not a file pointer); returns DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED. Review order: **spec-compliance reviewer FIRST, then code-quality reviewer.** → maps to BeQuite's Delegate Mode + `/bq-review` → `/bq-red-team`.
7. **Bite-sized tasks + stop-and-ask on blockers.** 2–5 min tasks each carrying their own verification; STOP on blocker/test-fail/unclear instruction rather than forcing through.
8. **Rationalization tables.** Capture the exact excuses an agent makes ("should work now", "I'm confident", "just this once") + the counter. → BeQuite's MISTAKE_MEMORY + banned-weasel-word discipline.

## Top principles BeQuite encodes

1. Design DNA persisted + locked before code.
2. Section-by-section checkpoints (build → check → continue).
3. Verify-before-done with fresh evidence (Visual QA render, not code-only claims).
4. Concise SKILL.md + on-demand `references/` (the structure of this very skill).
5. Description = triggers only ("Use when…"), never the workflow.
6. Effort/depth scales the rigor (low→compact, high→full, xhigh→deep) — BeQuite's effort-awareness mirror of Superpowers' "scale to complexity."
7. Two-stage review order for delegated frontend work.
8. No completion claim without rendered evidence + no banned weasel words.

**Note:** This is methodology, not design rules. BeQuite keeps its own 23-gate system; Superpowers tightens *how* BeQuite proves frontend work is actually done.
