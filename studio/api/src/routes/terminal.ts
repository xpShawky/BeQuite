/**
 * Terminal exec routes (v0.20.5; per ADR-016).
 *
 * POST   /api/v1/terminal/exec                 — start a command (X-BeQuite-RoE-Ack required)
 * GET    /api/v1/terminal/sessions             — list sessions
 * GET    /api/v1/terminal/sessions/:id         — session status
 * GET    /api/v1/terminal/sessions/:id/stream  — SSE stream of output + exit
 * POST   /api/v1/terminal/sessions/:id/cancel  — SIGTERM (then SIGKILL after 5s)
 *
 * SAFETY: every commit on this surface should re-read ADR-016 first. The
 * RoE is the rule-set; this file is the enforcement.
 */

import { Hono } from "hono";
import { streamSSE } from "hono/streaming";
import path from "node:path";
import fs from "node:fs";
import crypto from "node:crypto";
import { z } from "zod";
import { getWorkspaceRoot } from "../lib/fs-loader.js";
import { getAuth } from "../lib/auth.js";
import { buildIronLawXBlock } from "../lib/iron-law-x.js";
import {
  parseCommandLine,
  checkAllowed,
  DEFAULT_ALLOWLIST,
} from "../lib/exec-allowlist.js";
import {
  startSession,
  cancelSession,
  getSession,
  getRingBuffer,
  listSessions,
  subscribe as subscribeSession,
} from "../lib/exec-session.js";

export const terminal = new Hono();

const ROE_HEADER = "x-bequite-roe-ack";
const ROE_VALUE = "ADR-016";
const HEARTBEAT_MS = 30_000;

function projectCwd(c: import("hono").Context, requested?: string): {
  cwd: string;
  error?: string;
} {
  const queryPath = requested ?? c.req.query("path") ?? getWorkspaceRoot();
  const cwd = path.resolve(queryPath);
  if (!cwd.startsWith(getWorkspaceRoot())) {
    return { cwd, error: "cwd outside workspace root" };
  }
  if (!fs.existsSync(cwd)) {
    return { cwd, error: `cwd does not exist: ${cwd}` };
  }
  return { cwd };
}

const ExecBodySchema = z.object({
  command: z.string().min(1).max(2048),
  cwd: z.string().optional(),
  timeout_seconds: z.number().int().positive().max(21_600).optional(),
  stdin: z.string().max(64 * 1024).optional(),
});

terminal.post("/exec", async (c) => {
  const auth = getAuth(c);

  // ADR-016 §11 — RoE acknowledgment header
  const roe = c.req.header(ROE_HEADER) || c.req.header(ROE_HEADER.toUpperCase());
  if (roe !== ROE_VALUE) {
    return c.json(
      {
        error: "missing or invalid X-BeQuite-RoE-Ack header — see ADR-016 §11",
        expected: ROE_VALUE,
        received: roe ?? null,
        adr: "ADR-016",
      },
      412,
    );
  }

  let body: unknown;
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: "body must be JSON" }, 400);
  }
  const parsed = ExecBodySchema.safeParse(body);
  if (!parsed.success) {
    return c.json(
      { error: "invalid exec request", issues: parsed.error.issues },
      400,
    );
  }

  // Parse + allow-list check
  const { binary, args } = parseCommandLine(parsed.data.command);
  const check = checkAllowed(binary, args, DEFAULT_ALLOWLIST);
  if (!check.ok) {
    return c.json(
      {
        error: "command not on allow-list",
        binary,
        reason: check.reason,
        adr: "ADR-016 §1",
        allowed_binaries: DEFAULT_ALLOWLIST.map((e) => e.binary),
      },
      403,
    );
  }

  // Cwd guard
  const cwdCheck = projectCwd(c, parsed.data.cwd);
  if (cwdCheck.error) {
    return c.json({ error: cwdCheck.error, adr: "ADR-016 §3" }, 403);
  }

  // Spawn
  const start = startSession({
    binary,
    args,
    cwd: cwdCheck.cwd,
    identity: auth.identity,
    timeoutSeconds: parsed.data.timeout_seconds,
    stdin: parsed.data.stdin,
  });

  // Iron Law X attestation — was the spawn live at response time?
  if (start.session.exit_reason === "error" || start.pid === null) {
    return c.json(
      {
        ok: false,
        session: start.session,
        error: "spawn failed",
      },
      500,
    );
  }

  // Per-execution receipt (ADR-016 §8)
  let receiptPath: string | null = null;
  try {
    receiptPath = writeExecReceipt(cwdCheck.cwd, start.session, auth.identity);
  } catch (e) {
    // Receipt failed — return 500 so the operator sees the issue immediately.
    cancelSession(start.session.session_id);
    return c.json(
      {
        ok: false,
        error: `Iron Law X violation: per-exec receipt write failed — ${String(e)}`,
        session: start.session,
      },
      500,
    );
  }

  const ironLawX = await buildIronLawXBlock(receiptPath, {
    what: `started exec session ${start.session.session_id} (pid ${start.pid}) running ${binary} ${args.join(" ")}`,
    routeAlive: async () => {
      // Probe: session still tracked + child not exited yet
      const live = getSession(start.session.session_id);
      return !!live && live.exit_reason === "running";
    },
    callerMust: [
      `GET /api/v1/terminal/sessions/${start.session.session_id}/stream to receive live output via SSE`,
      `POST /api/v1/terminal/sessions/${start.session.session_id}/cancel to stop the command`,
      "no service restart required — the session is live in this API process and the spawned child is running",
    ],
  });

  return c.json(
    {
      ok: true,
      session: start.session,
      receipt_path: receiptPath,
      iron_law_x: ironLawX,
    },
    201,
  );
});

terminal.get("/sessions", (c) => {
  return c.json({ items: listSessions() });
});

terminal.get("/sessions/:id", (c) => {
  const s = getSession(c.req.param("id"));
  if (!s) return c.json({ error: "session not found" }, 404);
  return c.json(s);
});

terminal.post("/sessions/:id/cancel", (c) => {
  const id = c.req.param("id");
  const s = getSession(id);
  if (!s) return c.json({ error: "session not found" }, 404);
  if (s.ended_at_utc) {
    return c.json({ ok: false, reason: "session already ended", session: s }, 409);
  }
  const cancelled = cancelSession(id);
  return c.json({ ok: cancelled, session: getSession(id) });
});

terminal.get("/sessions/:id/stream", (c) => {
  const id = c.req.param("id");
  const s = getSession(id);
  if (!s) return c.json({ error: "session not found" }, 404);

  return streamSSE(c, async (stream) => {
    // Hello + replay of any output already in the ring
    await stream.writeSSE({
      event: "hello",
      data: JSON.stringify({
        session: s,
        replayed_lines: getRingBuffer(id).length,
      }),
    });
    for (const line of getRingBuffer(id)) {
      await stream.writeSSE({
        event: "line",
        data: JSON.stringify(line),
      });
    }

    // If session already exited before subscribe arrived, emit the exit then close
    if (s.ended_at_utc) {
      await stream.writeSSE({
        event: "exit",
        data: JSON.stringify({ session: s }),
      });
      return;
    }

    // Live subscription
    let resolveDone: () => void = () => {};
    const done = new Promise<void>((resolve) => {
      resolveDone = resolve;
    });
    const unsubscribe = subscribeSession(id, async (event) => {
      try {
        if ("type" in event && event.type === "exit") {
          await stream.writeSSE({
            event: "exit",
            data: JSON.stringify({ session: event.session }),
          });
          resolveDone();
          return;
        }
        await stream.writeSSE({
          event: "line",
          data: JSON.stringify(event),
        });
      } catch {
        // Client disconnected — teardown handled below
      }
    });

    // Heartbeat
    const heartbeat = setInterval(async () => {
      try {
        await stream.writeSSE({
          event: "heartbeat",
          data: JSON.stringify({ ts: new Date().toISOString() }),
        });
      } catch {
        // ignore
      }
    }, HEARTBEAT_MS);

    stream.onAbort(() => {
      clearInterval(heartbeat);
      unsubscribe();
      resolveDone();
    });

    await done;
    clearInterval(heartbeat);
    unsubscribe();
  });
});

// ----- per-exec receipt writer -----------------------------------------

function writeExecReceipt(
  workspace: string,
  session: { session_id: string; binary: string; args: string[]; started_at_utc: string },
  identity: string | null,
): string {
  const dir = path.join(workspace, ".bequite", "receipts");
  fs.mkdirSync(dir, { recursive: true });

  const payload = {
    version: "1",
    session_id: session.session_id,
    phase: "EXEC",
    timestamp_utc: session.started_at_utc,
    model: { name: "n/a-exec", reasoning_effort: "n/a", fallback_model: null },
    input: {
      prompt_hash: crypto.createHash("sha256").update("exec").digest("hex"),
      memory_snapshot_hash: crypto.createHash("sha256").update("exec").digest("hex"),
    },
    output: {
      diff_hash: crypto.createHash("sha256").update("").digest("hex"),
      files_touched: [] as string[],
    },
    tools_invoked: [
      {
        name: "exec",
        binary: session.binary,
        args: session.args,
        cwd: workspace,
      },
    ],
    cost: { input_tokens: 0, output_tokens: 0, usd: 0 },
    doctrine: [],
    constitution_version: "1.3.0",
    parent_receipt: null,
    exec: {
      binary: session.binary,
      args: session.args,
      cwd: workspace,
      session_id: session.session_id,
      started_at_utc: session.started_at_utc,
      ended_at_utc: null,
      exit_code: null,
      exit_reason: "running",
      duration_ms: null,
      stdout_sha256: null,
      stderr_sha256: null,
      output_truncated: false,
    },
    identity: identity ?? "local-dev",
    adr: "ADR-016",
  };

  const sha = crypto
    .createHash("sha256")
    .update(JSON.stringify(payload))
    .digest("hex");
  const filename = `${sha}-EXEC.json`;
  const filepath = path.join(dir, filename);
  fs.writeFileSync(filepath, JSON.stringify(payload, null, 2), "utf8");
  return filepath;
}
