# Low-Cost Model Rules (operational card)

Strategy: `docs/architecture/LOW_COST_MODEL_EXECUTION_STRATEGY.md` · runbook: `docs/runbooks/USING_BEQUITE_WITH_SMALLER_MODELS.md`. **Honest claim: BeQuite narrows the gap (structure · memory · checklists · decomposition · evidence · gates) — it does not make small models frontier models.**

## Tiers

- **A (frontier):** architecture · security · system design · ambiguous scope · large refactors · strategy · final review
- **B (mid):** implementation from exact task packs · docs · simple tests · scoped refactors
- **C (small/local, Ollama-class):** drafts · summaries · boilerplate · fixture/demo data · simple docs · checklist filling · narrow edits

**NEVER for C (and never for B without A-review):** production security decisions · DB migrations · auth changes · payment logic · destructive edits · broad refactors · final release approval.

## The 10 rules (apply to every B/C run)

1 smaller chunks · 2 fewer files · 3 exact paths · 4 explicit acceptance criteria · 5 skills pasted as checklist text · 6 evidence per step · 7 confidence updates · 8 assumptions written, never held · 9 Guard Pass on all output · 10 stronger-model review for risky tasks

B/C confidence claims are treated as claims-to-verify, not facts. The frontier 10-rule card (`FRONTIER_REASONING_SUMMARY.md`) ships in every task pack.
