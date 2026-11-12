# Adapter: Blender (3D)

Most important first: **use Blender for what needs real 3D (devices, products, ribbons, materials, light, depth of field), render passes with alpha, and keep UI, text and logos out of the render** — composite them sharp in the assembly engine. What to aim for creatively: `.claude/skills/bequite-motion-director/references/3d-and-filmed-look.md`.

- **Best for:** product and device shots, extruded logos, ribbons around a product, object transformations inside one continuous camera move, turntables, shadow catchers.
- **How an agent drives it:** Python (`bpy`) scripts run headless (`blender -b scene.blend -P build.py -- args`) or in a live session through an MCP server (official and community Blender MCP servers existed in 2026; some include asset search and text/image-to-3D generation that may cost credits). Inspect before changing a user's scene; never assume names (look nodes up by type, read enum values instead of hardcoding them).
- **Install / licence:** free (GPL); a GPU strongly recommended for Cycles; EEVEE for speed.
- **Honest limits:** taste is on the director; render time grows fast with samples/resolution; text objects and Arabic shaping UNVERIFIED — do type in AE/code; recipes below are practitioner notes, prove each small first.

## Headless use

```bash
blender -b scene.blend -P build.py -- --out renders/ --frames 1-240     # args after "--" go to the script
blender -b scene.blend -o //renders/shot_#### -F PNG -s 1 -e 240 -a     # render a frame range
blender -b scene.blend -f 120                                            # one still for review
```

Set colour management deliberately (view transform, look) and keep it identical across shots; render 16-bit PNG or EXR with alpha; motion blur on with a modest shutter (≈0.5).

## Render passes for assembly

Use view layers or collections with holdouts:
- background (or none: plate added in assembly)
- back elements (ribbons behind the product)
- product
- front elements (ribbons in front)
- shadow catcher
- **screen corners instead of a screen pass**: add four empties at the screen corners (parented to the device), export their 2D positions per frame, and corner-pin the real UI at native resolution in the assembly engine.

```python
# Export screen-corner screen-space coordinates per frame for a corner pin (practitioner sketch; test on a short range first)
import bpy, json
from bpy_extras.object_utils import world_to_camera_view
sc = bpy.context.scene; cam = sc.camera
names = ("SC_TL", "SC_TR", "SC_BL", "SC_BR")
corners = [bpy.data.objects[n] for n in names]
W = sc.render.resolution_x * sc.render.resolution_percentage / 100
H = sc.render.resolution_y * sc.render.resolution_percentage / 100
out = {}
for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    out[f] = [[v.x * W, (1 - v.y) * H] for v in (world_to_camera_view(sc, cam, o.matrix_world.translation) for o in corners)]
json.dump(out, open(bpy.path.abspath("//screen_corners.json"), "w"))
```

## Recipes

- **Camera rig:** camera with a Track To constraint on an animated empty → smooth orbits; or camera on a path. Ease the target, not the camera.
- **Transform inside the move:** on the frame where a foreground surface fills the frame or blur peaks, key visibility (render + viewport, constant interpolation) to swap object A for B; keep the camera moving.
- **Through-object:** put scene B in a separate collection offset in space; fly the camera through an opening of A.
- **Ribbons:**
  1. Curve + flat profile (Extrude, or Bevel → Object with a short line); shape with per-point Tilt and a Taper object; grow by keying Bevel Factor End 0→1 with Spline mapping (check it applies to your curve setup in your version).
  2. Geometry Nodes: Curve → Trim Curve (key End) → Curve to Mesh with a line profile; Set Curve Tilt/Radius for twist and width.
  3. Mesh strip + Curve modifier (slide along the path) + Shrinkwrap (target = product, "Above Surface", small offset) to hug the product + thin Solidify.
  - Look: two-sided colour via a Backfacing-driven mix of two shaders; satin roughness ≈0.3–0.45 with some sheen; Twist Method Minimum/Z-Up against flips; never zero thickness (black edge-on).
- **Pop-out from a screen:** model the element on the screen plane with an identical texture; on the lift frame switch the screen texture to a version without it; add Z, +5–15 % scale and a soft shadow.
- **Extruded logo:** import the official SVG → curve → extrude/bevel; never redraw the mark.
- **Turntable:** product on a slow eased rotation or camera on an empty; shadow catcher floor for compositing.
- **AI-to-3D props:** acceptable for background props after a licence check; never for the hero product (topology, accuracy).

Evidence: render command, frames, elapsed time, and a contact sheet of the passes in `evidence.md`.
