# High-Risk Command Hardening Audit (alpha.24, 2026-06-13)

Hardened the 5 market-claim commands against fake/generic/overconfident output. Test cases: `docs/specs/HIGH_RISK_COMMAND_TEST_CASES.md`. Research sourcing honest per the evidence-log convention.

## Research notes (honest labels)

- **Income/earnings-claim deception** — `ECO` (FTC endorsement-guide page returned HTTP 403 this session; NOT live-fetched). Established principle stated as ecosystem knowledge: earnings claims need substantiation; atypical results require a clear "typical results" disclosure; cherry-picked success testimonials presented as normal are deceptive. **Applied:** C10/C11 ban guaranteed-income framing and require proof-gap disclosure; this is encoded as a rule, not cited as a live source.
- **Productized services / offer design** — `PRIOR-LIVE` (the *Your First Million* Arabic PDF, read 2026-06-12): fixed scope + explicit exclusions + risk-reversal + test-on-5-people + MVP-first. Already encoded in OFFER_ENGINE; reinforced in C11 test cases.
- **Cold outreach / proposal honesty / scam patterns** — `ECO`: upfront-fee, identity-doc requests, unpaid-spec-work, MLM/get-rich-quick, VPN-misrepresentation are known red flags; already in job-finder/make-money safety rules — extended to the test cases.
- **Pain mining ethics** — `PRIOR-LIVE` (PAIN_RADAR spec): official-API-first, no auth bypass, no ToS violation. Confirmed sufficient.

## Hardening applied

Each command's test-case set adds: explicit refusal cases, generic-output traps, mandatory `UNVERIFIED ASSUMPTION` marking, evidence requirements, language/localization checks, and **confidence caps** (offer 75% no-buyer-signal · proposal 80% pre-reply · pain-radar 70% single-source · make-money 70% no-channel · job-finder 75% weak-fit). These caps mean the Confidence Forecast cannot report high certainty on the exact claims most likely to be fabricated.

## Verdict

The 5 commands already carried refusal-grade honesty rules (built in alpha.22–23); this pass converts those rules into **concrete, testable behavioral cases** + confidence caps, closing the "guards exist on paper" gap flagged in the alpha.23 generic-output audit as much as is possible without a live trial. Live validation of the caps still rides on first real runs (MASTER §A).
