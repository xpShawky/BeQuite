#!/usr/bin/env bash
# skill/hooks/pretooluse-scraping-respect.sh
#
# PreToolUse hook: enforces Article VIII (Constitution v1.1.0) — scraping &
# automation discipline. Fires on Edit | Write | Bash. Exit code 2 (block) when:
#
#   1. New code imports a scraping library AND no robots.txt-respect path exists
#      in the same module/repo.
#   2. New code imports a scraping library AND no rate-limit/cache config exists
#      in the project.
#   3. New code imports a STEALTH library (undetected-chromedriver, Camoufox,
#      Scrapling stealth mode, Pydoll-with-stealth) AND no ADR with
#      `legitimate-basis ∈ { own-site, bug-bounty-allows, ToS-explicitly-allows,
#      security-research-with-coordinated-disclosure }` exists.
#   4. New code imports a CAPTCHA-solving service (2Captcha, CapSolver,
#      AntiCaptcha, DeathByCaptcha) AND no ADR with `legitimate-basis` exists.
#   5. New code aggregates PII fields (phone, ssn, email, address, dob) from
#      scraped HTML AND no consent-log path is in the same module.
#
# Wired in template/.claude/settings.json under PreToolUse for Edit + Write.
# Reads tool call JSON from stdin. Exit 0 = allow. Exit 2 = block (with reason).
#
# Cross-references: Article VIII binding rules; the hook is the enforcement
# layer that makes the prose rules unbypassable without an explicit ADR.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')

case "$TOOL_NAME" in
  Edit|Write) ;;
  *) exit 0 ;;
esac

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // ""')
case "$TOOL_NAME" in
  Edit) CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.new_string // ""') ;;
  Write) CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.content // ""') ;;
esac

# Skip the hook on the canonical reference doc + the hook itself + the persona +
# the doctrine — they legitimately *contain* the patterns as documentation.
case "$FILE_PATH" in
  *skill/references/scraping-and-automation.md|\
  *skill/agents/scraping-engineer.md|\
  *skill/hooks/pretooluse-scraping-respect.sh|\
  *skill/doctrines/ai-automation.md|\
  *skill/skills-bundled/ai-automation/*|\
  *.bequite/memory/constitution.md|\
  *.bequite/memory/decisions/ADR-009-*|\
  *CHANGELOG.md|\
  *tests/integration/scraping/*)
    exit 0
    ;;
esac

# ----- Define detection patterns ---------------------------------------------

# General scraping libraries — imports of any of these triggers the robots.txt +
# rate-limit + cache checks.
SCRAPING_IMPORTS=(
  # Python
  'from\s+scrapy\b' '\bimport\s+scrapy\b'
  'from\s+crawlee\b' '\bimport\s+crawlee\b'
  'from\s+trafilatura\b' '\bimport\s+trafilatura\b'
  'from\s+playwright\b' '\bimport\s+playwright\b'
  'from\s+selenium\b' '\bimport\s+selenium\b'
  'from\s+requests_html\b' '\bimport\s+requests_html\b'
  'from\s+bs4\b' '\bimport\s+bs4\b'
  'from\s+selectolax\b' '\bimport\s+selectolax\b'
  'from\s+pyppeteer\b' '\bimport\s+pyppeteer\b'
  'from\s+autoscraper\b' '\bimport\s+autoscraper\b'
  # Node/TS
  '"crawlee"' "'crawlee'"
  '"@crawlee/'
  '"firecrawl-js"' "'firecrawl-js'"
  '"@mendable/firecrawl-js"'
  '"playwright"' "'playwright'"
  '"puppeteer"' "'puppeteer'"
  '"cheerio"' "'cheerio'"
  '"jsdom"' "'jsdom'"
  # Go
  '"github.com/gocolly/colly"'
  '"github.com/MontFerret/ferret"'
  # Java/JVM
  'us\.codecraft\.webmagic'
)

# Stealth libraries — REQUIRE ADR with legitimate-basis field.
STEALTH_IMPORTS=(
  '\bundetected_chromedriver\b'
  '"undetected-chromedriver"' "'undetected-chromedriver'"
  '\bcamoufox\b'
  '"camoufox"' "'camoufox'"
  'scrapling[^"]*\bstealth\b'
  'pydoll[^"]*\bstealth\b'
  'playwright_stealth\b'
  '"playwright-extra-plugin-stealth"'
)

# Captcha-solving services — REQUIRE ADR with legitimate-basis field.
CAPTCHA_IMPORTS=(
  '\b2captcha\b' "'2captcha'" '"2captcha"' '\btwocaptcha\b'
  '\bcapsolver\b' '"capsolver"' "'capsolver'"
  '\banticaptcha\b' '"anticaptcha"' "'anticaptcha'"
  '\bdeathbycaptcha\b' '"deathbycaptcha"' "'deathbycaptcha'"
)

# PII fields — when assigned from scraped data without a consent log.
PII_FIELD_ASSIGNS=(
  '\b(phone_number|phoneNumber|phone)\b\s*[:=]'
  '\b(ssn|socialSecurityNumber|social_security)\b\s*[:=]'
  '\b(email|emailAddress|email_address)\b\s*[:=]'
  '\b(home_address|homeAddress|street_address|streetAddress)\b\s*[:=]'
  '\b(dob|date_of_birth|dateOfBirth|birthdate)\b\s*[:=]'
  '\b(passport|passport_number|passportNumber|nationalId|national_id)\b\s*[:=]'
)

# ----- Helpers ---------------------------------------------------------------

content_matches_any() {
  local content="$1"; shift
  local patterns=("$@")
  for pattern in "${patterns[@]}"; do
    if printf '%s' "$content" | grep -qE "$pattern"; then
      return 0
    fi
  done
  return 1
}

# Check that the project / module has at least ONE robots.txt-respect path.
# Heuristic: look for known robots.txt-checking patterns in the same file or in
# any sibling file in the same directory.
has_robots_respect() {
  local file="$1"
  local content="$2"
  # Same-file check.
  if printf '%s' "$content" | grep -qE 'robots[._-]?txt|RobotFileParser|robotparser|reppy|robotstxt'; then
    return 0
  fi
  # Sibling-file check.
  local dir
  dir=$(dirname "$file")
  if [[ -d "$dir" ]]; then
    if grep -rqE 'robots[._-]?txt|RobotFileParser|robotparser|reppy|robotstxt' "$dir" 2>/dev/null; then
      return 0
    fi
  fi
  # Project-level check (bequite.config.toml::scraping.respect_robots_txt = true).
  if [[ -f ".bequite/bequite.config.toml" ]] && grep -qE 'respect_robots_txt\s*=\s*true' .bequite/bequite.config.toml 2>/dev/null; then
    return 0
  fi
  return 1
}

# Check rate-limit + cache config exists somewhere in the project.
has_rate_limit_and_cache() {
  # Check bequite.config.toml.
  if [[ -f ".bequite/bequite.config.toml" ]]; then
    if grep -qE 'rate_limit|polite_mode\s*=\s*true' .bequite/bequite.config.toml 2>/dev/null && \
       grep -qE 'cache_ttl|cache_dir' .bequite/bequite.config.toml 2>/dev/null; then
      return 0
    fi
  fi
  # Check for in-code rate-limit/cache patterns (Crawlee/Scrapy/Trafilatura
  # have built-in patterns; user-side patterns also acceptable).
  if grep -rqE 'RATE_LIMIT|rate_limit|RATE_DELAY|throttle|polite_delay|DOWNLOAD_DELAY|requestQueue|concurrency_limit' \
        skill apps src cli 2>/dev/null; then
    if grep -rqE 'cache|sqlite_cache|HTTPCacheMiddleware|requests_cache|redis_cache|aiohttp_client_cache' \
          skill apps src cli 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

# Check ADR exists with a legitimate-basis field set to one of the four values.
has_legitimate_basis_adr() {
  local decisions_dir=".bequite/memory/decisions"
  [[ -d "$decisions_dir" ]] || return 1
  if grep -lE 'legitimate[-_]basis\s*[:=]\s*"?(own-site|bug-bounty-allows|ToS-explicitly-allows|security-research-with-coordinated-disclosure)' \
        "$decisions_dir"/*.md 2>/dev/null | head -1 | grep -q .; then
    return 0
  fi
  return 1
}

# Check that a consent-log path exists in the same module / repo.
has_consent_log() {
  local file="$1"
  local content="$2"
  # Same-file pattern.
  if printf '%s' "$content" | grep -qE 'consent[._-]?log|consent_record|consentTracker|withConsent|GDPR|gdpr_basis|lawful[._-]?basis'; then
    return 0
  fi
  # Project-level pattern.
  if grep -rqE 'consent[._-]?log|consent_record|consentTracker' \
        apps src skill 2>/dev/null; then
    return 0
  fi
  return 1
}

# ----- Run the checks --------------------------------------------------------

# Stealth — block immediately without ADR.
if content_matches_any "$CONTENT" "${STEALTH_IMPORTS[@]}"; then
  if ! has_legitimate_basis_adr; then
    cat >&2 <<EOF
[bequite hook: pretooluse-scraping-respect] BLOCKED — stealth library import without ADR.

Article VIII (Constitution v1.1.0): stealth scraping libraries
(undetected-chromedriver, Camoufox, Scrapling stealth mode, Pydoll
stealth, playwright-stealth) require an ADR enumerating
legitimate-basis ∈ {
  own-site,
  bug-bounty-allows,
  ToS-explicitly-allows,
  security-research-with-coordinated-disclosure
}.

File: $FILE_PATH
Hook scanned: stealth-import patterns

To proceed:
1. Write an ADR at .bequite/memory/decisions/ADR-SCRAPE-NNN-stealth-justification.md
2. Set the frontmatter field `legitimate-basis` to one of the four values above.
3. Document target scope, time window, and coordinated-disclosure path.
4. Re-run the Edit/Write.

Stealth without recorded legitimate basis is forbidden, period.
EOF
    exit 2
  fi
fi

# Captcha — block immediately without ADR.
if content_matches_any "$CONTENT" "${CAPTCHA_IMPORTS[@]}"; then
  if ! has_legitimate_basis_adr; then
    cat >&2 <<EOF
[bequite hook: pretooluse-scraping-respect] BLOCKED — captcha-solving service import without ADR.

Article VIII: captcha-solving services (2Captcha, CapSolver, AntiCaptcha,
DeathByCaptcha) require an ADR with legitimate-basis ∈ {
  own-site,
  bug-bounty-allows-captcha-bypass
}.

In many jurisdictions captcha-solving constitutes bypassing access
controls (CFAA-class). Default forbidden.

File: $FILE_PATH

To proceed: write an ADR at
.bequite/memory/decisions/ADR-SCRAPE-NNN-captcha-justification.md
documenting the legitimate basis. Re-run the Edit/Write.
EOF
    exit 2
  fi
fi

# General scraping import — require robots.txt + rate-limit/cache.
if content_matches_any "$CONTENT" "${SCRAPING_IMPORTS[@]}"; then
  if ! has_robots_respect "$FILE_PATH" "$CONTENT"; then
    cat >&2 <<EOF
[bequite hook: pretooluse-scraping-respect] BLOCKED — scraping library import without robots.txt path.

Article VIII Rule 1: ALWAYS read /robots.txt before scraping any domain.

File: $FILE_PATH

The hook found a scraping library import but no robots.txt-checking path
in this file, sibling files in the same directory, or in
.bequite/bequite.config.toml::scraping.respect_robots_txt.

To proceed:
- Add robotparser / robotstxt / reppy import + RobotFileParser usage in
  this module, OR
- Set bequite.config.toml::scraping = { polite_mode = true,
  respect_robots_txt = true } (the polite-mode preset).
EOF
    exit 2
  fi

  if ! has_rate_limit_and_cache; then
    cat >&2 <<EOF
[bequite hook: pretooluse-scraping-respect] BLOCKED — scraping library import without rate-limit + cache config.

Article VIII Rule 3: ALWAYS rate-limit (default 1 req/3 sec/domain).
Article VIII Rule 5: ALWAYS cache aggressively.

File: $FILE_PATH

To proceed (the easy path): set
.bequite/bequite.config.toml::
  [scraping]
  polite_mode = true   # enables 1 req/3 sec + 24h sqlite cache + UA + watch-budget

Or wire framework-level settings (Crawlee concurrency_limit + requestQueue;
Scrapy DOWNLOAD_DELAY + HTTPCacheMiddleware; Trafilatura built-in defaults).
EOF
    exit 2
  fi
fi

# PII aggregation — block when scraped + no consent log.
if content_matches_any "$CONTENT" "${PII_FIELD_ASSIGNS[@]}"; then
  # Cross-check: is this file part of a module that imports a scraping library?
  if content_matches_any "$CONTENT" "${SCRAPING_IMPORTS[@]}" || \
     ( [[ -d "$(dirname "$FILE_PATH")" ]] && \
       grep -rqE 'scrapy|crawlee|trafilatura|playwright|selenium|cheerio' "$(dirname "$FILE_PATH")" 2>/dev/null ); then
    if ! has_consent_log "$FILE_PATH" "$CONTENT"; then
      cat >&2 <<EOF
[bequite hook: pretooluse-scraping-respect] BLOCKED — PII field aggregation from scraped data without consent log.

Article VIII Rule 4: NEVER scrape personal data (names, emails, phones,
addresses, IDs, dates of birth, government IDs) without explicit user
consent + a documented legal basis (GDPR Art. 6, CCPA, Egyptian PDPL,
Saudi PDPL, UAE PDPL, or local equivalent).

File: $FILE_PATH

The hook found a PII field assignment in scraping-context code but no
consent-log / consent-tracker / lawful-basis pattern in this module or
the project tree.

To proceed:
1. Document the legal basis in .bequite/memory/decisions/
   ADR-SCRAPE-NNN-pii-lawful-basis.md
2. Add a consent-log / consent-tracker module that records each
   data-subject's consent (or other lawful basis: legitimate-interest,
   contractual-necessity, public-interest, etc.) before persistence.
3. Reference the consent log in this file.

If the data is genuinely public-figure / public-interest aggregation
(GDPR Art. 6(1)(e) or 6(1)(f)), document the assessment in the ADR.
EOF
      exit 2
    fi
  fi
fi

# All checks passed.
exit 0
