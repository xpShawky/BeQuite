# evidence/

> **Filesystem evidence for every BeQuite task.** Per master §3.6, §10.3, §21. Complementary to the signed-receipt chain at `.bequite/receipts/` (v0.7.0+).
>
> A task is **not done** without evidence. No exceptions.

---

## Structure

```
evidence/
├── README.md                     ← this file
├── <phase>/                      ← one of P0..P7 (or phase-0..phase-4 for BeQuite-itself)
│   ├── phase_summary.md          ← end-of-phase summary
│   └── <task_id>/                ← per task
│       ├── manifest.json         ← machine-readable evidence record
│       ├── summary.md            ← human-readable summary
│       ├── test-output.txt       ← captured test stdout/stderr
│       ├── lint-output.txt
│       ├── typecheck-output.txt
│       ├── build-output.txt
│       ├── screenshots/          ← UI evidence (PNG)
│       │   ├── before.png
│       │   └── after.png
│       ├── playwright-traces/    ← Playwright trace ZIPs (P6)
│       └── logs/                 ← misc logs (security scan, deploy, migration, seed)
└── ...
```

For BeQuite-itself (the build of BeQuite), the phases are `phase-0`, `phase-1`, …, `phase-4` plus `studio-phase-1`. For BeQuite-managed downstream projects, the phases are `P0` (Research) through `P7` (Handoff).

---

## Manifest schema (master §21)

Every `<task_id>/manifest.json` follows this shape:

```json
{
  "$schema": "https://bequite.dev/schemas/evidence_manifest.v1.json",
  "taskId": "TASK-001",
  "phase": "PHASE-1",
  "subVersion": "0.5.0",
  "status": "passed",
  "commands": [
    {
      "command": "pnpm test",
      "exitCode": 0,
      "status": "passed",
      "outputPath": "evidence/PHASE-1/TASK-001/test-output.txt"
    },
    {
      "command": "pnpm lint",
      "exitCode": 0,
      "status": "passed",
      "outputPath": "evidence/PHASE-1/TASK-001/lint-output.txt"
    }
  ],
  "screenshots": [
    "evidence/PHASE-1/TASK-001/screenshots/dashboard.png"
  ],
  "tracesAndLogs": [
    "evidence/PHASE-1/TASK-001/logs/security-scan.txt"
  ],
  "filesChanged": [
    "apps/web/src/components/Dashboard.tsx",
    "apps/web/src/components/Dashboard.test.tsx"
  ],
  "notes": "Task passed all validation gates.",
  "skepticQuestion": "What happens when the API times out mid-render?",
  "skepticAnswer": "Loading state is shown for up to 30s; after that, an error boundary renders a 'try again' UI; covered by Dashboard.timeout.test.tsx.",
  "createdAt": "2026-05-10T00:00:00Z",
  "receiptSha": "sha256:..."          // Filled in v0.7.0+ when receipts ship
}
```

---

## Evidence types (master §14.7)

The `commands[].command` and `tracesAndLogs[]` entries cover these types:

- `test` — unit / integration / e2e
- `lint` — eslint / ruff / clippy
- `typecheck` — tsc / mypy / pyright / cargo check
- `build` — webpack / vite / cargo build / pyproject build
- `screenshot` — UI evidence
- `trace` — Playwright trace ZIPs
- `log` — security scan / deploy / migration / seed / runtime errors
- `migration` — DB migration up/down output
- `seed` — DB seed result
- `security` — semgrep / snyk / trivy / osv-scanner output
- `deployment` — deploy URL + health-check transcript
- `manual-check` — human-verified observation (rare; document why automation didn't apply)

---

## Phase summary

At the end of every phase, write `evidence/<phase>/phase_summary.md`:

```markdown
# <Phase> summary — <YYYY-MM-DD>

## Status
PASSED

## Tasks
- TASK-001 — passed
- TASK-002 — passed
- TASK-003 — passed (with 1 follow-up: TASK-004)

## Validation results
- Lint: passed
- Typecheck: passed
- Unit: 84 tests, 84 passed, 0 failed
- Integration: 12 tests, 12 passed, 0 failed
- E2E: 6 flows, 6 passed, 0 failed
- Security scan: 0 criticals, 2 medium (filed as TASK-004, TASK-005)
- Coverage: 87% (lines)

## Known issues
- TASK-005 — medium-severity finding from `osv-scanner`. Mitigation planned in v0.6.0.

## Next phase
Phase-2 (DB + API). Pre-requisites: ADR-002 (database choice) + ADR-003 (auth) accepted.
```

---

## What is NOT evidence

- "Looks good to me" without a captured test output.
- A passing local test that wasn't re-run after rebase / merge / dependency bump.
- A screenshot of the *last* UI when the task changed something else.
- A log file from a previous session (cross-session reuse violates Article II — "executed in this session").

---

## Cleanup policy

- **Never** `git clean -fd` the `evidence/` directory. It is gitignore-protected (NOT ignored).
- **Never** delete an evidence directory that's referenced by a receipt.
- Evidence older than 12 months can be archived to `evidence/_archive/<YYYY-QQ>.tar.gz` if size becomes a problem (rare).

---

## Cross-reference with receipts (v0.7.0+)

Every receipt at `.bequite/receipts/<sha>-<phase>-<task_id>.json` carries:

- `output.files_touched` — same file paths as `manifest.json::filesChanged`.
- `tests.command` + `tests.exit` — same as `manifest.json::commands`.
- `tests.stdout_hash` — sha256 of `evidence/<phase>/<task_id>/test-output.txt`.

The receipt is the **cryptographic** proof. The evidence directory is the **filesystem** proof. Both are required.
