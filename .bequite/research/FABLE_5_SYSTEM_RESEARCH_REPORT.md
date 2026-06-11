# BeQuite — Fable 5 System Research Report

**Run:** 2026-06-11 · Deep Mode · Claude Fable 5
**Method:** principle extraction from established ecosystems (tool-neutral: sources cited by ecosystem, principles captured — not implementations copied). Builds on `.bequite/research/BEQUITE_SYSTEM_RESEARCH_REPORT.md` (alpha.14) and the 6 cited research streams from alpha.18 — **no-research-repeat rule applied**: prior findings referenced, not re-derived.

---

## 1. Sources reviewed (by ecosystem)

**Claude Code platform:** slash commands (markdown dispatch) · Skills (SKILL.md progressive disclosure, description-based activation) · hooks (PreToolUse/PostToolUse/Stop/SessionStart, exit-2 block semantics, `stop_hook_active` guard) · subagents (isolated context windows, result-only return) · memory (CLAUDE.md auto-load, /compact behavior, 5-min prompt-cache TTL) · auto-mode failure modes (assumption stacking, context drift after compaction, premature "done" claims)
**Spec-driven:** GitHub Spec Kit (9-command loop, spec-as-contract) · BMad Method (agent persona + brief + checklist packs)
**Workflow systems:** Superpowers-style skill packs (mandatory skill invocation before response; TDD/debugging/verification-before-completion as rigid skills; brainstorm-before-build) · OpenClaw-style harnesses (heartbeat loops, gateway control plane — heavyweight)
**Context engineering:** Cline Memory Bank · Letta/MemGPT hierarchical memory · compaction-survival patterns (critical facts in always-loaded files) · context-pack pattern (curated minimal file set per task type)
**Safety/verification:** OWASP LLM Top 10 2025 · PhantomRaven/Shai-Hulud supply chain · file-risk tiering in enterprise CI (CODEOWNERS-style sensitive-path lists) · visual QA agents (screenshot-diff loops)
**Creative:** PowerPoint Morph / Keynote Magic Move object-continuity · reveal.js/Slidev/Marp · brand-voice extraction systems · style-transfer writing systems (corpus → style profile → constrained generation) · academic-writing assistants (citation fidelity, no-fabrication constraints)
**Shipping:** release-gate checklists · last-mile verification (fresh-clone test, smoke matrix) · "ship readiness" scorecards

## 2. What applies to BeQuite

1. **Execution contract as a single citable artifact** (Superpowers' rigid-skill insight): discipline holds better when a command can say "per COMMAND_EXECUTION_CONTRACT step 8" than when rules are diffused. → COMMAND_EXECUTION_CONTRACT.md.
2. **Context packs** (enterprise context engineering): every task TYPE gets a named minimal file set. BeQuite already has 4 implicit packs (frontend, presentation, opportunity, delegate) — naming the pattern makes the 5th+ packs (writing, backend) cheap to add. → CONTEXT_ENGINEERING_STRATEGY.
3. **Evidence ledger** (verification systems): claims die at compaction unless evidence is externalized. A per-run EVIDENCE_LOG that anti-hallucination writes to makes "citation-or-strike" durable. → EVIDENCE_LOG.md.
4. **Style profile → constrained generation** (style-transfer research): the robust pattern is corpus analysis → explicit profile document → generation constrained by profile → review against profile. NOT "write like a human" prompting, which produces generic median text. This is exactly the Writing DNA shape. Ethical line: improve quality/fidelity/voice; never promise detector evasion; never fabricate citations.
5. **File-risk tiering** (CODEOWNERS / sensitive-path patterns): classify paths+patterns into risk tiers; high-tier edits require confirmation regardless of how the edit happens (shell or Edit tool). Complements (not replaces) the alpha.18 hooks, which only see shell + secret-strings.
6. **Skill quality loop** (skill-pack maintenance): packs stagnate without periodic structural review; a dedicated audit command with measurable checks (size bounds, required sections, activation-description length, cross-listing) keeps 26 skills healthy.
7. **Uncertain-scope refusal** (auto-mode failure-mode literature): the #1 autonomous failure is confident execution of a misread goal. A cheap guard: if intent inference relied on assumption rather than user text, surface ONE question or log the assumption explicitly before proceeding.

## 3. What does not apply / rejected

| Idea | Source | Why rejected |
|---|---|---|
| Gateway/daemon control plane | OpenClaw-style | ADR-004 — no daemons |
| Mandatory hooks always-on | safety maximalism | RCE-vector review model (alpha.18) — opt-in stands |
| Vector-DB memory / RAG store | Letta-style | heavy dependency; markdown memory suffices at this scale |
| Screenshot-diff CI for every UI change | visual QA agents | needs browser runtime by default; existing optional-browser-tier model stands |
| Separate `/bq-write` AND `/bq-writing-dna` | — | one command (user: "use one command only if possible"); profile-building and writing are one workflow |
| Professional Expert Mode as a 5th operating mode | user prompt list | capability already = `deep` + anti-hallucination + doctrine; a 5th mode raises conflict-matrix complexity 25%. Proposed as composition alias in GAME_CHANGER_FEATURE_DISCOVERY instead |
| AI-detector-evasion framing for Writing DNA | — | ethically refused; goal is quality + fidelity + voice, stated explicitly in skill rules |
| 3D/animated site builder, product movie generator | game-changer candidates | stay proposals (heavy tooling decisions per-project; tracked in discovery plan) |

## 4. New ideas adopted this pass

- **Workflow:** 11-step execution contract; uncertain-scope hard gate; no-research-repeat lookup step
- **Context:** generic CONTEXT_SUMMARY (extends alpha.17's frontend-only summary); named context-pack pattern; evidence ledger
- **Prompt:** 4 prompt classes (complete/compact/neutral/strict) with skeletons in PROMPT_PATTERNS.md; delegate-pack neutrality note
- **Harness:** file-risk classification tier joining hooks (shell) + contract (agent) as third enforcement surface
- **Skills architecture:** master-skill tier (alpha.17 precedent) now documented as a named pattern; skill-quality loop command
- **Memory:** writing/ as third DNA pillar
- **Features:** Writing DNA (build now — direct user approval in this prompt); Skill Audit (build now — direct approval); everything else stays proposed in GAME_CHANGER_FEATURE_DISCOVERY.md

## 5. Risks

1. Doc proliferation — mitigated: new strategy docs are thin indexes linking alpha.18 deep docs, not duplicates
2. Writing DNA misuse for academic dishonesty — mitigated: explicit refusal rules in skill + command (no fabricated sources, no ghost-writing graded work presented as the student's own, no detector-evasion promises)
3. File-risk false positives annoying users — mitigated: classification informs CONFIRMATION, not blocking; tiers documented; user can tune FILE_RISK_RULES.md
4. 46 commands approaching cognitive load ceiling — mitigated: /bq-suggest routing + this is +2 with clear distinct jobs; clutter review discipline stands
5. Skill-audit command auto-"improving" skills could churn — mitigated: audit REPORTS by default; edits only on explicit user approval

## 6. Final recommendations (= the alpha.19 build list)

Implement now: the 6 strategy docs, 4 memory files, Writing DNA, Skill Audit, discovery tracker, auto-mode hardening, docs/installer/version updates — per audit §9. Defer (tracked in discovery plan): regression ledger, drift detector, confidence surfacing, opportunity radar, ship-readiness scorecard, Professional Expert alias decision.
