# 3D Assets

> GLB-format models loaded by React Three Fiber components.
>
> The astronaut character lands here as `astronaut.glb` once v0.17.5 ships (the Blender pipeline is currently waiting on the BlenderMCP add-on to respond).

## Expected files

| File | Used by | Animations |
|---|---|---|
| `astronaut.glb` | `components/three/AgentCharacter3D.tsx` | `Idle.Breathe`, `Idle.Wave`, `Idle.Point`, `Idle.Float` |
| `mark.glb` | `components/three/MarkRotation.tsx` (v0.17.6+) | `Spin` |

## Production rules

- Keep each GLB under **3 MB** (compressed gLTF; use `glTF-Transform` + Draco compression).
- Embed PBR materials; use the brand palette in `studio/brand/tokens.css`.
- Each animation loop **MUST** be cleanly cyclical (no pop at the wrap point).
- Test in `studio/marketing/components/three/AgentCharacter3D.tsx` before committing.

## Blender export settings (when v0.17.5 ships)

When exporting from Blender:

- Format: **glTF Binary (.glb)**
- Include: **Selected Objects** (not the whole scene — keep size down).
- Geometry: Apply Modifiers ✓, UVs ✓, Normals ✓, Tangents ✓, Vertex Colors ✓
- Materials: **Export** (with Image option set to "AUTO" or "JPEG" for size).
- Animation: **Limit to Playback Range** ✓, **Always Sample Animations** ✓, **Group by NLA Track** ✓
- Compression: **Draco mesh compression** ✓ (compression level 10).
