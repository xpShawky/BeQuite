# Auto Mode Orchestration Strategy

Auto Mode is **not** a "continue automatically" switch — it is BeQuite's orchestration layer. As the pack grew (52 commands, 30 skills, two routers, 4 modes, capability specs), shallow continuation became the biggest quality risk: skipping steps, losing context, forgetting available skills, ignoring system-design risks, shipping pretty-but-broken work. This strategy makes Auto Mode a disciplined orchestrator. Companion: `BEQUITE_ORCHESTRATION_MODEL.md` (the global brain, not auto-only) · operational rules `.bequite/state/AUTO_MODE_RULES.md` · base doc `AUTO_MODE_STRATEGY.md` (intents + gates, still canonical for those).

## 1. What the orchestrator must know before acting

Current phase · current command · operating mode · available commands (`COMMAND_ID_MAP.md`) · available skills (`SKILL_REGISTRY.md`) · memory state (preflight files) · gate states · file-risk tier of likely-touched paths · current confidence + what would move it · likely failure modes for the domain · required tests · the next workflow step · relevant capability commands · **when to stop, ask, continue, compact context, run Guard Pass, and write memory**. All of this is readable from files — an orchestrator that "doesn't know" didn't read.

## 2. The 15-step internal sequence (anti-skip)

```
1 Memory preflight          6 Context budget check        11 Guard Pass
2 Command router check      7 Confidence forecast         12 Verification
3 Skill router check        8 Task plan                   13 Evidence log
4 System design risk check  9 Implementation              14 Memory writeback
5 File risk classification 10 Tests                       15 Next command recommendations
```

**No silent skips.** Irrelevant step ⇒ output `Not applicable — reason: …`. Impossible step ⇒ `Blocked — reason: …` (and decide stop-vs-ask per hard-gate rules). This maps onto the 12-step execution contract (steps 4–6 here expand contract steps 6–8); the contract remains the per-command law, this sequence is the auto-run traversal of it.

## 3. "Continue coding" vs orchestrated build — the canonical example

User: *"Build an e-commerce store feature."* A shallow continuation builds a nice product grid. The orchestrator must reason across: product flow · frontend · backend · database · **inventory** · concurrency · payments · order states · security · idempotency · race conditions · tests · release readiness.

**The one-item-two-buyers test:** one unit in stock, two users order simultaneously. The orchestrated workflow must answer — inventory reservation? transaction locking (optimistic vs pessimistic)? payment-before-stock vs stock-before-payment? idempotency keys? order status transitions? retry behavior? refund/cancel flows? audit log? what each user *sees*? race-condition tests? If the plan can't answer these, the System Design Risk Check (step 4) failed and implementation must not start. Full domain libraries: `SYSTEM_DESIGN_REASONING_STANDARD.md`.

## 4. Stop / ask / continue / compact rules

- **Stop** at the 17 hard human gates — unchanged, the orchestrator never routes around them.
- **Ask** (one high-value question) when scope is inferred on a risky action, when a risk-check unknown blocks safe implementation, or when Missing Capability is detected (`BEQUITE_ORCHESTRATION_MODEL.md` §missing-capability).
- **Continue** when the step is safe, scoped, and gated-through — never pause for "should I continue?".
- **Compact** at the context thresholds in `CONTEXT_COMPACTION_STRATEGY.md` (40/60/75/85%); auto mode checks pressure at every task boundary (step 6).
- **Guard Pass** after implementation/tests (step 11), before verify/release — always in auto mode; report-only findings escalate per severity.
- **Write memory** at every step boundary that produced a durable fact (step 14 + compaction rules) — chat memory is never the only copy of a critical fact.

## 5. Mode interaction

fast/token-saver compress step *size*, never step *sequence* (same law as the contract). delegate mode runs this sequence twice: the strong model owns steps 1–8 + 11–15; the cheap model executes step 9–10 from the task pack (see `LOW_COST_MODEL_EXECUTION_STRATEGY.md` tiers). `expert` alias = deep + strict evidence on every step.
