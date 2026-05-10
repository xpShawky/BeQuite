---
name: bequite.snapshot
description: Versioned snapshot of the Memory Bank + state files + active ADRs to .bequite/memory/prompts/v<N>/<timestamp>_<phase>.tar (or directory). BeQuite-unique. Runs at end-of-phase per Article III. Mandatory for auto-mode phase exits.
phase: any (most often phase boundaries)
persona: orchestrator (this SKILL)
---

# /bequite.snapshot [phase?] [reason?]

When invoked (or `bequite snapshot --phase P5 --reason "TASK-007 complete"`):

## Step 1 — Determine the snapshot target

`.bequite/memory/prompts/v<N>/<timestamp>_<phase>_<reason-slug>/` where:

- `<N>` is the next major snapshot version (incremented at major milestones).
- `<timestamp>` is `YYYY-MM-DDTHH-MM-SSZ`.
- `<phase>` is `P0`–`P7` or sub-version `v0.x.0`.
- `<reason-slug>` is `kebab-case` of the reason.

## Step 2 — Capture

Copy (read-only):

- `.bequite/memory/{constitution, projectbrief, productContext, systemPatterns, techContext, activeContext, progress}.md`
- `.bequite/memory/decisions/*.md` (all accepted ADRs)
- `state/{project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json}`
- The active feature's spec / plan / data-model / tasks (if applicable)
- Last 10 receipts at `.bequite/receipts/` (v0.7.0+)
- Most recent commit SHA + diff stat

Write a `manifest.json`:

```json
{
  "snapshot_version": "v3",
  "timestamp_utc": "2026-05-10T14:23:01Z",
  "phase": "P5",
  "reason": "TASK-007 complete",
  "captured": {
    "memory_bank": ["constitution.md", "projectbrief.md", ...],
    "decisions": ["ADR-001-stack.md", ...],
    "state": ["project.yaml", ...],
    "receipts": ["abc123-P5-TASK-007.json", ...]
  },
  "git": {
    "head_sha": "abc1234",
    "tag": "v0.4.1",
    "branch": "main"
  },
  "constitution_version": "1.0.1",
  "active_doctrines": ["library-package", "cli-tool", "mena-bilingual"],
  "mode": "safe"
}
```

## Step 3 — Update prompts/v<N>/INDEX.md

Append entry: timestamp, phase, reason, snapshot path. Index lets `/bequite.recover` and `/bequite.memory diff` find prior states fast.

## Step 4 — Optionally compress

For long-term archival (`--archive`): pack into `.tar.gz`. Default: keep as a directory for easy git diff.

## When snapshots fire automatically

- End of every phase (auto-mode).
- Before any one-way-door operation (auto-mode pauses + snapshots first).
- On `Stop` hook firing with non-trivial work done (`v0.10.0+`).
- On every `bequite release` invocation.

## Stop condition

- Snapshot directory created + populated.
- `manifest.json` written.
- `INDEX.md` updated.
- Receipt entry recording the snapshot location.

## Anti-patterns

- Snapshotting after destructive ops (capture *before*).
- Snapshotting without a `reason` — makes the index unsearchable.
- Compressing inline-edits-friendly content (defeats the diff utility).

## Related

- `/bequite.memory diff` — diff against the last snapshot.
- `/bequite.recover` — reads snapshots when chain-integrity check passes.
- `prompts/recovery_prompt.md` — references the snapshot index.
