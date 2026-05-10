# BeQuite Constitution v1.0.0 — operating under BeQuite

> Drafted: 2026-05-10 · Maintainer: Ahmed Shawky (xpShawky) · BeQuite version: 0.1.0
>
> This Constitution governs every action taken inside this repository — by humans, by AI agents, by automation. It is layered: **Iron Laws** are universal and immutable-ish (amendable only via ADR + version bump); **Doctrines** are forkable rule packs loaded per project type (`@doctrines/<active>.md`).
>
> Read this file fully before taking any action. Re-read on every session start (Article III). When in doubt, an Iron Law beats a Doctrine; a Doctrine beats convenience.

---

## Iron Laws (universal)

### Article I — Specification supremacy

Code serves the spec. `spec.md` is technology-agnostic; `plan.md` owns implementation. **No code merges without an updated spec or ADR.** A diff that is not traceable to a `spec.md` line, a `tasks.md` ID, or a recorded ADR amendment violates this article and is rejected at merge.

### Article II — Verification before completion

A task is "done" only after its acceptance evidence (Playwright spec, unit tests, smoke test, contract test, whatever the task declared) **has been executed in this session and passed.** The agent **MUST NOT** use the words *should*, *probably*, *seems to*, *appears to*, or *I think it works* in completion messages. Hedge language in a completion message is a Stop-hook violation (exit code 2). State what ran, what passed, what failed, what was not run.

### Article III — Memory discipline

At the start of every session and every major task, read all six Memory Bank files (`projectbrief`, `productContext`, `systemPatterns`, `techContext`, `activeContext`, `progress`) plus the active ADRs and the loaded Doctrines. At the end of every task, update `activeContext.md` and `progress.md`. At the end of every phase, snapshot to `.bequite/memory/prompts/v<N>/`. Memory is the only persistence between sessions; treating it as optional breaks every later phase.

### Article IV — Security & destruction discipline

- **Never read** `.env*` files. **Never write** secrets to disk. **Never commit** keys, tokens, JWTs, AWS access patterns, or anything matching the secret-scan regex.
- **Never run** `rm -rf` outside `/tmp` or an explicit ADR-approved scope, `terraform destroy`, `DROP DATABASE`, `git push -f` to a protected branch, `git reset --hard` discarding uncommitted work, or any equivalent destructive operation without an explicit ADR authorising it for this project.
- PreToolUse hooks (`pretooluse-secret-scan.sh`, `pretooluse-block-destructive.sh`, `pretooluse-verify-package.sh`) enforce these at exit code 2. **Never bypass hooks under any flag.**
- Reference: OWASP Top 10 for LLM Applications 2025 (final) and OWASP Web Application Top 10 (2021 stable / 2025 draft).

### Article V — Scale honesty

The declared scale tier in `plan.md` is binding. The implementation **MUST NOT** introduce architecture that caps below the declared tier. Tiers:

| Tier | Bound | Bound-violating patterns (auto-fail audit) |
|---|---|---|
| ≤1K users | Solo / hobby | (none — anything works) |
| 1K–50K | Small SaaS | Vercel-hobby-only deploy paths; SQLite for write-heavy multi-tenant; Supabase free tier reliance |
| 50K–500K | Mid-market | Single-instance + no caching; in-memory queues; synchronous fan-out |
| 1M+ ("country") | National scale | Single-region writes; monolithic VM; reactive-only stores (Convex/Firebase) for write-heavy paths |
| Millions / global | Hyperscale | Anything without explicit modular boundaries; non-replicated primary; cache-invalidation-by-prayer |

For BeQuite itself: **scale tier = library / tool**. The harness has no hot path; usage is per-developer-laptop. We do not pretend otherwise.

### Article VI — Honest reporting

Do not report a feature as complete if any test failed, was skipped, or was not run. Report exactly:

1. What was built (file paths, line counts, links to receipts).
2. What was tested (commands run, outputs read, exit codes).
3. What remains (unimplemented tasks, deferred TODOs).
4. What is uncertain (where the author lacks confidence and why).

A completion message that omits any of (1)–(4) violates this article.

### Article VII — Hallucination defense

Never import a package without verifying it exists in the relevant registry (npm / PyPI / crates.io / Cargo / Go modules) **in this session** via:

- `npm view <pkg>` for npm
- `pip index versions <pkg>` for PyPI
- `cargo search <pkg>` for Rust
- `go list -m <pkg>@latest` for Go
- WebFetch the registry page when none of the above is available

PreToolUse hook `pretooluse-verify-package.sh` greps every Edit/Write for new imports and runs the verifier. Cross-checks the package against `references/package-allowlist.md` (BeQuite's known-good list) and recorded supply-chain incidents (the **PhantomRaven** campaign — Koi Security 2025, 126 packages exploiting hallucinated names; **Shai-Hulud** ~700 packages; the September 8 attack 18 packages). A package not in the allowlist requires a freshness probe pass before import.

---

## Doctrines (loaded per project type)

This project (BeQuite itself) is currently running with the following Doctrines:

```
- library-package      (BeQuite is a published tool; semver-strict, no telemetry)
- cli-tool             (one of BeQuite's deliverables is a CLI; man-page + bash completions)
- mena-bilingual       (BeQuite ships with first-class MENA support — author + audience overlap)
```

(`default-web-saas` is bundled but not loaded for BeQuite-itself; it's a doctrine BeQuite *ships* for downstream projects, not one BeQuite-itself runs under.)

Doctrines live at `.bequite/doctrines/` (per-project) or `skill/doctrines/` (BeQuite-shipped). Each Doctrine carries its own version and supersedes record. To load a Doctrine: edit `.bequite/bequite.config.toml::doctrines = [...]`.

---

## Governance

**Amendments** to Iron Laws require a new ADR + version bump:

- Patch (`1.0.0` → `1.0.1`) — clarification, no semantic change.
- Minor (`1.0.0` → `1.1.0`) — additive Iron Law or explicit additional gate.
- Major (`1.0.0` → `2.0.0`) — removing or relaxing an Iron Law (rare; requires explicit project-owner sign-off).

**Doctrines** version independently of the Constitution. A Doctrine bump does not bump the Constitution version.

**Conflict resolution:**

1. Iron Law beats Doctrine.
2. Doctrine beats convenience.
3. ADR with `status: accepted` beats convention.
4. A superseded ADR (`status: superseded`) is non-binding; the superseding ADR governs.

**RATIFICATION_DATE:** `2026-05-10`

**Maintainer:** `Ahmed Shawky (xpShawky)`

---

## Quick reference: banned phrases in completion messages (Article II)

```
should           probably          seems to         appears to
I think it works  might work       hopefully        in theory
```

Stop-hook `stop-verify-before-done.sh` exits 2 on detection. Re-state with concrete evidence (commands, exit codes, paths).

## Quick reference: tool calls that always pause auto-mode (Article IV)

```
rm -rf <path>                git push --force
DROP DATABASE                git reset --hard
terraform destroy            git push to protected branches
DROP TABLE                   anything in pretooluse-block-destructive.sh
```

## Quick reference: amendments log

ADRs at `.bequite/memory/decisions/` document every constitutional amendment. A pristine project has zero amendments. BeQuite-itself currently has zero amendments — the first ADR will be ADR-001 covering the BeQuite stack itself (Python CLI + Markdown skill + bash hooks).

```
(none yet)
```
