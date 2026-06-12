# Proposal Builder — `/bq-proposal` (C8) — alpha.22

Turn a job post, client request, RFP, or discovered opportunity (C6/C9 output) into a tailored, honest proposal.

## Uses

Writing DNA (the user's voice, not template-speak) · Confidence Forecast (win-likelihood + delivery-confidence stated) · proof/case studies **if present in memory** (`.bequite/` evidence, `/bq-release proof` packs) · client pain analysis · milestones · pricing options (2–3 structures with trade-offs) · risk notes · honest scope boundaries (what's explicitly NOT included).

## Hard rules (refusal-grade)

**Do not overpromise. Do not claim skills, experience, or past results not present in memory or provided by the user.** Unsupported capability claims are removed or flagged to the user before the proposal is shown. Every metric/case-study reference must trace to a memory file or user input. QUESTIONS.md captures what must be asked before sending — a proposal with unresolved blockers says so.

## Outputs — `.bequite/proposals/`

PROPOSAL · CLIENT_NEEDS · MILESTONES · PRICING_OPTIONS · RISK_NOTES · QUESTIONS · DELIVERY_PLAN (one set per opportunity; created on first run).

## Routing

Skills: writing-dna + product-strategist + job-finder/make-money intake discipline + anti-hallucination. Usually follows C9 job-finder or C6 pain-radar; **sending the proposal is always user-performed** (external publishing = human action, never automated). Sibling: C11 `/bq-offer` (built alpha.23) — the standing productized package this command pitches per-client; an offer pack’s PROPOSAL_ANGLE.md feeds this builder directly.
