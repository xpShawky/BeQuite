# Command Router — operational routing map (alpha.22)

Strategy: `docs/architecture/WORKFLOW_COMMAND_ROUTER.md` · IDs: `COMMAND_ID_MAP.md` · log: `NEXT_COMMAND_LOG.md`.
Commands answer **what next**; skills answer **how well** (see `.bequite/skills/SKILL_ROUTER.md`).

## 1. Spine routes (gate-aware; PASS path)

```
W0.1 bequite → W0.2 init → W0.5 mode → W0.3 discover → W0.4 doctor
→ W1.1 clarify → W1.2 research → W1.3 scope → W1.4 plan [W1.6 multi-plan if high-stakes]
→ W2.1 assign → W2.2 implement (loop) | W2.3 feature | W2.4 fix
→ W3.1 test → W3.3 review [W3.2 audit · W3.4 red-team if risk]
→ Guard Pass (skill) → W4.1 verify → W4.3 changelog → W4.2 release (gate 17: user pushes)
→ W5.1 memory → W5.3 handoff
```

FAIL reroutes: verify FAIL → W2.4 fix (with `regressions` note) · review findings → W2.2 implement fixes · doctor blockers → fix env before W1 · gate blocked → emit the prerequisite command as Required next.

## 2. Signal → capability suggestions (only when signaled)

| Task signal | Suggest |
|---|---|
| slides / deck / lecture | C1 presentation |
| writing voice / human-style / scripts | C2 writing-dna |
| screenshot / competitor / "I like this style" | C3 reference (+ W2.5 variants) |
| docs pile / FAQ / chatbot / RAG | C4 knowledge |
| course / teach / curriculum / YouTube series | C5 course |
| niche / market pain / "what should I build" | C6 pain-radar |
| API / SDK / webhook / third-party service | C7 integrate |
| job post / client / RFP / bid | C8 proposal |
| find work | C9 job-finder · earn money | C10 make-money |
| Arabic / MENA / RTL / Egypt | localization-rtl **skill** (auto-attach; no command) |
| scrape / crawl / monitor a site / price-stock watch / automate a workflow | **scraping-automation skill** via W2.3 feature or O7 `/bq-auto scraping|automation` (API-first, Article VIII; future `/bq-automation` is parked V2) |

## 3. Journey routes (multi-command sets for /bq-suggest)

**"Monetize a niche"** → 1. C6 `/bq-pain-radar` (find verified pain first) → 2. C10 `/bq-make-money` (match pain to earning tracks) → 3. C8 `/bq-proposal` (pitch the chosen opportunity) → 4. C5 `/bq-course` *only if* an education product is viable → 5. W4.2 `/bq-release proof` once something ships. Order matters: evidence → opportunity → pitch → product → proof.

**"Create a course"** → 1. C5 `/bq-course` (validation + curriculum first, never slides first) → 2. C4 `/bq-knowledge build` if source docs exist → 3. C1 `/bq-presentation` when slides are needed → 4. C2 `/bq-writing-dna` for scripts/narration voice → 5. localization-rtl skill (or proposed `/bq-localize`) if Arabic/MENA.

**"I like this website style"** → 1. C3 `/bq-reference screenshot|url` (extraction + originality guardrails) → 2. W2.5 `/bq-uiux-variants` if multiple directions wanted → 3. W2.3 `/bq-feature` once a direction is approved → 4. W4.1 `/bq-verify` (visual QA + continuity gate) → 5. W4.2 `/bq-release proof` if it should become a case study.

**"Integrate an API"** → 1. C7 `/bq-integrate` (blueprint; UNVERIFIED markings) → 2. W1.4 `/bq-plan` to slot into the codebase → 3. W2.3 `/bq-feature` build → 4. W3.1 `/bq-test` (error matrix → tests) → 5. W4.1 `/bq-verify`. Skills: backend-architect + security-reviewer + testing-gate.

## 4. Output template (contract step 12)

```
Next Command Recommendations:
Required next:
- <ID> <cmd> — <reason> — can auto-run: yes/no — <why>
Recommended command set (2–6):
1. <ID> <cmd> <args> | Reason: | Skills likely used: | Can auto-run:
Optional accelerators:
- <cmd> — <why>
Do not run yet:
- <cmd> — <missing gate/artifact/order reason>
```

Auto mode instead reports: `Internal workflow executed: <ID list>` then the same block for what follows.

## 5. Standing "do not run yet" rules

- W4.2 release before W4.1 verify PASS — always blocked
- W2.x build before W1.3 scope locked (uncertain-scope gate)
- C8 proposal before any evidence of the opportunity (C6/C9 output or user-provided post)
- W2.5 variants winner merge before gate-16 user pick
- Any R3 file edit without explicit confirm — even in auto

## 6. Addendum signals (2026-06-12 — forgotten-candidate review)

| Task signal | Suggest |
|---|---|
| "app looks empty" / demo day / portfolio screenshots | `/bq-feature demo-data` (demo profile) |
| "can users actually use this?" / usability doubt / non-technical audience | `/bq-review persona` |
| new client / project kickoff / "what should I ask the client?" | `/bq-scope intake` (before the call) → `/bq-scope from-interview` (after) |
| "how much should I charge?" | `/bq-proposal price` (+ product-strategist pricing) |
| "record a walkthrough" / live demo | `/bq-release demo-video` (demo-script profile) |
| "package this project for resale" | `/bq-release template` (V2 — not yet built; say so) |
| "build me a sellable offer" | future C11 `/bq-offer` (alpha.23 queue — until built, route to C6 pain-radar + C8 proposal) |
