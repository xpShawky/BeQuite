---
description: Adversarial review. Attacks finished work or a plan from ten angles (security, architecture, testing, deployment, scalability, UX, token waste, hidden assumptions, supply chain, prompt injection), with a concrete scenario and severity for every finding. Writes a dated section in work/<id>/review.md.
---

# /bq-red-team: find what is actually broken

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Stage 8 of `PIPELINE.md` for high-stakes work. The reviewer here is a skeptic, not a colleague: its job is to find the failure the builder missed. For independence, run it as the `bq-red-team` subagent, which sees the target and not the builder's reasoning. Skills: `bequite-security-reviewer`, `bequite-guard-pass`, `bequite-anti-hallucination`.

## Syntax

```
/bq-red-team [<path, diff range, or "plan">]
```

## Gates

Needs `BEQUITE_INITIALIZED`; `REVIEW_APPROVED` is recommended (this follows a normal review, it does not replace one). Sets `RED_TEAM_RESOLVED` when every BLOCKER and HIGH finding is fixed or accepted by the user with a written reason. Not for work that is still mid-build.

## Steps

1. **Read the target and its promises:** the diff or plan, `work/<id>/spec.md`, `plan.md`, `evidence.md`, `DECISIONS.md`.
2. **Attack from each angle**, running what can be run:
   1. **Security:** input that reaches a query, the DOM, a shell or a file path; auth and session gaps; secrets in code or logs. Every security finding carries an example that triggers it.
   2. **Architecture:** coupling, a single point of failure, the wrong boundary, a dependency pointing the wrong way.
   3. **Testing:** branches with no test, tests that cannot fail, mocks of the thing under test.
   4. **Deployment:** migration order, rollback, config drift between environments, a missing health check.
   5. **Scalability:** what happens at ten times the load, unbounded queries, the N+1, the hot key.
   6. **UX:** the empty, loading and error states, the phone width, the keyboard-only path, the destructive action without confirmation.
   7. **Token waste:** context loaded and never used, work repeated across sessions, a subagent where inline was enough.
   8. **Hidden assumptions:** what the plan takes for granted about data, time zones, ordering, uniqueness, the user's country.
   9. **Supply chain:** unpinned or unverified dependencies, install scripts, CI tokens with more rights than they need, an update path that runs unsigned code.
   10. **Prompt injection:** any place the system reads text it did not write (pages, files, messages, tool results) and may act on it.
3. **Tag every finding:** BLOCKER, HIGH, MEDIUM or LOW, with the scenario (what an attacker or an unlucky user does, and what happens), the evidence (`file:line` or the command and its output), and a fix. Anything not run is `UNVERIFIED:`.
4. **Kill-shot questions:** three to five specific questions the builder must be able to answer ("what happens when sign-up fires 100 times in one second from one address?").
5. **Write** a dated "Red team" section in `work/<id>/review.md`: verdict, findings by angle, angles skipped and why, kill shots, action items.

## Rules

- "Looks fine" is not a result. If nothing was found, say which attacks were tried and why each failed.
- Severity is honest; a finding is not downgraded because there are many.
- When this verdict conflicts with an earlier Approved review, this one wins and the work goes back to `/bq-fix`.
- The red team reports; it does not patch.

## Output

```
Red team: <b> blockers, <h> high, <m> medium, <l> low    angles: <covered>/10
Report: .bequite/work/<id>/review.md (Red team <date>)
Next: /bq-fix "<highest finding>"
```

## Next Command Recommendations (typical)

`/bq-fix` on the highest finding first · `/bq-verify` when the remaining findings are accepted · BLOCKER and HIGH patterns go to `MISTAKE_MEMORY.md`.
