# BeQuite — New Capability Feature Ideas (2026)

**Status:** PROPOSAL / REPORT ONLY — ranked ideas for *new capability commands* in the spirit of `/bq-live-edit`, `/bq-make-money`, `/bq-presentation`, the scraping skill. Nothing here is built. A future release picks from this.
**Generated:** 2026-06-05 · evidence base: 4 cited demand-and-gap research streams (build / content / intelligence / earn). Source URLs are in the per-item lines + `.bequite/research/` notes for this cycle.
**Lens:** every candidate is screened to be **lightweight** — a slash command + a skill + markdown memory, tool-neutral, no daemon/dashboard/heavy dependency. BeQuite has no runtime, so "monitoring" features are reframed as **on-demand snapshot + diff-against-saved-baseline** (the user re-runs; BeQuite compares to last saved state).

---

## The 4 loudest 2026 demand signals (what to build around)

1. **The "last 20% / last-mile" gap is the #1 builder pain.** AI gets you to ~80% (the demo); the invisible 80% of real work — deploy, env vars, auth/webhooks, edge cases, security, perf, monitoring, launch — is where everyone stalls. "Three hours to build, four days to deploy." Now an industry-named problem. ([XDA](https://www.xda-developers.com/tested-every-ai-vibe-coding-tool-finish-real-project-all-choke-at-same-point/), [blendingbits](https://blendingbits.io/p/vibe-codings-last-mile-problem), [HBR](https://hbr.org/2026/03/the-last-mile-problem-slowing-ai-transformation))
2. **Vibe-coded apps are leaking data at scale.** ~5,000 of 380,000 apps actively leaking; 11% leaked Supabase keys; Moltbook leaked 1.5M tokens in 3 days (client-side key + no RLS); 40–62% of AI code has vulns. The failures are *specific + patternable*. ([AI2Work](https://ai2.work/blog/vibe-coding-s-security-reckoning-380-000-apps-expose-corporate-data), [ogwilliam](https://blog.ogwilliam.com/post/moltbook-hack-supabase-vibe-coding))
3. **Distribution/launch is the new bottleneck, not building.** "Building is no longer the hard part… the first 10 signups feel like pulling teeth… the part AI didn't help is distribution." ([Indie Hackers](https://www.indiehackers.com/post/i-shipped-a-productivity-saas-in-30-days-as-a-solo-dev-heres-what-ai-actually-changed-and-what-it-didn-t-15c8876106))
4. **Content/marketing's pain isn't "can AI write it" — it's fragmentation + no persistent brand context.** ~50% use ChatGPT one-off with "no persistent brand context"; the next tier suffers "brand voice drift at scale." A markdown `BRAND_VOICE.md` every command reads is *exactly* the missing layer. ([averi.ai](https://www.averi.ai/blog/the-state-of-ai-content-marketing-2026-benchmarks-report))

BeQuite is uniquely positioned for all four: they're **orchestration + checklists + persistent markdown memory + tool-neutral generation** — its core strengths, not new infra.

---

## ★ Build these 3 FIRST (highest demand × gap × fit × composes-with-existing)

| Rank | Command | Why first |
|---|---|---|
| 1 | **`/bq-ship`** — last-mile ship-readiness | THE loudest signal (the 80% problem). Pure orchestration BeQuite is built for; composes with `/bq-verify`. |
| 2 | **`/bq-brand`** — Brand Voice Memory (keystone) | Cheapest possible (one markdown file), and it *unlocks an entire content track* by giving every content command persistent brand context — the exact gap the market has. |
| 3 | **`/bq-secure-launch`** — vibe-coding security scan | Urgent + patternable (380k apps leaking); protects every builder; composes with `bequite-security-reviewer`. |

---

## Track A — BUILD & SHIP

| Command | Gap it fills (demand) | BeQuite shape | Leverage · Effort |
|---|---|---|---|
| **`/bq-ship`** | the "last 20%": env vars, dev-vs-prod DB drift, N+1, pagination, webhook/OAuth, perf, monitoring, launch — diagnoses the *specific* holes by project type + walks the fix | skill `bequite-ship-readiness` · memory `.bequite/ship/SHIP_READINESS.md` · composes with `/bq-verify` + devops/security skills | **High** · M |
| **`/bq-secure-launch`** | exposed service-role keys in client code, missing RLS, inverted access policies, hardcoded secrets, over-exposed schema — the exact vibe-coding leak patterns | skill `bequite-leak-scan` (grep + checklist) · memory `.bequite/audits/SECURITY_LEAK_SCAN.md` · extends `bequite-security-reviewer` | **High** · S–M |
| **`/bq-launch-kit`** | nobody hands a solo builder a concrete GTM: meta/OG tags, sitemap/robots, structured data, Product Hunt/Reddit/HN/directory submission copy, launch-day checklist | skill `bequite-launch-kit` · memory `.bequite/launch/LAUNCH_KIT.md` · composes with the content track | **High** · M |
| **`/bq-rebuild`** | "clone/recreate this site" is durable Fiverr/Upwork demand, but verbatim cloners produce IP-risky, framework-mismatched output — the real need is *rebuild the structure/flow in MY stack, cleanly* | skill `bequite-rebuild-from-reference` (analyze reference → structure spec → scaffold) + an **IP/originality gate** · composes with `/bq-uiux-variants` | **Med-High** · M |
| **`/bq-automate`** | builders know the outcome ("when X, do Y across 3 apps") but not the node graph, auth, webhooks, idempotency, or error paths | skill `bequite-automation-blueprint` · memory `.bequite/automation/AUTOMATION_PLAN.md` · tool-neutral (n8n/Make/Zapier/code as candidates) | **High** · M |
| **`/bq-chatbot`** | "chatbot on my data" (RAG) is a top build category but bolting an LLM on data → hallucinations, no chunking strategy, no grounding, injection exposure | skill `bequite-rag-design` (chunking/retrieval/grounding/eval-set/injection-defense) · composes with `bequite-security-reviewer` (OWASP LLM) · tool-neutral on vector store | **High** · M |

## Track B — EARN / DELIVER (services freelancers + agencies sell)

| Command | Gap it fills (demand) | BeQuite shape | Leverage · Effort |
|---|---|---|---|
| **`/bq-proposal`** | RFP volume up (166/yr avg); "bandwidth is proposal teams' #1 challenge for the first time in 5 years"; market $3.66B→$9.19B; SaaS targets mid-market, not freelancers | skill `bequite-proposal-builder` (parse RFP → compliance matrix → draft from a reusable **answer library** → gap flags) · memory `.bequite/proposals/` | **High** · M |
| **`/bq-client-report`** | agencies waste 8–15 hrs/wk turning a data export into a client-ready narrative; ChatGPT lacks persistent formatting memory | skill `bequite-report-narrator` (user pastes export + saved template → narrative + exception list) · memory `.bequite/reports/<client>/` | **High** · S–M |
| **`/bq-audit-site`** | productized SEO + accessibility + **AI-readiness** (GPTBot/ClaudeBot crawlability) audits are in demand but generic; AI-readiness auditing is brand-new | skill reuse `bequite-frontend-quality` + `security-reviewer` → sellable audit markdown/PDF · memory `.bequite/site-audits/` · *flags* where a real crawler is needed | **Med-High** · M |

## Track C — CONTENT / MARKETING / GROWTH (keystone-led)

| Command | Gap it fills (demand) | BeQuite shape | Leverage · Effort |
|---|---|---|---|
| **`/bq-brand`** ★keystone | "AI has no persistent brand context"; static style guides are "inconsistently applied" → voice drift at scale; SMBs pay $15K–40K for brand identity | skill `bequite-brand-voice` · memory `.bequite/brand/BRAND_VOICE.md` (voice/tone/lexicon/banned-words/audience/positioning + visual tokens) **read by every content command** | **High** · S |
| **`/bq-repurpose`** | teams spend ~70% of time reformatting; "insufficient repurposing" is the named scaling bottleneck; 10x formats → 3–5x reach | skill `bequite-content-atomizer` (1 source → 10 canonical formats) · memory `.bequite/content/REPURPOSE_PLAN.md` · reads `BRAND_VOICE.md` | **High** · M |
| **`/bq-seo-content`** (+`geo` mode) | programmatic-SEO failure = "missing template/publishing tooling"; GEO ("structure for AI extraction") is a *writing* task; AI-search converts far higher than Google organic | skill `bequite-seo-geo` (page template + data-merge schema + extraction-optimized structure) · memory `.bequite/content/SEO_GEO_PLAN.md` | **High** · M |
| **`/bq-email-sequence`** | email = $36 ROI/$1; 5 flows generate 80% of email revenue, yet solos skip them; AI misses voice | skill `bequite-email-sequences` · memory `.bequite/content/EMAIL_SEQUENCES.md` · reads `BRAND_VOICE.md` | **High** · S |
| **`/bq-social-kit`** | AI video skills surged 329% on Upwork; brand-matched scripts/hooks/carousel copy are the human bottleneck (BeQuite emits scripts/storyboards, not renders) | skill `bequite-social-content` · memory `.bequite/content/SOCIAL_KIT.md` | **Med-High** · S–M |
| **`/bq-lead-magnet`** | market shifted to ultra-specific snackable assets (15–25% vs 3% conversion); "a two-sentence checklist outperforms a beautiful ebook" | skill `bequite-lead-magnet` · markdown → tool-neutral PDF/HTML (reuse `/bq-presentation` export) | **Med-High** · S |
| **`/bq-marketing-copy`** | conversion copy is $750–3K/page; generic AI copy fails on voice + strategy | skill `bequite-conversion-copy` · memory `.bequite/content/SITE_COPY.md` · pairs with `bequite-frontend-quality` | **Med-High** · M |
| **`/bq-resume`** | 75% of resumes ATS-rejected pre-human; AI resumes flagged for cliché filler; 2026 ATS scores meaning + metrics | skill `bequite-resume-ats` · memory `.bequite/career/RESUME_PROFILE.md` · synergy with `/bq-job-finder` | **Med** (B2C-leaning) · S |

## Track D — INTELLIGENCE & VALIDATION

| Command | Gap it fills (demand) | BeQuite shape | Leverage · Effort |
|---|---|---|---|
| **`/bq-validate`** | validation-first is the 2026 solo doctrine; "120s validators" are shallow; serious go/no-go is still manual | composes `/bq-research` (11-dim) + `bequite-product-strategist` into a **GO/NO-GO/PIVOT verdict** with demand evidence + kill-criteria · memory `.bequite/validation/<idea>/` | **High** · S–M |
| **`/bq-competitor-intel`** | monitoring tools alert on raw diffs but don't *interpret strategy* ("dropped the free tier → moving upmarket") | skill `bequite-market-intel` (interpreted brief; saves baseline; diffs + explains on re-run — **on-demand, no daemon**) · memory `.bequite/intel/<competitor>/` | **High** · M |
| **`/bq-ai-visibility`** | new GEO category — "am I in the ChatGPT/Gemini/Claude/Perplexity answers?"; tools cost $49–599/mo | skill `bequite-ai-visibility` (query AI-answer surface for brand/competitor prompts, score, save baseline for diff) · memory `.bequite/visibility/` | **Med-High** · M |
| **`/bq-clean-data`** | analysts spend 40–80% on prep; solos can't justify an ETL stack for a one-off messy CSV | skill `bequite-data-prep` (profile → flag anomalies/dupes → write a reusable cleaning *recipe/spec*) · memory `.bequite/data-recipes/` · **not** an ETL runtime | **Med** · M |
| **`/bq-prep`** | interview *practice* tools are crowded; structured negotiation/high-stakes-meeting prep (BATNA, objection matrix, walk-away line, salary benchmarks) is underserved | skill `bequite-prep-coach` (research + prep pack; **not** a live in-call copilot) · memory `.bequite/prep/<scenario>/` · pairs with `/bq-job-finder` + `/bq-make-money` | **Med** · S |

---

## What NOT to build (the lightweight boundary — ADR-001 / ADR-004)

These have real demand but need a **runtime/daemon/dashboard/heavy dep** BeQuite must not own. Deliver the *content/analysis/prep layer* instead and let the user plug it into their tool:

- **Hosted support/FAQ bots** (need a live inference endpoint + widget) → ship the *knowledge base + answer playbook + escalation rules* as markdown, not the deployed bot.
- **Continuous monitoring with alerts** (price/reputation/website-change daemons) → use the **on-demand snapshot + saved-baseline diff** reframe (`/bq-competitor-intel`, `/bq-ai-visibility`).
- **Full-site crawlers / Lighthouse perf engines** (for `/bq-audit-site`) → scope to single-page + structured-data + a11y-tree + AI-readiness checklist; *note* where a real crawler is required.
- **Live in-call audio copilots** (for `/bq-prep`) → deliver the prep pack, not a live listener.
- **Verbatim site cloning** (for `/bq-rebuild`) → rebuild structure/flow in the user's stack with an IP/originality gate; never pixel-pirate.
- **Paid data-enrichment / ETL pipelines** (for `/bq-clean-data`) → write the cleaning recipe; don't call paid APIs by default.

## How they compose with the existing surface

- `/bq-ship` + `/bq-secure-launch` + `/bq-audit-site` extend `/bq-verify` + `bequite-security-reviewer` + `bequite-devops-cloud`.
- The whole content track reads one keystone file (`BRAND_VOICE.md`) and reuses `/bq-presentation`'s tool-neutral export + `bequite-frontend-quality`.
- `/bq-validate` composes `/bq-research` + `bequite-product-strategist`; `/bq-rebuild` composes `/bq-uiux-variants`; `/bq-resume` + `/bq-prep` pair with `/bq-job-finder` + `/bq-make-money`.
- Every new command goes through the **alpha.14 feature-addition workflow** and the **alpha.18 reliability discipline** (PROJECT_DNA, evidence-over-claims, hooks-eligible).

## Honest notes

- The **"earn" research stream hit a session cap** this cycle; its territory (proposals, client reports, audits, resumes) is covered by the content + intelligence streams above. A future pass can deepen pure-services ideas (automation-as-a-service packaging, lead-gen delivery).
- A few figures are single-source / secondary summaries (flagged UNVERIFIED in the stream notes): "70% reformatting time," "$15K–40K brand identity," "16+ martech tools." Treat as directional.
