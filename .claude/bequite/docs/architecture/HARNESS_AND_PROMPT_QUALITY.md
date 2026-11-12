# Harness & Prompt Quality (authoring standard for BeQuite commands & skills)

The standard every new BeQuite command, skill, and CLAUDE.md edit is held to. Grounded in Anthropic guidance (cited inline by source name). Read this before authoring or editing any `.claude/commands/*.md`, `.claude/skills/*/SKILL.md`, or `CLAUDE.md`.

BeQuite is a **no-runtime markdown pack** — no Studio, no CLI, no daemon. The "harness" here is the prompt surface: commands, skills, hooks, sub-agents, and memory files. These levers, applied well, are what make the pack reliable.

---

## TL;DR — the rules that catch the most mistakes

| # | Rule | Source |
|---|------|--------|
| 1 | Use the simplest pattern. Add an "agent" only when you can't hardcode the path. | Anthropic *building-effective-agents* |
| 2 | A **workflow** (fixed code path) beats an **agent** (model-directed path) whenever the steps are predictable. | *building-effective-agents* |
| 3 | Every action command ENDS by running a check and SHOWING the evidence. No evidence = not done. | *Claude Code best-practices*, ADR-002 |
| 4 | Verification/feedback loops are the highest-leverage lever — invest there first. | *effective-harnesses* |
| 5 | When authoring prompts: be explicit, tell what TO do, give 3-5 canonical examples, repeat the output format at the END. | *prompt-engineering overview*, *multishot* |
| 6 | Keep CLAUDE.md LEAN (<200 lines). Bloated context = ignored rules. | *Claude Code best-practices* |
| 7 | Right-altitude: give strong heuristics + decision questions, not brittle step-scripts. | *effective-harnesses*, *writing-tools-for-agents* |

---

## 1. Harness principles (3)

From Anthropic *building-effective-agents* and *writing-tools-for-agents*:

| Principle | Meaning for BeQuite | Test applied at review |
|-----------|--------------------|------------------------|
| **Simplicity** | Fewest moving parts that solve the task. No new command if an existing one + a flag covers it. | "Could a flag on an existing command do this?" |
| **Transparency** | The agent's plan and steps are visible to the user — show the route, show the gate, show the evidence. | "Does the command surface what it did and why?" |
| **ACI (agent-computer interface)** | The contract between agent and its tools/files is documented as carefully as a human API: clear names, clear inputs, clear outputs, examples, no ambiguous overlap. | "Are the files this reads/writes named + described unambiguously?" |

> **Load-bearing rule:** *"Use the simplest pattern; add agents only when you can't hardcode the path."* (*building-effective-agents*) Most BeQuite features are workflows, not agents.

ACI quality is the difference between a tool the model uses correctly and one it misuses. For BeQuite, the "tools" are the memory files and the commands themselves — name them, scope them, and document inputs/outputs so the model never guesses.

---

## 2. Workflow-pattern map — what BeQuite already is

*building-effective-agents* names five workflow patterns plus the autonomous-agent pattern. BeQuite already implements most as fixed code paths. **Rule: don't reach for an "agent" when a workflow suffices.**

| Anthropic pattern | What it is | BeQuite feature(s) that already are this |
|-------------------|-----------|------------------------------------------|
| **Prompt chaining** | Decompose into fixed ordered steps; gate between them | Phase orchestrators `/bq-p0`…`/bq-p5`; the 6-phase P0→P5 pipeline |
| **Routing** | Classify input, dispatch to a specialist path | `/bq-feature` 12-type router · `/bq-fix` 15-type router · `/bq-auto` 17-intent router · `/bq-suggest` situation→route |
| **Parallelization** | Run independent variants/voices, then aggregate | `/bq-uiux-variants` (1-10 isolated directions) · `/bq-multi-plan` (parallel/specialist/debate voices) · `/bq-red-team` (10 attack angles) |
| **Orchestrator-workers** | A lead plans + farms subtasks to workers | `/bq-auto` (walks phases, dispatches scope) · Delegate Mode (strong model writes task pack, cheap model implements) |
| **Evaluator-optimizer** | Generate → evaluate → refine in a loop | `/bq-verify` → `/bq-fix` → re-verify loop · `/bq-review` findings → patch |
| **Autonomous agent** | Open-ended, model directs its own path | Used sparingly; only `/bq-auto` is near-autonomous, and it is **scoped** + pauses at the 17 hard human gates |

**Authoring consequence:** before proposing a new "smart" command, name which of the five patterns it is. If it's a fixed sequence, write it as a chained/routed workflow with explicit steps — not as an open-ended agent prompt. (*building-effective-agents*)

---

## 3. Verification / feedback loops — the highest-leverage lever

*effective-harnesses*: the single biggest reliability gain comes from giving the agent a way to **check its own work and act on the result**. BeQuite encodes this as a hard convention.

**Rule:** every action-taking command ENDS by running a check and SHOWING the evidence (command output, file diff, test result, screenshot). This is also Iron Law X (ship operationally complete) and rule #2 ("never claim done unless `/bq-verify` passes").

### Escalation ladder (cheapest first)

| Tier | Mechanism | When to use | BeQuite location |
|------|-----------|-------------|------------------|
| 1 | **In-prompt self-check** — the command re-reads the goal and confirms output matches before claiming done | Every action command | command body, final step |
| 2 | **Re-checked goal** — restate acceptance criteria, diff actual vs expected, list any gap | Multi-step or risky changes | `/bq-implement`, `/bq-feature` |
| 3 | **Stop hook** — deterministic gate the runtime enforces regardless of model judgment | Rules that must never be skipped (weasel-word ban, evidence-before-done) | `.claude/settings.json` hooks (*hooks docs*) |
| 4 | **Fresh-context verifier sub-agent** — a clean agent re-verifies with no memory of how the work was done | Release, audits, "is this really fixed?" | `/bq-verify`, `/bq-red-team` run as isolated context |

> A fresh-context verifier avoids the failure mode where the same context that wrote the bug also "confirms" the fix. (*effective-harnesses*, *reduce-hallucinations*) Isolating context for the check is what makes the evidence trustworthy.

**Banned in any completion report:** should, probably, seems to, appears to, I think it works, might, hopefully, in theory. Replace with the concrete check that was run, or explicitly state the check was NOT run. (rule #6)

---

## 4. Prompt-engineering reliability stack (for authoring NEW commands & skills)

Apply this stack to every new command/skill body. Cited from *prompt-engineering overview* and *multishot*.

| Lever | Do this | Why |
|-------|---------|-----|
| **Be explicit** | State the exact behavior, inputs, outputs, and stop conditions. No implied steps. | Models follow what is written, not what is meant. (*prompt-engineering overview*) |
| **Tell what TO do** | Phrase as positive instructions ("write the report to X"), not only prohibitions. | Negative-only framing leaves the model guessing the desired action. (*prompt-engineering overview*) |
| **3-5 CANONICAL examples** | Show typical, correct usage — not a dump of every edge case. | Multishot lifts reliability most when examples are representative, not exhaustive. (*multishot*) |
| **XML / Markdown sections** | Delimit role, context, instructions, examples, output format with clear headers/tags. | Structure reduces cross-contamination of instructions. (*prompt-engineering overview*) |
| **Give a role** | Open with the persona/expertise the command operates as. | Role priming sharpens domain behavior. (*prompt-engineering overview*) |
| **Let it think** | Allow a reasoning/plan step before the output for non-trivial tasks. | Reasoning-before-answer reduces errors. (*prompt-engineering overview*) |
| **Repeat output format at the END** | Restate the required output shape as the final lines of the prompt. | Claude weights the END of long prompts; the last instruction wins ties. (*prompt-engineering overview*) |
| **Right-altitude** | Encode strong heuristics + the 10 decision questions, not brittle line-by-line scripts. | Over-specified scripts break on the first unforeseen case; heuristics generalize. (*effective-harnesses*, *writing-tools-for-agents*) |

**Anti-pattern to avoid:** stuffing the body with rare edge cases. Push heavy/rarely-needed reference into a sibling file (e.g. `reference.md` next to `SKILL.md`) and keep the body focused. Claude truncates skill bodies keeping the START — put the most load-bearing content first.

---

## 5. Keep CLAUDE.md LEAN

*Claude Code best-practices*: **"a bloated CLAUDE.md means ignored rules."** Every token in CLAUDE.md is read on every session — it competes for attention with the user's actual task.

| Rule | Detail |
|------|--------|
| **Target < 200 lines** | If it grows past that, something belongs in a skill or a doc. |
| **Per-line test** | For each line ask: *"would removing this cause a concrete mistake?"* If not, cut it. |
| **Push sometimes-relevant detail into skills** | Detail needed only for UI work, only for DB work, etc. lives in the matching skill, loaded on demand. |
| **Use IMPORTANT / YOU MUST sparingly** | Emphasis works only when rare. Marking everything critical marks nothing critical. (*Claude Code best-practices*) |
| **HTML comments are free** | `<!-- ... -->` is stripped before the model reads it — use for maintainer notes without spending the model's attention. |
| **Codebase map, not a manual** | CLAUDE.md is a map ("where things live", "what to read first"), not exhaustive documentation. (*codebase maps* article) |

The "Required reads on every session start" list in CLAUDE.md is the canonical codebase-map pattern: a short pointer list, not the content itself.

---

## 6. The five harness levers for a no-runtime markdown pack

BeQuite has no daemon, so its harness is these five surfaces. Use the lightest one that solves the problem.

| Lever | What it is | Use when | Freshness/cost note |
|-------|-----------|----------|---------------------|
| **Lean CLAUDE.md** | Always-loaded codebase map + non-negotiable rules | Rule applies to every session | Cheapest attention if kept small; most expensive if bloated |
| **On-demand skills** | `SKILL.md` loaded only when its `description` triggers match | Procedure needed only in a domain/situation | Zero cost until triggered — push detail here |
| **Deterministic hooks** | Runtime-enforced gates in `.claude/settings.json` | A rule must hold regardless of model judgment | Not subject to model attention — guarantees the gate (*hooks docs*) |
| **Context-isolated sub-agents** | Fresh-context agent for a scoped job (verify, red-team, research) | Need an unbiased check or a big-context job that shouldn't pollute the main thread | Isolation is the value; the verifier hasn't "seen" the buggy reasoning (*effective-harnesses*) |
| **External memory files** | `.bequite/**` markdown state | Cross-session continuity (state, gates, decisions, logs) | MUST carry freshness metadata: last-updated timestamp + the command that wrote it; stale memory loses to active-session evidence (*reduce-hallucinations*) |

> Memory freshness rule (CLAUDE.md "When in doubt"): *latest-verified-research beats memory; active session evidence beats memory of a previous run.* Every memory write stamps who/when so readers can judge staleness.

---

## 7. New command / skill authoring checklist

Run this before shipping any new command or skill. Pair with the alpha.14 15-step feature-addition workflow (this checklist covers the *quality* of the artifact; that workflow covers the *process*).

### For a new COMMAND (`.claude/commands/bq-*.md`)

- [ ] Named which workflow pattern it is (chain / route / parallel / orchestrator / evaluator) — §2. If "agent", justified why a workflow can't do it.
- [ ] Most load-bearing content is at the TOP (Claude keeps the start).
- [ ] Role stated; explicit positive instructions; stop conditions defined — §4.
- [ ] 3-5 canonical examples, not an edge-case dump — §4.
- [ ] Output format restated at the END of the body — §4.
- [ ] Right-altitude: heuristics + decision questions, not a brittle line-script — §4.
- [ ] ENDS with a verification step that runs a check and SHOWS evidence — §3.
- [ ] No banned weasel words anywhere in the body or its report template.
- [ ] Declares which gates it requires + which gate(s) it satisfies (refuses if prerequisites unmet — rule #11).
- [ ] Reads core memory first (state/mode/phase/gates/last-run); writes back with freshness stamp — §6.
- [ ] Registered in `/bequite` menu, `/bq-help`, `commands.md`, `COMMAND_CATALOG.md` (alpha.14 steps 9-11).

### For a new SKILL (`.claude/skills/bequite-*/SKILL.md`)

- [ ] YAML frontmatter: `name`, `description`, `allowed-tools`.
- [ ] `description` STARTS with "Use when …" and states ONLY triggers — never the workflow.
- [ ] Body focused; heavy reference pushed to a sibling file (`reference.md`).
- [ ] Most load-bearing content first; canonical examples over edge cases — §4.
- [ ] Ends with `## When NOT to use this skill` + `## Quality gate` sections (alpha.15 convention).
- [ ] Right-altitude — strong heuristics, not a fragile script — §4.
- [ ] Triggers are specific enough to avoid false activation, broad enough to catch real cases (ACI clarity — §1).

### For a CLAUDE.md edit

- [ ] Total file < 200 lines after the edit — §5.
- [ ] Per-line test passed: every added line would cause a concrete mistake if removed — §5.
- [ ] Sometimes-relevant detail routed to a skill or doc, not added inline — §5.
- [ ] IMPORTANT / YOU MUST used only where adherence genuinely requires it — §5.
- [ ] Maintainer-only notes placed in HTML comments (free attention) — §5.

---

## Sources cited

Anthropic *building-effective-agents* · *writing-tools-for-agents* · *prompt-engineering overview* · *multishot* (multishot prompting) · *Claude Code best-practices* · *effective-harnesses* (effective context engineering / harnesses) · *reduce-hallucinations* · *hooks docs* · the *codebase maps* article. BeQuite internal: ADR-002 (mandatory gates), Iron Law X, CLAUDE.md core operating rules.
