import { Hono } from "hono";
import { ProjectQuerySchema } from "../schemas.js";
import { listProjects, loadProject } from "../lib/fs-loader.js";

export const projects = new Hono();

projects.get("/", (c) => c.json({ items: listProjects() }));

projects.get("/snapshot", (c) => {
  const query = ProjectQuerySchema.safeParse({
    path: c.req.query("path") ?? undefined,
  });
  if (!query.success) {
    return c.json({ error: "invalid query", issues: query.error.issues }, 400);
  }
  const snapshot = query.data.path ? loadProject(query.data.path) : loadProject();
  return c.json(snapshot);
});
