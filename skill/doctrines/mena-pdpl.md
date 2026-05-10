---
name: mena-pdpl
version: 1.0.0
applies_to: [mena, egypt, saudi-arabia, uae, regulated, personal-data]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: mena-pdpl v1.0.0

> MENA-region personal data protection. **Jurisdiction-branched** because Egyptian PDPL, Saudi PDPL, and UAE PDPL differ materially. Stacks with `mena-bilingual` (locale + RTL) and pairs with `eu-gdpr` for projects serving EU + MENA users.
>
> The `jurisdiction` field in `state/project.yaml::compliance` selects the active branch. Multiple branches can be active simultaneously (project serves users in all three).
>
> **Disclaimer**: this Doctrine is a starting point shaped by current authoritative sources (May 2026). It is NOT a substitute for local legal counsel. Egyptian executive regulations are still pending publication as of 2026; UAE has free-zone carve-outs (DIFC, ADGM) with their own DPLs.

## 1. Scope

Applications that process personal data of residents of:

- **Egypt** (Egyptian PDPL — Law No. 151 of 2020; in force 2020-10-17)
- **Kingdom of Saudi Arabia** (Saudi PDPL — Royal Decree M/19 (2021), amended M/148 (2023); fully enforceable since 2024-09-14; 48+ SDAIA enforcement decisions by Jan 2026)
- **United Arab Emirates** (UAE PDPL — Federal Decree-Law 45/2021; in force 2022-01-02)

Active jurisdiction selected by:

```toml
[compliance]
mena_jurisdiction = ["egypt", "ksa", "uae-federal"]
# or include free-zone-specific:
# mena_jurisdiction = ["uae-difc", "uae-adgm", "uae-dhcc"]
```

## 2. Common rules (all jurisdictions)

### R-COMMON-1 — Lawful basis required

Every PII processing operation has a documented lawful basis. Branch to the active jurisdiction's enumeration:

- **Egypt** (Law 151/2020 Art. 7): consent / contractual necessity / legal obligation / vital interests / public interest / data controller's legitimate interest.
- **KSA** (PDPL Art. 5): consent (default) / contract / legal obligation / public interest / vital interests / legitimate interests of controller (limited).
- **UAE Federal** (Decree-Law 45/2021 Art. 5): consent / contract / legal obligation / vital interests / public interest / legitimate interests of controller.

Document in `compliance/lawful-basis-<jurisdiction>.md` per controller-jurisdiction pair.

### R-COMMON-2 — Data subject rights endpoints

Every regulated project ships endpoints for:

- Right of access (export user's data)
- Right of rectification
- Right of erasure (with allowed-retention exceptions)
- Right of restriction of processing
- Right of objection
- Right of data portability (where applicable)
- Right not to be subject to automated decision (where applicable)

Implementation: REST or GraphQL endpoints under `/api/data-subject/{userId}/{operation}`. Audit-logged.

### R-COMMON-3 — Encryption at rest + in transit

- **At rest**: AES-256 (column-level for PII columns). FIPS-validated when KSA / FedRAMP-overlap.
- **In transit**: TLS 1.2+ (1.3 preferred). FIPS-approved suites for KSA.

### R-COMMON-4 — Cross-border transfer documentation

When personal data crosses jurisdictions, document:

- Source jurisdiction
- Destination jurisdiction
- Mechanism (SCCs equivalent / adequacy decision / explicit consent / SDAIA license)
- Data minimisation (only necessary fields)
- Retention period after transfer

### R-COMMON-5 — Breach notification within 72 hours (default)

Per regulator + per affected data subjects (when high risk).

- **Egypt**: Data Protection Centre (yet to be operational pending executive regs); plan for 72h.
- **KSA**: SDAIA within 72 hours; data subjects when high risk to their rights.
- **UAE Federal**: UAE Data Office; affected individuals when high risk.

Breach runbook at `compliance/breach-runbook-<jurisdiction>.md`. Tabletop exercise annually.

### R-COMMON-6 — DPO appointment (when required)

- **KSA**: DPO required for large-scale processing or special categories.
- **UAE**: DPO required for sensitive personal data processing or specific cases.
- **Egypt**: DPO model encoded in pending executive regs.

## 3. Egypt-specific rules

### R-EGY-1 — Data Protection Centre license (when required)

Many controllers/processors must obtain a license from the Data Protection Centre under MCIT.

- License application: `compliance/egypt-dpc-license-application.md`
- License status tracker: pending / approved / renewed / suspended

### R-EGY-2 — Egyptian Arabic notice + consent

Privacy notice + consent flows MUST be available in Arabic (Egyptian dialect acceptable). Pair with `mena-bilingual` Doctrine.

### R-EGY-3 — Sensitive data restrictions

Special categories (health, biometric, religion, political opinion, ethnic origin, criminal records) — explicit consent + Data Protection Centre approval often required.

### R-EGY-4 — Pending executive regulations awareness

Executive regulations not yet published as of 2026. Doctrine must be revisited when MCIT publishes.

## 4. KSA-specific rules

### R-KSA-1 — Data localisation default

Personal data of KSA residents stored within Saudi Arabia by default. Cross-border transfer requires SDAIA license + adequacy assessment + standard contractual clauses (or equivalent).

- Allowed regions: KSA, GCC (with case-by-case adequacy).
- Documented in `compliance/ksa-data-localisation.md`.

### R-KSA-2 — SDAIA registration

Controllers register with SDAIA's National Data Office (NDO). Track registration in `compliance/ksa-sdaia-registration.md`.

### R-KSA-3 — Breach notification within 72 hours to SDAIA

`compliance/breach-runbook-ksa.md` — SDAIA contact + escalation chain.

### R-KSA-4 — Records of Processing Activities (RoPA)

Maintain RoPA per controller. Updated per change.

### R-KSA-5 — Sensitive personal data extra protection

Special categories: health, biometric, genetic, religious, philosophical, ethnic, financial-credit. Extra consent + DPO involvement.

## 5. UAE-specific rules

### R-UAE-1 — Jurisdictional branching (free zones)

UAE Federal PDPL (Decree-Law 45/2021) **excludes**:

- Government data (federal + emirate)
- Free zone entities with their own data laws:
  - **DIFC** — Data Protection Law DIFC 5/2020
  - **ADGM** — Data Protection Regulations 2021
  - **DHCC** (Dubai Healthcare City) — own regs
- Health data (separate UAE health-data-specific regs)
- Personal banking / credit data (Central Bank-regulated)

Active sub-jurisdiction selected:

```toml
[compliance]
mena_jurisdiction = ["uae-federal", "uae-difc"]
```

`compliance/uae-jurisdiction-mapping.md` documents which entity is in which regime.

### R-UAE-2 — UAE Data Office notification

When UAE Federal PDPL applies: register processing with the UAE Data Office. Track in `compliance/uae-data-office-registration.md`.

### R-UAE-3 — DIFC-specific rules (when active)

DIFC DPL 5/2020 closely tracks GDPR. Adopt the `eu-gdpr` Doctrine on top of mena-pdpl when DIFC is active.

### R-UAE-4 — ADGM-specific rules (when active)

ADGM Data Protection Regulations 2021 also GDPR-aligned. Same advice as DIFC.

## 6. Stack guidance

### MENA-eligible cloud regions

| Provider | Region | When |
|---|---|---|
| **AWS** | `me-south-1` (Bahrain), `me-central-1` (UAE) | KSA + UAE-eligible; KSA might require local-DC partnership |
| **Azure** | `UAE North`, `Saudi Arabia Central` (per Microsoft expansion) | Native KSA / UAE residency |
| **Oracle Cloud** | `me-jeddah-1` (KSA), `me-dubai-1` (UAE) | KSA + UAE residency |
| **Google Cloud** | `me-central1` (Doha) | UAE / GCC; verify per-jurisdiction adequacy |
| **Local** | STC Cloud (KSA), Mobily Cloud, Etisalat Smart Hub | KSA / UAE local providers |

### LLM with MENA-region BAA / DPA

When LLM API touches PII subject to mena-pdpl:

- AWS Bedrock (Anthropic) in `me-south-1` / `me-central-1` — verify per-jurisdiction adequacy.
- Azure OpenAI Service in `UAE North` / `Saudi Arabia Central`.
- Self-hosted (vLLM + Llama) on local cloud — when zero-trust toward vendors.

**No PII to LLM without DPA/BAA + de-identification + no-data-retention enterprise tier.**

## 7. Verification

`bequite verify` for mena-pdpl projects:

1. **Lawful-basis documentation** present per active jurisdiction.
2. **Data subject rights endpoints** implemented + tested.
3. **Encryption at rest** column-level for PII columns.
4. **TLS 1.2+ in transit**.
5. **Cross-border transfer log** (when applicable).
6. **Breach runbook** present per jurisdiction + tabletop within last 12 months.
7. **DPO appointed** (KSA / UAE when required).
8. **Egypt DPC license** (Egypt; when required).
9. **KSA data localisation** verified in IaC.
10. **UAE jurisdiction mapping** documented.

## 8. References

- **Egypt PDPL (Law No. 151 of 2020)** — official PDF: https://mcit.gov.eg/Upcont/Documents/Reports%20and%20Documents_1232021000_Law_No_151_2020_Personal_Data_Protection.pdf · MCIT portal: https://mcit.gov.eg/
- **KSA PDPL** (SDAIA hub): https://sdaia.gov.sa/en/Research/Pages/DataProtection.aspx · DGP guide portal: https://dgp.sdaia.gov.sa/ · Royal Decree M/19 (2021) + amendment M/148 (2023); fully enforceable since 2024-09-14
- **UAE Federal PDPL** (Federal Decree-Law 45/2021): https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws · Legislation download: https://uaelegislation.gov.ae/en/legislations/1972/download
- **DIFC DPL 5/2020**: https://www.difc.ae/business/laws-regulations/legal-database/data-protection-law-difc-law-no-5-of-2020/
- **ADGM Data Protection Regulations 2021**: https://www.adgm.com/operating-in-adgm/office-of-data-protection
- IAPP MENA tracker: https://iapp.org/resources/article/middle-east-and-north-africa/

## 9. Forking guidance

Common forks:
- **`mena-pdpl-egypt-only`** — when project targets Egypt only.
- **`mena-pdpl-ksa-strict`** — adds extra rigour for SDAIA-registered processors.
- **`mena-pdpl-uae-financial`** — when UAE Central Bank credit-data rules apply on top.

## 10. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Three jurisdictions branched. Egypt's executive regs flagged as pending. UAE free-zone carve-outs documented (DIFC / ADGM / DHCC). NOT a substitute for local legal counsel.
```
