# Auto Mode Rules (operational card)

Strategy: `docs/architecture/AUTO_MODE_ORCHESTRATION_STRATEGY.md` (+ base `AUTO_MODE_STRATEGY.md` for intents/gates). Auto Mode = orchestrator, never "continue coding".

## The 15-step sequence (no silent skips)

1 Memory preflight → 2 Command router check → 3 Skill router check → 4 System design risk check → 5 File risk classification → 6 Context budget check → 7 Confidence forecast → 8 Task plan → 9 Implementation → 10 Tests → 11 Guard Pass → 12 Verification → 13 Evidence log → 14 Memory writeback → 15 Next command recommendations

- Irrelevant step ⇒ output `Not applicable — reason: …`
- Impossible step ⇒ `Blocked — reason: …` then stop-or-ask per gates
- fast/token-saver compress step SIZE, never SEQUENCE

## Stop / Ask / Continue / Compact

- **STOP:** the 17 hard human gates (unchanged, never routed around) + R3 file edits + blocking risk-check unknowns on safety-relevant work
- **ASK (one question):** inferred scope on risky action · Missing Capability detected · risk unknown that blocks safe implementation
- **CONTINUE:** safe + scoped + gates green — never pause for approval theater
- **COMPACT:** ~40% summary / ~60% externalize / ~75% finish-only / ~85% handoff (`CONTEXT_COMPACTION_RULES.md`); check at every task boundary
- **GUARD PASS:** always after implement/tests in auto mode, before verify/release
- **MEMORY:** every durable fact written at the step boundary that produced it

## Reporting

Report internally-executed steps by catalog ID (`Internal workflow executed: W0.3 → W1.2 → …`), then the standard Next Command Recommendations block. Confidence stated at plan and at completion; banned weasel words apply.
