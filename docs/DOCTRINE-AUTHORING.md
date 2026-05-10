# Doctrine authoring

> How to fork or write a new Doctrine.

## What's a Doctrine?

A Doctrine is a forkable rule pack. It declares which rules apply to a project type. Stack two or more (e.g. `default-web-saas + mena-bilingual + mena-pdpl`).

## File format

Every Doctrine is a single Markdown file at `skill/doctrines/<name>.md` (parent BeQuite) or `.bequite/doctrines/<name>.md` (project fork). Required frontmatter:

```yaml
---
name: <slug>
version: 1.0.0
applies_to: [<categories>]   # e.g. [web-saas, frontend]
supersedes: null             # or "<name>@<version>"
maintainer: <name (handle)>
ratification_date: YYYY-MM-DD
license: MIT
---
```

Required sections:

1. `## 1. Scope` — what projects this Doctrine targets + does NOT target.
2. `## 2. Rules` (or `Common rules`, `Strict rules`) — numbered binding rules.
3. `## 3. Stack guidance` — recommended stack per layer.
4. `## 4. Verification` — extra `bequite verify` gates.
5. `## 5. Examples and references` — links.
6. `## 6. Forking guidance` — how to extend.
7. `## 7. Changelog`.

## Rule format

Each rule has 4 fields:

```markdown
### Rule N — <slug>
**Kind:** `block` | `recommend` | `warn`
**Statement:** <what is required / forbidden>.
**Check:** <how `bequite audit` enforces (or "advisory")>.
**Why:** <one sentence rationale>.
```

`block` rules trip exit-code-2 on violation. `recommend` are advisory. `warn` flag in CI but don't fail.

## Forking an existing Doctrine

```bash
# 1. Copy the parent Doctrine into your project.
mkdir -p .bequite/doctrines/
cp skill/doctrines/default-web-saas.md .bequite/doctrines/my-saas.md

# 2. Edit frontmatter:
#    - name: my-saas
#    - version: 0.1.0
#    - supersedes: default-web-saas@1.1.0

# 3. Add ## Changes section explaining your overrides.

# 4. Load via .bequite/bequite.config.toml
#    doctrines = ["my-saas"]
```

## Writing a new Doctrine from scratch

1. Pick a unique `name` slug.
2. Copy `skill/templates/doctrine.md.tpl` as the starting skeleton.
3. Define 6-15 rules (binding + recommend mix).
4. Document stack guidance (per-layer table — frontend / backend / db / auth / hosting / pooling).
5. Document additional `bequite verify` gates if the Doctrine adds any.
6. PR into BeQuite's `skill/doctrines/` if it's general-purpose; otherwise keep at `.bequite/doctrines/<your-org>-<name>.md`.

## Stack honesty (Article V)

A Doctrine's stack guidance MUST be scale-tier-honest. If your Doctrine targets ≥50K MAU projects, do not recommend SQLite for write-heavy workloads. The audit rules in `cli/bequite/audit.py` cross-check Doctrine recommendations against declared scale tier.

## Stacking rules

Multiple Doctrines stack additively. When two Doctrines have conflicting rules, the LATER-LOADED Doctrine wins (last-write semantics). Use this carefully; document the override in `## Changes`.

## Examples in the BeQuite repo

- `skill/doctrines/default-web-saas.md` — most-used; v1.1.0 with 14 rules + frontend MCPs (v0.6.1 update).
- `skill/doctrines/mena-bilingual.md` — Arabic + RTL; stacks with default-web-saas.
- `skill/doctrines/vibe-defense.md` — Veracode 2025 backstop; default for `audience: vibe-handoff`.
- `skill/doctrines/ai-automation.md` — n8n/Make/Zapier projects.

## Cross-references

- Existing Doctrines: `skill/doctrines/`
- Doctrine schema template: `skill/templates/doctrine.md.tpl`
- Constitution Article references: `.bequite/memory/constitution.md`
