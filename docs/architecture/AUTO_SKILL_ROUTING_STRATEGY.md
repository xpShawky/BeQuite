# Auto Skill Routing Strategy (alpha.20)

> **You describe the goal. BeQuite chooses the expert procedures.** Users never need to name skills manually — the router infers them from the request, command, context, mode, phase, files present, repo type, memory, risk level, and requested output type.

**Status:** active · **Adopted:** alpha.20
**Artifacts:** `.bequite/skills/SKILL_REGISTRY.md` (routing index) · `SKILL_ROUTER.md` (domain map + algorithm) · `SKILL_USAGE_LOG.md` (selections + outcomes)
**Wired into:** `COMMAND_EXECUTION_CONTRACT.md` steps 2–4 (registry check → task classification → automatic selection) and the action commands (auto / feature / fix / plan / implement / review / verify / suggest / skill-audit).

---

## The routing pipeline (runs before every non-trivial command)

1. **Discover** — confirm the registry is current (`SKILL_REGISTRY.md`); if a skill dir exists that isn't indexed (or vice versa), flag drift and proceed with the live Glob result. Global `~/.claude/skills/` is probed at refresh; if inaccessible/empty, that limitation is recorded in the registry header and only project skills are indexed.
2. **Load the registry summary** — NOT the skill files. The registry is the token-cheap lookup layer.
3. **Classify the task** into one or more domains (see `SKILL_ROUTER.md` domain map) using, in priority order: explicit user text → invoking command → files present / repo type → current mode + phase → memory (PROJECT_DNA, MISTAKE_MEMORY, MODE_HISTORY) → risk level (FILE_RISK tier of likely-touched paths) → requested output type.
4. **Select skills** per the router's domain→skill map, applying mode sizing (below) and the cross-cutting auto-attach rules.
5. **Report the selection** — every command output includes a `Skill Selection:` section listing selected skills WITH one-line reasons, and notable NOT-selected skills with reasons (so the user can correct the routing).
6. **Load only selected** SKILL.md files (masters may pull their `references/` on demand).
7. **Log** to `SKILL_USAGE_LOG.md` at writeback (selection + outcome) — feeds workflow-advisor pattern learning and `/bq-skill-audit` orphan detection.

## Mode sizing (don't over-trigger)

| Mode | Skill-set sizing |
|---|---|
| **Fast** | smallest SAFE set — primary domain skill + testing-gate when code changes; skip advisory extras |
| **Balanced** (default) | primary domain set + cross-cutting auto-attach |
| **Deep** | broader set — primary + adjacent domains + researcher + anti-hallucination + red-team-relevant skills |
| **Token Saver** | registry summary only at selection; load full SKILL.md lazily, only at the step that needs it |
| **Delegate** | selected skills are NAMED in the delegate task pack (`DELEGATE_INSTRUCTIONS.md` gets a "Disciplines to follow" list) so the cheaper model loads the same procedures |

**Small task rule:** a one-file trivial change gets at most 2 skills. **Over-triggering is a routing defect** — log it to MISTAKE_MEMORY when caught.

## Cross-cutting auto-attach rules

- `anti-hallucination` — attaches whenever the run will make "works/done/true" claims (i.e., almost every action command at verification step)
- `context-engineer` — attaches when the task spans >1 session or >5 files
- `testing-gate` — attaches whenever code changes
- `security-reviewer` — attaches when touched paths hit FILE_RISK R3 categories (auth/secrets/payments/migrations) even if the user didn't say "security"
- `frontend-design-system` — attaches (as coordinator) whenever >1 visible UI section is touched; it then activates its members (ux-ui-designer, frontend-quality, live-edit) itself

## Conflict + arbitration

Current pack has no hard skill conflicts (registry column tracks this). Arbitration rules: master beats member (don't separately load members frontend-design-system already coordinates) · specialist beats generalist for the primary domain · cross-cutting skills never count against the small-task cap.

## What this is NOT

- Not a runtime/daemon — routing is the agent reading the registry per the contract
- Not a replacement for explicit user choice — "use only X skill" always wins and is logged
- Not Claude Code's own description-matching replacement — it complements it: descriptions get the skill CONSIDERED; the router makes selection deliberate, explained, and logged

## Failure behavior

Registry missing → rebuild from Glob (slow path) + flag for `/bq-skill-audit` · classification ambiguous between 2 domains → select both primaries if budget allows, else ask ONE question · user names a skill that doesn't exist → list nearest matches from registry

## alpha.22 extension — capability domains + the second router

Eight routing domains added for the alpha.22 capability commands + cross-cutting skills (see `SKILL_ROUTER.md`): Arabic/MENA/RTL → **localization-rtl** (auto-attach, any workflow) · post-work quality → **guard-pass** (auto-attach after implement/test, before verify/release) · plus the C3–C8 command domains (reference / knowledge / course / pain-radar / integrate / proposal). Registry now indexes **29 skills**.

**Two routers, two questions:** the Skill Router (this strategy) answers *which expert procedures*; the **Workflow Command Router** (`WORKFLOW_COMMAND_ROUTER.md`, alpha.22) answers *which command next*. They run together in contract steps 2–4 (skills) and 12 (commands) and must never be conflated in output: `Skill Selection:` block vs `Next Command Recommendations:` block.
