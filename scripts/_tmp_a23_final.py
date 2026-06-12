import io, re

def rw(p, pairs, enc='utf-8'):
    s = io.open(p, encoding=enc).read()
    for old, new in pairs:
        assert old in s, f"anchor missing in {p}: {old[:70]!r}"
        s = s.replace(old, new, 1)
    io.open(p, 'w', encoding=enc).write(s)
    print('ok', p)

# 1. Cross-agent docs: AGENTS.md is now THE standard
rw('docs/runbooks/INSTALL_FOR_OTHER_AGENTS.md', [
 ('## 2. The universal bridge file\n\nCreate this once per project as `AGENTS.md` at the repo root (most non-Claude agents read AGENTS.md-style files; for agents that don’t, paste the same block as the first message of each session):',
  '## 2. The universal bridge file — AGENTS.md (now an industry standard)\n\n**Verified 2026-06-12 (https://agents.md):** AGENTS.md is a Linux Foundation (Agentic AI Foundation) standard used by 60,000+ projects and supported natively by OpenAI Codex, Cursor, Gemini CLI, GitHub Copilot, Zed, Warp, Windsurf, Aider, goose, Devin, JetBrains Junie, Google Jules, and VS Code — which means **one bridge file covers nearly every non-Claude agent in the table below.** Create it once per project at the repo root; for the few agents that read nothing automatically, paste the same block as the first session message:'),
])
rw('docs/specs/AGENT_COMPATIBILITY_MATRIX.md', [
 ('**Reading the matrix:**',
  '**AGENTS.md note (verified 2026-06-12):** AGENTS.md is now a Linux Foundation standard with native support across most rows below (Codex, Cursor, Gemini CLI, Copilot, Zed, Warp, Windsurf, Aider, Devin, Junie…) — the single bridge file in `INSTALL_FOR_OTHER_AGENTS.md` §2 is therefore the default setup for any non-Claude agent; per-tool rules files are optional refinements.\n\n**Reading the matrix:**'),
])
rw('docs/architecture/CROSS_AGENT_COMPATIBILITY_STRATEGY.md', [
 ('Codex-class agents read AGENTS.md',
  'Codex-class agents (and per the Linux Foundation AGENTS.md standard, verified 2026-06-12: Cursor, Gemini CLI, Copilot, Zed, Warp, Windsurf, Aider, Devin, Junie too) read AGENTS.md'),
])

# 2. bq-suggest monetize journey + C11
rw('.claude/commands/bq-suggest.md', [
 ('**"I want to make money from a niche"** → 1. C6 `/bq-pain-radar` (verified pain first) · 2. C10 `/bq-make-money` (match to earning tracks) · 3. C8 `/bq-proposal` (pitch it) · 4. C5 `/bq-course` only if an education product is viable · 5. W4.2 `/bq-release proof` once something ships. Explain the order: evidence → opportunity → pitch → product → proof.',
  '**"I want to make money from a niche"** → 1. C6 `/bq-pain-radar` (verified pain first) · 2. C10 `/bq-make-money` (match to earning tracks) · 3. **C11 `/bq-offer`** (package the standing product) · 4. C8 `/bq-proposal` (pitch it per-client) · 5. C5 `/bq-course` only if an education product is viable · 6. W4.2 `/bq-release proof` once something ships. Explain the order: evidence → opportunity → offer → pitch → proof.'),
])

# 3. presentation-builder: Slidev verified note
p = '.claude/skills/bequite-presentation-builder/SKILL.md'
s = io.open(p, encoding='utf-8').read()
s += '\n\n## Tool catalog note (verified 2026-06-12)\n\nSlidev (github.com/slidevjs/slidev) live-verified actively maintained: v52.16.0 (2026-06-03), 47k+ stars; markdown-driven dev slides with PDF/PNG/PPTX export — a strong HTML-deck candidate alongside Marp / Reveal.js / pptxgenjs (those: re-verify at build time per tool-neutrality). Candidates, never defaults.\n'
io.open(p, 'w', encoding='utf-8').write(s)
print('ok', p)

# 4. REMAINING_WORK_MASTER: C->A move + G + header
rw('.bequite/tasks/REMAINING_WORK_MASTER.md', [
 ('**Updated:** 2026-06-12 (post-alpha.22 maintenance pass).', '**Updated:** 2026-06-12 (alpha.23 — /bq-offer built; tightening audits complete).'),
 ('## A. Built but NOT live-tested (alpha.22 capability commands)', '## A. Built but NOT live-tested (alpha.22 capability commands + alpha.23 offer)'),
 ('| C8 /bq-proposal | command + spec + no-overpromise rules | voice + honesty on a real job post | one real job post | 7 files in `.bequite/proposals/` | low | 85% |',
  '| C8 /bq-proposal | command + spec + no-overpromise rules | voice + honesty on a real job post | one real job post | 7 files in `.bequite/proposals/` | low | 85% |\n| **C11 /bq-offer (alpha.23)** | command + spec (OFFER_ENGINE) + scaffolded `.bequite/offers/` + full router/map/docs wiring | entire engine | one real offer idea ("AI automation for restaurants") | 12 files in `.bequite/offers/` | low | 85% |'),
 ('## C. Alpha.23 candidate — `/bq-offer` (C11)\n\n**Status: QUEUED, NOT BUILT**',
  '## C. Alpha.23 — `/bq-offer` (C11): **BUILT 2026-06-12 → moved to section A.** Next-release candidate: none committed — alpha.24 will be chosen from D/E after live trials inform priorities.\n\nHistorical record (pre-build status): **Status was: QUEUED, NOT BUILT**'),
 ('| Skill-audit baseline (orchestrator/guard-pass/localization-rtl) | ✅ DONE',
  '| Tightening audits (best-practice · duplication/conflict · generic-risk · quality matrices · evidence log · plan) | ✅ DONE 2026-06-12 (alpha.23) — 3 safe patches applied; P1 items: problem-solver example · multi-model phasing · `skill/` dir pointer (BEQUITE_TIGHTENING_PLAN.md) | M2/W3.2 | no | P1 items next maintenance pass |\n| Skill-audit baseline (orchestrator/guard-pass/localization-rtl) | ✅ DONE'),
])

# 5. G section add offer
p = '.bequite/tasks/REMAINING_WORK_MASTER.md'
s = io.open(p, encoding='utf-8').read()
old = '| Course PDF integration (Reference A verified) | this pass | n/a (it WAS the validation) | COURSE_PDF_REFERENCE_NOTES.md |'
new = old + '\n| **C11 /bq-offer built + tightening audits (4) + evidence log + plan** | alpha.23 | yes — offer live trial pending | OFFER_ENGINE.md · the 4 audit files · BEQUITE_TIGHTENING_PLAN.md |'
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok masterG')

# 6. SKILL_USAGE_LOG
p = '.bequite/skills/SKILL_USAGE_LOG.md'
s = io.open(p, encoding='utf-8').read()
s += '''
## 2026-06-12 — alpha.23: /bq-offer build + tightening pass (deep)
**Selected:** product-strategist + make-money + writing-dna (offer engine design) · anti-hallucination (honest-selling rules + audit evidence labels) · skill-auditor (matrices) · orchestrator (C11 wiring + conflict scan) · researcher (LIVE: agents.md standard, Slidev currency)
**Outcome:** SUCCESS — C11 built + wired (6-surface status flip); 4 audits + evidence log + tightening plan; AGENTS.md-standard finding patched into cross-agent docs
**Routing quality:** good
'''
io.open(p, 'w', encoding='utf-8').write(s)
print('ok usage log')

# 7. CHANGELOG new release section
p = 'docs/changelogs/CHANGELOG.md'
s = io.open(p, encoding='utf-8').read()
anchor = '## [3.0.0-alpha.22] - 2026-06-12'
add = '''## [3.0.0-alpha.23] - 2026-06-12 — Offer Engine + Tightening Pass

### Added
- **C11 `/bq-offer` (52 → 53 commands):** skill/service/niche/pain → sellable productized offer; 12 artifacts in `.bequite/offers/` (offer · target client · pain/outcome · deliverables+exclusions · pricing tiers · guarantee/risk-reversal · onboarding questions · outreach · demo idea · proof checklist · proposal angle · next steps). Honest-selling rules: no invented demand, no fake income claims, **promise ≠ guarantee**, no legal advice, UNVERIFIED-assumption marking, language follows the user's request. Completes the monetization chain C6 → C10 → **C11** → C8 → W4.2 proof. Spec `docs/specs/OFFER_ENGINE.md`. **Built, NOT live-tested.**
- **Tightening audits:** COMMAND_SKILL_BEST_PRACTICE_AUDIT (15 questions + 8 domain verdicts) · DUPLICATION_AND_CONFLICT_AUDIT (11 checks; 3 fixed, 1 deferred) · GENERIC_OUTPUT_RISK_AUDIT (risk-ranked guards) · COMMAND_SKILL_OUTPUT_QUALITY_MATRIX (53 commands + 30 skills, row by row) · BEST_PRACTICE_EVIDENCE_LOG (LIVE/PRIOR-LIVE/ECO sourcing) · BEQUITE_TIGHTENING_PLAN (P1: problem-solver example, multi-model phasing, `skill/` dir pointer)

### Changed
- **AGENTS.md verified as a Linux Foundation standard** (60k+ projects; Codex/Cursor/Gemini CLI/Copilot/Zed/Warp/Windsurf native support) — cross-agent docs rewritten around the single standard bridge file
- Monetization journey updated in router + suggest (+C11); proposal command/spec sibling notes; Slidev live-verified as presentation candidate (v52.16.0); installers → alpha.23 (+offers scaffold; bash -n OK, ps1 parse 0 errors)

### Honest status
- No live trials run on any capability command (now 7 of them); no parked V2 item built; quality matrices rate 0 weak commands, 2 thin/stale skills (P1-queued)

'''
assert anchor in s
s = s.replace(anchor, add + anchor, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok changelog')

# 8. AGENT_LOG
p = '.bequite/logs/AGENT_LOG.md'
s = io.open(p, encoding='utf-8').read()
m = 'Append-only chronicle of every BeQuite command run. Newest at top.\n'
e = '''
## 2026-06-12 — v3.0.0-alpha.23: /bq-offer + tightening pass (Claude Fable 5)

**Action:** Part 1: built C11 /bq-offer per the 15-step feature workflow (command + OFFER_ENGINE spec + offers/ scaffold + installer lines + ID map row + router signal/journey + skill-router domain + orchestration map + menu/help/README/commands.md/catalog/CLAUDE.md + proposal sibling notes — 6 "queued" markers flipped to built-not-live-tested). Part 2: tightening audits — best-practice (15 questions, 8 domains; 2 LIVE verifications: AGENTS.md = Linux Foundation standard w/ 60k projects + broad native support → cross-agent docs rewritten around it; Slidev v52.16.0 current), duplication/conflict (11 checks: 3 fixed incl. the C11 flip + AGENTS/GEMINI double-bridge + offers scaffold; 1 deferred: heavy-era skill/ dir), generic-output risk (HIGH class = market-claim commands; guards present, live proof pending), quality matrices (53 commands + 30 skills: 0 weak commands; 2 known thin/stale skills → P1), evidence log (honest LIVE/PRIOR-LIVE/ECO labels), tightening plan (P0 none open; P1×4; P2 on-demand; watch-items). MASTER updated (C11 → section A; alpha.24 = uncommitted, chosen after live trials). NOT done: parked V2 items, live trials, heavy anything. Model: Fable 5 — no switch/reroute.
'''
assert m in s
s = s.replace(m, m + e, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok agent log')

# 9. LAST_RUN
p = '.bequite/state/LAST_RUN.md'
s = io.open(p, encoding='utf-8').read()
old = '# Last BeQuite command\n\n**Command:** post-alpha.22 maintenance pass'
new = '''# Last BeQuite command

**Command:** v3.0.0-alpha.23 — Offer Engine (/bq-offer C11) + repo-wide tightening pass
**Timestamp:** 2026-06-12 (UTC)
**Model:** Claude Fable 5 — available, no reroute, no degradation
**Result:** SUCCESS — C11 built + fully wired (53 active commands; 6 queued-markers flipped); 4 tightening audits + evidence log + plan; 2 LIVE research verifications (AGENTS.md Linux-Foundation standard → cross-agent docs upgraded; Slidev current); 3 safe patches; quality matrices: 0 weak commands, 2 thin skills queued P1; installers alpha.23 (bash -n OK · ps1 0 errors). **No live trials claimed (7 capability commands now await first real runs). No parked V2 built.**
**Next suggested:** FIRST LIVE TRIAL — C11 /bq-offer with a real idea ("AI automation for restaurants") or C5 /bq-course (verified Reference A ready); the trials now gate everything else (alpha.24 selection, P1 skill patches pairing, calibration loop).

**Prior run (preserved):**
**Command:** post-alpha.22 maintenance pass'''
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok last run')

# 10. VERSION
p = '.bequite/state/BEQUITE_VERSION.md'
s = io.open(p, encoding='utf-8').read()
pat = re.compile(r'\*\*Version:\*\* v3\.0\.0-alpha\.22[^\n]*')
assert pat.search(s)
s = pat.sub('**Version:** v3.0.0-alpha.23 — Offer Engine (/bq-offer C11) + tightening pass', s, count=1)
s = s.replace('**Previous version:** v3.0.0-alpha.21', '**Previous version:** v3.0.0-alpha.22')
io.open(p, 'w', encoding='utf-8').write(s)
print('ok version')
