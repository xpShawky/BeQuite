// type.jsx - kinetic-type toolkit for After Effects (ExtendScript / ES3). Needs core.jsx first.
// The treatments and when to use each are defined in the bequite-kinetic-type skill (references/toolbox.md);
// this file is only the AE implementation.
//
// Segment = [text, kind, font?, color?]   kind: 0 plain | 1 key (accent) | 2 key (failure red)
// Direction: these helpers sweep in logical order (left -> right for LTR text). For Arabic / RTL text use
// o.by = "word" (never per-character on connected scripts) and check the result on stills - see
// bequite-kinetic-type/references/arabic-rtl.md. AE RTL paragraph control from script is UNVERIFIED.

K.segStyle = function (s, o) {
  var k = s[1] || 0, dark = !!o.dark;
  return { font: s[2] || (k ? K.F.bold : (o.font || K.F.semi)),
           color: s[3] || (k == 2 ? K.C.red : (k ? (dark ? K.C.acc2 : K.C.acc) : (dark ? "#F2F2F2" : K.C.ink))) };
};
// advance width of a string (trailing spaces count)
K.advOf = function (l, str) {
  K.setText(l, str + "|"); var a = K.textRect(l).width; K.setText(l, "|"); var b = K.textRect(l).width; K.setText(l, str); return a - b;
};
K.nchars = function (s) { return s.replace(/\s/g, "").length; };
K.srcText = function (l) { return l.property("ADBE Text Properties").property("ADBE Text Document").value.text; };

// Lay out segments on one line (centred on cx, or starting at cx when o.just == "left"). No animation.
K.lay = function (c, segs, cx, y, o) {
  o = o || {};
  var size = o.size || 64, res = { layers: [], adv: [], x: [], total: 0, size: size, y: y };
  for (var i = 0; i < segs.length; i++) {
    var st = K.segStyle(segs[i], o);
    var l = K.text(c, segs[i][0], { font: st.font, size: size, just: "left", tracking: o.tracking === undefined ? -20 : o.tracking, color: st.color, name: (o.name || "say") + " " + segs[i][0].substr(0, 14) });
    var a = K.advOf(l, segs[i][0]);
    res.layers.push(l); res.adv.push(a); res.total += a;
  }
  var x = o.just == "left" ? cx : cx - res.total / 2;
  for (var j = 0; j < res.layers.length; j++) { K.tr(res.layers[j], "pos").setValue([x, y]); res.x.push(x); x += res.adv[j]; }
  return res;
};

// Character (or word) write-on: blur -> sharp, small rise, scale 82 -> 100, soft trailing bounce.
// D = sweep duration. o.by = "char" | "word". rate (s per unit) = D * 100 / (len * (100 + w)).
K.write = function (l, t0, D, o) {
  o = o || {};
  var size = o.size || 64, w = o.width || 34;
  var A = function () { return l.property("ADBE Text Properties").property("ADBE Text Animators"); };
  A().addProperty("ADBE Text Animator"); K.lastAnim(l).name = "write";
  K.ap(l).addProperty("ADBE Text Opacity").setValue(0);
  var bl = o.blur === undefined ? [14, 14] : (o.blur instanceof Array ? o.blur : [o.blur, o.blur]);
  K.ap(l).addProperty("ADBE Text Blur").setValue(bl);
  K.ap(l).addProperty("ADBE Text Position 3D").setValue([o.dx || -size * 0.12, o.dy === undefined ? size * 0.26 : o.dy, 0]);
  K.ap(l).addProperty("ADBE Text Scale 3D").setValue([o.sc || 82, o.sc || 82, 100]);
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  var adv = function () { return K.lastSel(l).property("ADBE Text Range Advanced"); };
  adv().property("ADBE Text Range Type2").setValue(K.byIndex(o.by)); adv().property("ADBE Text Range Shape").setValue(2);
  adv().property("ADBE Text Levels Max Ease").setValue(60); adv().property("ADBE Text Levels Min Ease").setValue(40);
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0); K.lastSel(l).property("ADBE Text Percent End").setValue(w);
  K.keys(K.lastSel(l).property("ADBE Text Percent Offset"), [[t0, -w, "lin"], [t0 + D, 100]]);
  if (o.bump !== 0) {
    var b = o.bump || 7, w2 = w * 1.2, v = (100 + w) / D;
    A().addProperty("ADBE Text Animator"); K.lastAnim(l).name = "bounce";
    K.ap(l).addProperty("ADBE Text Position 3D").setValue([0, -size * b / 100, 0]);
    K.ap(l).addProperty("ADBE Text Scale 3D").setValue([100 + b, 100 + b, 100]);
    K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
    adv().property("ADBE Text Range Type2").setValue(K.byIndex(o.by)); adv().property("ADBE Text Range Shape").setValue(6);
    K.lastSel(l).property("ADBE Text Percent Start").setValue(0); K.lastSel(l).property("ADBE Text Percent End").setValue(w2);
    var o0 = -w - w2 * 0.55;
    K.keys(K.lastSel(l).property("ADBE Text Percent Offset"), [[t0, o0, "lin"], [t0 + (100 - o0) / v, 100]]);
  }
  try { l.property("ADBE Text Properties").property("ADBE Text More Options").property("ADBE Text Anchor Point Align").setValue([0, -35]); } catch (e) {}
};
// write a laid-out line: first unit starts at t0, last unit starts at t1 (one rhythm across segments)
K.writeLay = function (lay, t0, t1, o) {
  o = o || {}; var w = o.width || 34, N = 0, i;
  for (i = 0; i < lay.layers.length; i++) N += K.nchars(K.srcText(lay.layers[i]));
  var r = (t1 - t0) / Math.max(1, N - 1), before = 0;
  for (i = 0; i < lay.layers.length; i++) {
    var n = K.nchars(K.srcText(lay.layers[i]));
    if (n == 0) continue;
    var o2 = {}; for (var k in o) if (o.hasOwnProperty(k)) o2[k] = o[k]; o2.size = lay.size;
    K.write(lay.layers[i], t0 + r * before, Math.max(0.12, r * n * (100 + w) / 100), o2);
    lay.layers[i].tIn = t0 + r * before;
    before += n;
  }
  lay.rate = r; return lay;
};
// exit: characters lift away into blur, in reading order
K.unwrite = function (lay, t, o) {
  o = o || {};
  for (var i = 0; i < lay.layers.length; i++) {
    if (!K.nchars(K.srcText(lay.layers[i]))) continue;
    K.hide(lay.layers[i], t + i * 0.025, o.dur || 0.24, "blur", { size: lay.size, width: 45, by: o.by });
    lay.layers[i].outPoint = t + i * 0.025 + (o.dur || 0.24) + 0.05;
  }
};
// say: lay out + write + returns lay with .out(t). Add K.push / K.drift so held text is never static.
K.say = function (c, segs, cx, y, t0, t1, o) {
  o = o || {};
  var lay = K.lay(c, segs, cx, y, o);
  K.writeLay(lay, t0, t1, o);
  for (var i = 0; i < lay.layers.length; i++) lay.layers[i].inPoint = Math.max(0, t0 - 0.05);
  lay.out = function (t, oo) { K.unwrite(lay, t, oo || { by: o.by }); };
  return lay;
};
// slow push on a set of layers (parented to a null at the line centre)
K.push = function (c, layers, cx, cy, t0, t1, amt) {
  var n = K.nul(c, "push", [cx, cy]); K.tr(n, "anchor").setValue([cx, cy]);
  for (var i = 0; i < layers.length; i++) layers[i].parent = n;
  K.keys(K.tr(n, "scale"), [[t0, [100, 100], "lin"], [t1, [100 + (amt || 3), 100 + (amt || 3)]]]);
  return n;
};

// Mask slide-up: each segment rises out of its own baseline mask, word by word, in reading order.
// segs as in K.lay. o.times[j] overrides the start of segment j. Returns {layers, out(t)}.
K.maskRise = function (c, segs, cx, y, o) {
  o = o || {};
  var lay = K.lay(c, segs, cx, y, o), size = lay.size;
  var tIn = o.tIn || 0, per = o.per || 0.04, words = 0;
  for (var j = 0; j < lay.layers.length; j++) {
    var L = lay.layers[j], rr = K.textRect(L);
    K.maskRect(L, rr.left - 20, rr.top - size * 0.4, rr.width + 40, rr.height + size * 0.9);
    var nw = segs[j][0].replace(/^\s+|\s+$/g, "").split(/\s+/).length;
    var t0 = (o.times && o.times[j] !== undefined) ? o.times[j] : tIn + words * per;
    K.reveal(L, t0, Math.max(0.35, nw * per + 0.3), "rise", { size: size, by: "word", width: 30, curve: "expo" });
    words += nw;
  }
  lay.out = function (t) { for (var k = 0; k < lay.layers.length; k++) K.hide(lay.layers[k], t + k * 0.02, 0.26, "rise", { size: size, by: "word", width: 40 }); };
  return lay;
};

// permanent recolour sweeping in reading order (left -> right for LTR)
K.recolor = function (l, t0, dur, hex) {
  l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  K.lastAnim(l).name = "recolor"; K.ap(l).addProperty("ADBE Text Fill Color").setValue(K.col(hex));
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  K.lastSel(l).property("ADBE Text Range Advanced").property("ADBE Text Range Shape").setValue(3);
  K.lastSel(l).property("ADBE Text Percent Start").setValue(0); K.lastSel(l).property("ADBE Text Percent End").setValue(40);
  K.go(K.lastSel(l).property("ADBE Text Percent Offset"), t0, -40, t0 + dur, 100, "inout");
};
// letters fall out of line (static random per letter) - for a line whose meaning is "nothing lines up". LTR/Latin only.
K.misalign = function (l, t, amt, rot) {
  l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
  K.lastAnim(l).name = "misalign";
  K.ap(l).addProperty("ADBE Text Position 3D"); K.ap(l).addProperty("ADBE Text Rotation");
  K.lastAnim(l).property("ADBE Text Selectors").addProperty("ADBE Text Wiggly Selector");
  var s = K.lastAnim(l).property("ADBE Text Selectors").property(1);
  s.property("ADBE Text Temporal Freq").setValue(0); s.property("ADBE Text Character Correlation").setValue(0);
  s.property("ADBE Text Wiggly Random Seed").setValue(7);
  K.spring(K.ap(l).property("ADBE Text Position 3D"), t, [0, 0, 0], t + 0.45, [0, amt, 0], 0.25);
  K.spring(K.ap(l).property("ADBE Text Rotation"), t, 0, t + 0.45, rot || 9, 0.25);
};

// Word swap in one slot: prefix + words[i] at times[i]; the line re-centres and the new word rides the same glide.
// prefix, words: segment arrays. o.wMul[i]: layout width factor for word i (e.g. a stretched word).
K.swapLine = function (c, prefix, words, cx, y, tIn, times, o) {
  o = o || {};
  var size = o.size || 64, i, j;
  var P = prefix.length ? K.lay(c, prefix, 0, y, { size: size, just: "left", dark: o.dark, name: "prefix" }) : { layers: [], adv: [], x: [], total: 0, size: size };
  var W = [], tot = [], x0 = [];
  for (i = 0; i < words.length; i++) {
    var wl = K.lay(c, [words[i]], 0, y, { size: size, just: "left", dark: o.dark, name: "slot" });
    W.push(wl); var ww = wl.total * (o.wMul && o.wMul[i] ? o.wMul[i] : 1);
    tot.push(P.total + ww); x0.push(o.just == "left" ? cx : cx - (P.total + ww) / 2);
  }
  for (j = 0; j < P.layers.length; j++) {
    var px = x0[0] + (P.x[j] - P.x[0]), ks = [[times[0] > tIn ? tIn : times[0], [px, y], "hold"]];
    for (i = 1; i < words.length; i++) {
      var pxi = x0[i] + (P.x[j] - P.x[0]);
      ks.push([times[i] - 0.06, [x0[i - 1] + (P.x[j] - P.x[0]), y], "inout"]); ks.push([times[i] + 0.28, [pxi, y], "hold"]);
    }
    K.keys(K.tr(P.layers[j], "pos"), ks);
  }
  var rate = o.rate || 0.026, Np = 0, tw0 = times[0];
  for (j = 0; j < P.layers.length; j++) Np += K.nchars(K.srcText(P.layers[j]));
  if (P.layers.length) { K.writeLay(P, tIn, tIn + rate * Math.max(1, Np - 1), { width: o.width }); tw0 = Math.max(times[0], tIn + rate * Np); }
  for (i = 0; i < W.length; i++) {
    var L = W[i].layers[0], xw = x0[i] + P.total;
    K.tr(L, "pos").setValue([xw, y]); W[i].x0 = xw;
    if (i == 0) { var n0 = K.nchars(words[0][0]); K.writeLay(W[0], tw0, tw0 + rate * Math.max(1, n0 - 1), { width: o.width }); }
    else {
      var rr = K.textRect(L); K.maskRect(L, rr.left - 30, rr.top - size * 0.35, rr.width * 1.8 + 60, rr.height + size * 0.7);
      K.reveal(L, times[i] + 0.02, 0.32, "rise", { size: size, width: 35, curve: "expo" });
      L.inPoint = times[i] - 0.02;
      K.keys(K.tr(L, "pos"), [[times[i] - 0.06, [x0[i - 1] + P.total, y], "inout"], [times[i] + 0.28, [xw, y]]]);
    }
    if (i < W.length - 1) {
      if (i == 0) { var r0 = K.textRect(L); K.maskRect(L, r0.left - 30, r0.top - size * 0.35, r0.width * 1.8 + 60, r0.height + size * 0.7); }
      K.hide(L, times[i + 1] - 0.14, 0.2, "rise", { size: size, width: 40 }); L.outPoint = times[i + 1] + 0.1;
    }
  }
  var res = { prefix: P, words: W, x0: x0, tot: tot, size: size, y: y };
  res.out = function (t) { if (P.layers.length) K.unwrite(P, t); K.unwrite(W[W.length - 1], t + 0.05); };
  return res;
};

// Real typing with a caret (chat prompt / search bar). Works for RTL text too: characters are appended to one text
// layer, so shaping stays intact; place the caret on the left end for RTL (o.rtl).
K.typeOn = function (c, str, x, y, t0, t1, o) {
  o = o || {};
  var l = K.text(c, str, { font: o.font || K.F.reg, size: o.size || 26, color: o.color || K.C.ink, just: o.rtl ? "right" : "left", pos: [x, y], tracking: -5, name: o.name || "typed" });
  var n = str.length, cps = (n - 1) / Math.max(0.05, t1 - t0), esc = str.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  l.property("ADBE Text Properties").property("ADBE Text Document").expression =
    'var n=Math.floor(clamp((time-' + t0.toFixed(3) + ')*' + cps.toFixed(3) + '+1,0,' + n + ')); "' + esc + '".substr(0,n)';
  var sz = o.size || 26;
  var cr = K.rect(c, (o.name || "typed") + " caret", 3, sz * 1.15, { fill: o.caret || K.C.acc, radius: 1.5 });
  var edge = o.rtl ? "r.left-5" : "(r.width>0?r.left+r.width:0)+5";
  K.tr(cr.layer, "pos").expression = 'var L=thisComp.layer("' + l.name + '"); var r=L.sourceRectAtTime(time,false); var p=L.toComp([' + edge + ',' + (-sz * 0.36).toFixed(1) + ']); [p[0],p[1]]';
  K.tr(cr.layer, "op").expression = '(time>' + (t0 - 0.05).toFixed(3) + '&&time<' + (t1 + 0.15).toFixed(3) + ')?100:((Math.floor((time-' + t1.toFixed(3) + ')*2.6)%2)?0:100)';
  cr.layer.motionBlur = false;
  return { layer: l, caret: cr.layer };
};

// Pill with an icon slot and a swapping label. items: [{t, label, icon: fn(c,x,y) -> [layers]}]
K.pillSwap = function (c, cx, cy, items, o) {
  o = o || {};
  var h = o.h || 64, size = o.size || 30, padL = o.icons === false ? 30 : 74, padR = 30, fill = o.fill || K.C.surface, col = o.color || "#FFFFFF";
  var labs = [], ws = [], lastIcon = null, i;
  for (i = 0; i < items.length; i++) {
    var l = K.text(c, items[i].label, { font: K.F.semi, size: size, color: col, just: "left", tracking: -10, name: "pill " + items[i].label });
    ws.push(K.advOf(l, items[i].label)); labs.push(l);
  }
  var W = function (k) { return padL + ws[k] + padR; };
  var bg = K.rect(c, "pill bg", W(0), h, { fill: fill, radius: h / 2, pos: [cx, cy] }); K.shadow(bg.layer, 30, 8, 26);
  for (i = 0; i < labs.length; i++) labs[i].moveBefore(bg.layer);   // background first, or it hides its own label
  var t0 = items[0].t, ks = [[t0, [W(0) * 0.3, h * 0.3], "expo"], [t0 + 0.42, [W(0), h], "hold"]];
  for (i = 1; i < items.length; i++) { ks.push([items[i].t - 0.06, [W(i - 1), h], "inout"]); ks.push([items[i].t + 0.36, [W(i), h], "hold"]); }
  K.keys(bg.size, ks); bg.layer.inPoint = t0;
  var left = function (k) { return cx - W(k) / 2; };
  for (i = 0; i < items.length; i++) {
    var L = labs[i], xl = left(i) + padL - 10;
    K.tr(L, "pos").setValue([xl, cy + size * 0.36]);
    var rr = K.textRect(L); K.maskRect(L, rr.left - 20, rr.top - size * 0.3, rr.width + 60, rr.height + size * 0.6);
    K.reveal(L, items[i].t + 0.04, 0.4, "rise", { size: size, width: 35, curve: "expo" }); L.inPoint = items[i].t;
    if (i < items.length - 1) { K.hide(L, items[i + 1].t - 0.1, 0.3, "rise", { size: size, width: 40 }); L.outPoint = items[i + 1].t + 0.25; }
    if (items[i].icon) {
      var ix = left(i) + 38, ic = K.ident(c, "pill icon " + i), parts = items[i].icon(c, ix, cy);
      for (var p = 0; p < parts.length; p++) parts[p].parent = ic;
      K.tr(ic, "anchor").setValue([ix, cy]); K.tr(ic, "pos").setValue([ix, cy]);
      var ti = items[i].t + 0.02, to = i < items.length - 1 ? items[i + 1].t - 0.08 : null;
      var sk = [[ti, [0, 0], "expo"], [ti + 0.22, [118, 118], "inout"], [ti + 0.4, [100, 100], "hold"]];
      if (to !== null) { sk.push([to, [100, 100], "in"]); sk.push([to + 0.18, [0, 0]]); }
      K.keys(K.tr(ic, "scale"), sk);
      for (p = 0; p < parts.length; p++) { parts[p].inPoint = ti; if (to !== null) parts[p].outPoint = to + 0.2; }
      if (to === null) lastIcon = { root: ic, parts: parts };
    }
  }
  var res = { bg: bg.layer, labels: labs, ws: ws, W: W };
  res.out = function (t) {
    K.go(bg.size, t, [W(items.length - 1), h], t + 0.3, [0, h * 0.2], "in"); bg.layer.outPoint = t + 0.3; K.hide(labs[labs.length - 1], t, 0.2, "blur", { size: size });
    if (lastIcon) for (var q = 0; q < lastIcon.parts.length; q++) lastIcon.parts[q].outPoint = t + 0.12;
  };
  return res;
};

// small generic line icons for pills / inline icons (30 px box). Replace with the brand's real icon set when it exists.
K.ICON = {
  check: function (c, x, y) { return [K.line(c, "i check", [[x - 10, y + 1], [x - 3, y + 8], [x + 11, y - 8]], { color: K.C.acc2, width: 4 }).layer]; },
  arrow: function (c, x, y) { return [K.line(c, "i arrow", [[x - 12, y], [x + 10, y]], { color: "#FFFFFF", width: 3.5 }).layer, K.line(c, "i arrow head", [[x + 2, y - 8], [x + 11, y], [x + 2, y + 8]], { color: "#FFFFFF", width: 3.5 }).layer]; },
  plus: function (c, x, y) { return [K.line(c, "i plus h", [[x - 10, y], [x + 10, y]], { color: "#FFFFFF", width: 3.5 }).layer, K.line(c, "i plus v", [[x, y - 10], [x, y + 10]], { color: "#FFFFFF", width: 3.5 }).layer]; },
  dot: function (c, x, y) { return [K.ellipse(c, "i dot", 12, 12, { fill: K.C.acc2, pos: [x, y] }).layer]; }
};
