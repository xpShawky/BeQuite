---
name: fintech-pci
version: 1.0.0
applies_to: [fintech, payments, regulated]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: fintech-pci v1.0.0

> Doctrine for fintech / payments / cardholder-data-handling projects. PCI DSS controls, audit log retention, cardholder data segregation, key management, fraud monitoring. Loaded by `.bequite/bequite.config.toml::doctrines = ["fintech-pci"]`. Stack with `default-web-saas` for the application layer; this Doctrine governs the fintech-specific overlays.
>
> **Disclaimer:** this Doctrine is a *starting point* shaped by PCI DSS v4.0 (Mar 2024). It is NOT a substitute for a Qualified Security Assessor (QSA) review. Use it to guide implementation; certify with a QSA.

## 1. Scope

Applications that store, process, or transmit cardholder data (CHD) — primary account number (PAN), cardholder name, expiry, service code — or sensitive authentication data (SAD) — full track data, CAV2/CVC2/CVV2/CID, PINs/PIN blocks. Includes payment gateways, card-present terminals, e-commerce checkouts, and any system in the cardholder data environment (CDE).

**Does NOT cover:** projects that *integrate with* a tokenised payment provider (Stripe, Adyen, …) and never see CHD — those projects are NOT in PCI scope and don't need this Doctrine. Use `default-web-saas` instead.

## 2. Rules

### Rule 1 — Cardholder Data Environment (CDE) is segmented
**Kind:** `block`
**Statement:** Systems in the CDE (storing, processing, transmitting CHD) are network-segregated from non-CDE systems. Public-cloud: separate VPC / project / subscription with explicit firewall + flow logs. On-prem: separate VLAN. The segregation is documented in a network diagram inside `infra/network-diagram.md`.
**Check:** `bequite audit` checks for the diagram; lints Terraform / CloudFormation for VPC isolation patterns.
**Why:** PCI DSS Req 1.

### Rule 2 — Never store SAD post-authorisation
**Kind:** `block`
**Statement:** Sensitive Authentication Data (full track, CAV2/CVC2/CVV2/CID, PINs) is NEVER stored after authorisation, even encrypted. PreToolUse hook + `bequite audit` greps schemas + code for `cvv` / `track1` / `track2` columns/fields.
**Check:** `bequite audit` runs the SAD-grep on schemas + code; exit 2 on match.
**Why:** PCI DSS Req 3.2 (the most-violated requirement).

### Rule 3 — PAN is masked or tokenised everywhere it's not strictly needed
**Kind:** `block`
**Statement:** Wherever the full PAN is not strictly needed — UI, logs, reports, exports, emails — it is **masked** (display only first-6 + last-4) or **tokenised** (replaced with a vault-issued token). Full PAN access is logged with user + reason.
**Check:** `bequite audit` greps logs / templates / exports for unmasked PAN patterns; flags violations.
**Why:** PCI DSS Req 3.4, 3.5.

### Rule 4 — PAN at rest is encrypted with strong, ratable crypto
**Kind:** `block`
**Statement:** Stored PAN is encrypted with **AES-256** (or equivalent) using keys managed by an HSM (FIPS 140-2 Level 3 minimum) or a cloud KMS (AWS KMS / GCP Cloud KMS / Azure Key Vault). Database column-level encryption (`pgcrypto`, `mssql Always Encrypted`) preferred over disk-only encryption.
**Check:** `bequite audit` parses schemas; flags PAN-shaped columns without explicit `encrypted: true`.
**Why:** PCI DSS Req 3.5, 3.6.

### Rule 5 — Key management discipline
**Kind:** `block`
**Statement:** Key custodians are documented (named individuals). Keys rotate at least annually. Key deletion is irreversible. Master-key access requires dual control (no single person can unilaterally extract). KEK / DEK separation is enforced.
**Check:** `bequite audit` checks for `key-management.md` artifact + KMS rotation policy in IaC.
**Why:** PCI DSS Req 3.6, 3.7.

### Rule 6 — TLS 1.2+ everywhere; no SSL, no early TLS
**Kind:** `block`
**Statement:** All transmission of CHD over public networks uses TLS 1.2 or 1.3. SSL, TLS 1.0, TLS 1.1 are disabled at the edge. Internal CDE traffic is also encrypted (TLS or VPN).
**Check:** `bequite audit` checks `nginx.conf` / `caddyfile` / `terraform load_balancer` for protocol allow-list.
**Why:** PCI DSS Req 4.

### Rule 7 — Strong authentication on all CDE access
**Kind:** `block`
**Statement:** All CDE access (admin, user, API) requires **multi-factor authentication**. Service accounts use short-lived credentials (OIDC / IRSA / Workload Identity) — never long-lived API keys.
**Check:** `bequite audit` reviews IAM policies; flags long-lived keys + non-MFA-required policies.
**Why:** PCI DSS Req 8.

### Rule 8 — Audit log retention: 1 year minimum, 3 months readily accessible
**Kind:** `block`
**Statement:** Audit logs of CDE access (who, what, when, success/fail) retained for **at least 1 year**, with **at least 3 months immediately searchable**. Stored in a tamper-evident way (write-once / append-only / cryptographically chained).
**Check:** `bequite audit` checks log retention config in CloudTrail / GCP Audit / Azure Monitor / self-hosted SIEM.
**Why:** PCI DSS Req 10.

### Rule 9 — File integrity monitoring on critical files
**Kind:** `block`
**Statement:** File integrity monitoring (FIM) on system binaries, config files, and CDE application code. Tools: AIDE, Tripwire, Wazuh, Falco. Alerts on unauthorised change.
**Check:** `bequite audit` checks for FIM IaC / playbooks.
**Why:** PCI DSS Req 11.5.

### Rule 10 — Quarterly external + annual penetration testing
**Kind:** `block`
**Statement:** Quarterly external vulnerability scans by an Approved Scanning Vendor (ASV). Annual penetration testing (network + application) by qualified personnel.
**Check:** `bequite audit` checks for the artifact `compliance/ASV-scan-<YYYY-Q>.pdf` and `compliance/pentest-<YYYY>.pdf`. Doesn't run them; just confirms they exist.
**Why:** PCI DSS Req 11.

### Rule 11 — Incident response plan tested annually
**Kind:** `block`
**Statement:** Documented incident response plan (`SECURITY.md::incident-response`). Tabletop exercise at least annually; results recorded.
**Check:** `bequite audit` checks for the plan + a tabletop log.
**Why:** PCI DSS Req 12.10.

### Rule 12 — All third-party services have signed BAAs / DPAs
**Kind:** `block`
**Statement:** Any third-party that touches CHD has a signed contract documenting their PCI compliance + their responsibilities. Listed in `compliance/third-parties.md`.
**Check:** `bequite audit` checks for the file + an entry per service in `techContext.md::external-services`.
**Why:** PCI DSS Req 12.8.

### Rule 13 — No CHD in non-prod environments
**Kind:** `block`
**Statement:** Development, staging, QA environments use synthetic / tokenised data. Real CHD never reaches non-prod. Test card numbers from card networks (Visa 4111-1111-1111-1111, etc.) only.
**Check:** `bequite audit` greps test data for real-PAN regex; flags violations.
**Why:** PCI DSS Req 6.4.3 + the "we leaked CHD via the staging DB backup" classic.

### Rule 14 — Code review on every CHD-touching commit
**Kind:** `block`
**Statement:** Every commit that touches CHD-handling code requires a separate reviewer (not the author). The review log is preserved.
**Check:** GitHub branch protection on `main`; required-reviewer count ≥ 1; CODEOWNERS file specifies CDE paths.
**Why:** PCI DSS Req 6.5.

## 3. Stack guidance

### Tokenisation vendor (preferred over building your own)
| Choice | When |
|---|---|
| **Stripe** | E-commerce / SaaS payments (Stripe Vault) — keeps you out of PCI scope |
| **Adyen** | Global enterprise (multi-acquirer, multi-currency) |
| **Spreedly** | When you need multiple acquirer relationships |
| **Very Good Security (VGS)** | When you need vault but not gateway |
| **Skyflow** | Privacy-focused tokenisation API |

If you can use a tokenisation vendor, **DO** — it removes most of your CDE.

### Database (when you must store PAN)
- **Postgres** with `pgcrypto` for column-level AES-256.
- **AWS RDS / GCP Cloud SQL / Azure Database** with KMS-managed CMK + TDE.
- **HSM-backed key custody** (AWS CloudHSM, Azure Dedicated HSM) for the most regulated environments.

### KMS / HSM
| Choice | When |
|---|---|
| AWS KMS | Default on AWS (CMK with key rotation) |
| GCP Cloud KMS | Default on GCP |
| Azure Key Vault | Default on Azure |
| AWS CloudHSM / Azure Dedicated HSM | When FIPS 140-2 L3 is mandated |
| Thales / Entrust | On-prem |

### SIEM / log retention
- **Datadog** / **Splunk** / **Sumo Logic** / **Elastic Security**.
- **CloudTrail** + S3 Object Lock + Glacier for AWS.

### Fraud monitoring
- Stripe Radar (when on Stripe).
- Sift / Riskified / Forter.
- Custom rules engine (lower priority unless you have specific needs).

## 4. Verification

`bequite verify` for fintech-pci projects (in addition to `default-web-saas` walks):

1. **PAN-in-logs scan** — full repository + last 90 days of log archives; PAN-shaped strings flagged.
2. **TLS configuration audit** — `testssl.sh` or `qualys-ssl-labs` against every public endpoint; assert TLS 1.2+ only.
3. **MFA enforcement** — assert all admin / API service accounts require MFA / use short-lived OIDC.
4. **Encryption-at-rest verification** — query the database directly with no application; assert PAN columns return ciphertext, not plaintext.
5. **Audit log search** — assert "user X accessed PAN Y at time T" is searchable for the last 90 days.
6. **Compliance artifact presence** — ASV scan, pentest, IR-plan tabletop, BAAs.

## 5. Examples and references

- PCI DSS v4.0: https://www.pcisecuritystandards.org/document_library/?category=pcidss
- PCI DSS QSA list: https://www.pcisecuritystandards.org/assessors_and_solutions/qualified_security_assessors
- Stripe + PCI scope: https://stripe.com/guides/pci-compliance
- Skyflow tokenisation: https://www.skyflow.com/
- Datadog PCI compliance: https://www.datadoghq.com/security/

## 6. Forking guidance

Common forks:
- **`fintech-pci-saq-a`** — for SAQ-A merchants (e-commerce with full outsourcing); relax requirements that are vendor's responsibility.
- **`fintech-pci-saq-d`** — for full SAQ-D merchants (storing CHD on-premise); add custom rules.
- **`fintech-psd2-eu`** — overlay for European PSD2 / Strong Customer Authentication / Open Banking.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: fintech-pci@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–14 ratified. Reflects PCI DSS v4.0 (Mar 2024). NOT a substitute for QSA review.
```
