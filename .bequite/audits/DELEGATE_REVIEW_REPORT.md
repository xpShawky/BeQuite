# Delegate Review Report

Strong-model review of the cheaper model's implementation work. Written in Phase 3 of Delegate Mode.

---

**Generated:** <ISO 8601 UTC>
**Reviewer (strong model):** <e.g. Claude Opus 4.7>
**Implementer model:** <e.g. Claude Sonnet 4.5 / Haiku>
**Tasks reviewed:** <N>
**Time span:** <ISO start> → <ISO end>

## Verdict

**Overall:** APPROVED | APPROVED-WITH-COMMENTS | REJECTED

<one-paragraph reasoning>

---

## Per-task review

<!--
  Template per task:

  ### T-D-<n>: ✅ APPROVED | ⚠ APPROVED-WITH-COMMENTS | ❌ REJECTED

  - file placement: ✓ | ✗ <reason>
  - function design: ✓ | ✗ <reason>
  - naming: ✓ | ✗ <recommendation>
  - integration: ✓ | ✗ <reason>
  - tests: ✓ <count pass> | ✗ <reason>
  - security: ✓ | ✗ <flag>
  - regressions: none | <list>
  - UX (if relevant): ✓ | ✗ <reason>
  - docs/log updates: ✓ | ✗ <missing>
  - weasel words in commit: ✓ none | ✗ <found>

  (If REJECTED — add)
  **Reason for rejection:**
  <specific reason>

  **Fix instructions:**
  <how to fix; either revert + re-instruct, or specific corrections>

  **Re-run:** `/bq-implement delegate T-D-<n>` after fix
-->

(populated by `/bq-review delegate` Phase 3)

---

## Action items (if not fully approved)

1. <action>
2. <action>

## Cost summary

- Phase 1 (strong model planning): ~<tokens>, ~$<USD>
- Phase 2 (cheap model implementation): ~<tokens>, ~$<USD>
- Phase 3 (strong model review): ~<tokens>, ~$<USD>
- **Total:** ~$<sum>
- **vs. strong model end-to-end:** ~$<comparison>
- **Savings:** ~<%>

## Final verify

After action items above are complete:
- Run `/bq-verify` for full gate matrix
- If PASS → `/bq-changelog` then `/bq-release`
