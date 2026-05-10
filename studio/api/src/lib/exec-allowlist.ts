/**
 * Hardcoded execution allow-list (v0.20.5; per ADR-016 §1).
 *
 * THIS LIST IS DELIBERATELY HARDCODED. There is no env override, no config
 * flag, no runtime mutation. Widening the list requires a code change + an
 * ADR amendment. Article IV (Security & destruction discipline) + Article X
 * (Operational completeness) demand this — auth controls *who* can call the
 * endpoint; this list controls *what* they can run. Defense-in-depth: a
 * stolen token shouldn't be able to `rm -rf`.
 *
 * Add an entry by:
 *   1. Authoring an ADR amendment to ADR-016 documenting the addition.
 *   2. Editing this file.
 *   3. Restarting the API.
 *
 * Operators who fork BeQuite to widen the list should record their fork's
 * allow-list in their fork's CHANGELOG so the audit trail stays clear.
 */

export interface AllowEntry {
  binary: string;
  description: string;
  /** null = any subcommand allowed. Array = only these subcommands allowed. */
  allowed_subcommands: string[] | null;
  note: string;
}

export const DEFAULT_ALLOWLIST: ReadonlyArray<AllowEntry> = Object.freeze([
  Object.freeze({
    binary: "bequite",
    description: "BeQuite CLI",
    allowed_subcommands: null,
    note: "Per ADR-016 §1. No shell, no piping, no redirects.",
  }),
  Object.freeze({
    binary: "bq",
    description: "BeQuite CLI shorthand",
    allowed_subcommands: null,
    note: "Alias of bequite; same RoE.",
  }),
]);

export interface AllowCheck {
  ok: boolean;
  reason?: string;
  entry?: AllowEntry;
}

/**
 * Whitespace-splitter used by exec parsing. INTENTIONALLY does not handle
 * shell quoting — if you need quotes, fork the allow-list. The exec endpoint
 * passes args as an array to spawn(... { shell: false }) so quoting wouldn't
 * make sense anyway.
 *
 * Strips leading/trailing whitespace; collapses runs to single spaces; never
 * preserves spaces-inside-quotes (because YAGNI; shell:false won't see them).
 */
export function parseCommandLine(input: string): { binary: string; args: string[] } {
  const tokens = input.trim().split(/\s+/u).filter(Boolean);
  if (tokens.length === 0) {
    return { binary: "", args: [] };
  }
  const [binary, ...args] = tokens;
  return { binary: binary!, args };
}

export function checkAllowed(
  binary: string,
  args: string[],
  allowlist: ReadonlyArray<AllowEntry> = DEFAULT_ALLOWLIST,
): AllowCheck {
  if (!binary) {
    return { ok: false, reason: "empty binary" };
  }
  // Reject any binary path containing a path separator — must be looked up
  // via PATH (forces the operator to install the binary properly + can't run
  // /tmp/evil-binary by spelling its path).
  if (binary.includes("/") || binary.includes("\\")) {
    return {
      ok: false,
      reason: "binary must be a bare name on PATH (no path separators allowed)",
    };
  }

  const entry = allowlist.find((e) => e.binary === binary);
  if (!entry) {
    return {
      ok: false,
      reason: `binary "${binary}" not on allow-list`,
    };
  }

  if (entry.allowed_subcommands !== null) {
    const sub = args[0];
    if (!sub || !entry.allowed_subcommands.includes(sub)) {
      return {
        ok: false,
        reason: `subcommand "${sub ?? "(none)"}" not in allowed_subcommands for ${binary}`,
        entry,
      };
    }
  }

  return { ok: true, entry };
}
