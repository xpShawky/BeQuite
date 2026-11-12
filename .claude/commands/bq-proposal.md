---
description: Proposal Builder (C8). Turn a job post, client request, RFP, or discovered opportunity into a tailored, honest proposal using Writing DNA, confidence forecast, real proof from memory, milestones, pricing options, and explicit scope boundaries. Never overpromises; never claims skills or experience not in memory or user-provided.
---

# /bq-proposal — opportunity → honest tailored proposal (C8)

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 2. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 3. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 4. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 5. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 6. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 7. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

Full spec: `.claude/bequite/docs/specs/PROPOSAL_BUILDER.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block.

## Syntax

```
/bq-proposal "<job post / RFP text or path>" [pricing=fixed|milestone|retainer] [tone=<writing-dna profile>]
```

## Preconditions / gates

`BEQUITE_INITIALIZED`. **Sending is always user-performed** — BeQuite drafts; the user submits (external publishing = human action).

## Honesty rules (refusal-grade)

**Do not overpromise. Do not claim skills, experience, or results not present in `.bequite/` memory or provided by the user this session.** Each capability claim traces to a source; unsupported claims are cut or flagged before the draft is shown. Unresolved blockers land in `QUESTIONS.md` and the proposal says so.

## Steps (after contract steps 1–7)

1. **Decode the client** — `CLIENT_NEEDS.md`: stated asks vs underlying pain vs success criteria vs red flags (scope traps, payment risk — job-finder safety rules apply).
2. **Match honestly** — map needs to *evidenced* capabilities (memory, `/bq-release proof` packs, user input). Gaps stated, with mitigation (learning plan / partner / descope).
3. **Structure the offer** — `MILESTONES.md` (verifiable deliverables) · `PRICING_OPTIONS.md` (2–3 structures + trade-offs) · `RISK_NOTES.md` · `DELIVERY_PLAN.md` · explicit out-of-scope list.
4. **Write in the user's voice** — Writing DNA profile if present (else offer to build one via C2); confidence forecast included (win-likelihood + delivery confidence).
5. **Pre-send check** — `QUESTIONS.md`: what to ask before sending; weasel-word and overclaim scan on the final draft.

## Writes

`.bequite/proposals/{PROPOSAL,CLIENT_NEEDS,MILESTONES,PRICING_OPTIONS,RISK_NOTES,QUESTIONS,DELIVERY_PLAN}.md` + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

Sibling: **C11 `/bq-offer`** (alpha.23) builds the standing offer this command pitches per-client; if `.bequite/offers/PROPOSAL_ANGLE.md` exists, read it first.

writing-dna · product-strategist · job-finder/make-money intake + safety discipline · anti-hallucination.

## Next Command Recommendations (typical)

Required next: **user reviews + sends** (no auto-run — external action). Set: C2 `/bq-writing-dna` (no profile yet) · W4.2 `/bq-release proof` (build the evidence pack that wins the next one) · C9 `/bq-job-finder` (more opportunities). Do not run yet: building the project before the client accepts — proposals are offers, not commitments.
