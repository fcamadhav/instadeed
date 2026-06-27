import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const aiSettingsSchema = z.object({
  provider: z.string().optional(),
  model: z.string().optional(),
  apiKey: z.string().optional(),
  temperature: z.number().min(0).max(2).optional(),
  maxTokens: z.number().int().positive().optional(),
  systemPrompt: z.string().optional(),
  retryCount: z.number().int().min(0).optional(),
  fallbackModel: z.string().optional(),
  isEnabled: z.boolean().optional(),
});

const ocrSettingsSchema = z.object({
  provider: z.string().optional(),
  apiKey: z.string().optional(),
  isEnabled: z.boolean().optional(),
});

const ocrDocumentSchema = z.object({
  name: z.string().min(1),
  fields: z.record(z.unknown()).optional(),
  isActive: z.boolean().optional(),
});

router.get(
  "/api/admin/ai-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      let settings = await prisma.aiSetting.findFirst();
      if (!settings) {
        settings = await prisma.aiSetting.create({ data: {} });
      }
      res.json({ success: true, data: { ...settings, apiKey: settings.apiKey ? "[ENCRYPTED]" : null } });
    } catch (error) {
      console.error("Get AI settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/ai-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = aiSettingsSchema.parse(req.body);
      let settings = await prisma.aiSetting.findFirst();
      if (settings) {
        settings = await prisma.aiSetting.update({ where: { id: settings.id }, data });
      } else {
        settings = await prisma.aiSetting.create({ data });
      }
      await logActionSync(req.user!.userId, "UPDATE", "ai_settings", settings.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: { ...settings, apiKey: settings.apiKey ? "[ENCRYPTED]" : null } });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update AI settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/ai/test",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const settings = await prisma.aiSetting.findFirst();
      if (!settings || !settings.isEnabled) {
        res.status(503).json({ success: false, error: "AI service is not configured or disabled" });
        return;
      }
      res.json({
        success: true,
        data: {
          status: "ok",
          message: `AI connection test for ${settings.provider}/${settings.model} - simulated success`,
          provider: settings.provider,
          model: settings.model,
        },
      });
    } catch (error) {
      console.error("Test AI error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/ocr-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      let settings = await prisma.ocrSetting.findFirst();
      if (!settings) {
        settings = await prisma.ocrSetting.create({ data: {} });
      }
      res.json({ success: true, data: { ...settings, apiKey: settings.apiKey ? "[ENCRYPTED]" : null } });
    } catch (error) {
      console.error("Get OCR settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/ocr-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = ocrSettingsSchema.parse(req.body);
      let settings = await prisma.ocrSetting.findFirst();
      if (settings) {
        settings = await prisma.ocrSetting.update({ where: { id: settings.id }, data });
      } else {
        settings = await prisma.ocrSetting.create({ data });
      }
      await logActionSync(req.user!.userId, "UPDATE", "ocr_settings", settings.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: { ...settings, apiKey: settings.apiKey ? "[ENCRYPTED]" : null } });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update OCR settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/ocr-documents",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const documents = await prisma.ocrSupportedDocument.findMany({ orderBy: { name: "asc" } });
      res.json({ success: true, data: documents });
    } catch (error) {
      console.error("List OCR documents error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/ocr-documents",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = ocrDocumentSchema.parse(req.body);
      const document = await prisma.ocrSupportedDocument.create({ data: { ...data, fields: JSON.stringify(data.fields) } });
      await logActionSync(req.user!.userId, "CREATE", "ocr_documents", document.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: document });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create OCR document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
