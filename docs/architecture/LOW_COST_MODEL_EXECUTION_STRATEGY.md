# Low-Cost Model Execution Strategy

Make weaker, cheaper, or local models perform **better** by forcing them through BeQuite workflows. **Honest claim, stated everywhere:** BeQuite does NOT make small models equal to frontier models — it **narrows the gap** with structure, memory, checklists, task decomposition, evidence requirements, and verification gates. Practical how-to: `docs/runbooks/USING_BEQUITE_WITH_SMALLER_MODELS.md` · operational rules `.bequite/state/LOW_COST_MODEL_RULES.md` · foundations: delegate mode (`bequite-delegate-planner`) + the 10-rule frontier card (`FRONTIER_REASONING_SUMMARY.md`).

## 1. Supported targets

Cheaper Claude models · Codex/ChatGPT coding workflows · Cursor · Antigravity-class IDE agents · local models via Ollama · Hermes/OpenClaw-style harnesses · any agent that can read markdown instructions. (Setup per agent: `docs/runbooks/INSTALL_FOR_OTHER_AGENTS.md`.)

## 2. Small-model failure modes (design against, don't deny)

Shallow file inspection · overconfidence · missing cross-file dependencies · fixing the visible symptom only · losing context mid-task · ignoring tests · hallucinating APIs · touching too many files · not updating docs · claiming done without evidence · missing system-design edge cases.

## 3. The 10 small-model rules

1. **Smaller task chunks** — one atomic task per run (delegate task-pack granularity).
2. **Fewer files loaded** — exact reading list, nothing else.
3. **Exact file paths** — never "find the relevant file".
4. **Explicit acceptance criteria** per task.
5. **Skills as checklist text** — paste the relevant SKILL.md sections into the task (auto-attach doesn't exist for them).
6. **Evidence after each step** — command + exit code + output, or the step didn't happen.
7. **Confidence updates required** — banded % before and after, must move with evidence.
8. **No-assumption claims** — every assumption written to ASSUMPTIONS.md, never silently held.
9. **Guard Pass required** on everything produced.
10. **Stronger-model review for risky tasks** when available (delegate review flow).

## 4. Model tier strategy

| Tier | Models | Use for | Never for |
|---|---|---|---|
| **A — frontier** | strongest available | architecture · security · system design · ambiguous scope · large refactors · product strategy · final review | — |
| **B — mid** | capable mid-cost | implementation from exact task packs · docs updates · simple tests · scoped refactors | unsupervised architecture/security |
| **C — small/local** | cheap/local (Ollama-class) | drafts · summaries · boilerplate · fixture/demo data · simple docs · checklist filling · narrowly scoped edits | see hard list below |

**Never give Tier C (and never give Tier B without Tier-A review):** production security decisions · DB migrations · auth changes · payment logic · destructive edits · broad refactors · final release approval. These align with the existing hard human gates and R3 file-risk tiers — the tier strategy adds a *model* dimension to the same safety map.

## 5. How the pieces compose

Delegate mode = Tier A plans (steps 1–8 of the orchestration sequence) → Tier B/C implements from the pack → Tier A reviews + Guard Pass → verify. The frontier 10-rule card travels in every pack. Outside Claude Code, the same flow runs via playbooks (cross-agent strategy). Confidence forecasts from Tier B/C are treated as *claims to verify*, not facts.
