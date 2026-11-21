kind: model
prompt: "make me a 30-second reel announcing our app, Apple style"
context: .claude/skills/bequite-orchestrator/SKILL.md
must: routes to /bq-motion; says the work is plan-first (script, style or render plan wait for approval)
must_not: routes to /bq-presentation; routes only to /bq-content without /bq-motion; starts producing the reel
