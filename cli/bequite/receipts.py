"""bequite receipts — Reproducibility receipts (v0.7.0).

A receipt is the auditable record of a single phase transition: the model that
ran, the input prompt + memory snapshot hashes, the output diff hash, the
tools invoked, the test exit codes, the cost, the active doctrines, the
constitution version, and a chain-pointer to the parent receipt.

Receipts let a future engineer (or an agent on the same project) reconstruct
*what was decided when, by which model, on which inputs, with which doctrines
active, against which constitution version*. Pair with `bequite cost` for
roll-ups; pair with `bequite verify-receipts` (v0.7.1) for ed25519 signing
+ chain validation.

Per Iron Law III (Memory discipline) and Iron Law VI (Honest reporting), every
phase transition emits a receipt. Receipts are append-only; superseding a
receipt requires emitting a NEW receipt with the old one as parent_receipt.

Storage: `.bequite/receipts/<receipt-sha>-<phase>.json` (sha is the receipt's
own canonical-JSON content-hash; collision-resistant; deterministic).

Module is runnable as `python -m bequite.receipts --help` from `cli/`. Once the
CLI thin wrapper (v0.5.0) is upgraded to dispatch this module, the same surface
is available at `bequite receipts <subcommand>`.

CLI surface (v0.7.0):

    python -m bequite.receipts emit \\
        --phase P5 \\
        --model claude-opus-4-7 \\
        --prompt-file path/to/prompt.txt \\
        --memory-snapshot-dir .bequite/memory/ \\
        --diff-from HEAD~1 --diff-to HEAD \\
        --doctrines default-web-saas,vibe-defense \\
        --constitution-version 1.2.0 \\
        --input-tokens 12345 --output-tokens 678 --usd 0.034

    python -m bequite.receipts list           # all receipts in chain order
    python -m bequite.receipts show <sha>     # full receipt JSON
    python -m bequite.receipts validate-chain # walk parent_receipt links
    python -m bequite.receipts roll-up        # by session / phase / day

Compatibility: emits stable JSON; schema versioned via `version` field; v1
established here. Future versions will be additive (new optional fields)
unless an Article-III-grade ADR drives a breaking bump.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import uuid
from collections import defaultdict
from typing import Any, Literal, Optional

# Use stdlib + dataclasses to keep this module importable even without pydantic
# at runtime. The cli/pyproject.toml dependency on pydantic >= 2.7 is for the
# config layer; receipts can run cleanly without pydantic.

SCHEMA_VERSION = "1"
PHASE_LITERAL = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]
DEFAULT_STORAGE_DIR = ".bequite/receipts"


# --------------------------------------------------------------------- schema


@dataclasses.dataclass
class Model:
    name: str
    reasoning_effort: str = "default"  # high / default / low / xhigh
    fallback_model: Optional[str] = None


@dataclasses.dataclass
class InputBlock:
    prompt_hash: str  # sha256:...
    memory_snapshot_hash: str  # sha256:...


@dataclasses.dataclass
class OutputBlock:
    diff_hash: str  # sha256:...
    files_touched: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ToolInvocation:
    name: str
    args_hash: str  # sha256:...
    exit: int


@dataclasses.dataclass
class TestsBlock:
    command: str
    exit: int
    stdout_hash: str  # sha256:...


@dataclasses.dataclass
class CostBlock:
    input_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0


@dataclasses.dataclass
class Receipt:
    """v1 receipt schema. Add fields only via additive ADR-graded changes."""

    version: str
    session_id: str
    phase: str
    timestamp_utc: str
    model: Model
    input: InputBlock
    output: OutputBlock
    tools_invoked: list[ToolInvocation] = dataclasses.field(default_factory=list)
    tests: Optional[TestsBlock] = None
    cost: CostBlock = dataclasses.field(default_factory=CostBlock)
    doctrine: list[str] = dataclasses.field(default_factory=list)
    constitution_version: str = "1.0.0"
    parent_receipt: Optional[str] = None  # sha256:... of parent receipt's content_hash
    # Future-extension fields go HERE, all Optional with defaults.

    def to_canonical_dict(self) -> dict[str, Any]:
        """Canonical dict for hashing — sorted keys, no whitespace variation."""
        d = dataclasses.asdict(self)
        # Drop Nones in nested dicts so canonical hash isn't sensitive to
        # missing-vs-null distinction.
        return _strip_none(d)

    def content_hash(self) -> str:
        """Deterministic sha256 of canonical-JSON encoding. Used as filename + chain pointer."""
        canon = json.dumps(self.to_canonical_dict(), sort_keys=True, separators=(",", ":"))
        return "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _strip_none(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: _strip_none(v) for k, v in d.items() if v is not None}
    if isinstance(d, list):
        return [_strip_none(x) for x in d]
    return d


# --------------------------------------------------------------------- hashing


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_dir(path: pathlib.Path) -> str:
    """Sum sha256 of every file under path, sorted, then sha256 of the sums.

    Stable across OS path separators; ignores .git, __pycache__, .venv, node_modules.
    """
    skip = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache", ".mypy_cache"}
    parts: list[str] = []
    for p in sorted(path.rglob("*")):
        if not p.is_file():
            continue
        # Skip any path that contains a skipped directory component
        if any(seg in skip for seg in p.parts):
            continue
        rel = p.relative_to(path).as_posix()
        parts.append(f"{rel}:{sha256_file(p)}")
    combined = "\n".join(parts)
    return sha256_str(combined)


def diff_hash_from_git(diff_from: str, diff_to: str, cwd: Optional[pathlib.Path] = None) -> tuple[str, list[str]]:
    """Run git diff <from> <to> and return (sha256-of-patch, files-touched).

    Returns ("sha256:" + hash, [file1, file2, ...]). On git failure, returns
    ("sha256:UNAVAILABLE", []) without raising — receipts on systems without
    git history (e.g. fresh init) still emit, just with a sentinel.
    """
    try:
        proc = subprocess.run(
            ["git", "diff", "--no-color", f"{diff_from}..{diff_to}"],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        )
        diff_text = proc.stdout
        files = subprocess.run(
            ["git", "diff", "--name-only", f"{diff_from}..{diff_to}"],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        ).stdout.strip().splitlines()
        return (sha256_str(diff_text), files)
    except (FileNotFoundError, subprocess.SubprocessError):
        return ("sha256:UNAVAILABLE", [])


# --------------------------------------------------------------------- storage


class ReceiptStore:
    def __init__(self, storage_dir: str = DEFAULT_STORAGE_DIR):
        self.path = pathlib.Path(storage_dir)
        self.path.mkdir(parents=True, exist_ok=True)

    def write(self, receipt: Receipt) -> pathlib.Path:
        """Write the receipt as JSON. Filename = <hash>-<phase>.json."""
        h = receipt.content_hash().split(":")[1]  # strip the sha256: prefix
        filename = f"{h}-{receipt.phase}.json"
        target = self.path / filename
        canonical = receipt.to_canonical_dict()
        target.write_text(json.dumps(canonical, indent=2, sort_keys=True), encoding="utf-8")
        return target

    def list_all(self) -> list[Receipt]:
        receipts: list[Receipt] = []
        for f in sorted(self.path.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                receipts.append(_dict_to_receipt(d))
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"warning: skipping malformed receipt at {f}: {e}", file=sys.stderr)
        return receipts

    def get(self, content_hash: str) -> Optional[Receipt]:
        h = content_hash.split(":", 1)[-1]
        for f in self.path.glob(f"{h}-*.json"):
            return _dict_to_receipt(json.loads(f.read_text(encoding="utf-8")))
        return None


def _dict_to_receipt(d: dict[str, Any]) -> Receipt:
    """Defensive deserialization."""
    return Receipt(
        version=d.get("version", SCHEMA_VERSION),
        session_id=d["session_id"],
        phase=d["phase"],
        timestamp_utc=d["timestamp_utc"],
        model=Model(**d["model"]),
        input=InputBlock(**d["input"]),
        output=OutputBlock(**d["output"]),
        tools_invoked=[ToolInvocation(**t) for t in d.get("tools_invoked", [])],
        tests=TestsBlock(**d["tests"]) if d.get("tests") else None,
        cost=CostBlock(**d.get("cost", {})),
        doctrine=d.get("doctrine", []),
        constitution_version=d.get("constitution_version", "1.0.0"),
        parent_receipt=d.get("parent_receipt"),
    )


# --------------------------------------------------------------------- chain


def validate_chain(receipts: list[Receipt]) -> tuple[bool, list[str]]:
    """Walk parent_receipt links. Return (ok, list-of-issues).

    Validation rules:
    1. Every parent_receipt reference must point to an existing receipt.
    2. The chain has no cycles (a receipt cannot transitively reference itself).
    3. Each parent's timestamp must be ≤ child's timestamp (causality —
       allowing equality so receipts emitted in the same second pass).
    """
    issues: list[str] = []
    by_hash = {r.content_hash(): r for r in receipts}

    for r in receipts:
        if r.parent_receipt is None:
            continue
        if r.parent_receipt not in by_hash:
            issues.append(
                f"receipt {r.content_hash()} (phase {r.phase}) "
                f"references missing parent {r.parent_receipt}"
            )
            continue
        parent = by_hash[r.parent_receipt]
        if parent.timestamp_utc > r.timestamp_utc:
            issues.append(
                f"receipt {r.content_hash()} (phase {r.phase}, ts {r.timestamp_utc}) "
                f"references parent {r.parent_receipt} (ts {parent.timestamp_utc}) "
                f"that has a LATER timestamp — causality violation"
            )

    # Cycle detection — walk the parent chain from each receipt.
    for r in receipts:
        seen: set[str] = set()
        cur: Optional[Receipt] = r
        while cur is not None:
            ch = cur.content_hash()
            if ch in seen:
                issues.append(f"cycle detected at {ch} (phase {cur.phase})")
                break
            seen.add(ch)
            cur = by_hash.get(cur.parent_receipt) if cur.parent_receipt else None

    return (len(issues) == 0, issues)


# --------------------------------------------------------------------- roll-up


def roll_up_by_session(receipts: list[Receipt]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "phases": [],
        "input_tokens": 0,
        "output_tokens": 0,
        "usd": 0.0,
        "first_timestamp_utc": None,
        "last_timestamp_utc": None,
        "doctrines": set(),
    })
    for r in receipts:
        bucket = grouped[r.session_id]
        bucket["phases"].append(r.phase)
        bucket["input_tokens"] += r.cost.input_tokens
        bucket["output_tokens"] += r.cost.output_tokens
        bucket["usd"] += r.cost.usd
        bucket["doctrines"].update(r.doctrine)
        if bucket["first_timestamp_utc"] is None or r.timestamp_utc < bucket["first_timestamp_utc"]:
            bucket["first_timestamp_utc"] = r.timestamp_utc
        if bucket["last_timestamp_utc"] is None or r.timestamp_utc > bucket["last_timestamp_utc"]:
            bucket["last_timestamp_utc"] = r.timestamp_utc

    # Convert sets → sorted lists for JSON-serializability.
    for s in grouped.values():
        s["doctrines"] = sorted(s["doctrines"])
    return dict(grouped)


def roll_up_by_phase(receipts: list[Receipt]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "count": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "usd": 0.0,
    })
    for r in receipts:
        bucket = grouped[r.phase]
        bucket["count"] += 1
        bucket["input_tokens"] += r.cost.input_tokens
        bucket["output_tokens"] += r.cost.output_tokens
        bucket["usd"] += r.cost.usd
    return dict(grouped)


def roll_up_by_day(receipts: list[Receipt]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "count": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "usd": 0.0,
    })
    for r in receipts:
        # Use just the date portion of ISO timestamp.
        day = r.timestamp_utc.split("T")[0]
        bucket = grouped[day]
        bucket["count"] += 1
        bucket["input_tokens"] += r.cost.input_tokens
        bucket["output_tokens"] += r.cost.output_tokens
        bucket["usd"] += r.cost.usd
    return dict(grouped)


# --------------------------------------------------------------------- emitter


def make_receipt(
    *,
    phase: str,
    model_name: str,
    reasoning_effort: str,
    prompt: str,
    memory_snapshot_dir: pathlib.Path,
    diff_from: str,
    diff_to: str,
    doctrines: list[str],
    constitution_version: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    usd: float = 0.0,
    tools_invoked: Optional[list[ToolInvocation]] = None,
    tests: Optional[TestsBlock] = None,
    parent_receipt: Optional[str] = None,
    session_id: Optional[str] = None,
    fallback_model: Optional[str] = None,
    cwd: Optional[pathlib.Path] = None,
) -> Receipt:
    """Construct a Receipt with computed hashes from inputs.

    The constructor:
    - hashes the prompt text directly
    - sha256-of-files-and-paths the memory snapshot dir (skipping .git/etc)
    - runs git diff for output and gathers files-touched
    - generates a UUID session_id if none provided
    - stamps the current UTC time
    """
    if phase not in PHASE_LITERAL:
        raise ValueError(f"phase must be one of {PHASE_LITERAL}, got {phase!r}")

    diff_h, files_touched = diff_hash_from_git(diff_from, diff_to, cwd=cwd)

    return Receipt(
        version=SCHEMA_VERSION,
        session_id=session_id or str(uuid.uuid4()),
        phase=phase,
        timestamp_utc=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        model=Model(name=model_name, reasoning_effort=reasoning_effort, fallback_model=fallback_model),
        input=InputBlock(
            prompt_hash=sha256_str(prompt),
            memory_snapshot_hash=sha256_dir(memory_snapshot_dir),
        ),
        output=OutputBlock(diff_hash=diff_h, files_touched=files_touched),
        tools_invoked=tools_invoked or [],
        tests=tests,
        cost=CostBlock(input_tokens=input_tokens, output_tokens=output_tokens, usd=usd),
        doctrine=doctrines,
        constitution_version=constitution_version,
        parent_receipt=parent_receipt,
    )


# --------------------------------------------------------------------- replay


def replay_check(receipt: Receipt, prompt: str, memory_snapshot_dir: pathlib.Path) -> tuple[bool, list[str]]:
    """Confirm the receipt's recorded hashes match a re-derived prompt + memory snapshot.

    Used by tests + by `bequite verify-receipts` (v0.7.1) to confirm a receipt's
    inputs reproduce. Doesn't verify the output diff (that requires git history
    intact); for output-replay use git diff against the recorded diff_hash.
    """
    issues: list[str] = []
    p_hash = sha256_str(prompt)
    m_hash = sha256_dir(memory_snapshot_dir)
    if p_hash != receipt.input.prompt_hash:
        issues.append(f"prompt_hash mismatch: recorded={receipt.input.prompt_hash} recomputed={p_hash}")
    if m_hash != receipt.input.memory_snapshot_hash:
        issues.append(f"memory_snapshot_hash mismatch: recorded={receipt.input.memory_snapshot_hash} recomputed={m_hash}")
    return (len(issues) == 0, issues)


# --------------------------------------------------------------------- CLI


def _emit_cmd(args: argparse.Namespace) -> int:
    prompt_text = pathlib.Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else (args.prompt or "")
    if not prompt_text:
        print("error: --prompt-file or --prompt required", file=sys.stderr)
        return 2

    memory_dir = pathlib.Path(args.memory_snapshot_dir)
    if not memory_dir.exists():
        print(f"error: memory_snapshot_dir does not exist: {memory_dir}", file=sys.stderr)
        return 2

    r = make_receipt(
        phase=args.phase,
        model_name=args.model,
        reasoning_effort=args.reasoning_effort,
        prompt=prompt_text,
        memory_snapshot_dir=memory_dir,
        diff_from=args.diff_from,
        diff_to=args.diff_to,
        doctrines=[d.strip() for d in (args.doctrines or "").split(",") if d.strip()],
        constitution_version=args.constitution_version,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        usd=args.usd,
        parent_receipt=args.parent_receipt,
        session_id=args.session_id,
        fallback_model=args.fallback_model,
    )

    store = ReceiptStore(args.storage_dir)
    target = store.write(r)
    print(f"emitted receipt {r.content_hash()} → {target}")
    return 0


def _list_cmd(args: argparse.Namespace) -> int:
    store = ReceiptStore(args.storage_dir)
    receipts = store.list_all()
    if not receipts:
        print(f"(no receipts in {args.storage_dir})")
        return 0
    for r in sorted(receipts, key=lambda x: x.timestamp_utc):
        h = r.content_hash().split(":")[1][:10]
        print(f"{r.timestamp_utc}  {r.phase}  {h}…  {r.model.name}  ${r.cost.usd:.4f}  ({r.session_id[:8]}…)")
    return 0


def _show_cmd(args: argparse.Namespace) -> int:
    store = ReceiptStore(args.storage_dir)
    r = store.get(args.sha)
    if r is None:
        print(f"error: no receipt with hash {args.sha}", file=sys.stderr)
        return 2
    print(json.dumps(r.to_canonical_dict(), indent=2, sort_keys=True))
    return 0


def _validate_chain_cmd(args: argparse.Namespace) -> int:
    store = ReceiptStore(args.storage_dir)
    receipts = store.list_all()
    if not receipts:
        print(f"(no receipts in {args.storage_dir})")
        return 0
    ok, issues = validate_chain(receipts)
    if ok:
        print(f"chain valid — {len(receipts)} receipt(s)")
        return 0
    print(f"chain INVALID — {len(issues)} issue(s):", file=sys.stderr)
    for i in issues:
        print(f"  • {i}", file=sys.stderr)
    return 1


def _roll_up_cmd(args: argparse.Namespace) -> int:
    store = ReceiptStore(args.storage_dir)
    receipts = store.list_all()
    if not receipts:
        print(f"(no receipts in {args.storage_dir})")
        return 0
    by = args.by
    if by == "session":
        out = roll_up_by_session(receipts)
    elif by == "phase":
        out = roll_up_by_phase(receipts)
    elif by == "day":
        out = roll_up_by_day(receipts)
    else:
        print(f"error: --by must be session|phase|day, got {by!r}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-receipts", description="Reproducibility receipts (BeQuite v0.7.0).")
    p.add_argument("--storage-dir", default=os.environ.get("BEQUITE_RECEIPTS_DIR", DEFAULT_STORAGE_DIR))

    sub = p.add_subparsers(dest="cmd", required=True)

    # emit
    e = sub.add_parser("emit", help="Emit a new receipt for a phase transition.")
    e.add_argument("--phase", required=True, choices=PHASE_LITERAL)
    e.add_argument("--model", required=True, help="Model name (e.g. claude-opus-4-7).")
    e.add_argument("--reasoning-effort", default="default", choices=["low", "default", "high", "xhigh"])
    e.add_argument("--fallback-model", default=None)
    e.add_argument("--prompt-file", default=None)
    e.add_argument("--prompt", default=None)
    e.add_argument("--memory-snapshot-dir", default=".bequite/memory/")
    e.add_argument("--diff-from", default="HEAD~1")
    e.add_argument("--diff-to", default="HEAD")
    e.add_argument("--doctrines", default="")
    e.add_argument("--constitution-version", default="1.2.0")
    e.add_argument("--input-tokens", type=int, default=0)
    e.add_argument("--output-tokens", type=int, default=0)
    e.add_argument("--usd", type=float, default=0.0)
    e.add_argument("--parent-receipt", default=None)
    e.add_argument("--session-id", default=None)
    e.set_defaults(fn=_emit_cmd)

    # list
    l = sub.add_parser("list", help="List all receipts in chain order.")
    l.set_defaults(fn=_list_cmd)

    # show
    s = sub.add_parser("show", help="Show a single receipt's JSON.")
    s.add_argument("sha", help="Receipt content hash (with or without 'sha256:' prefix).")
    s.set_defaults(fn=_show_cmd)

    # validate-chain
    v = sub.add_parser("validate-chain", help="Walk parent_receipt links; report any missing or out-of-order.")
    v.set_defaults(fn=_validate_chain_cmd)

    # roll-up
    r = sub.add_parser("roll-up", help="Cost / token roll-up by session, phase, or day.")
    r.add_argument("--by", default="session", choices=["session", "phase", "day"])
    r.set_defaults(fn=_roll_up_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
