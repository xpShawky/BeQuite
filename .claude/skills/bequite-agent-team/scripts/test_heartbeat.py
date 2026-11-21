#!/usr/bin/env python3
"""Ledger test for heartbeat.py with scripted role outputs (no model calls).

Run: python -I test_heartbeat.py   -> exit 0 and "ALL N CHECKS PASSED"
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HB = Path(__file__).resolve().parent / "heartbeat.py"
passed = 0


def hb(team, *args):
    r = subprocess.run([sys.executable, "-I", str(HB), *args, "--team", str(team)],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def check(cond, what):
    global passed
    if not cond:
        print("FAIL:", what)
        sys.exit(1)
    passed += 1
    print("ok  ", what)


def job(team):
    code, out, err = hb(team, "next")
    assert code == 0, (code, out, err)
    return json.loads(out)


def record(team, j, tokens=1000, status="ok"):
    return hb(team, "record", "--job", j["id"], "--tokens", str(tokens), "--status", status)


def state(team, tid):
    return [l for l in (team / "tickets" / tid / "ticket.md").read_text(encoding="utf-8").splitlines()
            if l.startswith("state:")][0].split(":", 1)[1].strip()


BRIEF = "# Brief\n\n## Claims\n1. A fact [S1]\n2. Another [S2]\n\n## Sources\n- S1: https://example.org/a\n- S2: https://example.org/b\n"

with tempfile.TemporaryDirectory() as d:
    team = Path(d) / "team"
    check(hb(team, "init")[0] == 0, "init scaffolds a team folder")
    check((team / "roles" / "editor.md").exists() and (team / "budget.json").exists(), "roles and budget exist")
    check(hb(team, "gate")[0] == 3, "gate says NO_WORK on an empty team (exit 3)")

    (team / "inbox" / "idea-1.md").write_text("Post about X", encoding="utf-8")
    (team / "inbox" / "idea-2.md").write_text("Post about Y", encoding="utf-8")
    check(hb(team, "gate")[0] == 0, "gate sees inbox work (exit 0)")

    j = job(team)
    check(j["role"] == "chief" and "Inbox items" in j["prompt"], "first job is the chief")
    check(hb(team, "next")[0] == 4, "a second `next` is refused while a job is pending")
    (team / "tickets" / "_chief.json").write_text(json.dumps({"tickets": [
        {"title": "X explained", "angle": "for beginners", "inbox": "idea-1.md"},
        {"title": "Y explained", "angle": "for builders", "inbox": "idea-2.md"}], "dropped": []}), encoding="utf-8")
    check(record(team, j)[0] == 0, "chief output recorded")
    check(not list((team / "inbox").glob("idea-*.md")) and (team / "inbox" / "done" / "idea-1.md").exists(),
          "inbox items moved to inbox/done")

    # T-0001: scout -> writer -> editor rejects twice -> needs-owner
    j = job(team)
    check(j["role"] == "scout" and j["ticket"] == "T-0001", "scout takes T-0001")
    (team / "tickets" / "T-0001" / "brief.md").write_text("# Brief\n\n## Claims\n1. only one link https://e.org\n", encoding="utf-8")
    check(record(team, j)[0] == 1 and state(team, "T-0001") == "new", "a brief with 1 source is rejected by the ledger")
    j = job(team)
    (team / "tickets" / "T-0001" / "brief.md").write_text(BRIEF, encoding="utf-8")
    check(record(team, j)[0] == 0 and state(team, "T-0001") == "brief", "valid brief -> state brief")

    # T-0002 also needs a scout; the order is role first, so the scout job for T-0002 comes before the writer
    j = job(team)
    check(j["role"] == "scout" and j["ticket"] == "T-0002", "pipeline order: scout jobs before writer jobs")
    (team / "tickets" / "T-0002" / "brief.md").write_text(BRIEF, encoding="utf-8")
    record(team, j)

    for rnd in (1, 2):
        j = job(team)
        check(j["role"] == "writer" and j["ticket"] == "T-0001", f"writer drafts T-0001 (round {rnd})")
        if rnd == 2:
            check("rejected the last draft" in j["prompt"], "writer prompt carries the rejection on round 2")
        (team / "tickets" / "T-0001" / "draft.md").write_text(f"draft {rnd}", encoding="utf-8")
        record(team, j)
        j = job(team)
        if j["ticket"] != "T-0001":   # writer for T-0002 comes before editor for T-0001
            (team / "tickets" / j["ticket"] / "draft.md").write_text("draft", encoding="utf-8")
            record(team, j)
            j = job(team)
        check(j["role"] == "editor", f"editor reviews (round {rnd})")
        check(f"draft body is {len(f'draft {rnd}')} characters" in j["prompt"], f"editor prompt carries the measured length (round {rnd})")
        (team / "tickets" / j["ticket"] / "review.md").write_text("verdict: reject\n## Errors\n1. unsourced\n", encoding="utf-8")
        record(team, j)
    check(state(team, "T-0001") == "needs-owner", "two rejections -> needs-owner")
    appr = sorted((team / "approvals").glob("A-*.md"))
    check(any("kind: decision" in a.read_text(encoding="utf-8") for a in appr), "a decision approval was filed")
    check((team / "tickets" / "T-0001" / "review-round1.md").exists(), "each rejected round is kept")

    # T-0002: editor passes -> producer -> publish approval -> owner yes -> outbox
    j = job(team)
    check(j["role"] == "editor" and j["ticket"] == "T-0002", "editor reviews T-0002")
    (team / "tickets" / "T-0002" / "review.md").write_text("`verdict: pass`\n## Checked\n- S1\n", encoding="utf-8")
    record(team, j)
    check(state(team, "T-0002") == "passed", "pass -> state passed")
    j = job(team)
    check(j["role"] == "producer", "producer packages T-0002")
    (team / "tickets" / "T-0002" / "package.md").write_text("# Package\n## Final text\nhello\n", encoding="utf-8")
    record(team, j)
    check(state(team, "T-0002") == "awaiting-approval", "package -> awaiting-approval")
    pub = [a for a in (team / "approvals").glob("A-*.md") if "kind: publish" in a.read_text(encoding="utf-8")][0]
    check(hb(team, "gate")[0] == 3, "nothing runs while the only open items wait for the owner")
    check(not (team / "outbox" / "T-0002").exists(), "nothing reaches outbox before the yes")
    check(hb(team, "decide", "--approval", pub.stem, "--yes", "--by", "test")[0] == 0, "owner approves")
    check((team / "outbox" / "T-0002" / "package.md").exists() and state(team, "T-0002") == "approved",
          "approved package copied to outbox/")
    check(hb(team, "decide", "--approval", pub.stem, "--yes")[0] == 2, "an approval cannot be decided twice")

    # Budget: cap the scout, add work, expect a spend approval and no scout job
    b = json.loads((team / "budget.json").read_text(encoding="utf-8"))
    b["roles"]["scout"]["cap_tokens"] = 500
    (team / "budget.json").write_text(json.dumps(b), encoding="utf-8")
    (team / "inbox" / "idea-3.md").write_text("Post about Z", encoding="utf-8")
    j = job(team)
    (team / "tickets" / "_chief.json").write_text(json.dumps({"tickets": [{"title": "Z", "angle": "a", "inbox": "idea-3.md"}]}), encoding="utf-8")
    record(team, j)
    check(hb(team, "gate")[0] == 3, "scout over its cap: no job offered")
    spend = [a for a in (team / "approvals").glob("A-*.md") if "kind: spend" in a.read_text(encoding="utf-8")]
    check(len(spend) == 1, "one spend approval filed for the capped role")
    hb(team, "gate")
    spend = [a for a in (team / "approvals").glob("A-*.md") if "kind: spend" in a.read_text(encoding="utf-8")]
    check(len(spend) == 1, "the spend approval is not filed twice")
    hb(team, "decide", "--approval", spend[0].stem, "--yes")
    check(job(team)["role"] == "scout", "after the owner's yes the scout works again")

    log = "".join(p.read_text(encoding="utf-8") for p in (team / "log").glob("*.jsonl"))
    events = [json.loads(l)["event"] for l in log.splitlines()]
    check(all(e in events for e in ("job_start", "job_end", "state", "approval_filed", "approval_decided")),
          "log holds job, state and approval events")
    check("| T-0002 |" in (team / "board.md").read_text(encoding="utf-8"), "board.md lists the tickets")

print(f"ALL {passed} CHECKS PASSED")
