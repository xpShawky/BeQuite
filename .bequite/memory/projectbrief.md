# Project Brief: BeQuite

> Source of truth for BeQuite's own scope. Do not amend without an ADR.

---

## 1. The product in one sentence

A host-portable harness that turns Claude (and every peer coding agent that reads SKILL.md or AGENTS.md) into a senior tech-lead capable of shipping software end-to-end without producing the broken half-builds that dominate today's AI vibe-coding output.

## 2. Who it's for

- **Primary user:** engineers and motivated power-users who today copy ChatGPT/Claude prompts into Lovable, v0, Bolt, Replit Agent, Cursor, or Claude Code — and end up with broken half-builds, leaked secrets, hallucinated packages, or 70%-finished projects with no clean handoff.
- **Secondary users:**
  - Regulated-industry teams (fintech, healthcare, gov) who need *auditable* AI-generated code — the receipt chain is the wedge.
  - Tech-leads who want their team to stop re-litigating "what stack do we use" every two weeks (Constitution + Doctrines pin the answer to an ADR).
  - MENA developers building bilingual or RTL-by-default products — first-class Arabic support is in v1.0.0, not retrofitted.
- **Explicit non-users:** people writing software entirely by hand without AI assistance; people who want a hosted no-code product (BeQuite emits a real git repo, not a vendor's prompt history).

## 3. The problem

> "I built a great-looking landing page in Lovable in a weekend. Then I needed real auth, then I needed a worker queue, then the bills hit $200/mo, then the AI started hallucinating, then I gave up."

Veracode's 2025 GenAI Code Security Report found ~45% of AI-generated samples contain OWASP Top-10 issues (XSS 86% fail rate, log injection 88%, Java 72% fail). The PhantomRaven supply-chain attack (Koi Security, Aug-Oct 2025) shipped 126 malicious npm packages exploiting names AI tools hallucinate.

There are excellent **specs frameworks** (Spec-Kit, BMAD), excellent **memory patterns** (Cline Memory Bank), excellent **design lenses** (Impeccable), excellent **persona patterns** (Superpowers). None of them combine. None of them ship as the SKILL/CLI/template trio. None of them ship deterministic gates (hooks) that *block* bad behaviour rather than warning about it. None of them ship signed reproducibility receipts. None of them ship first-class MENA support. None of them are designed for the vibe-to-handoff bridge.

That's the gap.

## 4. The success criteria

| Criterion | Threshold | How measured |
|---|---|---|
| GitHub stars at 6 months | ≥ 1,000 | https://github.com/xpShawky/BeQuite |
| Monthly active CLI installs | ≥ 100 | PyPI download stats |
| Doctrine forks (industry-specific) | ≥ 10 | GitHub search for `bequite-doctrine-` repos |
| Successful auto-mode runs to DONE without rail-trip | ≥ 50 | Receipt chain analysis, opt-in telemetry |
| Vibe-to-handoff conversions (project moves from auto-mode → engineer follow-up in another host) | ≥ 20 | Cross-host import receipts |
| Time to first PR for a new contributor | ≤ 1 hour | Average from issue-open to first-commit by external contributor |

## 5. The hard constraints

- **Scale tier:** library / tool (no production hot path; the harness runs on developer laptops + CI).
- **Compliance:** none for BeQuite itself. Doctrines for fintech / healthcare / gov are shipped; we do not certify any specific compliance for the harness itself.
- **Locales:** `en-US`, `ar-EG`. Full RTL support in v0.11.0.
- **Audience flag:** `engineer` (v1 primary). v2 will add `vibe-handoff` web UI; v1 artifacts are designed to be portable to that surface.
- **Active Doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual`.
- **Cost ceiling (auto-mode default):** $20 USD per session, configurable.
- **Wall-clock ceiling (auto-mode default):** 6 hours per session, configurable.

## 6. Explicit non-goals

- **BeQuite is not a product builder.** It does not host your app. It does not run your database. It is a discipline + a harness.
- **BeQuite is not a no-code platform.** Output is a real git repo with real source code in real files.
- **BeQuite is not a Claude-only tool.** The Skill is the source of truth, but the artifacts (AGENTS.md, spec.md, plan.md, tasks.md) are designed to load in 25+ hosts.
- **BeQuite is not a "best agent" leaderboard winner.** The AkitaOnRails 2026 finding (solo frontier > forced multi-model) shapes our routing — Skeptic runs at boundaries, not inside coupled tasks.
- **BeQuite does not auto-publish.** PyPI publish, npm publish, git push to remote, terraform apply — all pause auto-mode for human approval.

## 7. The hand-off bar

A second engineer can:

1. Run `uvx bequite init demo --doctrine default-web-saas --scale 5000` from a clean machine.
2. Read `HANDOFF.md` end-to-end.
3. Boot the demo, deploy it, hand it to their CTO.

If `HANDOFF.md` doesn't pass that test, BeQuite is not done.

## Revisions

```
2026-05-10 — initial draft (this file). Sub-version v0.1.0.
```
