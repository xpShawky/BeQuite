# Export log

> Written by `/bq-presentation` when an output file is rendered. One entry per export attempt.

> Captures: tool chosen, output path, verification result, and the decision section ref.

---

## Export 1 — `<timestamp>`

- **Format:** `<pptx | html>`
- **Variant:** `<base | Variant K>`
- **Tool / library:** `<name + version>`
- **Decision section ref:** `DECISIONS.md#ADR-XXX`
- **Output path:** `.bequite/presentations/outputs/...`
- **Slide count:** N
- **File size:**
- **Speaker notes included:** yes/no
- **References slide included:** yes/no
- **Animations:** count + summary
- **Verification result:** PASS / PARTIAL / FAIL
- **Verification notes:**
  - [ ] Opens in target tool (PowerPoint / browser)
  - [ ] All slides render without missing fonts / images
  - [ ] Motion plays correctly
  - [ ] Speaker notes visible in presenter mode
  - [ ] References resolve
  - [ ] Brand identity consistent
- **User-visible result:**

---

## Export 2 — `<timestamp>`

(repeat block)

---

## Aggregate notes

- (Cross-format lessons learned)
- (Tools that worked well for this project type)
- (Tools to avoid for similar work next time → also append to `.bequite/state/MISTAKE_MEMORY.md`)
