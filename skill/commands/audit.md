---
name: bequite.audit
description: Constitution + Doctrine drift detector. BeQuite-unique. Scans the codebase against Iron Laws (Constitution v1.0.1) + active Doctrines + accepted ADRs. Surfaces violations as inline-comment-style findings with file:line + suggested fix. Implementation lands in v0.4.2 as cli/bequite/audit.py.
phase: any (most often P5/P6 + CI on every PR)
persona: software-architect (delegates to specific personas per rule pack)
implementation: cli/bequite/audit.py (v0.4.2)
---

# /bequite.audit [scope?]

When invoked (or `bequite audit [--phase P5] [--rule article-iv] [--doctrine default-web-saas]`):

## Step 1 — Read context

- `.bequite/memory/constitution.md` — Iron Laws + active Doctrines.
- `state/project.yaml::active_doctrines, mode, scale_tier`.
- All accepted ADRs (some ADRs override / scope rules).
- `skill/references/package-allowlist.md` (drafted v0.4.3).

## Step 2 — Walk rule packs

For each rule, run the corresponding scan. Categorise findings: `block` / `warn` / `recommend`.

### Iron Laws (always on)

- **Article I — Spec supremacy**: code paths without a corresponding spec ID in commit messages → `warn`.
- **Article III — Memory discipline**: missing `activeContext.md` updates after a code commit → `warn`.
- **Article IV — Security & destruction**:
  - `.env*` reads in code → `block` (cross-references hook `posttooluse-audit.sh`).
  - Destructive ops outside ADR-approved scripts → `block`.
  - Secret-shaped strings in source (regex from `pretooluse-secret-scan.sh`) → `block`.
- **Article V — Scale honesty**: synchronous in-process job patterns above scale tier 50K → `block`.
- **Article VII — Hallucination defense**: imports not in lockfile + not in allowlist + not in `state/decision_index.json::approved-deps` → `block`.

### Doctrine packs

#### default-web-saas

- Rule 1 (tokens-only design): hardcoded `font-family` / `color` / `background` outside `tokens.css` / `tokens.json` → `block`.
- Rule 2 (recorded design choice): font-family declarations without an adjacent `WHY` comment → `warn`.
- Rule 4 (no nested cards): TSX / Vue templates with `.card` / `[role="region"]` nested → `block`.
- Rule 5 (no gray-on-color): WCAG AA contrast violations from `axe-core` log → `block`.
- Rule 6 (no bounce / elastic easing): `cubic-bezier(...overshoot...)` / `bounce` keywords → `block`.
- Rule 10 (deny-by-default authz): tables in migrations without an explicit RLS / RBAC policy → `block`.
- Rule 11 (input validation): API handlers without Zod / Pydantic / Valibot at entry → `block`.

#### cli-tool

- Rule 1 (semver-strict on flags): `--help` output diff between commits without semver bump → `warn`.
- Rule 6 (NO_COLOR support): pipe output through `cat`; expect no ANSI escapes → `block`.

#### library-package

- Rule 1 (semver-strict on public API): API diff (api-extractor / cargo public-api) shows breaking change without major bump → `block`.
- Rule 7 (no telemetry without opt-in): telemetry-shaped fetch outside config gate → `block`.
- Rule 8 (license clarity): missing OSI-recognised LICENSE file → `block`.
- Rule 9 (GPL contamination): copyleft dependency in permissive package → `block`.

#### ai-automation

- Rule 1 (workflows version-controlled): no flow JSON committed → `block`.
- Rule 4 (secrets out of flow JSON): secret-shaped strings in `.n8n/workflows/` / `scenarios/` → `block` (cross-references `pretooluse-secret-scan.sh`).
- Rule 8 (schema validation at edge): webhook entries without validation → `block`.

#### Regulated (fintech-pci / healthcare-hipaa / gov-fedramp)

Each Doctrine's binding rules invoked when active. PHI / CHD / FIPS-validated checks per the Doctrine. See per-Doctrine markdown for the full list.

## Step 3 — Output

For each finding:

```
[block | warn | recommend] file:line — <rule id> (<rule statement>)
  Found:    <code excerpt>
  Suggest:  <remediation>
  Why:      <Iron Law / Doctrine reference>
```

CI mode (`--ci`): post findings as PR review comments via `gh pr review`.

## Step 4 — Save

- Write to stdout (paste-able) AND `evidence/<phase>/audit-<YYYY-MM-DD>.md`.
- Update `state/evidence_index.json` with audit-evidence entry.

## Stop condition

- Every active Iron Law + Doctrine rule scanned.
- Findings surfaced.
- For CI mode: posted as PR review.
- Exit code: 0 if zero blockers; 1 if any block-severity finding.

## Anti-patterns

- Skipping rules with "we'll fix later" — file as a new task with deadline; rule still flagged.
- Auto-fixing without surfacing first.
- Cherry-picking which rules to run.

## Related

- `posttooluse-audit.sh` — lightweight per-edit subset.
- `/bequite.freshness` — knowledge probe (different concern: stale dependencies vs Constitution drift).
- `/bequite.validate` — Phase 6 includes audit as a gate.
