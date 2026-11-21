# bq-kinetic/1: the scene description

One JSON object. Double quotes everywhere, no comments, no trailing commas. Fields you leave out take the default.

## Top level

| Field | Type | Default | Meaning |
|---|---|---|---|
| `version` | `"bq-kinetic/1"` | required | Format version. The engine refuses anything else. |
| `title` | string | `"BQ Kinetic"` | The composition name in After Effects. |
| `format` | object | `{"width":1920,"height":1080,"fps":30}` | Frame size and frame rate. 9:16 Reels: `1080` x `1920`. fps: 24, 25, 30, 50 or 60. |
| `tempo` | object | `{"bpm":120,"first_beat":0.5}` | The music: beats per minute (60 to 200) and the second of its first beat. All timing follows this grid. |
| `style` | `"night-gold"`, `"ink-green"`, `"paper"` | `"night-gold"` | The look (fonts, colours, sizes): see PRESETS.md. |
| `music` | string | none | Optional full path to the music file on the user's computer; the engine places it at 0 s. |
| `scenes` | list | required | 1 to 12 scenes, played one after the other. |

## A scene

| Field | Type | Default | Meaning |
|---|---|---|---|
| `rows` | list of rows | required | 1 to 5 rows, top to bottom. A row is a list of 1 to 4 items. |
| `hold_beats` | number | `2` | Beats the finished block stays on screen after its last word lands (1 to 16). |
| `camera` | `"follow"` or `"static"` | `"follow"` | `follow`: the camera sits a little closer (at most 15% closer than the whole block), leans towards each new word and moves with motion blur; the row being built always stays in frame, and the rows above it too whenever they fit. At the slam (or after the last word) it settles on the whole block. `static`: one framing size for the whole scene; the camera only glides gently so the lines built so far stay centred. Calm; good for an opening or an ending. |
| `exit` | `"cut"`, `"fade"`, `"whip-up"` | `"cut"` | How the scene leaves. `whip-up` throws it up out of frame with motion blur. |

## An item: a word or a stack

A **word**:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `text` | string | required (or `parts`) | One word, at most 28 characters. |
| `parts` | list of 2 or 3 `{"text":..., "accent":true/false}` | none | Instead of `text`: one word in two colours, for brand names. Example: `[{"text":"Be"},{"text":"Quite","accent":true}]`. |
| `size` | `"S"`, `"M"`, `"L"`, `"XL"` | `"M"` | S is for small stacked words; XL for the one hero word. |
| `beat` | number | required | When the word lands, in beats from the start of the scene. Whole, half or quarter beats. |
| `accent` | true / false | false | The accent colour. One word per scene at most. |
| `slam` | true / false | false | The word lands big (152% settling to 100%) with a short flash, and the camera pulls back to the whole block at that moment. One per scene, usually the last word. |

A **stack**: 2 or 3 small words stacked one above the other, beside the previous word, e.g. "the" over "most" next to "BeQuite":

```json
{ "stack": [ { "text": "the", "beat": 1 }, { "text": "most", "beat": 1.5 } ] }
```

Stack words default to size `S`; `M` is allowed. A stack reads as one small unit beside the word before it, so keep it to connectors ("the / most", "out / a"). An `M` word in a stack makes the whole row taller and turns the small word above it into something like a superscript; put a phrase like that on its own row instead.

## How the engine builds it (so you can predict the picture)

- Each row is centred. A new word appears right beside the word before it, and the whole row slides to stay centred (the push); words never overlap. A stack grows wider only when a wider stack word lands.
- Rows stack downward with tight leading. The block is as wide as its widest row.
- With `camera: follow`, the camera moves in slightly on the newest row, leans towards each new word, and at the slam (or right after the last word lands) settles so the whole block fills about 80% of the frame. It finishes that move before a `whip-up` or `fade` exit starts, so keep `hold_beats` at 2 or more if the whole block must be read.
- With `camera: static`, the first line starts in the centre of the frame and the block glides up as lines are added; the size never changes.
- A word lands at 118% (a slam at 152%) and settles to 100% in a quarter second, so for an instant a long hero word can touch the frame edges. That is the hit, not a mistake.
- Timing: scene 1 starts at `first_beat`; each next scene starts where the previous one ends (last word beat + `hold_beats`). The film ends exactly when the last scene ends, so its length is `first_beat` + the sum of every scene's (last beat + `hold_beats`) in beats.

## The smallest valid film

```json
{
  "version": "bq-kinetic/1",
  "scenes": [ { "rows": [ [ { "text": "Hello", "size": "XL", "beat": 0 } ] ] } ]
}
```

## Errors you may get back from the panel (and what they mean)

- `scene 2 > row 3 > item 1 ("Faster"): "beat" must be a number...`: the word has no beat or a text beat like "2".
- `... lands on beat 3, before a word that reads earlier (beat 4)`: a later word in reading order lands first; reorder the beats.
- `... two words land 0.06 s apart`: too close to read; spread them at least a quarter beat.
- `style: "neon" is not a preset`: use one of the three presets.
