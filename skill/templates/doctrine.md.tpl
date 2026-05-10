---
name: {{DOCTRINE_NAME}}
version: {{DOCTRINE_VERSION}}
applies_to: [{{APPLIES_TO}}]   # tags: web-saas, cli, ml, desktop, library, regulated, locale-mena, etc.
supersedes: {{SUPERSEDES}}     # null on first version; otherwise the doctrine name + version this replaces
maintainer: {{MAINTAINER}}
ratification_date: {{RATIFICATION_DATE}}
license: MIT
---

# Doctrine: {{DOCTRINE_NAME}} v{{DOCTRINE_VERSION}}

> Loaded by `.bequite/bequite.config.toml::doctrines = [...]`. Iron Laws beat this Doctrine when in conflict. Other Doctrines may stack — when two Doctrines conflict, the one declared earliest in the config list wins (deterministic order).

## 1. Scope

What this Doctrine governs. Be specific about which project types it loads on and what it does NOT cover.

## 2. Rules

A numbered list of enforceable rules. Each rule:

- has a one-line statement
- declares a **rule kind**: `block` (audit fails) / `warn` (audit logs) / `recommend` (advisory)
- where possible, names a check (regex, file presence, dependency check, contract test)

Example format:

> ### Rule 1 — Tokens-only design
> **Kind:** `block`
> **Statement:** No hardcoded `font-family`, `color`, or `background` outside `tokens.css` / `tokens.json`.
> **Check:** `bequite audit` greps non-token color/font usage in CSS/TSX/Tailwind classes.

## 3. Stack guidance

When this Doctrine recommends a stack, list it here with a 1-line "why" per option. Cross-reference `references/stack-matrix.md`. The Architect agent uses this as a starting point for `bequite stack`; it MUST run `bequite freshness` before signing the ADR.

## 4. Verification

What `bequite verify` runs additionally for projects loaded with this Doctrine. Walk templates, smoke commands, axe-core configurations, contract test suites, etc.

## 5. Examples and references

Real-world projects that exemplify this Doctrine. External docs (Google's HEART framework, OWASP Top 10, etc.) the Doctrine relies on.

## 6. Forking guidance

How to fork this Doctrine for a downstream project. Pattern:

1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: <upstream-doctrine-name>@<upstream-version>` if applicable.
4. Document changes in a `## Changes` section.
5. Load via `.bequite/bequite.config.toml::doctrines = ["<your-name>"]`.

## 7. Changelog

Track every revision here, with a one-line reason.

```
{{DOCTRINE_VERSION}} — {{RATIFICATION_DATE}} — initial draft
```
