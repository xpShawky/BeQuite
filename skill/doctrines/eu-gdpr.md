---
name: eu-gdpr
version: 1.0.0
applies_to: [eu, eea, gdpr, regulated, personal-data]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: eu-gdpr v1.0.0

> EU General Data Protection Regulation 2016/679. Regulates processing of personal data of EU/EEA residents. Stacks with `mena-pdpl` (when project serves both regions; e.g. UAE-DIFC also tracks GDPR).
>
> **Disclaimer**: starting point shaped by GDPR + EDPB guidance + national-DPA-specific guidance (CNIL, BfDI, AEPD, Garante). NOT a substitute for legal counsel.

## 1. Scope

Applications that:

- Are established in the EU/EEA (regardless of where data subjects live).
- Process personal data of EU/EEA residents (regardless of where the controller is established — extra-territorial reach per Art. 3).
- Offer goods or services to EU residents.
- Monitor behavior of EU residents.

Active when `compliance` includes `gdpr` in `state/project.yaml`.

## 2. Rules

### Rule 1 — Lawful basis required (Art. 6) — every processing operation

One of:

1. **Consent** (Art. 6(1)(a)) — freely given, specific, informed, unambiguous; withdrawal as easy as giving.
2. **Contract** (Art. 6(1)(b)) — necessary for contract performance.
3. **Legal obligation** (Art. 6(1)(c)).
4. **Vital interests** (Art. 6(1)(d)).
5. **Public interest** (Art. 6(1)(e)).
6. **Legitimate interests** (Art. 6(1)(f)) — with balancing test (LIA).

Document in `compliance/lawful-basis.md` per processing-purpose. Special category data (health, biometric, racial, political, religious, sexual orientation, trade union, genetic) requires Art. 9 separate basis.

### Rule 2 — Data subject rights endpoints (Arts. 15-22)

Endpoints for:

- **Art. 15 Access** — export user's data within 30 days.
- **Art. 16 Rectification**.
- **Art. 17 Erasure** ("right to be forgotten") — with retention exceptions documented.
- **Art. 18 Restriction**.
- **Art. 19 Notification of rectification/erasure**.
- **Art. 20 Data portability** — machine-readable export.
- **Art. 21 Objection** — including direct marketing opt-out.
- **Art. 22 Automated decision** — when automated decision has legal effects.

Implementation: REST or GraphQL endpoints under `/api/data-subject/{userId}/{operation}`. Audit-logged. SLA tracked (default 30 days).

### Rule 3 — Privacy by design + by default (Art. 25)

- Data minimisation: only fields strictly necessary collected.
- Purpose limitation: data used only for the documented purpose.
- Storage limitation: retention periods documented + enforced.
- Privacy-friendly defaults: most-private settings as initial values.

### Rule 4 — Records of processing activities (Art. 30)

`compliance/ropa.md` — comprehensive list of processing activities. Updated on every new feature touching personal data.

### Rule 5 — Data Protection Impact Assessment (Art. 35)

DPIA required for high-risk processing:

- Systematic and extensive evaluation of personal aspects via automated processing.
- Large-scale processing of special categories or criminal-conviction data.
- Systematic monitoring of public areas.

`compliance/dpia-<feature>.md` template per high-risk feature. Cross-reference threat-model from `security-auditor`.

### Rule 6 — Encryption + pseudonymisation (Art. 32)

- **Encryption at rest**: AES-256 on PII columns.
- **TLS 1.2+ in transit**.
- **Pseudonymisation** when feasible (replace direct identifiers with tokens).

### Rule 7 — Cross-border transfer (Chapter V)

EU/EEA → outside requires:

- **Adequacy decision** (UK, Canada, Switzerland, Japan, Israel, etc.) — automatic.
- **Standard Contractual Clauses (SCCs)** — 2021 modules.
- **Binding Corporate Rules** — for intra-group transfers.
- **Explicit consent** — narrow.
- **Public interest** — narrow.

Transfer Impact Assessment (TIA) when destination has surveillance / no equivalent rights. Document in `compliance/cross-border-transfer.md`.

### Rule 8 — Breach notification (Art. 33-34)

- **Within 72 hours** to lead supervisory authority when likely risk to rights.
- **Without undue delay** to affected data subjects when high risk.

`compliance/breach-runbook.md` — DPO contact, regulator chain, communication templates. Tabletop exercise annually.

### Rule 9 — DPO appointment (Art. 37)

DPO required when:

- Public authority.
- Large-scale regular and systematic monitoring.
- Large-scale special-category processing.

Document DPO appointment in `compliance/dpo-appointment.md`.

### Rule 10 — Cookie + tracking consent (ePrivacy + GDPR)

- Cookie banner: pre-ticked boxes forbidden.
- Reject-all as easy as accept-all.
- Granular per-purpose consent.
- Withdrawal as easy as giving.
- Documented consent log.

Approved patterns: Klaro, OneTrust (with caution), self-built compliant banner. **Avoid** dark-pattern banners.

### Rule 11 — Children's data (Art. 8)

Processing children's data (under 16, member-state-variable down to 13) requires verifiable parental consent. Age-gate at sign-up. `compliance/children-protection.md` per applicable jurisdictions.

### Rule 12 — Logging excludes PII

Application logs (operational + security) exclude direct identifiers. Use opaque user IDs + request IDs.

## 3. Stack guidance

### EU-region cloud

| Provider | Region | When |
|---|---|---|
| AWS | `eu-west-1`, `eu-central-1`, `eu-north-1` | Default; Schrems II + SCCs apply for any non-EEA processing |
| Azure | `West Europe`, `North Europe`, `Sweden Central` | Same |
| GCP | `europe-west1`, `europe-west3` | Same |
| OVHCloud, Scaleway, Hetzner | Various EU | EU-only providers; lighter Schrems II concerns |

### LLM with EU DPA

Provider DPAs that include EU adequacy provisions:

- Anthropic (DPA available) — Claude API; **enterprise-tier with no data retention required for PII**.
- OpenAI (DPA available) — same conditions.
- Google Vertex AI — DPA + EU regions.
- Self-hosted (vLLM + Llama) on EU cloud — when zero-trust.

### Auth + consent

- **Better-Auth** with consent-log integration.
- **Clerk** with GDPR-compliant config.
- **Supabase Auth** — EU region; consent-log via separate table.

## 4. Verification

`bequite verify` for eu-gdpr projects:

1. **Lawful-basis documentation** complete per processing operation.
2. **Data subject rights endpoints** all 8 implemented + tested + 30-day SLA verified.
3. **DPIA present** for high-risk features.
4. **RoPA up-to-date**.
5. **Breach runbook + tabletop** within last 12 months.
6. **DPO appointed + documented** (when required).
7. **Cookie banner compliant** (no dark patterns; reject-all available).
8. **Cross-border transfers documented + SCCs in place**.
9. **Encryption at rest + in transit** verified.
10. **Logs exclude PII** verified by sample audit.

## 5. References

- **GDPR full text**: https://gdpr-info.eu/
- **EDPB guidance**: https://edpb.europa.eu/edpb_en
- **Schrems II ruling**: CJEU C-311/18
- **Standard Contractual Clauses (2021)**: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
- **CNIL** (France): https://www.cnil.fr/
- **BfDI** (Germany): https://www.bfdi.bund.de/
- **AEPD** (Spain): https://www.aepd.es/
- **Garante** (Italy): https://www.garanteprivacy.it/
- **DPC** (Ireland): https://www.dataprotection.ie/

## 6. Forking guidance

- **`eu-gdpr-strict-dpa`** — for high-stakes processors needing extra controls.
- **`eu-gdpr-ad-tech`** — extra rules for advertising / tracking specific concerns.
- **`eu-gdpr-health`** — overlay for health data + Art. 9 special category rules.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Twelve rules. Stacks with mena-pdpl when DIFC / ADGM in scope (those track GDPR closely). NOT a substitute for legal counsel.
```
