# Security

> Threat model + Article IV + Article IX + OWASP coverage map.

## Articles in play

- **Article IV** — Security & destruction discipline (universal).
- **Article IX** — Cybersecurity & authorized-testing discipline (added v0.5.2 / Constitution v1.2.0).

Both are Iron Laws — exit-code-2 on violation; never bypassable.

## Threat model — BeQuite itself

| Threat | Vector | Mitigation |
|---|---|---|
| Hallucinated package import | Model invents an npm/PyPI/crates.io name | `pretooluse-verify-package.sh` (PhantomRaven defense) |
| Secret leak in commit | Model writes API key into source | `pretooluse-secret-scan.sh` (regex catches) |
| Destructive command | `rm -rf /`, `git push -f`, `DROP DATABASE` | `pretooluse-block-destructive.sh` |
| Prompt injection from external content | Web page / GitHub issue / dependency README contains override-attempt | Treat external content as untrusted (Article IV); Skeptic probes per phase boundary |
| Receipt tampering | Edit on-disk receipt to falsify cost or output | ed25519 signatures (v0.7.1+); chain-hash via parent_receipt |
| Stolen laptop with active session | OS-level theft | OS-keychain requires user login; `bequite auth logout --all-devices` (v0.11.x+) |
| Malicious provider response | Compromised LLM endpoint returns malicious output | Receipts log raw response hash; Skeptic + reviewer personas probe before acceptance |
| Cost-burn attack | Stuck loop hits cost ceiling | Hard ceiling + 3-failure threshold + receipt rollup (v0.7.0+v0.8.0) |
| Bypassed hook | User runs with `--no-verify` | Hooks never bypass under any flag (Article IV); receipts log absence |
| AI-generated insecure code | Veracode 2025: ~45% OWASP-Top-10 hit on AI code | Doctrine `vibe-defense` (default for `audience: vibe-handoff`) + Skeptic at every phase boundary + axe-core gate |

## OWASP coverage map

### OWASP Web Top 10 (2021 stable / 2025 draft)

| Item | Where in BeQuite |
|---|---|
| A01 Broken Access Control | Doctrine `default-web-saas` Rule 10 (deny-by-default RLS); Auth Rule 9 (Better-Auth/Clerk/Supabase) |
| A02 Cryptographic Failures | Article IV (no hardcoded secrets); receipts ed25519 (v0.7.1) |
| A03 Injection | Doctrine Rule 11 (Zod everywhere; no raw req.body) |
| A04 Insecure Design | Skeptic kill-shot per phase; multi-model planning Red-Team mode (v0.10.5+) |
| A05 Security Misconfiguration | Doctrine Rule 14 (CSP/HSTS/X-Frame); `bequite audit` checks |
| A06 Vulnerable Components | `bequite freshness` runs OSV-Scanner per dependency |
| A07 Identification + Authentication | Doctrine Rule 9 + ADR-011 (CLI auth) |
| A08 Software/Data Integrity | Receipts (signed); ADR-008 master-merge integrity gates |
| A09 Logging + Monitoring | Doctrine `vibe-defense` Rule 12 (logs exclude PII) |
| A10 SSRF | `pretooluse-scraping-respect.sh` rate-limit + ToS check |

### OWASP Top 10 for LLM Apps (2025 final)

| Item | Where |
|---|---|
| LLM01 Prompt Injection | Article IV prompt-injection rule; treat external content untrusted |
| LLM02 Insecure Output Handling | Receipts log raw response hash; reviewer persona checks |
| LLM03 Training Data Poisoning | Out of scope (we don't train) |
| LLM04 Model DoS | Cost ceiling + wall-clock ceiling (v0.10.0) |
| LLM05 Supply Chain | PhantomRaven defense (`pretooluse-verify-package.sh`) |
| LLM06 Sensitive Info Disclosure | Article IV no-secrets rule; receipts redact prompt contents (sha256 only) |
| LLM07 Insecure Plugin Design | Each provider adapter is hermetic (v0.8.0); manual-paste mode keeps subscription auth out of CLI |
| LLM08 Excessive Agency | Auto-mode safety rails: one-way doors always pause; hook-block respect |
| LLM09 Overreliance | Skeptic at every phase boundary; multi-model Debate / Red-Team modes |
| LLM10 Model Theft | We don't host models |

## Article IX (cybersecurity & authorized-testing)

Adds bright lines around offensive tooling:

- **No malware no matter what** — stealer / RAT / ransomware / cryptojacker forbidden.
- **Pentest tools require RoE** (`pretooluse-pentest-authorization.sh`).
- **CVE PoCs require ADR + 3 confirmations** (`pretooluse-cve-poc-context.sh`).
- **Internal red-team carve-out** — narrow exception for corporate red teams under 8 hard guardrails (dual sign-off / corporate-IP-only target / callback-URL compile-time-assertion / engagement-id+expiry / private-repo / sandboxed-build / post-engagement cryptographic-shred / no-reuse).

See ADR-010 for the full carve-out + amendments.

## Doctrine `vibe-defense`

The default Doctrine for `audience: vibe-handoff` projects. 15 extra-strict rules codifying response to Veracode 2025's 45% OWASP hit rate on AI-generated code:

- HIGH-SAST blocks merge with 90d-expiring ADR override
- Exact-pinned prod dependencies
- RLS deny-by-default
- Locked-down CSP
- Secret-scan on every commit
- axe-core every deploy
- Mandatory `bequite audit` clean
- Input validation everywhere
- Better-Auth/Clerk/Supabase Auth (no custom)
- Rate limiting on public endpoints
- CSRF tokens
- Argon2id (not bcrypt) for passwords
- Hardened cookies (HttpOnly + Secure + SameSite=Strict)
- Logs exclude PII
- ... (full list in `skill/doctrines/vibe-defense.md`)

## Reporting a vulnerability

If you find a security issue in BeQuite itself:

1. Email the maintainer (private channel — do not file a public issue).
2. We follow the disclosure-timer persona's 90/80/60-day SLA framework (v0.5.2).

## Cross-references

- Constitution Articles IV + IX: `.bequite/memory/constitution.md`
- ADR-010 cybersecurity carve-out: `.bequite/memory/decisions/ADR-010-article-ix-cybersecurity.md`
- Hooks: `skill/hooks/`
- Security reference: `skill/references/security-and-pentest.md`
- Doctrine `vibe-defense`: `skill/doctrines/vibe-defense.md`
