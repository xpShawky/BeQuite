#!/usr/bin/env python3
"""List post-worthy moments in a work folder's evidence and log: lines that carry a number AND a
failure, fix, before/after, cost or surprise. Every candidate keeps its file and line so the post
can quote the evidence verbatim (from-work never invents a result).

  python from_work_moments.py .bequite/work/0001-launch [more work folders] [--top 15]

Scores: +2 a number with a unit (s, MB, %, credits, x, frames, views), +2 a failure/fix word,
+1 a before/after or comparison word, +1 a lesson marker ("Rule:", "Lesson", "Mistake"),
-2 a line that is mostly a path or a command. Read the top lines, pick three, write them in the
owner's voice, and run the human test.
"""
import argparse
import re
import sys
from pathlib import Path

NUM = re.compile(r"\b\d[\d,.]*\s?(%|s\b|ms\b|MB|KB|GB|credits?|cr\b|x\b|frames?|views|px|LUFS|min\b|fps)", re.I)
FAIL = re.compile(r"\b(fail(ed|s)?|broke|bug|wrong|lost|crash(ed)?|reject(ed)?|mistake|stalled|timed? out|429|error|fix(ed)?|root cause|instead)\b", re.I)
CMP = re.compile(r"\b(vs\.?|versus|before|after|from .* to|than|was .* now|x faster|times)\b", re.I)
LESSON = re.compile(r"(Rule:|Lesson|Mistake:|lesson|learned)")
PATHY = re.compile(r"(`[^`]*[/\\][^`]*`|\$ |python |\.py\b|\.jsx\b)")


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("works", nargs="+")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    rows = []
    for w in a.works:
        for name in ("evidence.md", "log.md", "evidence-B.md", "log-B.md"):
            f = Path(w) / name
            if not f.exists():
                continue
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if len(line) < 30:
                    continue
                score = 2 * bool(NUM.search(line)) + 2 * bool(FAIL.search(line)) + bool(CMP.search(line)) + bool(LESSON.search(line))
                score -= 2 * (len(PATHY.findall(line)) >= 3)
                if score >= 4:
                    rows.append((score, f"{f}:{i}", line.strip()[:240]))
    rows.sort(key=lambda r: -r[0])
    for s, ref, line in rows[: a.top]:
        print(f"[{s}] {ref}\n    {line}")
    print(f"\n{len(rows)} candidates scored 4+; showing {min(a.top, len(rows))}")


if __name__ == "__main__":
    main()
