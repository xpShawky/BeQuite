# Current phase

**Phase:** P0 — Setup and Discovery

## Allowed phases

| Phase | Name | Commands | Goal |
|---|---|---|---|
| **P0** | Setup and Discovery | `/bq-init`, `/bq-mode`, `/bq-discover`, `/bq-doctor` | Learn what's there |
| **P1** | Product Framing and Research | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`, `/bq-multi-plan` | Decide what to build |
| **P2** | Planning and Build | `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix` | Build it |
| **P3** | Quality and Review | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` | Confirm it works |
| **P4** | Release | `/bq-verify`, `/bq-release`, `/bq-changelog` | Ship |
| **P5** | Memory and Handoff | `/bq-memory`, `/bq-recover`, `/bq-handoff` | Continue / hand off |

## Phase orchestrators

| Command | Effect |
|---|---|
| `/bq-p0` | Walks through P0 in order |
| `/bq-p1` | Walks through P1 in order |
| `/bq-p2` | Walks through P2 in order |
| `/bq-p3` | Walks through P3 in order |
| `/bq-p4` | Walks through P4 in order |
| `/bq-p5` | Walks through P5 in order |
| `/bq-auto` | Walks ALL phases autonomously; stops at hard human gates |

## Phase transitions

A phase is considered "complete" when:
- All **required** gates for that phase are `✅ done` in `WORKFLOW_GATES.md`
- Optional gates may remain pending (e.g. multi-plan, red-team are optional)

Phase transition is automatic — once all required gates of phase N are met, you can run phase N+1 commands.

You cannot SKIP a phase (e.g. run `/bq-implement` while P1 gates are pending). The gate system blocks this.

You CAN re-enter an earlier phase (e.g. mid-implementation, run `/bq-research` again for newly-surfaced questions). The earlier phase's gates stay `✅ done`; new artifacts append.
