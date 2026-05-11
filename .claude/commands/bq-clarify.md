---
description: Ask the user 3-5 high-value clarifying questions. Skips anything obvious. Writes answers to .bequite/state/OPEN_QUESTIONS.md.
---

# /bq-clarify — high-value questions only

You are asking the user **exactly 3-5 clarifying questions** that will materially change the implementation. No filler. No "what's your favorite color" trivia.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md` (especially section 11 "Missing information")
- `.bequite/audits/DOCTOR_REPORT.md` (especially the Blockers section)
- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/DECISIONS.md`

If `DISCOVERY_REPORT.md` doesn't exist, suggest running `/bq-discover` first.

## Step 2 — Pick the 3-5 questions

**Good question signals:**
- The answer changes the architecture (e.g. "monolith vs microservices")
- The answer changes the stack (e.g. "SQLite or Postgres?")
- The answer changes the scope (e.g. "is multi-tenant required for v1?")
- The answer affects compliance (e.g. "PHI / PCI / GDPR involved?")
- The answer affects scale (e.g. "10 users or 10,000?")
- The answer locks one ADR (e.g. "Better-Auth or Clerk?")

**Skip these (don't ask them):**
- Questions whose answers are already in DISCOVERY_REPORT
- Aesthetic preferences (gradients, animation speed) — those go in `/bq-add-feature` per-feature
- Questions you can decide with a recommended default

For each question, also give a **Recommended default** the user can accept by just saying "yes" or "all defaults".

## Step 3 — Present them

Print this in the chat:

```
Five clarifying questions (or fewer). You can answer each individually,
say "all defaults" to accept every default at once, or say "skip" on
any single one.

Q1. <Question text — punchy, one sentence>
    Why it matters: <one sentence>
    Recommended default: <default>

Q2. ...

Q3. ...

Q4. (skip if not needed)

Q5. (skip if not needed)
```

## Step 4 — Wait for answers

Don't proceed until the user replies. Their answers can be:
- Specific (e.g. "Postgres", "Better-Auth", "10k users")
- "default" or "yes" → accept your recommended default
- "skip" → skip and use the recommended default silently
- "all defaults" → accept all defaults at once and move on

## Step 5 — Record answers

Update `.bequite/state/OPEN_QUESTIONS.md`:

```markdown
# Open questions

Latest round: <date>

## Resolved

### Q1. <question>
- Answer: <user's answer>
- Decided: <date>

### Q2. <question>
- Answer: <user's answer>
- Decided: <date>

### Q3. ...

## Still open

(items the user said "skip — come back later" to)
```

Also append a Decision entry to `.bequite/state/DECISIONS.md` for each resolved question.

## Step 6 — Report back

```
✓ Clarify complete

Resolved: <count> questions
Still open: <count>

Decisions recorded: .bequite/state/DECISIONS.md
Open items: .bequite/state/OPEN_QUESTIONS.md

Next: /bq-research (if any answer needs evidence) or /bq-plan (write the plan)
```

## Rules

- **Maximum 5 questions per round.** If more come up, ask the most critical 5; queue the rest as "next round" in OPEN_QUESTIONS.md.
- Each question must propose a **recommended default** so the user can quickly accept.
- Do NOT ask questions whose answers are already in the discovered repo state.

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/DOCTOR_REPORT.md`
- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `.bequite/state/OPEN_QUESTIONS.md` (updated)
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/LAST_RUN.md` (updated)
- `.bequite/logs/AGENT_LOG.md` (appended)

## Usual next command

- `/bq-research` if any answer needs library/freshness verification
- `/bq-plan` otherwise
