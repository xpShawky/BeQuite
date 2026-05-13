# Motion plan

> Written by `/bq-presentation`. Per-slide motion + transitions. Motion must be deliberate. Match audience.

## Audience-fit motion baseline

- **Audience:** (cross-ref `PRESENTATION_BRIEF.md::audience`)
- **Motion intensity:** `<subtle | clear | engaging | cinematic | minimal>`
- **Banned transitions:** spin / cube / random / glitter / typewriter

## Format

- **Format:** `<pptx | html | both>`
- (Different plans apply per format)

---

## PPTX motion (morph-like discipline)

### Object naming convention

Stable IDs that the morph engine can recognize across slides:

| ID | Slide range | Notes |
|---|---|---|
| `hero-circle` | 1–4 | Logo mark that scales + repositions |
| `title-text` | 1, 5, 12 | Section title — stable across section opens |
| `chart-bar-N` | 8–10 | Each bar gets its own stable ID |

### Per-slide transition plan

| Slide | Transition | Objects involved | Trigger | Duration | Rationale |
|---|---|---|---|---|---|
| 1 → 2 | Morph | `hero-circle` (scale + reposition) | After 2.0s | 0.6s | Continues the opening visual story |
| 2 → 3 | Fade | — | On click | 0.4s | Section divider |
| 3 → 4 | Morph | `chart-bar-1..3` (grow) | On click | 0.8s | Data emphasis |
| (...)| | | | | |

### Morph-like rules to enforce

- Same object across sequential slides keeps the **same name** + similar bounding box
- Duplicate slides for elements that move/scale/fade
- Combine 1–2 transformations at a time (not all four — move + scale + fade + rotate)
- Micro-slides used sparingly (they bloat the file)
- Avoid excessive animation
- Don't let text collide
- Timing 0.3–0.8s for morph (longer feels slow on projectors)

---

## HTML motion (CSS/JS)

### Motion vocabulary (use restraint)

| Effect | Where | Rationale |
|---|---|---|
| Title glow intro | Slide 1 only | Earned: opening |
| Staged bullet reveal | Content slides | 100–200ms delay per bullet |
| Card focus transition | Comparison slides | Emphasis on the card being discussed |
| Light sweep | Section dividers | Resets attention |
| Smooth section transitions | Section breaks | 0.4–0.6s slide-fade |
| (...) | | |

### Animation library decision (per tool neutrality)

- **Candidates considered:** (CSS-only, GSAP, Motion One, Anime.js, vanilla)
- **Picked:** `<none yet | <choice>>`
- **Decision section ref:** `DECISIONS.md#ADR-XXX`
- **Reason:** (Problem / Options / Sources / Best option / Why / Why others rejected / Risk / Cost / Test plan / Rollback)

### Banned in HTML motion

- Random / noisy auto-play motion
- Parallax just for parallax's sake
- Frame-by-frame effect unless deeply justified
- Motion that runs while the speaker is talking (steals attention)

---

## Per-format trade-offs

| Effect | PPTX | HTML |
|---|---|---|
| Morph between shapes | Excellent (morph transition) | Possible (FLIP technique) |
| Cinematic camera moves | Limited | Excellent (CSS transforms) |
| Frame-perfect timing | OK | Excellent |
| Voice-recording flow | Excellent (PowerPoint built-in) | Different (browser tooling) |
| Audience familiarity | High (institutional) | Lower (modern product teams) |

If both PPTX and HTML are produced from the same content plan, **the story flow is identical**. Only the rendering of motion changes.

---

## Verification

- [ ] Every motion entry has a rationale
- [ ] No transition is "decorative" — each earns its place
- [ ] Timing fits audience (subtle for academic; cinematic for keynote)
- [ ] No text-collision risk
- [ ] No banned transitions
- [ ] PPTX object names stable across morph slides
- [ ] HTML animation library decision recorded (if any library considered)
