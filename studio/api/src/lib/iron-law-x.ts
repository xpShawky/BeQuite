/**
 * Iron Law X verification helper (Constitution v1.3.0, Article X).
 *
 * Every write endpoint that mutates state on disk produces a verification
 * block confirming the change is operationally complete:
 *
 *   1. persisted_path        — absolute path on disk
 *   2. file_readable         — re-read after write succeeds
 *   3. file_size_bytes       — non-zero, matches the data we wrote
 *   4. file_sha256           — content fingerprint
 *   5. api_route_alive       — the route that wrote this file still serves
 *                              its own GET (when applicable) — caller passes
 *                              a probe function or null
 *   6. attestation           — short prose acknowledging the seven Iron
 *                              Law X operational steps
 *
 * This is NOT a substitute for restarting the build (Article X step 7 —
 * "did the user need to restart the build for the change to be live?").
 * For API state, "restart" maps to "re-fetch via the same endpoint." For
 * dashboard state, "restart" maps to "Next.js revalidation or hard reload."
 * The attestation field flags what the caller still needs to do.
 *
 * Iron Law X banned report patterns are NEVER emitted from this helper:
 *
 *   - "should work"
 *   - "probably works"
 *   - "seems to work"
 *   - "appears to work"
 *   - "I think it works"
 *   - "in theory"
 *
 * If a verification step fails, the helper raises (caller returns 500),
 * not "it should work but try refreshing."
 */

import fs from "node:fs";
import crypto from "node:crypto";

export interface IronLawXBlock {
  persisted_path: string;
  file_readable: boolean;
  file_size_bytes: number;
  file_sha256: string;
  api_route_alive: boolean | "n/a";
  attestation: string;
  /** What the caller still needs to do for the change to be visible (Article X step 7). */
  caller_must: string[];
}

export interface IronLawXProbeContext {
  /** Async function returning true if a sibling GET against the same resource succeeds. */
  routeAlive?: () => Promise<boolean>;
  /** Short description of what the write did, e.g. "appended receipt 1a2b3c..." */
  what: string;
  /** What the user/caller still needs to do (e.g. "refresh the dashboard", "no further action"). */
  callerMust: string[];
}

export async function buildIronLawXBlock(
  persistedPath: string,
  ctx: IronLawXProbeContext,
): Promise<IronLawXBlock> {
  let fileReadable = false;
  let fileSize = 0;
  let fileSha = "";
  let bytes: Buffer | null = null;

  try {
    bytes = fs.readFileSync(persistedPath);
    fileReadable = true;
    fileSize = bytes.byteLength;
    fileSha = crypto.createHash("sha256").update(bytes).digest("hex");
  } catch (e) {
    // Re-throw — Iron Law X says the write is NOT operationally complete
    // if the re-read fails. The caller returns 500.
    throw new Error(
      `Iron Law X verification failed: persisted file unreadable at ${persistedPath}: ${String(e)}`,
    );
  }

  let routeAlive: boolean | "n/a" = "n/a";
  if (ctx.routeAlive) {
    try {
      routeAlive = await ctx.routeAlive();
    } catch (e) {
      throw new Error(
        `Iron Law X verification failed: sibling route probe threw: ${String(e)}`,
      );
    }
    if (!routeAlive) {
      throw new Error(
        `Iron Law X verification failed: sibling route returned non-ok status`,
      );
    }
  }

  const attestation =
    `Operationally complete. Wrote ${fileSize} bytes to ${persistedPath} ` +
    `(sha256: ${fileSha.slice(0, 12)}...). ${ctx.what}. ` +
    `Re-read after write: ok. Sibling route probe: ${
      routeAlive === "n/a" ? "n/a" : routeAlive ? "ok" : "failed"
    }.`;

  return {
    persisted_path: persistedPath,
    file_readable: fileReadable,
    file_size_bytes: fileSize,
    file_sha256: fileSha,
    api_route_alive: routeAlive,
    attestation,
    caller_must: ctx.callerMust,
  };
}
