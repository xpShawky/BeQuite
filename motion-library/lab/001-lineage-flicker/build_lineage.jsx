// Lab 001 - lineage flicker (after Apple Event Sep 2026, 07:10.9: chip generations cut every 3 frames in one position).
// Builds a 1920x1080 30 fps comp: version cards in the exact same place, cuts accelerating (18 -> 3 frames),
// a slow push carried across every cut, then the newest card lands and settles. Saves the .aep; render is separate.
var FPS = 30, W = 1920, H = 1080, DUR = 5;
var VERS = [
  ["v0.1", "alpha",  [0.16, 0.16, 0.18]],
  ["v1",   "lean",   [0.20, 0.27, 0.42]],
  ["v2",   "studio", [0.36, 0.20, 0.42]],
  ["v3",   "light",  [0.13, 0.38, 0.34]],
  ["v3.5", "gates",  [0.45, 0.30, 0.12]],
  ["v3.9", "work",   [0.12, 0.30, 0.50]],
  ["v4",   "Titan",  [0.96, 0.42, 0.10]]
];
var HOLD = [18, 12, 8, 6, 4, 3];          // frames per card before the final one (accelerating)
var START = 15;                            // first card at 0.5 s

app.beginUndoGroup("lab 001");
app.newProject();
var comp = app.project.items.addComp("LINEAGE", W, H, 1, DUR, FPS);
comp.layers.addSolid([0.95, 0.95, 0.95], "paper", W, H, 1, DUR);

var push = comp.layers.addNull(DUR);       // one camera-like push carried across every cut
push.name = "push";
push.property("Position").setValue([W / 2, H / 2]);
push.property("Anchor Point").setValue([50, 50]);
var sc = push.property("Scale");
sc.setValueAtTime(START / FPS, [100, 100]);
var landF = START; for (var h = 0; h < HOLD.length; h++) landF += HOLD[h];
sc.setValueAtTime(landF / FPS, [106, 106]);
sc.setValueAtTime(landF / FPS + 0.7, [100, 100]);   // the land: settle back with an ease
var ez = new KeyframeEase(0, 75);
sc.setTemporalEaseAtKey(3, [ez, ez, ez], [ez, ez, ez]);

function card(i, inF, outF) {
  var v = VERS[i];
  var s = comp.layers.addShape();
  s.name = "card " + v[0];
  var g = s.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
  var rect = g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Rect");
  rect.property("ADBE Vector Rect Size").setValue([1280, 620]);
  rect.property("ADBE Vector Rect Roundness").setValue(64);
  var fill = g.property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill");
  fill.property("ADBE Vector Fill Color").setValue(v[2]);
  s.property("Position").setValue([W / 2, H / 2]);
  var t = comp.layers.addText(v[0]);
  var td = t.property("Source Text").value;
  td.fontSize = 260; td.fillColor = [1, 1, 1]; td.justification = ParagraphJustification.CENTER_JUSTIFY;
  td.font = "Geist-Bold";   // installed here; SF Pro is not (lab finding)
  t.property("Source Text").setValue(td);
  t.property("Position").setValue([W / 2, H / 2 + 40]);
  var sub = comp.layers.addText(v[1]);
  var sd = sub.property("Source Text").value;
  sd.fontSize = 64; sd.font = "Geist-Medium"; sd.fillColor = [1, 1, 1]; sd.justification = ParagraphJustification.CENTER_JUSTIFY;
  sub.property("Source Text").setValue(sd);
  sub.property("Position").setValue([W / 2, H / 2 + 170]);
  var ls = [s, t, sub];
  for (var k = 0; k < ls.length; k++) {
    ls[k].parent = push;
    ls[k].inPoint = inF / FPS;
    ls[k].outPoint = outF / FPS;
  }
}

var f = START;
for (var i = 0; i < VERS.length; i++) {
  var out = (i < HOLD.length) ? f + HOLD[i] : DUR * FPS;
  card(i, f, out);
  f = out;
}
app.endUndoGroup();

var lab = new Folder(AE_ROOT);
var aep = new File(lab.fsName + "/lineage.aep");
app.project.save(aep);
RESULT = { aep: aep.fsName, landFrame: landF, landTime: landF / FPS, cuts: (function () {
  var c = [], g = START; for (var j = 0; j < HOLD.length; j++) { g += HOLD[j]; c.push(g / FPS); } return c; })() };
