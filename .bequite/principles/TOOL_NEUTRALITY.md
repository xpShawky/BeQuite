# BeQuite tool neutrality — global principle

**Status:** active doctrine (binding on every BeQuite skill, command, doctrine, plan, ADR, and conversation)
**Adopted:** 2026-05-11 (v3.0.0-alpha.3)
**ADR:** `docs/decisions/ADR-003-tool-neutrality.md`

---

## The rule

Any tool, library, repo, framework, design system, workflow, or method mentioned anywhere in BeQuite is an **EXAMPLE**, not a fixed mandatory choice.

Do not hardcode any specific tool as the default just because it was mentioned in a skill, command, doctrine, plan, or doc.

### Common examples in BeQuite materials (all references only — never mandatory)

The following names appear in BeQuite files as *learning sources*. They are not automatic decisions.

- **Frontend / UI quality:** Impeccable, shadcn/ui, Tailwind, Radix, Aceternity, Magic, tweakcn
- **Scraping & automation:** Scrapy, Crawlee, Firecrawl, Playwright, Puppeteer, Cheerio, Trafilatura, Crawl4AI, Browser-use, Browserless, Colly, Crawl4AI, AutoScraper
- **Backend frameworks:** NestJS, Next.js, FastAPI, Express, Django, Hono, Fastify, tRPC
- **Database:** PostgreSQL, MongoDB, SQLite, Redis, Supabase, Neon, RDS, Drizzle, Prisma, Kysely
- **Deployment / hosting:** Docker, Nginx, PM2, systemd, Vercel, Fly.io, Render, Railway, Cloudflare Workers, AWS Lambda
- **Testing:** Playwright, Vitest, Jest, Pytest, Cypress, Testcontainers, Pact, MSW
- **Automation:** Make, Zapier, n8n, Temporal, Inngest, Trigger.dev, webhooks, queues
- **Workflow / agent patterns:** Spec Kit, BMad Method, OpenClaw, Hermes-style agents, Cline Memory Bank, AGENTS.md
- **Auth:** Better-Auth, Clerk, Auth0, NextAuth, Supabase Auth, Firebase Auth, Descope, Keygen
- **Email:** Resend, Postmark, SendGrid, Mailgun
- **Observability:** Sentry, Datadog, Axiom, OpenTelemetry, Better Stack
- **Secrets management:** Doppler, Infisical, AWS Secrets Manager, 1Password Secrets Automation

**Every name above is a reference and learning source, not an automatic decision.**

---

## The 10 decision questions

Before adopting any major tool, library, framework, or method, BeQuite must answer:

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

If you cannot answer all 10, you are not ready to pick. Go back to `/bq-research`.

---

## How to phrase recommendations

**Do not say:** "Use X."

**Say:** "X is one candidate. Research and compare against other options. Use it only if it fits this project."

This applies to:

- Skill files
- Command files
- Doctrine files
- Plans (IMPLEMENTATION_PLAN.md)
- ADRs
- Spec docs
- Commit messages
- Chat with users

---

## The decision section (mandatory before any tool pick)

Every major tool, library, framework, or method pick must produce a decision section.

### Format

```markdown
## Decision: <choice>

**Problem:** (1-2 sentences — what are we solving?)
**Options considered:** (3+ named alternatives, with one-line summary each)
**Sources / references checked:** (URLs with date accessed)
**Best option:** <X>
**Why it fits this project:** (concrete reasons tied to the 10 questions)
**Why other options were rejected:** (per option, one reason each)
**Risk:** (what could go wrong with this pick)
**Cost / complexity:** (price, install size, maintenance burden)
**Test plan:** (how we will know it's working)
**Rollback plan:** (how to back out if wrong)
```

### When to write a full ADR

| Project size / sensitivity | Decision format |
|---|---|
| Small / prototype / spike | Short inline section in the plan or commit message |
| Standard SaaS / app | Full decision section in IMPLEMENTATION_PLAN §11 or §12 |
| Large / regulated / mission-critical | Full ADR at `.bequite/decisions/ADR-XXX-<tool>-choice.md` |

ADR path convention (for project-level tool ADRs, inside the target project): `.bequite/decisions/ADR-<NNN>-<short-slug>.md`. Increment NNN per project.

(BeQuite's own framework-level ADRs live at `docs/decisions/`. Tool-neutrality formalizes there as ADR-003.)

---

## Research-depth rule

BeQuite must not only research stack choices.

Equally important dimensions of research:

- Project domain
- User needs
- Competitors
- Failure modes
- Success patterns
- UX expectations
- Security risks
- Scalability risks
- Deployment risks
- Differentiation opportunities

**Tool choice comes AFTER project understanding, not before.**

This is why `/bq-research` covers 11 dimensions, not 1. Stack is dimension 1 of 11.

---

## Implementation rule (do not auto-install)

By default, BeQuite does NOT add:

- Dependencies (any package)
- Scraping tools
- Frontend libraries
- Docker
- Testing frameworks
- Deployment tools
- Monitoring tools
- Auth libraries

Only add a tool when ALL six are true:

1. The project genuinely needs it
2. It is justified (decision section written)
3. It is compatible with the existing stack
4. It does not overcomplicate the project
5. It has a clear test plan
6. It has a rollback path

If any of those 6 fail → don't add it.

---

## Learn from popular tools, but think independently

BeQuite learns from many sources — Spec Kit, BMad Method, Cline Memory Bank, Impeccable, Anthropic Skills format, Linux Foundation AGENTS.md, industry doctrines.

BeQuite does **not** copy any of them blindly.

**The final decision must fit the project, not the example.**

---

## Where this rule applies (every domain)

- Frontend
- UI/UX
- Backend
- Database
- Authentication
- Security
- Scraping
- Crawling
- Browser automation
- General automation
- Testing
- DevOps
- Cloud / VPS
- Deployment
- Monitoring
- Logging
- Documentation
- Agent workflow
- Multi-model planning
- Release process

---

## Enforcement

This rule is enforced by:

1. **Every skill file** — has a Tool-neutrality section reminding readers
2. **Every command file** (for the 8 tool-touching commands) — has the same reminder
3. **CLAUDE.md** — surfaces the principle at session start
4. **ADR-003** — formalizes the decision
5. **`/bq-plan`** — refuses to lock a plan that names tools without a decision section
6. **`/bq-implement`** — refuses to install a new dependency without an inline decision or ADR
7. **`/bq-research`** — covers 11 dimensions of research (not just stack)
8. **`/bq-review` + `/bq-red-team`** — flag any "use X" claim without justification

---

## How to use this rule

When reading any BeQuite file that names tools:

1. Treat each name as a **candidate** to evaluate, not a default to use
2. Apply the 10 decision questions to the project
3. Write a decision section before adopting
4. Commit the section alongside the change

When you see the phrase "X is one candidate. Research and compare against other options. Use it only if it fits this project." — that's the canonical phrasing every BeQuite material aspires to.

---

## Anti-patterns to refuse

- ❌ "Use Drizzle." → ✅ "Drizzle is one candidate. Verify it fits this project's stack and scale before adopting."
- ❌ "Install shadcn/ui." → ✅ "shadcn/ui is one candidate for the component layer. Compare against alternatives before installing."
- ❌ "Default to Vercel." → ✅ "Vercel is one candidate. Compare cold-start, region count, function duration limits, and pricing against alternatives for this specific project."
- ❌ "Just add Docker." → ✅ "Docker is one candidate for containerization. Determine first whether containerization is needed at all for this project."

Apply this transformation to every tool mention in every BeQuite file.
