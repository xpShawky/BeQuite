# Command Navigation & Capability Consolidation Audit (alpha.22)

**Run:** 2026-06-12 · Claude Fable 5 (no switch) · Deep Mode
**Repo at audit:** alpha.21 (`bffbd67`) · 47 command files = **46 active commands** (1 menu + 45 active `bq-*`) **+ 1 deprecated alias** (`bq-add-feature`) · **27 skills** · 4 operating modes · 6 phases · 23 + 3 + 17 gates

---

## 1. Current structure

**Categories:** Navigation (bequite, now, help, explain, suggest — 5) · W0 Setup (init, mode, new, existing, discover, doctor — 6) · W1 Framing (clarify, research, scope, spec, plan, multi-plan — 6) · W2 Build (assign, implement, feature, fix — 4 + alias) · W3 Quality (test, audit, review, red-team — 4) · W4 Release (verify, release, changelog — 3) · W5 Memory (memory, recover, handoff — 3) · Orchestrators (p0–p5, auto — 7) · UI (uiux-variants, live-edit — 2) · Earning (job-finder, make-money — 2) · Creative/Content (presentation, writing-dna — 2) · Maintenance (update, skill-audit — 2).

## 2. Overlap findings

**Commands:** No true duplicates. One deprecated alias correctly marked. Near-misses that must NOT merge: audit≠review (whole-project vs diff), spec≠scope≠plan (3 artifact tiers), now≠bequite≠suggest (1-line vs menu vs advisor).
**Skills:** quality-vs-design-system role split holds (alpha.17); job-finder/make-money share intake but distinct intents — keep. No merges this pass.

## 3. Navigation quality (the gap this pass fixes)

| Surface | State | Verdict |
|---|---|---|
| `/bequite` menu | complete map, gate-aware next-3 | good but **unnumbered**; long list hard to scan |
| `/bq-help` | purpose-grouped, current | good; **unnumbered** |
| `/bq-suggest` | trigger tables + skill routing | good single-route advisor; **does not emit multi-command SETS, IDs, or auto-run flags** |
| Per-command "usual next" | exists (1 command) | **single-next only**; no optional set, no capability suggestions, no "do not run yet" |
| Auto-mode internal workflow | runs correct sequence per intent | ✅ correct, but **doesn't report which catalog steps it executed internally** |
| Skill Router | ✅ alpha.20 | answers WHICH SKILLS; nothing answers WHICH COMMAND NEXT systematically → **Command Router is the missing layer** |

**Naming/ordering confusion:** alphabetical file listing scatters the workflow (assign before init). Phase grouping in docs mitigates; stable IDs fix it fully.

## 4. Numbering feasibility ruling

- **Option C (rename files): REJECTED.** Filenames = slash names. Renaming breaks: every doc cross-ref (300+ mentions), user muscle memory, `/bq-update` migration for existing installs, registry/router references, hooks examples. Zero capability gained. Cost/benefit catastrophic.
- **Option B (ordered aliases): REJECTED.** +20 duplicate files = clutter, double maintenance, two names per action confuses more than it orders. Violates anti-clutter charter.
- **Option A (display-only IDs): ✅ ADOPTED.** Stable IDs in docs/menus/router; files untouched; IDs become the router's vocabulary. Full scheme in `COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md` + `COMMAND_ID_MAP.md`.

## 5. Shape rulings (user provisional vs audit)

**Approved as NEW standalone commands (6):** reference · knowledge · course · pain-radar · integrate · proposal — each passes the standalone test: major workflow + distinct artifact set + own memory dir + reusable across projects. Clone-safe naming honored (`/bq-reference`, never "clone").
**Approved as ARGUMENTS (8):** plan from-issues · scope from-interview · test from-spec · release announce · release proof · handoff client · audit client · verify regressions/drift/ship-ready (V1 integrations). All correct — none has enough distinct surface for a command.
**Localization:** skill-first (`bequite-localization-rtl`, auto-attached on Arabic/MENA/RTL signals); `/bq-localize` listed as optional proposal only. Agreed — command would be 70% redundant with the skill auto-attach.
**Parked:** `/bq-recording` (heavy media path; recorded in V2 tracker).

**Disagreements / refinements (independent judgment, as requested):**
1. **`/bq-release demo-video` over `/bq-presentation movie`** for the Product Movie Generator V1 item — a launch video is release collateral (joins announce/proof in one launch-kit family); presentation stays slide-focused. Provisional offered both; I pick release.
2. **`knowledge-builder` skill is NOT needed** — `/bq-knowledge` (command) + existing researcher/anti-hallucination/context-engineer cover it; a new skill would duplicate the command's own procedure. Skill count grows only +2 (localization-rtl, guard-pass), not +3.
3. **Ship-readiness → `/bq-release readiness`** (not verify ship-ready): verify answers "does it work", release answers "should it ship". Cleaner ownership; verify gets regressions/drift (mechanical checks), release gets readiness (judgment scorecard).
4. **V3 idea `/bq-offer`** (the user hinted "bq-offer if added later") ranks high — proposed in V3, not built now.

## 6. Roadmap items that must NOT become commands yet

Automation/Bot Builder (scope unclear; tool-neutral spec first) · Data-to-Product (park; revisit vs /bq-integrate overlap) · AI Service Business Builder (orchestrator — needs underlying commands stable first) · Agent Pack Generator (needs Guard Pass + Skill Audit maturity) · Workflow Export (secret-scan design first) · 3D Site Builder (style argument inside frontend system, not command).

## 7. Consolidation plan (executed this pass)

1. IDs: strategy + map + menus/docs display them (Option A)
2. Command Router layer: strategy + operational map + NEXT_COMMAND_LOG; contract step 12 upgraded to multi-command recommendation sets + auto-mode "Internal workflow executed" reporting
3. Build 6 capability command skeletons + 7 specs + 2 skills (localization-rtl, guard-pass)
4. 8 argument workflows appended to existing commands
5. Guard Pass system (strategy + skill + seed report — finding #1: INSTALL runbook stale at "24 commands/7 skills", caught by user, fixed this pass)
6. V1 12-candidate review + V2 updates + V3 20 fresh ideas
7. Full doc/registry/router/installer/runbook sync → ship as **alpha.22**

**Post-pass counts:** 52 active commands (+6) + 1 alias = 53 files · 29 skills (+2).
**No beginner/advanced hiding. No renames. No heavy deps.**
