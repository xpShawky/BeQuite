---
name: bequite-context-engineer
description: Use when a task spans many steps, files or sessions, when the context is getting long, before /compact, after a resume, or when deciding whether reading belongs in a subagent. Keeps the live context small and the important state in files, so nothing decided is lost to compaction or a new session.
last_verified: 2026-11-21
sources:
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://code.claude.com/docs/en/memory
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/skills
  - https://www.trychroma.com/research/context-rot
  - https://arxiv.org/abs/2307.03172
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://code.claude.com/docs/en/costs
---

# bequite-context-engineer

Context is finite and degrades as it grows: an 18-model study found accuracy falls with input length even on simple tasks, and facts in the middle of a long context are recalled worst. So keep the window small, put state in files, and re-read a fact from its file before acting on it.

## When to use

- Multi-step or multi-session work (`/bq-plan`, `/bq-implement`, `/bq-auto`, `/bq-recover`).
- Before a manual `/compact`, after a resume or a compaction, or when the window passes about half full.
- When about to read more than five sources or a large tree (decide: inline or subagent).

Not for: a one-turn, one-file change.

## What loads by itself (do not repeat it by hand)

| Mechanism | What it gives | Limit (Claude Code docs, 2026-11) |
|---|---|---|
| Root `CLAUDE.md` | Always loaded; re-read after /compact | Aim under 200 lines |
| `.claude/rules/*.md` with `paths:` | Loads only when matching files are touched | Reloads on demand after compaction |
| Auto memory `MEMORY.md` | Loaded at start | First 200 lines or 25 KB |
| SessionStart hook (BeQuite, A2) | Active work, open gates, last run, top lessons | 10,000 characters (more is saved to a file with a 2,000-character preview) |
| Skills | Description always; body on invocation | Description + when_to_use cut at 1,536 characters; after compaction each skill keeps its first 5,000 tokens, 25,000 total |

So: must-not-forget rules go in root `CLAUDE.md` or the hook, never only in a skill body or a nested rule; the most important lines go at the top of every file.

## Procedure

1. **Orient from files, not memory.** Read what the SessionStart block points to: `work/<id>/` (spec, plan, tasks, gates, log), `.bequite/state/PROJECT_DNA.md`, `git log -5`. If the hook is not enabled, read `.bequite/ACTIVE.md`, `LAST_RUN.md` and `WORKFLOW_GATES.md` yourself.
2. **One task at a time.** Pick the single highest-priority open item; run a smoke check of the current state before changing it.
3. **Externalise at each boundary.** After each step append to `work/<id>/log.md` (or `.bequite/state/WORKING_NOTES.md`):
   ```
   ## <task id> <time>
   - tried / learned / pending / re-read next
   ```
   Machine state (gates, task status, counters) lives in JSON or a strict table, which the model is less likely to rewrite by accident.
4. **Keep the window lean.** Prefer paths and queries over pasted content; drop stale tool output before compacting; give `/compact` focus instructions (decisions, open bugs, files touched, commands, open questions).
5. **Isolate wide reading.** More than five sources, or a sweep of many files: a subagent reads in its own window and returns 1,000 to 2,000 tokens of findings with paths and URLs. Tightly coupled implementation stays in one context.
6. **Match the house style.** Before new code, read `PROJECT_DNA.md` (conventions, layering, error and test patterns). If it is a placeholder, fill it from the existing code first. UI work also reads `DESIGN_DNA.md`.

## Worked example (measured here, 2026-11-21)

This repo's `CLAUDE.md` is 68 lines and the owner's `MEMORY.md` 10 lines: both well inside their load limits, so nothing must move. One track of work 0002 had a dozen skills to research; the agent sent ten reader subagents to about 60 pages and kept only their findings (one section per URL) in the main context, then wrote each finding to the work folder's `research/<skill>.md` before writing the skill. After any compaction the notes, not the chat, are the source.

## Quality gate

- State that must survive is in files (work folder, `PROJECT_DNA.md`, root `CLAUDE.md`), not only in chat.
- No decision acted on from the middle of the conversation without re-reading its file.
- Subagents returned distilled findings, not transcripts.
- The log has one entry per step taken.

## Boundaries

These are harness mechanisms, not dependencies; nothing is installed. Do not re-read the whole `.bequite/` tree each step: that is the opposite failure.
