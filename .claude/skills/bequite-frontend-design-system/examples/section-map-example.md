# Section Map — worked example: ClinicFlow

Purpose: a fully filled section map showing the richer per-section entry format for one real product, so middle sections stay on-DNA from hero to footer.

| Field | Value |
|---|---|
| Product | ClinicFlow — clinic booking platform |
| Surfaces | `/` marketing landing (public) · `/dashboard` staff dashboard (internal) |
| Stack | Next.js (App Router) + Tailwind CSS |
| Dev URL | `http://localhost:3000` (marketing) · `http://localhost:3000/dashboard` (staff) |
| DNA reference | `../DESIGN_DNA.md` (calm clinical teal in OKLCH, tinted-neutral backgrounds, humanist-sans display + clean-sans body, no purple/pink AI gradients) |
| Contrast target | AA for marketing (body 4.5:1, large text 3:1, UI/focus 3:1) · lean AAA (7:1 / 4.5:1) for dashboard critical actions |
| Sibling files | `./design-dna-example.md` (DNA template), `./continuity-gate-example.md` (gate report), `../SKILL.md` (loop + gate) |

Brand adjectives drive every "Visual role" below: **trustworthy, calm, efficient.** Every section is checked against the same DNA — that is the point of the map.

---

## Page `/` — marketing landing (AA)

### 1. Nav

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Orient, route to primary CTA (Book a demo), set brand tone in first 200ms |
| Source file | `app/(marketing)/_components/nav.tsx` |
| Component | `<MarketingNav>` |
| Visual role | Quiet anchor — establishes teal accent + body type without competing with hero |
| Content rules | Logo + max 5 links + 1 primary CTA. Link labels sentence case, no all-caps. No tagline crammed into nav. |
| Layout constraints | Sticky top, height 64px desktop / 56px mobile. Tinted-neutral background, 1px hairline border on scroll only. CTA min touch 44x44pt. |
| Responsive behavior | Links collapse to a disclosure menu < 768px. Disclosure toggle 44x44pt; panel traps focus; Esc closes. |
| Known risks | CTA button can drift to a purple/pink gradient pulled from a generic template — must stay DNA teal. Sticky shadow can over-darken and break the calm tone. |
| Acceptance criteria | Logo + CTA contrast >=4.5:1 on tinted-neutral; CTA uses DNA teal (no gradient); no all-caps labels; focus ring visible at 3:1; touch targets >=44x44pt with >=8dp spacing; passes continuity gate (type + color + spacing match DNA). |

### 2. Hero

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | One-sentence value prop + primary CTA; convey trustworthy + calm immediately |
| Source file | `app/(marketing)/_components/hero.tsx` |
| Component | `<Hero>` |
| Visual role | Loudest section by design — but loud via type scale + whitespace, not via gradient noise |
| Content rules | One H1 (humanist display), one supporting line (body, <=2 sentences, measure 45-75ch), one primary + one optional secondary CTA. No stacked badges. |
| Layout constraints | Single column < 1024px; split (copy + product still) >= 1024px. Headline line-height 1.1-1.2; body 1.5-1.7. Vertical rhythm on 8pt scale. |
| Responsive behavior | Product still drops below copy on mobile, never crops the headline. Entrance reveal animates transform+opacity only, 300-500ms ease-out `cubic-bezier(0.16,1,0.3,1)`; reveal-safe if JS fails. |
| Known risks | This section usually looks fine — it is the baseline the rest of the page must match, so over-polishing it widens the gap to drifting middle sections. |
| Acceptance criteria | H1 contrast >=4.5:1 (>=3:1 if large); body >=16px at 45-75ch; CTA = DNA teal, no gradient; motion respects `prefers-reduced-motion: reduce`; no all-caps headline; renders without JS; passes continuity gate as the reference frame. |

### 3. How-it-works

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Reduce booking anxiety by showing 3 simple steps |
| Source file | `app/(marketing)/_components/how-it-works.tsx` |
| Component | `<HowItWorks>` |
| Visual role | Calm explainer — quieter than hero, still clearly on-brand teal accents |
| Content rules | Exactly 3 steps. Step titles sentence case. Numbered eyebrow allowed ONLY as a <=4-word label at 0.05-0.12em tracking. Body copy 45-75ch. |
| Layout constraints | 3 columns >= 1024px, 1 column below. Numbers as DNA-teal accent, not decorative gray. Consistent 8pt gaps. |
| Responsive behavior | Steps stack vertically with connector line on mobile. Connector hidden if it would crowd < 360px. |
| Known risks | **Classic drift hotspot:** tempts an all-caps numbered eyebrow ("STEP 01 — CREATE ACCOUNT") with wide tracking — violates all-caps rule (<=4 words, 0.05-0.12em only). Also tends to introduce a second accent color for "variety." |
| Acceptance criteria | Step text contrast >=4.5:1; eyebrow is sentence case OR a <=4-word all-caps label at 0.05-0.12em tracking; only DNA teal accent (no new color); numbers >=3:1 against background; 8pt spacing; passes continuity gate (no new color/type introduced). |

### 4. Features

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Show what ClinicFlow does for clinics (scheduling, reminders, records) |
| Source file | `app/(marketing)/_components/features.tsx` |
| Component | `<Features>` |
| Visual role | Substantive middle section — the highest drift risk on the page |
| Content rules | Each feature: real verb-led title (sentence case) + 1-2 sentence body at 45-75ch. No filler "Lorem"-flavored copy. Icons must be semantically distinct per feature. |
| Layout constraints | Asymmetric or 2-up layout preferred over a flat 3-card grid. Card padding on 8pt scale; consistent corner radius matching DNA. |
| Responsive behavior | Reflows to single column < 768px without orphaned icons. Hover lifts via transform/opacity only, 200-300ms; never animates the icon image on hover. |
| Known risks | **Classic drift hotspot:** Features tends toward an identical 3-card icon grid with interchangeable generic icons and copy that says nothing — the #1 "AI-looking middle section" tell. Second risk: card background drifts off the tinted-neutral palette into pure white, breaking calm tone. |
| Acceptance criteria | Title + body contrast >=4.5:1; icons are distinct and meaningful (not 3 near-identical glyphs); copy is specific, not filler; layout is NOT a flat identical 3-card grid OR justified in DESIGN_DNA notes; card bg on tinted-neutral; hover motion transform+opacity only with reduced-motion fallback; passes continuity gate. |

### 5. Social proof / testimonials

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Build trust with real clinic quotes + outcomes |
| Source file | `app/(marketing)/_components/social-proof.tsx` |
| Component | `<SocialProof>` |
| Visual role | Warm trust anchor — reinforces "trustworthy" adjective |
| Content rules | Real-shaped quotes with attributable name + clinic role. Logos grayscale-to-color on a tinted band. No fabricated 5-star clusters or fake counts. |
| Layout constraints | Quote measure 45-75ch; line-height 1.5-1.7. Logo row on consistent baseline, equal optical sizing. |
| Responsive behavior | Carousel becomes swipe on mobile with visible, 44x44pt controls; auto-advance disabled under `prefers-reduced-motion: reduce`. |
| Known risks | Logo wall can pull brand colors that clash with DNA teal; auto-advancing carousel often ships without a reduced-motion stop and without keyboard controls. |
| Acceptance criteria | Quote contrast >=4.5:1; controls >=44x44pt and keyboard reachable with >=3:1 focus ring; no autoplay when reduced-motion is set; logos do not introduce competing accents that clash with DNA teal; passes continuity gate. |

### 6. Pricing

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Convert — clear tier comparison + primary CTA |
| Source file | `app/(marketing)/_components/pricing.tsx` |
| Component | `<PricingTable>` |
| Visual role | Decisive but calm — one highlighted tier, not a rainbow of badges |
| Content rules | Tier names sentence case; feature rows scannable. One "recommended" highlight max. Currency + interval explicit. No dark-pattern strikethroughs. |
| Layout constraints | 3 tiers side-by-side >= 1024px. Highlight uses DNA teal border/fill, not a gradient. Numbers aligned on an 8pt grid. |
| Responsive behavior | Tiers stack vertically < 1024px with the recommended tier first. CTAs remain >=44x44pt. |
| Known risks | "Recommended" tier frequently gets a purple/pink gradient or glow that violates DNA; feature checkmarks drift to a non-teal accent green. |
| Acceptance criteria | Price + feature text contrast >=4.5:1; highlight uses DNA teal (no gradient/glow); CTA >=44x44pt with >=8dp spacing; checkmarks within DNA palette; no all-caps tier names beyond <=4-word labels; passes continuity gate. |

### 7. FAQ

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Remove last-mile objections (HIPAA-adjacent, onboarding, cancellation) |
| Source file | `app/(marketing)/_components/faq.tsx` |
| Component | `<Faq>` |
| Visual role | Quiet utility — readable, accessible accordion |
| Content rules | Real questions in sentence case; answers 45-75ch. No marketing fluff masquerading as a question. |
| Layout constraints | Single-column accordion, max-width clamped to keep 45-75ch measure. Trigger row min height 44px. |
| Responsive behavior | Full-width < 768px. Accordion expand/collapse 200-300ms transform/opacity; content reveal-safe if JS disabled (open by default fallback). |
| Known risks | Accordion triggers often lack accessible state (`aria-expanded`) and visible focus; answer text width can blow past 75ch on wide screens, hurting readability. |
| Acceptance criteria | Question + answer contrast >=4.5:1; trigger has `aria-expanded` + focus ring >=3:1; measure stays 45-75ch; trigger height >=44px; reduced-motion respected; content readable with JS off; passes continuity gate. |

### 8. Footer

| Field | Value |
|---|---|
| Route | `/` |
| Purpose | Close the page — secondary nav, legal, contact, trust marks |
| Source file | `app/(marketing)/_components/footer.tsx` |
| Component | `<MarketingFooter>` |
| Visual role | Calm sign-off — darker tinted-neutral band, still on-DNA, not a dumping ground |
| Content rules | Grouped link columns with sentence-case headings. Real contact + legal links. No orphaned single-link columns. |
| Layout constraints | Multi-column >= 768px; link tap targets >=24x24 CSS px floor with >=8dp spacing. Headings on humanist display at small scale. |
| Responsive behavior | Columns stack to an accordion or single column < 768px without losing groupings. |
| Known risks | Footer is the most-ignored section — link contrast on the darker band frequently drops below 4.5:1; type scale and color often diverge from DNA because no one re-checks the footer. |
| Acceptance criteria | All link text contrast >=4.5:1 on the dark band; tap targets >=24x24 CSS px with >=8dp spacing; headings use DNA display font; colors match DNA teal/tinted-neutral; no all-caps beyond <=4-word labels; passes continuity gate (footer must match the same DNA as the hero). |

---

## Page `/dashboard` — staff dashboard (lean AAA on critical actions)

### 9. Sidebar nav

| Field | Value |
|---|---|
| Route | `/dashboard` |
| Purpose | Persistent navigation across staff workspace areas |
| Source file | `app/(dashboard)/_components/sidebar.tsx` |
| Component | `<DashboardSidebar>` |
| Visual role | Stable, low-noise frame — efficiency over decoration |
| Content rules | Icon + sentence-case label per item; active item clearly marked. No collapsing labels to cryptic icon-only without tooltip. |
| Layout constraints | Fixed left rail 240px expanded / 64px collapsed. Active state = DNA teal indicator. Items on 8pt vertical rhythm. |
| Responsive behavior | Off-canvas drawer < 1024px with a 44x44pt toggle; drawer traps focus and closes on Esc. |
| Known risks | Active-state indicator drifts to a non-teal accent; collapsed icon-only mode ships without tooltips/labels, hurting recognition and a11y. |
| Acceptance criteria | Label contrast >=4.5:1; active critical-nav indicator leans AAA >=7:1; active state uses DNA teal; collapsed mode keeps accessible names (tooltip/aria-label); toggle >=44x44pt with focus ring >=3:1; passes continuity gate. |

### 10. KPI summary cards

| Field | Value |
|---|---|
| Route | `/dashboard` |
| Purpose | At-a-glance daily metrics (today's appointments, no-shows, utilization) |
| Source file | `app/(dashboard)/_components/kpi-cards.tsx` |
| Component | `<KpiCard>` |
| Visual role | Efficient scan row — numbers first, calm supporting labels |
| Content rules | One metric per card: big number + sentence-case label + optional delta. Real data wired; loading + error states defined. No decorative sparkline noise without meaning. |
| Layout constraints | Equal-height cards on an 8pt grid; number uses display font, label body. Delta color within DNA palette (teal/neutral; reserved semantic for true negatives). |
| Responsive behavior | 4-up >= 1280px, 2-up >= 768px, 1-up below. Skeleton loaders match final card height to avoid layout shift. |
| Known risks | **Classic drift hotspot:** KPI cards become an identical 4-card grid with placeholder numbers and a hardcoded green up-arrow on every card — mock data masquerading as live, plus an accent that is not DNA teal. |
| Acceptance criteria | Number + label contrast leans AAA >=7:1 (critical glance values); cards show real loading/empty/error states (no static mock numbers); delta colors within DNA palette; no layout shift on load; 8pt grid; passes continuity gate. |

### 11. Appointments table

| Field | Value |
|---|---|
| Route | `/dashboard` |
| Purpose | The core work surface — view, sort, filter, act on appointments |
| Source file | `app/(dashboard)/_components/appointments-table.tsx` |
| Component | `<AppointmentsTable>` |
| Visual role | Dense but legible — efficiency is the dominant adjective here |
| Content rules | Real columns (patient, time, provider, status, actions). Status chips use a DNA-aligned palette. Row actions reachable by keyboard. No all-caps column headers. |
| Layout constraints | Sticky header; row height >=44px for the action affordance; zebra/tinted rows on the neutral scale. Column text honors readable measure where wrapping. |
| Responsive behavior | Horizontal scroll with frozen first column < 1024px, OR card-per-row layout below 768px. Sort controls remain keyboard + touch reachable. |
| Known risks | Column headers tempt all-caps with wide tracking; status chip colors drift into a random traffic-light palette that ignores DNA teal; dense rows drop row-action contrast below threshold. |
| Acceptance criteria | Cell + header text contrast >=4.5:1 (status of critical actions leans AAA >=7:1); headers sentence case (or <=4-word labels at 0.05-0.12em); status chips within DNA palette; row actions keyboard reachable with >=3:1 focus ring; row action targets >=44x44pt; passes continuity gate. |

### 12. Empty state

| Field | Value |
|---|---|
| Route | `/dashboard` |
| Purpose | Guide a new clinic / quiet day — what to do when there are no appointments |
| Source file | `app/(dashboard)/_components/appointments-empty.tsx` |
| Component | `<AppointmentsEmptyState>` |
| Visual role | Helpful, calm — never a dead blank panel |
| Content rules | One plain-language line explaining the state + one clear primary action ("Book first appointment"). No generic "No data" with no next step. Sentence case throughout. |
| Layout constraints | Centered within the table region, on 8pt rhythm. Illustration (if any) on-DNA, monochrome teal — not a stock gradient blob. |
| Responsive behavior | Scales down gracefully; CTA stays >=44x44pt and above the fold on mobile. |
| Known risks | Empty state is frequently skipped or shipped as bare "No results," and any illustration tends to import an off-brand gradient that violates the no-purple/pink rule. |
| Acceptance criteria | Copy contrast >=4.5:1; one real, actionable CTA (not just "No data"); CTA = DNA teal, >=44x44pt; illustration on-DNA (no purple/pink gradient); distinct loading + error states exist alongside this empty state; passes continuity gate. |

### 13. Booking modal

| Field | Value |
|---|---|
| Route | `/dashboard` (overlay) |
| Purpose | Create / edit an appointment — a critical action |
| Source file | `app/(dashboard)/_components/booking-modal.tsx` |
| Component | `<BookingModal>` |
| Visual role | Focused, trustworthy task surface — calm form, decisive confirm |
| Content rules | Labeled fields (no placeholder-as-label), inline validation, explicit primary (Confirm) + secondary (Cancel). Sentence-case labels. Error text specific, not "Invalid input." |
| Layout constraints | Centered dialog, max-width clamped for 45-75ch field help; controls on 8pt scale. Confirm = DNA teal solid; Cancel = quiet neutral. |
| Responsive behavior | Full-screen sheet < 640px. Focus trapped on open, returned on close; Esc closes (unless unsaved-changes guard). Enter/exit motion 200-300ms transform+opacity with reduced-motion fallback. |
| Known risks | Confirm button drifts to a gradient; modal ships without focus trap / return-focus and without a reduced-motion fallback; validation errors are generic and low-contrast. |
| Acceptance criteria | Field labels are real `<label>`s (not placeholders); confirm action contrast leans AAA >=7:1 (critical); Confirm = DNA teal solid, no gradient; focus trapped on open + returned on close; Esc + keyboard fully operable; error text contrast >=4.5:1 and specific; reduced-motion respected; targets >=44x44pt; passes continuity gate. |

---

## Continuity check (every section, every time)

Each entry above must clear the Design Continuity Gate before it is marked done. The gate (see `../SKILL.md` and `./continuity-gate-example.md`) verifies, per section, that it matches DNA on:

- [ ] Color — only DNA teal + tinted-neutral; no purple/pink AI gradient introduced
- [ ] Type — humanist display + clean body; body >=16px; measure 45-75ch; line-height 1.1-1.2 headings / 1.5-1.7 body
- [ ] All-caps — only on <=4-word labels at 0.05-0.12em tracking
- [ ] Contrast — AA (4.5:1 / 3:1) on marketing; lean AAA (7:1 / 4.5:1) on dashboard critical actions
- [ ] Touch + focus — targets >=44x44pt (24x24 CSS px floor), >=8dp spacing, focus ring >=3:1
- [ ] Motion — transform+opacity only, ease-out (no bounce), reduced-motion fallback, reveal-safe
- [ ] State honesty — real empty / loading / error states; no mock data masquerading as live
- [ ] No drift — section matches the hero's DNA, not a generic template
