import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const workflowSchema = z.object({
  name: z.string().min(1),
  steps: z.array(z.record(z.unknown())),
  isActive: z.boolean().optional(),
});

router.get(
  "/api/admin/workflows",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const workflows = await prisma.workflow.findMany({ orderBy: { createdAt: "desc" } });
      res.json({ success: true, data: workflows });
    } catch (error) {
      console.error("List workflows error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/workflows",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const parsed = workflowSchema.parse(req.body);
      const workflow = await prisma.workflow.create({ data: { ...parsed, steps: JSON.stringify(parsed.steps) } });
      await logActionSync(req.user!.userId, "CREATE", "workflows", workflow.id, undefined, parsed as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: workflow });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create workflow error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/workflows/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const parsed = workflowSchema.partial().parse(req.body);
      const old = await prisma.workflow.findUnique({ where: { id: req.params.id as string } });
      if (!old) {
        res.status(404).json({ success: false, error: "Workflow not found" });
        return;
      }
      const workflow = await prisma.workflow.update({ where: { id: req.params.id as string }, data: { ...parsed, steps: JSON.stringify(parsed.steps) } });
      await logActionSync(req.user!.userId, "UPDATE", "workflows", req.params.id as string, old as unknown as Record<string, unknown>, parsed as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: workflow });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update workflow error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/workflows/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.workflow.findUnique({ where: { id: req.params.id as string } });
      if (!old) {
        res.status(404).json({ success: false, error: "Workflow not found" });
        return;
      }
      await prisma.workflow.delete({ where: { id: req.params.id as string } });
      await logActionSync(req.user!.userId, "DELETE", "workflows", req.params.id as string, old as unknown as Record<string, unknown>, undefined, req.ip);
      res.json({ success: true, data: { message: "Workflow deleted" } });
    } catch (error) {
      console.error("Delete workflow error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
