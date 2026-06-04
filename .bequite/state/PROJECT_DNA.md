# Project DNA

> **Status:** `template` → set to `locked` once filled.
> **Last updated:** `<YYYY-MM-DD>`
> **Read before any implementation; new code must match this or update it first.**

**Freshness:** `commit <hash>` · `<YYYY-MM-DD HH:MM TZ>` · **Refresh rule:** re-derive on any stack/architecture change, on a new exemplar, or every 20 commits — whichever comes first. Stale DNA is treated as unverified (effective-context-engineering: load current ground truth, not memory).

This file is the codebase's "how we do things here" contract — the workflow-agnostic generalization of frontend Design DNA. One screen, high signal. If reality and this file disagree, **fix the code or update this file first — never let them silently drift** (reduce-hallucinations: prefer recorded ground truth over guessing).

---

## 1 · Stack + versions (pinned)

> One row per runtime/tool. Pin exact versions — verify each exists in its registry this session (PhantomRaven defense).

| Layer | Tool | Pinned version | Source of truth |
|---|---|---|---|
| Language/runtime | `<e.g. Node>` | `<x.y.z>` | `<.nvmrc / .python-version>` |
| Package manager | `<e.g. pnpm>` | `<x.y.z>` | `<packageManager field>` |
| Framework | `<…>` | `<…>` | `<lockfile>` |
| Key libs | `<…>` | `<…>` | `<lockfile>` |

## 2 · Architecture + layers + dependency direction

> Name the layers top-to-bottom and state which way imports flow. Arrow = "may import".

| Layer | May import → | May NOT import |
|---|---|---|
| `<UI/entry>` | `<app/service>` | `<infra directly>` |
| `<app/service>` | `<domain, ports>` | `<UI>` |
| `<domain/core>` | `<nothing external>` | `<framework, infra>` |
| `<infra/adapters>` | `<ports>` | `<UI, app internals>` |

Dependency rule (1 line): `<e.g. dependencies point inward; domain has zero framework imports>`

## 3 · Directory / responsibility map

> One responsibility per area. If a directory does two unrelated jobs, split it.

| Path | Holds | Single responsibility |
|---|---|---|
| `<src/…>` | `<…>` | `<one sentence>` |
| `<src/…>` | `<…>` | `<one sentence>` |

## 4 · Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Files | `<kebab / PascalCase>` | `<…>` |
| Types/classes | `<PascalCase>` | `<…>` |
| Functions/vars | `<camelCase / snake_case>` | `<…>` |
| Constants | `<UPPER_SNAKE>` | `<…>` |
| Tests | `<*.test.* / test_*.py>` | `<…>` |

## 5 · Error-handling pattern

> The ONE pattern. New code uses it; no second style.

- Throw vs return: `<e.g. throw typed errors at boundaries; Result type in domain>`
- Error type/shape: `<…>`
- Boundary handling: `<where caught, how surfaced>`
- Never: `<e.g. swallow errors; catch + console.log + continue>`

## 6 · API / contract conventions *(if applicable — else "N/A")*

- Style: `<REST / RPC / GraphQL>` · Versioning: `<…>`
- Request/response shape: `<envelope, casing>`
- Error responses: `<status codes + body shape>`
- Validation: `<where + tool>`

## 7 · Data / DB conventions *(if applicable — else "N/A")*

- Engine + access: `<DB + ORM/query layer>`
- Migrations: `<forward-only? tool? location>`
- Naming: `<table/column casing>`
- Rules: `<soft vs hard delete; no raw SQL in domain>`

## 8 · Test conventions

| Aspect | Rule |
|---|---|
| Framework | `<vitest / pytest / …>` |
| Location | `<co-located / tests dir>` |
| "Done" = | `<unit covers logic + 1 integration path; suite green>` |
| Hard rule | **Never edit a test to make it pass; fix the code or the contract** (demystifying-evals). |

## 9 · Build / run / verify commands (the proof commands)

> Exact, copy-pasteable. These are what `/bq-verify` runs to prove "done" (Claude Code best-practices: scripted, repeatable proof).

| Action | Command |
|---|---|
| Install | `<…>` |
| Lint | `<…>` |
| Typecheck | `<…>` |
| Test | `<…>` |
| Build | `<…>` |
| Run/smoke | `<…>` |

## 10 · Security conventions

- Secrets: `<.env, never committed; loaded via …>` · Scanner: `<…>`
- Auth pattern: `<where enforced, token/session model>`
- Input trust boundary: `<validate at …>`
- Never: `<hardcode keys; log secrets; disable TLS verify>`

## 11 · Logging / observability conventions

- Logger + format: `<structured JSON / …>` · Levels: `<…>`
- What to log / never log: `<no PII, no secrets>`
- Correlation: `<request id / trace propagation>`

## 12 · Exemplar files

> "When adding X, follow this file as the pattern." Point at the best real file, not an ideal.

| When adding… | Follow this exemplar |
|---|---|
| `<a new endpoint>` | `<path/to/file>` |
| `<a new module>` | `<path/to/file>` |
| `<a new test>` | `<path/to/file>` |

## 13 · Forbidden patterns (anti-spaghetti)

- No god-files: `<max ~N lines / one responsibility per file>`
- No cyclic dependencies between layers/modules.
- No drive-by refactors: change only what the task needs; unrelated cleanup is a separate task.
- No off-convention code: a second naming/error/test style is rejected — match §4–§8 or change them first.
- No dead/duplicate code paths: delete or reuse, don't fork.

## 14 · Decisions log pointer

- Architecture decisions live in [`.bequite/state/DECISIONS.md`](./DECISIONS.md).
- **Superseded-by:** when a rule here is replaced, mark it `~~struck~~ — superseded by DECISIONS.md#<anchor> (<date>)` rather than deleting silently.

---

## How this is used

- **Read before implementing.** New code must match this contract or update it first.
- The **Consistency check** and **`/bq-review` spec-pass** judge new code against §1–§13 — off-DNA code is a review finding, not a style nit.
- For UI specifics (tokens, type scale, components, motion), defer to [`.bequite/design/DESIGN_DNA.md`](../design/DESIGN_DNA.md); this file owns everything else.
