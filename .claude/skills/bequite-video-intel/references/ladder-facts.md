# Ladder facts (measured 2026-11-21 on a Windows 11 machine, home connection)

Every row is a run with `scripts/watch.py` or the yt-dlp / ffmpeg command it wraps. Re-measure on a new machine before quoting these numbers to a user.

## Cost per level

| Level | Video | Bytes fetched | Wall time |
|---|---|---|---|
| L0 meta | YouTube Short (88 s) | 1,124 | 2.5 s |
| L0 meta | YouTube long (20:38) | 4,505 | 2.4 s |
| L0 meta | TikTok (150 s) | 971 | 12.4 s |
| L1 captions, 1 language | YouTube tutorial (3:44) | 7,151 | 2.7 s |
| L1 captions | YouTube long, `en` | 36,568 | about 4 s |
| L1b audio fetch | YouTube Short | 542,454 | 15.9 s |
| L1b audio fetch | YouTube 13 min | 4,745,049 | 6.6 s |
| L1b audio fetch | TikTok 150 s | 2,402,473 | 3.5 s |
| L1b transcribe, faster-whisper `small`, CPU int8 | 13 min English | 0 | about 3 min |
| L1b transcribe, `small`, CPU int8, `--lang ar` | 88 s Egyptian Arabic | 0 | 184 s, and the text came out in English: unusable |
| L1b transcribe, `large-v3-turbo`, CPU int8, `--lang ar` | same 88 s | 1.6 GB model download once | 547 s incl. download; English mixed with garbage: unusable |
| L1 captions `ar-orig` | same Short | 15,914 | 2.9 s, clean Egyptian Arabic |
| L2 storyboard `sb0` | Short (101x180 thumbs, 10 sheets) | 84,594 | 4.3 s |
| L2 storyboard `sb0` | 3.5 min video (320x180, 108 thumbs) | 305,661 | 4.8 s (Fable, same day) |
| L2b section 3 s at 720p | tutorial screen recording | 100,475-169,999 | 4-6 s |
| L2b section 3-4 s at 360p | long video, graphics | 21,317-89,071 | 3-4 s |
| L2b section 10 s at 144p | (Fable, same day) | 136,226 | 4.3 s |
| L3 full 360p | Short 88 s | 1,524,409 | 4.7 s |
| L3 full (smallest offered, 576x1024) | TikTok 150 s | 6,582,018 | 11.7 s |
| L3 full 240p | long 20:38 | 24,027,686 | 10.9 s |
| L3 study (`film_study.py`) | long 20:38 at 240p | 0 | 55.8 s |

## Failure modes seen, and the rule each one produced

| Seen | Rule |
|---|---|
| `--sub-langs "en.*"` returned HTTP 429 (Fable) | exact language codes only; the script refuses wildcards |
| After about 6 caption requests in 10 minutes, every caption request returned HTTP 429 (first at 19:52, last at 20:08); the next try at 20:27 worked. Video, audio and storyboard requests kept working throughout | on 429, wait about 20 minutes or switch level; do not retry captions in a loop |
| Whisper (`small` and `large-v3-turbo`) on Egyptian Arabic returned English or garbage, while YouTube's `ar-orig` track was clean | Arabic dialect: platform captions first; Whisper output on Arabic is flagged UNVERIFIED and spot-checked; English Whisper is reliable for words (names and numbers still checked) |
| One yt-dlp call with five `--download-sections` ranges produced nothing for over 3 minutes; the same ranges one per call took 3-6 s each | one range per call, hard timeout on every call |
| `bv*[height<=360]` gave 144x256 on a vertical video (its 360p stream is 360x640) | select with `-S res:N` (yt-dlp: "res = smallest dimension") |
| `-f worst` is discouraged by the yt-dlp README | audio with `-f ba/b -S +size,+br` |
| The global `whisper` CLI crashed: "Numba needs NumPy 2.3 or less. Got NumPy 2.4." | L1b uses faster-whisper in its own venv (`faster-whisper==1.2.1`, ctranslate2 4.9.0 has a cp314 Windows wheel); never downgrade the global NumPy |
| faster-whisper's own decoder failed with a newer PyAV (`open() got an unexpected keyword argument 'metadata_errors'`) | decode with the system ffmpeg to 16 kHz mono and pass the samples (the shipped `transcribe.py` already does) |
| `--device cuda` failed: `cublas64_12.dll is not found` | CPU int8 is the default; GPU needs cuBLAS 12 + cuDNN 9 (faster-whisper README). On PyPI the latest `nvidia-cublas-cu12` (12.9.3.13) has no Windows wheel and `nvidia-cudnn-cu12` 9.28.1.4 is 696 MB: a choice for the user, not a default |
| `python -I` hid the user site-packages that hold numpy and OpenCV, so `film_study.py` reported numpy missing | run our own scripts with `-P -E` (no script dir or cwd on the path, no PYTHON* variables) |
| TikTok: no captions in `ar`, no storyboards | for TikTok go L0 → L1b → L3 |
| AI Studio: "Model isn't available right now" on a 130K-token video | rerun once after a minute (worked) |

## What each source of truth is good for

- Captions and Whisper: words and when they were said. Whisper mishears names, numbers and dates ("April 30, 2029" for 2026); check them against a second source.
- Storyboards: layout and what kind of shot, not text smaller than the thumbnail.
- L2b frames at 720p: UI values, filenames, on-screen text.
- `film_study.py`: cut list (hard cuts; position-locked graphic changes inflate the count on screen-recording videos), shot lengths, loudness, sound at each cut, silences.
- Route G: structure, on-screen text, sound design and critique in one pass; not cut counts (it says UNSURE) and not pause lengths (it said 0.3-0.5 s where the measurement was 1.25 s).

## Options that run only when the user asks

- **GPU transcription.** faster-whisper on the GPU needs cuBLAS 12 + cuDNN 9 (faster-whisper README). If the user already has a working GPU install (another project's venv), pass that interpreter: `watch.py audio URL OUT --py <that python> --device cuda --model large-v3-turbo`. Otherwise ask before installing the NVIDIA wheels (about 1.3 GB, NVIDIA licence).
- **Cloud session.** A cloud Claude session runs in a container built from the GitHub repo, so downloads use the provider's network, not the user's. Open risk: YouTube often refuses data-centre IPs ("confirm you're not a bot"). The test, when the user wants it: start a cloud session on the repo and run `watch.py meta URL out/` then `watch.py section URL out/ --at 0:10-0:13`; if both pass, the cloud can run the ladder; if they fail, use it for text research only. Results come back as files on a branch, so keep them small (breakdowns, not videos).
- **If YouTube blocks a server.** Order of fixes: (1) don't download at all: route G (a multimodal model in the user's browser) or captions only; (2) run the download step on the user's own machine and send only the small result to the server; (3) yt-dlp's own options (`--sleep-requests`, a different client, `--cookies-from-browser` only on the user's own machine, never copied to a server). Third-party "downloader" sites and extensions (the `ss` prefix sites, ymusic.io and similar) are not a default: they are web pages with ads and changing terms, they re-host YouTube streams outside YouTube's terms, and an agent cannot verify what they run. Use one only if the user picks it, by hand, on his own machine.
- **Prerequisite for the cloud test:** the user connects GitHub to Claude (the repo on GitHub and a cloud environment). Until then the test stays here as written. The test brief (read-only, nothing pushed): install yt-dlp after checking it on PyPI; with a 120 s timeout each, run metadata (`-J --skip-download`), captions (exact language), storyboard (`-f sb0`), a 3-second section at 240p, and TikTok metadata; on a bot check or HTTP 429/403 retry once with `--sleep-requests 2`; no cookies, proxies or downloader sites; report a table of exit code, seconds, bytes, error, and the verdict: full ladder / text research only / nothing.

