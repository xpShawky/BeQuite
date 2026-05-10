# Rules of Engagement — ROE-<id>

> Article IX (Constitution v1.2.0) requires this document for any work that touches a system you do not own and operate. Modeled on PTES (Penetration Testing Execution Standard) + NIST SP 800-115 + standard bug-bounty contract clauses. The hook (`pretooluse-pentest-authorization.sh`) checks for the existence + minimum-viable-content of this file before allowing any non-defensive tool to run.
>
> Variants:
> - `ROE-<id>.md` — standard external pentest with signed customer contract or bug-bounty program rules.
> - `RoE-RT-<id>.md` — internal red-team engagement (8-guardrail carve-out per Article IX).
> - `RoE-self-<id>.md` — defensive validation against own systems (e.g. verify a CVE patch fixed the issue).
> - `RoE-CTF-<id>.md` — academic / lab CTF (DVWA, HackTheBox, TryHackMe, OWASP Juice Shop).

```
---
roe_id: ROE-<id>
status: active            # active | expired | superseded
type: standard            # standard | RT | self | CTF
created_at: <ISO 8601>
expires_at: <ISO 8601>
---
```

## 1. Authorization source

Pick exactly one (multiple → confused; split into separate ROEs):

- [ ] **Self-owned** — operator owns 100% of every target asset listed in §2.
- [ ] **Customer-signed contract** — attach: contract name, signature date, signatory, link/path.
- [ ] **Bug-bounty program** — name, URL, program rules link, your researcher handle.
- [ ] **Academic CTF / lab** — name, URL.

## 2. Targets in scope

Exact list. No globs without explicit allowlist.

- **Domains**: `<list>`
- **IP ranges**: `<list>`
- **Repositories**: `<list>`
- **Accounts**: `<list>`
- **Cloud accounts**: `<list>`
- **Mobile apps** (when applicable): `<list>`
- **APIs** (when applicable): `<list>`

## 3. Targets out of scope

Everything else. Explicit list of subdomains, third-party deps, production payment systems, etc. that must NOT be touched. When in doubt, list it here.

- `<list>`

## 4. Time window

- **Start (UTC)**: `<ISO 8601>`
- **End (UTC)**: `<ISO 8601>`
- **Maintenance windows** (do NOT test during): `<list>`

## 5. Allowed actions

- [ ] Passive recon (DNS, certs, public OSINT)
- [ ] Active recon (port scan, content discovery, fingerprinting)
- [ ] DAST scanning (Nuclei templates / ZAP active scan)
- [ ] Web app fuzzing
- [ ] Authentication brute force (only against explicitly listed services in §2)
- [ ] Exploit PoC execution (only against explicitly listed CVEs / services)
- [ ] Post-exploitation (only with explicit approval; specify boundaries)
- [ ] Social engineering (almost always FORBIDDEN — explicit yes required)
- [ ] Physical security testing (rarely; legal complications)

## 6. Forbidden actions

- DoS / volumetric / disruptive testing of any kind
- Actions that destroy or modify production data
- Movement outside scope (lateral pivot, pivot to systems not in §2)
- Anything that would violate local law in operator's or target's jurisdiction
- Distribution / publication of exploit code outside this engagement
- Storing target data anywhere except `<designated location>`
- Communication with target users / customers without explicit authorization

## 7. Coordinated disclosure

- **Vendor contact**: `<email/PGP>`
- **Disclosure framework**: project-zero-90d | cert-cc | mitre-cna | fda | ics-cert | ncsc | other
- **Disclosure SLA**: `<days>`
- **Extension policy**: `<conditions for extension>`
- **CVE assignment**: yes / no, who files

## 8. Data handling

- **What gets stored**: `<findings, screenshots, never raw user data>`
- **Where**: `<encrypted location with access controls>`
- **For how long**: `<retention period; default 90d audit window>`
- **Who has access**: `<named individuals>`
- **Destruction at end**: `<cryptographic shred / overwrite procedure>`

## 9. Reporting

- **Format**: `<template path>`
- **Cadence**: daily / weekly / end-of-engagement
- **Recipient**: `<name/email>`
- **Distribution restrictions**: `<who else may receive copies>`

## 10. Sign-off

- **Operator**: `<name, date, signature/PGP>`
- **Authoriser**: `<name, date, signature/PGP>`
- (For RoE-RT) **Red-team lead**: `<name, date, signature>`
- (For RoE-RT) **Blue-team lead**: `<name, date, signature>`

## 11. Linked artifacts

- Spec: `<link>`
- Plan: `<link>`
- Tasks: `<link>`
- Findings: `<link to findings/ directory>`
- Receipt(s): `<link to .bequite/receipts/>`

---

## RoE-RT additions (internal red-team only — 8 hard guardrails per Article IX)

If `type: RT`, the following 8 acknowledgments are MANDATORY. Hook checks all 8.

### Guardrail 1 — Dual sign-off

Both red-team-lead AND blue-team-lead must sign §10. Single sign-off invalid.

### Guardrail 2 — Target scope = corporate-owned only

§2 must list ONLY corporate-owned IP ranges + accounts. Any external IP listed → not eligible for RT carve-out.

### Guardrail 3 — Compile-time callback URL assertion

Custom artifact (C2 / implant / payload) source code must contain an assertion:

```python
# Or equivalent in Go / Rust / C / etc.
assert callback_url_resolves_to_corporate_internal_ip_range(C2_URL), \
    "C2 URL not in corporate-internal range; refusing to build"
```

Document the corporate-internal IP range here:

- `<10.0.0.0/8 | 172.16.0.0/12 | 192.168.0.0/16 | <internal-DNS-suffix>>`

### Guardrail 4 — engagement_id + expiry_timestamp hard-coded

Artifact source must include:

```python
ENGAGEMENT_ID = "<roe_id>"
EXPIRY_TIMESTAMP = "<ISO 8601>"   # same as §4 End

if datetime.utcnow() > parse_iso(EXPIRY_TIMESTAMP):
    raise RuntimeError(f"Engagement {ENGAGEMENT_ID} expired; refusing to run")
```

### Guardrail 5 — Private repo with branch protection

- Repo URL: `<private-repo>`
- Branch protection on `main`: required-reviewers ≥ 2, no force-push, no direct pushes
- Confirmed: `<date, name>`

### Guardrail 6 — Sandboxed build; no internet egress to non-corp IPs

- Build environment: `<isolated-VM | container | air-gapped-machine>`
- Egress allowlist: corporate-internal only
- Confirmed: `<date, name>`

### Guardrail 7 — Post-engagement: cryptographic shred + ≤90d audit retention

- Source destruction method: `<shred -uvz / cryptographic-erase>`
- Binaries collection location: `<encrypted-vault>`
- Audit retention: ≤ 90 days
- Destruction date: `<scheduled date; populated post-engagement>`

### Guardrail 8 — No reuse across engagements

- This artifact is single-use for this engagement.
- New engagement → new RoE-RT + new build.
- Reuse → forbidden; constitutes new artifact and new RoE.

---

## RoE-self additions (defensive validation only)

If `type: self`, this is for verifying your own patches against your own systems.

- **CVE id being verified**: `<CVE-YYYY-NNNNN>`
- **Patched system**: `<which system; must match §2 scope>`
- **Validation method**: run public PoC; confirm patched version no longer vulnerable; revert; confirm un-patched version IS vulnerable; produce evidence.
- **Non-deployment statement**: I confirm this PoC will NOT be deployed against any system not in §2. (Required exact phrase.)
- **Disclosure**: not applicable for self-validation; CVE already public.

---

## RoE-CTF additions

If `type: CTF`, this is for academic / lab use.

- **Lab name**: DVWA | OWASP Juice Shop | HackTheBox | TryHackMe | VulnHub | other
- **Lab URL or local install**: `<link>`
- **Active machine / challenge**: `<name>`
- **In-scope per lab rules**: confirmed `<date, source-link>`
