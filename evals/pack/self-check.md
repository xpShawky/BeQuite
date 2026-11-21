kind: script
run: python scripts/bq_check.py
must: exit code 0; the last line reads "N/10 checks passed" with no FAIL line
must_not: any line starting with "FAIL"
