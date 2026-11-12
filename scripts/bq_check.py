#!/usr/bin/env python3
"""bq_check - BeQuite self-check. Turns written rules into failing checks.

Standard library only (no installs). Run from anywhere:
    python3 scripts/bq_check.py            # all checks
    python3 scripts/bq_check.py --list     # list checks
    python3 scripts/bq_check.py installer  # run named checks only

Exit code 0 = all checks pass, 1 = at least one failure.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


# ---------------------------------------------------------------- installer
@check
def installer():
    """install-bequite.ps1 must be pure ASCII with no BOM (irm|iex breaks otherwise)."""
    errors = []
    ps1 = os.path.join(ROOT, "scripts", "install-bequite.ps1")
    data = read_bytes(ps1)
    if data[:3] == b"\xef\xbb\xbf":
        errors.append("scripts/install-bequite.ps1: starts with a UTF-8 BOM (breaks `irm | iex`)")
    bad = [i for i, b in enumerate(data) if b > 127]
    if bad:
        line = data[: bad[0]].count(b"\n") + 1
        errors.append("scripts/install-bequite.ps1:%d: non-ASCII byte (%d found in total)" % (line, len(bad)))
    head = data[:2000].decode("ascii", "replace").lower()
    if "[cmdletbinding()]" in head or "\nparam(" in head:
        errors.append("scripts/install-bequite.ps1: has a param()/CmdletBinding block (Invoke-Expression cannot run it)")
    import re
    for n, line in enumerate(data.decode("ascii", "replace").splitlines(), 1):
        code = line.split("#", 1)[0]
        if re.search(r"(^|[\s;{])exit(\s|$|;)", code):
            errors.append("scripts/install-bequite.ps1:%d: uses `exit` (closes the user's shell under irm|iex; use return)" % n)
    if not os.path.isdir(os.path.join(ROOT, "templates", "bequite")):
        errors.append("templates/bequite/ missing (installers copy the memory scaffold from it)")
    sh = os.path.join(ROOT, "scripts", "install-bequite.sh")
    if read_bytes(sh)[:3] == b"\xef\xbb\xbf":
        errors.append("scripts/install-bequite.sh: starts with a UTF-8 BOM")
    return errors


def main(argv):
    if "--list" in argv:
        for fn in CHECKS:
            print("%-14s %s" % (fn.__name__, (fn.__doc__ or "").strip()))
        return 0
    wanted = [a for a in argv if not a.startswith("-")]
    selected = [fn for fn in CHECKS if not wanted or fn.__name__ in wanted]
    failed = 0
    for fn in selected:
        errors = fn()
        if errors:
            failed += 1
            print("FAIL  %s (%d)" % (fn.__name__, len(errors)))
            for e in errors:
                print("      - " + e)
        else:
            print("ok    %s" % fn.__name__)
    print("\n%d/%d checks passed" % (len(selected) - failed, len(selected)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
