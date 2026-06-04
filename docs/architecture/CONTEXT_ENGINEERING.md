# Context Engineering (all workflows)

Strategy doc behind the `bequite-context-engineer` skill. Workflow-agnostic parent of `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md` (the UI specialization). Grounded in Anthropic guidance — sources cited inline.

---

## 1. The principle (read this first)

**Find the smallest set of high-signal tokens that maximizes the likelihood of the desired outcome.** (effective-context-engineering)

Three facts make this load-bearing, not optional:

| Fact | Source | Consequence |
|---|---|---|
| Context is a **finite, scarce resource** with diminishing marginal returns | effective-context-engineering | Every token added competes with every other token; more is not better. |
| **Context rot is real and measurable** — model accuracy drops as token count grows, even below the stated window | Chroma context-rot study | A "full but noisy" window performs worse than a small clean one. The middle gets buried. |
| The attention budget is depleted by **every** token, including stale memory, dead tool output, and redundant restatements | effective-context-engineering | Curate ruthlessly. Treat the window as a working set, not an archive. |

**Operating stance:** the goal is not to stuff context. The goal is to engineer the *minimal correct* context for the task at hand, then refresh it before it rots.

---

## 2. The three primitives + diagnostic table

Every context problem reduces to one of three moves (effective-context-engineering, effective-harnesses, memory docs):

| Primitive | What it does | When |
|---|---|---|
| **Compact** | Summarize the live window into a dense recap; drop dead tool output and resolved tangents | Window is filling; long session; many tool calls |
| **Clear** | Reset the window and re-load only what the *next* task needs | Switching tasks/domains; context is noisy or contradictory |
| **Externalize** | Write durable facts to a file (memory) instead of holding them in context; re-read on demand | Anything that must survive `/compact`, a session break, or a sub-agent |

**Symptom → primitive diagnostic:**

| Symptom | Primitive |
|---|---|
| Agent re-derives facts it already established earlier | Externalize (write it to memory; re-read) |
| Window is large and answers are getting vaguer / it forgets early instructions | Compact |
| Agent references a now-irrelevant task or stale plan | Clear, then re-load |
| Same convention re-explained every few turns | Externalize to path-scoped `.claude/rules/*.md` |
| Tool output (logs, file dumps) dominating the window | Compact (drop dead output) |
| Decision keeps flip-flopping across turns | Externalize the decision to `DECISIONS.md`; re-read |
| Memory file disagrees with what the code shows now | Refresh the artifact (freshness rule, §4) — a stale map is worse than no map |

---

## 3. What survives `/compact` (the survival rule)

`/compact` replaces the live window with a summary. **What is reliably re-injected after compaction is narrow** (Claude Code best-practices, memory docs):

| Survives `/compact` | Can be LOST |
|---|---|
| **Project-root `CLAUDE.md`** (re-injected) | Path-scoped / nested `CLAUDE.md` not in scope |
| **Auto-loaded memory** that the harness re-injects | Skill bodies (loaded on demand, not re-injected) |
| Anything you **re-read from a file** after compaction | Mid-window tool output and prose tangents |

Skill bodies are also **capped and truncated**: SKILL.md frontmatter description budget is small; bodies load on demand and are truncated **from the start kept first** when long (Claude Code best-practices). Two rules follow.

### Compaction-survival rule
> If a fact must outlive `/compact` or a session break, it lives in a **file** (project-root `CLAUDE.md`, auto-memory, or a `.bequite/` artifact you re-read) — never only in the live window. After `/compact`, re-read the orientation files (§5) before acting.

### Top-of-file rule
> Put the most load-bearing content at the **top** of every CLAUDE.md, SKILL.md, and memory file. Long bodies bury the middle (context rot, §1) and skill bodies truncate from the start. Lead with rules and contracts; push heavy reference to sibling files.

---

## 4. The generic memory contract (all workflows)

Externalized memory is only useful if it stays trustworthy. Every workflow uses the same shapes (memory docs, effective-context-engineering).

### Two anchor files per project

| File | Holds | Shape |
|---|---|---|
| `PROJECT_DNA.md` | Durable codebase conventions, architecture, stack, naming, layering, invariants — the stable "this is how this repo works" | Markdown narrative |
| `WORKING_NOTES.md` | Same-shape scratchpad per domain: what was tried, what worked, open threads, the next safe step | Markdown narrative |

`WORKING_NOTES.md` uses one **consistent shape** so any session (or sub-agent) can resume without re-deriving. The frontend cousin's Design DNA + section notes are the UI specialization of this exact pair (§7).

### Machine state vs narrative — split by consumer

| Content kind | Format | Why |
|---|---|---|
| Machine/agent state (gates met, current phase, mode, version, structured task lists) | **JSON** | Deterministic to parse and update; no ambiguity |
| Human/agent narrative (decisions, rationale, working notes, DNA) | **Markdown** | Reasoning and nuance survive; readable in handoff |

Rule: **machine-state-in-JSON, narrative-in-Markdown.** Do not encode reasoning in JSON or encode gate flags in prose.

### Path-scoped rules

Conventions that apply only to a subtree live in `.claude/rules/*.md` next to the code they govern, not in the root `CLAUDE.md`. This keeps the always-loaded root small and loads detail only when that path is in scope (Claude Code best-practices).

### Freshness metadata on every artifact

Every memory artifact carries a freshness header so a reader can trust or distrust it:

```
<!-- freshness: commit <hash> | <ISO-8601 timestamp> | refresh-when: <trigger> -->
```

- **commit hash** — the repo state the artifact describes
- **timestamp** — when it was written
- **refresh rule** — the trigger that makes it stale (e.g. "refresh when stack changes", "refresh after each release")

> **A stale map is worse than no map.** If the artifact's commit/trigger no longer matches reality, refresh it before trusting it (diagnostic table, §2). Out-of-date memory actively misleads; the freshness header is what lets a reader catch that.

---

## 5. Session ritual + work discipline

### Session-orientation ritual (every session start, and after every `/compact`)

Re-read, in order — these are the files that survive or must be re-loaded:

1. project-root `CLAUDE.md`
2. `PROJECT_DNA.md`
3. machine state (phase / mode / gates, JSON)
4. `WORKING_NOTES.md` (current domain) + last few `AGENT_LOG.md` entries

Skipping orientation after `/compact` is the most common cause of re-derived, contradictory work (compaction-survival rule, §3).

### Work discipline

- **One task at a time.** Load only the context that task needs; finish or checkpoint before switching (clear primitive, §2). Reduces rot and keeps the window high-signal.
- **Never edit tests to make them pass.** Fix the code or fix the test for a real reason. Editing assertions to go green is a hallucinated success and corrupts the verification signal (reduce-hallucinations, demystifying-evals). If a test blocks, diagnose; do not silence it.
- **Verify before claiming done.** Evidence over assertion — no weasel words. (reduce-hallucinations)

---

## 6. Sub-agent isolation + the multi-agent cost rule

Sub-agents get **isolated context windows**: the parent delegates a scoped task, the sub-agent burns its own window on exploration, and returns only a **distilled result** to the parent (effective-context-engineering, effective-harnesses). This protects the parent's window from rot.

| Use sub-agents for | Avoid sub-agents for |
|---|---|
| Read-heavy exploration (search, audit, research, "find where X is") | Token-cheap or trivial work |
| Tasks whose intermediate output is large but whose answer is small | Anything where the cost outweighs the context saved |

**The ~15x rule:** a multi-agent fan-out can consume on the order of **15x the tokens** of a single-agent chat (Anthropic multi-agent research guidance). Justify the spend. The pattern earns its cost **only when read-heavy** — when a sub-agent reads a lot and returns a little, keeping the parent window clean. For write-heavy or coordination-tight work, a single agent is cheaper and safer.

Each sub-agent gets the orientation files it needs (§5) and writes durable findings back to memory (externalize, §2) so the result survives the sub-agent's own teardown.

---

## 7. Relationship to the frontend cousin

`docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md` is the **UI specialization** of this doc. The mapping is exact:

| General (this doc) | Frontend specialization |
|---|---|
| `PROJECT_DNA.md` — codebase conventions/architecture | **Design DNA** — tokens, type scale, spacing, component identity |
| Consistency check (memory vs reality, §4 freshness) | **Design Continuity Gate** — every section matches the Design DNA hero-to-footer |
| `WORKING_NOTES.md` per domain | Section-by-section UI notes / `SECTION_MAP.md` |
| Externalize → re-read | Re-read Design DNA before each section edit |

If a rule here changes, the frontend cousin inherits it. The frontend doc adds UI-only mechanics (visual QA, slop detection); it does not contradict the primitives, the survival rule, or the freshness rule.

---

## 8. Effort awareness

Match context spend to task stakes (effective-harnesses, demystifying-evals):

| Stakes | Context posture |
|---|---|
| Trivial / single-file edit | Minimal load; skip sub-agents; no new memory artifact |
| Standard feature/fix | Full orientation ritual; update `WORKING_NOTES.md` + log |
| High-stakes / irreversible / regulated | Full ritual + sub-agent exploration + refreshed `PROJECT_DNA.md` + recorded decision; more verification passes |

Higher effort buys more context-loading, more sub-agent exploration, and more verification — not more raw tokens for their own sake. The principle (§1) holds at every level: smallest high-signal set that maximizes the right outcome.

---

## Cited sources

- **effective-context-engineering** — smallest high-signal token set; context as scarce resource; compact/clear/externalize; sub-agent isolation; machine-vs-narrative split.
- **effective-harnesses** — harness/context discipline; effort awareness; sub-agent delegation.
- **Chroma context-rot study** — measurable accuracy decay as token count grows.
- **memory docs / context-window docs** — what auto-memory re-injects; durable memory shapes.
- **Claude Code best-practices** — `/compact` survival; CLAUDE.md re-injection; skill body caps/truncation; path-scoped rules.
- **reduce-hallucinations** — never edit tests to pass; verify before claiming; no weasel words.
- **demystifying-evals** — verification signal integrity; effort-to-stakes matching.
- **multi-agent research guidance** — ~15x multi-agent token cost; read-heavy justification.
