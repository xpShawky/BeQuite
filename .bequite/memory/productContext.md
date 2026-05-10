# Product Context: BeQuite

> Why BeQuite exists and the journey of the people who use it. Pair with `projectbrief.md` (scope) and `systemPatterns.md` (architecture).

---

## 1. Why this product exists

In 2025–2026 a class of tools emerged that let non-engineers (and time-pressed engineers) ship working web apps from a prompt: Lovable, v0, Bolt, Replit Agent. They closed the "I have an idea, give me a deployed React app" loop in minutes. They also concentrated almost every failure mode of AI-assisted coding into a single audience:

- **Hallucinated dependencies.** PhantomRaven (Koi Security, Aug–Oct 2025) shipped 126 malicious npm packages with names AI tools were caught suggesting. Shai-Hulud added ~700 more.
- **Leaked secrets.** Veracode 2025 found ~45% of AI-generated samples have OWASP Top-10 issues. XSS fail rate 86%, log injection 88%, Java fail 72%.
- **Generic AI aesthetics.** Inter font, purple-blue gradients, nested cards, gray-on-color text, bounce easings. The "AI slop tells."
- **The 70% wall.** Vibe-coders ship a polished 70% of an app, then debugging burns credits, complex logic breaks, the project is abandoned. A Lovable user who outgrows React+Supabase has no migration path; their "code" is a vendor's prompt history.
- **The handoff fail.** "I built X, please test." The agent never booted the app. The handoff doc is for AI agents, not humans.

Meanwhile a parallel ecosystem of *engineer-grade* tools emerged: Spec-Kit, BMAD-Method, Superpowers (Jesse Vincent), Cline Memory Bank, Impeccable, Aider architect mode, Anthropic Skills, AGENTS.md. These tools work brilliantly — *if you already know how to install them*. The vibe-coders never touch them.

> **No one currently owns "vibe-to-handoff."** A spec-first, framework-disciplined surface that emits portable, agent-readable artifacts (`AGENTS.md` + `spec.md` + `tasks.md`) into a real git repo, designed to be picked up by Claude Code / Cursor / Codex without rewriting.

Closest prior art is `oimiragieo/BMAD-SPEC-KIT` — 5 stars, 1 fork. The niche is essentially open. **That's why BeQuite exists.**

## 2. The user journey

### A vibe-coder — without BeQuite (today)

```
Step 1 — open Lovable, prompt "build me a clinic-bookings app for Cairo"
Step 2 — get a polished React + Supabase scaffold in 60 seconds
Step 3 — start adding features; the auth gets confused with admin/customer roles
Step 4 — debug loop: 4 hours, $30 in credits, regression in unrelated panel
Step 5 — try to migrate to "real code"; discover there's no spec, no plan, no tasks file
Step 6 — abandon; rebuild from scratch with a real engineer two months later
Pain — sunk cost, no learning, lost time-to-market
```

### A vibe-coder — with BeQuite (v1)

```
Step 1 — `uvx bequite init clinic --doctrine default-web-saas,mena-bilingual --scale 5000`
Step 2 — Researcher (P0) quotes back findings about MENA clinic-software competitors and asks for ack
Step 3 — Architect (P1) walks through Next.js + Hono + Supabase + Better-Auth + Vercel; the freshness probe catches that Stronghold is deprecated, recommends OS-keychain instead; ADR-001 is signed
Step 4 — `bequite auto --feature confirm-bookings --max-cost-usd 10` runs P2 → P7
Step 5 — Skeptic produces a kill-shot question at every phase boundary; primary answers them
Step 6 — Implementer + Reviewer ship the feature; receipts emitted; HANDOFF.md generated
Step 7 — Tester walks the app at `?locale=en` AND `?locale=ar` (RTL); admin walk + user walk pass; axe-core green
Win — six tagged commits; six signed receipts; a real git repo a real engineer can pick up tomorrow.
```

### An engineer — without BeQuite (today)

```
Step 1 — set up Cursor / Claude Code / Codex
Step 2 — install Spec-Kit, install Superpowers, install Cline Memory Bank, install Impeccable, set up Playwright MCP, set up shadcn registry, set up context7
Step 3 — assemble per-project rules in .cursor/rules/, CLAUDE.md, AGENTS.md
Step 4 — every project re-derives the rules; rules drift; new hire onboarding takes a week
Step 5 — agent hallucinates a package; deploy to staging; security finding from PostHog
Step 6 — write up postmortem; "we should have a Constitution"; nothing happens
Pain — every project is bespoke; institutional memory drains
```

### An engineer — with BeQuite (v1)

```
Step 1 — `uvx bequite init my-saas --doctrine default-web-saas,fintech-pci --scale 50000`
Step 2 — fork the Constitution if needed; add Doctrines from the market
Step 3 — Constitution + Doctrines auto-load on every session; PreToolUse hooks block bad behaviour at the exit code level
Step 4 — `bequite audit` runs in CI; Article-V scale-honesty + Article-VII hallucination + Doctrine rules all enforced as inline PR comments
Step 5 — `bequite freshness` runs quarterly; deprecated dependencies flagged before they hit production
Step 6 — receipt chain proves to the security auditor that every line is traceable to a spec, a Skeptic answer, and a verifier output
Win — institutional memory is in the repo, not the heads of the senior engineers.
```

## 3. User segments

| Segment | % of TAM (rough) | Acquisition channel | Notes |
|---|---|---|---|
| Vibe-coders (Lovable / v0 / Bolt refugees) | 60% | TechCrunch MENA, X, HN, Arab Net | The wedge — vibe-to-handoff |
| Engineers in skills-aware hosts (Claude Code / Cursor / Codex / Cline) | 25% | Anthropic plugin marketplace, AGENTS.md registry | The early-adopter beachhead |
| Regulated-industry teams (fintech / health / gov) | 10% | Doctrine market, conferences | Highest LTV; receipt chain is the wedge |
| MENA developers (bilingual / RTL needs) | 5% | Direct relationship via @xpshawky's network | Differentiated value prop |

## 4. Competitor landscape

| Competitor | What they do well | Where they fall short | Why we beat them |
|---|---|---|---|
| Spec-Kit | Spec-driven workflow grammar; 90k+ stars | No memory layer; no Constitution; no audit; no receipts | We extend Spec-Kit's commands and add 9 of our own |
| BMAD-Method | Phase decomposition + 12+ persona agents; opinionated | Heavy ceremony; specs as inputs not outputs | Our Skeptic + lean phases are lighter |
| Cline Memory Bank | Six-file durable memory; portable to any host | Pure convention, no enforcement | We adopt verbatim, add audit + freshness |
| Superpowers (Jesse Vincent) | TDD + brainstorm + plan; Anthropic plugin marketplace | Claude-Code-only; no Memory Bank; no Constitution | We're host-portable; we layer Constitution |
| Impeccable (Paul Bakaus) | Design language + 23 UI/UX commands; ~26.6k stars | Single-maintainer; design only | We bundle as Doctrine, not as core dependency |
| Aider architect mode | Frontier-reasoner + cheap-editor split | Single-shot; no memory; no audit | Our routing reflects AkitaOnRails 2026; Skeptic at boundaries |
| Lovable / v0 / Bolt / Replit Agent | Polished prompt-to-app for non-engineers | Vendor lock-in; cratering past 70%; no real git repo | We emit real artifacts; vibe-to-handoff portable |
| Kiro (AWS) | Native specs (`requirements.md` / `design.md` / `tasks.md`) | AWS-flavoured; heavy for prototypes | We're host-agnostic; lighter |

## 5. The "why now" thesis

Three enablers crossed in 2025–2026:

1. **Anthropic Skills format stabilised** (frontmatter, three-level loading, no-network constraint on API skills). Cursor 3.0 (Apr 2026) followed with `.cursor/skills/SKILL.md`. The format is now portable.
2. **AGENTS.md adoption hit critical mass** — Linux Foundation Agentic AI Foundation took stewardship; 25+ hosts (Codex, Cursor, Aider, Copilot, Gemini, Jules, Factory, Windsurf, Devin, Amp, Zed, Warp, VS Code, Junie, RooCode, Augment, Continue, …). Cross-host portability is now a real thing.
3. **MCP ecosystem matured** — Context7 (54k stars, version-pinned docs that fight hallucination), Playwright MCP (Microsoft, accessibility-first), shadcn registry MCP (built into shadcn CLI v3+), 21st.dev Magic. Together: the de facto frontend agent stack. We can compose without reimplementing.

The window is now: build the unified harness before the vendor-lock-in vibe-coders capture the non-engineer audience permanently.

## 6. The acceptance criteria — qualitative

> "I prompted BeQuite once. It pushed back on my stack pick because Stronghold is deprecated. I learned three things that day. Now I review every Constitution amendment my team proposes."
> — fictional MENA engineer, 6 months after v1.0.0

> "Our auditor accepted the BeQuite receipt chain as evidence-of-process. We did not have to write a single line of compliance documentation."
> — fictional fintech CISO, 12 months after v1.0.0

## 7. Anti-patterns we'll avoid

- **Yet-another-skill-marketplace.** We bundle proven peer skills (Impeccable, Memory Bank pattern, Spec-Kit grammar) by *vendoring pinned snapshots* — not by depending on a marketplace. Our marketplace is the Doctrine market.
- **AGI-shaped marketing.** BeQuite is not "the autonomous AI tech-lead." It is a discipline that *contains* the AI tech-lead so the human running it can sleep at night.
- **Pretend universality.** A library project does not need RTL-by-default fonts. We layer.
- **Whisper-mode amendments.** A new rule that isn't in an ADR doesn't exist.

## 8. Open product questions

- Should v2 ship a hosted UI or a desktop Tauri app? (TBD; pause for user research after v1 lands.)
- Do we accept opt-in telemetry for the success-criteria metrics? (Privacy-first stance; receipt-chain hashing only, never code or prompts. ADR-002 will decide.)
- Do we accept community Doctrines into the main repo, or maintain a separate `bequite-doctrines` org? (The latter scales better. ADR-003 will decide.)
