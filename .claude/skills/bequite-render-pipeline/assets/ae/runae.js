#!/usr/bin/env node
// runae.js - run an ExtendScript (.jsx) file inside the running After Effects and print its result as JSON.
//
//   node runae.js <script.jsx> [--timeout 300] [--root <folder>]
//   node runae.js --detect                 print which After Effects would be used, then exit
//   node runae.js --help
//
// The script may set a global `RESULT` (any JSON-able value). It is written to <root>/build/result.json and printed.
// `AE_ROOT` (= --root, default: the folder this file sits in) is defined for the script, so it can
// $.evalFile(AE_ROOT + "/lib/core.jsx").
//
// AE path: env BEQUITE_AE_PATH, else auto-detected (see aepath.js). Never hardcoded.
// One-time user setting (BeQuite never changes it): AE > Preferences > Scripting & Expressions >
// "Allow Scripts to Write Files and Access Network".
// Exit codes: 0 ok, 1 script error, 2 setup error / timeout.
"use strict";
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { findAe } = require("./aepath");

function usage(code) {
  console.log([
    "usage: node runae.js <script.jsx> [--timeout SEC] [--root FOLDER]",
    "       node runae.js --detect",
    "",
    "  <script.jsx>     ExtendScript file to run inside the open After Effects",
    "  --timeout SEC    seconds to wait for the result (default 300)",
    "  --root FOLDER    project 'ae' folder: holds lib/ and build/ (default: this file's folder)",
    "  --detect         print the detected After Effects / aerender paths and exit",
    "",
    "env: BEQUITE_AE_PATH (AfterFX.com on Windows, the .app on macOS), BEQUITE_AERENDER_PATH (optional)",
  ].join("\n"));
  process.exit(code);
}

const argv = process.argv.slice(2);
if (!argv.length || argv.includes("--help") || argv.includes("-h")) usage(argv.length ? 0 : 2);
if (argv.includes("--detect")) {
  const r = findAe(); console.log(JSON.stringify(r, null, 2)); process.exit(r.error ? 2 : 0);
}

let scriptArg = null, timeoutSec = 300, root = __dirname;
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "--timeout") timeoutSec = Number(argv[++i]);
  else if (a === "--root") root = path.resolve(argv[++i]);
  else if (/^\d+$/.test(a) && scriptArg) timeoutSec = Number(a); // legacy: runae.js file.jsx 900
  else if (!scriptArg) scriptArg = a;
  else { console.error("unknown argument: " + a); usage(2); }
}
if (!scriptArg) usage(2);
if (!(timeoutSec > 0)) { console.error("--timeout must be a positive number"); process.exit(2); }

const script = path.resolve(scriptArg);
if (!fs.existsSync(script)) { console.error("script not found: " + script); process.exit(2); }

const ae = findAe();
if (ae.error) { console.error(ae.error); process.exit(2); }

const build = path.join(root, "build");
fs.mkdirSync(build, { recursive: true });
const result = path.join(build, "result.json");
const wrapper = path.join(build, "_run.jsx");
const fwd = (p) => p.split(path.sep).join("/");
const esc = (s) => s.replace(/\\/g, "/").replace(/"/g, '\\"');

let json2 = path.join(root, "lib", "json2.jsx");
if (!fs.existsSync(json2)) json2 = path.join(__dirname, "lib", "json2.jsx");

try { fs.unlinkSync(result); } catch (e) {}
fs.writeFileSync(wrapper, [
  "var RESULT = null, __err = null;",
  `var AE_ROOT = "${esc(fwd(root))}";`,
  "try {",
  `  $.evalFile(new File("${esc(fwd(json2))}"));`,
  `  $.evalFile(new File("${esc(fwd(script))}"));`,
  "} catch (e) { __err = (e && e.toString()) + ' @line ' + (e && e.line) + ' in ' + (e && e.fileName); }",
  `var __f = new File("${esc(fwd(result))}"); __f.encoding = "UTF-8"; __f.open("w");`,
  "__f.write(JSON.stringify({ ok: !__err, error: __err, result: RESULT })); __f.close();",
].join("\n"));

const t0 = Date.now();
let child;
if (ae.platform === "win32") {
  // AfterFX.com -r <file> runs the script in the already-open AE (starts AE if it is not running).
  child = spawn(ae.afterfx, ["-r", wrapper], { stdio: "ignore", detached: true });
} else {
  // macOS: AppleScript DoScriptFile (UNVERIFIED on this pack's test machine; documented in the AE scripting guide).
  const as = `tell application "${ae.appName.replace(/"/g, '\\"')}" to DoScriptFile "${fwd(wrapper).replace(/"/g, '\\"')}"`;
  child = spawn("osascript", ["-e", as], { stdio: "ignore", detached: true });
}
child.on("error", (e) => { console.error("could not start After Effects: " + e.message); process.exit(2); });
child.unref();

(function poll() {
  if (fs.existsSync(result)) {
    setTimeout(() => {
      const r = fs.readFileSync(result, "utf8");
      console.log(r);
      let ok = false; try { ok = JSON.parse(r).ok; } catch (e) {}
      process.exit(ok ? 0 : 1);
    }, 150);
  } else if (Date.now() - t0 > timeoutSec * 1000) {
    console.log("TIMEOUT: no result after " + timeoutSec + " s. Check: is 'Allow Scripts to Write Files and Access Network' ticked? Is a dialog open in AE? Is AE still busy?");
    process.exit(2);
  } else setTimeout(poll, 250);
})();
