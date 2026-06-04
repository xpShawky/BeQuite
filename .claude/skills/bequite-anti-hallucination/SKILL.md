---
name: bequite-anti-hallucination
description: Use when verifying work, reviewing/auditing, recommending a package, or making any factual claim — forces evidence over assertion and an explicit UNVERIFIED label over confident guessing.
allowed-tools: Read, Glob, Grep, Bash, WebFetch, WebSearch
---

# bequite-anti-hallucination

Turn assertion into evidence. Every claim BeQuite makes either ships with proof or ships with an explicit `UNVERIFIED:` label. No confident guessing.

## The 6 rules (top = most load-bearing)

| # | Rule | One-line enforcement |
|---|---|---|
| 1 | Evidence over claims | Paste the command + exit code + output. Never a bare "done" / "it works". |
| 2 | Citation-or-strike | Every finding carries a `file:line` quote of the real code, or you RETRACT it. |
| 3 | Forced fork | Each uncertain claim → concrete evidence OR an explicit `UNVERIFIED:` / "I don't know". |
| 4 | Package verification | Verify a package is real IN-SESSION before importing/installing it. |
| 5 | Version-pinned API grounding | Pin the version; ground every non-trivial call on docs fetched this session. |
| 6 | Fresh-context verifier | A blind sub-agent refutes the diff; severity-gated; escalate only LOW-confidence claims. |

Plus: confidence calibration (rule 7) before risky actions.

---

### Rule 1 — Evidence over claims (Anthropic reduce-hallucinations; Claude Code best-practices)

> "Show evidence rather than asserting success — the test output, the command run and what it returned, or a screenshot."

The **trust-then-verify gap**: an agent reports success, the human trusts it, nobody re-runs the check. Close it at the source.

- A completion report is INVALID without: the exact command run, its exit code, and its output (or a screenshot for UI).
- "Done" / "it works" / "tests pass" with no pasted proof = retract and re-run.
- Format every completion line as: `$ <command>` → `exit <N>` → `<relevant output>`.

Strengthens: **/bq-verify**, **/bq-implement**, **/bq-fix**, **/bq-test**.

### Rule 2 — Citation-or-strike (Anthropic citation-verification)

Every review / audit / red-team finding MUST carry a `path:line` quote of the ACTUAL code it describes. If you cannot find the supporting quote in the file right now, the claim is unsupported — **RETRACT it**, do not soften it.

```
FINDING (HIGH): unbounded loop on user input
  src/api/handler.ts:142  → `while (req.body.items.length) {`
```

No quote → no finding. This kills "the code probably does X" review noise.

Strengthens: **/bq-review**, **/bq-audit**, **/bq-red-team**.

### Rule 3 — Forced fork (Anthropic reduce-hallucinations)

Anthropic's #1 anti-hallucination move: **give the model permission to say "I don't know."** Banning hedge words (should / probably / seems to) WITHOUT an escape valve just manufactures false confidence. So the rule is a fork, not a ban:

On any uncertain claim, do EXACTLY ONE:
- **A — Evidence:** produce the concrete proof (command output, file:line quote, fetched doc), OR
- **B — Label:** emit `UNVERIFIED: <claim>` or "I don't know — <the gap>".

`UNVERIFIED:` is a first-class, acceptable output. A labeled unknown beats a confident wrong answer every time.

Strengthens: every command. Most visible in **/bq-research**, **/bq-plan**, **/bq-verify**.

### Rule 4 — Package / dependency verification (Anthropic PhantomRaven defense; USENIX slopsquatting research)

5–22% of LLM package suggestions are hallucinated; ~58% of those fakes recur across runs (slopsquatting / PhantomRaven). Before importing or installing ANY package, verify IN THIS SESSION:

- [ ] Exists on the real registry (npm / PyPI / crates.io — fetch it)
- [ ] Package age (brand-new + critical = suspect)
- [ ] Weekly downloads — **< 1,000 on a critical dep = red flag**
- [ ] Publisher identity matches the expected maintainer
- [ ] Repo link resolves and matches the package
- [ ] Already present in the lockfile

Install from **pinned lockfiles**, not model-suggested names. Iron Law 8 (PhantomRaven defense) is enforced here.

Strengthens: **/bq-research**, **/bq-plan**, **/bq-feature**, **/bq-implement**.

### Rule 5 — Version-pinned API grounding (Anthropic reduce-hallucinations)

For any non-trivial library/API call: pin the version, then ground the call on **version-matched docs fetched this session**. Never quote a method signature from memory.

Caveat (do not over-retrieve): retrieve docs only when the API is unfamiliar or version-sensitive. **A bad retriever HURTS familiar APIs** — pulling stale or mismatched docs for a well-known call adds error, not safety.

Strengthens: **/bq-implement**, **/bq-feature**, **/bq-fix**.

### Rule 6 — Fresh-context adversarial verifier (Anthropic effective-harnesses; information asymmetry)

A verifier sub-agent sees ONLY the diff + the acceptance criteria — NOT the implementer's reasoning — and tries to refute the work. Information asymmetry stops the verifier from rubber-stamping the implementer's own story.

Two guardrails so the verifier stays useful and cheap:
- **Severity-gate:** "tell the reviewer to flag only gaps that affect correctness or the stated requirements." A reviewer told to "find gaps" will manufacture them. (Anthropic effective-harnesses.)
- **Cost-aware escalation:** escalate to a second model / sub-agent ONLY on LOW-confidence claims. High-confidence, evidence-backed claims do not need a second pass.

Strengthens: **/bq-review**, **/bq-red-team**, **/bq-verify**, **/bq-auto** (verifier step).

### Rule 7 — Confidence calibration (Anthropic demystifying-evals)

Agents are systematically overconfident — measured success ~22% against self-predicted ~77%. Before any risky action, surface:

- **Confidence:** high / medium / low (with the reason)
- **The single biggest unknown** that could make this wrong

Low confidence is the trigger for Rule 3-B (label it) and Rule 6 (escalate).

Strengthens: **/bq-plan**, **/bq-fix**, **/bq-auto**, **/bq-release**.

---

## When this skill activates

- Any completion / verification report (Rules 1, 3, 7)
- Any review, audit, or red-team finding (Rules 2, 6)
- Recommending, importing, or installing a package (Rule 4)
- Writing a non-trivial library/API call (Rule 5)
- Before a hard-human-gate action or any one-way door (Rule 7)

## Effort-awareness

- **Fast / token-saver mode:** Rules 1–4 are mandatory (cheap, high-value). Rule 6 escalation fires only on declared LOW-confidence claims.
- **Deep mode:** all 7 rules; fresh-context verifier runs on every diff that touches correctness-critical paths.
- Match verification depth to risk — a one-line doc fix does not need a second model; an auth change does.

## Tool-neutrality note

Registry names (npm / PyPI / crates.io) and fetch tools here are EXAMPLES, not commands. Use the verification source that fits the project's actual ecosystem. This skill installs nothing and adds no dependency — it only inspects and verifies (per ADR-003 + do-not-auto-install).

## When NOT to use this skill

- Pure brainstorming / ideation where nothing is being claimed as factual or shipped.
- Quoting the user's own input back to them (no external claim to verify).
- Casual orientation reads (`/bq-now`, `/bequite` menu) — read-only, no factual assertions to ground.
- When evidence is already inline and current (do not re-fetch familiar, version-matched docs — Rule 5 caveat).

## Quality gate

This skill's output is acceptable only when:

- [ ] Every success claim carries command + exit code + output (or screenshot). (Rule 1)
- [ ] Every review/audit/red-team finding carries a real `file:line` quote, or is retracted. (Rule 2)
- [ ] Every uncertain claim is either evidence-backed OR labeled `UNVERIFIED:` / "I don't know". (Rule 3)
- [ ] No package is imported/installed without in-session registry + downloads + publisher + lockfile checks. (Rule 4)
- [ ] Every non-trivial API call is version-pinned and grounded on docs fetched this session. (Rule 5)
- [ ] Low-confidence claims were escalated to a fresh-context, severity-gated verifier. (Rules 6, 7)
- [ ] No banned weasel word stands alone — each is replaced by evidence or an explicit `UNVERIFIED:` label.
