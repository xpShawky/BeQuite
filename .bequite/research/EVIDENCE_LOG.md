# Evidence Log

> **Durable verification evidence** — the file backing `bequite-anti-hallucination`'s evidence-over-claims rule. Every "works / done / passes" claim in a long run records its proof here so it survives compaction and feeds `/bq-verify`, `/bq-review`, and audits. Short runs may paste evidence inline instead; long runs MUST externalize here.
>
> Created alpha.19 (Fable Strengthening Pass). Per `docs/architecture/CONTEXT_ENGINEERING_STRATEGY.md` + execution contract step 8.

---

## Entry format

```markdown
## <ISO 8601 UTC> — <claim being evidenced>
**Claim:** <e.g. "build passes after the auth fix">
**Command:** `<exact command>`
**Exit code:** <n>
**Key output:** <the lines that prove the claim — trimmed, not the whole log>
**Verified by:** <command run live this session | UNVERIFIED — reason>
**Related:** <file:line / task ID / gate>
```

Rules:
- One claim per entry. No entry → the claim is `UNVERIFIED:` and must be labeled so in any report.
- Trim output to the proving lines; link big logs by path instead of pasting.
- Never log secret values — reference by key name.
- Prune: archive entries for shipped releases into `EVIDENCE_LOG-<version>.md` at release time.

---

## Entries (newest at top)

## 2026-06-11 — alpha.19 ship verification (dogfood — first entries)

**Claim:** sh installer remains syntactically valid after alpha.19 edits
**Command:** `bash -n scripts/install-bequite.sh`
**Exit code:** 0
**Key output:** (none — clean parse)
**Verified by:** command run live this session
**Related:** scripts/install-bequite.sh · alpha.19 installer updates

**Claim:** ps1 installer parses cleanly after BOM fix (and the parse errors it fixes were PRE-EXISTING, not a regression)
**Command:** `[System.Management.Automation.Language.Parser]::ParseFile(...)` on (a) HEAD extraction and (b) working copy
**Exit code:** 0 both runs
**Key output:** (a) "HEAD version: 3 parse errors - PRE-EXISTING" · (b) "ps1 parse OK"
**Verified by:** both commands run live this session
**Related:** scripts/install-bequite.ps1 · UTF-8 BOM fix

**Claim:** `bq-review` frontmatter degradation was a display artifact, not a file defect
**Command:** Read `.claude/commands/bq-review.md` lines 1–10
**Key output:** line 2 = full description string intact
**Verified by:** read live this session
**Related:** SKILL_QUALITY_AUDIT.md finding #4 (false alarm)

## 2026-06-12 — alpha.22 verification evidence

- `bash -n scripts/install-bequite.sh` → exit 0 ("sh syntax OK")
- PowerShell `[Parser]::ParseFile(install-bequite.ps1)` → "ps1 parse OK - 0 errors" (BOM preserved via utf-8-sig round-trip)
- File counts post-pass: `ls .claude/commands/*.md | wc -l` → **53** (52 active + 1 deprecated alias) · `ls -d .claude/skills/bequite-*/ | wc -l` → **29**
- guard-skills concept: WebFetch https://github.com/amElnagdy/guard-skills → 5 guards, progressive disclosure, reactive diff-review, no-scripts/no-network principles (concept only; nothing copied)
- Course PDF: `find . -iname "*.pdf"` → no results — PDF NOT accessible this session; recorded honestly in COURSE_ENGINE.md
- Stale-count sweep: fixed INSTALL runbook (24/7, alpha.1-era), bequite.md ("34 commands"), bq-help quality gate ("37"), bq-suggest ("39/15"), commands.md:218 ("37"), CLAUDE.md (header drifted at alpha.19)

## 2026-06-13 - alpha.24 hotfix: ps1 install via iex
- Repro (user-reported): `irm ...install-bequite.ps1 | iex` -> "Unexpected attribute CmdletBinding" / "Unexpected token param". Root cause: param() block invalid under Invoke-Expression.
- Fix verified: replaced param() with manual $args/env parsing. `[ScriptBlock]::Create((Get-Content -Raw install-bequite.ps1))` -> "iex-path compile: OK"; `ParseFile` -> 0 errors. Both paths now compile.
- New standing check: installer release verify must run the [ScriptBlock]::Create iex-path test, not only ParseFile.

## 2026-06-13 - alpha.24 hotfix #2: BOM/non-ASCII in ps1 install
- 2nd user error after param fix: `.SYNOPSIS`/`Copies`/`No`/`By` "not recognized" + `﻿<#` token. Cause: UTF-8 BOM + em/en-dashes; BOM glued to `<#` so comment block never opened under iex.
- Fix: stripped BOM, replaced all em/en-dashes with ASCII "-", replaced `<# #>` help block with `#` comments. Verified: 0 bytes >127, no BOM, [ScriptBlock]::Create(UTF8 decode) OK, AND full end-to-end run via `Get-Content -Raw | iex` (env BEQUITE_FROM_LOCAL, temp dir) -> "v3.0.0-alpha.24 installed", 60 cmd files / 31 skills / scaffold incl automation. No network.
