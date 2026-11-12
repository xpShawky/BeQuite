// aepath.js - find After Effects and aerender without hardcoding a path.
// Order: env BEQUITE_AE_PATH (and BEQUITE_AERENDER_PATH) -> auto-detect common install folders.
// Windows: BEQUITE_AE_PATH = full path to AfterFX.com (or the "Support Files" folder, or the version folder).
// macOS:   BEQUITE_AE_PATH = path to "Adobe After Effects <ver>.app" (or the folder that contains it).
"use strict";
const fs = require("fs");
const path = require("path");

const IS_WIN = process.platform === "win32";
const IS_MAC = process.platform === "darwin";

function exists(p) { try { return !!p && fs.existsSync(p); } catch (e) { return false; } }

// "Adobe After Effects 2026" -> 2026 ; "Adobe After Effects CC 2019" -> 2019 ; "Adobe After Effects (Beta)" -> 9999 (sorted last unless asked)
function versionKey(name) {
  const m = name.match(/(\d{4})/);
  const beta = /beta/i.test(name);
  return { year: m ? Number(m[1]) : 0, beta };
}

function listAeFolders(base) {
  if (!exists(base)) return [];
  let names = [];
  try { names = fs.readdirSync(base); } catch (e) { return []; }
  return names
    .filter((n) => /^Adobe After Effects/i.test(n))
    .map((n) => ({ name: n, dir: path.join(base, n), key: versionKey(n) }))
    .sort((a, b) => (a.key.beta - b.key.beta) || (b.key.year - a.key.year));
}

// Windows: resolve to ...\Support Files\AfterFX.com
function resolveWinAfterFx(p) {
  if (!p) return null;
  if (/afterfx\.(com|exe)$/i.test(p)) return exists(p) ? p : null;
  const tries = [path.join(p, "AfterFX.com"), path.join(p, "Support Files", "AfterFX.com")];
  for (const t of tries) if (exists(t)) return t;
  return null;
}

// macOS: resolve to the .app bundle
function resolveMacApp(p) {
  if (!p) return null;
  if (/\.app\/?$/i.test(p)) return exists(p) ? p.replace(/\/$/, "") : null;
  if (!exists(p)) return null;
  try {
    const app = fs.readdirSync(p).find((n) => /^Adobe After Effects.*\.app$/i.test(n));
    if (app) return path.join(p, app);
  } catch (e) {}
  return null;
}

function candidatesWin() {
  const bases = [];
  for (const v of ["ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"]) {
    if (process.env[v]) bases.push(path.join(process.env[v], "Adobe"));
  }
  bases.push("C:\\Program Files\\Adobe");
  const seen = new Set(), out = [];
  for (const b of bases) {
    if (seen.has(b.toLowerCase())) continue; seen.add(b.toLowerCase());
    for (const f of listAeFolders(b)) out.push(f.dir);
  }
  return out;
}

function candidatesMac() {
  return listAeFolders("/Applications").map((f) => f.dir);
}

// Returns { platform, afterfx (win) | app (mac), aerender, source } or { error }
function findAe() {
  const env = process.env.BEQUITE_AE_PATH;
  if (IS_WIN) {
    let afterfx = null, source = null;
    if (env) { afterfx = resolveWinAfterFx(env); source = "BEQUITE_AE_PATH"; if (!afterfx) return { error: `BEQUITE_AE_PATH is set but AfterFX.com was not found under: ${env}` }; }
    else { for (const d of candidatesWin()) { afterfx = resolveWinAfterFx(d); if (afterfx) { source = "auto-detect"; break; } } }
    if (!afterfx) return { error: "After Effects not found. Set BEQUITE_AE_PATH to the full path of AfterFX.com (e.g. <Adobe folder>\\Adobe After Effects <ver>\\Support Files\\AfterFX.com)." };
    let aerender = process.env.BEQUITE_AERENDER_PATH || path.join(path.dirname(afterfx), "aerender.exe");
    if (!exists(aerender)) aerender = null;
    return { platform: "win32", afterfx, aerender, source };
  }
  if (IS_MAC) {
    let app = null, source = null;
    if (env) { app = resolveMacApp(env); source = "BEQUITE_AE_PATH"; if (!app) return { error: `BEQUITE_AE_PATH is set but no "Adobe After Effects*.app" was found at: ${env}` }; }
    else { for (const d of candidatesMac()) { app = resolveMacApp(d); if (app) { source = "auto-detect"; break; } } }
    if (!app) return { error: "After Effects not found in /Applications. Set BEQUITE_AE_PATH to the 'Adobe After Effects <ver>.app' path." };
    let aerender = process.env.BEQUITE_AERENDER_PATH || path.join(path.dirname(app), "aerender");
    if (!exists(aerender)) aerender = null;
    return { platform: "darwin", app, appName: path.basename(app).replace(/\.app$/i, ""), aerender, source };
  }
  return { error: `After Effects does not run on ${process.platform}. Use another engine (see references/engine-choice.md).` };
}

module.exports = { findAe, versionKey, listAeFolders };

if (require.main === module) {
  const r = findAe();
  console.log(JSON.stringify(r, null, 2));
  process.exit(r.error ? 2 : 0);
}
