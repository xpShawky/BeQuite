"""bequite.pricing — Live pricing fetch (best-effort) (v0.8.1).

Reads vendor pricing pages, caches at `.bequite/cache/pricing.json` for 24h,
falls back to vendored `skill/references/pricing-table.md` when offline.
Provider adapters (`cli/bequite/providers/*.py`) consult this module before
their hard-coded fallback tables.

Cache shape (`.bequite/cache/pricing.json`):

    {
      "fetched_utc": "2026-05-10T14:23:01Z",
      "ttl_hours": 24,
      "models": {
        "claude-opus-4-7":   {"input": 15.00, "output": 75.00, "source": "live"},
        "claude-sonnet-4-6": {"input":  3.00, "output": 15.00, "source": "live"},
        ...
      },
      "warnings": [
        "Anthropic pricing page changed structure on 2026-05-10; verify rates manually."
      ]
    }

Sources tried in order:
1. Cache (if < 24h old).
2. WebFetch the vendor pricing page (best-effort; returns partial dict on parse failure).
3. Vendored `skill/references/pricing-table.md` (always present; flagged stale).

Article VI honest reporting: every cache entry carries `source` ∈
{"live", "stale", "fallback"}. Callers display the source so users know
which data they're seeing.

NOTE: The actual live-fetch (HTTP + LLM extraction) is intentionally
conservative. WebFetch + LLM extraction is brittle for pricing pages (HTML
shifts, vendor adds new tiers). v0.8.1 ships the **infrastructure**: cache
shape + fallback path + adapter wiring. Live extraction is a best-effort
operation that gracefully degrades to "fallback (stale)" when extraction
fails.

Module is runnable as `python -m bequite.pricing --help` from `cli/`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import pathlib
import re
import sys
from typing import Any, Optional


DEFAULT_CACHE_PATH = ".bequite/cache/pricing.json"
DEFAULT_TTL_HOURS = 24


# --------------------------------------------------------------------- vendored fallback


# Hard-coded May-2026 snapshot. Last sync to skill/references/pricing-table.md.
_FALLBACK_TABLE: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-opus-4-7":   {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5": {"input":  0.80, "output":  4.00},
    # OpenAI
    "gpt-5":         {"input": 12.00, "output": 50.00},
    "gpt-5-mini":    {"input":  0.50, "output":  2.00},
    "gpt-4.1":       {"input":  3.00, "output": 12.00},
    "gpt-4.1-mini":  {"input":  0.40, "output":  1.60},
    "o3":            {"input": 10.00, "output": 40.00},
    "o3-mini":       {"input":  1.50, "output":  6.00},
    # Google
    "gemini-2.5-pro":   {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.30, "output":  2.50},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
    # DeepSeek
    "deepseek-chat":   {"input": 0.27, "output": 1.10},
    "deepseek-coder":  {"input": 0.27, "output": 1.10},
    "deepseek-reasoner":{"input": 0.55, "output": 2.19},
}


def fallback_pricing(model: str) -> Optional[dict[str, float]]:
    """Return hard-coded pricing for `model`, or None if unknown."""
    return _FALLBACK_TABLE.get(model)


# --------------------------------------------------------------------- cache


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _parse_iso(ts: str) -> _dt.datetime:
    return _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def cache_age_hours(cache_data: dict[str, Any]) -> float:
    """Hours since `fetched_utc`. Returns +inf if missing/invalid."""
    fetched = cache_data.get("fetched_utc")
    if not fetched:
        return float("inf")
    try:
        dt = _parse_iso(fetched)
    except ValueError:
        return float("inf")
    delta = _dt.datetime.now(_dt.timezone.utc) - dt
    return delta.total_seconds() / 3600.0


def read_cache(cache_path: pathlib.Path) -> dict[str, Any]:
    if not cache_path.exists():
        return {}
    try:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_cache(cache_path: pathlib.Path, data: dict[str, Any]) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def is_cache_fresh(cache_data: dict[str, Any], ttl_hours: int = DEFAULT_TTL_HOURS) -> bool:
    return cache_age_hours(cache_data) < ttl_hours


# --------------------------------------------------------------------- live fetch (best-effort)


VENDOR_URLS = {
    "anthropic": "https://www.anthropic.com/pricing",
    "openai":    "https://openai.com/pricing",
    "google":    "https://ai.google.dev/pricing",
    "deepseek":  "https://api-docs.deepseek.com/quick_start/pricing",
}


def fetch_vendor_page(url: str, timeout_s: float = 10.0) -> Optional[str]:
    """Best-effort GET of a vendor pricing page. Returns HTML text or None on failure."""
    try:
        import httpx
        with httpx.Client(timeout=timeout_s, follow_redirects=True) as client:
            resp = client.get(url, headers={"User-Agent": "bequite-pricing-probe/0.8.1"})
            if resp.status_code == 200:
                return resp.text
    except Exception:  # noqa: BLE001
        pass
    return None


# Coarse regex extraction. Vendors love to format prices as "$X.XX / 1M tokens"
# or "$X.XX per million". We extract pairs and pin them to model names that
# appear within the same paragraph. Hardly perfect but better than nothing.
_PRICE_REGEX = re.compile(r"\$?\s*(\d+\.\d{1,3})\s*(?:/|per)\s*(?:1M|million)", re.IGNORECASE)
_MODEL_REGEX = re.compile(
    r"(claude-opus-4-7|claude-sonnet-4-6|claude-haiku-4-5|"
    r"gpt-5(?:-mini)?|gpt-4\.1(?:-mini)?|o3(?:-mini)?|"
    r"gemini-2\.5-(?:pro|flash|flash-lite)|"
    r"deepseek-(?:chat|coder|reasoner))",
    re.IGNORECASE,
)


def extract_prices_from_html(html: str) -> dict[str, dict[str, float]]:
    """Coarse extraction. Pairs nearest model + 2 prices in the page."""
    text = re.sub(r"<[^>]+>", " ", html)  # strip tags
    text = re.sub(r"\s+", " ", text)
    out: dict[str, dict[str, float]] = {}
    # Walk over paragraphs split by big-gap whitespace, looking for a model + two prices.
    chunks = re.split(r"(?<=[.!?])\s+", text)
    for chunk in chunks:
        m = _MODEL_REGEX.search(chunk)
        if not m:
            continue
        model = m.group(1).lower()
        prices = _PRICE_REGEX.findall(chunk)
        if len(prices) >= 2:
            try:
                out[model] = {"input": float(prices[0]), "output": float(prices[1])}
            except ValueError:
                continue
    return out


def fetch_pricing(provider: Optional[str] = None) -> dict[str, dict[str, float]]:
    """Fetch live pricing for one provider, or all when `provider=None`.

    Returns a dict {model: {input: ..., output: ...}}. Empty dict on failure.
    """
    out: dict[str, dict[str, float]] = {}
    providers = [provider] if provider else list(VENDOR_URLS.keys())
    for p in providers:
        url = VENDOR_URLS.get(p)
        if not url:
            continue
        html = fetch_vendor_page(url)
        if not html:
            continue
        out.update(extract_prices_from_html(html))
    return out


# --------------------------------------------------------------------- public API


def pricing_for(
    model: str,
    *,
    repo_root: Optional[pathlib.Path] = None,
    cache_path: Optional[pathlib.Path] = None,
    ttl_hours: int = DEFAULT_TTL_HOURS,
    refresh: bool = False,
) -> tuple[Optional[dict[str, float]], str]:
    """Return (pricing_dict, source) for `model`.

    pricing_dict has {input, output} per-1M-token USD rates.
    source ∈ {"live", "stale", "fallback", "unknown"}:
      - "live"     — from a fresh cache entry (< ttl_hours old).
      - "stale"    — cache is older than ttl_hours but exists; flagged for warning.
      - "fallback" — vendored hard-coded table (cache absent or model not in cache).
      - "unknown"  — model not in cache OR fallback; pricing_dict is None.

    On `refresh=True`, attempts a live fetch first and updates the cache.
    """
    if repo_root is None:
        repo_root = pathlib.Path.cwd()
    if cache_path is None:
        cache_path = repo_root / DEFAULT_CACHE_PATH

    if refresh:
        live = fetch_pricing()
        if live:
            data = read_cache(cache_path)
            data["fetched_utc"] = _now_iso()
            data["ttl_hours"] = ttl_hours
            data.setdefault("models", {})
            for m, rates in live.items():
                data["models"][m] = {**rates, "source": "live"}
            write_cache(cache_path, data)

    cache = read_cache(cache_path)
    cache_models = cache.get("models", {})

    if model in cache_models:
        rates = cache_models[model]
        if is_cache_fresh(cache, ttl_hours):
            return ({"input": rates["input"], "output": rates["output"]}, "live")
        return ({"input": rates["input"], "output": rates["output"]}, "stale")

    fallback = fallback_pricing(model)
    if fallback is not None:
        return (dict(fallback), "fallback")

    return (None, "unknown")


def estimate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
    *,
    repo_root: Optional[pathlib.Path] = None,
) -> tuple[float, str]:
    """Convenience wrapper used by provider adapters: returns (usd, source)."""
    rates, source = pricing_for(model, repo_root=repo_root)
    if rates is None:
        return (0.0, source)
    usd = (input_tokens / 1_000_000) * rates["input"] + (output_tokens / 1_000_000) * rates["output"]
    return (usd, source)


# --------------------------------------------------------------------- CLI


def _refresh_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    cache_path = repo / DEFAULT_CACHE_PATH
    print(f"Fetching pricing for: {args.provider or 'all providers'}...")
    live = fetch_pricing(args.provider)
    if not live:
        print("(no live pricing extracted; cache unchanged)")
        return 1
    data = read_cache(cache_path)
    data["fetched_utc"] = _now_iso()
    data["ttl_hours"] = args.ttl_hours
    data.setdefault("models", {})
    for m, rates in live.items():
        data["models"][m] = {**rates, "source": "live"}
    write_cache(cache_path, data)
    print(f"Updated cache at {cache_path} with {len(live)} models.")
    for m, rates in live.items():
        print(f"  {m:32s} input=${rates['input']:.2f}/1M  output=${rates['output']:.2f}/1M")
    return 0


def _show_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    rates, source = pricing_for(args.model, repo_root=repo, ttl_hours=args.ttl_hours)
    if rates is None:
        print(f"unknown model: {args.model}")
        return 1
    print(f"model:  {args.model}")
    print(f"input:  ${rates['input']:.2f}/1M")
    print(f"output: ${rates['output']:.2f}/1M")
    print(f"source: {source}")
    if source == "stale":
        print("WARN: cache is older than TTL. Run `bequite pricing refresh` to update.")
    elif source == "fallback":
        print("INFO: using vendored hard-coded snapshot (skill/references/pricing-table.md).")
    return 0


def _list_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    cache = read_cache(repo / DEFAULT_CACHE_PATH)
    age = cache_age_hours(cache)
    if not cache:
        print("(cache empty — using fallback table only)")
        for m, rates in sorted(_FALLBACK_TABLE.items()):
            print(f"  {m:32s} input=${rates['input']:.2f}/1M  output=${rates['output']:.2f}/1M  [fallback]")
        return 0
    fetched = cache.get("fetched_utc", "?")
    ttl = cache.get("ttl_hours", DEFAULT_TTL_HOURS)
    print(f"cache fetched_utc: {fetched}  (age: {age:.1f}h, ttl: {ttl}h)")
    print("")
    models = cache.get("models", {})
    for m in sorted(set(list(models.keys()) + list(_FALLBACK_TABLE.keys()))):
        rates, source = pricing_for(m, repo_root=repo, ttl_hours=ttl)
        if rates is None:
            continue
        print(f"  {m:32s} input=${rates['input']:.2f}/1M  output=${rates['output']:.2f}/1M  [{source}]")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-pricing", description="Live pricing fetch + cache (BeQuite v0.8.1).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)

    rf = sub.add_parser("refresh", help="Fetch live pricing for one provider (or all) and update the cache.")
    rf.add_argument("--provider", default=None, choices=list(VENDOR_URLS.keys()))
    rf.add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS)
    rf.set_defaults(fn=_refresh_cmd)

    sh = sub.add_parser("show", help="Show pricing for a model.")
    sh.add_argument("model")
    sh.add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS)
    sh.set_defaults(fn=_show_cmd)

    ls = sub.add_parser("list", help="List all known models with cache + fallback rates.")
    ls.set_defaults(fn=_list_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
