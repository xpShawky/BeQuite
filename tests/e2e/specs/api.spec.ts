import { test, expect } from "@playwright/test";

/**
 * API smoke (http://localhost:3002).
 * Doubles as the Phase 4 API_AUDIT verification.
 */

test.use({ baseURL: "http://localhost:3002" });

test.describe("api / public surface", () => {
  test("GET / returns metadata + endpoint catalog", async ({ request }) => {
    const res = await request.get("/");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.name).toBe("BeQuite Studio API");
    expect(body.endpoints).toBeDefined();
    expect(body.endpoints.public).toContain("GET /healthz");
  });

  test("GET /healthz returns ok", async ({ request }) => {
    const res = await request.get("/healthz");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body.status).toBe("ok");
    expect(body.service).toBe("bequite-api");
    expect(typeof body.uptime_s).toBe("number");
  });

  test("GET /api/v1/auth/status returns mode info", async ({ request }) => {
    const res = await request.get("/api/v1/auth/status");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(["local-dev", "token", "device-code"]).toContain(body.mode);
  });

  test("GET /api/v1/projects returns items array", async ({ request }) => {
    const res = await request.get("/api/v1/projects");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body.items)).toBe(true);
  });

  test("GET /api/v1/projects/snapshot returns ProjectSnapshot shape", async ({ request }) => {
    const res = await request.get("/api/v1/projects/snapshot");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body).toHaveProperty("root");
    expect(body).toHaveProperty("exists");
    expect(body).toHaveProperty("projectName");
    expect(body).toHaveProperty("phases");
    expect(body).toHaveProperty("constitutionVersion");
    expect(Array.isArray(body.phases)).toBe(true);
  });

  test("GET /api/v1/receipts returns items array", async ({ request }) => {
    const res = await request.get("/api/v1/receipts");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body.items)).toBe(true);
  });

  test("GET /api/v1/receipts/INVALID-SHA returns 400", async ({ request }) => {
    const res = await request.get("/api/v1/receipts/not-a-valid-sha-because-too-short");
    // Either 400 (validation error) or 404 (no matching receipt)
    expect([400, 404]).toContain(res.status());
  });

  test("GET /nonexistent returns 404", async ({ request }) => {
    const res = await request.get("/nonexistent");
    expect(res.status()).toBe(404);
    const body = await res.json();
    expect(body.error).toBe("not found");
  });

  test("CORS preflight from dashboard origin", async ({ request }) => {
    const res = await request.fetch("/api/v1/projects", {
      method: "OPTIONS",
      headers: {
        "Origin": "http://localhost:3001",
        "Access-Control-Request-Method": "GET",
      },
    });
    // Hono CORS responds with 204 No Content for OPTIONS preflight.
    expect([200, 204]).toContain(res.status());
    expect(res.headers()["access-control-allow-origin"]).toBe("http://localhost:3001");
  });

  test("POST /api/v1/terminal/exec without RoE-Ack header returns 412", async ({ request }) => {
    const res = await request.post("/api/v1/terminal/exec", {
      data: { command: "bequite --version" },
    });
    expect(res.status()).toBe(412);
    const body = await res.json();
    expect(body.error).toContain("X-BeQuite-RoE-Ack");
  });

  test("POST /api/v1/terminal/exec rejects disallowed binary", async ({ request }) => {
    const res = await request.post("/api/v1/terminal/exec", {
      headers: {
        "X-BeQuite-RoE-Ack": "ADR-016",
        "Content-Type": "application/json",
      },
      data: { command: "rm -rf /" },
    });
    expect(res.status()).toBe(403);
    const body = await res.json();
    expect(body.error).toBe("command not on allow-list");
  });
});
