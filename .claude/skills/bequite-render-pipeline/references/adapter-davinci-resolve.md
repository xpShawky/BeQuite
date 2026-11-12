# Adapter: DaVinci Resolve (edit, grade, deliver)

Most important first: **Resolve is the right adapter when the film is footage-led or needs a real colour grade and finishing; drive it by script only on a copy of the project, and check which features need the paid Studio version before planning around them.**

- **Best for:** editing filmed footage and screen recordings, colour grading (one grade across AE, 3D and AI shots), audio post (Fairlight), deliver presets for many formats, conforming masters.
- **How an agent drives it:** the Resolve scripting API (Python/Lua: project manager → project → media pool → timeline → render queue) and, per late-2026 reports, a **native MCP server in Resolve Studio 21.1** for edit building, render queue and media organisation (secondary sources; UNVERIFIED in this pack). Computer use for anything the API doesn't expose.
- **Install / licence:** free version and paid Studio. Per the same reports, from 21.1 **external scripting, Workflow Integrations and UIManager are Studio-only**; the free version keeps console scripting; Python 2 support was removed. Verify on Blackmagic's release notes for the installed version.
- **Honest limits:** not a kinetic-type tool (Fusion Text+ can animate per character for Latin; Arabic shaping in Fusion UNVERIFIED); no documented safeguards for destructive operations through the MCP — always duplicate the project or timeline first; GPU-heavy.

## Typical uses in `/bq-motion`

1. **Grade pass:** import the master (or passes) → one grade (lifted blacks, one LUT/curve, consistent grain) → deliver.
2. **Footage edit:** cut b-roll/interview material to the voice; motion graphics come in as alpha overlays from AE/code.
3. **Deliver:** render presets per platform; still re-check every output with `qc_report.py`.

## Scripting sketch (Studio or console; version-dependent — UNVERIFIED)

```python
# Inside Resolve's console, or externally (Studio) with the scripting modules on the Python path per Blackmagic's README.
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()          # work on a duplicate project, never the only copy
media = project.GetMediaPool()
clips = media.ImportMedia(["/abs/path/master.mov"])
timeline = media.CreateTimelineFromClips("grade_v1", clips)
project.SetRenderSettings({"TargetDir": "/abs/out", "CustomName": "film_graded"})
project.AddRenderJob(); project.StartRendering()
```

Read the scripting README shipped with the installed Resolve for exact module paths and method names; they change between versions.

Evidence: script or MCP calls made, render job settings, output path, and the `qc_report.py` block in `evidence.md`.
