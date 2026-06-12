---
description: Knowledge Engine (C4). Turn docs into a knowledge pack, FAQ, glossary, troubleshooting trees, chatbot-ready KB, RAG blueprint, or source-grounded Q&A with answer confidence. Modes — build / ask / rag-plan / export. Extractive without an LLM; synthesized with one. No vector DB or RAG runtime installed by default.
---

# /bq-knowledge — docs → knowledge products (C4)

Full spec: `docs/specs/KNOWLEDGE_ENGINE.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block.

## Syntax

```
/bq-knowledge build "<sources: folder / files / URLs>"
/bq-knowledge ask "<question>"          ← grounded Q&A over an existing pack
/bq-knowledge rag-plan "<target use>"   ← tool-neutral RAG architecture blueprint
/bq-knowledge export "<format/target>"  ← chatbot-ready / static / handoff bundle
```

## Preconditions / gates

`BEQUITE_INITIALIZED`. `ask`/`export` require an existing `.bequite/knowledge/KNOWLEDGE_PACK.md` (else: refuse, recommend `build` first).

## Steps (after contract steps 1–7)

**build:** inventory sources → `SOURCE_INDEX.md` · chunk with stable IDs → `CHUNK_MAP.md` · assemble `KNOWLEDGE_PACK.md` · derive `FAQ.md` + `GLOSSARY.md` + `TROUBLESHOOTING.md` (decision trees) + `INTENTS.md` (chatbot intents). Every derived line traces to chunk IDs.
**ask:** retrieve relevant chunks → answer **grounded in sources only**, citing chunk IDs, with confidence per `ANSWER_CONFIDENCE.md` bands. Not in sources ⇒ say "not in sources" — never improvise.
**rag-plan:** `RAG_BLUEPRINT.md` — compare retrieval options (keyword/extractive vs embeddings; hosted vs local models) per the 10 decision questions. **Plans only — installs nothing.**
**export:** package the pack for the requested target; note the two-tier honesty rule (extractive vs LLM-synthesized) in the export.

## Writes

`.bequite/knowledge/{KNOWLEDGE_PACK,CHUNK_MAP,SOURCE_INDEX,FAQ,GLOSSARY,TROUBLESHOOTING,INTENTS,RAG_BLUEPRINT,ANSWER_CONFIDENCE}.md` (per mode) + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

researcher · anti-hallucination (citation-or-strike on every derived claim) · context-engineer · writing-dna strict mode when prose fidelity matters · localization-rtl on Arabic sources.

## Next Command Recommendations (typical)

After `build`: set = C5 `/bq-course` (if teaching material) · `export` (if chatbot/KB target) · C1 `/bq-presentation` (if the pack should become a deck). Do not run yet: `rag-plan` implementation builds before the blueprint's tool decision is approved.
