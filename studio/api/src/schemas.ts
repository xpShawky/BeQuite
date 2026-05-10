import { z } from "zod";

export const PhaseStatusSchema = z.object({
  id: z.string(),
  name: z.string(),
  status: z.enum(["done", "in_progress", "pending", "blocked"]),
});

export const ReceiptSummarySchema = z.object({
  filename: z.string(),
  phase: z.string(),
  timestamp_utc: z.string(),
  model: z.string(),
  cost_usd: z.number(),
  signed: z.boolean(),
});

export const ProjectSnapshotSchema = z.object({
  root: z.string(),
  exists: z.boolean(),
  projectName: z.string(),
  doctrineList: z.array(z.string()),
  constitutionVersion: z.string(),
  currentPhase: z.string(),
  lastGreenTag: z.string().nullable(),
  activeContextSummary: z.string(),
  phases: z.array(PhaseStatusSchema),
  recentReceipts: z.array(ReceiptSummarySchema),
  costSession: z
    .object({
      usd: z.number(),
      tokens: z.number(),
      calls: z.number(),
    })
    .nullable(),
  recoveryPreview: z.string(),
});

export type PhaseStatus = z.infer<typeof PhaseStatusSchema>;
export type ReceiptSummary = z.infer<typeof ReceiptSummarySchema>;
export type ProjectSnapshot = z.infer<typeof ProjectSnapshotSchema>;

export const ProjectQuerySchema = z.object({
  path: z.string().optional(),
});
