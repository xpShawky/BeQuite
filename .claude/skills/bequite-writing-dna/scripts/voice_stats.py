#!/usr/bin/env python3
"""Measure a set of posts (a voice) so a Writing DNA rests on numbers, not adjectives.

Input: a JSON file that is a list of strings, or {"posts": [{"t": "..."} or "..."]}, or a .txt
file with one post per blank-line-separated block. Compare two sets side by side with --vs.

  python voice_stats.py human.json
  python voice_stats.py human.json --vs generated.json --names human,generated
  python voice_stats.py posts.json --json > stats.json

Measures per set (medians and spread across posts, rates per 100 words):
  length: words per post, sentences per post, words per sentence (mean, SD, % under 8, % over 20)
  punctuation per 100 words: Arabic comma ، , Latin comma , full stop, ! ? … .. :, dash — –, quotes
  line breaks per post, blank-line paragraphs, emoji per post and share of posts with emoji,
  emoji at the start of a post, hashtags, mentions, links
  Arabic: share of Egyptian / Gulf / MSA markers, particles (يعني، بقى، كده، اللي، عشان، مش، وش، مو، زي، يا),
  diacritics per 100 words, tatweel and letter elongation, Latin-script words share, Eastern vs Western digits
  structure: numbered or bulleted lines, posts that end in a call (احفظ، تابع، 👇), openers (first word)
  vocabulary: type-token ratio on the pooled set, share of the 20 most frequent words (repetition)

Stdlib only. Counts are heuristics: read them next to the posts, not instead of them.
"""
import argparse
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

AR = re.compile(r"[؀-ۿ]")
WORD = re.compile(r"[\w؀-ۿ]+(?:['’][\w]+)?", re.U)
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF☀-➿⬀-⯿\U0001F1E6-\U0001F1FF]")
DIAC = re.compile(r"[ً-ْ]")
LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z0-9.+#-]*\b")
URL = re.compile(r"(https?://\S+|\b[\w-]+\.(?:com|ai|io|im|art|club|org|net|dev|app|me)\b\S*)")
SENT_END = re.compile(r"[.!?؟…]+|\n+")

MARKERS = {
    "egyptian": ["كده", "بقى", "عشان", "مش", "ده", "دي", "دلوقتي", "إزاي", "ازاي", "ليه", "اللي", "بتاع", "أوي", "اوي", "خالص", "يعني", "هو", "بيعمل", "هتحتاج", "هيخلي"],
    "gulf": ["وش", "مو", "زين", "يسوي", "سويت", "سو", "شي", "لين", "هذي", "هالـ", "يبي", "ابي", "كذا", "يراويك", "تراه", "حيل", "مره"],
    "msa": ["الذي", "التي", "الذين", "لقد", "إن", "إنّ", "كما", "حيث", "ذلك", "هذه", "سوف", "لكن", "بل", "أيضاً", "أيضا", "يجب", "ينبغي", "مما"],
}
PARTICLES = ["يعني", "بقى", "كده", "اللي", "عشان", "مش", "وش", "مو", "زي", "يا", "طيب", "خلاص", "والله", "بس"]


def load(path):
    p = Path(path)
    if p.suffix.lower() == ".json":
        d = json.loads(p.read_text(encoding="utf-8"))
        items = d.get("posts", d) if isinstance(d, dict) else d
        posts = [x if isinstance(x, str) else x.get("t") or x.get("text") or "" for x in items]
    else:
        posts = [b.strip() for b in re.split(r"\n\s*\n", p.read_text(encoding="utf-8")) if b.strip()]
    return [re.sub(r"\s*Show more\s*$", "", x).strip() for x in posts if x and x.strip()]


def per100(n, words):
    return 100.0 * n / words if words else 0.0


def med(xs):
    return round(st.median(xs), 2) if xs else 0


def measure(posts):
    rows, pooled = [], []
    for t in posts:
        words = WORD.findall(t)
        nw = max(len(words), 1)
        sents = [s for s in SENT_END.split(t) if WORD.search(s)]
        slen = [len(WORD.findall(s)) for s in sents] or [nw]
        lower = [w.lower() for w in words]
        pooled += lower
        rows.append({
            "words": len(words), "sentences": len(sents), "sent_len": slen,
            "ar_comma": per100(t.count("،"), nw), "comma": per100(t.count(","), nw),
            "stop": per100(len(re.findall(r"(?<![.\d])\.(?![.\d])", t)), nw),
            "excl": per100(t.count("!"), nw), "q": per100(t.count("؟") + t.count("?"), nw),
            "ellipsis": per100(t.count("…") + len(re.findall(r"\.\.+", t)), nw),
            "colon": per100(t.count(":"), nw), "dash": per100(t.count("—") + t.count("–"), nw),
            "lines": t.count("\n"), "paras": len(re.findall(r"\n\s*\n", t)),
            "emoji": len(EMOJI.findall(t)), "emoji_start": bool(EMOJI.match(t)),
            "hashtags": len(re.findall(r"#\w+", t)), "mentions": len(re.findall(r"@\w+", t)),
            "links": len(URL.findall(t)),
            "diacritics": per100(len(DIAC.findall(t)), nw),
            "tatweel": t.count("ـ") + len(re.findall(r"([ء-ي])\1\1", t)),
            "latin_share": len(LATIN_WORD.findall(t)) / nw,
            "eastern_digits": len(re.findall(r"[٠-٩]", t)), "western_digits": len(re.findall(r"[0-9]", t)),
            "list_lines": len(re.findall(r"(?m)^\s*(?:\d+[.)]|0\d\.|[-•🔹❌✅📌]|\d+\s*[-–])\s*", t)),
            "ends_call": bool(re.search(r"(احفظ|تابع|اكتب|جرب|👇|🔖)[^\n]*$", t)),
            "opener": words[0] if words else "",
            "markers": {k: sum(lower.count(m) for m in v) for k, v in MARKERS.items()},
            "particles": sum(lower.count(m) for m in PARTICLES),
        })
    all_sl = [x for r in rows for x in r["sent_len"]]
    nposts = len(rows) or 1
    total_words = sum(r["words"] for r in rows) or 1
    top20 = sum(c for _, c in Counter(pooled).most_common(20))
    mk = {k: sum(r["markers"][k] for r in rows) for k in MARKERS}
    mk_total = sum(mk.values()) or 1
    return {
        "posts": len(rows),
        "words_per_post_median": med([r["words"] for r in rows]),
        "words_per_post_sd": round(st.pstdev([r["words"] for r in rows]), 1) if rows else 0,
        "sentence_len_mean": round(st.mean(all_sl), 1) if all_sl else 0,
        "sentence_len_sd": round(st.pstdev(all_sl), 1) if all_sl else 0,
        "sentences_under_8_pct": round(100 * sum(1 for x in all_sl if x < 8) / max(len(all_sl), 1)),
        "sentences_over_20_pct": round(100 * sum(1 for x in all_sl if x > 20) / max(len(all_sl), 1)),
        **{f"{k}_per100w": round(sum(r[k] * r["words"] / 100 for r in rows) * 100 / total_words, 2)
           for k in ("ar_comma", "comma", "stop", "excl", "q", "ellipsis", "colon", "dash", "diacritics")},
        "line_breaks_per_post_median": med([r["lines"] for r in rows]),
        "emoji_per_post_mean": round(sum(r["emoji"] for r in rows) / nposts, 2),
        "posts_with_emoji_pct": round(100 * sum(1 for r in rows if r["emoji"]) / nposts),
        "posts_starting_with_emoji_pct": round(100 * sum(1 for r in rows if r["emoji_start"]) / nposts),
        "hashtags_per_post": round(sum(r["hashtags"] for r in rows) / nposts, 2),
        "posts_with_link_pct": round(100 * sum(1 for r in rows if r["links"]) / nposts),
        "posts_with_list_pct": round(100 * sum(1 for r in rows if r["list_lines"] >= 2) / nposts),
        "posts_ending_in_call_pct": round(100 * sum(1 for r in rows if r["ends_call"]) / nposts),
        "particles_per100w": round(100 * sum(r["particles"] for r in rows) / total_words, 2),
        "dialect_mix_pct": {k: round(100 * v / mk_total) for k, v in mk.items()},
        "latin_word_share_pct": round(100 * sum(r["latin_share"] * r["words"] for r in rows) / total_words, 1),
        "elongation_or_tatweel_posts": sum(1 for r in rows if r["tatweel"]),
        "digits_eastern_vs_western": [sum(r["eastern_digits"] for r in rows), sum(r["western_digits"] for r in rows)],
        "type_token_ratio": round(len(set(pooled)) / max(len(pooled), 1), 3),
        "top20_words_share_pct": round(100 * top20 / max(len(pooled), 1), 1),
        "top_openers": Counter(r["opener"] for r in rows).most_common(5),
    }


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("posts")
    ap.add_argument("--vs")
    ap.add_argument("--names", default="A,B")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sets = {a.names.split(",")[0]: measure(load(a.posts))}
    if a.vs:
        sets[a.names.split(",")[1]] = measure(load(a.vs))
    if a.json:
        print(json.dumps(sets, ensure_ascii=False, indent=1))
        return
    names = list(sets)
    print("| measure | " + " | ".join(names) + " |")
    print("|---|" + "---|" * len(names))
    for k in sets[names[0]]:
        print(f"| {k} | " + " | ".join(str(sets[n][k]) for n in names) + " |")


if __name__ == "__main__":
    main()
