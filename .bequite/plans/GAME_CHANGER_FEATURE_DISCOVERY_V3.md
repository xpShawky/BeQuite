# Game-Changer Feature Discovery V3 (alpha.22) — 20 fresh candidates

**Rules honored:** zero V2 repeats · zero already-built features · zero internal-reliability items (game changer = user can do a new valuable thing, taxonomy type 1) · nothing built now — ranked proposals only.
**Method note (honest):** ranked from ecosystem patterns (Claude Code skill packs, guard-skills, n8n/Activepieces-style automation, indie-hacker/freelancer tooling, course/RAG/UI-builder platforms, MENA gaps) + this project's own demand history. Live per-idea market validation is deferred to approval time via C6 `/bq-pain-radar` + `/bq-research` — confidence values below reflect that.
**Columns:** Conf = build-feasibility confidence · $$ = monetization potential · YT = YouTube/demo potential · Shape = command/skill/argument/template/roadmap · Overlap → verdict.

| R | Idea | What the user can newly do | Conf | $$ | YT | Shape | Overlap | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | **/bq-offer — Offer Builder** | turn skills/results into a productized offer: package, deliverables, pricing tiers, guarantee, offer-page copy | 85% | high | high | command (later) | complements C8 proposal (per-client) — offer = standing package; user already hinted "bq-offer" | **KEEP — strongest V3; build after C8 proves out** |
| 2 | **Migration Planner** | framework/version upgrade blueprint (deps diff, breaking-change map, phased plan, rollback) | 82% | med | high | argument `/bq-plan migration` | plan owns blueprints | **KEEP as argument** |
| 3 | **Interview Prep Engine** | job post + own profile → likely questions, answer drafts in own voice, gap study plan | 80% | med | high | argument `/bq-job-finder interview-prep` | job-finder owns the intake | **KEEP as argument** |
| 4 | **Landing Page Engine** | conversion-focused landing structure + copy (hero/proof/CTA) wired to Design DNA | 80% | high | high | argument `/bq-feature landing` + writing-dna | feature + frontend-design-system own builds | **KEEP as argument — not a command** |
| 5 | **Local Business Digitizer** | restaurant/clinic/shop → digital-presence blueprint (menu/booking/WhatsApp automation plan); MENA SMB gap | 75% | high | high | template+route (pain-radar → feature), command later if demand | C6 finds the pain; this packages the solution | **KEEP — template/route first** |
| 6 | **Content Repurposing Engine** | one pillar piece → multi-platform calendar (posts, shorts script, thread, email) in own voice | 78% | med | high | argument `/bq-writing-dna repurpose` | writing-dna owns voice | **KEEP as argument** |
| 7 | **SEO Content Brief Engine** | keyword → brief (intent, outline, entities, gap vs top results) | 75% | med | med | argument `/bq-writing-dna seo-brief` | writing/researcher | **KEEP as argument** |
| 8 | **Persona Engine** | real reviews/comments → evidence-based personas (feeds course/landing/proposal) | 74% | med | med | argument `/bq-pain-radar personas` | heavy C6 overlap | **MERGE into C6** |
| 9 | **Voiceover / Dubbing Script Engine** | bilingual AR/EN narration scripts with timing marks for courses/demos | 72% | med | high | argument `/bq-course narration` + localization-rtl | course/recording plan own it | **MERGE into C5** |
| 10 | **Contract / SOW Generator** | accepted proposal → SOW (milestones, IP, payment terms, change control) — template-based, explicit "not legal advice" | 70% | med | low | argument `/bq-proposal sow` | proposal family | **KEEP as argument** |
| 11 | **Pricing Strategist** | research-backed pricing for product/service/course (anchors, tiers, MENA purchasing power) | 72% | high | med | skill (feeds offer/proposal/course) | product-strategist extension | **MERGE into product-strategist skill** |
| 12 | **App Store Launch Kit** | ASO keywords, listing copy, screenshot plan, review-response templates | 68% | med | med | argument `/bq-release store-kit` | release launch-kit family (announce/proof/demo-video) | **KEEP as argument — V2 timing** |
| 13 | **Onboarding Flow Designer** | first-run UX: activation path, empty states, aha-moment design + metrics | 70% | med | med | skill reference inside frontend-design-system | UX family | **MERGE into frontend-design-system references** |
| 14 | **Community Pack** | Discord/Telegram community blueprint: structure, rules, onboarding, engagement calendar | 65% | med | med | template under launch planning | course/launch family | **PARK — revisit with course adoption** |
| 15 | **A11y Compliance Pack** | WCAG audit + prioritized remediation plan as client deliverable | 75% | med | low | argument `/bq-audit a11y` | audit + ux-ui-designer own WCAG | **KEEP as argument** |
| 16 | **Diagram Engine** | code/architecture → mermaid diagrams (flows, ERD, sequence) for docs/handoffs | 72% | low | med | argument `/bq-explain diagram` | explain/handoff | **KEEP as argument** |
| 17 | **Resume/CV DNA** | ATS-aware, honest resume tailoring per job post (proposal's no-overclaim rules apply) | 70% | med | med | argument `/bq-job-finder resume` | job-finder/writing-dna | **KEEP as argument** |
| 18 | **Test-Data Factory** | realistic seed/fixture data plan (shapes, edge cases, anonymization rules) | 68% | low | low | argument `/bq-test fixtures` | testing-gate | **KEEP as argument — low priority** |
| 19 | **Brand Kit Generator** | one questionnaire → name shortlist, logo brief, palette, type, social templates | 62% | med | high | roadmap (reference + design-DNA outward) | C3 reference adjacency | **PARK — C3 must mature first** |
| 20 | **Email Sequence Engine** | onboarding/launch/nurture sequences in own voice | 64% | med | low | argument `/bq-writing-dna sequence` | overlaps #6 repurposing | **REJECT as separate — fold into #6** |

## Summary verdicts

- **Build-track (future releases, in order):** #1 /bq-offer (only V3 candidate that earns a command) → #2 plan migration → #3 interview-prep → #4 feature landing → #6 repurpose.
- **Merged into existing surfaces:** #8→C6 · #9→C5 · #11→product-strategist · #13→frontend-design-system · #20→#6.
- **Parked:** #5 (template first) · #12 · #14 · #19. **Rejected as standalone:** #20.
- **Pattern confirmed:** 13 of 20 best-shaped as arguments/skills, not commands — the anti-bloat charter holds. Command count should grow by ~1 (offer) across the next several releases, not 20.

Nothing from this list is built in alpha.22. Promotion path: user approval → 15-step feature workflow → taxonomy shape check → build.
