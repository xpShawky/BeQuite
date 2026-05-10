# Project Brief: {{PROJECT_NAME}}

> **Source of truth for scope.** When the team disagrees about what we're building, this file wins. When this file disagrees with new direction, amend this file (don't whisper the new direction into a chat).
>
> Read this on every session start (Article III). Update only via explicit decision, recorded in the `## Revisions` section at the bottom.

---

## 1. The product in one sentence

{{ONE_SENTENCE_PRODUCT}}

## 2. Who it's for

- **Primary user:** {{PRIMARY_USER}} — what problem do they currently solve manually or with a competitor?
- **Secondary user(s):** {{SECONDARY_USERS}} — second-order beneficiaries.
- **Explicit non-users:** {{NON_USERS}} — who this product is *not* for.

## 3. The problem

What is broken in the world without this product? Quote the user; don't paraphrase. Cite at least one piece of evidence (interview, support ticket, market data, personal pain log).

## 4. The success criteria

How do we know this product is working — quantitatively and qualitatively? Numbers when possible.

| Criterion | Threshold | How measured |
|---|---|---|
| | | |

## 5. The hard constraints

- **Scale tier:** {{SCALE_TIER}}  (Article V binding)
- **Compliance:** {{COMPLIANCE}} (PCI / HIPAA / SOC 2 / FedRAMP / GDPR / none)
- **Locale(s):** {{LOCALES}}  (e.g. `en-US`, `ar-EG`, `en-US,ar-EG`)
- **Audience flag:** {{AUDIENCE}}  (engineer / vibe-handoff)
- **Active Doctrines:** {{ACTIVE_DOCTRINES}}
- **Cost ceiling:** {{COST_CEILING}}  (per-session USD for AI assistance)
- **Wall-clock ceiling:** {{WALLCLOCK_CEILING}}  (per-session hours for autonomous mode)

## 6. Explicit non-goals

What we will NOT build, even if asked. Avoiding scope creep is half the work.

- {{NON_GOAL_1}}
- {{NON_GOAL_2}}

## 7. The hand-off bar

When can a second engineer take this project from us? They can run locally + deploy from `HANDOFF.md` alone. If `HANDOFF.md` doesn't pass that test, the project is not done.

## Revisions

```
{{REVISIONS_LOG}}
```
