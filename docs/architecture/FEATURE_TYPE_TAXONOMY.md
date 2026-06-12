# Feature Type Taxonomy (alpha.21)

> Ends the internal-vs-user-facing confusion permanently. Every BeQuite feature gets exactly one PRIMARY type; every FUTURE feature must declare its type (and shape) before building.

**Status:** active · **Adopted:** alpha.21 (per FABLE_5_FOLLOWUP_AUDIT findings)

## The 8 types

| # | Type | Test | Examples |
|---|---|---|---|
| 1 | **User-facing capability** | the user can DO a new valuable thing | Presentation Builder · Writing DNA · Live Edit · UI Variants · Job/Money Finders · Delegate Mode · Skill Audit |
| 2 | **Internal reliability feature** | the agent fails less; user does nothing new | execution contract · file-risk tiers · evidence log · skill routing · confidence calibration mechanics |
| 3 | **Workflow gate** | something is BLOCKED until a condition | 23 ledger gates · 17 hard human gates · design continuity gates · uncertain-scope/R3 |
| 4 | **Skill-only capability** | deep procedure invoked by commands, never by users directly | all 27 `bequite-*` skills (incl. frontier-reasoning-coach) |
| 5 | **Command capability** | user-invokable slash command | the 46 commands |
| 6 | **Memory pattern** | a file shape + update discipline | DNA files · CONTEXT_SUMMARY · MISTAKE_MEMORY · registries · logs |
| 7 | **Documentation pattern** | knowledge with no runtime behavior | strategy docs · playbook · this taxonomy |
| 8 | **Roadmap-only idea** | tracked, not built | discovery trackers V1+V2 entries |

(Types compose: Writing DNA = capability(1) delivered via command(5) + skill(4) + memory(6). The PRIMARY label is what the user gets: 1.)

## The shape decision (mandatory before building anything)

```
Does the user invoke it directly? ──no──► skill (4) or memory (6) or doc (7)
        │yes
Is it a major workflow with distinct artifacts? ──no──► ARGUMENT on an existing command
        │yes                                            (anti-clutter default)
New command (5). Does it change depth/cost/safety posture? ──yes──► composition ALIAS,
        │no                                                          never a new mode
Ship command + skill + memory pack + docs per the 15-step workflow.
```

## Professional Expert — the worked ruling (Part 5)

`expert` = **composition alias**, NOT a 5th operating mode: `deep` + strict evidence (anti-hallucination + EVIDENCE_LOG mandatory) + safety scope (R3 awareness) + professional domain checklist (doctrine). Usage: `/bq-auto expert "review this auth flow"` expands to that composition. A 5th mode would expand the conflict matrix ~25% for zero new capability. Type: 7 (documented composition) routing into existing 2+4.

## Honest-labeling rules

1. Never market a type-2/3/6/7 item as a "game changer" — game changer = type 1 only.
2. Changelogs name the type for every added feature.
3. Discovery sprints (V2 onward) only count type-1 candidates as "new capabilities."
4. When in doubt: "what can the user do AFTER this that they couldn't before?" No answer → not type 1.

## alpha.22 worked shape decisions (precedents)

| Request | Shape ruling | Why |
|---|---|---|
| Reference/knowledge/course/pain-radar/integrate/proposal | **commands** (C3–C8) | major workflow + distinct artifact set + own memory dir + cross-project reuse |
| Roadmap/interview/spec-tests/announce/proof/vault/client-audit/regressions/drift/readiness/demo-video | **arguments** on plan/scope/test/release/handoff/audit/verify | variants of an existing workflow's intent; no distinct surface |
| Localization/RTL | **skill** (auto-attach) | cross-cutting concern, attaches to any workflow; standalone command would idle |
| Guard Pass | **skill** + strategy doc | reactive procedure invoked by other commands, not a user destination |
| Catalog IDs / Command Router | **docs + memory pattern** | navigation metadata, not behavior users invoke directly |
| 3D site builder | **argument** (`style=` on reference/uiux-variants) | a direction within an existing surface, not a new workflow |
| /bq-recording | **roadmap (parked)** | heavy media path unresearched; fails the lightweight test |

Anti-bloat outcome: 11 capability requests → 6 commands, not 17. Use these as precedents in future shape decisions.
