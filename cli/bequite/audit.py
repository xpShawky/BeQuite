"""bequite audit — Constitution + Doctrine drift detector.

BeQuite-unique. Walks Iron Laws (Constitution v1.0.1) + active Doctrines + accepted
ADRs against the codebase. Surfaces findings with file:line + suggested fix.

Rule packs:
- Iron Laws (always-on): Article I (spec supremacy), III (memory), IV (security &
  destruction), V (scale honesty), VII (hallucination defense).
- Doctrine packs (loaded per state/project.yaml::active_doctrines).

Implementation is rule-based — each rule is a function that yields Finding objects.
No regex-on-everything; the rules are deliberately narrow + explainable.

Cross-references:
- skill/hooks/posttooluse-audit.sh (lightweight per-edit subset; this is the full
  scan).
- .github/workflows/audit.yml (CI mode; posts findings as PR review).

Pre-CLI usage (v0.4.2 → v0.5.0):
    python -m cli.bequite.audit                  # full scan
    python -m cli.bequite.audit --rule article-iv-secrets
    python -m cli.bequite.audit --doctrine default-web-saas
    python -m cli.bequite.audit --ci             # CI mode; markdown table
    python -m cli.bequite.audit --json           # machine-readable
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Iterator

# tomllib is stdlib in Python 3.11+
try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]


# ----------------------------------------------------------------------------
# Domain types
# ----------------------------------------------------------------------------

SEVERITY_BLOCK = "block"
SEVERITY_WARN = "warn"
SEVERITY_RECOMMEND = "recommend"


@dataclass(frozen=True)
class Finding:
    rule_id: str        # e.g. "iron-law-iv-secrets"
    severity: str       # SEVERITY_BLOCK | SEVERITY_WARN | SEVERITY_RECOMMEND
    file: str           # repo-relative path
    line: int           # 1-based; 0 = not-line-specific
    statement: str      # human-readable rule statement
    found: str          # the matched text (trimmed)
    suggest: str        # remediation
    why: str            # Iron Law / Doctrine reference

    def to_dict(self) -> dict:
        return asdict(self)

    def render_markdown(self) -> str:
        return (
            f"- **[{self.severity}]** `{self.file}:{self.line}` "
            f"— **{self.rule_id}**\n"
            f"  - Statement: {self.statement}\n"
            f"  - Found: `{self.found}`\n"
            f"  - Suggest: {self.suggest}\n"
            f"  - Why: {self.why}\n"
        )


@dataclass
class AuditConfig:
    repo_root: Path
    active_doctrines: list[str] = field(default_factory=list)
    mode: str = "safe"
    scale_tier: str = "library_tool"
    package_allowlist: set[str] = field(default_factory=set)
    rule_filter: str | None = None       # if set, only run matching rule
    doctrine_filter: str | None = None   # if set, only run matching doctrine pack
    ci_mode: bool = False
    json_output: bool = False


# ----------------------------------------------------------------------------
# Helpers — file discovery
# ----------------------------------------------------------------------------

EXCLUDED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", "target", ".next", ".turbo",
    ".bequite/cache", ".bequite/.keys",
    "evidence", ".bequite/memory/prompts",   # snapshots: read-only history
}


def iter_repo_files(repo_root: Path, suffixes: tuple[str, ...] | None = None) -> Iterator[Path]:
    """Yield every tracked file under repo_root, skipping EXCLUDED_DIRS."""
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        # Skip if any path component matches an excluded dir.
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if suffixes and path.suffix not in suffixes:
            continue
        yield path


def file_line_iter(path: Path) -> Iterator[tuple[int, str]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, start=1):
                yield line_no, line.rstrip("\n")
    except (OSError, UnicodeDecodeError):
        return


# ----------------------------------------------------------------------------
# Iron Law IV — Security & destruction
# ----------------------------------------------------------------------------

# A subset of patterns from skill/hooks/pretooluse-secret-scan.sh — we re-grep
# the committed tree (the hook only catches in-flight Edit/Write).
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws-akia",        re.compile(r"(?:^|[^A-Z0-9])AKIA[0-9A-Z]{16}(?:[^A-Z0-9]|$)")),
    ("github-token",    re.compile(r"\bgh[posru]_[A-Za-z0-9]{36,}\b")),
    ("anthropic-key",   re.compile(r"\bsk-ant-[A-Za-z0-9_-]{50,}\b")),
    ("openai-key",      re.compile(r"\bsk-proj-[A-Za-z0-9_-]{40,}\b")),
    ("stripe-restricted", re.compile(r"\brk_(live|test)_[A-Za-z0-9]{24,}\b")),
    ("slack-token",     re.compile(r"\bxox[bopsa]-[0-9]+-[0-9]+-[A-Za-z0-9]+\b")),
    ("google-api",      re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("jwt",             re.compile(r"\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
    ("ssh-private",     re.compile(r"-----BEGIN (RSA|OPENSSH|DSA|EC|PGP) PRIVATE KEY-----")),
]


def rule_iron_law_iv_secrets(config: AuditConfig) -> Iterator[Finding]:
    """Article IV — secrets in committed source."""
    for path in iter_repo_files(config.repo_root):
        # Skip our own audit code (contains the patterns).
        if path.name == "audit.py":
            continue
        # Skip hook scripts that legitimately *contain* the patterns as detectors.
        if "pretooluse-secret-scan" in path.name:
            continue
        for line_no, line in file_line_iter(path):
            for kind, pattern in SECRET_PATTERNS:
                m = pattern.search(line)
                if m:
                    yield Finding(
                        rule_id=f"iron-law-iv-secrets/{kind}",
                        severity=SEVERITY_BLOCK,
                        file=str(path.relative_to(config.repo_root)).replace("\\", "/"),
                        line=line_no,
                        statement="No secrets in committed source (Iron Law IV).",
                        found=m.group(0)[:80],
                        suggest=(
                            "Replace with env-var reference (e.g. process.env.X / "
                            "os.getenv('X')). Use Doppler / Vault / AWS Secrets "
                            "Manager / 1Password Connect for secret storage."
                        ),
                        why="Constitution v1.0.1 Article IV; OWASP Top 10 A02 (Cryptographic Failures).",
                    )


def rule_iron_law_iv_env_reads(config: AuditConfig) -> Iterator[Finding]:
    """Article IV — code reading .env* files directly."""
    pattern = re.compile(
        r"(?:fs\.read|open|read_text|readFile|readFileSync|Path\([^)]+\)\.read|with\s+open)"
        r"[^)]*['\"][^'\"]*\.env",
        re.IGNORECASE,
    )
    for path in iter_repo_files(
        config.repo_root,
        suffixes=(".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".rs", ".go"),
    ):
        for line_no, line in file_line_iter(path):
            if pattern.search(line):
                yield Finding(
                    rule_id="iron-law-iv-env-reads",
                    severity=SEVERITY_BLOCK,
                    file=str(path.relative_to(config.repo_root)).replace("\\", "/"),
                    line=line_no,
                    statement="Never read .env* files directly (Iron Law IV).",
                    found=line.strip()[:120],
                    suggest=(
                        "Use the framework's env loader (Next.js process.env, "
                        "FastAPI Pydantic Settings, Django settings, etc.) which "
                        "reads from process env at boot — not from disk in code."
                    ),
                    why="Constitution v1.0.1 Article IV.",
                )


# ----------------------------------------------------------------------------
# Doctrine: default-web-saas
# ----------------------------------------------------------------------------

INTER_PATTERN = re.compile(r"font-family\s*:\s*['\"]?Inter\b", re.IGNORECASE)


def rule_default_web_saas_inter_without_reason(config: AuditConfig) -> Iterator[Finding]:
    """default-web-saas Rule 2 — recorded design choice; Inter requires a comment."""
    if "default-web-saas" not in config.active_doctrines:
        return
    for path in iter_repo_files(
        config.repo_root,
        suffixes=(".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte"),
    ):
        relstr = str(path.relative_to(config.repo_root)).replace("\\", "/")
        if "tokens" in relstr or "theme" in relstr:
            continue
        prev_line = ""
        for line_no, line in file_line_iter(path):
            if INTER_PATTERN.search(line):
                # Check if the immediately preceding line has a comment with WHY/why/reason.
                if not re.search(r"(?i)(why|reason|design|chose)", prev_line):
                    yield Finding(
                        rule_id="default-web-saas-rule-2-inter-no-reason",
                        severity=SEVERITY_WARN,
                        file=relstr,
                        line=line_no,
                        statement=(
                            "Font choice must be a deliberate, recorded decision "
                            "(Doctrine default-web-saas Rule 2). Inter is allowed but only "
                            "with a recorded reason."
                        ),
                        found=line.strip()[:120],
                        suggest=(
                            "Add a comment one line above explaining WHY this font fits "
                            "this product (e.g. \"// Why: Linear/Vercel/Stripe-class "
                            "neutrality is the brand voice.\")."
                        ),
                        why="default-web-saas Rule 2; Constitution v1.0.1 doctrine layer.",
                    )
            prev_line = line


NESTED_CARD_PATTERN = re.compile(
    r'<\w+[^>]*\bclassName=["\'][^"\']*\bcard\b[^"\']*["\'][^>]*>'
    r'(?:[^<]|<(?!\/\w+>))*'
    r'<\w+[^>]*\bclassName=["\'][^"\']*\bcard\b',
    re.DOTALL,
)


def rule_default_web_saas_nested_cards(config: AuditConfig) -> Iterator[Finding]:
    """default-web-saas Rule 4 — no nested cards."""
    if "default-web-saas" not in config.active_doctrines:
        return
    for path in iter_repo_files(
        config.repo_root,
        suffixes=(".tsx", ".jsx", ".vue", ".svelte", ".html"),
    ):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in NESTED_CARD_PATTERN.finditer(content):
            line_no = content[: m.start()].count("\n") + 1
            yield Finding(
                rule_id="default-web-saas-rule-4-nested-cards",
                severity=SEVERITY_BLOCK,
                file=str(path.relative_to(config.repo_root)).replace("\\", "/"),
                line=line_no,
                statement="A .card must not contain another .card (Doctrine default-web-saas Rule 4).",
                found=m.group(0)[:120].replace("\n", " "),
                suggest="Use sections, dividers, or layout grids instead of nested cards.",
                why="Doctrine default-web-saas Rule 4; AI-slop tell.",
            )


# ----------------------------------------------------------------------------
# Doctrine: library-package
# ----------------------------------------------------------------------------

TELEMETRY_FETCH_PATTERN = re.compile(
    r"fetch\s*\(\s*['\"]https?://[^'\"]*"
    r"(telemetry|analytics|track|metrics|usage|stats)",
    re.IGNORECASE,
)


def rule_library_package_telemetry_opt_in(config: AuditConfig) -> Iterator[Finding]:
    """library-package Rule 7 — telemetry must be opt-in only."""
    if "library-package" not in config.active_doctrines:
        return
    for path in iter_repo_files(
        config.repo_root,
        suffixes=(".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py"),
    ):
        # Skip BeQuite's own audit/freshness/cost code.
        relstr = str(path.relative_to(config.repo_root)).replace("\\", "/")
        if "cli/bequite/" in relstr or "tests/" in relstr:
            continue
        for line_no, line in file_line_iter(path):
            if TELEMETRY_FETCH_PATTERN.search(line):
                yield Finding(
                    rule_id="library-package-rule-7-telemetry",
                    severity=SEVERITY_BLOCK,
                    file=relstr,
                    line=line_no,
                    statement=(
                        "Telemetry must be opt-in only "
                        "(Doctrine library-package Rule 7)."
                    ),
                    found=line.strip()[:120],
                    suggest=(
                        "Gate the fetch behind a config flag the user sets "
                        "explicitly (config.telemetry === 'enabled'). Document "
                        "what's collected. Default OFF."
                    ),
                    why="Doctrine library-package Rule 7; Constitution v1.0.1 doctrine layer.",
                )


# ----------------------------------------------------------------------------
# Doctrine: ai-automation
# ----------------------------------------------------------------------------


def rule_ai_automation_secrets_in_flow_json(config: AuditConfig) -> Iterator[Finding]:
    """ai-automation Rule 4 — secrets via connector / env, never in flow JSON."""
    if "ai-automation" not in config.active_doctrines:
        return
    flow_dirs = [
        config.repo_root / ".n8n" / "workflows",
        config.repo_root / "scenarios",
        config.repo_root / "zaps",
        config.repo_root / "workflows",
        config.repo_root / "inngest",
    ]
    for d in flow_dirs:
        if not d.is_dir():
            continue
        for path in d.rglob("*.json"):
            for line_no, line in file_line_iter(path):
                for kind, pattern in SECRET_PATTERNS:
                    m = pattern.search(line)
                    if m:
                        yield Finding(
                            rule_id=f"ai-automation-rule-4-flow-secret/{kind}",
                            severity=SEVERITY_BLOCK,
                            file=str(path.relative_to(config.repo_root)).replace("\\", "/"),
                            line=line_no,
                            statement=(
                                "Workflow JSON must reference credentials by ID, "
                                "never contain secret values "
                                "(Doctrine ai-automation Rule 4)."
                            ),
                            found=m.group(0)[:80],
                            suggest=(
                                "Move the secret to the platform's credential store "
                                "(n8n Credentials / Make Connections / Zapier auth / "
                                "Temporal secret store / env). Reference by ID."
                            ),
                            why="Doctrine ai-automation Rule 4; Iron Law IV.",
                        )


def rule_ai_automation_workflows_committed(config: AuditConfig) -> Iterator[Finding]:
    """ai-automation Rule 1 — workflows are version-controlled source code."""
    if "ai-automation" not in config.active_doctrines:
        return
    flow_dirs = [".n8n/workflows", "scenarios", "zaps", "workflows", "inngest"]
    found_any = False
    for d in flow_dirs:
        if (config.repo_root / d).is_dir():
            files = list((config.repo_root / d).rglob("*"))
            if any(p.is_file() for p in files):
                found_any = True
                break
    if not found_any:
        yield Finding(
            rule_id="ai-automation-rule-1-no-flows-committed",
            severity=SEVERITY_WARN,
            file="(repo root)",
            line=0,
            statement=(
                "No flow / scenario / zap / workflow JSON files found in any of "
                ".n8n/workflows/, scenarios/, zaps/, workflows/, inngest/."
            ),
            found="(none)",
            suggest=(
                "Export your workflow(s) from the platform UI to JSON and commit "
                "them. The platform UI is for visualisation, not authoritative storage."
            ),
            why="Doctrine ai-automation Rule 1.",
        )


# ----------------------------------------------------------------------------
# Rule registry
# ----------------------------------------------------------------------------

RULES: list[tuple[str, str, Callable[[AuditConfig], Iterator[Finding]]]] = [
    # (rule_id, doctrine_or_iron_law, function)
    ("iron-law-iv-secrets", "iron-law", rule_iron_law_iv_secrets),
    ("iron-law-iv-env-reads", "iron-law", rule_iron_law_iv_env_reads),
    ("default-web-saas-rule-2", "default-web-saas", rule_default_web_saas_inter_without_reason),
    ("default-web-saas-rule-4", "default-web-saas", rule_default_web_saas_nested_cards),
    ("library-package-rule-7", "library-package", rule_library_package_telemetry_opt_in),
    ("ai-automation-rule-1", "ai-automation", rule_ai_automation_workflows_committed),
    ("ai-automation-rule-4", "ai-automation", rule_ai_automation_secrets_in_flow_json),
]


# ----------------------------------------------------------------------------
# Config loader
# ----------------------------------------------------------------------------


def load_audit_config(repo_root: Path, args: argparse.Namespace) -> AuditConfig:
    """Build AuditConfig from state/project.yaml / bequite.config.toml + CLI args."""
    active_doctrines: list[str] = []
    mode = "safe"
    scale_tier = "library_tool"

    # Try state/project.yaml (fields are simple key=value or YAML).
    project_yaml = repo_root / "state" / "project.yaml"
    if project_yaml.exists():
        text = project_yaml.read_text(encoding="utf-8", errors="replace")
        # Extract `active_doctrines` block (best-effort YAML-lite).
        m = re.search(r"^\s*active_doctrines\s*:\s*((?:\n\s+-\s+\S+)+)", text, re.MULTILINE)
        if m:
            active_doctrines = re.findall(r"-\s+(\S+)", m.group(1))
        m = re.search(r"^\s*mode\s*:\s*(\S+)", text, re.MULTILINE)
        if m:
            mode = m.group(1).strip()
        m = re.search(r"^\s*scale_tier\s*:\s*(\S+)", text, re.MULTILINE)
        if m:
            scale_tier = m.group(1).strip()

    # Try bequite.config.toml as fallback.
    config_toml = repo_root / ".bequite" / "bequite.config.toml"
    if config_toml.exists():
        try:
            with config_toml.open("rb") as f:
                cfg = tomllib.load(f)
            project = cfg.get("project", {})
            if not active_doctrines:
                active_doctrines = project.get("doctrines", []) or []
            if mode == "safe":
                mode = project.get("mode", "safe")
            if scale_tier == "library_tool":
                scale_tier = project.get("scale_tier", "library_tool")
        except Exception:
            pass

    # CLI override.
    if args.doctrine:
        active_doctrines = [args.doctrine]

    return AuditConfig(
        repo_root=repo_root,
        active_doctrines=active_doctrines,
        mode=mode,
        scale_tier=scale_tier,
        rule_filter=args.rule,
        doctrine_filter=args.doctrine,
        ci_mode=args.ci,
        json_output=args.json,
    )


# ----------------------------------------------------------------------------
# Runner
# ----------------------------------------------------------------------------


def run_audit(config: AuditConfig) -> list[Finding]:
    findings: list[Finding] = []
    for rule_id, scope, fn in RULES:
        if config.rule_filter and config.rule_filter not in rule_id:
            continue
        if config.doctrine_filter and scope not in (config.doctrine_filter, "iron-law"):
            continue
        findings.extend(fn(config))
    return findings


def render_console(findings: list[Finding]) -> str:
    if not findings:
        return "[bequite audit] PASS — zero findings."
    lines = [f"[bequite audit] {len(findings)} finding(s):\n"]
    by_severity: dict[str, list[Finding]] = {}
    for f in findings:
        by_severity.setdefault(f.severity, []).append(f)
    for severity in (SEVERITY_BLOCK, SEVERITY_WARN, SEVERITY_RECOMMEND):
        for f in by_severity.get(severity, []):
            lines.append(f.render_markdown())
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bequite audit",
        description=(
            "Constitution + Doctrine drift detector. Walks Iron Laws + active "
            "Doctrines + accepted ADRs against the codebase. Surfaces findings."
        ),
    )
    parser.add_argument("--repo", default=".", help="repo root (default: cwd)")
    parser.add_argument("--rule", default=None, help="run only rules matching this substring")
    parser.add_argument("--doctrine", default=None, help="scope to one Doctrine (e.g. default-web-saas)")
    parser.add_argument("--ci", action="store_true", help="CI mode (markdown output, exit 1 on block)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve()
    config = load_audit_config(repo_root, args)
    findings = run_audit(config)

    if config.json_output:
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    else:
        print(render_console(findings))

    blocks = [f for f in findings if f.severity == SEVERITY_BLOCK]
    if blocks:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
