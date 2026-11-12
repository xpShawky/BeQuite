# Knowledge Engine — `/bq-knowledge` (C4) — alpha.22

Turn a docs pile into a usable knowledge product: knowledge pack, FAQ, glossary, troubleshooting trees, chatbot-ready KB, RAG blueprint, source-grounded Q&A with answer confidence.

## Modes

| Mode | Does |
|---|---|
| `build` | sources → chunked knowledge pack + FAQ + glossary + troubleshooting + intents |
| `ask` | source-grounded Q&A over an existing pack; every answer cites chunk IDs + carries confidence; no-source answer ⇒ `UNVERIFIED` or "not in sources" |
| `rag-plan` | architecture blueprint for a future RAG system (tool-neutral; local-model-compatible options documented) |
| `export` | pack → chatbot-ready / static-site / handoff formats |

## The two-tier honesty rule (documented in every output)

- **Without an LLM:** BeQuite builds a searchable pack and retrieves relevant chunks (extractive — quotes + locations). This works offline and is the default deliverable.
- **With an LLM:** synthesized natural answers grounded in those chunks.
Never promise a chatbot runtime by default. **No vector database, no embedding service, no RAG runtime installed by default** — `rag-plan` *plans* them tool-neutrally (compare options per the 10 decision questions; local-model paths included).

## Outputs — `.bequite/knowledge/`

KNOWLEDGE_PACK · CHUNK_MAP · SOURCE_INDEX · FAQ · GLOSSARY · TROUBLESHOOTING · INTENTS · RAG_BLUEPRINT · ANSWER_CONFIDENCE (created per mode on first run).

## Routing

Skills: researcher + anti-hallucination + context-engineer (no dedicated knowledge skill — deliberate, see shape decisions §3). Feeds C5 course (source materials) and client handoffs. Strict source fidelity honors Writing-DNA strict mode when generating prose.
