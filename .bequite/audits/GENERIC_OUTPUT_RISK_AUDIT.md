# Generic-Output Risk Audit (alpha.23 tightening, 2026-06-12)

Question: which commands could produce AI-filler output, and what structurally prevents it? Risk = how easy it is for a model to emit plausible-but-generic text that passes superficial review.

## Risk ranking (HIGH = needs the strongest guards)

| Risk | Commands | Why risky | Existing guards | Gap? |
|---|---|---|---|---|
| **HIGH** | C6 pain-radar · C10 make-money · C9 job-finder | live-market claims invite invented "opportunities" | citation-or-strike (anti-hallucination) · source confidence columns · safety rules · live-research requirement | guards exist on paper; **first live run is the real test** — flagged in MASTER §A |
| **HIGH** | C11 offer · C8 proposal | marketing text is the natural habitat of AI filler | no-invented-demand + no-fake-income + promise≠guarantee + UNVERIFIED ASSUMPTION marking + proof-gap lists + Writing DNA voice | same — live trial pending |
| **MED-HIGH** | C5 course · C1 presentation · C2 writing-dna | "outline generator" failure mode | C5: verified Reference A + mandatory practical-task-per-module + completion psychology + curriculum-before-slides refusal; C1: AI-slop anti-pattern list + variants discipline; C2: profile-constrained generation + ethics rules | strongest guard set in the pack; pending live proof |
| **MED** | W1.2 research · W1.4 plan · C4 knowledge · C7 integrate | hand-wavy research/plans; invented endpoints | 11-dim + WebFetch-first + EVIDENCE_LOG; File-Responsibility Map + risk block; chunk-ID grounding; UNVERIFIED endpoint rule | adequate |
| **LOW** | W2.x build · W3.x quality · W4.x release | grounded in actual repo/diff/tests | evidence rules + Guard Pass + gates | adequate |
| **LOW** | N/O/M navigation/orchestration/maintenance | read state files, not prose | file-grounded by construction | adequate |

## Structural anti-generic mechanisms (apply pack-wide)

1. Banned weasel words + evidence-or-UNVERIFIED (contract step 9) — kills confident filler.
2. Confidence with evidence levels that must MOVE — kills static fake certainty.
3. Output = named artifacts with required fields — a generic essay can't satisfy a 12-file pack with exclusions/proof-gaps/confidence columns.
4. Guard Pass docs-guard — catches filler that drifts from repo reality.
5. Primary-source grounding where it matters most (course/offer ← the verified Arabic PDF; integrate ← actual API docs; reference ← actual screenshot).

## Verdict + the honest caveat

Every HIGH-risk command carries explicit, refusal-grade guards — **on paper**. The pack's biggest open quality question is unchanged: zero live trials. The guards' real-world bite is unproven until §A trials run. No new guards needed now; adding more rules without live evidence would be speculative tightening.
