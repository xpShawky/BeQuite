# Frontend Skill Map

**The coordination map for BeQuite's frontend skills.** One master, three supporting. No clutter, no duplication by designation.

**Last updated:** 2026-06-04 (v3.0.0-alpha.17)

---

## The skills

| Skill | Role | Master / Supporting | Canonical owner of |
|---|---|---|---|
| `bequite-frontend-design-system` | **Orchestrator + continuity** | **MASTER** | Design DNA · section-by-section loop · Design Continuity Gate · visual QA · product-type rules · effort awareness · the role split below |
| `bequite-ux-ui-designer` | Design + token **generation** | Supporting | the 10 design principles · token contract (canonical) |
| `bequite-frontend-quality` | AI-slop **detection** in code | Supporting | the 15 AI-slop tells · component-sourcing order (canonical) |
| `bequite-live-edit` | Section **edit** + browser tiers | Supporting | the 3-tier browser inspection strategy · rollback (canonical) |

The master does NOT restate the supporting skills' canonical lists — it **calls** them. This is how we de-duplicate without deleting.

## When each is used

- **`bequite-frontend-design-system` (master)** — activates whenever a frontend task spans more than one section or needs design identity held across a page/app: new UI builds, redesigns, full-page audits, variant merges, "make the whole thing consistent." It defines/reads the DNA, plans the section map, runs the section-by-section loop, and runs the Design Continuity Gate + visual QA. It decides which supporting skill to call for each step.
- **`bequite-ux-ui-designer`** — when *generating* design: picking palette/type/spacing, designing a new screen, proposing variant directions. Called by the master for "design this section."
- **`bequite-frontend-quality`** — when *detecting* slop in existing/just-written code: the 15-tell scan, tokens.css discipline, real-states check. Called by the master during the continuity gate.
- **`bequite-live-edit`** — when *editing one section* of a running frontend: section→file mapping, smallest-change edit, browser screenshot tiers. Called by the master during the section loop and by `/bq-live-edit` directly.

## Which commands activate which skill

| Command | Master | ux-ui-designer | frontend-quality | live-edit |
|---|---|---|---|---|
| `/bq-feature` (UI types 1/8/9) | ✅ orchestrate | ✅ design | ✅ detect | – |
| `/bq-fix` (types 1/15) | ✅ continuity re-check | – | ✅ detect | ✅ edit |
| `/bq-auto` (`uiux`/`frontend`/`live-edit`/`variants`) | ✅ orchestrate | ✅ | ✅ | ✅ |
| `/bq-uiux-variants` | ✅ continuity per variant | ✅ directions | ✅ slop check | – |
| `/bq-live-edit` | ✅ section loop | – | ✅ post-edit | ✅ primary |
| `/bq-audit` (frontend present) | ✅ full sweep | – | ✅ detect | – |
| `/bq-review` (UI diff) | ✅ continuity dim | – | ✅ | – |
| `/bq-red-team` (UI) | ✅ "worst section" angle | – | ✅ | – |
| `/bq-verify` (frontend present) | ✅ gate matrix | – | ✅ | – |

## Which docs / memory each updates

| Skill | Writes / updates |
|---|---|
| master | `.bequite/design/DESIGN_DNA.md`, `DESIGN_CONTINUITY_REPORT.md`, `.bequite/audits/VISUAL_QA_REPORT.md`, `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md`, `.bequite/uiux/SECTION_MAP.md` |
| ux-ui-designer | `tokens.css` (project), variant directions, `DESIGN_DNA.md` (palette/type sections) |
| frontend-quality | `MISTAKE_MEMORY.md` (`[fe][design]`), audit findings |
| live-edit | `SECTION_MAP.md`, `LIVE_EDIT_LOG.md`, `screenshots/` |

## Governing docs

- `docs/architecture/DESIGN_CONTINUITY_GATE.md` — the gate the master runs
- `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md` — why design is persisted, not held in chat
- `docs/architecture/LIVE_EDIT_STRATEGY.md`, `docs/architecture/UIUX_VARIANTS_STRATEGY.md` — the two FE workflows
- `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` — read design memory before acting

## Anti-clutter rule

Do NOT create new scattered frontend skills. New frontend capability goes into the master skill's `references/` as a loaded-on-demand file, or into an existing supporting skill — never a new top-level skill — unless it is a genuinely separate domain. See `FRONTEND_SKILL_INTEGRATION_AUDIT.md` for the rationale.
