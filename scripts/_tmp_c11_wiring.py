import io

def rw(p, pairs, enc='utf-8'):
    s = io.open(p, encoding=enc).read()
    for old, new in pairs:
        assert old in s, f"anchor missing in {p}: {old[:60]}"
        s = s.replace(old, new, 1)
    io.open(p, 'w', encoding=enc).write(s)
    print('ok', p)

# 1. COMMAND_ID_MAP
rw('.bequite/commands/COMMAND_ID_MAP.md', [
 ('**52 active commands + 1 deprecated alias.**', '**53 active commands + 1 deprecated alias.**'),
 ('| C10 | `/bq-make-money` | capability | any | legitimate earning tracks | (profile) | C6 / C8 | yes | no | CAP |',
  '| C10 | `/bq-make-money` | capability | any | legitimate earning tracks | (profile) | C6 / C8 | yes | no | CAP |\n| C11 | `/bq-offer` | capability | any | idea/niche/pain → sellable productized offer (12-file pack; no overpromise, no fake income claims) | C6 / C10 / C8 / C5 / user idea | C8 proposal / W4.2 proof / C1 / C2 / W1.3 intake / W2.3 landing | yes | no | CAP (alpha.23) · ARG `refine`, `lang=` |'),
 ('**Queued for alpha.23 (approved, not built):** C11 `/bq-offer` — sellable-offer builder (forgotten-candidate review + V3 #1). **Proposed only (not built):** `/bq-localize`',
  '**Proposed only (not built):** `/bq-localize`'),
])

# 2. ORCHESTRATION_MAP
rw('.bequite/state/ORCHESTRATION_MAP.md', [
 ('## 1–5. Commands (52 active + 1 alias', '## 1–5. Commands (53 active + 1 alias'),
 ('- **C capabilities:** presentation · writing-dna · reference · knowledge · course · pain-radar · integrate · proposal · job-finder · make-money (C11 offer = queued, NOT built)',
  '- **C capabilities:** presentation · writing-dna · reference · knowledge · course · pain-radar · integrate · proposal · job-finder · make-money · offer(C11, alpha.23 — built, not live-tested)'),
 ('proposal=per-client vs offer(future)=standing package', 'proposal=per-client pitch vs offer=standing productized package'),
])

# 3. COMMAND_ROUTER
rw('.bequite/commands/COMMAND_ROUTER.md', [
 ('| "build me a sellable offer" | future C11 `/bq-offer` (alpha.23 queue — until built, route to C6 pain-radar + C8 proposal) |',
  '| "build me a sellable offer" / productize my skill | **C11 `/bq-offer`** (built alpha.23 — needs an idea/niche; without one, C6 pain-radar or C10 make-money first) |'),
 ('**"Monetize a niche"** → 1. C6 `/bq-pain-radar` (find verified pain first) → 2. C10 `/bq-make-money` (match pain to earning tracks) → 3. C8 `/bq-proposal` (pitch the chosen opportunity) → 4. C5 `/bq-course` *only if* an education product is viable → 5. W4.2 `/bq-release proof` once something ships. Order matters: evidence → opportunity → pitch → product → proof.',
  '**"Monetize a niche"** → 1. C6 `/bq-pain-radar` (verified pain first) → 2. C10 `/bq-make-money` (match to earning tracks) → 3. **C11 `/bq-offer`** (package the standing product) → 4. C8 `/bq-proposal` (pitch it per-client) → 5. C5 `/bq-course` *only if* an education product is viable → 6. W4.2 `/bq-release proof` once something ships. Order matters: evidence → opportunity → offer → pitch → proof.'),
])

# 4. SKILL_ROUTER
rw('.bequite/skills/SKILL_ROUTER.md', [
 ('| proposal / RFP / client pitch | **writing-dna** + **product-strategist** (via C8 /bq-proposal) | job-finder/make-money safety intake · anti-hallucination |',
  '| proposal / RFP / client pitch | **writing-dna** + **product-strategist** (via C8 /bq-proposal) | job-finder/make-money safety intake · anti-hallucination |\n| productized offer / "package my skill into a product" | **product-strategist** + **make-money** (via C11 /bq-offer) | writing-dna (outreach voice) · anti-hallucination (no invented demand) · researcher (market claims) · localization-rtl (Arabic/MENA) |'),
])

# 5. bq-proposal + spec sibling notes
rw('.claude/commands/bq-proposal.md', [
 ('Future sibling: `/bq-offer` (productized offers) — proposed in Discovery V3, not built.',
  'Sibling: **C11 `/bq-offer`** (built alpha.23) — the standing productized package this command pitches per-client; its PROPOSAL_ANGLE.md feeds this command directly.'),
])
rw('docs/specs/PROPOSAL_BUILDER.md', [
 ('**sending the proposal is always user-performed** (external publishing = human action, never automated). Future sibling: `/bq-offer` (productized offers) — proposed in Discovery V3, not built.',
  '**sending the proposal is always user-performed** (external publishing = human action, never automated). Sibling: C11 `/bq-offer` (alpha.23) — the standing offer; PROPOSAL_ANGLE.md from an offer pack feeds this builder.'),
])

# 6. bequite menu
rw('.claude/commands/bequite.md', [
 ('Command map (52 active commands + 1 deprecated alias', 'Command map (53 active commands + 1 deprecated alias'),
 ('    C10 /bq-make-money  legitimate earning tracks (10 tracks + hidden gems)',
  '    C10 /bq-make-money  legitimate earning tracks (10 tracks + hidden gems)\n    C11 /bq-offer       idea/niche → sellable productized offer (honest: no fake demand or income claims)'),
])

# 7. bq-help
rw('.claude/commands/bq-help.md', [
 ('- **C8 `/bq-proposal`** — job post / RFP → honest tailored proposal (Writing DNA; never claims unevidenced skills)',
  '- **C8 `/bq-proposal`** — job post / RFP → honest tailored proposal (Writing DNA; never claims unevidenced skills)\n\nNew in alpha.23:\n- **C11 `/bq-offer`** — skill/service/niche/pain → sellable productized offer: target client, pain/outcome, deliverables + exclusions, pricing tiers, safe guarantee (promise ≠ guarantee), onboarding questions, outreach, demo idea, proof checklist, proposal angle. Monetization chain: pain-radar → make-money → **offer** → proposal → release proof.'),
 ('output covers all 52 active commands', 'output covers all 53 active commands'),
])

# 8. commands.md
rw('commands.md', [
 ('52 active slash commands (catalog IDs W/N/O/C/M) · 30 specialist skills', '53 active slash commands (catalog IDs W/N/O/C/M) · 30 specialist skills'),
 ('> **alpha.22 orchestration update (2026-06-12):**',
  '> **alpha.23 (2026-06-12) — `/bq-offer` (C11), the Offer Engine:** turn a skill, service, automation, product idea, course idea, niche, or pain point into a sellable productized offer — 12 artifacts in `.bequite/offers/` (offer, target client, pain/outcome, deliverables + exclusions, pricing tiers, guarantee/risk-reversal, onboarding questions, outreach, demo idea, proof checklist, proposal angle, next steps). Honest by contract: no invented demand, no fake income claims, promise separated from guarantee, no legal advice, assumptions marked. Completes the monetization chain: C6 pain-radar → C10 make-money → **C11 offer** → C8 proposal → W4.2 release proof. Spec: `docs/specs/OFFER_ENGINE.md`. Status: built, NOT live-tested.\n>\n> **alpha.22 orchestration update (2026-06-12):**'),
])

# 9. README
rw('README.md', [
 ('**Latest:** `v3.0.0-alpha.22` · MIT', '**Latest:** `v3.0.0-alpha.23` · MIT'),
 ('<img alt="52 commands" src="https://img.shields.io/badge/slash_commands-52-7c3aed?style=flat-square">', '<img alt="53 commands" src="https://img.shields.io/badge/slash_commands-53-7c3aed?style=flat-square">'),
 ('The installer copies `.claude/commands/` (52 active slash commands + 1 deprecated alias)', 'The installer copies `.claude/commands/` (53 active slash commands + 1 deprecated alias)'),
 ('`/bq-pain-radar` · `/bq-integrate` · `/bq-proposal` · `/bq-job-finder` · `/bq-make-money` |', '`/bq-pain-radar` · `/bq-integrate` · `/bq-proposal` · `/bq-offer` · `/bq-job-finder` · `/bq-make-money` |'),
 ("- **`/bq-job-finder`** / **`/bq-make-money`** — verified work opportunities and legitimate earning tracks, safety-first.",
  "- **`/bq-offer`** — a skill, niche, or pain point → a sellable productized offer: specific target client, deliverables with explicit exclusions, pricing tiers, a guarantee you can actually honor, outreach, demo idea, and proof checklist. Completes the monetization chain (pain-radar → make-money → offer → proposal → proof). No invented demand, no income hype.\n- **`/bq-job-finder`** / **`/bq-make-money`** — verified work opportunities and legitimate earning tracks, safety-first."),
 ('next command candidate is `/bq-offer` (sellable-offer builder); parked candidates', 'newest command is `/bq-offer` (alpha.23, not yet live-tested); parked candidates'),
])

# 10. catalog
rw('docs/specs/COMMAND_CATALOG.md', [
 ('**Total commands:** 52 active + 1 deprecated alias', '**Total commands:** 53 active + 1 deprecated alias'),
 ('**alpha.22:** Command Router layer', '**alpha.23:** **C11 /bq-offer** — Offer Engine (idea/niche → sellable productized offer; 12 outputs in `.bequite/offers/`; honest-selling rules; completes the monetization chain C6→C10→C11→C8→proof; spec `docs/specs/OFFER_ENGINE.md`; built, not live-tested)\n**alpha.22:** Command Router layer'),
])

# 11. CLAUDE.md (lean: bump spec line + commands count)
rw('CLAUDE.md', [
 ('## Current spec: v3.0.0-alpha.22 — Navigation & Capability Consolidation', '## Current spec: v3.0.0-alpha.23 — Offer Engine (+ alpha.22 navigation/orchestration base)'),
 ('- **52 active slash commands + 1 deprecated alias** (`.claude/commands/`) — alpha.22 adds', '- **53 active slash commands + 1 deprecated alias** (`.claude/commands/`) — alpha.23 adds C11 `/bq-offer` (Offer Engine — monetization chain C6→C10→C11→C8→proof; `.bequite/offers/`, spec OFFER_ENGINE.md); alpha.22 adds'),
])

# 12. installers: version + offers scaffold
BS = chr(92)
p = 'scripts/install-bequite.sh'
s = io.open(p, encoding='utf-8').read()
s = s.replace('BEQUITE_VERSION="v3.0.0-alpha.22"', 'BEQUITE_VERSION="v3.0.0-alpha.23"')
s = s.replace(',commands,reference,knowledge,courses,pain-radar,integrations,proposals}', ',commands,reference,knowledge,courses,pain-radar,integrations,proposals,offers}')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', p)
p = 'scripts/install-bequite.ps1'
s = io.open(p, encoding='utf-8-sig').read()
s = s.replace('$BEQUITE_VERSION = "v3.0.0-alpha.22"', '$BEQUITE_VERSION = "v3.0.0-alpha.23"')
old = '  "' + '.bequite' + BS + 'proposals' + '"' + '\n)'
new = '  "' + '.bequite' + BS + 'proposals' + '",\n  "' + '.bequite' + BS + 'offers' + '"\n)'
assert old in s, 'ps1 proposals anchor'
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8-sig', newline='\r\n').write(s)
print('ok', p)
