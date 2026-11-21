kind: script
run: build a package folder whose Telegram text is 5,000 characters and whose one claim has no source, then python -I .claude/skills/bequite-publish-prep/scripts/package_check.py <folder>
must: exit code 1; a FAIL line about the Telegram text length; a FAIL or warn line about the unsourced claim
must_not: exit code 0
