// core.jsx - After Effects helper library for films built 100 % from script (ExtendScript / ES3).
// Everything is namespaced in K. Load it from a build script:  $.evalFile(new File(AE_ROOT + "/lib/core.jsx"));
// AE_ROOT is defined by runae.js. ES3 only: no let/const, no arrow functions, no native JSON (json2.jsx is preloaded).
//
// Style is NOT baked in. Call K.config({...}) with the tokens from the film's Motion DNA (colours, fonts, size, fps).
// Defaults below are neutral placeholders so a starter build runs on any machine.
var K = {};
K.W = 1920; K.H = 1080; K.FPS = 60;
K.ROOT = (typeof AE_ROOT !== "undefined") ? AE_ROOT : Folder.current.fsName;
K.PROJECT = "bequite-film";            // marker folder name; also used by K.newProject's guard
// colour tokens (replace from the Motion DNA): neutral stage + ONE accent
K.C = { ink: "#1A1A1A", paper: "#F2F2F2", deep: "#141414", surface: "#262626", soft: "#A0A0A0", mute: "#6E6E6E",
        border: "#D6D6D6", acc: "#2F6BFF", acc2: "#7FA4FF", red: "#E5484D", white: "#FFFFFF",
        mist1: "#F7F7F7", mist2: "#E6E6E6" };
// font tokens = installed PostScript names (AE text layers need installed fonts). Replace from the Motion DNA.
K.F = { reg: "ArialMT", med: "ArialMT", semi: "Arial-BoldMT", bold: "Arial-BoldMT", light: "ArialMT",
        mono: "CourierNewPSMT", monoReg: "CourierNewPSMT" };

// K.config({ W, H, FPS, name, C: {...}, F: {...} }) - merge project tokens
K.config = function (o) {
  o = o || {};
  if (o.W) K.W = o.W; if (o.H) K.H = o.H; if (o.FPS) K.FPS = o.FPS; if (o.name) K.PROJECT = o.name;
  var k;
  if (o.C) for (k in o.C) if (o.C.hasOwnProperty(k)) K.C[k] = o.C[k];
  if (o.F) for (k in o.F) if (o.F.hasOwnProperty(k)) K.F[k] = o.F[k];
  K.PAL = K.palette();
  return K;
};

K.col = function (hex) {
  hex = hex.replace("#", "");
  return [parseInt(hex.substr(0, 2), 16) / 255, parseInt(hex.substr(2, 2), 16) / 255, parseInt(hex.substr(4, 2), 16) / 255];
};
K.col4 = function (hex, a) { var c = K.col(hex); c.push(a === undefined ? 1 : a); return c; };

// ---------- project ----------
K.folder = null;
K.items = {};
// Start a clean project for this film.
// Guard (fixed): it refuses ONLY when the open project has unsaved changes and is not this film's project.
// A saved, clean project (any name, any version number) is closed without loss. "Ours" = the project contains the
// marker folder K.PROJECT, or its file name matches o.filePattern (RegExp). o.force = true closes without asking.
// (The earlier guard used a one-digit version regex, so a clean saved "..._v13.aep" was wrongly refused.)
K.newProject = function (o) {
  o = o || {};
  if (o.name) K.PROJECT = o.name;
  var p = app.project;
  if (p) {
    var ours = false, i;
    if (p.file && o.filePattern && o.filePattern.test(p.file.name)) ours = true;
    for (i = 1; i <= p.numItems && !ours; i++) {
      var it = p.item(i);
      if (it instanceof FolderItem && it.name == K.PROJECT) ours = true;
    }
    if (p.dirty && !ours && !o.force) {
      throw new Error("After Effects has unsaved changes in another project" + (p.file ? " (" + p.file.name + ")" : "") +
        ". Save or close it first, or call K.newProject({force: true}) to discard them.");
    }
    p.close(CloseOptions.DO_NOT_SAVE_CHANGES);
  }
  app.newProject();
  app.project.bitsPerChannel = o.bpc || 16;   // 16 bpc + AE dither on output: no banding in dark gradients
  K.items = {};
  K.folder = app.project.items.addFolder(K.PROJECT);
  K.fFoot = app.project.items.addFolder("footage"); K.fFoot.parentFolder = K.folder;
  K.fPre = app.project.items.addFolder("precomps"); K.fPre.parentFolder = K.folder;
  if (!K.PAL) K.PAL = K.palette();
};

K.comp = function (name, dur, w, h, bg, isPre) {
  var c = app.project.items.addComp(name, w || K.W, h || K.H, 1, dur, K.FPS);
  c.motionBlur = true; c.shutterAngle = 200; c.shutterPhase = -100;
  c.motionBlurSamplesPerFrame = 16; c.motionBlurAdaptiveSampleLimit = 128;
  c.bgColor = K.col(bg || "#FFFFFF");
  c.parentFolder = isPre ? K.fPre : K.folder;
  K.items[name] = c;
  return c;
};

// footage relative to AE_ROOT (or an absolute path)
K.foot = function (rel) {
  if (K.items["F:" + rel]) return K.items["F:" + rel];
  var f0 = new File(rel);
  var file = (f0.exists && (rel.charAt(0) == "/" || rel.charAt(1) == ":")) ? f0 : new File(K.ROOT + "/" + rel);
  if (!file.exists) throw new Error("footage not found: " + file.fsName);
  var f = app.project.importFile(new ImportOptions(file)); f.parentFolder = K.fFoot;
  K.items["F:" + rel] = f;
  return f;
};

// ---------- layers ----------
K.solid = function (comp, hex, name, w, h) {
  return comp.layers.addSolid(K.col(hex), name || "bg", w || comp.width, h || comp.height, 1);
};
// soft radial "mist" background
K.mistBG = function (comp, c1, c2) {
  var l = K.solid(comp, c1 || K.C.mist1, "bg");
  var r = l.property("ADBE Effect Parade").addProperty("ADBE Ramp");
  r.property("ADBE Ramp-0001").setValue([comp.width * 0.5, comp.height * 0.42]);
  r.property("ADBE Ramp-0002").setValue(K.col4(c1 || K.C.mist1));
  r.property("ADBE Ramp-0003").setValue([comp.width * 1.05, comp.height * 1.25]);
  r.property("ADBE Ramp-0004").setValue(K.col4(c2 || K.C.mist2));
  r.property("ADBE Ramp-0005").setValue(2);  // radial
  try { r.property("ADBE Ramp-0006").setValue(20); } catch (e) {} // ramp scatter (fights banding)
  l.locked = true;
  return l;
};
K.nul = function (comp, name, pos) {
  var n = comp.layers.addNull(); n.name = name; n.enabled = false;
  if (pos) n.property("ADBE Transform Group").property("ADBE Position").setValue(pos);
  return n;
};
K.tr = function (l, name) {
  var map = { pos: "ADBE Position", scale: "ADBE Scale", rot: "ADBE Rotate Z", op: "ADBE Opacity", anchor: "ADBE Anchor Point" };
  return l.property("ADBE Transform Group").property(map[name] || name);
};
K.span = function (l, t0, t1) { l.inPoint = Math.max(0, t0); l.outPoint = t1; return l; };

// ---------- keyframes & easing ----------
// curve names: "expo" (fast start, long soft landing), "inout", "whip" (slow-fast-slow, strong), "in" (accelerate away),
// "soft", "lin", "hold".  Values are [outgoing influence %, incoming influence %].
K.CURVES = { expo: [6, 92], inout: [60, 60], whip: [85, 85], "in": [80, 4], soft: [33, 75], lin: null, hold: null };
K.dims = function (p) {
  var t = p.propertyValueType;
  if (t == PropertyValueType.TwoD) return 2;
  if (t == PropertyValueType.ThreeD) return 3;
  return 1;
};
K.ease = function (p, k, inInf, outInf) {
  var n = K.dims(p), a = [], b = [];
  for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, Math.max(0.1, inInf))); b.push(new KeyframeEase(0, Math.max(0.1, outInf))); }
  p.setTemporalEaseAtKey(k, a, b);
};
// keys: [[t, value, curveToNext], ...]  (the curve of the last key is ignored)
K.keys = function (p, keys) {
  var i;
  for (i = 0; i < keys.length; i++) p.addKey(keys[i][0]);
  for (i = 0; i < keys.length; i++) p.setValueAtKey(p.nearestKeyIndex(keys[i][0]), keys[i][1]);
  for (i = 0; i < keys.length; i++) {
    var k = p.nearestKeyIndex(keys[i][0]);
    var cOut = keys[i][2] || "expo", cIn = i > 0 ? (keys[i - 1][2] || "expo") : "expo";
    if (cOut == "hold") {
      // a hold key still needs its INCOMING ease, or the move into it falls back to AE's default curve
      var easedIn = i > 0 && cIn != "lin" && cIn != "hold";
      p.setInterpolationTypeAtKey(k, easedIn ? KeyframeInterpolationType.BEZIER : p.keyInInterpolationType(k), KeyframeInterpolationType.HOLD);
      if (easedIn) { try { K.ease(p, k, K.CURVES[cIn] ? K.CURVES[cIn][1] : 33, 33); } catch (e) {} }
      continue;
    }
    if (cOut == "lin" && cIn == "lin") { p.setInterpolationTypeAtKey(k, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); continue; }
    var outInf = K.CURVES[cOut] ? K.CURVES[cOut][0] : 0.1;
    var inInf = K.CURVES[cIn] ? K.CURVES[cIn][1] : 0.1;
    if (i == 0) inInf = 33; if (i == keys.length - 1) outInf = 33;
    K.ease(p, k, inInf, outInf);
    try { if (p.isSpatial) { p.setSpatialAutoBezierAtKey(k, false); p.setSpatialContinuousAtKey(k, false); p.setSpatialTangentsAtKey(k, [0, 0, 0], [0, 0, 0]); } } catch (e) {}
  }
  return p;
};
K.go = function (p, t0, v0, t1, v1, curve) { return K.keys(p, [[t0, v0, curve || "expo"], [t1, v1]]); };
// landing with a small overshoot (spring look without expressions). Use only on things that land.
K.spring = function (p, t0, v0, t1, v1, over) {
  over = over === undefined ? 0.07 : over;
  var vo, i;
  if (v1 instanceof Array) { var n = Math.min(v0.length, v1.length); v0 = v0.slice(0, n); v1 = v1.slice(0, n); vo = []; for (i = 0; i < n; i++) vo.push(v1[i] + (v1[i] - v0[i]) * over); }
  else vo = v1 + (v1 - v0) * over;
  var tm = t0 + (t1 - t0) * 0.58;
  return K.keys(p, [[t0, v0, "expo"], [tm, vo, "inout"], [t1, v1]]);
};
K.fade = function (l, t0, t1, a0, a1, curve) { return K.go(K.tr(l, "op"), t0, a0, t1, a1, curve || "inout"); };
// constant gentle drift (camera breathing, 0.5-1 % of frame). Nothing is ever fully static.
K.drift = function (l, px, py, speed) {
  K.tr(l, "pos").expression = "add(value, [Math.sin(time*" + (speed || 0.35) + ")*" + (px || 6) + ", Math.cos(time*" + ((speed || 0.35) * 0.8) + ")*" + (py || 4) + "])";
};
// scale punch on an emphasis layer: from -> 100 % with a strong ease-out
K.punch = function (l, t, from, dur) {
  var f = from || 125;
  return K.keys(K.tr(l, "scale"), [[t, [f, f], "expo"], [t + (dur || 0.35), [100, 100]]]);
};

// ---------- text ----------
// o: font, size, color, tracking (1/1000 em), just ("left"|"center"|"right"), pos [x,y], leading, name
K.text = function (comp, str, o) {
  o = o || {};
  var l = comp.layers.addText(str);
  var tp = l.property("ADBE Text Properties").property("ADBE Text Document");
  var td = tp.value;
  td.resetCharStyle(); td.resetParagraphStyle();
  td.font = o.font || K.F.semi; td.fontSize = o.size || 80;
  td.applyFill = true; td.fillColor = K.col(o.color || K.C.ink);
  td.applyStroke = false; td.tracking = o.tracking === undefined ? -20 : o.tracking;
  td.justification = o.just == "left" ? ParagraphJustification.LEFT_JUSTIFY : (o.just == "right" ? ParagraphJustification.RIGHT_JUSTIFY : ParagraphJustification.CENTER_JUSTIFY);
  if (o.leading) { td.autoLeading = false; td.leading = o.leading; }
  tp.setValue(td);
  l.name = o.name || str.substr(0, 24);
  var r = l.sourceRectAtTime(0, false);
  if (o.just == "left" || o.just == "right") K.tr(l, "anchor").setValue([0, 0]);
  else K.tr(l, "anchor").setValue([r.left + r.width / 2, r.top + r.height / 2]);
  if (o.pos) K.tr(l, "pos").setValue(o.pos);
  l.motionBlur = true;
  return l;
};
K.textRect = function (l) { return l.sourceRectAtTime(0, false); };
K.setText = function (l, str) {
  var tp = l.property("ADBE Text Properties").property("ADBE Text Document"); var td = tp.value; td.text = str; tp.setValue(td);
};
K.lastAnim = function (l) { var an = l.property("ADBE Text Properties").property("ADBE Text Animators"); return an.property(an.numProperties); };
K.ap = function (l) { return K.lastAnim(l).property("ADBE Text Animator Properties"); };
K.lastSel = function (l) { return K.lastAnim(l).property("ADBE Text Selectors").property(1); };

// Text animator: hidden -> visible, sweeping by character / word / line.
// mode: "blur" (opacity+blur+rise), "rise" (rise only, pair with a mask), "smear" (side travel + horizontal blur), "pop" (scale from 0)
// o.by: "char" (default) | "word" | "line". Use "word" for connected scripts (Arabic) - see bequite-kinetic-type.
K.byIndex = function (by) { return by == "word" ? 3 : (by == "line" ? 4 : 2); }; // 2 = characters excluding spaces
K.reveal = function (l, t0, dur, mode, o) {
  o = o || {};
  var anim = l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  anim.name = "reveal";
  var size = o.size || 80;
  if (mode == "blur" || mode == "smear" || mode == "pop" || o.fade !== false) K.ap(l).addProperty("ADBE Text Opacity").setValue(0);
  if (mode == "blur") { K.ap(l).addProperty("ADBE Text Blur").setValue([o.blur || 22, o.blur || 22]); K.ap(l).addProperty("ADBE Text Position 3D").setValue([0, size * 0.35, 0]); }
  if (mode == "rise") K.ap(l).addProperty("ADBE Text Position 3D").setValue([0, size * 1.15, 0]);
  if (mode == "smear") { K.ap(l).addProperty("ADBE Text Position 3D").setValue([o.dx || 260, 0, 0]); K.ap(l).addProperty("ADBE Text Blur").setValue([60, 0]); }
  if (mode == "pop") { K.ap(l).addProperty("ADBE Text Scale 3D").setValue([0, 0, 100]); }
  if (o.track) K.ap(l).addProperty("ADBE Text Tracking Amount").setValue(o.track);
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  var adv = function () { return K.lastSel(l).property("ADBE Text Range Advanced"); };
  adv().property("ADBE Text Range Type2").setValue(K.byIndex(o.by));
  adv().property("ADBE Text Range Shape").setValue(2);   // ramp up
  adv().property("ADBE Text Levels Max Ease").setValue(o.easeHi === undefined ? 50 : o.easeHi);
  adv().property("ADBE Text Levels Min Ease").setValue(o.easeLo === undefined ? 50 : o.easeLo);
  var w = o.width || 40; // softness of the sweep in %
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0);
  K.lastSel(l).property("ADBE Text Percent End").setValue(w);
  K.go(K.lastSel(l).property("ADBE Text Percent Offset"), t0, -w, t0 + dur, 100, o.curve || "soft");
  return anim;
};
// Reverse: visible -> hidden (exit)
K.hide = function (l, t0, dur, mode, o) {
  o = o || {};
  var anim = l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  anim.name = "hide";
  var size = o.size || 80;
  K.ap(l).addProperty("ADBE Text Opacity").setValue(0);
  if (mode == "blur") { K.ap(l).addProperty("ADBE Text Blur").setValue([18, 18]); K.ap(l).addProperty("ADBE Text Position 3D").setValue([0, -size * 0.3, 0]); }
  if (mode == "rise") K.ap(l).addProperty("ADBE Text Position 3D").setValue([0, -size * 1.15, 0]);
  if (mode == "smear") { K.ap(l).addProperty("ADBE Text Position 3D").setValue([-(o.dx || 260), 0, 0]); K.ap(l).addProperty("ADBE Text Blur").setValue([60, 0]); }
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  var adv = function () { return K.lastSel(l).property("ADBE Text Range Advanced"); };
  adv().property("ADBE Text Range Type2").setValue(K.byIndex(o.by));
  adv().property("ADBE Text Range Shape").setValue(2);
  var w = o.width || 40;
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0);
  K.lastSel(l).property("ADBE Text Percent End").setValue(w);
  // ramp up: sweep from "none selected" (offset 100) to "all selected" (offset -w)
  K.go(K.lastSel(l).property("ADBE Text Percent Offset"), t0, 100, t0 + dur, -w, o.curve || "in");
  return anim;
};
// rectangular mask on a layer in its own coordinates (for mask slide-up reveals)
K.maskRect = function (l, x, y, w, h, feather) {
  var m = l.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
  var s = new Shape(); s.vertices = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; s.closed = true;
  m.property("ADBE Mask Shape").setValue(s);
  if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
  return m;
};

// ---------- shapes ----------
// re-fetch the contents of the last group of a shape layer (property references die when properties are added)
K.gc = function (l) { var root = l.property("ADBE Root Vectors Group"); return root.property(root.numProperties).property("ADBE Vectors Group"); };
// returns {layer, size, round, fill, stroke, trim, start, end}
K.rect = function (comp, name, w, h, o) {
  o = o || {};
  var l = comp.layers.addShape(); l.name = name;
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"); g.name = "box";
  var r = g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Rect");
  r.property("ADBE Vector Rect Size").setValue([w, h]);
  r.property("ADBE Vector Rect Roundness").setValue(o.radius || 0);
  if (o.fill) K.gc(l).addProperty("ADBE Vector Graphic - Fill");
  if (o.stroke) K.gc(l).addProperty("ADBE Vector Graphic - Stroke");
  if (o.trim) K.gc(l).addProperty("ADBE Vector Filter - Trim");
  if (o.pos) K.tr(l, "pos").setValue(o.pos);
  l.motionBlur = true;
  var cc = K.gc(l), rr = cc.property("ADBE Vector Shape - Rect");
  var res = { layer: l, size: rr.property("ADBE Vector Rect Size"), round: rr.property("ADBE Vector Rect Roundness") };
  if (o.fill) {
    res.fill = cc.property("ADBE Vector Graphic - Fill");
    res.fill.property("ADBE Vector Fill Color").setValue(K.col(o.fill));
    if (o.fillOpacity !== undefined) res.fill.property("ADBE Vector Fill Opacity").setValue(o.fillOpacity);
  }
  if (o.stroke) {
    res.stroke = cc.property("ADBE Vector Graphic - Stroke");
    res.stroke.property("ADBE Vector Stroke Color").setValue(K.col(o.stroke));
    res.stroke.property("ADBE Vector Stroke Width").setValue(o.strokeW || 2);
  }
  if (o.trim) { res.trim = cc.property("ADBE Vector Filter - Trim"); res.end = res.trim.property("ADBE Vector Trim End"); res.start = res.trim.property("ADBE Vector Trim Start"); }
  return res;
};
// "marching ants" outline: a crawling dashed guide element (one of many possible guide elements). Size via .size
K.marquee = function (comp, name, w, h, o) {
  o = o || {};
  var l = comp.layers.addShape(); l.name = name || "marquee";
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"); g.name = "ants";
  g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size").setValue([w, h]);
  var sw = o.width || 2.5;
  K.gc(l).addProperty("ADBE Vector Graphic - Stroke");
  K.gc(l).addProperty("ADBE Vector Graphic - Stroke");
  K.gc(l).addProperty("ADBE Vector Filter - Trim");
  // shape contents draw top-of-list on top: the dashed dark stroke (2) sits over the solid light stroke (3)
  var s2 = K.gc(l).property(2);
  s2.property("ADBE Vector Stroke Color").setValue(K.col(o.dark || K.C.ink)); s2.property("ADBE Vector Stroke Width").setValue(sw);
  var s1 = K.gc(l).property(3);
  s1.property("ADBE Vector Stroke Color").setValue(K.col(o.light || "#FFFFFF")); s1.property("ADBE Vector Stroke Width").setValue(sw);
  // dash slots must exist (Dash, Gap, Offset) before the Offset gets an expression
  K.gc(l).property(2).property("ADBE Vector Stroke Dashes").addProperty("ADBE Vector Stroke Dash 1");
  K.gc(l).property(2).property("ADBE Vector Stroke Dashes").addProperty("ADBE Vector Stroke Gap 1");
  K.gc(l).property(2).property("ADBE Vector Stroke Dashes").addProperty("ADBE Vector Stroke Offset");
  var d = K.gc(l).property(2).property("ADBE Vector Stroke Dashes");
  d.property("ADBE Vector Stroke Dash 1").setValue(o.dash || 9);
  d.property("ADBE Vector Stroke Gap 1").setValue(o.dash || 9);
  K.gc(l).property(2).property("ADBE Vector Stroke Dashes").property("ADBE Vector Stroke Offset").expression = "time*-" + (o.speed || 40);
  if (o.pos) K.tr(l, "pos").setValue(o.pos);
  l.motionBlur = false; // crawling dashes must stay crisp
  var cc = K.gc(l), tr = cc.property("ADBE Vector Filter - Trim");
  return { layer: l, size: cc.property("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size"), trim: tr, start: tr.property("ADBE Vector Trim Start"), end: tr.property("ADBE Vector Trim End") };
};
// line path in comp coordinates (arrows, underlines, guides). Returns {layer, stroke, start, end, path}
K.line = function (comp, name, pts, o) {
  o = o || {};
  var l = comp.layers.addShape(); l.name = name;
  K.tr(l, "pos").setValue([0, 0]);
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
  var p = g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Group");
  var s = new Shape(); s.vertices = pts; s.closed = !!o.closed; p.property("ADBE Vector Shape").setValue(s);
  K.gc(l).addProperty("ADBE Vector Graphic - Stroke");
  if (o.fill) K.gc(l).addProperty("ADBE Vector Graphic - Fill");
  K.gc(l).addProperty("ADBE Vector Filter - Trim");
  var cc = K.gc(l), st = cc.property("ADBE Vector Graphic - Stroke");
  st.property("ADBE Vector Stroke Color").setValue(K.col(o.color || K.C.ink));
  st.property("ADBE Vector Stroke Width").setValue(o.width || 4);
  st.property("ADBE Vector Stroke Line Cap").setValue(2); // round
  st.property("ADBE Vector Stroke Line Join").setValue(2);
  if (o.fill) cc.property("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue(K.col(o.fill));
  l.motionBlur = true;
  cc = K.gc(l); var tr = cc.property("ADBE Vector Filter - Trim");
  return { layer: l, stroke: cc.property("ADBE Vector Graphic - Stroke"), end: tr.property("ADBE Vector Trim End"), start: tr.property("ADBE Vector Trim Start"), path: cc.property("ADBE Vector Shape - Group").property("ADBE Vector Shape") };
};
K.ellipse = function (comp, name, w, h, o) {
  o = o || {};
  var l = comp.layers.addShape(); l.name = name;
  var g = l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
  g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([w, h]);
  if (o.fill) K.gc(l).addProperty("ADBE Vector Graphic - Fill");
  if (o.stroke) K.gc(l).addProperty("ADBE Vector Graphic - Stroke");
  if (o.trim) K.gc(l).addProperty("ADBE Vector Filter - Trim");
  if (o.pos) K.tr(l, "pos").setValue(o.pos);
  l.motionBlur = true;
  var cc = K.gc(l);
  var res = { layer: l, size: cc.property("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size") };
  if (o.fill) { res.fill = cc.property("ADBE Vector Graphic - Fill"); res.fill.property("ADBE Vector Fill Color").setValue(K.col(o.fill)); }
  if (o.stroke) { res.stroke = cc.property("ADBE Vector Graphic - Stroke"); res.stroke.property("ADBE Vector Stroke Color").setValue(K.col(o.stroke)); res.stroke.property("ADBE Vector Stroke Width").setValue(o.strokeW || 4); }
  if (o.trim) { var t = cc.property("ADBE Vector Filter - Trim"); res.end = t.property("ADBE Vector Trim End"); res.start = t.property("ADBE Vector Trim Start"); }
  return res;
};
// soft drop shadow (one shadow recipe per film)
K.shadow = function (l, opacity, dist, soft) {
  var e = l.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
  e.property("ADBE Drop Shadow-0001").setValue(K.col4("#0B0B0F"));
  e.property("ADBE Drop Shadow-0002").setValue(opacity === undefined ? 40 : opacity * 2.55);
  e.property("ADBE Drop Shadow-0003").setValue(180);
  e.property("ADBE Drop Shadow-0004").setValue(dist === undefined ? 24 : dist);
  e.property("ADBE Drop Shadow-0005").setValue(soft === undefined ? 60 : soft);
  return e;
};
K.gblur = function (l, amount) {
  var e = l.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
  e.property("ADBE Gaussian Blur 2-0001").setValue(amount || 0);
  e.property("ADBE Gaussian Blur 2-0003").setValue(1); // repeat edge pixels
  return e.property("ADBE Gaussian Blur 2-0001");
};
// place a precomp/footage in a comp
K.place = function (comp, item, pos, scale, name) {
  var l = comp.layers.add(item);
  if (name) l.name = name;
  if (pos) K.tr(l, "pos").setValue(pos);
  if (scale !== undefined) K.tr(l, "scale").setValue([scale, scale]);
  l.motionBlur = true;
  return l;
};
// identity null (anchor 0,0 at 0,0) so parenting does not move children
K.ident = function (comp, name) {
  var n = comp.layers.addNull(); n.name = name; n.enabled = false;
  K.tr(n, "anchor").setValue([0, 0]); K.tr(n, "pos").setValue([0, 0]);
  return n;
};

// ---------- backgrounds ----------
// Palettes derived from the colour tokens: "light" (paper stage) and "dark" (deep stage).
K.palette = function () {
  return { light: { base: K.C.paper, center: K.C.mist1, edge: K.C.mist2, glow: "#FFFFFF" },
           dark: { base: K.C.deep, center: K.C.surface, edge: "#0A0A0A", glow: K.C.surface } };
};
K.PAL = null;
// Quiet living background: soft vignette + optional slowly drifting light pool + constant grain. No blobs, no hue washes.
// One precomp per palette for the whole film; place it in each scene at -sceneStart so it flows across cuts.
K.bgComp = function (name, o) {
  o = o || {};
  if (!K.PAL) K.PAL = K.palette();
  var key = "BG " + name;
  if (K.items[key]) return K.items[key];
  var p = K.PAL[name], c = K.comp(key, o.dur || 120, 0, 0, p.base, true);
  var v = K.solid(c, p.base, "vignette");
  var r = v.property("ADBE Effect Parade").addProperty("ADBE Ramp");
  r.property("ADBE Ramp-0001").setValue([c.width / 2, c.height * 0.44]); r.property("ADBE Ramp-0002").setValue(K.col4(p.center));
  r.property("ADBE Ramp-0003").setValue([c.width / 2 + c.width * 0.68, c.height * 0.44 + c.height * 0.66]); r.property("ADBE Ramp-0004").setValue(K.col4(p.edge));
  r.property("ADBE Ramp-0005").setValue(2); try { r.property("ADBE Ramp-0006").setValue(30); } catch (e) {}
  if (o.pool !== false) {
    var pool = K.ellipse(c, "light pool", c.width * 0.57, c.height * 0.74, { fill: p.glow, pos: [c.width * 0.4, c.height * 0.39] });
    K.tr(pool.layer, "op").setValue(name == "dark" ? 35 : 55); pool.layer.motionBlur = false;
    K.tr(pool.layer, "pos").expression = "add(value,[Math.sin(time*0.12)*" + Math.round(c.width * 0.135) + ",Math.cos(time*0.09)*" + Math.round(c.height * 0.11) + "])";
    var soft = c.layers.addSolid([0.5, 0.5, 0.5], "soften", c.width, c.height, 1); soft.adjustmentLayer = true; K.gblur(soft, 300);
  }
  var g = c.layers.addSolid([0.5, 0.5, 0.5], "grain", c.width, c.height, 1);
  g.adjustmentLayer = true;
  g.property("ADBE Effect Parade").addProperty("ADBE Noise").property(1).setValue(name == "dark" ? 1.6 : 0.9);
  K.items[key] = c;
  return c;
};
K.bg = function (comp, name, sceneStart, o) {
  var l = comp.layers.add(K.bgComp(name, o)); l.startTime = -(sceneStart || 0); l.name = "bg " + name;
  l.moveToEnd(); l.locked = true; l.motionBlur = false;
  return l;
};

// keyframes along a curved path (arc), middle key roving for constant speed
K.arc = function (p, t0, p0, t1, p1, bend, curve) {
  var mid = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2];
  var dx = p1[0] - p0[0], dy = p1[1] - p0[1], len = Math.sqrt(dx * dx + dy * dy) || 1;
  mid = [mid[0] - dy / len * bend, mid[1] + dx / len * bend];
  p.addKey(t0); p.addKey((t0 + t1) / 2); p.addKey(t1);
  p.setValueAtKey(p.nearestKeyIndex(t0), p0);
  p.setValueAtKey(p.nearestKeyIndex((t0 + t1) / 2), mid);
  p.setValueAtKey(p.nearestKeyIndex(t1), p1);
  var k0 = p.nearestKeyIndex(t0), km = p.nearestKeyIndex((t0 + t1) / 2), k1 = p.nearestKeyIndex(t1);
  p.setSpatialAutoBezierAtKey(km, true); p.setSpatialContinuousAtKey(km, true);
  p.setRovingAtKey(km, true);
  var c = K.CURVES[curve || "inout"];
  K.ease(p, k0, 33, c[0]); K.ease(p, k1, c[1], 33);
  return p;
};

// letter pop: each character scales up from nothing, bumps past 100 %, settles
K.pop = function (l, t0, dur, o) {
  o = o || {};
  K.reveal(l, t0, dur, "pop", { width: o.width || 12, curve: "lin", by: o.by });
  K.lastSel(l).property("ADBE Text Range Advanced").property("ADBE Text Levels Max Ease").setValue(0);
  l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  K.lastAnim(l).name = "bump";
  K.ap(l).addProperty("ADBE Text Scale 3D").setValue([o.bump || 128, o.bump || 128, 100]);
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  var adv = function () { return K.lastSel(l).property("ADBE Text Range Advanced"); };
  adv().property("ADBE Text Range Type2").setValue(K.byIndex(o.by));
  adv().property("ADBE Text Range Shape").setValue(6); // smooth
  var w2 = o.bumpWidth || 26;
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0);
  K.lastSel(l).property("ADBE Text Percent End").setValue(w2);
  K.keys(K.lastSel(l).property("ADBE Text Percent Offset"), [[t0 + 0.02, -w2, "lin"], [t0 + dur + 0.12, 100]]);
  try { l.property("ADBE Text Properties").property("ADBE Text More Options").property("ADBE Text Anchor Point Align").setValue([0, -40]); } catch (e) {}
};
// light passing over text (right -> left by default; o.ltr for left -> right)
K.shine = function (l, t0, dur, hex, o) {
  o = o || {};
  l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  K.lastAnim(l).name = "shine";
  K.ap(l).addProperty("ADBE Text Fill Color").setValue(K.col(hex || "#FFFFFF"));
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  K.lastSel(l).property("ADBE Text Range Advanced").property("ADBE Text Range Shape").setValue(6);
  var w = o.width || 40;
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0);
  K.lastSel(l).property("ADBE Text Percent End").setValue(w);
  if (o.ltr) K.go(K.lastSel(l).property("ADBE Text Percent Offset"), t0, -w, t0 + dur, 100, "inout");
  else K.go(K.lastSel(l).property("ADBE Text Percent Offset"), t0, 100, t0 + dur, -w, "inout");
};

// mouse pointer (arrow) + click ripple
K.cursor = function (comp, name) {
  var c = K.line(comp, name || "cursor", [[0, 0], [0, 34], [9, 26], [15, 40], [21, 37], [15, 24], [27, 24]], { closed: true, fill: "#FFFFFF", color: "#000000", width: 2 });
  K.shadow(c.layer, 35, 3, 8);
  return c.layer;
};
K.click = function (comp, cur, pos, t, color) {
  K.keys(K.tr(cur, "scale"), [[t - 0.05, [100, 100], "inout"], [t, [82, 82], "expo"], [t + 0.22, [100, 100]]]);
  var r = K.ellipse(comp, "ripple", 12, 12, { stroke: color || K.C.acc, strokeW: 3, pos: pos });
  K.go(r.size, t, [12, 12], t + 0.45, [70, 70], "expo");
  K.fade(r.layer, t, t + 0.45, 90, 0, "expo");
  r.layer.inPoint = t; r.layer.outPoint = t + 0.5;
};
// arrowhead marker: a triangle with a notched base
K.arrowhead = function (comp, name, size, hex) {
  var s = size || 40;
  return K.line(comp, name, [[0, 0], [-s, -s * 0.55], [-s * 0.72, 0], [-s, s * 0.55]], { closed: true, fill: hex || "#000000", color: hex || "#000000", width: 1 });
};
K.imgLayer = function (comp, rel, pos, scale, name) { return K.place(comp, K.foot(rel), pos, scale, name); };
// show a layer only between t0 and t1 with short crossfades
K.window = function (l, t0, t1, fade) {
  fade = fade === undefined ? 0.08 : fade;
  var ks = [];
  if (t0 > 0) ks.push([t0 - fade, 0, "inout"], [t0, 100, "inout"]); else ks.push([0, 100, "inout"]);
  if (t1 !== null && t1 !== undefined) ks.push([t1, 100, "inout"], [t1 + fade, 0]);
  K.keys(K.tr(l, "op"), ks);
};
// children of a group null. AE parenting passes transforms ONLY (not opacity, not in/out points): animate the children.
K.kids = function (comp, root) {
  var out = [];
  for (var i = 1; i <= comp.numLayers; i++) { var l = comp.layer(i); if (l.parent && l.parent.index == root.index) out.push(l); }
  return out;
};
K.groupOp = function (comp, root, keys) { var k = K.kids(comp, root); for (var i = 0; i < k.length; i++) K.keys(K.tr(k[i], "op"), keys); };
K.groupSpan = function (comp, root, t0, t1) {
  var k = K.kids(comp, root);
  for (var i = 0; i < k.length; i++) { if (t0 !== null) k[i].inPoint = t0; if (t1 !== null) k[i].outPoint = t1; }
  if (t0 !== null) root.inPoint = t0;
};

// save stills for review. times: array of seconds. saveFrameToPng is asynchronous: poll for the files before using them.
// Pass `times` explicitly every run (globals such as STILLS persist inside AE's scripting engine between runs).
K.stills = function (comp, times, dir) {
  var d = new Folder(dir || (K.ROOT + "/build/stills")); if (!d.exists) d.create();
  var out = [];
  for (var s = 0; s < times.length; s++) {
    var f = new File(d.fsName + "/t" + ("000000" + Math.round(times[s] * 100)).slice(-6) + ".png");
    comp.saveFrameToPng(times[s], f); out.push(f.fsName);
  }
  return out;
};
