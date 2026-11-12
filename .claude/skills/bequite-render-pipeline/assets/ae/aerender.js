#!/usr/bin/env node
// aerender.js - render an After Effects project with aerender, with optional cache purge before and after.
//
//   node aerender.js --project film.aep [--rqindex 1] [--purge] [--sound OFF] [-- <extra aerender args>]
//   node aerender.js --project film.aep --comp "FILM" --output out/film.mov [--purge]
//   node aerender.js --project film.aep --comp "FILM" --frame 120 --output stills/f120.png   (one still)
//
// aerender path: env BEQUITE_AERENDER_PATH, else next to the detected AfterFX (see aepath.js).
// --purge runs build/purge.jsx inside the open AE via runae.js before and after the render
// (the AE disk cache can fill a disk during long build + render sessions).
// This is a full render: in BeQuite it runs only after the render plan was approved (hard stop M8).
"use strict";
const path = require("path");
const fs = require("fs");
const { spawnSync } = require("child_process");
const { findAe } = require("./aepath");

function usage(code) {
  console.log([
    "usage: node aerender.js --project FILE.aep [--rqindex N | --comp NAME --output FILE [--frame N]]",
    "                        [--purge] [--sound ON|OFF] [--root FOLDER] [-- extra aerender args]",
    "",
    "  --project   absolute or relative path to the .aep (required)",
    "  --rqindex   render-queue item to render (default 1 when --comp is not given)",
    "  --comp      render this comp instead of a queue item (needs --output)",
    "  --frame     render a single frame (sets -s and -e)",
    "  --purge     purge AE caches before and after (needs AE open + runae.js)",
    "  --sound     aerender -sound flag (default OFF)",
    "  --root      folder holding build/purge.jsx (default: this file's folder)",
  ].join("\n"));
  process.exit(code);
}

const argv = process.argv.slice(2);
if (!argv.length || argv.includes("--help") || argv.includes("-h")) usage(argv.length ? 0 : 2);
const o = { rqindex: null, comp: null, output: null, frame: null, purge: false, sound: "OFF", root: __dirname, extra: [] };
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "--") { o.extra = argv.slice(i + 1); break; }
  else if (a === "--project") o.project = path.resolve(argv[++i]);
  else if (a === "--rqindex") o.rqindex = Number(argv[++i]);
  else if (a === "--comp") o.comp = argv[++i];
  else if (a === "--output") o.output = path.resolve(argv[++i]);
  else if (a === "--frame") o.frame = Number(argv[++i]);
  else if (a === "--purge") o.purge = true;
  else if (a === "--sound") o.sound = String(argv[++i]).toUpperCase();
  else if (a === "--root") o.root = path.resolve(argv[++i]);
  else { console.error("unknown argument: " + a); usage(2); }
}
if (!o.project || !fs.existsSync(o.project)) { console.error("project not found: " + o.project); process.exit(2); }
if (o.comp && !o.output) { console.error("--comp needs --output"); process.exit(2); }
// aerender refuses to write into a folder that does not exist ("Directory does not exist"): create it first.
if (o.output) fs.mkdirSync(path.dirname(o.output), { recursive: true });

const ae = findAe();
if (ae.error) { console.error(ae.error); process.exit(2); }
if (!ae.aerender) { console.error("aerender not found next to After Effects. Set BEQUITE_AERENDER_PATH."); process.exit(2); }

function purge(label) {
  const purgeJsx = path.join(o.root, "build", "purge.jsx");
  if (!fs.existsSync(purgeJsx)) { console.error("purge.jsx not found at " + purgeJsx); return; }
  const r = spawnSync(process.execPath, [path.join(__dirname, "runae.js"), purgeJsx, "--timeout", "60", "--root", o.root], { encoding: "utf8" });
  console.log(`[purge ${label}] exit ${r.status} ${String(r.stdout || "").trim()}`);
}

const args = ["-project", o.project];
if (o.comp) {
  args.push("-comp", o.comp, "-output", o.output);
  if (o.frame !== null) args.push("-s", String(o.frame), "-e", String(o.frame));
} else {
  args.push("-rqindex", String(o.rqindex || 1));
}
args.push("-sound", o.sound, ...o.extra);

if (o.purge) purge("before");
console.log("RUN " + JSON.stringify([ae.aerender, ...args]));
const t0 = Date.now();
const r = spawnSync(ae.aerender, args, { stdio: "inherit" });
const secs = ((Date.now() - t0) / 1000).toFixed(1);
if (o.purge) purge("after");
console.log(`aerender exit ${r.status} after ${secs} s`);
process.exit(r.status === null ? 2 : r.status);
