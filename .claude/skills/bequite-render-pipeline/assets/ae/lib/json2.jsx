// Minimal JSON.stringify for ExtendScript (ES3). Loaded by runae.js before the user script.
if (typeof JSON === "undefined") { JSON = {}; }
if (!JSON.stringify) {
  JSON.stringify = function (v) {
    function q(s) {
      return '"' + String(s).replace(/[\\"]/g, function (c) { return "\\" + c; })
        .replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t") + '"';
    }
    if (v === null || v === undefined) return "null";
    var t = typeof v;
    if (t === "number") return isFinite(v) ? String(v) : "null";
    if (t === "boolean") return String(v);
    if (t === "string") return q(v);
    if (v instanceof Array) { var a = []; for (var i = 0; i < v.length; i++) a.push(JSON.stringify(v[i])); return "[" + a.join(",") + "]"; }
    var o = []; for (var k in v) if (v.hasOwnProperty(k)) o.push(q(k) + ":" + JSON.stringify(v[k])); return "{" + o.join(",") + "}";
  };
}
