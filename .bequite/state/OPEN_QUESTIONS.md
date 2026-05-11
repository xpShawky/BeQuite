# Open questions

Tracked questions awaiting answers. Set status to **resolved** when answered.

## For BeQuite itself

### Q1. Should studio/ + Docker assets be deleted now or kept paused on disk?

**Status:** unresolved — awaiting user direction
**Context:** Direction reset moved BeQuite to a lightweight skill pack. Heavy assets (studio/, docker-compose.yml, tests/e2e/) are currently PAUSED (kept on disk). User can decide whether to delete now or keep deferred.
**Recommended default:** keep deferred for v3.0.0-alpha.1; revisit in v3.1 once skill pack adoption is real.

### Q2. Should v3.0.0-alpha.1 be tagged + pushed immediately, or wait for live verification inside a Claude Code session?

**Status:** unresolved — awaiting user direction
**Context:** All files authored; CLI command files have YAML frontmatter; skills follow Anthropic Skills SKILL.md format. But the actual `/bequite` slash command behavior hasn't been observed in a live Claude Code instance yet.
**Recommended default:** push to main (no tag yet) → user tests `/bequite` in a fresh Claude Code session → if good, tag.

### Q3. Should the Python CLI v1.0.4 stay as an optional install path, or be retired in favor of slash commands only?

**Status:** unresolved
**Context:** v1.0.4 CLI works (`bequite doctor` + `bequite dev` + `bequite status` + 19 other commands). But it duplicates functionality with the slash commands. Maintaining both is overhead.
**Recommended default:** keep both for now. Slash commands are the MVP entry point; CLI is for power users / scripting / CI.

---

## For installed projects

When users install BeQuite into THEIR project, this file starts empty:

```markdown
# Open questions

(none yet — run /bq-clarify when ready to surface high-value questions)
```
