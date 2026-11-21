---
description: The content studio. One piece from what is moving to a packaged draft that waits for your yes. Modes - radar / study / script / produce / package / queue / from-work, plus brand-kit, community and course. Every mode starts from measured human references and ends with evidence; nothing is posted without approval per post.
---

# /bq-content: from radar to a packaged draft

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` (hourly; it updates BeQuite when a newer version is published, backs up first, never touches `.bequite/` memory, never blocks) and say its one line.
> 2. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 3. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 4. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 5. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 6. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 7. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 8. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

## Syntax

```
/bq-content radar "<niche>" [--country EG]        what is moving this week, with links and numbers
/bq-content study "<niche>"                        the format sheet of the niche's top five (same as /bq-dna)
/bq-content script "<topic>" [--voice <name>]      hook + beats + captions in the measured format and voice
/bq-content produce                                hand the script to the production route (motion, screen, face cam)
/bq-content package                                per-platform files and texts, checked against the platform limits
/bq-content queue                                  APPROVAL.md per post; posts only on your yes
/bq-content from-work <work-id>                    turn a closed work's evidence into posts (receipts, not opinions)
/bq-content brand-kit "<niche + audience + what the brand does>"   brand identity: name directions, brand DNA, visuals, voice
/bq-content community "<who it is for + purpose>"                  platform, onboarding, calendar, engagement loops, moderation
/bq-content course "<idea>" | course validate|curriculum|launch "<idea>"   a course from validation to launch
```

## Modes and the skills they run

| Mode | Skill | Output in `work/<id>/` | Gate |
|---|---|---|---|
| radar | `bequite-trend-radar` | `research/radar/brief-*.md` | - |
| study | `bequite-format-dna` (+ `bequite-video-intel`) | `research/format/format-sheet-*.md` | `REFERENCES_STUDIED` (owner approves the five) |
| script | `bequite-hooks-and-copy`, `bequite-writing-dna` | `script.md`, `captions.srt`, `hooks.md`, blind-pick record | needs `REFERENCES_STUDIED` |
| produce | `bequite-motion-director` / `bequite-render-pipeline` | the video, a contact sheet | `HUMAN_TEST_PASSED` before package |
| package | `bequite-publish-prep` | `package/<piece>/` + `package_check.py` output | - |
| queue | `bequite-publish-prep` | `APPROVAL.md` PENDING | the owner's yes, per post |
| from-work | `bequite-writing-dna` + this command's from-work steps | `drafts/from-work-*.md` | `HUMAN_TEST_PASSED` |
| brand-kit | `bequite-human-taste`, `bequite-ux-ui-designer`, `bequite-writing-dna`; spec `.claude/bequite/docs/specs/BRAND_KIT_ENGINE.md` | `.bequite/brand/` | `REFERENCES_STUDIED` (every visual choice says why it fits the niche) |
| community | `bequite-product-strategist`, `bequite-writing-dna`; spec `.claude/bequite/docs/specs/COMMUNITY_PACK.md` | `.bequite/community/` | - |
| course | `bequite-product-strategist`, `bequite-presentation-builder`, `bequite-writing-dna`; spec `.claude/bequite/docs/specs/COURSE_ENGINE.md` | `.bequite/courses/` | validation before curriculum (one painful specific problem) |

## Steps (any mode)

1. Name the mode and the piece; read the work's gates.
2. Run the mode's skill procedure; refuse a later mode whose gate is open (name the gate).
3. Every number and claim carries its source; every creative output carries its human-test record.
4. Stop at `APPROVAL.md`. The owner's "yes" names the post and the platform.

## from-work

Read the closed work's `evidence.md` and `log.md`; list moments worth a post (a failure and its fix, a before/after, a number); for each, a draft in the owner's voice that quotes the real command, number or output; the human test; then package. Never invent a result; every number appears verbatim in the evidence.

## Never

Post, schedule, like, follow or message without a yes per action. Automate a platform's app or website. Put credentials in files the agent writes.

## Next Command Recommendations

- After radar: `/bq-content study`. After study: `/bq-content script`. After package: read `APPROVAL.md` and answer yes or no per post.
