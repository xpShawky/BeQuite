# Design Continuity Report — Cadence continuity-demo

**Generated:** 2026-06-04 (UTC)
**DNA:** `examples/continuity-demo/DESIGN_DNA.md` (locked)
**Checklist:** `.claude/skills/bequite-frontend-design-system/references/design-continuity-checklist.md`
**Effort level:** high (full section-by-section)
**Overall:** `before-drifted.html` = **FAIL** · `after-fixed.html` = **PASS**

This is the dogfood proof that the gate catches middle-section drift on a rendered multi-section page. Evidence below is from an **independent audit** (a fresh subagent that read the DNA + both HTML files + the checklist, with contrast ratios computed) — not self-assessment.

---

### Route: before-drifted.html

**Sections inspected:** Nav · Hero · Features · How it works · Testimonials · Footer (all 6, not a sample)
**Design DNA summary:** SaaS landing · grounded/steady/warm · clay `#b14a2e` on warm tinted paper · Fraunces display + Public Sans body · 4/8 spacing · cards ≤16px radius · no AI gradients · no gray-on-clay.

#### Issues found

| # | Section | Drift tell | CSS evidence | Severity | In DNA |
|---|---|---|---|---|---|
| 1 | Features | Nested cards (card-in-card) | `.feat-card` (L42) wraps `.feat-inner` (L43); markup L88/90/92 | **BLOCKER** | §6 no card-in-card |
| 2 | Features | ALL-CAPS multi-word titles | `.feat-title{text-transform:uppercase}` L45 → "ADAPTIVE TRAINING PLANS" etc. | HIGH | §3 |
| 3 | Features | Wide tracking on titles | `letter-spacing:0.22em` L45 (≈3× the 0.12em ceiling) | HIGH | §3 |
| 4 | Features | Off-scale title type / pure-white surface | `font-size:14px`, `background:#fff` (L42/45) | MEDIUM/LOW | §2/§3 |
| 5 | How it works | Purple→pink AI gradient on a full band | `.how{background:linear-gradient(135deg,#a855f7,#ec4899)}` L51 | **BLOCKER** | §2/§8 |
| 6 | How it works | `01/02/03` eyebrow markers as decoration | `.eyebrow` L54 → "01 — SET YOUR RACE" L100–102 | HIGH | §8 |
| 7 | How it works | Card radius ≥ 32px | `.blob{border-radius:36px}` L56 | HIGH | §5 |
| 8 | How it works | Arbitrary off-scale spacing | `62px` (L51), `13px 27px`, `21px` (L56) | MEDIUM | §4 |
| 9 | How it works | White body on mid-gradient < AA | `color:#fff` over magenta midpoint ≈ **3.12:1** | MEDIUM | AA |
| 10 | Testimonials | Gray-on-clay primary quote | `#9ca3af` on `#b14a2e` = **2.13:1** (L60–61) | **BLOCKER** | §2/§8 |
| 11 | Testimonials | Gray-on-clay cite / note | `#d9b8ac` = 2.93:1; `#c9a99e` = 2.48:1 (L62/64) | HIGH | §2 |
| 12 | Testimonials | Text-overflow risk | `.overflow-note{width:220px}` + long unbroken token, no `overflow-wrap`/`min-width:0` (L64/109) | MEDIUM | §8 |

#### Quality-cliff check

- **Strongest section:** Hero (on-DNA, Fraunces, clay CTA, 5.28:1 body).
- **Weakest sections:** Features, How it works, Testimonials — **each carries ≥1 BLOCKER.** The purple→pink band reads as a different product; the gray quote is barely legible (2.13:1).
- **Squint test:** FAIL — the gradient + low-contrast clay sections don't read as the same brand as the hero.
- **Slop test:** FAIL — Features/How-it-works are guessable from "SaaS landing" alone (3-up icon cards + 01/02/03 steps).

**Route status: FAIL** (3 of 6 sections fail, 3 BLOCKERs). The drift is real — confirmed against the markup, not the file's self-labels.

---

### Route: after-fixed.html

**Every BLOCKER/HIGH above corrected in CSS** (not relabeled):

| Before tell | Fix (after-fixed.html) |
|---|---|
| Nested cards | single-depth `.feat-card{background:var(--paper);border-radius:var(--r-md)}` (L40); no `.feat-inner` |
| ALL-CAPS + 0.22em titles | `<h3>` sentence-case Fraunces, no transform/tracking (L42, L81–83) |
| Purple→pink gradient | `.how{background:var(--paper)}` (L46) — clay identity restored |
| 01/02/03 eyebrows | real clay Fraunces numerals 1/2/3 in a genuine 3-step sequence (`.num` L49, L92–94) |
| 36px blob radius | hairline `border-left:2px solid var(--line)` step, no card radius (L48) |
| Off-scale spacing | `--s-24`/`--s-8`/`--s-6`/`--s-2` (L46–50), all on 4/8 |
| Gray-on-clay quote (2.13:1) | `blockquote{color:var(--paper)}` = **5.02:1** (L54–55) |
| Overflow token | `.tag{max-width:100%;min-width:0;overflow-wrap:anywhere}` (L57) |

#### Residual caught by the gate (and closed)

The independent audit flagged **one** residual in the first cut of `after-fixed.html`: `.testi cite` at `#f6ddd3` on clay = **4.17:1**, a hair under AA-body (4.5:1) for 15px normal text. Per verify-before-done, it was fixed to `color:var(--paper)` (**5.02:1**), hierarchy carried by size, not opacity (opacity would re-muddy the contrast). This is the gate doing its job on the author's own work.

#### Quality-cliff check

- No section below the hero. Features/How-it-works/Testimonials now share Fraunces-on-warm-paper, clay accent, 4/8 rhythm. Squint + slop tests pass.

**Route status: PASS.**

---

## Independent verification

Auditor: a fresh general-purpose subagent (no knowledge of intent) that read `DESIGN_DNA.md`, both HTML files, and `design-continuity-checklist.md`, computed contrast ratios, and reported per-section. Conclusion (verbatim intent): *the demo is honest — `before` genuinely drifts (3 real BLOCKERs) and FAILs; `after` corrects each tell in CSS and PASSes; the only blemish was the `cite` 4.17:1, now closed.*

## Roll-up

| Route | Sections | BLOCKER | HIGH | MEDIUM | LOW | Status |
|---|---|---|---|---|---|---|
| before-drifted.html | 6 | 3 | 4 | 4 | 1 | FAIL |
| after-fixed.html | 6 | 0 | 0 | 0 | 0 (residual closed) | PASS |

**Final status: the Design Continuity Gate demonstrably catches middle-section drift (before → FAIL) and confirms a consistent page (after → PASS).**
