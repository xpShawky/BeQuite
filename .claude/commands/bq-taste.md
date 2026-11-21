---
description: Learn from the user's corrections. Turns the entries in .bequite/state/TASTE_INBOX.md (written by the UserPromptSubmit hook when a prompt says "no", "not like that", "لا", "مش كده", or added by hand) into proposed rules for the Design, Writing or Motion DNA, each with the example that caused it, shows them to the user, and saves only the approved ones. Modes - review, add, list.
---

# /bq-taste: every "no, like this" becomes a rule

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks).
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

The agent stops repeating the same mistake of taste. Corrections land in `.bequite/state/TASTE_INBOX.md` (the plugin's UserPromptSubmit hook appends them; `/bq-taste add` does it by hand). This command proposes rules; the user decides. Skill: `bequite-human-taste` (with writing-dna, frontend-design-system and motion-director for where each rule lives).

## Syntax

```
/bq-taste                      same as review
/bq-taste review               propose rules from the unprocessed inbox entries
/bq-taste add "<correction>" [about=<what it corrected>]
/bq-taste list                 the rules already saved, by DNA file
```

## Steps (review)

1. Read the unprocessed entries in `TASTE_INBOX.md` and, for each, the work and output it corrected (the work log around its time).
2. Group entries that say the same thing. One group = one proposed rule.
3. Write each rule so it can be checked: what to do, with a number where there is one ("camera zoom at most 15% closer than the whole block", not "less zoom"), the medium (design, writing, motion), the example that caused it (date, work, the user's words in their language), and the DNA file it belongs in: `.bequite/design/DESIGN_DNA.md`, `.bequite/writing/WRITING_DNA.md`, or the work's Motion DNA in `spec.md` (project-wide motion rules: `.bequite/design/MOTION_DNA.md`).
4. Show the proposals as a numbered list and wait. Save only what the user approves (all, some numbers, or edited text); write "declined" next to the rest.
5. Mark the inbox entries processed with the rule they became (or "declined", or "one-off").
6. A rule that contradicts an existing rule is shown next to it; the user picks.

## Quality gate

No rule is saved without the user's yes; every saved rule quotes its example and date; a rule is specific enough that a reviewer could fail a piece of work against it.

## Next Command Recommendations (typical)

Re-run the work's review (`/bq-review`, or the motion or content QA) against the new rules.
