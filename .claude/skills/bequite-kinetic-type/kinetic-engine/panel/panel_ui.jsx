// BQ Kinetic panel UI. make_panel.py joins the engine and this file into "BQ Kinetic.jsx".
// Install: copy "BQ Kinetic.jsx" into After Effects' "Scripts/ScriptUI Panels" folder, restart, open Window > BQ Kinetic.jsx.
// Or run it once with File > Scripts > Run Script File. Needs: Preferences > Scripting & Expressions >
// "Allow Scripts to Write Files and Access Network" (for the contact sheet, the render path and the clipboard).
(function (thisObj) {
  var ROUND = 0, LAST_REPORT = "", LAST_SHEET_DIR = null;

  function baseFolder(name) {
    var base = (app.project && app.project.file) ? app.project.file.parent : Folder.desktop;
    var f = new Folder(base.fsName + "/" + name);
    if (!f.exists) f.create();
    return f;
  }
  function safeName(s) { return String(s).replace(/[^A-Za-z0-9_\-]+/g, "_").replace(/^_+|_+$/g, "") || "film"; }
  function listLines(a) { var s = ""; for (var i = 0; i < a.length; i++) s += "\n- " + a[i]; return s; }
  function count(n, word) { return n + " " + word + (n === 1 ? "" : "s"); }
  function copyText(s) {
    try {
      var f = new File(Folder.temp.fsName + "/bqk_report.txt");
      f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close();
      if ($.os.indexOf("Windows") >= 0) system.callSystem('powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 \'' + f.fsName + '\' | Set-Clipboard"');
      else system.callSystem("LANG=en_US.UTF-8 pbcopy < '" + f.fsName + "'");
      return true;
    } catch (e) { return false; }
  }
  function lastComp() {
    try { if (BQK.LAST && BQK.LAST.comp && BQK.LAST.comp.name) return BQK.LAST.comp; } catch (e) {}
    var a = app.project.activeItem;
    return (a && a instanceof CompItem && !/ sheet$/.test(a.name)) ? a : null;
  }

  // ------------------------------------------------------------------ the window
  var ui = (thisObj instanceof Panel) ? thisObj : new Window("palette", "BQ Kinetic", undefined, { resizeable: true });
  ui.orientation = "column"; ui.alignChildren = ["fill", "top"]; ui.spacing = 6; ui.margins = 10;
  ui.add("statictext", undefined, "Paste the director's reply (or just its JSON):");
  var input = ui.add("edittext", undefined, "", { multiline: true, scrolling: true, wantReturn: true });
  input.preferredSize = [400, 190];
  var r1 = ui.add("group"); r1.orientation = "row"; r1.alignChildren = ["fill", "center"];
  var bLoad = r1.add("button", undefined, "Load .json");
  var bCheck = r1.add("button", undefined, "Check");
  var bBuild = r1.add("button", undefined, "Build");
  var bSheet = r1.add("button", undefined, "Contact sheet");
  var cRQ = ui.add("checkbox", undefined, "Add the film to the Render Queue (H.264)"); cRQ.value = true;
  ui.add("statictext", undefined, "Report (copy it back to the director):");
  var out = ui.add("edittext", undefined, "", { multiline: true, scrolling: true, readonly: true });
  out.preferredSize = [400, 150];
  var r2 = ui.add("group"); r2.orientation = "row"; r2.alignChildren = ["fill", "center"];
  var bCopy = r2.add("button", undefined, "Copy report");
  var bOpen = r2.add("button", undefined, "Open sheets folder");

  function show(s) { LAST_REPORT = s; out.text = s; }

  bLoad.onClick = function () {
    var f = File.openDialog("Choose a BQ Kinetic JSON file", "*.json;*.txt");
    if (!f) return;
    f.encoding = "UTF-8"; f.open("r"); input.text = f.read(); f.close();
    show("Loaded " + f.name + ". Press Check or Build.");
  };

  bCheck.onClick = function () {
    var r = BQK.check(input.text);
    if (r.errors.length) show("The JSON did not pass the check (" + count(r.errors.length, "error") + "):" + listLines(r.errors) +
      (r.warnings.length ? "\nWarnings:" + listLines(r.warnings) : "") + "\nFix every error and send the complete JSON again.");
    else {
      var n = 0; for (var i = 0; i < r.doc.scenes.length; i++) n += r.doc.scenes[i].words.length;
      show("Check passed: " + count(r.doc.scenes.length, "scene") + ", " + count(n, "word") + ", " + count(r.warnings.length, "warning") + "." +
        (r.warnings.length ? listLines(r.warnings) : "") + "\nPress Build.");
    }
  };

  bBuild.onClick = function () {
    var chk = BQK.check(input.text);
    if (chk.errors.length) { bCheck.onClick(); return; }
    ROUND++;
    var title = chk.doc.title, opts = {};
    if (cRQ.value) {
      try { opts.outFile = baseFolder("BQ Kinetic renders").fsName + "/" + safeName(title) + "_round" + ROUND + ".mp4"; }
      catch (e) { show("Could not create the renders folder. Turn on Preferences > Scripting & Expressions > Allow Scripts to Write Files and Access Network."); return; }
    }
    var r;
    try { r = BQK.build(input.text, opts); }
    catch (e) { show("The build stopped: " + e.toString() + (e.line ? " (line " + e.line + ")" : "") + "\nUndo (Ctrl+Z) removes what was made."); return; }
    if (!r.ok) { show("The JSON did not pass the check:" + listLines(r.errors)); return; }
    try { r.comp.openInViewer(); } catch (e) {}
    show("Round " + ROUND + ": built in After Effects with 0 errors and " + count(r.warnings.length, "warning") + ". Length " + r.duration +
      " s, " + count(r.scenes.length, "scene") + "." + (r.warnings.length ? listLines(r.warnings) : "") +
      "\nThe contact sheet is attached (12 frames, the time of each frame in its top-left corner). Do step 5: critique it " +
      "(at most five points, each with its time), then send the complete revised JSON." +
      (opts.outFile ? "\n\n[for you, not the director] Render: Composition > Add to Render Queue is done; press Render. File: " + opts.outFile : ""));
  };

  bSheet.onClick = function () {
    var comp = lastComp();
    if (!comp) { show("Build a film first, or select its composition in the Project panel."); return; }
    var dir;
    try { dir = baseFolder("BQ Kinetic sheets"); }
    catch (e) { show("Could not create the sheets folder. Turn on Preferences > Scripting & Expressions > Allow Scripts to Write Files and Access Network."); return; }
    var file = dir.fsName + "/" + safeName(comp.name) + "_round" + Math.max(ROUND, 1) + ".png", res;
    try { res = BQK.sheet(comp, file, 12, null, 20000); }
    catch (e) { show("The contact sheet failed: " + e.toString()); return; }
    LAST_SHEET_DIR = dir;
    show(LAST_REPORT + "\n\nContact sheet: " + file + (res.written ? "\nSaved. Attach it to your reply to the director." :
      "\nAfter Effects is still writing it; it appears in that folder in a moment."));
  };

  bCopy.onClick = function () {
    if (!LAST_REPORT) return;
    var cut = LAST_REPORT.indexOf("\n\n[for you");
    var txt = cut > 0 ? LAST_REPORT.substring(0, cut) : LAST_REPORT;
    cut = txt.indexOf("\n\nContact sheet:");
    if (cut > 0) txt = txt.substring(0, cut);
    if (!copyText(txt)) alert("Copy failed. Select the report text and press Ctrl+C (Cmd+C).");
  };

  bOpen.onClick = function () {
    var d = LAST_SHEET_DIR;
    try { if (!d) d = baseFolder("BQ Kinetic sheets"); d.execute(); } catch (e) { show("Could not open the folder: " + e.toString()); }
  };

  if ($.global.BQK_PANEL_TEST) {  // tests drive the buttons without showing the window
    $.global.BQK_PANEL = { ui: ui, input: input, out: out, check: bCheck, build: bBuild, sheet: bSheet, copy: bCopy, rq: cRQ };
    return;
  }
  ui.onResizing = ui.onResize = function () { this.layout.resize(); };
  if (ui instanceof Window) { ui.center(); ui.show(); } else { ui.layout.layout(true); }
})(this);
