---
name: bequite-researcher
description: Deep verified-evidence procedures for the 11-dimension research model (stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation). WebFetch-first, never memory-first. Anti-PhantomRaven defense. Loaded by /bq-research and /bq-plan when fresh evidence is required.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Bash
---

# bequite-researcher — verified evidence over memory

## Why this skill exists

LLMs are confidently wrong about 2026. Pricing pages changed. Libraries were deprecated. New CVEs landed. Whole companies pivoted or died (Roo Code, Stronghold, EV-cert SmartScreen reputation, ...).

**Memory is a guess. WebFetch is evidence.**

This skill encodes the verification discipline so every research session produces sources you can defend.

---

## The 11 dimensions, deep

### 1. Stack

For every library, framework, or runtime under consideration:

**Freshness probe:**
- npm: `npm view <pkg> time.modified` (or WebFetch https://www.npmjs.com/package/<pkg>)
- PyPI: `pip index versions <pkg>` (or WebFetch https://pypi.org/project/<pkg>/)
- Crates: WebFetch https://crates.io/crates/<pkg>
- GitHub: WebFetch https://github.com/<org>/<repo> → look at "Last commit", "Stars", open vs closed issues

**Verdict thresholds:**
- Last release < 6 months → fresh ✓
- 6-12 months → warn ⚠ (verify roadmap before adoption)
- > 12 months → stale ✗ (require explicit user OK)

**License flags (rejection cause unless user explicitly accepts):**
- AGPL — viral, blocks commercial closed-source
- GPL v2/v3 — viral, more permissive than AGPL but still restrictive
- SSPL / Commons Clause / Elastic License — non-OSI

**Bundle size (JS/TS):**
- WebFetch https://bundlephobia.com/package/<pkg>
- > 200KB gzipped → warn for client-side libs

### 2. Product

Two-paragraph definition:
- **What it is** — one sentence, no jargon
- **Who it's for** — concrete persona, not "everyone"
- **What it replaces** — what the user currently does without this

Verify against market — is there demand for this? Search:
- "best <category> 2026"
- "alternative to <closest competitor>"
- Reddit r/<relevant> for complaints

### 3. Competitors

3-5 direct competitors. For each:
- URL
- Pricing tier you'd use
- Strongest feature
- Most-complained-about gap
- Trajectory (growing? sunsetting? acquired?)

Sources:
- G2 / Capterra / Product Hunt for B2B
- Reddit + Twitter for sentiment
- LinkedIn for headcount trajectory

### 4. Failures (what failed before)

Look at:
- GitHub repos archived in this space
- Crunchbase shutdowns
- Hacker News postmortems
- Indie Hackers fail stories

For each failure, extract the **specific lesson** — not generic platitudes.

### 5. Success (what worked)

3-5 reference implementations. For each:
- Open-source repo OR public case study
- The specific pattern they used
- Why it worked for their context (does it apply to yours?)

### 6. User journey

End-to-end flow from the user's POV:
- Sign-up trigger (what made them try this?)
- First-time experience (5 minutes after sign-up)
- Daily/weekly use
- The "this is why I pay" moment
- The "this is why I cancel" moment

### 7. UX/UI

For UI products, gather 3-5 design references:
- Mobbin.com — interaction patterns
- Dribbble / Pinterest — visual references
- Real product screenshots from competitors

Note for each: what works (hierarchy, density, typography) and what to avoid (AI-slop patterns — see bequite-ux-ui-designer skill).

Accessibility baseline: WCAG 2.1 AA. Tools: axe-core in CI, Pa11y for crawls.

### 8. Security

Two reference maps:
- **OWASP Web App Top 10** (2021 stable, 2025 draft)
- **OWASP Top 10 for LLM Applications** (2025 final, if AI involved)

Per chosen lib, check:
- OSV scanner: https://osv.dev/list?q=<pkg>
- GitHub Security Advisories on the repo
- Snyk vulnerability database

Supply chain:
- Lockfile committed (yes/no)
- Dependency-confusion risk (is the same package on multiple registries?)
- PhantomRaven (Aug-Oct 2025): never install a package without WebFetch-verifying it exists in the registry

### 9. Scalability

Don't pick a stack for 50K users when you have 50. The scale-tier table:

| Tier | Users | Architecture |
|---|---|---|
| Solo / demo | 1-50 | Single VPS, SQLite, no queue |
| Small SaaS | 50-5K | Managed Postgres, single region, CDN |
| Growth | 5K-50K | Read replicas, Redis cache, background queue |
| Scale | 50K-500K | Sharded DB, multi-region, dedicated queue infra |
| Big tech | 500K+ | Custom infra, not your problem yet |

Verify against verified 2026 cost data per tier.

### 10. Deployment

Compare 3-5 hosts for the chosen stack:
- Cold start time (Vercel ~50ms, Fly ~200ms, Render ~500ms for free tier)
- Region count + locations
- Pricing 2026 (WebFetch the pricing page; do NOT use memory)
- Build minutes / function duration limits

Note 2026 reconciliations:
- Vercel: Hobby hard cap 300s; Pro/Enterprise default 300s, configurable to 800s
- AWS Lambda: 15min hard cap
- Cloudflare Workers: 30s CPU, unlimited wall-clock (subrequests)

### 11. Differentiation

The kill question: "Why would a user pick this over <closest competitor>?"

Acceptable answers (in order of strength):
1. **Concrete capability they lack** — "they don't support X; we do"
2. **10x cheaper / faster** — quantified
3. **Niche fit** — "they target SMB; we target solo founders"
4. **Regional / language fit** — "they only support English; we ship Arabic"

Unacceptable answers:
- "Better UX" (everyone says this)
- "Modern stack" (users don't care)
- "AI-powered" (they all are now)

If you can't write a strong differentiation, flag in OPEN_QUESTIONS.md.

---

## Anti-hallucination defenses

### PhantomRaven (npm, 2025)

Threat: malicious npm packages with squatted/typosquatted names.

Defense:
- Before recommending `npm install <pkg>`, WebFetch https://www.npmjs.com/package/<pkg>
- Confirm the package exists, has > 1 release, and the org matches what you expect
- Cross-check against `references/package-allowlist.md` (project-specific allowlist)
- For new deps not on allowlist, surface as "needs user approval"

### Shai-Hulud (broader, 2025)

Threat: 700+ packages compromised via maintainer-account takeover.

Defense:
- Pin to exact versions (no `^` or `~`) for security-critical deps
- Commit lockfile
- Enable Dependabot or Renovate with auto-merge OFF
- 2FA on registry accounts (you don't control this, but flag it for users)

### Memory-based pricing claims

Defense:
- Never quote pricing from memory
- WebFetch the vendor's pricing page within the last 24h
- If WebFetch fails, mark the figure as "unverified — verify before commitment"

---

## Output discipline

Every claim in RESEARCH_REPORT.md has:
- URL (with date accessed)
- Quote or paraphrase that supports it
- Verdict (fresh / warn / stale / unverified)

No claim without a source. No source without a date.

---

## Failure modes

- WebFetch rate-limited → use cache, mark items unverified, exit gracefully
- Library doesn't exist in registry → flag as hallucination risk, do NOT recommend
- Pricing page paywalled / requires login → mark unverified, note alternatives
- Two reputable sources disagree → cite both, recommend the more recent one

---

## When NOT to use this skill

- Trivial fixes (use `bequite-problem-solver`)
- UI critique without backend changes (use `bequite-ux-ui-designer`)
- Already-decided projects rebuilding the same plan (waste of WebFetch budget)

---

## Tie-break protocol

When two libraries are equivalent on freshness + license + CVEs, prefer:
1. The one with more concrete user count / production deployments
2. The one with TypeScript types shipped (for JS/TS projects)
3. The one with a paid commercial backer (sustainability)
4. The one with smaller bundle / install size
5. Coin flip — flag both, let user pick

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file is an EXAMPLE, not a mandatory default.**

Research the best fit for the specific project before adopting any candidate.

**Do not say:** "Use X."
**Say:** "X is one candidate. Research and compare against other options. Use it only if it fits this project."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan). Short inline for small projects; full ADR at `.bequite/decisions/ADR-XXX-<tool>-choice.md` for large / regulated work.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
