---
name: bequite-skill-auditor
description: Use for /bq-skill-audit and /bq-eval, after adding or merging skills, before a release, or when a skill fires for the wrong request or fails to fire. Reviews every skill against the v1 rubric (trigger description, short body, references one level deep, dated sources that say what the skill claims, a worked example, a quality gate), finds overlaps and stale facts, and reports with quoted evidence; edits only after approval.
last_verified: 2026-11-22
sources:
  - https://code.claude.com/docs/en/skills  # SKILL.md fields; the description decides when a skill loads; keep SKILL.md short, details in supporting files
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices  # third-person description (what + when), body under 500 lines, references one level deep
  - https://agentskills.io/specification  # name 1-64 chars matching the folder, description 1-1024 chars
  - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills  # progressive disclosure: metadata, body, extra files
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  # the smallest set of high-signal tokens
  - https://github.com/anthropics/skills  # example skills to compare structure against
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-skill-auditor

A skill pack decays in known ways: descriptions stop matching how people ask, two skills claim the same job, facts and counts go stale, and a source is cited for something it never said. `scripts/bq_check.py` catches the mechanical part; this skill is the judgement the script cannot make.

## When to use

- `/bq-skill-audit` (the whole pack) and `/bq-eval` (scenarios per skill).
- After a skill is added, merged, split or forged; before a release.
- A skill loaded for the wrong request, or did not load for the right one.

Not for: the project's own code (`/bq-audit`); a single edit the user already specified (just make it); command files (the self-check covers their contract, references and size).

## The v1 rubric

| Part | A healthy skill | How to check |
|---|---|---|
| `name` | lowercase with hyphens, at most 64 characters, same as the folder | read the frontmatter |
| `description` | third person; says what it does **and when to use it**, in the words a user would type; at most 1,024 characters | read it as a router would: could two skills both claim this request? |
| Body | at most 150 lines (BeQuite's budget; the harness guidance is under 500); a numbered procedure, not an essay | `bq_check.py` size check |
| Depth | detail lives in `references/` or `scripts/`, one level below `SKILL.md`, loaded on demand | Glob the folder; every file is cited from `SKILL.md` |
| Sources | `last_verified` within 120 days and at least five `sources`, each with what it was read for | open two sources per skill and confirm they say it |
| Worked example | one real run with real values and a date | not "e.g. some project" |
| Quality gate and boundaries | checkable statements; what the skill never does | each gate line can fail |
| Reach | at least one command or the orchestrator's routing table names it; it is in `SKILL_REGISTRY.md` and, outside core, in `PACKS.txt` | Grep |

## Procedure

1. **Enumerate** with Glob (`.claude/skills/bequite-*/SKILL.md`), never from memory. Run `python3 scripts/bq_check.py` first and take its warnings as given.
2. **Read every frontmatter** in one pass and lay the descriptions side by side. Mark pairs that would both answer the same request: that is an overlap finding, with the two quoted sentences.
3. **Per skill**, walk the rubric. For sources, open two (the web-fetch route, or the browser when a site refuses scripts) and compare with the claim they are cited for. A source that did not load is not evidence: say "not read", and remove it or mark the claim `UNVERIFIED:`.
4. **Stale facts:** versions, prices, platform limits and counts older than the skill's `last_verified`, files and commands the skill names that no longer exist.
5. **Rate** each finding: HIGH (broken frontmatter, a skill nothing reaches, direct duplication, a source that contradicts the claim), MEDIUM (a missing rubric part, a stale fact, a description that does not say when), LOW (thin example, minor repetition).
6. **Verdict per skill:** keep, improve, merge, split, or archive, with one line of reason. A merge must not erase a distinct trigger.
7. **Report** to `.bequite/audits/SKILL_QUALITY_AUDIT.md`: the table of verdicts, findings with `skill:line` and the quoted text, and the trend against the previous audit. Report only: edits wait for the user's approval, then update the registry, the router, the packs file and the counts in the same change.

## Worked example (2026-11-22, the v1 review of this pack)

- `bq_check.py --strict` listed six skills with no `last_verified` and no sources (the four film skills, this one, the updater). This skill's own profile still allowed "60-400 lines" while the pack budget was 150: a stale fact inside the auditor.
- 39 candidate source pages were fetched for those six skills; 32 loaded and said what they were needed for, 7 refused automated reading or returned only a title (two Adobe help pages, a BBC guide, an ElevenLabs help article, two design-guideline pages, an Instagram help page). The seven were not cited.
- One reading changed a design: GitHub's "latest release" excludes prereleases and drafts, which is exactly what the update script needs, so a release candidate tag never reaches users by itself.
- Verdicts: improve (sources added) for the four film skills; rewrite for the auditor and the updater.

## Quality gate

- Every skill was enumerated from the file system and has a verdict.
- Every finding quotes its evidence; a finding without a quote is dropped.
- At least two sources per skill were opened in this session, and the report says which.
- Nothing was edited before approval; after approved edits the self-check passes.

## Boundaries

It does not rewrite prose for style, does not install third-party skills, and does not judge a creative skill's taste: that is the owner's verdict.
