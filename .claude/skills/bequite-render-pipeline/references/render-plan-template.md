# Render plan template (goes into the work's `plan.md` · ✋ `RENDER_PLAN_APPROVED`)

Most important first: **nothing renders at full quality, and no paid credit is spent, until this plan is approved; the master render needs one more yes at M8.** Copy the block below into `plan.md` and fill it.

```markdown
## Render plan — <film title> (v<plan version>, <date>)

### Engine per shot
| Shot / scene | Needs | Engine (adapter) | Why | Fallback |
|---|---|---|---|---|
| S1 hook | 3D camera over UI, text animators | After Effects | user owns it; text animators | HTML frame capture |
(decision records per engine-choice.md below the table)

### Output spec
- Master: <W×H>, <fps> fps, <bit depth> project, codec <…>, colour bt709, audio AAC 48 kHz stereo 320 kb/s
- Preview: 1280×720, same fps, crf ~25 (≈ a few MB/min)
- Recuts: 9:16 (real recut | stacked with approval), 1:1, 4:5, cut-downs 15 s / 30 s
- Captions: .srt side-car + burn-in on vertical

### Build structure
- Project file(s): <path in assets/>, naming `<film>_v<N>.<ext>`
- Comps / compositions / scenes: <list with durations and start times>
- Delivery comp: <e.g. FILM 1920×1080 inside a 2560×1440 comp, collapse on>

### Budget and safety
- Expected render time: master <…> min, preview <…> min (measure on a 5 s proof first)
- Disk: free now <…> GB; expected use <…> GB; cache cap <…> GB; purge before/after: yes
- GPU/CPU: <GPU model / fallback>; known risks (OOM → black frames)
- Fonts installed: <list>; missing: <list>

### Paid items (each needs its own yes before spending)
| Item | Vendor / plan | Price | Licence covers | Needed for |
|---|---|---|---|---|

### Proof render
- 3–5 s at full spec of the hardest shot → `qc_report.py` → evidence.md

### Approval
- [ ] User approved this plan on <date> (→ gates.md `RENDER_PLAN_APPROVED`)
- [ ] Master render approved on <date> (M8)
```
