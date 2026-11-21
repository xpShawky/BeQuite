kind: script
run: python -I .claude/skills/bequite-agent-team/scripts/test_heartbeat.py && python -I .claude/skills/bequite-agent-team/scripts/test_operator_bridge.py
must: "ALL 37 CHECKS PASSED" and "ALL 19 CHECKS PASSED"; exit code 0
must_not: any "FAIL" line
