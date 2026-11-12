/* kinetic.js - dependency-free kinetic typography for the browser (Web Animations API).
 * One function per treatment in ../references/toolbox.md. Works in any page, in an HTML-to-video renderer
 * (Remotion / HyperFrames / headless-browser frame capture) or as a reference for a GSAP / CSS port.
 *
 *   <script src="kinetic.js"></script>
 *   Kinetic.writeOn(el, { dur: 0.6 });         // headline: blur -> sharp, small rise, by character
 *   Kinetic.swapInPlace(slot, ["calm.", "focus.", "you."], { every: 1.1 });
 *
 * Connected scripts (Arabic, Persian, Urdu...) and RTL: units default to WORDS, never single letters, because
 * splitting a connected word into separately transformed boxes breaks letter joining. Reveals follow the
 * text's own direction (dir="rtl" -> right to left). See ../references/arabic-rtl.md.
 * prefers-reduced-motion: every treatment degrades to a short opacity fade.
 * For frame-accurate video renders, pass { paused: true } and drive the returned animations' currentTime
 * from the renderer's frame clock (Kinetic.seek(anims, ms)).
 */
(function (root) {
  "use strict";

  var CONNECTED = /[؀-ۿݐ-ݿࡰ-࢟ࢠ-ࣿﭐ-﷿ﹰ-﻿܀-ݏ߀-߿]/;
  var EASE_OUT = "cubic-bezier(0.16, 1, 0.3, 1)";      // strong ease-out for arrivals
  var EASE_IN = "cubic-bezier(0.7, 0, 0.84, 0)";        // accelerate away for exits
  var EASE_INOUT = "cubic-bezier(0.65, 0, 0.35, 1)";

  function reduced() {
    return !!(root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }
  function isRTL(el) {
    var d = el.closest && el.closest("[dir]");
    if (d) return d.getAttribute("dir").toLowerCase() === "rtl";
    return root.getComputedStyle ? root.getComputedStyle(el).direction === "rtl" : false;
  }
  function isConnected(text) { return CONNECTED.test(text); }
  function ms(s) { return Math.round(s * 1000); }

  // Split el's text into spans. by: "char" | "word" | "auto" (auto = words for connected scripts, chars otherwise).
  // Characters use Intl.Segmenter graphemes when available, so emoji and combining marks stay whole.
  function split(el, by) {
    if (el.__kinetic) return el.__kinetic;
    var text = el.textContent;
    var mode = by || "auto";
    if (mode === "auto") mode = isConnected(text) ? "word" : "char";
    if (mode === "char" && isConnected(text)) mode = "word";   // safety: never split a connected word into letters
    el.textContent = "";
    el.setAttribute("aria-label", text);
    var units = [];
    var words = text.split(/(\s+)/);
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (!w) continue;
      if (/^\s+$/.test(w)) { el.appendChild(document.createTextNode(w)); continue; }
      var wordSpan = document.createElement("span");
      wordSpan.className = "k-word";
      wordSpan.setAttribute("aria-hidden", "true");
      wordSpan.style.display = "inline-block";
      wordSpan.style.whiteSpace = "nowrap";
      if (mode === "word") {
        wordSpan.textContent = w; units.push(wordSpan);
      } else {
        var parts = graphemes(w);
        for (var j = 0; j < parts.length; j++) {
          var c = document.createElement("span");
          c.className = "k-char"; c.textContent = parts[j]; c.style.display = "inline-block";
          wordSpan.appendChild(c); units.push(c);
        }
      }
      el.appendChild(wordSpan);
    }
    el.__kinetic = { units: units, mode: mode, text: text };
    return el.__kinetic;
  }
  function graphemes(s) {
    if (root.Intl && Intl.Segmenter) {
      var out = [], it = new Intl.Segmenter(undefined, { granularity: "grapheme" }).segment(s);
      for (var seg of it) out.push(seg.segment);
      return out;
    }
    return Array.from(s);
  }
  function play(list, o) {
    if (o && o.paused) for (var i = 0; i < list.length; i++) list[i].pause();
    return list;
  }
  function fadeOnly(el, o) {
    return play([el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, delay: ms(o.delay || 0), fill: "both" })], o);
  }
  // per-unit delays spread so the LAST unit starts at dur * (1 - tail) (one rhythm across the line)
  function stagger(n, dur, tail) {
    var span = dur * (1 - (tail === undefined ? 0.45 : tail));
    var step = n > 1 ? span / (n - 1) : 0;
    var d = []; for (var i = 0; i < n; i++) d.push(i * step);
    return { delays: d, unitDur: Math.max(0.12, dur - span) };
  }

  // 1. Blur-in write-on (headline / turning point)
  function writeOn(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    var s = split(el, o.by), u = s.units, st = stagger(u.length, o.dur || 0.6), rise = o.rise === undefined ? 0.26 : o.rise;
    var out = [];
    for (var i = 0; i < u.length; i++) {
      out.push(u[i].animate([
        { opacity: 0, filter: "blur(" + (o.blur || 12) + "px)", transform: "translateY(" + rise + "em) scale(" + (o.scale || 0.82) + ")" },
        { opacity: 1, filter: "blur(0px)", transform: "translateY(" + (-rise * 0.08) + "em) scale(1.03)", offset: 0.75 },
        { opacity: 1, filter: "blur(0px)", transform: "translateY(0) scale(1)" }
      ], { duration: ms(st.unitDur), delay: ms((o.delay || 0) + st.delays[i]), easing: EASE_OUT, fill: "both" }));
    }
    return play(out, o);
  }

  // 2. Mask slide-up (calm, editorial): each word rises from behind its own baseline mask
  function maskRise(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    var s = split(el, "word"), u = s.units, out = [];
    for (var i = 0; i < u.length; i++) {
      var w = u[i];
      if (!w.parentNode.classList.contains("k-mask")) {
        var m = document.createElement("span");
        m.className = "k-mask"; m.style.display = "inline-block"; m.style.overflow = "hidden";
        m.style.verticalAlign = "bottom"; m.style.paddingBottom = "0.12em"; m.style.marginBottom = "-0.12em";
        m.style.paddingTop = "0.25em"; m.style.marginTop = "-0.25em";   // room for ascenders / Arabic marks
        w.parentNode.insertBefore(m, w); m.appendChild(w);
      }
      out.push(w.animate([{ transform: "translateY(110%)" }, { transform: "translateY(0)" }],
        { duration: ms(o.unitDur || 0.45), delay: ms((o.delay || 0) + i * (o.stagger || 0.04)), easing: EASE_OUT, fill: "both" }));
    }
    return play(out, o);
  }

  // 3. Directional smear (energetic): word travels in with a stretched, blurred look and lands with a small overshoot.
  // CSS has no directional blur; scaleX stretch + blur approximates it. Direction follows the text direction.
  function smear(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    var s = split(el, "word"), u = s.units, dir = isRTL(el) ? -1 : 1, dx = (o.dx || 0.9) * dir, out = [];
    for (var i = 0; i < u.length; i++) {
      out.push(u[i].animate([
        { opacity: 0, filter: "blur(8px)", transform: "translateX(" + (-dx) + "em) scaleX(1.6)" },
        { opacity: 1, filter: "blur(2px)", transform: "translateX(" + (0.03 * dir) + "em) scaleX(1.04)", offset: 0.7 },
        { opacity: 1, filter: "blur(0px)", transform: "translateX(0) scaleX(1)" }
      ], { duration: ms(o.unitDur || 0.18), delay: ms((o.delay || 0) + i * (o.stagger || 0.09)), easing: EASE_OUT, fill: "both" }));
    }
    return play(out, o);
  }

  // 4. Scale punch (one emphasis word)
  function punch(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    el.style.display = el.style.display || "inline-block";
    return play([el.animate([{ transform: "scale(" + (o.from || 1.25) + ")" }, { transform: "scale(1)" }],
      { duration: ms(o.dur || 0.35), delay: ms(o.delay || 0), easing: EASE_OUT, fill: "both" })], o);
  }

  // 5. Letter pop (brand moment). Latin only - connected scripts pop by word automatically.
  function letterPop(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    var s = split(el, o.by || "auto"), u = s.units, out = [];
    for (var i = 0; i < u.length; i++) {
      out.push(u[i].animate([
        { opacity: 0, transform: "scale(0)" }, { opacity: 1, transform: "scale(" + (o.bump || 1.28) + ")", offset: 0.6 },
        { opacity: 1, transform: "scale(1)" }
      ], { duration: ms(o.unitDur || 0.32), delay: ms((o.delay || 0) + i * (o.stagger || 0.035)), easing: EASE_OUT, fill: "both" }));
    }
    return play(out, o);
  }

  // 6. Swap in place (lists / alternatives): one slot, words roll out and in; the slot width glides.
  function swapInPlace(slot, words, o) {
    o = o || {};
    var every = o.every || 1.1, out = [];
    slot.style.display = "inline-block"; slot.style.position = "relative"; slot.style.overflow = "hidden";
    slot.style.verticalAlign = "bottom"; slot.style.transition = "width " + (o.glide || 0.3) + "s " + EASE_INOUT;
    slot.style.paddingTop = "0.2em"; slot.style.marginTop = "-0.2em";
    slot.textContent = "";
    var spans = words.map(function (w) {
      var sp = document.createElement("span");
      sp.textContent = w; sp.style.display = "inline-block"; sp.style.whiteSpace = "nowrap";
      sp.style.position = "absolute"; sp.style.insetInlineStart = "0"; sp.style.opacity = "0";
      slot.appendChild(sp); return sp;
    });
    function widthOf(sp) { return sp.getBoundingClientRect().width; }
    spans[0].style.position = "relative"; spans[0].style.opacity = "1";
    slot.style.width = widthOf(spans[0]) + "px";
    var red = reduced();
    spans.forEach(function (sp, i) {
      if (i === 0) return;
      var t = (o.delay || 0) + i * every;
      var prev = spans[i - 1];
      out.push(prev.animate(red ? [{ opacity: 1 }, { opacity: 0 }] : [{ transform: "translateY(0)", opacity: 1 }, { transform: "translateY(-110%)", opacity: 0 }],
        { duration: ms(0.2), delay: ms(t - 0.14), easing: EASE_IN, fill: "forwards" }));
      out.push(sp.animate(red ? [{ opacity: 0 }, { opacity: 1 }] : [{ transform: "translateY(110%)", opacity: 1 }, { transform: "translateY(0)", opacity: 1 }],
        { duration: ms(0.32), delay: ms(t), easing: EASE_OUT, fill: "both" }));
      setTimeout(function () { slot.style.width = widthOf(sp) + "px"; }, ms(t - 0.06));
    });
    return play(out, o);
  }

  // 7. Recolour sweep (one key word). No splitting: a gradient clipped to the text slides across it, so it is safe
  // for connected scripts. Sweeps in the text's direction.
  function recolour(el, o) {
    o = o || {};
    var from = o.from || root.getComputedStyle(el).color, to = o.to || "#2F6BFF";
    var rtl = isRTL(el);
    el.style.backgroundImage = "linear-gradient(" + (rtl ? "to left" : "to right") + ", " + to + " 0%, " + to + " 45%, " + from + " 55%, " + from + " 100%)";
    el.style.backgroundSize = "220% 100%";
    el.style.webkitBackgroundClip = "text"; el.style.backgroundClip = "text";
    el.style.color = "transparent"; el.style.webkitTextFillColor = "transparent";
    var start = rtl ? "0% 0" : "100% 0", end = rtl ? "100% 0" : "0% 0";
    if (reduced()) { el.style.backgroundPosition = end; return []; }
    return play([el.animate([{ backgroundPosition: start }, { backgroundPosition: end }],
      { duration: ms(o.dur || 0.45), delay: ms(o.delay || 0), easing: EASE_INOUT, fill: "both" })], o);
  }

  // 8. Typing with a caret (chat / search / command). Text grows inside one node, so shaping stays correct in RTL.
  function typeOn(el, text, o) {
    o = o || {};
    var cps = o.cps || 18, units = graphemes(text), caret = document.createElement("span");
    caret.className = "k-caret"; caret.textContent = "​";
    caret.style.display = "inline-block"; caret.style.width = "0.08em"; caret.style.height = "1.05em";
    caret.style.verticalAlign = "-0.15em"; caret.style.background = o.caretColor || "currentColor";
    caret.style.marginInlineStart = "0.06em";
    var node = document.createTextNode("");
    el.textContent = ""; el.appendChild(node); el.appendChild(caret);
    el.setAttribute("aria-label", text);
    var i = 0, startAt = (o.delay || 0) * 1000;
    var blink = caret.animate([{ opacity: 1 }, { opacity: 1, offset: 0.5 }, { opacity: 0, offset: 0.51 }, { opacity: 0 }],
      { duration: 800, iterations: Infinity });
    var timer = setTimeout(function tick() {
      i++; node.data = units.slice(0, i).join("");
      if (i < units.length) timer = setTimeout(tick, 1000 / cps * (/[\s,.]/.test(units[i - 1]) ? 1.8 : 1));
      else if (o.done) o.done();
    }, startAt);
    return { cancel: function () { clearTimeout(timer); blink.cancel(); }, caret: caret };
  }

  // 9. Inline icon grows into the sentence (and can later swap with the word next to it)
  function growIn(el, o) {
    o = o || {};
    if (reduced()) return fadeOnly(el, o);
    el.style.display = "inline-block";
    return play([el.animate([
      { transform: "scale(0)", opacity: 0, width: "0px" },
      { transform: "scale(1.15)", opacity: 1, width: (o.width || "1.1em"), offset: 0.6 },
      { transform: "scale(1)", opacity: 1, width: (o.width || "1.1em") }
    ], { duration: ms(o.dur || 0.45), delay: ms(o.delay || 0), easing: EASE_OUT, fill: "both" })], o);
  }

  // Exit: units lift away into blur in reading order (or a whole-element fade for reduced motion)
  function unwrite(el, o) {
    o = o || {};
    if (reduced()) return play([el.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 160, delay: ms(o.delay || 0), fill: "forwards" })], o);
    var s = split(el, o.by), u = s.units, out = [];
    for (var i = 0; i < u.length; i++) {
      out.push(u[i].animate([{ opacity: 1, filter: "blur(0px)", transform: "translateY(0)" },
        { opacity: 0, filter: "blur(10px)", transform: "translateY(-0.25em)" }],
        { duration: ms(o.unitDur || 0.24), delay: ms((o.delay || 0) + i * (o.stagger || 0.02)), easing: EASE_IN, fill: "forwards" }));
    }
    return play(out, o);
  }

  // Slow living push while a line holds (nothing is ever fully static)
  function drift(el, o) {
    o = o || {};
    if (reduced()) return [];
    return play([el.animate([{ transform: "scale(1)" }, { transform: "scale(" + (1 + (o.amount || 0.02)) + ")" }],
      { duration: ms(o.dur || 3), delay: ms(o.delay || 0), easing: "linear", fill: "both" })], o);
  }

  // Reading-time rule (owned by the kinetic-type skill): hold after landing = max(1 s, 0.35 s x words + 0.5 s),
  // x1.5 when the line is not also spoken. Returns seconds.
  function holdFor(text, spoken) {
    var words = String(text).trim().split(/\s+/).filter(Boolean).length;
    var h = Math.max(1, 0.35 * words + 0.5);
    return spoken === false ? h * 1.5 : h;
  }

  function seek(anims, msTime) { for (var i = 0; i < anims.length; i++) anims[i].currentTime = msTime; }

  root.Kinetic = {
    split: split, writeOn: writeOn, maskRise: maskRise, smear: smear, punch: punch, letterPop: letterPop,
    swapInPlace: swapInPlace, recolour: recolour, typeOn: typeOn, growIn: growIn, unwrite: unwrite, drift: drift,
    holdFor: holdFor, seek: seek, isConnected: isConnected,
    EASE: { out: EASE_OUT, "in": EASE_IN, inout: EASE_INOUT }
  };
})(typeof window !== "undefined" ? window : globalThis);
