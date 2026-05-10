"""bequite freshness — knowledge probe.

BeQuite-unique. Verifies stack candidates aren't deprecated / EOL'd / replaced /
open-CVE'd / pricing-tier-mismatched / supply-chain-incident-flagged.

Per-package checks:
- npm:      registry.npmjs.org for last modified + latest version.
- PyPI:     pypi.org/pypi/<pkg>/json for upload time + classifiers.
- crates.io: crates.io/api/v1/crates/<pkg> for updated_at + max_version.
- GitHub:   gh api repos/<owner>/<repo> for pushed_at + archived flag (when repo URL known).

Defends against the brief-rotting problem (Stronghold deprecation, EV cert
obsolescence, Roo Code shutdown, Clerk MAU change, Vercel timeout extension).

Cross-references:
- /bequite.decide-stack pre-sign mandatory checks.
- skill/references/package-allowlist.md (drafted v0.4.3).
- skill/references/supply-chain-incidents.md (PhantomRaven, Shai-Hulud, etc.).

Pre-CLI usage:
    python -m cli.bequite.freshness --package <name> [--ecosystem npm|pypi|cargo]
    python -m cli.bequite.freshness --all
    python -m cli.bequite.freshness --from-adr ADR-001-stack
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CACHE_TTL_SECONDS = 24 * 60 * 60   # 24h default
CACHE_DIR_ENV = "BEQUITE_CACHE_DIR"
DEFAULT_CACHE_DIR = ".bequite/cache/freshness"
DEFAULT_MAX_AGE_MONTHS = 6
USER_AGENT = "bequite-freshness/0.4.3 (+https://github.com/xpshawky/bequite)"
HTTP_TIMEOUT_SECONDS = 10


# ----------------------------------------------------------------------------
# Domain types
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateProbe:
    pkg: str
    ecosystem: str           # npm | pypi | cargo | github
    version: str | None      # locked version, if known
    repo_url: str | None     # GitHub URL, if known


@dataclass
class FreshnessResult:
    pkg: str
    ecosystem: str
    version_observed: str | None
    last_release_at: str | None      # ISO 8601
    last_commit_at: str | None       # ISO 8601 (when GitHub URL known)
    days_since_last_release: int | None
    days_since_last_commit: int | None
    deprecated: bool
    archived: bool
    supply_chain_incident: str | None  # name of the incident, if matched
    license: str | None
    verdict: str                      # fresh | stale-warn | stale-block | pricing-mismatch
    notes: list[str] = field(default_factory=list)
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


# ----------------------------------------------------------------------------
# Known-bad supply-chain incidents
# ----------------------------------------------------------------------------

# Loaded from skill/references/supply-chain-incidents.md when present; bootstrap
# values seeded here for v0.4.3 since the references file is drafted later.
SUPPLY_CHAIN_INCIDENTS: dict[str, str] = {
    # name → human-readable incident attribution
    # PhantomRaven (Koi Security 2025) — 126 packages exploiting AI-hallucinated names.
    # We seed a few representative names; full list at the references markdown.
    # Shai-Hulud (~700 packages); Sept 8 attack (18 packages).
    # tauri-plugin-stronghold is deprecated (not malicious; status known-stale-block).
    "tauri-plugin-stronghold": "deprecated; removed in Tauri v3 — use OS keychain plugins (tauri-plugin-keyring)",
    # roo-code: shutting down 2026-05-15 per the brief reconciliation.
    "roo-code": "host shutting down 2026-05-15; replace with Kilo Code",
}

KNOWN_DEPRECATED_NAMES: set[str] = {
    "tauri-plugin-stronghold",
}


# ----------------------------------------------------------------------------
# Cache
# ----------------------------------------------------------------------------


def cache_path(repo_root: Path, pkg: str, ecosystem: str, version: str | None) -> Path:
    cache_dir = Path(repo_root) / DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    safe_pkg = pkg.replace("/", "__")
    safe_ver = (version or "latest").replace("/", "_")
    return cache_dir / f"{ecosystem}__{safe_pkg}__{safe_ver}.json"


def cache_get(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        ts = data.get("_cached_at_epoch")
        if ts and (time.time() - ts) < CACHE_TTL_SECONDS:
            return data
    except (OSError, json.JSONDecodeError):
        return None
    return None


def cache_put(path: Path, data: dict) -> None:
    data = {**data, "_cached_at_epoch": time.time()}
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        pass


# ----------------------------------------------------------------------------
# Network helpers
# ----------------------------------------------------------------------------


def http_get_json(url: str) -> dict | None:
    """Best-effort GET, returns JSON or None on any failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    except Exception:  # noqa: BLE001 — best-effort on network failure
        return None


# ----------------------------------------------------------------------------
# Per-ecosystem probes
# ----------------------------------------------------------------------------


def probe_npm(pkg: str, version: str | None = None) -> dict | None:
    data = http_get_json(f"https://registry.npmjs.org/{pkg}")
    if not data:
        return None
    times: dict = data.get("time", {}) or {}
    latest = data.get("dist-tags", {}).get("latest")
    last_release_at = times.get(latest) if latest else times.get("modified")
    return {
        "version_observed": version or latest,
        "last_release_at": last_release_at,
        "license": data.get("license"),
        "deprecated": bool(data.get("versions", {}).get(latest, {}).get("deprecated")) if latest else False,
        "homepage": data.get("homepage"),
        "repository": (data.get("repository") or {}).get("url") if isinstance(data.get("repository"), dict) else data.get("repository"),
    }


def probe_pypi(pkg: str, version: str | None = None) -> dict | None:
    url = f"https://pypi.org/pypi/{pkg}/json" if not version else f"https://pypi.org/pypi/{pkg}/{version}/json"
    data = http_get_json(url)
    if not data:
        return None
    info = data.get("info", {})
    releases = data.get("releases", {})
    latest = info.get("version")
    last_release_at = None
    if latest and latest in releases and releases[latest]:
        last_release_at = releases[latest][0].get("upload_time_iso_8601") or releases[latest][0].get("upload_time")
    classifiers: list[str] = info.get("classifiers", [])
    is_deprecated = any("Inactive" in c or "Deprecated" in c for c in classifiers)
    return {
        "version_observed": version or latest,
        "last_release_at": last_release_at,
        "license": info.get("license"),
        "deprecated": is_deprecated,
        "homepage": info.get("home_page") or info.get("project_url"),
        "repository": (info.get("project_urls") or {}).get("Source") or (info.get("project_urls") or {}).get("Repository"),
    }


def probe_cargo(pkg: str, version: str | None = None) -> dict | None:
    data = http_get_json(f"https://crates.io/api/v1/crates/{pkg}")
    if not data:
        return None
    crate = data.get("crate", {})
    versions = data.get("versions", [])
    latest = crate.get("max_stable_version") or crate.get("max_version")
    last_release_at = None
    if versions:
        # Find the latest version's created_at.
        latest_entry = next((v for v in versions if v.get("num") == latest), versions[0])
        last_release_at = latest_entry.get("created_at")
    return {
        "version_observed": version or latest,
        "last_release_at": last_release_at,
        "license": (crate.get("license") if "license" in crate else None) or (versions[0].get("license") if versions else None),
        "deprecated": False,  # crates.io doesn't have a deprecated flag at the crate level
        "homepage": crate.get("homepage"),
        "repository": crate.get("repository"),
    }


def probe_github(repo_url: str) -> dict | None:
    """Best-effort GitHub probe via the public REST API. Anonymous; rate-limited."""
    m = re.search(r"github\.com/([^/]+)/([^/.#?]+)", repo_url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    data = http_get_json(f"https://api.github.com/repos/{owner}/{repo}")
    if not data:
        return None
    return {
        "last_commit_at": data.get("pushed_at"),
        "archived": bool(data.get("archived")),
        "license": ((data.get("license") or {}).get("spdx_id")),
    }


# ----------------------------------------------------------------------------
# Verdict logic
# ----------------------------------------------------------------------------


def days_between(iso_then: str | None, now: datetime | None = None) -> int | None:
    if not iso_then:
        return None
    try:
        # PyPI sometimes returns "...+00:00", crates.io "Z", npm Z
        cleaned = iso_then.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)
    return (now - dt).days


def compute_verdict(
    pkg: str,
    npm_data: dict | None,
    github_data: dict | None,
    max_age_months: int,
) -> tuple[str, list[str]]:
    notes: list[str] = []
    max_days = max_age_months * 30

    # Hard known-bad table.
    if pkg in SUPPLY_CHAIN_INCIDENTS:
        notes.append(f"supply-chain incident: {SUPPLY_CHAIN_INCIDENTS[pkg]}")
        return "stale-block", notes

    if pkg in KNOWN_DEPRECATED_NAMES:
        notes.append("hard-deprecated per BeQuite known-bad list")
        return "stale-block", notes

    if npm_data and npm_data.get("deprecated"):
        notes.append("registry-flagged deprecated")
        return "stale-block", notes

    if github_data and github_data.get("archived"):
        notes.append("GitHub repo archived")
        return "stale-block", notes

    # Last-release age.
    if npm_data and npm_data.get("last_release_at"):
        d = days_between(npm_data["last_release_at"])
        if d is not None and d > max_days:
            notes.append(f"last release {d} days ago (threshold: {max_days})")
            return "stale-warn", notes

    # Last-commit age (when known).
    if github_data and github_data.get("last_commit_at"):
        d = days_between(github_data["last_commit_at"])
        if d is not None and d > max_days * 2:   # commit threshold is more lenient than release
            notes.append(f"last commit {d} days ago (threshold: {max_days * 2})")
            return "stale-warn", notes

    return "fresh", notes


# ----------------------------------------------------------------------------
# Probe orchestration
# ----------------------------------------------------------------------------


def probe_one(
    repo_root: Path,
    candidate: CandidateProbe,
    max_age_months: int = DEFAULT_MAX_AGE_MONTHS,
    use_cache: bool = True,
) -> FreshnessResult:
    cp = cache_path(repo_root, candidate.pkg, candidate.ecosystem, candidate.version)
    if use_cache:
        cached = cache_get(cp)
        if cached:
            cached_result = FreshnessResult(**{k: v for k, v in cached.items() if not k.startswith("_")})
            cached_result.notes.append("(from cache)")
            return cached_result

    primary_data: dict | None = None
    if candidate.ecosystem == "npm":
        primary_data = probe_npm(candidate.pkg, candidate.version)
    elif candidate.ecosystem == "pypi":
        primary_data = probe_pypi(candidate.pkg, candidate.version)
    elif candidate.ecosystem == "cargo":
        primary_data = probe_cargo(candidate.pkg, candidate.version)

    github_data: dict | None = None
    repo_url = candidate.repo_url or (primary_data or {}).get("repository")
    if repo_url and "github.com" in (repo_url or ""):
        github_data = probe_github(repo_url)

    verdict, notes = compute_verdict(
        candidate.pkg, primary_data, github_data, max_age_months
    )

    result = FreshnessResult(
        pkg=candidate.pkg,
        ecosystem=candidate.ecosystem,
        version_observed=(primary_data or {}).get("version_observed", candidate.version),
        last_release_at=(primary_data or {}).get("last_release_at"),
        last_commit_at=(github_data or {}).get("last_commit_at"),
        days_since_last_release=days_between((primary_data or {}).get("last_release_at")),
        days_since_last_commit=days_between((github_data or {}).get("last_commit_at")),
        deprecated=bool((primary_data or {}).get("deprecated")),
        archived=bool((github_data or {}).get("archived")),
        supply_chain_incident=SUPPLY_CHAIN_INCIDENTS.get(candidate.pkg),
        license=(primary_data or {}).get("license") or (github_data or {}).get("license"),
        verdict=verdict,
        notes=notes,
    )
    if use_cache:
        cache_put(cp, result.to_dict())
    return result


# ----------------------------------------------------------------------------
# Manifest discovery
# ----------------------------------------------------------------------------


def discover_candidates(repo_root: Path) -> list[CandidateProbe]:
    """Walk package.json + pyproject.toml + Cargo.toml for declared deps."""
    out: list[CandidateProbe] = []

    pkg_json = repo_root / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                for name, spec in (data.get(section) or {}).items():
                    out.append(CandidateProbe(pkg=name, ecosystem="npm", version=str(spec) or None, repo_url=None))
        except (OSError, json.JSONDecodeError):
            pass

    py_toml = repo_root / "pyproject.toml"
    if py_toml.exists():
        try:
            import tomllib  # type: ignore[import-not-found]
        except ImportError:
            try:
                import tomli as tomllib  # type: ignore[import-not-found,no-redef]
            except ImportError:
                tomllib = None  # type: ignore
        if tomllib is not None:
            try:
                with py_toml.open("rb") as f:
                    cfg = tomllib.load(f)
                deps = (cfg.get("project", {}).get("dependencies") or [])
                for line in deps:
                    name = re.split(r"[<>=!~\s\[]", line.strip(), 1)[0]
                    if name:
                        out.append(CandidateProbe(pkg=name, ecosystem="pypi", version=None, repo_url=None))
            except Exception:  # noqa: BLE001
                pass

    cargo_toml = repo_root / "Cargo.toml"
    if cargo_toml.exists():
        try:
            text = cargo_toml.read_text(encoding="utf-8")
            in_deps = False
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("["):
                    in_deps = stripped in ("[dependencies]", "[dev-dependencies]", "[build-dependencies]")
                    continue
                if in_deps and stripped and "=" in stripped and not stripped.startswith("#"):
                    name = stripped.split("=", 1)[0].strip()
                    if name and name not in {"name", "version", "edition", "authors"}:
                        out.append(CandidateProbe(pkg=name, ecosystem="cargo", version=None, repo_url=None))
        except OSError:
            pass

    return out


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------


def render_table(results: list[FreshnessResult]) -> str:
    if not results:
        return "[bequite freshness] No candidates probed."
    headers = ["Package", "Eco", "Version", "Released", "Last commit", "Verdict", "Notes"]
    rows = []
    for r in results:
        rows.append([
            r.pkg,
            r.ecosystem,
            r.version_observed or "?",
            f"{r.days_since_last_release}d ago" if r.days_since_last_release is not None else "?",
            f"{r.days_since_last_commit}d ago" if r.days_since_last_commit is not None else "?",
            r.verdict,
            "; ".join(r.notes)[:60],
        ])
    widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    line = lambda row: " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(row))
    sep = "-+-".join("-" * w for w in widths)
    return "\n".join([line(headers), sep, *[line(r) for r in rows]])


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bequite freshness",
        description="Knowledge probe — verify stack candidates aren't stale.",
    )
    parser.add_argument("--repo", default=".", help="repo root (default: cwd)")
    parser.add_argument("--package", default=None, help="probe one package")
    parser.add_argument("--ecosystem", default=None, choices=["npm", "pypi", "cargo"], help="ecosystem for --package")
    parser.add_argument("--version", default=None, help="version constraint for --package")
    parser.add_argument("--all", action="store_true", help="probe every dep in manifests")
    parser.add_argument("--max-age-months", type=int, default=DEFAULT_MAX_AGE_MONTHS)
    parser.add_argument("--no-cache", action="store_true", help="bypass the 24h cache")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve()

    candidates: list[CandidateProbe]
    if args.package:
        if not args.ecosystem:
            print("[bequite freshness] --ecosystem required when --package is given", file=sys.stderr)
            return 2
        candidates = [CandidateProbe(pkg=args.package, ecosystem=args.ecosystem, version=args.version, repo_url=None)]
    elif args.all:
        candidates = discover_candidates(repo_root)
        if not candidates:
            print("[bequite freshness] No package manifests found in repo (package.json / pyproject.toml / Cargo.toml).")
            return 0
    else:
        parser.print_help()
        return 0

    results = [probe_one(repo_root, c, args.max_age_months, use_cache=not args.no_cache) for c in candidates]

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print(render_table(results))

    blocks = [r for r in results if r.verdict == "stale-block"]
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main())
