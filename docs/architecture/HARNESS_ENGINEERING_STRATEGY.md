# Harness Engineering Strategy (alpha.19 index)

> **The index for BeQuite's harness layer** — how the agent is kept reliable across command entry → verification → writeback. This file orients; the deep content lives in the linked docs (one source of truth each; no duplication).

**Status:** active · **Adopted:** alpha.19 (Fable Strengthening Pass)

---

## What "harness" means in BeQuite

BeQuite has no runtime. The harness is the **layered set of contracts the agent operates inside**:

```
User intent
  └─ Command entry (.claude/commands/*.md — markdown dispatch)
      └─ COMMAND_EXECUTION_CONTRACT.md (the 11 steps — canonical)
          ├─ Memory preflight ........ MEMORY_FIRST_BEHAVIOR.md + CONTEXT_ENGINEERING.md
          ├─ Skill registry check .... .bequite/skills/SKILL_REGISTRY.md (alpha.20)
          ├─ Task classification ..... .bequite/skills/SKILL_ROUTER.md domain map (alpha.20)
          ├─ Auto skill selection .... AUTO_SKILL_ROUTING_STRATEGY.md (mode sizing + auto-attach)
          ├─ Gate check .............. WORKFLOW_GATES.md (23 gates + aliases)
          ├─ Research scope .......... RESEARCH_DEPTH_STRATEGY.md (+ no-research-repeat rule)
          ├─ Plan / task split ....... FEATURE_AND_FIX_WORKFLOWS.md + FILE_RESPONSIBILITY_MAP
          ├─ Implementation .......... PROJECT_DNA conformance + smallest-safe-change (CLAUDE.md rule 16)
          ├─ File-edit safety ........ FILE_RISK_CLASSIFICATION.md (alpha.19)
          ├─ Verification gate ....... bequite-anti-hallucination + EVIDENCE_LOG + /bq-verify
          ├─ Report .................. HARNESS_AND_PROMPT_QUALITY.md (output discipline)
          ├─ Memory writeback ........ MEMORY_FIRST_BEHAVIOR.md §writeback
          └─ Next command ............ gate-aware recommendation (/bequite logic)
      └─ Machine layer (opt-in) ..... CLAUDE_CODE_HOOKS_STRATEGY.md (3 hooks, exit-2 semantics)
      └─ Autonomy bounds ............ AUTO_MODE_STRATEGY.md (17 hard human gates + uncertain-scope)
```

## The three enforcement surfaces

1. **Convention** (strongest coverage, weakest guarantee): the execution contract + per-command blocks. Holds because every command cites it and the agent reads it fresh each invocation.
2. **State** (medium): gate ledger + DNA files + risk rules — checkable artifacts the agent must consult; drift is visible in git diffs.
3. **Machine** (narrowest, hardest): opt-in hooks — destructive-op block, secret scan, weasel-word stop. Catches the agent when convention fails under context pressure.

Design rule: **new safety needs go to the weakest sufficient surface.** Don't write a hook when a contract step suffices; don't write a contract step when a gate-ledger entry suffices.

## Subagent delegation policy

Subagents get **isolated context** and return results only. Use for: parallel fan-out reads, adversarial fresh-context verification (anti-hallucination), variant generation. Never for: decisions requiring accumulated session judgment, hard-gate approvals. The Delegate Mode cross-SESSION pattern (`bequite-delegate-planner`) is distinct from in-session subagents — task packs make the handoff explicit.

## Failure-mode map (what the harness defends against)

| Failure mode | Defense |
|---|---|
| Assumption stacking in auto mode | contract step 3 + ASSUMPTIONS.md + uncertain-scope gate |
| Context loss after compaction | PROJECT_DNA + CONTEXT_SUMMARY + WORKING_NOTES (compaction-survival rule) |
| Premature "done" claims | weasel-word rules + Stop hook + EVIDENCE_LOG |
| Repeated researched-before work | no-research-repeat rule (contract step 5) |
| Risky file edits sailing through | FILE_RISK_CLASSIFICATION tiers |
| Skipped writeback (esp. CHANGELOG) | contract step 10 explicit list |
| Skill stagnation | /bq-skill-audit loop (alpha.19) |
