---
name: healthcare-hipaa
version: 1.0.0
applies_to: [healthcare, hipaa, regulated, phi]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: healthcare-hipaa v1.0.0

> Doctrine for healthcare projects subject to HIPAA. PHI handling, BAAs, audit trail, breach notification, minimum-necessary access. Loaded by `.bequite/bequite.config.toml::doctrines = ["healthcare-hipaa"]`. Stack with `default-web-saas` for the application layer; this Doctrine governs the PHI-specific overlays.
>
> **Disclaimer:** this Doctrine is a starting point shaped by HIPAA Security Rule (45 CFR Parts 160 + 164) and the HHS HIPAA Privacy Rule. It is NOT a substitute for legal counsel or a HIPAA Security Officer review. Use it to guide implementation; certify with qualified counsel.

## 1. Scope

Applications that create, receive, maintain, or transmit Protected Health Information (PHI) on behalf of a Covered Entity or Business Associate. Includes Electronic Health Records (EHR), telehealth platforms, patient portals, clinical decision support, billing systems, and any system that processes individually identifiable health information.

**Does NOT cover:** projects that handle de-identified data only (per 45 CFR §164.514(b) Safe Harbor) — these are NOT HIPAA-regulated. Use `default-web-saas`. Projects that integrate with EHR vendors (Epic / Cerner / Athena) without storing PHI directly may need only a subset; review with QSO.

## 2. Rules

### Rule 1 — PHI inventory + data flow diagram
**Kind:** `block`
**Statement:** A complete inventory of every system component that handles PHI exists at `compliance/phi-inventory.md`, with a data-flow diagram at `compliance/data-flow.md`. Updated whenever a new component is added.
**Check:** `bequite audit` checks for both files; `bequite freshness` flags components in code that aren't listed.
**Why:** HIPAA Security Rule §164.308(a)(1)(ii)(A) — risk analysis is impossible without knowing where PHI lives.

### Rule 2 — Encrypt PHI at rest with FIPS-validated crypto
**Kind:** `block`
**Statement:** PHI at rest is encrypted with **AES-256** using FIPS 140-2 (or 140-3 when available) validated modules. Database column-level encryption preferred over disk-only. Backups encrypted with separate keys.
**Check:** `bequite audit` parses schemas + IaC; flags PHI-shaped columns without explicit encryption + flags non-FIPS crypto libraries.
**Why:** HIPAA Security Rule §164.312(a)(2)(iv).

### Rule 3 — Encrypt PHI in transit (TLS 1.2+, no SSL/TLS 1.0/1.1)
**Kind:** `block`
**Statement:** All PHI transmission uses TLS 1.2 or 1.3. SSL, TLS 1.0, TLS 1.1 disabled. Internal service-to-service traffic also encrypted (TLS or VPN). No plaintext PHI in logs, message queues, or notifications.
**Check:** `bequite audit` checks edge config + scans logs for PHI patterns.
**Why:** HIPAA Security Rule §164.312(e)(1).

### Rule 4 — Unique user IDs + automatic logoff + emergency access
**Kind:** `block`
**Statement:** Every workforce member has a unique account (no shared logins). Sessions automatically log off after a documented inactivity window (default: 15 minutes for clinical apps, 30 minutes for back-office). An "emergency access" procedure exists, documented in `compliance/emergency-access.md`.
**Check:** `bequite audit` reviews session config + checks for the emergency-access doc.
**Why:** HIPAA Security Rule §164.312(a)(2)(i)–(iii).

### Rule 5 — Audit controls (who, what, when on every PHI touch)
**Kind:** `block`
**Statement:** Every PHI access (read, write, export, delete) is logged with: user-id, timestamp, action, record-id, source-IP, application context. Logs are tamper-evident (write-once / append-only / cryptographically chained), retained for **at least 6 years**, and reviewed regularly per a documented schedule.
**Check:** `bequite audit` checks log retention IaC + the review-schedule artifact.
**Why:** HIPAA Security Rule §164.312(b) + §164.530(j) (6-year retention).

### Rule 6 — Minimum necessary access
**Kind:** `block`
**Statement:** Access controls enforce the minimum necessary rule — users see only the PHI required for their role. Patient-record access is logged; "break-the-glass" emergency access is logged separately and reviewed within 24 hours.
**Check:** `bequite audit` parses RLS / RBAC policies; flags wildcard PHI-table access for non-clinician roles.
**Why:** HIPAA Privacy Rule §164.502(b).

### Rule 7 — BAAs with every Business Associate
**Kind:** `block`
**Statement:** Any third party that creates / receives / maintains / transmits PHI on the Covered Entity's behalf has a signed Business Associate Agreement. Listed in `compliance/business-associates.md` with: name, services provided, BAA effective date, BAA expiration / renewal date.
**Check:** `bequite audit` cross-references `techContext.md::external-services` against `compliance/business-associates.md`; flags missing BAAs.
**Why:** HIPAA §164.502(e), §164.504(e).

### Rule 8 — De-identification before analytics / training
**Kind:** `block`
**Statement:** Data exported for analytics, ML training, or research is de-identified per 45 CFR §164.514(b) — either Safe Harbor (remove 18 specific identifiers) or Expert Determination. The de-identification method is recorded in `compliance/deidentification.md` with the reviewer's credentials.
**Check:** `bequite audit` scans export pipelines; flags exports without a documented de-identification step.
**Why:** HIPAA Privacy Rule.

### Rule 9 — Breach notification readiness
**Kind:** `block`
**Statement:** A breach notification runbook exists at `compliance/breach-runbook.md`. Identifies: detection triggers, internal escalation chain, breach-risk-assessment template, individual / HHS / media notification thresholds (≥500 individuals = HHS + media within 60 days), tabletop exercise log.
**Check:** `bequite audit` checks for the runbook + last tabletop date < 12 months.
**Why:** HIPAA Breach Notification Rule §164.404–408.

### Rule 10 — Workstation / device security
**Kind:** `block`
**Statement:** Workforce devices that access PHI are inventoried, encrypted (full-disk), MDM-managed, and have remote-wipe capability. BYOD policies require equivalent controls. Device loss has a documented procedure.
**Check:** `bequite audit` checks for `compliance/device-policy.md` + asset inventory artifact.
**Why:** HIPAA Security Rule §164.310(c)–(d).

### Rule 11 — Workforce training
**Kind:** `block`
**Statement:** All workforce members complete HIPAA training before PHI access; refresh annually. Training completion logged in `compliance/training-log.md` (or an equivalent system; reference required).
**Check:** `bequite audit` checks for the training-log reference.
**Why:** HIPAA Security Rule §164.308(a)(5).

### Rule 12 — Risk analysis + management
**Kind:** `block`
**Statement:** A documented risk analysis (`compliance/risk-analysis-<YYYY>.md`) is performed at least annually and after material changes. Risks are tracked in a register; mitigations have owners + due dates.
**Check:** `bequite audit` checks for the latest risk-analysis artifact (< 12 months).
**Why:** HIPAA Security Rule §164.308(a)(1).

### Rule 13 — Patient rights (access, amendment, accounting of disclosures)
**Kind:** `block`
**Statement:** The application supports patient requests to: access their PHI (within 30 days), request amendment, receive an accounting of disclosures (last 6 years), restrict disclosures. Procedures documented in `compliance/patient-rights.md`.
**Check:** `bequite audit` checks for the doc + the API endpoints implementing each right.
**Why:** HIPAA Privacy Rule §164.524–528.

### Rule 14 — No PHI in non-prod environments
**Kind:** `block`
**Statement:** Development, staging, QA environments use synthetic / de-identified data. Real PHI never reaches non-prod. Test data generated via tools like Synthea, Faker, or vendor-provided sandboxes.
**Check:** `bequite audit` scans non-prod data-loaders for real-PHI shape patterns; flags violations.
**Why:** breach-by-staging-DB-leak is a HIPAA classic.

### Rule 15 — No PHI in AI training without explicit DPIA + de-identification
**Kind:** `block`
**Statement:** PHI may not be sent to LLM APIs (Anthropic, OpenAI, Google, etc.) for training, fine-tuning, or even inference unless: (a) the vendor has signed a BAA, AND (b) a DPIA documents the data flow, AND (c) the data is de-identified to Safe Harbor standard before transmission, AND (d) `enterprise-grade` API tier with no-data-retention is used.
**Check:** `bequite audit` parses LLM API call sites; flags PHI-shaped payloads without de-id or BAA-vendor pinning.
**Why:** AI-and-PHI is the #1 emerging HIPAA risk in 2026; OWASP LLM Top 10 (LLM07 system prompt leakage, LLM09 misinformation).

## 3. Stack guidance

### EHR / clinical data integration
| Choice | When |
|---|---|
| Epic FHIR / Cerner FHIR / Athena | When integrating with major EHR vendors |
| Redox / Particle Health / Health Gorilla | Multi-EHR aggregator |
| Direct HL7 v2 / FHIR R4 / CCDA | When needed by partners |
| OpenEMR / OpenMRS | Self-hosted EHR |

### HIPAA-eligible cloud
| Choice | When |
|---|---|
| AWS (with BAA) | Default; BAA available; HIPAA-eligible service list |
| GCP (with BAA) | Google Cloud HIPAA |
| Azure (with BAA) | Microsoft Cloud HIPAA |
| Aptible / Datica / TrueVault | Pre-built HIPAA-compliant platforms |

### LLM with BAA (when AI on PHI is required)
| Choice | When |
|---|---|
| Anthropic via AWS Bedrock with BAA | HIPAA-eligible; check current eligibility list |
| Azure OpenAI Service with BAA | HIPAA-eligible |
| Google Cloud Vertex AI with BAA | HIPAA-eligible |
| Self-hosted (vLLM + Llama) | When zero-trust toward vendors |

**Without a BAA, no PHI to the LLM, period.**

### KMS / HSM
| Choice | When |
|---|---|
| AWS KMS (FIPS 140-2 L2) | Default on AWS |
| AWS CloudHSM (FIPS 140-2 L3) | When mandated |
| GCP Cloud KMS / Azure Key Vault | Default on respective clouds |

### SIEM + audit
- **Datadog** / **Splunk** / **Sumo Logic** with HIPAA add-ons.
- **CloudTrail** + S3 Object Lock for AWS.
- **Wazuh** for self-hosted FIM + SIEM.

## 4. Verification

`bequite verify` for healthcare-hipaa projects (in addition to `default-web-saas`):

1. **PHI-in-logs scan** — full repository + last 90 days of log archives; PHI-shaped strings flagged.
2. **PHI-in-non-prod scan** — non-prod data-loaders inspected for real-PHI patterns.
3. **TLS configuration audit** — every public endpoint TLS 1.2+ only.
4. **Encryption-at-rest verification** — sample PHI columns return ciphertext.
5. **Audit log search** — assert "user X accessed PHI for patient Y at time T" is searchable for 90+ days.
6. **De-identification round-trip** — sample record run through the de-id pipeline; assert all 18 Safe Harbor identifiers removed.
7. **BAA inventory completeness** — every external service in `techContext.md` has an entry in `business-associates.md`.
8. **Patient rights endpoints** — automated tests for access / amendment / accounting / restriction APIs.

## 5. Examples and references

- HIPAA Security Rule (45 CFR §164.300+): https://www.hhs.gov/hipaa/for-professionals/security/index.html
- HIPAA Privacy Rule (45 CFR §164.500+): https://www.hhs.gov/hipaa/for-professionals/privacy/index.html
- HIPAA-eligible AWS services: https://aws.amazon.com/compliance/hipaa-eligible-services-reference/
- HIPAA-eligible GCP services: https://cloud.google.com/security/compliance/hipaa
- Synthea (synthetic patient data): https://synthea.mitre.org/
- Aptible (HIPAA platform): https://www.aptible.com/
- HHS Wall of Shame (recent breach reports): https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf

## 6. Forking guidance

Common forks:
- **`healthcare-hipaa-eu-gdpr`** — overlay GDPR (Article 9 special-category data) on top of HIPAA.
- **`healthcare-hipaa-fda-saamd`** — for Software as a Medical Device (FDA Class I/II).
- **`healthcare-hipaa-research`** — IRB-supervised research with HIPAA waiver.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: healthcare-hipaa@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–15 ratified. Reflects HIPAA Security + Privacy + Breach Notification Rules (current as of May 2026). NOT a substitute for legal counsel.
```
