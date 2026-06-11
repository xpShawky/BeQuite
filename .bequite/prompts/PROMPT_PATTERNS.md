# Prompt Patterns (alpha.19)

> Reusable skeletons per `docs/architecture/PROMPT_ENGINEERING_STANDARD.md`. Fill the brackets; delete unused lines. Most important constraint goes FIRST.

---

## Pattern 1 — Complete (Deep Mode)

```
ROLE: You are <specialist> working on <project> (<stack, from PROJECT_DNA>).
GOAL: <one sentence, observable outcome>.
CONSTRAINTS (in priority order):
  1. <hard constraint — safety/scope>
  2. <DNA conformance — cite PROJECT_DNA / DESIGN_DNA / WRITING_DNA section>
  3. <quality bar + acceptance criteria>
SOURCES: <research report paths · spec paths · user-provided files>. Facts come from sources; label anything else [Assumption].
OUTPUT FORMAT: <exact artifact + structure>.
VERIFY: <command(s) to run + expected result>. Log evidence to EVIDENCE_LOG.md.
```

## Pattern 2 — Compact (Token Saver)

```
GOAL: <one sentence>. CONTEXT: see <artifact paths — do not re-derive>.
CONSTRAINTS: <only the binding ones>. OUTPUT: <format>. VERIFY: <check>.
```

## Pattern 3 — Neutral packet (multi-plan / delegate)

```
BRIEFING (identical for every model — contains NO prior conclusions):
  PROBLEM: <raw problem statement>
  KNOWN FACTS: <verified facts only, each with source>
  CONSTRAINTS: <hard constraints>
  DELIVERABLE: <plan structure requested>
Do not include: any prior model's plan, preferences phrased as facts, leading alternatives.
[Architect's preference]: <opinions go here, labeled, delegate packs only>
```

## Pattern 4 — Strict (source fidelity)

```
SOURCES: <files/URLs — the ONLY permitted fact base>.
RULE: every claim in the output traces to a source line. No additions. No invented citations.
If a needed fact is absent from sources: write "UNVERIFIED: <fact>" and continue — never fill the gap from memory.
GOAL: <transform — summarize/restructure/rewrite> while preserving meaning.
OUTPUT: <format>. Cite as: <citation style>.
```

## Pattern 5 — One high-value question

```
Proceeding requires one decision I can't resolve from <what was checked>:
Q: <question>?  Recommended default: <option + one-line why>.
(If no answer, I'll proceed with the default and log it to ASSUMPTIONS.md.)
```
