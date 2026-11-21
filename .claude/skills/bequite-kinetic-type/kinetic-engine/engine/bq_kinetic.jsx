// BQ Kinetic engine (bq-kinetic/1): builds a kinetic-type film in After Effects from a scene description.
// ExtendScript (ES3), no dependencies, tested on After Effects 2026 (26.2).
//   BQK.check(text)               -> { errors: [], warnings: [], doc }   (messages are written so a chat model can fix them)
//   BQK.build(text, opts)         -> { ok, comp, warnings, duration }    opts: { saveAs, outFile, newProject }
//   BQK.sheet(comp, file, n)      -> writes a contact sheet PNG of n frames (for the director's review loop)
var BQK = BQK || {};
(function () {
  BQK.SCHEMA = "bq-kinetic/1";
  BQK.SIZES = ["S", "M", "L", "XL"];
  BQK.CAMERAS = ["follow", "static"];
  BQK.EXITS = ["cut", "fade", "whip-up"];
  BQK.FPS = [24, 25, 30, 50, 60];

  // Style presets: measured from references (night-gold = the BeQuite film; ink-green = the owner's kinetic-type
  // reference; paper = a light editorial look). Fonts are static instances (variable fonts fall back to serif in AE).
  BQK.PRESETS = {
    "night-gold": { bg: "#000000", bg2: null, text: "#F4F4F6", accent: "#F2B53A", flash: "#FFF4DC", flashAmt: 22,
      font: { S: "GoogleSansFlex36pt-SemiBold", M: "GoogleSansFlex72pt-Bold", L: "GoogleSansFlex120pt-Bold", XL: "GoogleSansFlex120pt-Bold" },
      px: { S: 66, M: 150, L: 196, XL: 236 }, tracking: -20, lead: 0.10 },
    "ink-green": { bg: "#020705", bg2: "#0B3324", text: "#FFFFFF", accent: "#2FE6A0", flash: "#E6FFF4", flashAmt: 18,
      font: { S: "Montserrat-SemiBold", M: "Montserrat-ExtraBold", L: "Montserrat-ExtraBold", XL: "Montserrat-Black" },
      px: { S: 64, M: 142, L: 186, XL: 226 }, tracking: -30, lead: 0.06 },
    "paper": { bg: "#F1F0EC", bg2: null, text: "#15161A", accent: "#FF4A1C", flash: "#FFFFFF", flashAmt: 14,
      font: { S: "Geist-SemiBold", M: "Geist-Bold", L: "Geist-Bold", XL: "Geist-Black" },
      px: { S: 62, M: 140, L: 184, XL: 224 }, tracking: -40, lead: 0.10 }
  };
  BQK.FALLBACK_FONTS = ["Montserrat-Bold", "Geist-Bold", "Inter-Bold", "ArialMT"];

  // optional progress log (set BQK.LOGFILE to a path): shows where a build stopped if After Effects crashes
  BQK.LOGFILE = BQK.LOGFILE || null;
  BQK.log = function (m) {
    if (!BQK.LOGFILE) return;
    try { var f = new File(BQK.LOGFILE); f.encoding = "UTF-8"; f.open("a"); f.writeln(new Date().getTime() + " " + m); f.close(); } catch (e) {}
  };

  // ------------------------------------------------------------------ small helpers
  function isArr(x) { return x instanceof Array; }
  function isNum(x) { return typeof x === "number" && isFinite(x); }
  function isObj(x) { return x !== null && typeof x === "object" && !(x instanceof Array); }
  function has(a, v) { for (var i = 0; i < a.length; i++) if (a[i] === v) return true; return false; }
  function trim(s) { return String(s).replace(/^\s+|\s+$/g, ""); }
  function q(s) { return '"' + String(s) + '"'; }
  function col(hex) {
    hex = String(hex).replace("#", "");
    return [parseInt(hex.substr(0, 2), 16) / 255, parseInt(hex.substr(2, 2), 16) / 255, parseInt(hex.substr(4, 2), 16) / 255];
  }
  function tr(l, n) {
    var m = { pos: "ADBE Position", scale: "ADBE Scale", op: "ADBE Opacity", anchor: "ADBE Anchor Point", rot: "ADBE Rotate Z" };
    return l.property("ADBE Transform Group").property(m[n] || n);
  }
  function wordText(w) {
    if (w.parts) { var s = ""; for (var i = 0; i < w.parts.length; i++) s += w.parts[i].text; return s; }
    return w.text;
  }
  function round(x, n) { var k = Math.pow(10, n || 2); return Math.round(x * k) / k; }

  // ------------------------------------------------------------------ JSON (safe parser: After Effects has no JSON.parse)
  BQK.extractJSON = function (text) {
    text = String(text);
    var a = text.indexOf("{"), b = text.lastIndexOf("}");
    if (a < 0 || b < a) throw new Error("no JSON object found (it must start with { and end with })");
    return text.substring(a, b + 1);
  };
  BQK.parse = function (src) {
    var i = 0, ch = src.charAt(0);
    function err(m) {
      var near = src.substr(Math.max(0, i - 20), 40).replace(/\s+/g, " ");
      throw new Error("JSON " + m + " at character " + i + " (near: ..." + near + "...)");
    }
    function next() { i++; ch = src.charAt(i); return ch; }
    function white() { while (ch && ch <= " ") next(); }
    function str() {
      var out = "", esc = { '"': '"', "\\": "\\", "/": "/", b: "\b", f: "\f", n: "\n", r: "\r", t: "\t" };
      if (ch !== '"') err("expected a string in double quotes");
      next();
      while (ch) {
        if (ch === '"') { next(); return out; }
        if (ch === "\\") {
          next();
          if (ch === "u") {
            var h = src.substr(i + 1, 4);
            if (!/^[0-9a-fA-F]{4}$/.test(h)) err("bad \\u escape");
            out += String.fromCharCode(parseInt(h, 16)); i += 4;
          } else if (esc.hasOwnProperty(ch)) out += esc[ch];
          else err("bad escape \\" + ch);
          next();
        } else { out += ch; next(); }
      }
      err("unterminated string");
    }
    function num() {
      var s = "";
      if (ch === "-") { s = "-"; next(); }
      while (ch >= "0" && ch <= "9") { s += ch; next(); }
      if (ch === ".") { s += "."; next(); while (ch >= "0" && ch <= "9") { s += ch; next(); } }
      if (ch === "e" || ch === "E") { s += ch; next(); if (ch === "-" || ch === "+") { s += ch; next(); } while (ch >= "0" && ch <= "9") { s += ch; next(); } }
      var n = Number(s);
      if (s === "" || s === "-" || isNaN(n)) err("bad number");
      return n;
    }
    function word() {
      if (src.substr(i, 4) === "true") { i += 4; ch = src.charAt(i); return true; }
      if (src.substr(i, 5) === "false") { i += 5; ch = src.charAt(i); return false; }
      if (src.substr(i, 4) === "null") { i += 4; ch = src.charAt(i); return null; }
      err("unexpected '" + ch + "' (keys and strings need double quotes; no comments; no trailing commas)");
    }
    function arr() {
      var a = []; next(); white();
      if (ch === "]") { next(); return a; }
      while (ch) {
        a.push(val()); white();
        if (ch === "]") { next(); return a; }
        if (ch !== ",") err("expected , or ]");
        next(); white();
        if (ch === "]") err("trailing comma before ]");
      }
      err("unterminated array");
    }
    function obj() {
      var o = {}; next(); white();
      if (ch === "}") { next(); return o; }
      while (ch) {
        var k = str(); white();
        if (ch !== ":") err("expected : after " + q(k));
        next(); o[k] = val(); white();
        if (ch === "}") { next(); return o; }
        if (ch !== ",") err("expected , or }");
        next(); white();
        if (ch === "}") err("trailing comma before }");
      }
      err("unterminated object");
    }
    function val() {
      white();
      if (ch === "{") return obj();
      if (ch === "[") return arr();
      if (ch === '"') return str();
      if (ch === "-" || (ch >= "0" && ch <= "9")) return num();
      return word();
    }
    var v = val(); white();
    if (ch) err("extra text after the JSON object");
    return v;
  };

  // ------------------------------------------------------------------ check: validate + normalise, errors a model can act on
  BQK.check = function (text) {
    var E = [], W = [], d;
    try { d = BQK.parse(BQK.extractJSON(text)); }
    catch (e) { return { errors: [String(e.message || e) + ". Reply with the JSON object only, double quotes everywhere."], warnings: [], doc: null }; }
    if (!isObj(d)) return { errors: ["The top level must be one JSON object { ... }."], warnings: [], doc: null };

    if (d.version !== BQK.SCHEMA) E.push('version: must be "' + BQK.SCHEMA + '".');
    var doc = { version: BQK.SCHEMA, title: d.title ? trim(d.title) : "BQ Kinetic", style: d.style || "night-gold", music: d.music || null,
                format: { width: 1920, height: 1080, fps: 30 }, tempo: { bpm: 120, first_beat: 0.5 }, scenes: [] };
    if (d.format !== undefined) {
      if (!isObj(d.format)) E.push("format: must be an object like {\"width\":1920,\"height\":1080,\"fps\":30}.");
      else {
        if (d.format.width !== undefined) { if (!isNum(d.format.width) || d.format.width < 360 || d.format.width > 4096) E.push("format.width: a number from 360 to 4096."); else doc.format.width = Math.round(d.format.width); }
        if (d.format.height !== undefined) { if (!isNum(d.format.height) || d.format.height < 360 || d.format.height > 4096) E.push("format.height: a number from 360 to 4096."); else doc.format.height = Math.round(d.format.height); }
        if (d.format.fps !== undefined) { if (!has(BQK.FPS, d.format.fps)) E.push("format.fps: one of 24, 25, 30, 50, 60."); else doc.format.fps = d.format.fps; }
      }
    }
    if (d.tempo !== undefined) {
      if (!isObj(d.tempo)) E.push("tempo: must be an object like {\"bpm\":120,\"first_beat\":0.5}.");
      else {
        if (d.tempo.bpm !== undefined) { if (!isNum(d.tempo.bpm) || d.tempo.bpm < 60 || d.tempo.bpm > 200) E.push("tempo.bpm: a number from 60 to 200 (the music's tempo)."); else doc.tempo.bpm = d.tempo.bpm; }
        if (d.tempo.first_beat !== undefined) { if (!isNum(d.tempo.first_beat) || d.tempo.first_beat < 0 || d.tempo.first_beat > 30) E.push("tempo.first_beat: seconds from the start of the music to its first beat (0 to 30)."); else doc.tempo.first_beat = d.tempo.first_beat; }
      }
    }
    if (!BQK.PRESETS[doc.style]) {
      var names = []; for (var k in BQK.PRESETS) if (BQK.PRESETS.hasOwnProperty(k)) names.push(q(k));
      E.push("style: " + q(doc.style) + " is not a preset. Use one of " + names.join(", ") + ".");
    }
    if (!isArr(d.scenes) || d.scenes.length < 1) { E.push("scenes: a list with 1 to 12 scenes."); return { errors: E, warnings: W, doc: null }; }
    if (d.scenes.length > 12) E.push("scenes: at most 12 (found " + d.scenes.length + "); split into two films.");

    var bd = 60 / doc.tempo.bpm;
    for (var si = 0; si < d.scenes.length && si < 12; si++) {
      var s = d.scenes[si], S = "scene " + (si + 1);
      if (!isObj(s)) { E.push(S + ": must be an object with \"rows\"."); continue; }
      var sc = { rows: [], hold: 2, camera: "follow", exit: "cut", words: [] };
      if (s.hold_beats !== undefined) { if (!isNum(s.hold_beats) || s.hold_beats < 1 || s.hold_beats > 16) E.push(S + ".hold_beats: 1 to 16 (beats the finished block stays on screen)."); else sc.hold = s.hold_beats; }
      if (s.camera !== undefined) { if (!has(BQK.CAMERAS, s.camera)) E.push(S + ".camera: \"follow\" or \"static\"."); else sc.camera = s.camera; }
      if (s.exit !== undefined) { if (!has(BQK.EXITS, s.exit)) E.push(S + ".exit: \"cut\", \"fade\" or \"whip-up\"."); else sc.exit = s.exit; }
      if (!isArr(s.rows) || s.rows.length < 1 || s.rows.length > 5) { E.push(S + ".rows: a list of 1 to 5 rows; each row is a list of words."); continue; }
      for (var ri = 0; ri < s.rows.length; ri++) {
        var row = s.rows[ri], R = S + " > row " + (ri + 1), nrow = [];
        if (!isArr(row) || row.length < 1 || row.length > 4) { E.push(R + ": a list of 1 to 4 items (a word {\"text\":...} or a stack {\"stack\":[...]})."); continue; }
        for (var ii = 0; ii < row.length; ii++) {
          var it = row[ii], I = R + " > item " + (ii + 1);
          if (isObj(it) && it.stack !== undefined) {
            if (!isArr(it.stack) || it.stack.length < 2 || it.stack.length > 3) { E.push(I + ": \"stack\" holds 2 or 3 small words, e.g. {\"stack\":[{\"text\":\"the\",\"beat\":1},{\"text\":\"most\",\"beat\":1.5}]}."); continue; }
            var st = { stack: [] };
            for (var wi = 0; wi < it.stack.length; wi++) {
              var nw = normWord(it.stack[wi], I + " > stack word " + (wi + 1), "S", E, W);
              if (nw) { if (nw.size !== "S" && nw.size !== "M") E.push(I + " > stack word " + (wi + 1) + ": stack words are \"S\" or \"M\"."); st.stack.push(nw); sc.words.push({ w: nw, r: ri, i: ii, j: wi }); }
            }
            nrow.push(st);
          } else {
            var w = normWord(it, I, "M", E, W);
            if (w) { nrow.push(w); sc.words.push({ w: w, r: ri, i: ii, j: -1 }); }
          }
        }
        sc.rows.push(nrow);
      }
      // grammar warnings
      var last = -1, slams = 0, accents = 0, beats = [];
      for (var x = 0; x < sc.words.length; x++) {
        var ww = sc.words[x].w;
        if (ww.beat < last) W.push(S + ": " + q(wordText(ww)) + " lands on beat " + ww.beat + ", before a word that reads earlier (beat " + last + "). Words should land in reading order.");
        last = Math.max(last, ww.beat);
        if (ww.slam) slams++;
        if (ww.accent || ww.partsAccent) accents++;
        beats.push(ww.beat);
        if (Math.abs(ww.beat * 4 - Math.round(ww.beat * 4)) > 0.001) W.push(S + ": " + q(wordText(ww)) + " lands on beat " + ww.beat + "; use whole, half or quarter beats so it hits the music.");
      }
      beats.sort(function (a, b) { return a - b; });
      for (var y = 1; y < beats.length; y++) if (beats[y] - beats[y - 1] > 0 && beats[y] - beats[y - 1] < 0.25) W.push(S + ": two words land " + round((beats[y] - beats[y - 1]) * bd, 2) + " s apart; keep at least a quarter beat between landings.");
      if (slams > 1) W.push(S + ": " + slams + " slams; one per scene keeps it strong.");
      if (accents > 2) W.push(S + ": " + accents + " accented words; one, at most two, per scene.");
      if (sc.hold < 2) W.push(S + ": hold_beats " + sc.hold + "; the finished line usually needs 2 beats to be read.");
      if (sc.words.length) doc.scenes.push(sc);
    }
    return { errors: E, warnings: W, doc: E.length ? null : doc };
  };

  function normWord(o, P, defSize, E, W) {
    if (!isObj(o)) { E.push(P + ": must be an object like {\"text\":\"word\",\"beat\":2}."); return null; }
    var w = { size: o.size === undefined ? defSize : o.size, beat: o.beat, accent: !!o.accent, slam: !!o.slam };
    if (o.parts !== undefined) {
      if (!isArr(o.parts) || o.parts.length < 2 || o.parts.length > 3) { E.push(P + ".parts: 2 or 3 pieces, e.g. [{\"text\":\"Be\"},{\"text\":\"Quite\",\"accent\":true}]."); return null; }
      w.parts = [];
      for (var i = 0; i < o.parts.length; i++) {
        var p = o.parts[i];
        if (!isObj(p) || typeof p.text !== "string" || !p.text.length) { E.push(P + ".parts[" + (i + 1) + "]: {\"text\":\"...\"} with an optional \"accent\":true."); return null; }
        w.parts.push({ text: p.text, accent: !!p.accent });
        if (p.accent) w.partsAccent = true;
      }
    } else if (typeof o.text !== "string" || !trim(o.text).length) { E.push(P + ": \"text\" is missing or empty."); return null; }
    else w.text = trim(o.text);
    var t = wordText(w);
    if (t.length > 28) E.push(P + " (" + q(t) + "): " + t.length + " characters; one word or a short phrase, at most 28.");
    if (/\s.+\s.+\s/.test(t)) W.push(P + " (" + q(t) + "): several words in one item; kinetic type lands one word at a time.");
    if (!has(BQK.SIZES, w.size)) { E.push(P + " (" + q(t) + "): size must be \"S\", \"M\", \"L\" or \"XL\"."); return null; }
    if (!isNum(w.beat) || w.beat < 0 || w.beat > 64) { E.push(P + " (" + q(t) + "): \"beat\" must be a number from 0 to 64 (beats after the scene starts)."); return null; }
    return w;
  }

  // ------------------------------------------------------------------ After Effects building blocks
  var CURVES = { expo: [6, 92], inout: [60, 60], soft: [33, 75], "in": [80, 4] };
  function easeKey(p, k, inInf, outInf) {
    var n = p.propertyValueType == PropertyValueType.TwoD ? 2 : (p.propertyValueType == PropertyValueType.ThreeD ? 3 : 1), a = [], b = [];
    for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, Math.max(0.1, inInf))); b.push(new KeyframeEase(0, Math.max(0.1, outInf))); }
    p.setTemporalEaseAtKey(k, a, b);
  }
  // keys: [[t, value, curveToNext], ...]
  function keys(p, ks) {
    var i, k;
    for (i = 0; i < ks.length; i++) p.setValueAtTime(ks[i][0], ks[i][1]);
    for (i = 0; i < ks.length; i++) {
      k = p.nearestKeyIndex(ks[i][0]);
      var cOut = ks[i][2] || "expo", cIn = i > 0 ? (ks[i - 1][2] || "expo") : "expo";
      var outInf = CURVES[cOut] ? CURVES[cOut][0] : 33, inInf = CURVES[cIn] ? CURVES[cIn][1] : 33;
      if (i === 0) inInf = 33;
      if (i === ks.length - 1) outInf = 33;
      if (cOut === "hold") {  // a hold still lands with the incoming ease, or the move stops dead
        p.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.HOLD);
        try { easeKey(p, k, inInf, 33); } catch (e) {}
        continue;
      }
      p.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
      easeKey(p, k, inInf, outInf);
      try { if (p.isSpatial) { p.setSpatialAutoBezierAtKey(k, false); p.setSpatialContinuousAtKey(k, false); p.setSpatialTangentsAtKey(k, [0, 0, 0], [0, 0, 0]); } } catch (e) {}
    }
  }
  function fontOk(ps) { try { var a = app.fonts.getFontsByPostScriptName(ps); return !!(a && a.length); } catch (e) { return true; } }

  var CAP = {};
  function capHeight(comp, font, px, tracking) {
    var key = font + "@" + px;
    if (CAP[key]) return CAP[key];
    var L = comp.layers.addText("H");
    setDoc(L, "H", font, px, "#FFFFFF", tracking);
    var r = L.sourceRectAtTime(0, false);
    L.remove();
    CAP[key] = -r.top;
    return CAP[key];
  }
  function setDoc(L, str, font, px, hex, tracking) {
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document"), td = tp.value;
    td.resetCharStyle(); td.resetParagraphStyle();
    td.text = str; td.font = font; td.fontSize = px;
    td.applyFill = true; td.fillColor = col(hex); td.applyStroke = false;
    td.tracking = tracking; td.justification = ParagraphJustification.LEFT_JUSTIFY;
    tp.setValue(td);
  }
  function colorRange(L, startIdx, endIdx, len, hex) {
    var A = L.property("ADBE Text Properties").property("ADBE Text Animators");
    A.addProperty("ADBE Text Animator");
    var an = A.property(A.numProperties); an.name = "accent";
    an.property("ADBE Text Animator Properties").addProperty("ADBE Text Fill Color");
    an = A.property(A.numProperties);
    an.property("ADBE Text Animator Properties").property("ADBE Text Fill Color").setValue(col(hex));
    an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
    var sel = A.property(A.numProperties).property("ADBE Text Selectors").property(1);
    sel.property("ADBE Text Percent Start").setValue(startIdx / len * 100);
    sel = A.property(A.numProperties).property("ADBE Text Selectors").property(1);
    sel.property("ADBE Text Percent End").setValue(endIdx / len * 100);
  }
  function makeWord(comp, w, P, world) {
    var str = wordText(w), font = P.font[w.size], px = P.px[w.size];
    BQK.log("  word " + str + " " + font + " " + px);
    var L = comp.layers.addText(str);
    setDoc(L, str, font, px, w.accent ? P.accent : P.text, P.tracking);
    if (w.parts) {
      var at = 0;
      for (var i = 0; i < w.parts.length; i++) {
        if (w.parts[i].accent) colorRange(L, at, at + w.parts[i].text.length, str.length, P.accent);
        at += w.parts[i].text.length;
      }
    }
    L.name = str;
    var r = L.sourceRectAtTime(0, false);
    tr(L, "anchor").setValue([r.left + r.width / 2, r.top + r.height / 2]);
    L.parent = world;
    L.motionBlur = true;
    return { L: L, r: r, w: w, cap: capHeight(comp, font, px, P.tracking), px: px };
  }

  // ------------------------------------------------------------------ one scene: layout, landings, the push, the camera
  function buildScene(c, sc, P, bd, warnings, sceneNo) {
    var Wd = c.width, Hd = c.height, i, j, r;
    BQK.log("scene " + sceneNo + ": start");
    var world = c.layers.addNull(); world.name = "CAMERA"; world.enabled = false;
    tr(world, "anchor").setValue([0, 0, 0]); tr(world, "pos").setValue([0, 0, 0]);

    // 1. make and measure every word
    var rows = [];
    for (r = 0; r < sc.rows.length; r++) {
      var items = [];
      for (i = 0; i < sc.rows[r].length; i++) {
        var it = sc.rows[r][i];
        if (it.stack) {
          // stack lines sit on baselines measured from each word's own cap height, so "for" over an M word never overlaps it
          var ws = [], wmax = 0, sb = [], yy = 0;
          for (j = 0; j < it.stack.length; j++) {
            var m = makeWord(c, it.stack[j], P, world); m.t = it.stack[j].beat * bd; ws.push(m); wmax = Math.max(wmax, m.r.width);
            yy = j ? yy + ws[j - 1].cap * 0.42 + m.cap : m.cap; sb.push(yy);
          }
          items.push({ stack: ws, width: wmax, t: ws[0].t, sb: sb, h: yy });
        } else {
          var mw = makeWord(c, it, P, world); mw.t = it.beat * bd;
          items.push({ word: mw, width: mw.r.width, t: mw.t });
        }
      }
      var cap = 0, px = 0;
      for (i = 0; i < items.length; i++) {
        if (items[i].word) { cap = Math.max(cap, items[i].word.cap); px = Math.max(px, items[i].word.px); }
        else cap = Math.max(cap, items[i].h);  // a stack taller than the words makes the row taller
      }
      if (!px) px = items[0].stack[0].px * 2;
      rows.push({ items: items, cap: cap, px: px, gap: px * 0.24 });
    }
    BQK.log("scene " + sceneNo + ": words made");
    // 2. baselines
    var y = 0;
    for (r = 0; r < rows.length; r++) {
      if (r > 0) y += rows[r].cap * (1 + P.lead) + rows[r - 1].px * 0.16;
      rows[r].base = y;
    }
    // 3. horizontal positions per landing event in each row (the push: the row stays centred as it grows)
    function widthAt(item, tNow) {  // a stack is as wide as its widest word that has landed
      if (item.word) return item.width;
      var w = 0;
      for (var q = 0; q < item.stack.length; q++) if (item.stack[q].t <= tNow + 1e-6) w = Math.max(w, item.stack[q].r.width);
      return w;
    }
    function landsAt(item, tq) {
      if (item.word) return Math.abs(item.t - tq) < 1e-6;
      for (var q = 0; q < item.stack.length; q++) if (Math.abs(item.stack[q].t - tq) < 1e-6) return true;
      return false;
    }
    function rowXs(row, tNow) {
      var vis = [], total = 0, k;
      for (k = 0; k < row.items.length; k++) if (row.items[k].t <= tNow + 1e-6) vis.push(k);
      for (k = 0; k < vis.length; k++) total += widthAt(row.items[vis[k]], tNow) + (k ? row.gap : 0);
      var x = -total / 2, out = {};
      for (k = 0; k < vis.length; k++) { out[vis[k]] = x; x += widthAt(row.items[vis[k]], tNow) + row.gap; }
      return out;
    }
    var PUSH = Math.min(0.24, bd * 0.5), events = [];
    for (r = 0; r < rows.length; r++) {
      var row = rows[r], times = [];
      for (i = 0; i < row.items.length; i++) {
        if (row.items[i].word) addTime(times, row.items[i].t);
        else for (j = 0; j < row.items[i].stack.length; j++) addTime(times, row.items[i].stack[j].t);
      }
      times.sort(function (a, b) { return a - b; });
      row.final = rowXs(row, 1e9);
      for (i = 0; i < row.items.length; i++) {
        var item = row.items[i], ks = [], prev = null;
        for (j = 0; j < times.length; j++) {
          var T = times[j];
          if (T < item.t - 1e-6) continue;
          var xs = rowXs(row, T), dur = PUSH;
          if (j + 1 < times.length) dur = Math.max(0.06, Math.min(PUSH, times[j + 1] - T));
          if (prev === null) {
            // the new item enters beside where its neighbour stood, then travels with the row: words never overlap
            var before = rowXs(row, T - 1e-3), pidx = -1, q;
            for (q = i - 1; q >= 0; q--) if (before[q] !== undefined) { pidx = q; break; }
            var shift = (pidx >= 0 && xs[pidx] !== undefined) ? before[pidx] - xs[pidx] : 0;
            if (Math.abs(shift) > 0.01) { ks.push([T, xs[i] + shift]); ks.push([T + dur, xs[i]]); }
            else ks.push([T, xs[i]]);
          } else if (Math.abs(prev - xs[i]) > 0.01) { ks.push([T, prev]); ks.push([T + dur, xs[i]]); }
          prev = xs[i];
        }
        item.xKeys = dedupe(ks);
      }
      for (j = 0; j < times.length; j++) events.push({ t: times[j], r: r });
    }
    BQK.log("scene " + sceneNo + ": layout done");
    // 4. place, land and push every layer
    var slams = [], tLast = 0;
    function place(m, xLeft, base, xKeys, tLand, leftAnchor) {
      // a word with a neighbour on its left settles from its left edge, so the landing overshoot never covers that neighbour
      var cy = base + m.r.top + m.r.height / 2, p = tr(m.L, "pos"), off = leftAnchor ? 0 : m.r.width / 2;
      if (leftAnchor) tr(m.L, "anchor").setValue([m.r.left, m.r.top + m.r.height / 2]);
      if (xKeys.length < 2) p.setValue([xKeys[0][1] + off + xLeft, cy]);
      else { var kk = []; for (var a = 0; a < xKeys.length; a++) kk.push([xKeys[a][0], [xKeys[a][1] + xLeft + off, cy], "expo"]); keys(p, kk); }
      m.L.inPoint = tLand;
      var slam = m.w.slam, big = slam ? 152 : 118, d = slam ? 0.22 : 0.26;
      if (tLand < 0.05) tr(m.L, "op").setValue(100);  // first word of a scene: visible on the cut, no empty frames
      else keys(tr(m.L, "op"), [[tLand, 0, "expo"], [tLand + (slam ? 0.04 : 0.1), 100]]);
      keys(tr(m.L, "scale"), [[tLand, [big, big], "expo"], [tLand + d, [100, 100]]]);
      if (slam) slams.push(tLand);
      tLast = Math.max(tLast, tLand);
    }
    for (r = 0; r < rows.length; r++) {
      for (i = 0; i < rows[r].items.length; i++) {
        var itm = rows[r].items[i];
        if (itm.word) place(itm.word, 0, rows[r].base, itm.xKeys, itm.t, i > 0);
        else {
          var sTop = rows[r].base - rows[r].cap;
          for (j = 0; j < itm.stack.length; j++) place(itm.stack[j], 0, sTop + itm.sb[j], itm.xKeys, itm.stack[j].t, i > 0);
        }
      }
    }
    BQK.log("scene " + sceneNo + ": landings keyed");
    // 5. the camera: follow the newest word, then pull back to the whole block
    var minX = 1e9, maxX = -1e9;
    for (r = 0; r < rows.length; r++) for (i = 0; i < rows[r].items.length; i++) {
      var fx = rows[r].final[i]; minX = Math.min(minX, fx); maxX = Math.max(maxX, fx + rows[r].items[i].width);
    }
    var top = rows[0].base - rows[0].cap, bottom = rows[rows.length - 1].base + rows[rows.length - 1].px * 0.18;
    var bw = maxX - minX, bh = bottom - top, ccx = (minX + maxX) / 2, ccy = (top + bottom) / 2;
    var zFit = Math.min(0.84 * Wd / bw, 0.78 * Hd / bh, 1.6);
    if (zFit < 0.45) warnings.push("scene " + sceneNo + ": the block is large (fit zoom " + round(zFit, 2) + "); shorter words or fewer rows read better.");
    var P0 = tr(world, "pos"), S0 = tr(world, "scale");
    function camAt(cx, cy, z) { return [[Wd / 2 - z * cx, Hd / 2 - z * cy], [z * 100, z * 100]]; }
    var tEnd = (tLast / bd + sc.hold) * bd;
    function span(row, tq) {  // a row's left and right edge at a moment (rows are centred on x = 0)
      var xs3 = rowXs(row, tq), lo3 = 1e9, hi3 = -1e9;
      for (var k3 in xs3) if (xs3.hasOwnProperty(k3)) { lo3 = Math.min(lo3, xs3[k3]); hi3 = Math.max(hi3, xs3[k3] + widthAt(row.items[k3], tq)); }
      return hi3 > lo3 ? [lo3, hi3] : [0, 0];
    }
    function clamp(v, a, b) { return a > b ? (a + b) / 2 : Math.max(a, Math.min(b, v)); }
    {
      // follow: lean towards the newest word, but keep the row being built (and, where it fits, everything built so far) in frame.
      // static: one size for the whole scene; the camera only glides so the lines built so far stay centred.
      events.sort(function (a, b) { return a.t - b.t; });
      var follow = sc.camera !== "static";
      var pk = [], sk = [], cur = null, MOVE = follow ? Math.min(0.34, bd * 0.75) : Math.min(0.5, bd), lastRow = -1, z = zFit;
      var EXIT = sc.exit === "cut" ? 0 : 0.3;
      var tSlam = slams.length ? slams[0] : null;
      var tFit = (follow && tSlam !== null) ? tSlam : Math.min(tLast + PUSH + 0.06, Math.max(tLast, tEnd - EXIT - 0.45 - 0.35));
      var blockTop = rows[0].base - rows[0].cap;
      for (var e = 0; e < events.length; e++) {
        var ev = events[e];
        if (follow && tSlam !== null && ev.t >= tSlam - 1e-6) break;
        var rw = rows[ev.r], rowTop = rw.base - rw.cap, rowBot = rw.base + rw.px * 0.18;
        var visW = 0, ra;
        for (ra = 0; ra <= ev.r; ra++) { var sp = span(rows[ra], ev.t); visW = Math.max(visW, sp[1] - sp[0]); }
        var tx, ty;
        if (follow) {
          var fin = span(rw, 1e9), finW = fin[1] - fin[0], xs2 = rowXs(rw, ev.t), key;
          if (ev.r !== lastRow) z = Math.max(zFit, Math.min(zFit * 1.15, 0.8 * Wd / Math.max(finW, 1)));  // sized for the finished row: no zoom pumping
          var newest = -1; for (i = 0; i < rw.items.length; i++) if (landsAt(rw.items[i], ev.t)) newest = i;
          if (newest < 0 || xs2[newest] === undefined) { for (key in xs2) if (xs2.hasOwnProperty(key)) newest = Number(key); }
          var nx = xs2[newest] + widthAt(rw.items[newest], ev.t) / 2;
          var hw = Wd / (2 * z) * 0.94, hh = Hd / (2 * z) * 0.92;
          tx = clamp(nx * 0.3, finW / 2 - hw, hw - finW / 2);
          if (visW / 2 <= hw) tx = clamp(tx, visW / 2 - hw, hw - visW / 2);
          ty = clamp((rowTop + rowBot) / 2 * 0.6 + (blockTop + rowBot) / 2 * 0.4, rowBot - hh, rowTop + hh);
          if (blockTop + hh >= rowBot - hh) ty = clamp(ty, rowBot - hh, blockTop + hh);  // the first line stays in frame when it can
        } else {
          if (ev.r === lastRow) continue;
          z = zFit; tx = ccx; ty = (blockTop + rowBot) / 2;
        }
        var target = camAt(tx, ty, z);
        if (cur === null) { pk.push([0, target[0], "hold"]); sk.push([0, target[1], "hold"]); }
        else {
          var nextT = follow ? tFit : tEnd;  // the move ends before the next move starts (static moves only on a new row)
          for (var k4 = e + 1; k4 < events.length; k4++) if (follow || events[k4].r !== ev.r) { nextT = events[k4].t; break; }
          var t0 = ev.t, t1 = Math.min(ev.t + MOVE, nextT - 0.02);
          if (t1 <= t0 + 0.04) t1 = t0 + 0.04;
          pk.push([t0, cur[0], follow ? "expo" : "soft"]); sk.push([t0, cur[1], follow ? "expo" : "soft"]);
          pk.push([t1, target[0], "hold"]); sk.push([t1, target[1], "hold"]);
        }
        cur = target; lastRow = ev.r;
      }
      var fit = camAt(ccx, ccy, zFit), t2 = Math.max(tFit, (pk.length ? pk[pk.length - 1][0] : 0) + 0.05);
      if (cur !== null) { pk.push([t2, cur[0], "expo"]); sk.push([t2, cur[1], "expo"]); }
      var fd = tSlam !== null ? 0.3 : 0.45;
      pk.push([t2 + fd, fit[0]]); sk.push([t2 + fd, fit[1]]);
      // drop duplicate times (keep the last value at a time)
      keys(P0, dedupe(pk)); keys(S0, dedupe(sk));
    }
    BQK.log("scene " + sceneNo + ": camera keyed");
    return { slams: slams, end: tEnd, fit: round(zFit, 3) };
  }
  function addTime(arr, tt) { for (var q = 0; q < arr.length; q++) if (Math.abs(arr[q] - tt) < 1e-6) return; arr.push(tt); }
  function dedupe(ks) {
    var out = [];
    for (var i = 0; i < ks.length; i++) {
      if (out.length && Math.abs(out[out.length - 1][0] - ks[i][0]) < 1e-4) out[out.length - 1] = ks[i];
      else out.push(ks[i]);
    }
    return out;
  }

  // ------------------------------------------------------------------ the film
  BQK.build = function (text, opts) {
    opts = opts || {};
    var chk = BQK.check(text);
    if (chk.errors.length) return { ok: false, errors: chk.errors, warnings: chk.warnings };
    var doc = chk.doc, P0 = BQK.PRESETS[doc.style], warnings = chk.warnings.slice(), P = {}, k;
    for (k in P0) if (P0.hasOwnProperty(k)) P[k] = P0[k];
    P.font = {}; for (k in P0.font) if (P0.font.hasOwnProperty(k)) {
      P.font[k] = P0.font[k];
      if (!fontOk(P.font[k])) {
        for (var f = 0; f < BQK.FALLBACK_FONTS.length; f++) if (fontOk(BQK.FALLBACK_FONTS[f])) { warnings.push("font " + P0.font[k] + " is not installed; using " + BQK.FALLBACK_FONTS[f] + "."); P.font[k] = BQK.FALLBACK_FONTS[f]; break; }
      }
    }
    CAP = {};
    BQK.log("build: checked, " + doc.scenes.length + " scenes");
    app.beginUndoGroup("BQ Kinetic: " + doc.title);
    var proj = app.project;
    if (opts.newProject) {  // the caller has checked that the open project is empty or a throwaway test project
      try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (e) {}
      proj = app.newProject() || app.project;
    }
    var folder = proj.items.addFolder("BQ Kinetic - " + doc.title);
    var bd = 60 / doc.tempo.bpm, Wd = doc.format.width, Hd = doc.format.height, fps = doc.format.fps;
    var t = doc.tempo.first_beat, plan = [], s, x;
    for (s = 0; s < doc.scenes.length; s++) {
      var lastBeat = 0;
      for (x = 0; x < doc.scenes[s].words.length; x++) lastBeat = Math.max(lastBeat, doc.scenes[s].words[x].w.beat);
      var dur = (lastBeat + doc.scenes[s].hold) * bd;
      plan.push({ start: t, dur: dur, last: t + lastBeat * bd });
      t += dur;
    }
    var total = t;  // exactly the length the director planned: first_beat + every scene's (last beat + hold) in beats
    function mkComp(name, d, parent) {
      var c = proj.items.addComp(name, Wd, Hd, 1, d, fps);
      c.parentFolder = parent; c.bgColor = col(P.bg);
      c.motionBlur = true; c.shutterAngle = 200; c.shutterPhase = -100; c.motionBlurSamplesPerFrame = 16; c.motionBlurAdaptiveSampleLimit = 128;
      return c;
    }
    BQK.log("build: project ready");
    var main = mkComp(doc.title, total, folder);
    var bg = main.layers.addSolid(col(P.bg), "background", Wd, Hd, 1, total);
    if (P.bg2) {
      var ramp = bg.property("ADBE Effect Parade").addProperty("ADBE Ramp");
      ramp.property("ADBE Ramp-0001").setValue([Wd / 2, Hd / 2]);
      ramp.property("ADBE Ramp-0002").setValue(col(P.bg2));
      ramp.property("ADBE Ramp-0003").setValue([Wd, Hd]);
      ramp.property("ADBE Ramp-0004").setValue(col(P.bg));
      ramp.property("ADBE Ramp-0005").setValue(2);
    }
    var pre = proj.items.addFolder("scenes"); pre.parentFolder = folder;
    var info = [];
    for (s = 0; s < doc.scenes.length; s++) {
      var c = mkComp("scene " + (s + 1), plan[s].dur, pre);
      var res = buildScene(c, doc.scenes[s], P, bd, warnings, s + 1);
      var L = main.layers.add(c);
      L.startTime = plan[s].start; L.motionBlur = true; L.collapseTransformation = true;
      var e0 = plan[s].start + plan[s].dur;
      if (doc.scenes[s].exit === "fade") keys(tr(L, "op"), [[e0 - 0.3, 100, "inout"], [e0, 0]]);
      if (doc.scenes[s].exit === "whip-up") keys(tr(L, "pos"), [[e0 - 0.28, [Wd / 2, Hd / 2], "in"], [e0, [Wd / 2, -Hd * 0.65]]]);
      for (x = 0; x < res.slams.length; x++) {
        var ts = plan[s].start + res.slams[x];
        var fl = main.layers.addSolid(col(P.flash), "flash", Wd, Hd, 1, 0.2);
        fl.startTime = ts; fl.blendingMode = BlendingMode.ADD;
        keys(tr(fl, "op"), [[ts, 0, "expo"], [ts + 0.03, P.flashAmt, "inout"], [ts + 0.16, 0]]);
      }
      info.push({ scene: s + 1, start: round(plan[s].start, 3), dur: round(plan[s].dur, 3), last: round(plan[s].last, 3), exit: doc.scenes[s].exit, fit_zoom: res.fit, slams: res.slams.length });
    }
    if (doc.music) {
      try { var mf = new File(doc.music); if (mf.exists) { var it = proj.importFile(new ImportOptions(mf)); it.parentFolder = folder; main.layers.add(it).moveToEnd(); } else warnings.push("music file not found: " + doc.music); }
      catch (e) { warnings.push("music could not be imported: " + e); }
    }
    BQK.log("build: scenes placed");
    if (opts.outFile) {
      var rq = proj.renderQueue.items.add(main);
      try { rq.applyTemplate("Best Settings"); } catch (e) {}
      try { rq.outputModule(1).applyTemplate("H.264 - Match Render Settings - 15 Mbps"); }
      catch (e) { warnings.push("the H.264 output template was not found; choose the output format in the Render Queue."); }
      rq.outputModule(1).file = new File(opts.outFile);
    }
    app.endUndoGroup();
    BQK.log("build: undo group closed");
    if (opts.saveAs) proj.save(new File(opts.saveAs));
    BQK.log("build: saved");
    BQK.LAST = { comp: main, from: doc.tempo.first_beat + 0.12, to: t - 0.08, scenes: info };  // the span where type is on screen
    return { ok: true, comp: main, warnings: warnings, duration: round(total, 3), scenes: info };
  };

  // ------------------------------------------------------------------ contact sheet (for the director: 12 frames, with times)
  // Frames are picked per scene, not evenly: evenly spaced frames can miss a hero word that lands between two samples,
  // and the director then "fixes" the film for the sheet. The last frame of every scene is its finished block.
  BQK.sheetTimes = function (comp, n) {
    n = n || 12;
    var out = [], i;
    if (BQK.LAST && BQK.LAST.comp === comp && BQK.LAST.scenes && BQK.LAST.scenes.length) {
      var S = BQK.LAST.scenes, per = Math.max(1, Math.min(3, Math.floor(n / S.length)));
      for (i = 0; i < S.length && out.length < n; i++) {
        var s = S[i], end = s.start + s.dur - (s.exit === "cut" ? 0.08 : 0.38);
        var settled = Math.max(Math.min(end, s.last + 0.9), s.last + 0.05);
        if (per >= 3) out.push(s.start + 0.1);  // the first word, before the second one pushes it
        if (per >= 2) out.push(s.start + (s.last - s.start) * 0.6 + 0.1);
        out.push(settled);
      }
      return out;
    }
    var a = 0, b = comp.duration;
    for (i = 0; i < n; i++) out.push(a + (b - a) * (i + 0.5) / n);
    return out;
  };
  BQK.sheet = function (comp, file, n, times, waitMs) {
    if (!times) times = BQK.sheetTimes(comp, n || 12);
    n = times.length;
    var cols = comp.height > comp.width ? 6 : 4, rowsN = Math.ceil(n / cols), cw = comp.height > comp.width ? 300 : 480;
    var ch = Math.round(cw * comp.height / comp.width), pad = 8, lab = 26;
    var sw = cols * cw + (cols + 1) * pad, sh = rowsN * (ch + lab) + (rowsN + 1) * pad;
    for (var old = app.project.numItems; old >= 1; old--) {  // one sheet comp per film: replace the previous one
      var it = app.project.item(old);
      if (it instanceof CompItem && it.name === comp.name + " sheet" && it !== comp) { try { it.remove(); } catch (e) {} }
    }
    var sc = app.project.items.addComp(comp.name + " sheet", sw, sh, 1, 1, comp.frameRate);
    sc.parentFolder = comp.parentFolder; sc.bgColor = [0.16, 0.16, 0.17]; sc.motionBlur = true;
    sc.shutterAngle = comp.shutterAngle; sc.shutterPhase = comp.shutterPhase;
    sc.layers.addSolid([0.16, 0.16, 0.17], "sheet background", sw, sh, 1, 1);  // the PNG keeps alpha: without this the sheet is white
    for (var k = 0; k < n; k++) {
      var cx = pad + (k % cols) * (cw + pad), cy = pad + Math.floor(k / cols) * (ch + lab + pad);
      var L = sc.layers.add(comp);
      L.startTime = -times[k]; L.motionBlur = true;
      tr(L, "scale").setValue([cw / comp.width * 100, cw / comp.width * 100]);
      tr(L, "pos").setValue([cx + cw / 2, cy + lab + ch / 2]);
      var T = sc.layers.addText(round(times[k], 2) + " s");
      setDoc(T, round(times[k], 2) + " s", "ArialMT", 18, "#FFD84A", 0);
      tr(T, "pos").setValue([cx + 4, cy + 19]);
    }
    var png = new File(file);
    if (png.exists) png.remove();
    sc.saveFrameToPng(0, png);  // asynchronous: After Effects writes the file while the script waits or after it ends
    // the file appears empty first and fills a moment later: wait until its size is above zero and stable
    var t0 = new Date().getTime(), lastLen = -1, len = 0;
    while (waitMs && new Date().getTime() - t0 < waitMs) {
      var pf = new File(file); len = pf.exists ? pf.length : 0;
      if (len > 0 && len === lastLen) break;
      lastLen = len; $.sleep(200);
    }
    return { file: file, times: times, comp: sc, written: len > 0, bytes: len };
  };
})();
