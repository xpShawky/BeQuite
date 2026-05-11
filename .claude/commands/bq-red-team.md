---
description: Adversarial review. Skeptic mode. Try to find what's actually broken across 8 attack angles. Severity-tagged findings. Writes RED_TEAM-<timestamp>.md.
---

# /bq-red-team — adversarial review

You are the **Skeptic**. Your job is to find what's actually broken or about to break. Not be friendly. Not "approve with comments". Look for the failure modes the implementer missed.

## Step 1 — Read context

- Current diff or PR (same scope rules as `/bq-review`)
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/audits/RESEARCH_REPORT.md` (any flagged risks)
- `.bequite/state/OPEN_QUESTIONS.md` (unresolved questions)

## Step 2 — Apply 8 attack angles

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
