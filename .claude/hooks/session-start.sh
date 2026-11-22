#!/usr/bin/env bash
# BeQuite hook - SessionStart - inject what the agent must know before the first prompt.
# Plain stdout on exit 0 becomes context (Claude Code caps it at 10,000 characters; we stay under 9,000).
# Prints nothing outside a BeQuite project (no .bequite/ folder). Never blocks, never fails the session.
# Plugin installs run it from ${CLAUDE_PLUGIN_ROOT}; script installs enable it through /bq-hooks.
set -u
INPUT=""; [ -t 0 ] || INPUT="$(cat 2>/dev/null || true)"   # run by hand in a terminal: no input
PROJECT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT" 2>/dev/null || exit 0
if [ ! -d .bequite ]; then
  # a plugin install in a project with no memory yet: one line, so /bequite:bq-init knows where the scaffold is
  [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && echo "BeQuite plugin: this project has no .bequite/ memory yet. /bequite:bq-init creates it from $CLAUDE_PLUGIN_ROOT/templates/bequite (nothing is written until you run it)."
  exit 0
fi

HOME_DIR="${CLAUDE_PLUGIN_ROOT:-$PROJECT}"
first() { [ -f "$1" ] && head -n "$2" "$1" | tr -d '\r' | grep -v '^[[:space:]]*$'; }
field() { [ -f "$1" ] && sed -n "s/^\*\*$2:\*\* *//p" "$1" | head -n 1 | tr -d '\r'; }

{
  echo "## BeQuite session context"
  echo
  if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
    echo "BeQuite runs as a plugin: its docs, templates and scripts live under $CLAUDE_PLUGIN_ROOT. When a command cites \`.claude/bequite/...\`, \`templates/...\` or a skill's \`scripts/...\`, read it there. Updates come through /plugin."
  else
    if [ -f .claude/bequite/bin/bq-update.sh ]; then
      echo "Update check: $(bash .claude/bequite/bin/bq-update.sh 2>/dev/null | head -n 1)"
    fi
  fi
  echo "Every BeQuite command runs inside the pipeline (\`.claude/bequite/docs/architecture/PIPELINE.md\`): up to date, orient, references (creative work), research, options board, plan, approval, build, guard, verify, write back. No \"done\" without command + exit code + output, or UNVERIFIED."
  echo
  id="$(field .bequite/ACTIVE.md Id)"
  if [ -n "$id" ] && [ "$id" != "none" ]; then
    folder="$(field .bequite/ACTIVE.md Folder)"
    echo "### Active work: $id $(field .bequite/ACTIVE.md Title) (phase: $(field .bequite/ACTIVE.md Phase))"
    gates="${folder%/}/gates.md"
    [ -f "$gates" ] || gates=".bequite/work/$id/gates.md"
    if [ -f "$gates" ]; then
      open="$(grep -i 'pending\|open\|not set' "$gates" 2>/dev/null | head -n 8)"
      [ -n "$open" ] && { echo "Open gates:"; echo "$open"; }
    fi
  else
    echo "### Active work: none (new work starts with /bq-work new)"
  fi
  echo
  if [ -f .bequite/state/LAST_RUN.md ]; then echo "### Last run"; first .bequite/state/LAST_RUN.md 6; echo; fi
  if [ -f .bequite/state/MISTAKE_MEMORY.md ]; then
    echo "### Five most recent lessons (MISTAKE_MEMORY.md)"
    grep '^- ' .bequite/state/MISTAKE_MEMORY.md | tail -n 5 | cut -c1-400
    echo
  fi
  if [ -f .bequite/state/TASTE_RULES.md ]; then
    echo "### Taste rules (the owner's approved corrections)"
    grep '^- ' .bequite/state/TASTE_RULES.md | tail -n 12 | cut -c1-300
    echo
  fi
  n="$(grep -c '| new |' .bequite/state/TASTE_INBOX.md 2>/dev/null)"
  case "$n" in ''|*[!0-9]*) n=0 ;; esac
  [ "$n" -gt 0 ] && { echo "Taste inbox: $n new correction(s); /bq-taste review turns them into rules."; echo; }
  if [ -f .bequite/state/CAPABILITIES.md ] && ! grep -q 'Last updated:\*\* never' .bequite/state/CAPABILITIES.md; then
    echo "### Capabilities (CAPABILITIES.md)"
    grep '^| ' .bequite/state/CAPABILITIES.md | grep -v '^| *|\|---\|^| Program\|^| Browser\|^| Server\|^| Tool' | cut -d'|' -f2 | tr -s ' ' | paste -sd ',' - | cut -c1-600
  else
    echo "Capabilities: not recorded yet (/bq-doctor writes .bequite/state/CAPABILITIES.md)."
  fi
} 2>/dev/null | head -c 9000
exit 0
