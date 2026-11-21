# Sound study: Apple product films, 2026 (for the BeQuite hero film)

Shipped copy of the sound study in the BeQuite repo's motion library (2026-11-21); the films and curve images stay in the BeQuite repo, local only.

Owner brief (2026-11-14): energetic, Apple-style sound design and background music (drums, percussion, beats) for the product films Apple releases (not the keynote). Study it first; the music is laid down before the picture, and the shots are cut to its beat.

## 1. Measured (10 films on disk, `.claude/skills/bequite-sound-voice/scripts/sound_profile.py` + `sound_arc.py`)
Curves: `refs/apple-macbook-pro-14-m6/frames/sound_arc_apple2026.png` (white = loudness, orange = kick/low drums, blue = hats).

| Film | Length | Tempo | Kicks/s | Snares/s | Music ends | Silent tail |
|---|---|---|---|---|---|---|
| MacBook Pro M6 | 53.5 s | 107.7 BPM | 2.30 | 1.44 | fades 40→43 s | 10.8 s (logo) |
| MacBook Neo | 35.1 s | (172 = 86×2) | 1.45 | 2.05 | hard stop 29.5 s | 5.5 s |
| MacBook Pro M5 Pro/Max | 100 s | 112 BPM | 2.34 | 0.97 | 94 s | 6 s |
| MacBook Pro PROLED | 117 s | ~140 BPM | 2.62 | 1.49 | 111.75 s | 4.8 s |
| iPhone 17 Pro | 59.6 s | 129 BPM | 2.62 | 1.56 | hard stop 54.5 s | 5 s |
| iPhone 18 Pro (product film) | 54.9 s | 105.5 BPM | 2.92 | 2.04 | hard stop 49.5 s | 5.3 s |
| AirPods Pro 3 | 47.9 s | 129 BPM | 2.40 | 2.25 | hard stop 43 s | 4.8 s |
| iPhone Air | 53.6 s | 97.5 BPM | 2.88 | 1.23 | 47.75 s | 5.8 s |
| iPhone 17 | 50.9 s | ~140 BPM | 2.61 | 1.93 | 45.5 s | 5.3 s |

UNVERIFIED nuance: tempo comes from an onset autocorrelation (octave errors possible: Neo read 172 = 86 × 2). Cut-to-beat rates are only above chance in some films (M6: 30 % of cuts within 40 ms of a beat vs 14 % chance; iPhone 17: 27 % vs 19 %); scene detection misses masked transitions, so treat these as lower bounds.

## 2. The pattern
1. **Drums from the first 1–2 s.** No long ambient intro; the longest build is ~12 s (iPhone 18 Pro: hats rise 0→12 s, full kit at 12.5 s).
2. **Breath → drop.** The kit drops out for 0.5–1 s, then comes back full and a cut or whip lands on the hit (M6 at 7.7 s: whip on a boom; Neo at 11.6 s; iPhone 18 Pro at 12.5 s).
3. **One mid-film breakdown** (1–3 s with the drums out: iPhone 17 Pro 14–17 s; M6 17.5, 27 and 30 s), then back in bigger.
4. **Dense, driving low end:** 2.3–2.9 kicks per second, 1–2.3 snares/claps per second, busy hats (AirPods) or rising hats (iPhone 18 Pro).
5. **Hard stop 4–11 s before the end; the logo plays in silence.** Every film. The M6 is the one fade (3 s).
6. **Tempo 105–130 BPM.** At 120 BPM: 2 beats/s, a bar every 2 s, 30 frames per beat at 60 fps.
7. **Music choice:** Apple licenses artist tracks (M6: Teezo Touchdown; spring MacBook spots: "rhythm-driven", jazz/Fela Kuti per Ad Age). We can't use those; we pick library tracks with the same shape, then edit them to the picture.

## 3. Sound design on top (one sound per gesture)
- Whip / swish on every camera whip and lid move; a boom or low hit on the big cuts (the drop), a sub drop under "rn.".
- UI ticks and clicks tuned to the key on typed text; a soft riser into each breath; reversed cymbal into the drop.
- The 9:56 dead screen: the music cuts to nothing; one electrical buzz.
- "Be quiet.": everything stops (2 beats of silence), then the drums return.
- Lid close: a real close click, then total silence under the end card (the Apple silent tail, ~4–5 s).

## 4. Our beat map (draft, 120 BPM; 1 bar = 2 s; the picture is cut to this)
| Bars | Time | Music | Picture |
|---|---|---|---|
| 1 | 0–2 s | silence + one tick, a low pulse | light in the gap |
| 2 | 2–4 s | kick enters on the lid push | the lid opens |
| 3–4 | 4–8 s | groove (kick + hats), filtered | 9:41 notification, "Hi, I'm the BeQuite agent." |
| 5 | 8–10 s | 0.5 s breath → **drop** on "rn." | the claim lands on the downbeat |
| 6–9 | 10–18 s | full kit | flood → crew → plan (one task change every 2 beats) |
| 10–12 | 18–24 s | full kit + rising hats | swarm builds, evidence, make money (lid-light window turns 45° each 2 beats) |
| 13 | 24–26 s | **cut to silence** + buzz | 9:56 the screen dies |
| 14 | 26–28 s | kit slams back | /bq-recover |
| 15–16 | 28–32 s | the noise: busier, distorted | other tools' claims pile up |
| 17 | 32–34 s | **2 beats of silence** | "Be quiet." |
| 18–21 | 34–42 s | final section, biggest, one boom per slide | 10:00 projector, slides on the beats |
| 22 | 42–44 s | hard stop on the lid close | the agent closes the lid |
| 23–24 | 44–49 s | silence | end card, xpShawky glint |

## 5. Sources
- Measurements: local copies of the films listed above (third-party media, not committed).
- [9to5Mac: the M6 MacBook Pro ad](https://9to5mac.com/2026/10/27/watch-the-ad-for-apples-new-14-inch-macbook-pro-powered-by-m6/) (music by Teezo Touchdown).
- [Ad Age: Apple debuts new MacBooks with pair of rhythm-driven spots](https://adage.com/creativity/work/aa-apple-macbook-air-pro-best-performance-yet-tabs/).
- [Muse by Clio: Apple users find their work rhythm](https://musebyclios.com/music/apple-users-find-their-work-rhythm-with-the-m5-pro-and-m5-max/).
- [Pixabay music: Powerful Percussion playlist and percussion artists](https://pixabay.com/playlists/) (licence to re-check per track).
