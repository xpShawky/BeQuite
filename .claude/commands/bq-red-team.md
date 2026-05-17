---
description: Adversarial review. Skeptic mode. Try to find what's actually broken across 10 attack angles (8 original + supply-chain + prompt-injection, alpha.15). Severity-tagged findings. Writes RED_TEAM-<timestamp>.md.
---

# /bq-red-team — adversarial review (10 attack angles in alpha.15)

You are the **Skeptic**. Your job is to find what's actually broken or about to break. Not be friendly. Not "approve with comments". Look for the failure modes the implementer missed.

## Step 1 — Read context

- Current diff or PR (same scope rules as `/bq-review`)
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/audits/RESEARCH_REPORT.md` (any flagged risks)
- `.bequite/state/OPEN_QUESTIONS.md` (unresolved questions)
- `.bequite/state/MISTAKE_MEMORY.md` — past mistake patterns become attack-angle inputs

## Step 2 — Apply 10 attack angles (alpha.15)

For each angle, ask "what would break this?". Be specific.

### 1. Security
- Auth bypass paths
- IDOR (user A accessing user B's data via ID guessing)
- Injection (SQL / NoSQL / command / template)
- XSS (stored + reflected + DOM)
- CSRF
- Secrets in source / logs / URLs
- Open redirects
- Missing rate limits
- CORS too permissive
- Cookies missing SameSite / Secure / HttpOnly

### 2. Architecture
- Tight coupling that will hurt later
- Hidden coupling via global state
- A change that should have been an ADR but wasn't
- A wrong abstraction (e.g. inheritance where composition was needed)
- An "if we ever need to scale" assumption that's actually broken

### 3. Testing
- Untested error paths
- Untested concurrency
- Tests that pass because they don't exercise the right thing
- Snapshot tests that lock in bad behavior
- Tests that depend on test order
- Tests that depend on real network / wall clock

### 4. Deployment
- Migrations that aren't reversible
- Env vars expected but not in `.env.example`
- Builds that pass locally but will fail in CI
- Docker images that grow uncontrollably
- Image healthchecks that lie ("healthy" when not actually healthy)

### 5. Scalability
- O(n²) loops the user won't notice at 100 users but will at 10k
- N+1 queries
- Memory leaks (event listeners, intervals, websockets not cleaned up)
- Unbounded growth (queues, caches, logs, sessions)

### 6. UX
- Empty / loading / error states that aren't real
- Hardcoded mock data that looks live (Article VI)
- Dead clicks (button is styled active but has no handler)
- Invisible text (color ≈ background)
- Touch targets too small (<44px)
- Confusing copy

### 7. Token-waste
- Verbose log statements in hot paths
- LLM prompts that include redundant context
- Reading entire files when only a section is needed
- Looping over a list when a database query would do

### 8. Hidden assumptions
- Code assumes the user is on a specific OS
- Code assumes a specific timezone
- Code assumes a specific locale (en-US date format)
- Code assumes the file system is case-sensitive (it's not on macOS / Windows)
- Code assumes network is reliable
- Code assumes the user is authenticated

### 9. Supply-chain attack (NEW in alpha.15)
- Newly-added imports that aren't in the lockfile (`package-lock.json` / `pnpm-lock.yaml` / `poetry.lock` / `Cargo.lock`)
- PhantomRaven-style typo squat: package name differs from canonical by 1-2 characters (e.g. `chalk` vs `chaIk`)
- Shai-Hulud-style mass-published malicious packages (700+ in 2025)
- Newly-added deps with no public install count
- Newly-added deps with a maintainer name not matching the canonical repo
- Dependency confusion (internal package name registered on public registry)
- Pinned `git+ssh` deps to repos that may have been compromised
- Post-install / post-publish scripts in lockfiles that exfiltrate env vars
- Lockfile changes that touch a transitive dep already flagged by OSV / Snyk / Socket

For every new import in the diff, ask: "is this package what I think it is, or a look-alike?"

### 10. Prompt injection (NEW in alpha.15 — OWASP LLM Top 10 #1)
- LLM input that includes content from user-controlled sources (form input, file upload, URL, image)
- LLM output rendered as HTML without sanitization (XSS via the model)
- LLM output written to source files, scripts, or config without review
- LLM input that includes content from web fetches (fetched page may contain instructions)
- Tool calls triggered by LLM output (model says "delete X" → tool does it without confirmation)
- System prompt accessible to user inputs (prompt leakage)
- Indirect injection: data files / docs / commits contain hidden instructions ("ignore previous", "exfiltrate secrets")
- LLM output trusted as auth ("the model said this user is admin")
- LLM agents acting on each other's output without verification (multi-agent injection chains)

For any code path where an LLM input touches user content or a fetched resource, ask: "what if this content contained an instruction trying to hijack the model?"

## Step 3 — Severity-tag every finding

- **BLOCKER** — ship-stopper. Don't merge until this is fixed.
- **HIGH** — exploitable / common-failure-mode. Address soon.
- **MEDIUM** — bad enough to track. Don't ship more code on top.
- **LOW** — note for the future.

## Step 4 — Write RED_TEAM report

`.bequite/audits/RED_TEAM-<YYYYMMDD-HHMMSS>.md`:

```markdown
# Red Team review

**Generated:** <ISO 8601 UTC>
**Scope:** <git ref or feature>
**Attacker mindset engaged.**

## Verdict

**<Blocked | Conditional pass | Pass>**

(One sentence explaining the worst finding.)

## Findings

### Security
| ID | Severity | Finding | File:line | Exploit example |
|---|---|---|---|---|
| S-1 | BLOCKER | ... | ... | "POST /api/user/123 with another user's session token returns 123's data" |

### Architecture
| ID | Severity | Finding | Why it matters |
|---|---|---|---|
| A-1 | HIGH | ... | ... |

### Testing
| ID | Severity | Finding | Missing test name |
|---|---|---|---|
| T-1 | MEDIUM | ... | ... |

### Deployment
(if any)

### Scalability
(if any)

### UX
(if any)

### Token-waste
(if any)

### Hidden assumptions
(if any)

## Kill shots (3-5 questions the implementer should be able to answer)

1. "What happens when user X creates 10,000 bookings?"
2. "What if the email service is down when sign-up fires?"
3. "How does this behave when the session expires mid-request?"
4. ...

## Action items

By priority:

1. [BLOCKER] S-1: <one-liner>
2. [HIGH] A-1: <one-liner>
3. ...
```

## Step 5 — Update state + log

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Step 6 — Report back

```
Skeptic verdict: <Blocked | Conditional pass | Pass>

Findings:
  Security:           <count>
  Architecture:       <count>
  Testing:            <count>
  Deployment:         <count>
  Scalability:        <count>
  UX:                 <count>
  Token-waste:        <count>
  Hidden assumptions: <count>

Kill-shot questions: <count>

Report: .bequite/audits/RED_TEAM-<timestamp>.md

Next: /bq-fix <highest-severity-finding>
```

## Rules

- **No "looks fine."** If everything passed, the red team failed. Look harder.
- **Cite an exploit example for every Security finding.** "Could be XSS" is not useful; "GET /search?q=<script>alert(1)</script> renders the script in the title" is.
- **Severity is honest.** Don't downgrade something to MEDIUM because the codebase already has lots of HIGH findings.
- **Kill-shot questions must be specific.** "Have you thought about scale?" is not specific. "What happens when sign-up fires 100 times in 1 second from the same IP?" is.

## Standardized command fields (alpha.6)

**Phase:** P3 — Quality and Review
**When NOT to use:** code is mid-flight (red-team is for completed work); regulated-context paranoia not warranted (use `/bq-review`).
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED` (`REVIEW_DONE` recommended — red-team is adversarial follow-up to a normal review)
**Quality gate:**
- `RED_TEAM-<timestamp>.md` written
- All 9 attack angles addressed (security / architecture / testing / deployment / scalability / UX / token-waste / hidden assumptions / tool-choice)
- Each finding severity-tagged + kill-shot question + (for security) exploit example
- Mistake-memory entries for BLOCKER + HIGH findings
- Marks `RED_TEAM_DONE ⚪ optional ✅`
**Failure behavior:**
- "Nothing found" verdict → look harder; red-team's job is to find. If truly clean, document why.
- Conflicts with prior reviewer verdict (review = Approved, red-team = Blocked) → red-team wins; loop back to `/bq-fix`
**Memory updates:** Sets `RED_TEAM_DONE ⚪ optional ✅`. Appends BLOCKER+HIGH entries to `MISTAKE_MEMORY.md` with attack-angle tags.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- The current diff
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/state/OPEN_QUESTIONS.md`

## Memory files this command writes

- `.bequite/audits/RED_TEAM-<timestamp>.md` (new)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- `/bq-fix` (highest-severity finding first)
- `/bq-review` (if red-team passed, formalize a normal review)
- `/bq-verify` (if conditional-pass and you accept the medium/low findings as deferred)

---

## Mistake memory update

Red-team findings are **high-signal**. Every BLOCKER and most HIGH findings should produce a MISTAKE_MEMORY entry:

- Treat the kill-shot question as a **prevention rule** worth grep-ing for forever
- Tag with the attack-angle category (`[sec]`, `[arch]`, `[testing]`, `[deploy]`, `[scale]`, `[ux]`, `[token]`, `[assume]`, `[tool]`)
- Include the **exploit example** verbatim (for `[sec]` entries) so future code reviews can search for the pattern
- Cite related files for follow-up audits

Medium / Low findings: skip MISTAKE_MEMORY unless they're a **pattern** (multiple instances of the same root cause across the codebase).

See `.bequite/state/MISTAKE_MEMORY.md` template.

---

## Tool neutrality (global rule)

⚠ **Red Team probes the cost of tool choices that lack justification.**

Add a 9th attack angle to the 8 listed:

### 9. Tool choice

- Was the tool added by default rather than chosen for this project?
- Does the project really need it, or is it cargo-culted?
- Is the tool overkill for the project's actual scale?
- Has the project locked into a vendor whose pricing / availability / license is risky?
- Could a simpler / native alternative achieve the same outcome?
- Is the dependency tree growing for no clear reason?

**Kill-shot questions to add:**
- "Why this tool over [named alternative]? Show me the decision section."
- "At what scale does this tool become unnecessary?"
- "What's the rollback path if this tool is sunsetted next year?"
- "Could the existing stack handle this without the new dep?"

**Tool-choice findings are real BLOCKERS** if a critical dep was added without justification.

The 10 decision questions every named tool in the diff must answer:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
