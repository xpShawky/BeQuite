#!/usr/bin/env python3
"""The video ladder: look at a video at the lowest cost that answers the question.

Each level is a subcommand. Every call appends one line to OUT/ledger.jsonl (level, bytes
fetched, seconds, files, exit, note), so a breakdown can always say what it cost.

  L0  meta        URL OUT                      title, channel, date, length, views, likes, comments,
                                               chapters, caption languages (one JSON, no media)
  L1  captions    URL OUT --lang ar            platform captions, exact language codes only
  L1b audio       URL OUT [--lang ar]          worst audio stream + local transcript (faster-whisper)
  L2  storyboard  URL OUT [--fmt sb0]          YouTube's own thumbnail sheets, no video download
  L2b section     URL OUT --at 1:39-1:42       only those seconds, low resolution, + a 1 fps sheet
  L3  full        URL OUT [--height 360]       whole video at low resolution [--study runs film_study]
      ledger      OUT                          totals per level

Examples:
  python watch.py meta https://www.youtube.com/watch?v=joNgPsK0TRE out/
  python watch.py captions https://youtu.be/joNgPsK0TRE out/ --lang en
  python watch.py section https://youtu.be/joNgPsK0TRE out/ --at 1:39-1:42 --height 720
  python watch.py audio https://www.tiktok.com/@user/video/123 out/ --py C:/venvs/fw/Scripts/python.exe

Rules baked in (measured 2026-11-21, see the skill's references/ladder-facts.md):
  - never a wildcard caption language (`en.*` triggered HTTP 429); a 429 on captions is reported
    with the advice to wait or drop to L1b;
  - one --download-sections range per call (a call with five ranges stalled for minutes);
  - every network call runs under a hard timeout.
Needs: yt-dlp and ffmpeg on PATH. L1b needs a Python with faster-whisper (pass --py).
"""
import argparse
import email
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRANSCRIBER = HERE.parents[1] / "bequite-motion-director" / "scripts" / "transcribe.py"
FILM_STUDY = HERE.parents[1] / "bequite-motion-director" / "scripts" / "film_study.py"


def snapshot(out):
    return {p: p.stat().st_size for p in out.rglob("*") if p.is_file() and p.name != "ledger.jsonl"}


def run(cmd, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        code, err = p.returncode, (p.stderr or "") + (p.stdout or "")
    except subprocess.TimeoutExpired:
        code, err = 124, f"timeout after {timeout} s"
    return code, err, time.time() - t0


def ytdlp(url, out, args, timeout):
    cmd = ["yt-dlp", "--no-update", "--no-progress", "--socket-timeout", "20", *args, url]
    return run(cmd, timeout)


def log(out, level, url, before, code, err, secs, note="", fetched=None):
    """fetched: glob patterns (relative to out) of the files that came over the network."""
    after = snapshot(out)
    new = {str(p.relative_to(out)): s for p, s in after.items() if before.get(p) != s}
    got = {k: v for k, v in new.items() if fetched and any(Path(k).match(g) for g in fetched)}
    if code != 0 and "429" in err:
        note = (note + " rate-limited (HTTP 429): wait 15+ min or use L1b").strip()
    if code == 124:
        note = (note + " timed out").strip()
    entry = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "level": level, "url": url,
             "bytes": sum(got.values()), "written": sum(new.values()), "seconds": round(secs, 1), "exit": code,
             "files": sorted(new), "note": note}
    with open(out / "ledger.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(json.dumps(entry, ensure_ascii=False))
    if code != 0:
        tail = [l for l in err.splitlines() if "ERROR" in l or "timeout" in l][-3:]
        print("\n".join(tail), file=sys.stderr)
    return entry


def hms(s):
    s = float(s)
    return f"{int(s // 60)}:{s % 60:04.1f}"


def to_sec(t):
    parts = [float(x) for x in t.split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(parts)))


# ---------- L0 ----------
def cmd_meta(a, out):
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["-J", "--skip-download"], a.timeout)
    note = ""
    if code == 0:
        start = err.find("\n{") + 1 if not err.startswith("{") else 0
        j = json.JSONDecoder().raw_decode(err[start:])[0]
        fmt = max((f for f in j.get("formats") or [] if f.get("height")), key=lambda f: f["height"], default={})
        keep = {k: j.get(k) for k in ("id", "title", "channel", "uploader_id", "channel_url", "upload_date",
                                      "duration", "view_count", "like_count", "comment_count",
                                      "channel_follower_count", "language", "tags", "description")}
        keep["chapters"] = [{"start": c["start_time"], "title": c["title"]} for c in j.get("chapters") or []]
        keep["captions"] = sorted((j.get("subtitles") or {}).keys())
        auto = j.get("automatic_captions") or {}
        keep["auto_captions_orig"] = sorted(k for k in auto if k.endswith("-orig")) or None
        keep["auto_captions_count"] = len(auto)
        keep["width"], keep["height"] = fmt.get("width"), fmt.get("height")
        keep["vertical"] = bool(fmt.get("height") and fmt.get("width") and fmt["height"] > fmt["width"])
        keep["storyboards"] = sorted(f["format_id"] for f in j.get("formats") or [] if f.get("format_id", "").startswith("sb"))
        (out / "meta.json").write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")
        note = f"{keep['title']!r} {keep['duration']} s, {keep['view_count']} views"
    log(out, "L0", a.url, before, code, err, secs, note, ["meta.json"])


# ---------- L1 ----------
def vtt_to_lines(path):
    """Platform VTT (incl. rolling auto-captions) -> [(seconds, text)] without repeats."""
    # Read cue by cue, line by line: YouTube auto-caption cues begin with a whitespace-only
    # line, so splitting on blank lines would drop the first line of every cue.
    cues, cur = [], None
    for raw in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"(\d+):(\d\d):(\d\d)\.(\d+) -->", raw.strip())
        if m:
            cur = [int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000, []]
            cues.append(cur)
        elif cur is not None and raw.strip():
            cur[1].append(re.sub(r"<[^>]+>", "", raw).strip())
    lines, last = [], ""
    for start, texts in cues:
        for t in texts:
            if t and t != last and not last.endswith(t):
                lines.append((start, t))
                last = t
    return lines


def cmd_captions(a, out):
    if "*" in a.lang or ".*" in a.lang:
        sys.exit("Use exact language codes (ar, en, ar-orig). Wildcards trigger HTTP 429.")
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["--skip-download", "--write-subs", "--write-auto-subs",
                                         "--sub-langs", a.lang, "--sub-format", "vtt",
                                         "-o", str(out / "captions.%(ext)s")], a.timeout)
    vtts = sorted(out.glob("captions*.vtt"))
    note = ""
    if vtts:
        lines = vtt_to_lines(vtts[0])
        md = [f"# Captions ({vtts[0].name}), platform text, check names and numbers", ""]
        md += [f"[{hms(s)}] {t}" for s, t in lines]
        (out / "transcript.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        note = f"{len(lines)} lines, {sum(len(t.split()) for _, t in lines)} words"
    elif code == 0:
        code, note = 2, f"no captions in '{a.lang}': try another exact code or L1b"
    log(out, "L1", a.url, before, code, err, secs, note, ["captions*.vtt"])


# ---------- L1b ----------
def cmd_audio(a, out):
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["-f", "ba/b", "-S", "+size,+br", "-o", str(out / "audio.%(ext)s")],
                            a.timeout)
    log(out, "L1b-fetch", a.url, before, code, err, secs, "", ["audio.*"])
    audio = next(iter(sorted(out.glob("audio.*"))), None)
    if code != 0 or not audio:
        return
    tr = Path(a.transcriber) if a.transcriber else TRANSCRIBER
    if not tr.exists():
        sys.exit(f"transcriber not found: {tr} (pass --transcriber)")
    before = snapshot(out)
    cmd = [a.py, "-P", "-E", str(tr), str(audio), str(out / "transcript.md"), "--model", a.model,
           "--device", a.device] + (["--lang", a.lang] if a.lang else [])
    code, err, secs = run(cmd, 3600)
    print(err.strip().splitlines()[-1] if err.strip() else "", file=sys.stderr)
    log(out, "L1b-transcribe", a.url, before, code, err, secs, f"model {a.model} on {a.device}; 0 bytes fetched")


# ---------- L2 ----------
def cmd_storyboard(a, out):
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["-f", a.fmt, "-o", str(out / "storyboard.%(ext)s")], a.timeout)
    mh = out / "storyboard.mhtml"
    note = ""
    if mh.exists():
        msg = email.message_from_binary_file(open(mh, "rb"))
        html, imgs = "", []
        for p in msg.walk():
            if p.is_multipart():
                continue
            data = p.get_payload(decode=True) or b""
            if p.get_content_type() == "text/html":
                html = data.decode("utf-8", "replace")
            elif p.get_content_type().startswith("image/"):
                imgs.append(data)
        spans = re.findall(r"(\d\d):(\d\d):(\d\d),(\d+) \S+ (\d\d):(\d\d):(\d\d),(\d+)", html)
        sb = out / "storyboard"
        sb.mkdir(exist_ok=True)
        index = ["# Storyboard sheets (each sheet is a grid read left to right, top to bottom)", ""]
        for i, data in enumerate(imgs):
            raw = sb / f"sheet_{i:03d}.webp"
            raw.write_bytes(data)
            jpg = raw.with_suffix(".jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), str(jpg)])
            raw.unlink()
            if i < len(spans):
                s = spans[i]
                t0 = int(s[0]) * 3600 + int(s[1]) * 60 + int(s[2]) + int(s[3]) / 1000
                t1 = int(s[4]) * 3600 + int(s[5]) * 60 + int(s[6]) + int(s[7]) / 1000
                index.append(f"- {jpg.name}: {hms(t0)} to {hms(t1)}")
        (sb / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
        note = f"{len(imgs)} sheets"
    log(out, "L2", a.url, before, code, err, secs, note, ["storyboard.mhtml"])


# ---------- L2b ----------
def cmd_section(a, out):
    m = re.fullmatch(r"([\d:.]+)-([\d:.]+)", a.at)
    if not m:
        sys.exit("--at must look like 1:39-1:42")
    t0, t1 = to_sec(m[1]), to_sec(m[2])
    tag = f"{int(t0)}-{int(t1)}"
    # -S res:N sorts by the short side, so vertical video gets the same quality as landscape
    sel = "bv*+ba/b" if a.audio else "bv*/b"
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["-f", sel, "-S", f"res:{a.height}", "--download-sections", f"*{t0}-{t1}",
                                         "-o", str(out / f"section_{tag}.%(ext)s")], a.timeout)
    clip = next(iter(sorted(out.glob(f"section_{tag}.*"))), None)
    if clip:
        n = max(1, round((t1 - t0) * a.fps))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
                        f"fps={a.fps},scale=640:-2,tile=1x{n}", "-frames:v", "1",
                        str(out / f"section_{tag}_sheet.jpg")])
    log(out, "L2b", a.url, before, code, err, secs, f"{a.at} at <= {a.height}p", [f"section_{tag}.*"])


# ---------- L3 ----------
def cmd_full(a, out):
    before = snapshot(out)
    code, err, secs = ytdlp(a.url, out, ["-f", "bv*+ba/b", "-S", f"res:{a.height}", "--merge-output-format", "mp4",
                                         "-o", str(out / "full.%(ext)s")], a.timeout)
    log(out, "L3-fetch", a.url, before, code, err, secs, f"<= {a.height}p", ["full.*"])
    vid = next(iter(sorted(out.glob("full.*"))), None)
    if a.study and vid and code == 0:
        fs = Path(a.film_study) if a.film_study else FILM_STUDY
        before = snapshot(out)
        code, err, secs = run([a.py, "-P", "-E", str(fs), str(vid), str(out / "study")], 3600)
        log(out, "L3-study", a.url, before, code, err, secs, "film_study.py; 0 bytes fetched")


def cmd_ledger(a, out):
    rows = [json.loads(l) for l in (out / "ledger.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    tot = {}
    for r in rows:
        t = tot.setdefault(r["level"], [0, 0, 0.0])
        t[0] += 1
        t[1] += r["bytes"]
        t[2] += r["seconds"]
    print("| level | calls | bytes | seconds |\n|---|---|---|---|")
    for k, (n, b, s) in tot.items():
        print(f"| {k} | {n} | {b:,} | {s:.1f} |")
    print(f"| total | {len(rows)} | {sum(v[1] for v in tot.values()):,} | {sum(v[2] for v in tot.values()):.1f} |")


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, url=True):
        p = sub.add_parser(name)
        if url:
            p.add_argument("url")
        p.add_argument("out")
        p.add_argument("--timeout", type=int, default=120)
        p.set_defaults(fn=fn)
        return p

    add("meta", cmd_meta)
    add("captions", cmd_captions).add_argument("--lang", required=True)
    p = add("audio", cmd_audio)
    p.add_argument("--py", default=sys.executable)
    p.add_argument("--transcriber")
    p.add_argument("--model", default="small")
    p.add_argument("--device", default="cpu")
    p.add_argument("--lang")
    add("storyboard", cmd_storyboard).add_argument("--fmt", default="sb0")
    p = add("section", cmd_section)
    p.add_argument("--at", required=True)
    p.add_argument("--height", type=int, default=240)
    p.add_argument("--fps", type=float, default=1.0)
    p.add_argument("--audio", action="store_true")
    p = add("full", cmd_full)
    p.add_argument("--height", type=int, default=360)
    p.add_argument("--study", action="store_true")
    p.add_argument("--py", default=sys.executable)
    p.add_argument("--film-study")
    add("ledger", cmd_ledger, url=False)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    a.fn(a, out)


if __name__ == "__main__":
    main()
