# Frontend Context Engineering

**Status:** active (v3.0.0-alpha.17)
**Companion to:** `DESIGN_CONTINUITY_GATE.md`, `MEMORY_FIRST_BEHAVIOR.md`

---

## 1. The core insight

"Middle-section design drift" is, at root, a **context** failure. The hero looks good because the design intent is fresh in the conversation. By section 5 the intent has scrolled out of the live context window, so the model falls back to the statistical average of its training data — generic cards, flat hierarchy, AI-slop gradients.

You cannot fix this by being a better designer in the moment. You fix it by **engineering the context** so the design intent is *persisted, compact, and re-read* before every section — instead of being remembered, fuzzily, from earlier in the chat.

This is the frontend specialization of BeQuite's memory-first principle.

## 2. The rules

1. **Do not keep the design only in conversation memory.** Conversation memory decays; files don't. The hero's font, palette, spacing rhythm, and mood must be on disk.
2. **Persist the Design DNA before implementation.** `DESIGN_DNA.md` is written/updated *before* the first line of UI code. If it's missing, create it first. (Gate: `DESIGN_DNA_LOCKED`.)
3. **Persist the section map before implementation.** `SECTION_MAP.md` lists every section to build with its acceptance criteria, so "what's left" is never guessed.
4. **Persist a component map if the app is large.** For multi-page apps, record the shared component inventory (buttons, cards, inputs) so they stay identical across pages.
5. **Persist issues in mistake memory.** Every drift caught becomes a `[fe][design]` entry in `MISTAKE_MEMORY.md` with a detection rule, so it's prevented next time.
6. **Read design memory before each frontend task.** Before touching a section, re-read (at minimum) `FRONTEND_CONTEXT_SUMMARY.md`; before a deeper task, the DNA + section map.
7. **Use compact summaries instead of rereading everything.** `FRONTEND_CONTEXT_SUMMARY.md` is the 1-screen digest the agent reads every time. The full DNA / section map are read on demand. This keeps the design in-context cheaply (token-saver-friendly).
8. **Never continue frontend implementation from vague memory.** If you can't state the font, the primary color, the spacing scale, and the product type from memory — stop and re-read the DNA. "I think it was a blue SaaS thing" is a drift in progress.
9. **Before editing a section, inspect the source file AND the design DNA.** Both. The source tells you what's there; the DNA tells you what it should be.
10. **After editing a section, update the section map if structure changed.** The map is a contract; keep it true.
11. **After finishing, run the Design Continuity Gate.** Then write the Visual QA report. Only then is the surface "complete."

## 3. The design memory files (the persisted context layer)

| File | Role | Read when | Write when |
|---|---|---|---|
| `.bequite/design/DESIGN_DNA.md` | Source of truth for visual identity (product type, palette, type, spacing, motion, anti-patterns) | before any UI task | before first UI code; whenever identity changes |
| `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` | 1-screen compact digest (DNA gist + active task + touched files + risks + last QA result) | **every** frontend task (cheapest) | after every frontend step |
| `.bequite/uiux/SECTION_MAP.md` | Every section → source file + acceptance criteria | before building/editing a section | when a section is added/changed |
| `.bequite/design/DESIGN_CONTINUITY_REPORT.md` | Per-route continuity findings | when comparing a section to the DNA | after a continuity pass |
| `.bequite/audits/VISUAL_QA_REPORT.md` | Browser/manual render findings | before claiming a UI complete | after a visual QA pass |
| `.bequite/state/MISTAKE_MEMORY.md` | `[fe][design]` drift lessons | session start + before risky edits | when drift is found |

## 4. The compact-summary discipline (token economics)

Re-reading the full DNA + section map + every report before every micro-edit is wasteful and, ironically, can push *other* context out. So:

- `FRONTEND_CONTEXT_SUMMARY.md` is kept **under one screen**. It is the default read.
- It links to the full files. The agent escalates to the full DNA / map only when the summary is insufficient (new section type, identity question, ambiguity).
- In `token-saver` mode: read only the summary + the one section's source file. In `deep`/`xhigh` mode: read the full DNA + map + prior continuity report.

This is "compact summaries instead of rereading everything" — the design intent stays in-context at minimal cost.

## 5. The section-by-section loop (how context engineering becomes a workflow)

Frontend implementation is **never** "build the whole page and hope." It is:

1. Define / read **Design DNA** → `DESIGN_DNA.md`
2. Define **page structure**
3. Define **section map** → `SECTION_MAP.md` (each section gets acceptance criteria)
4. Build **section 1** → check section 1 against the DNA
5. Build **section 2** → check section 2 against the DNA *and* section 1
6. …continue section by section (re-reading the compact summary each time)
7. Run **full-page continuity audit** → `DESIGN_CONTINUITY_REPORT.md`
8. Run **responsive audit** (360 / 768 / 1440 + defined breakpoints)
9. Run **accessibility / contrast audit** (WCAG 2.2 AA; AAA for regulated types)
10. Run **final polish** (the weakest section gets pulled up to the strongest)

The check after each section is the whole point: drift is caught the moment it appears, while the section is cheap to fix — not at the end when the model has to re-understand five sections at once.

## 6. Effort awareness

- **low/medium** — read the compact summary; section checks are quick heuristic passes.
- **high** — read DNA + section map; full section-by-section loop + continuity report.
- **xhigh / max / Ultracode** — persist per-section critique snapshots, compare each section to the strongest, run browser visual QA, final polish pass. Treat Ultracode as senior-design-review depth.

## 7. Anti-patterns (context-engineering failures)

- Building the hero, then "freestyling" the rest from memory.
- Editing a section without re-reading the DNA ("I remember roughly what we picked").
- Letting `SECTION_MAP.md` go stale so "what's left" becomes a guess.
- Treating screenshots/visual QA as optional when a frontend exists.
- Re-reading the entire `.bequite/` tree every micro-edit (the opposite failure — wastes context). Use the compact summary.

See `DESIGN_CONTINUITY_GATE.md` for the gate that enforces the output, and `bequite-frontend-design-system` for the skill that runs the loop.
