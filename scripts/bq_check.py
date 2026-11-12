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


import re
import glob

CMD_DIR = os.path.join(ROOT, ".claude", "commands")
SKILL_DIR = os.path.join(ROOT, ".claude", "skills")


def commands():
    return sorted(glob.glob(os.path.join(CMD_DIR, "*.md")))


def is_deprecated(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(400)
    return re.search(r"^description:\s*['\"]?Deprecated alias", head, re.M) is not None


def active_commands():
    return [p for p in commands() if not is_deprecated(p)]


def skills():
    return sorted(d for d in glob.glob(os.path.join(SKILL_DIR, "bequite-*")) if os.path.isdir(d))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return None if end < 0 else text[3:end].strip("\n")


def public_docs():
    """Markdown that ships or is published (not CHANGELOG history)."""
    out = [os.path.join(ROOT, f) for f in ("README.md", "CLAUDE.md", "commands.md", "AGENTS.md")]
    for pat in (".claude/commands/*.md", ".claude/skills/bequite-*/**/*.md", ".claude/bequite/**/*.md",
                "templates/**/*.md", "motion-library/*.md"):
        out += glob.glob(os.path.join(ROOT, pat), recursive=True)
    return [p for p in out if os.path.isfile(p)]


# ---------------------------------------------------------------- frontmatter
@check
def frontmatter_valid():
    """Every command and skill has parseable frontmatter with a description (quote values containing ': ')."""
    errors = []
    files = commands() + [os.path.join(d, "SKILL.md") for d in skills()]
    for path in files:
        if not os.path.isfile(path):
            errors.append("%s: missing" % rel(path))
            continue
        fm = frontmatter(read(path))
        if fm is None:
            errors.append("%s: no frontmatter" % rel(path))
            continue
        keys = {}
        for n, line in enumerate(fm.splitlines(), 2):
            if not line.strip() or line.startswith((" ", "\t", "#")):
                continue
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not m:
                errors.append("%s:%d: not a `key: value` line" % (rel(path), n))
                continue
            key, val = m.group(1), m.group(2)
            keys[key] = val
            if val[:1] in ("'", '"'):
                if len(val) < 2 or val[-1] != val[0]:
                    errors.append("%s:%d: unterminated quoted value for `%s`" % (rel(path), n, key))
            elif val[:1] in ("|", ">", "[", "{", ""):
                pass
            elif ": " in val or " #" in val or val.endswith(":"):
                errors.append("%s:%d: unquoted `%s` contains ': ' or ' #' (YAML breaks; wrap it in quotes)" % (rel(path), n, key))
        if not keys.get("description", "").strip(" '\"|>"):
            errors.append("%s: frontmatter has no description" % rel(path))
        if path.endswith("SKILL.md") and keys.get("name", "").strip("'\"") != os.path.basename(os.path.dirname(path)):
            errors.append("%s: `name` must equal the folder name" % rel(path))
    return errors


# ---------------------------------------------------------------- references
NOT_BUILT_RE = re.compile(r"not built|removed in v4|proposed|proposal only|optional proposal|may be added later|rejected|deferred|no `/bq-|parked", re.I)
REF_RE = re.compile(r"(?<![\w./-])((?:scripts|templates|motion-library|\.claude/bequite|\.claude/commands|\.claude/skills|\.github)/[\w./-]*[\w/])")


@check
def references_exist():
    """Paths to repo files (docs/, scripts/, templates/, .claude/...) and /bq-* commands and bequite-* skills must exist."""
    errors = []
    cmd_names = {os.path.basename(p)[:-3] for p in commands()}
    skill_names = {os.path.basename(d) for d in skills()}
    for path in public_docs():
        r = rel(path)
        if r.startswith(".claude/bequite/docs/decisions/"):
            continue  # ADRs are immutable history; they may cite removed paths
        operational = not r.startswith(".claude/bequite/docs/")  # docs may discuss proposed/rejected names
        text = read(path)
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue  # code blocks hold examples and sample output
            if NOT_BUILT_RE.search(line):
                continue  # explicit mention of something that intentionally does not exist
            spans = [s.group(1) for s in re.finditer(r"`([^`]+)`", line)] + [s.group(1) for s in re.finditer(r"\]\(([^)\s]+)\)", line)]
            for span in spans:
              for m in REF_RE.finditer(span):
                ref = m.group(1).rstrip("./")
                nxt = span[m.end():m.end() + 2]
                if nxt[:1] in ("*", "{", "<", "-") or nxt in (".{", ".*") or any(ch in ref for ch in "<>*{}") or "..." in span or "/NNNN" in ref:
                    continue
                if not os.path.exists(os.path.join(ROOT, ref)):
                    errors.append("%s:%d: missing path `%s`" % (rel(path), n, ref))
            if not operational:
                continue
            for m in re.finditer(r"(?<![\w/.-])/(bq-[a-z0-9-]+|bequite)\b", line):
                if m.group(1) not in cmd_names:
                    errors.append("%s:%d: unknown command `/%s`" % (rel(path), n, m.group(1)))
            for m in re.finditer(r"\bbequite-[a-z0-9-]+\b", line):
                name = m.group(0)
                if name.startswith(("bequite-installer", "bequite-update", "bequite-project", "bequite-")) and name not in skill_names:
                    if name in ("bequite-installer", "bequite-update"):
                        continue
                    if re.search(r"bequite-[a-z0-9-]+\.(md|sh|ps1|json|py)", line[m.start():m.end() + 6]):
                        continue
                    errors.append("%s:%d: unknown skill `%s`" % (rel(path), n, name))
    return errors


# ---------------------------------------------------------------- counts
@check
def counts_match():
    """'N commands' / 'N skills' claims in current docs match the filesystem."""
    errors = []
    n_cmd_files = len(commands())
    n_active = len(active_commands())
    n_skills = len(skills())
    allowed_cmd = {n_cmd_files, n_active}  # "N commands" may count all files or only active ones
    files = [os.path.join(ROOT, f) for f in ("README.md", "CLAUDE.md", "commands.md")]
    files += glob.glob(os.path.join(ROOT, "docs", "specs", "COMMAND_CATALOG.md"))
    files += glob.glob(os.path.join(ROOT, "templates", "bequite", "**", "*.md"), recursive=True)
    files += glob.glob(os.path.join(SKILL_DIR, "bequite-*", "SKILL.md"))
    for path in files:
        for n, line in enumerate(read(path).splitlines(), 1):
            low = line.lower()
            if "alpha" in low or "->" in line or "→" in line or "was " in low:
                continue
            for m in re.finditer(r"\b(\d{2,3})\s+(?:active\s+)?(?:slash\s+)?commands\b", low):
                if int(m.group(1)) not in allowed_cmd:
                    errors.append("%s:%d: says %s commands (actual %d active, %d files incl. deprecated aliases)" % (rel(path), n, m.group(1), n_active, n_cmd_files))
            for m in re.finditer(r"\b(\d{2,3})\s+(?:specialist\s+|bequite\s+)?skills\b", low):
                if int(m.group(1)) != n_skills:
                    errors.append("%s:%d: says %s skills (actual %d)" % (rel(path), n, m.group(1), n_skills))
            for m in re.finditer(r"badge/(slash_commands|skills)-(\d+)", line):
                want = n_active if m.group(1) == "slash_commands" else n_skills
                if int(m.group(2)) not in (want, n_cmd_files):
                    errors.append("%s:%d: badge says %s=%s (actual %d)" % (rel(path), n, m.group(1), m.group(2), want))
    return errors


# ---------------------------------------------------------------- contract block
READ_ONLY = {"bequite", "bq-help", "bq-now", "bq-explain"}
CONTRACT_OPEN = "<!-- bq:contract -->"
CONTRACT_CLOSE = "<!-- /bq:contract -->"
CONTRACT_BODY = (
    "> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):\n"
    "> 1. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.\n"
    "> 2. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).\n"
    "> 3. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.\n"
    "> 4. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.\n"
    "> 5. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.\n"
    "> 6. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.\n"
    "> 7. **Finish** with the Next Command Recommendations block.\n"
)
CONTRACT_BLOCK = CONTRACT_OPEN + "\n" + CONTRACT_BODY + CONTRACT_CLOSE


def action_commands():
    return [p for p in commands() if os.path.basename(p)[:-3] not in READ_ONLY and not is_deprecated(p)]


@check
def contract_block():
    """Every action command carries the standard contract block (fix: bq_check.py --fix contract)."""
    errors = []
    for path in action_commands():
        text = read(path)
        if CONTRACT_BLOCK not in text:
            errors.append("%s: missing or outdated contract block" % rel(path))
    return errors


def fix_contract():
    changed = 0
    for path in action_commands():
        text = read(path)
        if CONTRACT_BLOCK in text:
            continue
        if CONTRACT_OPEN in text and CONTRACT_CLOSE in text:
            a = text.index(CONTRACT_OPEN)
            b = text.index(CONTRACT_CLOSE) + len(CONTRACT_CLOSE)
            text = text[:a] + CONTRACT_BLOCK + text[b:]
        else:
            m = re.search(r"^# .*\n", text, re.M)
            if not m:
                print("cannot place block (no H1): " + rel(path))
                continue
            text = text[:m.end()] + "\n" + CONTRACT_BLOCK + "\n" + text[m.end():]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        changed += 1
    print("contract block written to %d command(s)" % changed)


# ---------------------------------------------------------------- gates
GATE_RE = re.compile(r"`([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*_(?:DONE|COMPLETE|LOCKED|APPROVED|PASS|PASSED|ASSIGNED|STARTED|ANSWERED|"
                     r"RESOLVED|SELECTED|INITIALIZED|IDENTIFIED|APPLIED|VERIFIED|IMPLEMENTED|TESTED|PREPPED|UPDATED|"
                     r"SNAPSHOT|GENERATED|DECISION|OK|REPRODUCED)|CONVERGED)`")


@check
def gates_defined():
    """Every gate a command or skill names exists in the project ledger or the per-work gates template."""
    defined = set()
    for src in (os.path.join(ROOT, "templates", "bequite", "state", "WORKFLOW_GATES.md"),
                os.path.join(ROOT, "templates", "bequite", "work", "_template", "gates.md")):
        defined |= set(GATE_RE.findall(read(src)))
    errors = []
    files = commands() + glob.glob(os.path.join(SKILL_DIR, "bequite-*", "**", "*.md"), recursive=True)
    for path in files:
        for n, line in enumerate(read(path).splitlines(), 1):
            for g in GATE_RE.findall(line):
                if g not in defined:
                    errors.append("%s:%d: gate `%s` is not defined in WORKFLOW_GATES.md or work/_template/gates.md" % (rel(path), n, g))
    return errors


def main(argv):
    if "--fix" in argv:
        what = [a for a in argv if not a.startswith("-")]
        if "contract" in what:
            fix_contract()
        return 0
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
