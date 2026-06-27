import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const contentSchema = z.object({
  content: z.record(z.unknown()),
});

router.get("/api/website-content/:section", async (req: Request, res: Response) => {
  try {
    const content = await prisma.websiteContent.findUnique({ where: { section: req.params.section } });
    if (!content) {
      res.status(404).json({ success: false, error: "Section not found" });
      return;
    }
    res.json({ success: true, data: content });
  } catch (error) {
    console.error("Get website content error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.put(
  "/api/admin/website-content/:section",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = contentSchema.parse(req.body);
      const old = await prisma.websiteContent.findUnique({ where: { section: req.params.section } });

      let content;
      const jsonContent = JSON.stringify(data.content);
      if (old) {
        content = await prisma.websiteContent.update({ where: { section: req.params.section as string }, data: { content: jsonContent } });
      } else {
        content = await prisma.websiteContent.create({ data: { section: req.params.section as string, content: jsonContent } });
      }

      await logActionSync(req.user!.userId, "UPDATE", "website_content", req.params.section, old?.content as unknown as Record<string, unknown> || undefined, data.content as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: content });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update website content error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/website-content",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const sections = await prisma.websiteContent.findMany({ orderBy: { section: "asc" } });
      res.json({ success: true, data: sections });
    } catch (error) {
      console.error("List website content error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
