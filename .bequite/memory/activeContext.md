# Active Context: BeQuite

> The most-edited file in `.bequite/memory/`. Updated at the end of every task. Phase-snapshotted at the end of every phase.

---

## Now (last edited: 2026-05-10)

- **Active feature:** `BeQuite v1.0.0` (the build of BeQuite itself)
- **Active phase:** P5 Implement (the seven-phase loop, applied to BeQuite-itself; sub-version v0.1.0 in progress)
- **Active task ID:** `v0.1.0/foundation`
- **Active mode:** `auto` (Ahmed authorised autonomous execution through to v1.0.0 with safety rails)
- **Skeptic gate state:** `cleared` — the plan was reviewed via `ExitPlanMode` and accepted
- **Last green sub-version:** none (v0.1.0 is the first)
- **Cost-ceiling status:** session-default ($20 USD); not yet tracked (receipts ship in v0.7.0)
- **Wall-clock-ceiling status:** session-default (6 h); not yet tracked

## What I'm doing right now

Building v0.1.0 — the foundation: repository skeleton (README, LICENSE, .gitignore, CHANGELOG), the seven Memory Bank templates, the ADR template, the Doctrine schema template, and the Constitution v1.0.0 itself with seven Iron Laws (Specification supremacy, Verification before completion, Memory discipline, Security & destruction, Scale honesty, Honest reporting, Hallucination defense). The `.bequite/memory/` tree is being populated for BeQuite-itself (eating its own food), with a parallel `template/.bequite/memory/` tree shipped in the repo template for downstream projects. Next: snapshot the approved plan to `prompts/v1/`, update `progress.md`, commit + tag `v0.1.0`, then proceed to v0.1.1 (Doctrines pack).

## Open questions (need answers before I can continue)

- [ ] Confirm with Ahmed whether `bequite` is a viable PyPI package name (collision check is a Phase-1 task during v0.5.0; not blocking now).
- [ ] Confirm with Ahmed whether the GitHub org should be `xpshawky/bequite` (default assumption) or a separate `bequite-org`. Affects README badges and AGENTS.md metadata. **Not blocking v0.1.0–v0.4.x.**
- [ ] Confirm with Ahmed which Telegram + X/Twitter MENA channels seed the `mena-bilingual` Researcher in v0.11.0. **Not blocking until v0.11.0.**

## Blockers

| Blocker | Why it blocks | Owner | Mitigation |
|---|---|---|---|
| (none) | | | |

## Next 3 things I'll do

1. Snapshot the approved plan to `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`.
2. Update `progress.md` with the v0.1.0 work landed.
3. Commit + tag `v0.1.0`. Begin v0.1.1 (Doctrines pack).

## Heartbeat (auto-mode only)

- Last heartbeat: 2026-05-10 (this update)
- Last receipt: none (receipts ship in v0.7.0)
- Last commit: none yet (initial commit lands at end of v0.1.0)

## Recent decisions (last 5)

```
2026-05-10  Iron Laws layered (7 articles); Doctrines forkable.
2026-05-10  Skill-first distribution; CLI is thin Python wrapper.
2026-05-10  Engineer-first v1; vibe-handoff seeded into artifact discipline.
2026-05-10  Impeccable bundled as default Doctrine for frontend projects (pinned snapshot, not core dependency).
2026-05-10  Full v1 power from day 1 (15 sub-versions, autonomous execution authorised by Ahmed).
```
