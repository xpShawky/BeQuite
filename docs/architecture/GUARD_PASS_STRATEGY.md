# Guard Pass Strategy (alpha.22)

**What:** reactive second-pass quality gates that catch the failure modes AI-generated work specifically exhibits — run *after* work is produced, *before* it ships. Skill: `bequite-guard-pass`. Report: `.bequite/audits/GUARD_PASS_REPORT.md`.

## Provenance — concept adapted, nothing copied

Studied https://github.com/amElnagdy/guard-skills (fetched 2026-06-12). Pattern observed: 5 guards (clean-code / test / docs / wp / woo) · progressive disclosure (small SKILL.md entry + deeper references loaded on demand) · reactive diff-review placement (after output, before merge) · no scripts / no network / no MCP deps / no credentials · inspectable markdown + light YAML. **BeQuite adaptation rules honored: no install, no external dependency, no content copied — concept only.**

## How Guard Pass differs from what BeQuite already had

| Existing layer | Answers | Guard Pass adds |
|---|---|---|
| `/bq-review` | does the diff meet spec + quality? | a targeted AI-failure-mode hunt (hallucinated APIs, hardcoded success, over-mocking, doc drift) |
| `/bq-red-team` | what's broken adversarially? | cheaper, checklist-driven, runs every cycle (red-team is occasional) |
| anti-hallucination skill | are claims evidenced? | applies that discipline to *artifacts* (code/tests/docs), not statements |
| `/bq-verify drift` | counts/docs vs files | guard docs-checklist feeds it; drift arg is the mechanical check, docs guard is the judgment check |

## Placement in workflows

After `/bq-implement` · `/bq-feature` · `/bq-fix` (code guard) → after `/bq-test` (test guard) → **before `/bq-verify`** → before `/bq-release` (all three guards) → before any "docs are accurate" claim (docs guard). In auto mode the pass runs automatically at those points; in manual mode the router recommends it. Delegate mode: the strong-model review **always** includes a Guard Pass over the cheap model's diff.

## The three guards (checklists live in the skill)

1. **Code guard** — hallucinated APIs · hardcoded success · broad catch-alls · premature/over-abstraction · copy-from-similar bugs · bad naming · broken contracts
2. **Test guard** — implementation-detail assertions · over-mocking · duplicate tests · tests that catch nothing · missing regression tests · fake success (skips counted as passes)
3. **Docs guard** — nonexistent functions documented · README examples that don't run · commands.md / counts out of sync · unsupported changelog claims · broken install instructions

**Platform guards** (WordPress/Woo/etc.): added per-project only when that project needs them — none ship by default (lightweight charter).

## Rules

Evidence-cited findings only (`file:line` quote or struck). Report-only by default; fixes on approval or R1-safe in auto mode. A "no findings" verdict must list what was checked. No scripts, no network calls, no credentials — markdown discipline, optionally machine-assisted later via the existing opt-in hooks layer (not in this pass).

## Seed finding (proof the pattern works)

Finding #1 (docs guard, caught by the user, fixed in alpha.22): `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` claimed "24 slash commands / 7 skills" — stale since alpha.1 while the repo reached 46/27. Exactly the out-of-sync-counts failure mode this system exists to catch. See `GUARD_PASS_REPORT.md`.
