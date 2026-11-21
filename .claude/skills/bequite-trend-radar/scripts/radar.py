#!/usr/bin/env python3
"""YouTube side of the trend radar: what is moving this week in a niche, ranked by momentum.

Momentum = a video's views divided by the median views of its own channel's recent uploads
(the idea from youtube-agent-skill's yt-viral: raw views rank channel size, the multiple ranks
the idea). A channel needs at least 4 recent uploads for a median; otherwise it is skipped
and reported. Views per day since upload is reported next to it, because age matters.

  python radar.py sweep OUT --q "الذكاء الاصطناعي" --q "claude code شرح" --per-query 15
  python radar.py sweep OUT --q "..." --period week|month --watch watchlist.md
  python radar.py rank OUT [--min 2.0]          # re-rank what sweep collected

Writes OUT/collected.json (every video seen, with its channel median) and OUT/radar.md
(ranked table). Uses only public listings through yt-dlp: metadata, no media. Network calls run
under a timeout; a failed channel is skipped and named.
"""
import argparse
import datetime as dt
import json
import re
import statistics
import subprocess
import sys
import urllib.parse
from pathlib import Path

PERIOD = {"week": "EgQIAxAB", "month": "EgQIBBAB", "today": "EgQIAhAB"}  # upload date + type=video


def ytdlp_json_lines(args, timeout=120):
    cmd = ["yt-dlp", "--no-update", "--no-warnings", "--socket-timeout", "20", *args]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return [], "timeout"
    rows = []
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows, (p.stderr.strip().splitlines() or [""])[-1]


def search(query, period, n):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query) + "&sp=" + urllib.parse.quote(PERIOD[period])
    rows, err = ytdlp_json_lines(["--flat-playlist", "--playlist-end", str(n), "-j", url])
    return [r["id"] for r in rows if r.get("id")], err


def video_meta(vid):
    rows, err = ytdlp_json_lines(["--skip-download", "-j", f"https://www.youtube.com/watch?v={vid}"], timeout=60)
    if not rows:
        return None, err
    j = rows[0]
    return {k: j.get(k) for k in ("id", "title", "channel", "channel_url", "uploader_id", "upload_date",
                                   "duration", "view_count", "like_count", "comment_count",
                                   "channel_follower_count", "language")}, ""


def channel_recent(channel_url, shorts, n=30):
    tab = "/shorts" if shorts else "/videos"
    rows, err = ytdlp_json_lines(["--flat-playlist", "--playlist-end", str(n), "-j", channel_url.rstrip("/") + tab])
    return [r.get("view_count") for r in rows if isinstance(r.get("view_count"), int)], err


def days_since(yyyymmdd, today):
    try:
        d = dt.datetime.strptime(yyyymmdd, "%Y%m%d").date()
        return max((today - d).days, 1)
    except (TypeError, ValueError):
        return None


def cmd_sweep(a, out):
    seen, ids = {}, []
    for q in a.q:
        got, err = search(q, a.period, a.per_query)
        print(f"search {q!r}: {len(got)} videos {err if not got else ''}")
        for v in got:
            if v not in seen:
                seen[v] = q
                ids.append(v)
    if a.watch:
        page = Path(a.watch).read_text(encoding="utf-8")
        m = re.search(r"^## YouTube[^\n]*\n(.*?)(?=^## |\Z)", page, re.S | re.M)
        for handle in re.findall(r"^- (@[\w.\-]+)", m.group(1) if m else "", re.M):
            rows, err = ytdlp_json_lines(["--flat-playlist", "--playlist-end", "5", "-j",
                                          f"https://www.youtube.com/{handle}/videos"])
            for r in rows:
                if r.get("id") and r["id"] not in seen:
                    seen[r["id"]] = "watchlist " + handle
                    ids.append(r["id"])
    today = dt.date.today()
    medians, videos, skipped = {}, [], []
    for vid in ids:
        m, err = video_meta(vid)
        if not m or not m.get("channel_url"):
            skipped.append((vid, err or "no metadata"))
            continue
        short = (m.get("duration") or 0) <= 180
        key = (m["channel_url"], short)
        if key not in medians:
            views, err = channel_recent(m["channel_url"], short)
            medians[key] = (statistics.median(views), len(views)) if len(views) >= 4 else (None, len(views))
        med, n = medians[key]
        m["source_query"] = seen[vid]
        m["format"] = "short" if short else "long"
        m["channel_median"] = int(med) if med else None
        m["channel_sample"] = n
        m["multiple"] = round(m["view_count"] / med, 2) if med and m.get("view_count") is not None else None
        age = days_since(m.get("upload_date"), today)
        m["age_days"] = age
        m["views_per_day"] = int(m["view_count"] / age) if age and m.get("view_count") is not None else None
        m["url"] = f"https://www.youtube.com/watch?v={vid}"
        videos.append(m)
        print(f"  {m['multiple'] or '-':>6}x  {m['view_count'] or 0:>9,}  {(m['channel'] or '')[:24]:<24} {(m['title'] or '')[:50]}")
    data = {"date": today.isoformat(), "period": a.period, "queries": a.q, "videos": videos, "skipped": skipped}
    (out / "collected.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    rank(out, a.min)


def rank(out, lo, min_views=5000):
    data = json.loads((out / "collected.json").read_text(encoding="utf-8"))
    vids = data["videos"]
    ranked = sorted([v for v in vids if v.get("multiple")], key=lambda v: -v["multiple"])
    thin = [v for v in vids if not v.get("multiple")]
    lines = [f"# YouTube radar, {data['date']} (uploads this {data['period']})", "",
             "Queries: " + " · ".join(f"`{q}`" for q in data["queries"]), "",
             f"{len(vids)} videos, {len(ranked)} with a channel median (4+ recent uploads); shown: "
             f"{lo}x or more and {min_views:,}+ views. Official brand channels can be ad-boosted: check before trusting their multiple.", "",
             "| x median | views | views/day | age d | fmt | channel | title | link |",
             "|---|---|---|---|---|---|---|---|"]
    for v in ranked:
        if v["multiple"] < lo or (v.get("view_count") or 0) < min_views:
            continue
        t = (v.get("title") or "").replace("|", "/")[:70]
        lines.append(f"| {v['multiple']} | {v['view_count']:,} | {v['views_per_day'] or ''} | {v['age_days'] or ''} | "
                     f"{v['format']} | {v.get('channel') or ''} | {t} | {v['url']} |")
    if thin:
        lines += ["", "No median (fewer than 4 recent uploads, or the listing failed): " +
                  ", ".join(f"{(v.get('channel') or '?')} ({v['channel_sample']})" for v in thin[:12])]
    if data.get("skipped"):
        lines += ["", f"Skipped {len(data['skipped'])} video(s) with no metadata."]
    (out / "radar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out / 'radar.md'}: {sum(1 for v in ranked if v['multiple'] >= lo and (v.get('view_count') or 0) >= min_views)} rows")


def cmd_outliers(a, out):
    """Per channel tab (shorts or videos): recent uploads ranked by multiple over that tab's median."""
    rows, thin = [], []
    for handle in a.channel:
        url = f"https://www.youtube.com/{handle.lstrip('/')}/{a.tab}"
        got, err = ytdlp_json_lines(["--flat-playlist", "--playlist-end", str(a.recent), "-j", url])
        views = [r.get("view_count") for r in got if isinstance(r.get("view_count"), int)]
        if len(views) < 4:
            thin.append(f"{handle} ({len(views)}) {err}")
            continue
        med = statistics.median(views)
        for r in got:
            v = r.get("view_count")
            if isinstance(v, int) and med and v >= a.min_views:
                rows.append({"channel": handle, "title": r.get("title"), "views": v, "median": int(med),
                             "multiple": round(v / med, 2), "url": f"https://www.youtube.com/watch?v={r.get('id')}"})
        print(f"{handle}: {len(views)} recent {a.tab}, median {int(med):,}")
    rows.sort(key=lambda r: -r["multiple"])
    today = dt.date.today()
    if a.since_days:
        # Channel tabs list the last N uploads, which can span years on a slow channel:
        # fetch the date of each candidate (one metadata call) and keep the recent ones.
        kept = []
        for r in rows:
            if len(kept) >= a.top:
                break
            m, _ = video_meta(r["url"].split("v=")[-1])
            age = days_since((m or {}).get("upload_date"), today)
            r["upload_date"], r["age_days"] = (m or {}).get("upload_date"), age
            if age is not None and age <= a.since_days:
                kept.append(r)
        rows = kept
    lines = [f"# Outliers in recent {a.tab} ({today.isoformat()}, last {a.recent} per channel"
             + (f", uploaded in the last {a.since_days} days" if a.since_days else "") + ")", "",
             "| x median | views | median | age d | channel | title | link |", "|---|---|---|---|---|---|---|"]
    for r in rows[: a.top]:
        t = (r["title"] or "").replace("|", "/")[:70]
        lines.append(f"| {r['multiple']} | {r['views']:,} | {r['median']:,} | {r.get('age_days', '')} | {r['channel']} | {t} | {r['url']} |")
    if thin:
        lines += ["", "Skipped (under 4 uploads or listing failed): " + "; ".join(thin)]
    (out / f"outliers-{a.tab}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / f"outliers-{a.tab}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out / f'outliers-{a.tab}.md'}")


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sweep")
    p.add_argument("out")
    p.add_argument("--q", action="append", required=True)
    p.add_argument("--period", choices=list(PERIOD), default="week")
    p.add_argument("--per-query", type=int, default=15)
    p.add_argument("--watch")
    p.add_argument("--min", type=float, default=0.0)
    p.add_argument("--min-views", type=int, default=5000)
    r = sub.add_parser("rank")
    r.add_argument("out")
    r.add_argument("--min", type=float, default=1.5)
    r.add_argument("--min-views", type=int, default=5000)
    o = sub.add_parser("outliers")
    o.add_argument("out")
    o.add_argument("--channel", action="append", required=True, help="@handle, repeatable")
    o.add_argument("--tab", choices=["shorts", "videos"], default="shorts")
    o.add_argument("--recent", type=int, default=30)
    o.add_argument("--top", type=int, default=20)
    o.add_argument("--since-days", type=int, default=0, help="keep only uploads this recent (0 = no filter)")
    o.add_argument("--min-views", type=int, default=5000)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "sweep":
        cmd_sweep(a, out)
    elif a.cmd == "outliers":
        cmd_outliers(a, out)
    else:
        rank(out, a.min, a.min_views)


if __name__ == "__main__":
    main()
