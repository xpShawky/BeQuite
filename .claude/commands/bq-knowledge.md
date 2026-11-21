---
description: "Turn source material into structured knowledge and blueprints. Modes - build / ask / rag-plan / export (a knowledge pack from docs), recording (a long video, lecture or meeting into notes and assets), reference (a screenshot, URL or app flow into a clone-safe design blueprint), integrate (API docs into an integration blueprint), automation (a workflow or bot idea into a tool-neutral automation blueprint). Grounded in the sources; installs nothing."
---

# /bq-knowledge: sources into knowledge and blueprints

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks).
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

One command for "here is material, make it usable": documents, recordings, reference designs, API docs and workflow ideas. Each mode's full spec lives in `.claude/bequite/docs/specs/`. Every derived line traces back to a source; what is not in the sources is said to be missing, never improvised.

## Syntax and modes

```
/bq-knowledge build "<folder / files / URLs>"            knowledge pack, FAQ, glossary, troubleshooting, intents
/bq-knowledge ask "<question>"                            grounded answer over an existing pack, with confidence
/bq-knowledge rag-plan "<target use>"                     tool-neutral retrieval blueprint (plans only)
/bq-knowledge export "<format / target>"                  chatbot-ready, static or hand-off bundle
/bq-knowledge recording "<YouTube URL | video | audio | transcript | subtitles>"
/bq-knowledge reference screenshot|url|flow "<goal>" [style=<direction>]
/bq-knowledge integrate "<API docs URL | OpenAPI path>" [stack=<stack>] [workflow="<flow>"]
/bq-knowledge automation "<workflow in plain words>" | bot "<purpose + platform>" | workflow "<trigger -> steps -> action>"
```

| Mode | Produces | Spec | Writes |
|---|---|---|---|
| build / ask / rag-plan / export | source index, chunk map with stable IDs, knowledge pack, FAQ, glossary, troubleshooting trees, chatbot intents; grounded answers; a retrieval blueprint | `KNOWLEDGE_ENGINE.md` | `.bequite/knowledge/` |
| recording | clean summary, chapter map, notes, action items, repurposing ideas, a searchable pack; transcript first (the `bequite-video-intel` ladder for videos) | `RECORDING_TO_ASSETS.md` | `.bequite/recordings/` |
| reference | the design system of a screenshot or site (type, colour, spacing, components), a rebuild blueprint with originality guardrails, a better version of an app flow | `REFERENCE_ENGINE.md` | `.bequite/reference/`, `.bequite/design/` |
| integrate | auth flow, endpoint map, error matrix, retries and idempotency, rate limits, test plan, an example skeleton for the stack | `INTEGRATION_BLUEPRINT.md` | `.bequite/integrations/` |
| automation | trigger map, action map, data flow, the tool decision (official API first), retry and failure plan, secret handling, a bot profile | `AUTOMATION_ENGINE.md` | `.bequite/automation/` |

## Gates and rules

- `BEQUITE_INITIALIZED`. `ask` and `export` need `.bequite/knowledge/KNOWLEDGE_PACK.md` (else run `build`).
- Plans only: no vector database, RAG runtime, SDK or automation platform is installed by this command; building goes through `/bq-feature` after the user approves the blueprint's tool choice.
- reference never copies protected assets, code or copy; it extracts the system and rebuilds originally (`bequite-human-taste`).
- integrate and automation read the provider's own docs on the day (researcher); secrets are named, never written.

## Steps (any mode)

1. Inventory the sources and say which mode runs.
2. Follow the mode's spec; cite the source (chunk ID, timestamp, URL or doc section) for every derived line.
3. Mark confidence per answer or blueprint section; list what the sources do not cover.
4. Write the outputs to the mode's folder and the work's `evidence.md`.

## Skills

researcher · anti-hallucination · context-engineer · video-intel (recording) · human-taste and ux-ui-designer (reference) · backend-architect and security-reviewer (integrate) · automation (automation, bots) · writing-dna (strict prose fidelity) · localization-rtl (Arabic sources).

## Next Command Recommendations (typical)

- After build: `/bq-content course` (teaching material) · `export` (a chatbot) · `/bq-presentation` (a deck).
- After reference: `/bq-uiux-variants` or `/bq-feature` with the blueprint.
- After integrate or automation: `/bq-feature` to build it, once the tool choice is approved.
