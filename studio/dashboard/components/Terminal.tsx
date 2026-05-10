"use client";

/**
 * Terminal.tsx (v0.20.5).
 *
 * xterm.js renderer for the Studio API's /api/v1/terminal/* surface.
 *
 * Two modes:
 *   - HTTP mode: fully live. Type a command, hit Run, watch output stream
 *     into the terminal via SSE. Cancel via SIGTERM. Receipts auto-emit.
 *   - Filesystem mode: terminal renders but Run is disabled with a tooltip
 *     pointing at BEQUITE_DASHBOARD_MODE=http (the API is the executor;
 *     filesystem mode has no remote process to spawn).
 *
 * RoE per ADR-016:
 *   - Only `bequite *` and `bq *` commands are accepted (allow-list lives
 *     on the API; the dashboard surfaces the rejection cleanly).
 *   - X-BeQuite-RoE-Ack: ADR-016 sent on every exec request.
 *   - Cancel button sends SIGTERM (graceful), API auto-SIGKILLs after 5s.
 */

import { useEffect, useRef, useState, useCallback } from "react";
import type { Terminal as XTermTerminal } from "@xterm/xterm";
import {
  execCommand,
  cancelCommand,
  streamSession,
  type ExecSessionMeta,
  type StreamHandle,
} from "@/lib/terminal";
import type { DashboardMode } from "@/lib/projects-types";

interface Props {
  mode: DashboardMode;
  apiBase?: string | null;
  workspacePath?: string;
}

const PROMPT_HINT = "bequite ";

const XTERM_THEME = {
  background: "#0a0a0a",      // ink-pure
  foreground: "#e7e5e4",       // silver
  cursor: "#E5B547",           // gold-primary
  cursorAccent: "#0a0a0a",
  selectionBackground: "rgba(229, 181, 71, 0.25)",
  black: "#0a0a0a",
  brightBlack: "#3f3f46",
  red: "#ef4444",
  brightRed: "#f87171",
  green: "#22c55e",
  brightGreen: "#4ade80",
  yellow: "#E5B547",
  brightYellow: "#F2C76A",
  blue: "#3b82f6",
  brightBlue: "#60a5fa",
  magenta: "#a855f7",
  brightMagenta: "#c084fc",
  cyan: "#06b6d4",
  brightCyan: "#22d3ee",
  white: "#e7e5e4",
  brightWhite: "#fafaf9",
};

export function Terminal({ mode, apiBase, workspacePath }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const termRef = useRef<XTermTerminal | null>(null);
  const fitRef = useRef<{ fit: () => void } | null>(null);
  const streamRef = useRef<StreamHandle | null>(null);

  const [command, setCommand] = useState("bequite --version");
  const [running, setRunning] = useState(false);
  const [session, setSession] = useState<ExecSessionMeta | null>(null);
  const [error, setError] = useState<string | null>(null);

  const apiToken =
    typeof process !== "undefined"
      ? process.env.NEXT_PUBLIC_BEQUITE_API_TOKEN ?? null
      : null;

  // Initialize xterm.js on mount
  useEffect(() => {
    if (!containerRef.current) return;
    let cancelled = false;
    let resizeObserver: ResizeObserver | null = null;

    (async () => {
      const [{ Terminal }, { FitAddon }] = await Promise.all([
        import("@xterm/xterm"),
        import("@xterm/addon-fit"),
      ]);
      // The CSS for xterm's stylesheet — Next.js needs it imported via the
      // app/globals.css path; a runtime-link fallback below catches the case
      // where the operator hasn't yet wired the global.
      try {
        await import("@xterm/xterm/css/xterm.css" as unknown as string);
      } catch {
        // ignore — globals.css normally handles this
      }

      if (cancelled || !containerRef.current) return;

      const term = new Terminal({
        cursorBlink: true,
        fontFamily: '"Geist Mono", ui-monospace, SFMono-Regular, Menlo, monospace',
        fontSize: 13,
        lineHeight: 1.35,
        theme: XTERM_THEME,
        scrollback: 5000,
        convertEol: true,
        disableStdin: true, // ADR-016 §6 — no live stdin in v0.20.5
      });
      const fit = new FitAddon();
      term.loadAddon(fit);
      term.open(containerRef.current);
      fit.fit();
      term.writeln("\x1b[90mBeQuite Studio Terminal — v0.20.5 / ADR-016 RoE\x1b[0m");
      term.writeln(
        "\x1b[90mAllow-list: bequite, bq. Type a command + press Run.\x1b[0m",
      );
      term.writeln("");

      termRef.current = term;
      fitRef.current = fit;

      resizeObserver = new ResizeObserver(() => {
        try {
          fit.fit();
        } catch {
          // ignore — fit can transiently fail during layout shifts
        }
      });
      resizeObserver.observe(containerRef.current);
    })();

    return () => {
      cancelled = true;
      try {
        streamRef.current?.disconnect();
      } catch {
        // ignore
      }
      try {
        resizeObserver?.disconnect();
      } catch {
        // ignore
      }
      try {
        termRef.current?.dispose();
      } catch {
        // ignore
      }
      termRef.current = null;
      fitRef.current = null;
    };
  }, []);

  const writeLine = useCallback((channel: "stdout" | "stderr", text: string) => {
    const term = termRef.current;
    if (!term) return;
    if (channel === "stderr") {
      term.writeln(`\x1b[31m${text}\x1b[0m`);
    } else {
      term.writeln(text);
    }
  }, []);

  const writeMeta = useCallback((text: string) => {
    const term = termRef.current;
    if (!term) return;
    term.writeln(`\x1b[90m${text}\x1b[0m`);
  }, []);

  const handleRun = useCallback(async () => {
    if (mode !== "http") {
      setError("Set BEQUITE_DASHBOARD_MODE=http and start studio/api/ to run commands.");
      return;
    }
    if (!command.trim()) return;
    setError(null);
    setRunning(true);
    setSession(null);

    writeMeta("");
    writeMeta(`$ ${command}`);

    const opts = {
      apiBase: apiBase ?? undefined,
      apiToken,
    };
    const res = await execCommand(
      {
        command,
        cwd: workspacePath,
      },
      opts,
    );

    if (!res.ok || !res.session.session_id) {
      writeLine("stderr", `[exec rejected] ${res.error ?? "unknown error"}`);
      setError(res.error ?? "exec rejected");
      setRunning(false);
      return;
    }

    setSession(res.session);

    streamRef.current = streamSession(
      res.session.session_id,
      {
        onHello: (meta) => {
          writeMeta(
            `[session ${meta.session.session_id} pid=${meta.session.pid ?? "?"} replayed=${meta.replayed_lines}]`,
          );
        },
        onLine: (line) => {
          writeLine(line.channel, line.text);
        },
        onExit: (s) => {
          setSession(s);
          setRunning(false);
          const tag =
            s.exit_reason === "clean"
              ? `\x1b[32m[exit ${s.exit_code} · ${s.duration_ms}ms]\x1b[0m`
              : `\x1b[33m[exit ${s.exit_code ?? "n/a"} · ${s.exit_reason} · ${s.duration_ms ?? 0}ms]\x1b[0m`;
          const term = termRef.current;
          if (term) term.writeln(tag);
          if (s.output_truncated) {
            writeMeta("[output buffer was truncated to 10MB cap — ADR-016 §5]");
          }
        },
        onError: (err) => {
          writeLine("stderr", `[stream error] ${String(err instanceof Error ? err.message : "transport")}`);
        },
      },
      opts,
    );
  }, [command, mode, apiBase, apiToken, workspacePath, writeLine, writeMeta]);

  const handleCancel = useCallback(async () => {
    const id = session?.session_id;
    if (!id) return;
    await cancelCommand(id, { apiBase: apiBase ?? undefined, apiToken });
    writeMeta("[cancel requested — SIGTERM sent; SIGKILL after 5s if needed]");
  }, [session, apiBase, apiToken, writeMeta]);

  const handleClear = useCallback(() => {
    termRef.current?.clear();
  }, []);

  const httpDisabled = mode !== "http";

  return (
    <div className="flex h-full flex-col rounded border border-ink-edge bg-ink-pure">
      {/* Toolbar */}
      <div className="flex items-center gap-2 border-b border-ink-edge bg-ink-stage px-3 py-2">
        <span className="font-mono text-[10px] uppercase tracking-wider text-gold-bright">
          ▸
        </span>
        <input
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !running) {
              e.preventDefault();
              handleRun();
            }
          }}
          placeholder={PROMPT_HINT + "<subcommand>"}
          disabled={httpDisabled || running}
          spellCheck={false}
          className="flex-1 bg-transparent font-mono text-xs text-silver outline-none placeholder:text-silver-dim disabled:opacity-50"
        />
        {running ? (
          <button
            onClick={handleCancel}
            className="rounded border border-red-600/40 bg-red-950/40 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-red-300 hover:bg-red-900/60"
          >
            Cancel
          </button>
        ) : (
          <button
            onClick={handleRun}
            disabled={httpDisabled}
            title={
              httpDisabled
                ? "Set BEQUITE_DASHBOARD_MODE=http and start studio/api/"
                : "Run · ADR-016 RoE"
            }
            className="rounded border border-gold-deep bg-gold-deep/20 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-gold-bright hover:bg-gold-deep/40 disabled:cursor-not-allowed disabled:border-ink-edge disabled:bg-transparent disabled:text-silver-dim"
          >
            Run
          </button>
        )}
        <button
          onClick={handleClear}
          className="rounded border border-ink-edge px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-silver-dim hover:text-silver"
        >
          Clear
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <div className="border-b border-red-900/40 bg-red-950/30 px-3 py-1 font-mono text-[10px] text-red-300">
          {error}
        </div>
      )}

      {/* xterm.js mount point */}
      <div ref={containerRef} className="min-h-0 flex-1 overflow-hidden p-2" />

      {/* Footer status */}
      <div className="flex items-center justify-between border-t border-ink-edge bg-ink-stage px-3 py-1 font-mono text-[10px] text-silver-dim">
        <span>
          {session
            ? `session: ${session.session_id} · ${session.exit_reason}`
            : "session: (none)"}
        </span>
        <span>
          ADR-016 · allow-list: bequite, bq · stdin disabled in v0.20.5
        </span>
      </div>
    </div>
  );
}
