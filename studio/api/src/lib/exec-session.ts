/**
 * Exec session manager (v0.20.5; per ADR-016 §5–§7).
 *
 * Owns one ChildProcess per session. Captures stdout + stderr to a 10MB
 * ring buffer. Fans output to subscribers (SSE consumers) line-by-line.
 *
 * On session end:
 *   - sets exit_code, exit_reason, ended_at_utc
 *   - computes stdout_sha256 / stderr_sha256 over the full captured output
 *     (or the truncated tail, with output_truncated: true)
 *   - emits a final "exit" SSE event
 *   - leaves the session in memory for 5 minutes (so late-joiners can
 *     replay output) then garbage-collects
 *
 * Cancel = SIGTERM, then SIGKILL after 5 seconds. Timeout = same flow.
 */

import { spawn, type ChildProcess } from "node:child_process";
import crypto from "node:crypto";
import path from "node:path";

const RING_BYTES_MAX = 10 * 1024 * 1024; // 10MB
const SESSION_GC_AFTER_EXIT_MS = 5 * 60 * 1000; // 5 minutes
const KILL_GRACE_MS = 5_000;
const DEFAULT_TIMEOUT_S = 1800;
const MAX_TIMEOUT_S = 21_600;

export type ExitReason =
  | "running"
  | "clean"
  | "timeout"
  | "cancelled"
  | "error"
  | "killed";

export interface ExecLine {
  channel: "stdout" | "stderr";
  text: string;
  ts: string; // ISO 8601
}

export interface ExecSession {
  session_id: string;
  binary: string;
  args: string[];
  cwd: string;
  identity: string | null;
  started_at_utc: string;
  ended_at_utc: string | null;
  exit_code: number | null;
  exit_reason: ExitReason;
  duration_ms: number | null;
  output_truncated: boolean;
  stdout_sha256: string | null;
  stderr_sha256: string | null;
  pid: number | null;
}

interface InternalSession extends ExecSession {
  child: ChildProcess | null;
  ringBuffer: ExecLine[];
  ringBytes: number;
  totalStdoutBytes: number;
  totalStderrBytes: number;
  stdoutHash: crypto.Hash;
  stderrHash: crypto.Hash;
  subscribers: Set<(line: ExecLine | { type: "exit"; session: ExecSession }) => void>;
  killTimer: NodeJS.Timeout | null;
  timeoutTimer: NodeJS.Timeout | null;
  gcTimer: NodeJS.Timeout | null;
}

const sessions: Map<string, InternalSession> = new Map();

export function listSessions(): ExecSession[] {
  return Array.from(sessions.values()).map((s) => publicShape(s));
}

export function getSession(id: string): ExecSession | null {
  const s = sessions.get(id);
  return s ? publicShape(s) : null;
}

export function getRingBuffer(id: string): ExecLine[] {
  const s = sessions.get(id);
  return s ? [...s.ringBuffer] : [];
}

export interface StartOptions {
  binary: string;
  args: string[];
  cwd: string;
  identity: string | null;
  timeoutSeconds?: number;
  stdin?: string;
  env?: Record<string, string>;
}

export interface StartResult {
  session: ExecSession;
  pid: number | null;
}

export function startSession(opts: StartOptions): StartResult {
  const session_id = `exec-${crypto.randomUUID()}`;
  const started_at_utc = new Date().toISOString();
  const timeoutSeconds = Math.min(
    Math.max(opts.timeoutSeconds ?? DEFAULT_TIMEOUT_S, 1),
    MAX_TIMEOUT_S,
  );

  let child: ChildProcess | null = null;
  let spawnError: string | null = null;
  try {
    child = spawn(opts.binary, opts.args, {
      cwd: opts.cwd,
      shell: false, // ADR-016 §2 — never shell:true
      env: { ...process.env, ...(opts.env ?? {}) },
      windowsHide: true,
    });
  } catch (e) {
    spawnError = String(e);
  }

  const internal: InternalSession = {
    session_id,
    binary: opts.binary,
    args: opts.args,
    cwd: path.resolve(opts.cwd),
    identity: opts.identity,
    started_at_utc,
    ended_at_utc: null,
    exit_code: null,
    exit_reason: "running",
    duration_ms: null,
    output_truncated: false,
    stdout_sha256: null,
    stderr_sha256: null,
    pid: child?.pid ?? null,
    child,
    ringBuffer: [],
    ringBytes: 0,
    totalStdoutBytes: 0,
    totalStderrBytes: 0,
    stdoutHash: crypto.createHash("sha256"),
    stderrHash: crypto.createHash("sha256"),
    subscribers: new Set(),
    killTimer: null,
    timeoutTimer: null,
    gcTimer: null,
  };

  sessions.set(session_id, internal);

  if (spawnError) {
    finishSession(internal, "error", null, spawnError);
    return { session: publicShape(internal), pid: null };
  }
  if (!child) {
    finishSession(internal, "error", null, "spawn returned null without throwing");
    return { session: publicShape(internal), pid: null };
  }

  // Stdin (one-shot at spawn; no live forwarding per ADR-016 §6)
  if (opts.stdin && child.stdin) {
    try {
      child.stdin.write(opts.stdin);
    } catch {
      // ignore
    }
    try {
      child.stdin.end();
    } catch {
      // ignore
    }
  }

  // Stdout / stderr capture
  bindOutput(internal, child, "stdout");
  bindOutput(internal, child, "stderr");

  child.on("error", (err) => {
    if (internal.ended_at_utc) return;
    finishSession(internal, "error", null, String(err));
  });

  child.on("exit", (code, signal) => {
    if (internal.ended_at_utc) return;
    let reason: ExitReason = "clean";
    if (signal === "SIGTERM" || signal === "SIGKILL") {
      // Could be cancel or timeout — caller may have already set the reason.
      reason = internal.exit_reason === "running" ? "killed" : internal.exit_reason;
    } else if (code !== 0) {
      reason = "clean"; // non-zero exit is a "clean exit with non-zero code", not an error in the spawn sense
    }
    finishSession(internal, reason, code, null);
  });

  // Timeout
  internal.timeoutTimer = setTimeout(() => {
    if (internal.ended_at_utc) return;
    internal.exit_reason = "timeout";
    sendSignal(internal, "SIGTERM");
    internal.killTimer = setTimeout(() => {
      sendSignal(internal, "SIGKILL");
    }, KILL_GRACE_MS);
  }, timeoutSeconds * 1000);

  return { session: publicShape(internal), pid: child.pid ?? null };
}

export function cancelSession(id: string): boolean {
  const s = sessions.get(id);
  if (!s || s.ended_at_utc) return false;
  s.exit_reason = "cancelled";
  sendSignal(s, "SIGTERM");
  s.killTimer = setTimeout(() => {
    sendSignal(s, "SIGKILL");
  }, KILL_GRACE_MS);
  return true;
}

export function subscribe(
  id: string,
  cb: (event: ExecLine | { type: "exit"; session: ExecSession }) => void,
): () => void {
  const s = sessions.get(id);
  if (!s) return () => {};
  s.subscribers.add(cb);
  return () => {
    s.subscribers.delete(cb);
  };
}

// ----- internals --------------------------------------------------------

function publicShape(s: InternalSession): ExecSession {
  const {
    child: _child,
    ringBuffer: _ringBuffer,
    ringBytes: _ringBytes,
    totalStdoutBytes: _ts,
    totalStderrBytes: _te,
    stdoutHash: _sh,
    stderrHash: _eh,
    subscribers: _sub,
    killTimer: _kt,
    timeoutTimer: _tt,
    gcTimer: _gt,
    ...rest
  } = s;
  return { ...rest };
}

function bindOutput(
  internal: InternalSession,
  child: ChildProcess,
  channel: "stdout" | "stderr",
): void {
  const stream = channel === "stdout" ? child.stdout : child.stderr;
  if (!stream) return;
  let leftover = "";
  stream.setEncoding("utf8");
  stream.on("data", (chunk: string) => {
    if (channel === "stdout") {
      internal.totalStdoutBytes += Buffer.byteLength(chunk, "utf8");
      internal.stdoutHash.update(chunk);
    } else {
      internal.totalStderrBytes += Buffer.byteLength(chunk, "utf8");
      internal.stderrHash.update(chunk);
    }
    const combined = leftover + chunk;
    const lines = combined.split(/\r?\n/);
    leftover = lines.pop() ?? "";
    for (const line of lines) {
      pushLine(internal, channel, line);
    }
  });
  stream.on("end", () => {
    if (leftover) {
      pushLine(internal, channel, leftover);
      leftover = "";
    }
  });
}

function pushLine(
  internal: InternalSession,
  channel: "stdout" | "stderr",
  text: string,
): void {
  const line: ExecLine = { channel, text, ts: new Date().toISOString() };
  const lineBytes = Buffer.byteLength(text, "utf8") + 24; // rough overhead
  // Ring eviction
  while (
    internal.ringBuffer.length > 0 &&
    internal.ringBytes + lineBytes > RING_BYTES_MAX
  ) {
    const dropped = internal.ringBuffer.shift();
    if (dropped) {
      internal.ringBytes -= Buffer.byteLength(dropped.text, "utf8") + 24;
      internal.output_truncated = true;
    }
  }
  internal.ringBuffer.push(line);
  internal.ringBytes += lineBytes;
  for (const cb of internal.subscribers) {
    try {
      cb(line);
    } catch {
      // ignore — a subscriber that throws shouldn't break the session
    }
  }
}

function sendSignal(s: InternalSession, sig: NodeJS.Signals): void {
  if (!s.child || s.child.killed) return;
  try {
    s.child.kill(sig);
  } catch {
    // ignore — process may have already exited between our check and kill
  }
}

function finishSession(
  s: InternalSession,
  reason: ExitReason,
  exitCode: number | null,
  errorDetail: string | null,
): void {
  if (s.ended_at_utc) return;
  s.ended_at_utc = new Date().toISOString();
  s.exit_code = exitCode;
  // If reason was already set by cancel/timeout, keep it; otherwise use provided
  if (s.exit_reason === "running") {
    s.exit_reason = reason;
  }
  s.duration_ms =
    new Date(s.ended_at_utc).getTime() - new Date(s.started_at_utc).getTime();
  s.stdout_sha256 = s.stdoutHash.digest("hex");
  s.stderr_sha256 = s.stderrHash.digest("hex");
  if (s.timeoutTimer) {
    clearTimeout(s.timeoutTimer);
    s.timeoutTimer = null;
  }
  if (s.killTimer) {
    clearTimeout(s.killTimer);
    s.killTimer = null;
  }
  // Inject error detail as a final stderr line so subscribers see it.
  if (errorDetail) {
    pushLine(s, "stderr", `[exec error] ${errorDetail}`);
  }
  // Notify subscribers of exit, then clear them.
  const exitEvent = { type: "exit" as const, session: publicShape(s) };
  for (const cb of s.subscribers) {
    try {
      cb(exitEvent);
    } catch {
      // ignore
    }
  }
  s.subscribers.clear();
  // GC after grace period
  s.gcTimer = setTimeout(() => {
    sessions.delete(s.session_id);
  }, SESSION_GC_AFTER_EXIT_MS);
}
