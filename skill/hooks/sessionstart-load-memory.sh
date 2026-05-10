#!/usr/bin/env bash
# skill/hooks/sessionstart-load-memory.sh
#
# SessionStart hook: prints the paths the agent must read on session start
# (Iron Law III — Memory discipline). Claude Code captures this output and
# treats it as priority context.
#
# Non-blocking. Exit 0 always.

set -uo pipefail

cat <<'EOF'
[bequite hook: sessionstart-load-memory] Article III — load these on session start:

CONSTITUTION (binding):
- AGENTS.md
- CLAUDE.md
- .bequite/memory/constitution.md

MEMORY BANK (six files; durable cross-session brain):
- .bequite/memory/projectbrief.md
- .bequite/memory/productContext.md
- .bequite/memory/systemPatterns.md
- .bequite/memory/techContext.md
- .bequite/memory/activeContext.md
- .bequite/memory/progress.md

ACTIVE ADRs:
- .bequite/memory/decisions/

CURRENT OPERATIONAL STATE (master pattern; refresh more often):
- state/project.yaml
- state/current_phase.md
- state/recovery.md
- state/task_index.json

LOADED DOCTRINES (per state/project.yaml::active_doctrines):
- skill/doctrines/<doctrine>.md  (or .bequite/doctrines/ for forks)

LATEST SNAPSHOTS:
- .bequite/memory/prompts/v<N>/

Failure to load these breaks Iron Law III. Skip nothing.
EOF

# If state files exist, surface "what to resume from" pointer.
if [[ -f "state/recovery.md" ]]; then
  echo ""
  echo "RESUME FROM: state/recovery.md::What is the next safe task"
fi

exit 0
