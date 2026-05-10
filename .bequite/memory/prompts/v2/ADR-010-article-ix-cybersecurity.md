---
adr_id: ADR-010-article-ix-cybersecurity
title: Article IX added — cybersecurity & authorized-testing discipline; Constitution v1.1.0 → v1.2.0
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
superseded_by: null
constitution_version: 1.1.0   # decided UNDER 1.1.0; output is 1.2.0
related_articles: [IX]
related_doctrines: [vibe-defense, mena-pdpl, eu-gdpr, fintech-pci, healthcare-hipaa, gov-fedramp]
---

# ADR-010: Article IX added — cybersecurity & authorized-testing discipline

> Status: **accepted** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

The Veracode 2025 GenAI Code Security Report found ~45% of AI-generated code samples contain OWASP Top-10 issues (XSS 86% fail rate, log injection 88%, Java 72% fail). The PhantomRaven supply-chain attack (Koi Security, Aug-Oct 2025) shipped 126 malicious npm packages exploiting AI-hallucinated names. AI vibe-coding's primary failure mode is producing insecure-by-default code; AI agents asked to "make it secure" frequently misunderstand the threat model and ship things worse.

BeQuite already has Article IV (Security & destruction discipline — secrets, .env, destructive ops, hooks). It also has the `security-reviewer` persona (v0.2.0) for threat modeling + supply-chain review. What's missing is the **offensive boundary** — when may an agent run an exploit, develop a tool that could attack systems, or scan a third-party? Without a Constitution-level rule, agents operating under user instruction will produce things from "scan example.com to test our defenses" (potentially illegal without authorization) all the way to "develop an info-stealer for security research" (illegal full stop).

## Decision

Add **Article IX — Cybersecurity & authorized-testing discipline** to the Constitution as an Iron Law. Bump Constitution `1.1.0 → 1.2.0` (minor; additive only — no Iron Law removed or relaxed).

The article is renumbered from the brief's "Article XII" to fit BeQuite's structure. The substantive text is otherwise verbatim from the addendum, with **four senior-architect amendments**:

### Amendment 1 — Internal red-team carve-out (8 hard guardrails)

The original addendum's "no malware, no exception" rule would have blocked all corporate red teams from using BeQuite — which is exactly the legitimate-user category that most needs a Constitution-governed offensive harness. I proposed a single, narrow, hard-guardrailed carve-out for internal corporate red-team artifacts (custom C2, implants, payloads) under an `RoE-RT-<id>.md` ADR meeting all 8 conditions: dual-signature, corporate-IP-only target, compile-time-callback-URL-assertion, hard-coded engagement-id-and-expiry, private-repo-only source, sandboxed-no-egress build, post-engagement cryptographic-shred, no-reuse-without-new-RoE.

Without this carve-out, BeQuite is unusable for corporate red teams. With it, the door is narrow and audit-evidence-requiring. **Ahmed delegated to me; I'm in.**

### Amendment 2 — Cryptojackers added to forbidden-no-matter-what list

The original addendum listed "stealer, RAT, ransomware, C2-as-a-service" as primary-purpose-harm categories. Cryptojackers (cryptocurrency miners deployed without operator consent) are a separate category that doesn't fit under those four labels but is equally clearly malware. Added explicitly.

### Amendment 3 — Defensive validation clause for known-CVE PoCs

The original addendum forbade "exploit PoCs against targets outside an RoE" — correct for external use. But it left ambiguous the defensive case: using a public CVE PoC to verify your own patch actually fixes the CVE on your own systems. This is regression-testing, not exploitation. Added explicit allowed-clause: under an `RoE-self-<id>.md` ADR, defensive validation against own systems is permitted.

### Amendment 4 — Plural disclosure frameworks

The original addendum locked coordinated disclosure to "Project Zero 90-day convention." Project Zero is one framework; CERT/CC is another; MITRE CNA is a third; FDA (medical devices), ICS-CERT (industrial control), NCSC (nation-state-coordinated) are industry-specific. Locking to one framework misses regulated sectors. Changed wording to "per one of the recognised frameworks" + named the six.

## Rationale

- **Defensive-first by default.** No project needs explicit authorization to harden, scan, fix, threat-model, comply. The default mode does the 80% of useful security work without RoE friction.
- **RoE-gated offensive work.** Authorized-only mode requires a documented RoE per PTES / NIST SP 800-115 / standard bug-bounty contract conventions. The RoE template (`skill/templates/roe-template.md`) operationalises this.
- **Three hooks enforce, not exhort.** `pretooluse-pentest-authorization` (no offensive tool without RoE), `pretooluse-no-malware` (forbidden categories blocked at the regex level, no override), `pretooluse-cve-poc-context` (PoC detected → ADR with CVE-id + target-environment + non-deployment-statement + disclosure-path required).
- **Two new personas.** `security-auditor` (defensive, auto-invokes at end of P6) + `pentest-engineer` (offensive, refuses without RoE).
- **Pairs with existing personas.** `security-reviewer` (v0.2.0) does threat modeling + supply-chain review; the new pair extends to operational security testing.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| Keep "Article XII" numbering | Verbatim with addendum | Article numbering would jump VII → IX (no VIII), or jump IX → XII (no X / XI) | Renumber to IX (after Article VIII added in v0.5.1) |
| No internal red-team carve-out | Strictest possible posture | BeQuite cannot serve corporate red teams (a primary legitimate-user category) | 8-guardrail carve-out adopted |
| Lock disclosure to Project Zero only | Simplest rule | Misses regulated industries (medical, ICS, government) | Plural framework |
| Include Metasploit Framework in default tool list | Comprehensive | Too heavy + offensive to embed by default | RoE-only surface |
| Article-XII-as-Doctrine instead of Iron Law | Lighter; opt-in | Defensive baseline applies to every project | Iron Law is right home |

## Consequences

### Positive

- AI agents can no longer silently produce exploit code or malware under user prompts.
- Defensive baseline (SAST + dep scan + secret scan + container scan + IaC scan + WAF) applies to every BeQuite project.
- Corporate red teams have a narrow, audit-evidence-requiring path to use the harness.
- Disclosure framework plural means medical / ICS / government users can use BeQuite without framework-mismatch.

### Negative

- Two more personas to load (now 15: master's 10 + skeptic + automation-architect + scraping-engineer + security-auditor + pentest-engineer; plus support personas cve-watcher + disclosure-timer).
- Three more hooks (now 13 total). More integration surface.
- The 8-guardrail red-team carve-out is dense; users who want corporate red-team functionality have a high bar to satisfy. (Intentional.)
- Compliance Doctrines proliferate (now: existing fintech-pci + healthcare-hipaa + gov-fedramp + new vibe-defense + mena-pdpl + eu-gdpr).

### Constitutional impact

- Patch bump → Minor bump. v1.1.0 → v1.2.0. No Iron Law removed or relaxed; purely additive.

### Refactoring path

- If the 8-guardrail carve-out turns out to enable abuse, add a 9th guardrail (third-party audit attestation) without bumping Major. Removing the carve-out entirely requires Major bump.
- If the disclosure-framework plural needs more entries (CISA KEV, ENISA, etc.), add via patch bump.

## Verification

- ✅ Constitution v1.2.0 amendment applied to `.bequite/memory/constitution.md`.
- ✅ `skill/references/security-and-pentest.md` exists with verified May-2026 tool list + decision logic + workflow patterns + RoE template reference.
- ✅ Two new personas: `skill/agents/security-auditor.md` (defensive) + `skill/agents/pentest-engineer.md` (offensive; refuses without RoE).
- ✅ Two support personas: `skill/agents/cve-watcher.md` (I2.2) + `skill/agents/disclosure-timer.md` (I2.3).
- ✅ Three new hooks: `skill/hooks/pretooluse-pentest-authorization.sh` + `pretooluse-no-malware.sh` + `pretooluse-cve-poc-context.sh`.
- ✅ Two templates: `skill/templates/projects/scan-and-trigger.md` + `skill/templates/roe-template.md`.
- ✅ Three new Doctrines: `skill/doctrines/vibe-defense.md` (default for `audience: vibe-handoff` projects) + `skill/doctrines/mena-pdpl.md` (Egyptian / Saudi / UAE PDPL with jurisdiction branching) + `skill/doctrines/eu-gdpr.md`.
- ✅ `bequite audit` rule pack adds Article IX checks + per-Doctrine compliance checks (in v0.6.0+).

## References

- Related ADRs: ADR-009-article-viii-scraping (last Constitution amendment, v0.5.1).
- External docs:
  - PTES (Penetration Testing Execution Standard) — http://www.pentest-standard.org/
  - OSSTMM (Open Source Security Testing Methodology Manual) — https://www.isecom.org/OSSTMM.3.pdf
  - NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment) — https://csrc.nist.gov/publications/detail/sp/800-115/final
  - Project Zero disclosure policy — https://googleprojectzero.blogspot.com/
  - CERT/CC vulnerability disclosure — https://vuls.cert.org/
  - MITRE CNA (CVE Numbering Authority) — https://www.cve.org/ProgramOrganization/CNAs
  - OWASP LLM Top 10 (2025) — https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
  - Veracode 2025 GenAI Code Security Report
  - PhantomRaven incident (Koi Security, Aug-Oct 2025).
  - Egyptian PDPL (Law No. 151 of 2020) — https://mcit.gov.eg/Upcont/Documents/Reports%20and%20Documents_1232021000_Law_No_151_2020_Personal_Data_Protection.pdf
  - Saudi PDPL (SDAIA) — https://sdaia.gov.sa/en/Research/Pages/DataProtection.aspx (fully enforceable since 2024-09-14)
  - UAE PDPL — https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws (Federal Decree-Law 45/2021; carve-outs for DIFC / ADGM free zones)
- Memory Bank entries: `.bequite/memory/systemPatterns.md::ADR index`, `.bequite/memory/progress.md::Decisions made`.

## Amendments

```
2026-05-10 — initial draft + accepted in same session per Ahmed's "make it fully loaded" delegation. Four senior-architect amendments documented above.
```
