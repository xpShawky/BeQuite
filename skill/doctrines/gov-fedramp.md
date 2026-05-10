---
name: gov-fedramp
version: 1.0.0
applies_to: [government, fedramp, regulated, public-sector]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: gov-fedramp v1.0.0

> Doctrine for cloud services serving U.S. federal government customers. FedRAMP control families, FIPS-validated crypto, NIST 800-53 alignment, FedRAMP authorisation path. Loaded by `.bequite/bequite.config.toml::doctrines = ["gov-fedramp"]`. Stack with `default-web-saas` for the application layer; this Doctrine governs the federal-specific overlays.
>
> **Disclaimer:** this Doctrine is a starting point shaped by FedRAMP Rev 5 (Mar 2024+) baseline controls. It is NOT a substitute for a FedRAMP 3PAO assessment or your agency's authorising official. Use it to guide implementation; certify with a qualified 3PAO.

## 1. Scope

Cloud services (IaaS / PaaS / SaaS) seeking FedRAMP Authorisation (Low / Moderate / High impact level) to serve U.S. federal agencies. Aligned to NIST SP 800-53 Rev 5 control catalog as the baseline.

**Does NOT cover:** non-federal U.S. government (state / local — see CJIS for law enforcement), non-U.S. government (UK Cyber Essentials, EU Cloud Code of Conduct, IRAP for Australia). Future Doctrines for those.

## 2. Rules

### Rule 1 — Determine and document FedRAMP impact level early
**Kind:** `block`
**Statement:** Document the impact level (Low / Moderate / High) at `compliance/fedramp-impact-level.md` based on FIPS 199 categorisation across confidentiality, integrity, availability. Drives every other control decision.
**Check:** `bequite audit` checks for the file + a FIPS 199 categorisation matrix.
**Why:** the rest of the controls scale with impact level; getting this wrong wastes months.

### Rule 2 — System Security Plan (SSP) maintained
**Kind:** `block`
**Statement:** A System Security Plan exists at `compliance/ssp.md` (or in OSCAL format at `compliance/oscal/ssp.json`), documenting how each NIST 800-53 control is implemented. Updated within 30 days of any significant change.
**Check:** `bequite audit` checks for the SSP + a "last updated" timestamp < 90 days for active development.
**Why:** the central artifact for FedRAMP authorisation.

### Rule 3 — FIPS 140-2 / 140-3 validated crypto for everything sensitive
**Kind:** `block`
**Statement:** All cryptographic modules (TLS, at-rest encryption, signing, hashing) are FIPS 140-2 (140-3 when available) **validated** — not merely "compliant." Validation certificate numbers recorded in `compliance/crypto-modules.md`.
**Check:** `bequite audit` parses crypto library imports; cross-references against the NIST CMVP validated modules list.
**Why:** FedRAMP control SC-13 + the difference between "FIPS-compliant" (claim) and "FIPS-validated" (NIST-certified) is the single most-confused FedRAMP point.

### Rule 4 — TLS 1.2+ with FIPS-approved cipher suites only
**Kind:** `block`
**Statement:** All transmission uses TLS 1.2 or 1.3 with FIPS-approved cipher suites (e.g., TLS_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384). SSL, TLS 1.0/1.1, and non-FIPS suites disabled.
**Check:** `bequite audit` audits edge config; cross-references suite list against FIPS approval.
**Why:** SC-8, SC-13.

### Rule 5 — MFA on every privileged action
**Kind:** `block`
**Statement:** All privileged actions (admin login, configuration change, secret access, key rotation) require multi-factor authentication using a FIPS-validated authenticator (PIV, FIDO2 with FIPS-validated module, or NIST 800-63B AAL2+).
**Check:** `bequite audit` reviews IAM policies + authenticator configuration.
**Why:** IA-2(1), IA-2(2), IA-2(11), IA-2(12).

### Rule 6 — Continuous monitoring (ConMon)
**Kind:** `block`
**Statement:** Continuous monitoring program in place: monthly vulnerability scans, monthly POA&M (Plan of Action and Milestones) updates, annual assessments. Reports stored at `compliance/conmon/<YYYY-MM>/`.
**Check:** `bequite audit` checks for the latest monthly scan + POA&M update.
**Why:** CA-7, FedRAMP ConMon Strategy Guide.

### Rule 7 — Incident response within FedRAMP / US-CERT timelines
**Kind:** `block`
**Statement:** Incident response plan documented (`compliance/incident-response.md`). Incidents reported to US-CERT and the FedRAMP PMO within required timelines (1 hour for high-impact, varying for lower). Tabletop exercise at least annually.
**Check:** `bequite audit` checks for the IR plan + tabletop log.
**Why:** IR-4, IR-6, IR-8, FedRAMP Incident Communications Procedure.

### Rule 8 — Audit logs: immutable, retained, time-synced
**Kind:** `block`
**Statement:** Audit logs are immutable (append-only or write-once), retained for **at least 1 year** (longer for High impact), with time synced to authoritative NTP source. Captured events meet AU-2 baseline.
**Check:** `bequite audit` checks log retention + NTP config.
**Why:** AU-2, AU-3, AU-8, AU-11.

### Rule 9 — Configuration management + baseline configuration
**Kind:** `block`
**Statement:** Baseline configurations documented for every system component (`compliance/baseline-configs/`). Changes follow CM-3 change control. Unauthorised changes detected via FIM (Wazuh / Tripwire / AIDE).
**Check:** `bequite audit` checks for baselines + FIM IaC.
**Why:** CM-2, CM-3, CM-6, CM-7.

### Rule 10 — Personnel screening + access reviews
**Kind:** `block`
**Statement:** Workforce members with access to FedRAMP-authorised systems are screened to a level appropriate to the impact tier. Access is reviewed at least quarterly; terminated personnel access is removed within 24 hours.
**Check:** `bequite audit` checks for the personnel-screening artifact + access-review log.
**Why:** PS-3, PS-4, PS-5, AC-2.

### Rule 11 — Supply chain risk management (SCRM)
**Kind:** `block`
**Statement:** Software Bill of Materials (SBOM) generated and maintained. Third-party components reviewed for SCRM risks. Suppliers with significant access have CIS-aligned supply-chain assessments.
**Check:** `bequite audit` checks for SBOM (CycloneDX or SPDX) + SCRM artifact.
**Why:** SR-1 through SR-12 (NIST 800-53 Rev 5 added the SR family).

### Rule 12 — U.S.-only data residency (when required by impact level / agency)
**Kind:** `block`
**Statement:** For Moderate / High and any agency-required Low, all data + replicas + backups stored within the United States. Cloud regions / availability zones documented + verified.
**Check:** `bequite audit` parses IaC for region constraints.
**Why:** common agency requirement.

### Rule 13 — Personnel: U.S. citizens / persons + screening (when required)
**Kind:** `block`
**Statement:** For controlled-information environments (Moderate+ for some agencies), workforce with system access are U.S. persons (or specifically authorised). Screening status tracked.
**Check:** advisory; agency-specific.
**Why:** common agency-imposed constraint.

### Rule 14 — Plan of Action and Milestones (POA&M) discipline
**Kind:** `block`
**Statement:** Every identified weakness recorded in the POA&M with: ID, finding, severity, mitigation plan, owner, scheduled completion date. Updated monthly.
**Check:** `bequite audit` checks for the POA&M; flags items past due.
**Why:** CA-5; the most-watched FedRAMP artifact during ConMon.

### Rule 15 — Boundary documentation
**Kind:** `block`
**Statement:** Authorisation Boundary diagram exists at `compliance/authorization-boundary.md`. Shows every component "in scope" + every interconnection to "out of scope" systems with a justified Interconnection Security Agreement (ISA).
**Check:** `bequite audit` checks for the boundary doc + ISA artifacts per external interconnection.
**Why:** the FedRAMP boundary is the single biggest scoping decision; AC-20, CA-3.

## 3. Stack guidance

### FedRAMP-authorised cloud regions
| Choice | When |
|---|---|
| AWS GovCloud (US) | High and many Moderate workloads |
| AWS US-East/West (with FedRAMP) | Lower Moderate / Low |
| Azure Government | Microsoft federal stack |
| GCP Assured Workloads (US) | Google federal stack |
| Oracle Government Cloud | Oracle federal |

**Note:** FedRAMP authorisation is per-service-region; verify each component on the FedRAMP Marketplace.

### LLM with FedRAMP authorisation
| Choice | Status |
|---|---|
| Anthropic via AWS Bedrock (GovCloud) | Verify authorisation in current FedRAMP Marketplace |
| Azure OpenAI Government | Verify current authorisation |
| Self-hosted (Llama on GovCloud) | Always an option for High |

### KMS / HSM
| Choice | When |
|---|---|
| AWS KMS in GovCloud | FIPS 140-2 L2; default |
| AWS CloudHSM Classic | FIPS 140-2 L3 when required |
| Azure Dedicated HSM (Government) | Azure stack |

### SIEM + ConMon
- **Splunk** (FedRAMP authorised SaaS): https://www.splunk.com/en_us/partners/government/fedramp.html
- **Trellix XDR / IBM QRadar / Microsoft Sentinel (gov)** — common enterprise SIEMs.
- **Tenable.io / Qualys** for vulnerability scanning (FedRAMP authorised).

## 4. Verification

`bequite verify` for gov-fedramp projects (in addition to `default-web-saas`):

1. **FIPS-validated crypto check** — every crypto library import validated against NIST CMVP list.
2. **TLS suite audit** — every public endpoint serves only FIPS-approved cipher suites.
3. **Boundary verification** — components in code match the authorisation boundary diagram.
4. **POA&M staleness check** — open POA&M items older than scheduled completion date flagged.
5. **Region pin** — IaC region constraints verified to be U.S. (or GovCloud) only.
6. **Audit log immutability** — sample-tamper test of log storage.
7. **SSP freshness** — last update within 90 days during active development.

## 5. Examples and references

- FedRAMP Marketplace: https://marketplace.fedramp.gov/
- FedRAMP Rev 5 Baselines: https://www.fedramp.gov/baselines/
- NIST SP 800-53 Rev 5: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- NIST SP 800-63B Digital Identity: https://pages.nist.gov/800-63-3/sp800-63b.html
- NIST CMVP (FIPS 140 validated modules): https://csrc.nist.gov/projects/cryptographic-module-validation-program
- FIPS 199 (Categorisation): https://csrc.nist.gov/publications/detail/fips/199/final
- AWS GovCloud: https://aws.amazon.com/govcloud-us/
- Azure Government: https://azure.microsoft.com/en-us/global-infrastructure/government/
- OSCAL (machine-readable security plans): https://pages.nist.gov/OSCAL/

## 6. Forking guidance

Common forks:
- **`gov-cjis`** — Criminal Justice Information Services (FBI CJIS Security Policy) for law enforcement.
- **`gov-il5`** — DoD Impact Level 5 (Controlled Unclassified Information / Mission Critical).
- **`gov-il6`** — DoD Impact Level 6 (Classified up to Secret).
- **`gov-uk-essentials`** — UK Cyber Essentials Plus.
- **`gov-eu-c5`** — EU Cloud Code of Conduct / German C5.
- **`gov-au-irap`** — Australian IRAP / PROTECTED.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: gov-fedramp@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–15 ratified. Reflects FedRAMP Rev 5 (Mar 2024+) and NIST 800-53 Rev 5. NOT a substitute for 3PAO assessment.
```
