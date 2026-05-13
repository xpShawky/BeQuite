---
name: bequite-presentation-builder
description: BeQuite Presentation Builder — produces world-class PPTX or HTML presentations from a topic, files, brand assets, or research. Strict vs creative mode, variants, morph-like PPTX motion planning, CSS/JS HTML motion, brand asset extraction. Tool-neutral (no library installed by default).
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch
---

# bequite-presentation-builder — the presentation discipline

## Purpose

Encode the discipline behind BeQuite's `/bq-presentation` command. The presentation must **feel designed by a professional human**, not a generic AI deck. This skill is activated by `/bq-presentation` directly, and by `/bq-auto presentation ...`.

Outputs:
- Premium PPTX (editable in PowerPoint, supports speaker notes, suits institutional workflows)
- Cinematic HTML (browser slides with CSS/JS motion, modern responsive layout)
- Or both, from a single content plan

## When this skill activates

- `/bq-presentation ...`
- `/bq-auto presentation ...`
- `/bq-suggest` when user says: slides / presentation / lecture / PowerPoint / PPTX / keynote / course lesson / deck / convert PDF to slides / make lecture from Word file / screen recording / explain this topic visually

## What this skill knows

1. The 14-step workflow encoded in `.claude/commands/bq-presentation.md`
2. PPTX vs HTML trade-offs + when each wins
3. Morph-like motion planning for PPTX (the trick that makes PPTX feel cinematic)
4. CSS/JS motion vocabulary for HTML (without picking a library)
5. Design defaults that prevent AI-slop layouts
6. Strict vs creative content discipline
7. Brand asset extraction
8. Variants discipline (different *directions*, not color swaps)
9. Verification checklist before claiming complete

---

## PPTX vs HTML — picking the right format

### PPTX strengths
- Editable in PowerPoint / Keynote / Google Slides (import)
- Familiar to most institutional users
- Strong support for speaker notes
- Voice-recording workflow built into PowerPoint
- Offline delivery (one `.pptx` file)
- Easier to hand to non-technical collaborators

### PPTX limits
- Complex animations are harder to generate reliably
- Morph effects require careful slide / object planning
- Full cinematic effects may be capped by PowerPoint's animation engine

### HTML strengths
- Better for cinematic motion
- Better for custom animation
- Better for responsive layouts
- Better for premium interactive design
- Easier to control CSS/JS details
- Can feel like a modern product demo

### HTML limits
- Not everyone expects HTML slides
- Needs browser delivery (URL or local file)
- Less familiar for traditional academic users
- Voice-recording workflow is different (browser tooling, not PowerPoint)

### Decision rule

Do **not** force PPTX or HTML automatically. Recommend per audience + venue + delivery:

| Audience / context | Recommend |
|---|---|
| University lecture / conference / institutional | PPTX (with strong morph-like plan) |
| Product keynote / demo / cinematic | HTML |
| Mixed audience / wants both delivery modes | Both — single content plan, two renders |
| Quick internal share with non-technical users | PPTX |
| Pitch / investor deck | Either; HTML if cinematic motion matters, PPTX if exec wants to edit |
| Screen-recorded explainer | HTML (CSS/JS control over pacing) |
| Medical / scientific lecture | PPTX (familiar tooling + speaker notes + reference handling) |
| Course module / LMS-hosted | HTML (responsive) or PPTX (downloadable) — clarify |

Output the recommendation in `PRESENTATION_BRIEF.md` with: **best format / why / trade-offs / whether both versions are useful**.

---

## The 14-step workflow

(Encoded fully in `.claude/commands/bq-presentation.md`. Summary here for skill activation.)

1. Parse request — natural language + options
2. Memory-first context load
3. Source intake (files / folders / URLs / topic-only)
4. Content strategy → `CONTENT_OUTLINE.md`
5. Slide-by-slide plan → `SLIDE_PLAN.md`
6. Design strategy → `DESIGN_BRIEF.md`
7. Variants (when `variants>1`) → `PRESENTATION_VARIANTS_REPORT.md`
8. Motion + transition planning → `MOTION_PLAN.md`
9. Strict vs creative mode discipline
10. Brand asset extraction (when assets present)
11. Build output (only when explicitly requested; tool-neutral)
12. Verification (14-item checklist)
13. Final chat report
14. Update memory + logs + history

---

## Default design principles

Apply these unless the user explicitly overrides:

- Big readable titles
- Few lines per slide (max 3–5 bullets; ≤8 words/bullet)
- Clear hierarchy (one focal point per slide)
- Large font sizes (title 60–80pt, headline 36–48pt, body 24–32pt for projector; never below 18pt)
- Strong contrast (WCAG AA at minimum; AAA for large text on dark backgrounds)
- No crowded slides
- No tiny text
- No random icons
- No weak AI-looking layouts (no purple-blue gradients + Inter + stock-icon soup)
- No generic templates
- Consistent margins
- Consistent visual rhythm
- Clear slide purpose (if you can't say it in one sentence, the slide is wrong)
- Strong first-slide hook (not "Hello, today I'll talk about…")
- Clean final takeaway (one memorable line / one action)
- References handled cleanly (not jammed into a single tiny slide)

---

## AI-slop anti-patterns to reject

(Inherits from `bequite-frontend-quality` skill; restated here for presentation context.)

❌ Inter font by default with no recorded reason
❌ Purple → blue gradients on every section divider
❌ Stock-icon soup (8 different icon styles on one deck)
❌ Decorative icons that don't add meaning
❌ Cropped people-photo headers from generic stock libraries
❌ Quote marks the size of titles
❌ "Synergy" / "leverage" / "ecosystem" boilerplate
❌ Sub-12pt body text
❌ Tables with no visual hierarchy
❌ Gray-on-color text below WCAG AA
❌ Nested cards (card inside card inside card)
❌ "Lorem ipsum" left in any output
❌ Slide titles like "Introduction", "Overview", "Conclusion" (be specific)
❌ Speaker notes that say "Talk about this slide" with no actual notes
❌ Reference slides crammed with 30+ citations in 8pt
❌ Random animations on every slide (motion fatigue)

---

## Variants discipline

Variants must be **different design directions**, not color swaps.

For each variant in `PRESENTATION_VARIANTS_REPORT.md`:

| Field | Notes |
|---|---|
| Variant name | e.g. "Academic Clean", "Premium Cinematic" |
| Visual direction | One paragraph describing the mood |
| Slide structure | Same content, different layout choices |
| Color palette | 3–5 hex codes with usage rule |
| Typography direction | Heading + body fonts; sizes per tier |
| Motion direction | Transition style + intensity |
| Pros | Bulleted strengths |
| Cons | Bulleted weaknesses |
| Best use case | When this variant wins |
| Preview path | File path if implemented |
| Recommendation | Rank 1..N + rationale |

Candidate directions (these are EXAMPLES, not defaults — pick per topic + audience):
- Academic Clean
- Premium Cinematic
- Corporate Keynote
- Medical Conference
- Minimal Lecture
- Dark Futuristic
- Light Editorial
- Data-Dashboard
- Student-Friendly
- Brand-Led

**Hard gate:** when `variants>1`, the agent pauses after presenting variants. The user picks the winner; then the agent merges and proceeds. No silent variant selection.

---

## Motion planning

### PPTX morph-like discipline

PPTX cannot do everything HTML can. The trick is **morph-like planning**:

1. **Same object across sequential slides** — if a logical element should "move", duplicate it across slides with consistent naming. The morph engine (PowerPoint's Morph transition) detects matching object names + similar bounding boxes and animates between them.
2. **Object naming convention** — use stable IDs like `hero-circle`, `title-text`, `chart-bar-3`. Don't rename between slides.
3. **Duplicate slides** — when an element must move/scale/fade, duplicate the slide and adjust the element's position/size/opacity on the duplicate.
4. **Repositioning vocabulary** — move, scale, fade, rotate, reposition. Combine 1–2 at a time, not all four.
5. **Micro-slides used sparingly** — they bloat the file; use only when motion really needs them.
6. **Avoid excessive animation** — every animation must earn its place.
7. **Don't let text collide** during transitions.
8. **Timing** — unobtrusive (0.3–0.8s typical for morph; longer feels slow on projectors).

For each PPTX slide, the plan lists: object names, transition type (morph / fade / none), trigger (on-click vs after-Xs), rationale.

### HTML motion vocabulary

Use restrained CSS/JS animation. Candidates (not defaults — research per tool neutrality):

- Title glow intro
- Soft object movement
- Side panels entering
- Scroll-like reference reveal
- Staged bullet reveal (each bullet appears with a 100–200ms delay)
- Card focus transitions (the card the speaker references gets emphasis)
- Light sweep
- Parallax (only if useful)
- Smooth section transitions
- Frame-by-frame effect (only when justified)

### Motion fit by audience

| Audience | Motion |
|---|---|
| Master's thesis / defense | Subtle, professional, restrained |
| Doctors / medical / scientific | Clear, readable, restrained |
| Students | Engaging but not childish |
| Product keynote | Cinematic, polished |
| Screen-recording demo | Visually clear, well-paced |
| Executive briefing | Minimal, on-message |
| Investor pitch | Confident, cinematic |
| Course / training module | Predictable, learner-paced |

---

## Strict vs creative

### Strict mode

Use when the user provides PDF / Word / scientific / lecture / institutional material.

Rules:
- Do not invent facts
- Do not add unsupported claims
- Preserve source meaning
- Summarize clearly without distortion
- Add references when sources are present
- Speaker notes stay grounded in source

Every factual statement on a slide must trace to a line in `REFERENCES.md` or a user-supplied note. Mark "STRICT" in `PRESENTATION_BRIEF.md`.

### Creative mode

Use when the user provides only a topic OR wants a keynote / marketing deck.

Rules:
- May suggest additional sections
- May propose hooks
- May add story flow
- May add examples
- **Must mark assumptions** explicitly in `ASSUMPTIONS.md` and on the affected slide
- Must cite researched facts when research was used

If both `strict=true` and `creative=true` are passed → strict wins; warn the user.

---

## Brand asset extraction

When the user provides logo / images / screenshots / a brand kit / a brand reference URL:

1. **Inspect** the visual style — palette, typography, layout mood, icon style.
2. **Extract a palette** — 3–5 hex codes + usage rule (primary, secondary, accent, background, text).
3. **Identify typography mood** — geometric sans / humanist serif / condensed display / mono / etc.
4. **Identify layout mood** — dense / airy / editorial / minimal / data-heavy.
5. **Identify icon style** — outline / filled / duotone / illustrated / none.
6. **Use consistent visual language** across the deck.
7. **Do not copy unrelated brands** — never include Apple logos in a non-Apple deck, etc.
8. **Write to `DESIGN_BRIEF.md` first**, before building any slide.

Example (if user provides BeQuite assets):
- Black premium background
- Gold / yellow gradients
- Silver / gold wordmark
- Cute astronaut agent
- Space / cloud / glow mood
- Premium cinematic feel

→ Build the deck in that identity. Verify the wordmark + agent appearance against the user's actual assets (no hallucinated logos).

---

## Verification checklist

Before claiming complete, verify:

- [ ] Each slide has ONE clear purpose
- [ ] Text is readable at presentation distance
- [ ] Slides are not crowded
- [ ] Opening hook is strong
- [ ] Story flow is clear
- [ ] References are correct
- [ ] Images are purposeful
- [ ] Branding is consistent
- [ ] Animations earn their place
- [ ] Transitions are not distracting
- [ ] Speaker notes align with slides
- [ ] Output format suits audience
- [ ] All source claims supported in strict mode
- [ ] Output file is usable by target user

Result → `EXPORT_LOG.md` + `VERIFY_REPORT.md` if full verify follows.

---

## Tool neutrality

⚠ **Every PPTX library, HTML slide framework, animation library, and export tool is a CANDIDATE, not a default.**

Do NOT install `python-pptx`, `pptxgenjs`, `reveal.js`, `Slidev`, `Marp`, `Spectacle`, `Impress.js`, `GSAP`, `Motion One`, or `Playwright` by default. Each requires a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`:

Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan.

Recorded in `.bequite/state/DECISIONS.md` and referenced from `EXPORT_LOG.md`.

---

## Operating modes (alpha.12, composable)

| Mode | Effect on presentation work |
|---|---|
| `deep` | Full 11-dim research before content strategy; competitor / failure-mode scan when relevant; multi-variant strongly suggested |
| `fast` | Skip extensive research; use topic + memory; tight slide count; one variant |
| `token-saver` (`lean`) | Reuse cached research + targeted reads; compact briefs; one variant unless requested |
| `delegate` | Strong model writes BRIEF + OUTLINE + DESIGN_BRIEF + MOTION_PLAN; cheap model fills SLIDE_PLAN + SPEAKER_NOTES; strong model reviews against acceptance criteria |

---

## What this skill does NOT do

- Auto-install presentation tools
- Auto-publish to SlideShare / Google Slides / SharePoint / cloud storage
- Use copyrighted brand assets without explicit permission
- Override Iron Law X (every change ships in operationally complete state — the PPTX or HTML must open + render without errors)
- Override banned weasel words ("should work" / "appears to render" / etc.)
- Bypass any of the 17 hard human gates

---

## See also

- Command: `.claude/commands/bq-presentation.md`
- Memory layout: `.bequite/presentations/`
- UX/UI discipline: `.claude/skills/bequite-ux-ui-designer/SKILL.md`
- Front-end quality (AI-slop detection): `.claude/skills/bequite-frontend-quality/SKILL.md`
- Tool neutrality: `.bequite/principles/TOOL_NEUTRALITY.md`
- Operating modes: `commands.md` §Operating Modes
- Memory-first behavior: `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`
- Workflow advisor (mode controller): `.claude/skills/bequite-workflow-advisor/SKILL.md`
