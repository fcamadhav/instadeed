import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const systemSettingSchema = z.object({
  key: z.string().min(1),
  value: z.string(),
});

const apiSettingSchema = z.object({
  apiKey: z.string().optional(),
  apiSecret: z.string().optional(),
  extra: z.record(z.unknown()).optional(),
  isActive: z.boolean().optional(),
});

router.get(
  "/api/admin/settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const settings = await prisma.systemSetting.findMany({ orderBy: { key: "asc" } });
      const map: Record<string, string> = {};
      settings.forEach((s) => { map[s.key] = s.value; });
      res.json({ success: true, data: map });
    } catch (error) {
      console.error("List settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/settings",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const entries = req.body as Record<string, string>;
      if (!entries || typeof entries !== "object") {
        res.status(400).json({ success: false, error: "Expected object of key-value pairs" });
        return;
      }

      const upserts = Object.entries(entries).map(([key, value]) =>
        prisma.systemSetting.upsert({
          where: { key },
          update: { value: String(value) },
          create: { key, value: String(value) },
        })
      );
      await Promise.all(upserts);
      await logActionSync(req.user!.userId, "UPDATE", "settings", "bulk", undefined, entries, req.ip);
      res.json({ success: true, data: { message: "Settings updated", count: Object.keys(entries).length } });
    } catch (error) {
      console.error("Update settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/api-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const settings = await prisma.apiSetting.findMany({ orderBy: { provider: "asc" } });
      const sanitized = settings.map((s) => ({
        ...s,
        apiKey: s.apiKey ? "[ENCRYPTED]" : null,
        apiSecret: s.apiSecret ? "[ENCRYPTED]" : null,
      }));
      res.json({ success: true, data: sanitized });
    } catch (error) {
      console.error("List API settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/api-settings/:provider",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = apiSettingSchema.parse(req.body);
      const provider = req.params.provider.toUpperCase();
      const old = await prisma.apiSetting.findUnique({ where: { provider } });

      let setting;
      const apiData = { ...data, extra: JSON.stringify(data.extra) };
      if (old) {
        setting = await prisma.apiSetting.update({ where: { provider }, data: apiData });
      } else {
        setting = await prisma.apiSetting.create({ data: { provider, ...apiData } });
      }

      await logActionSync(req.user!.userId, "UPDATE", "api_settings", provider, old as unknown as Record<string, unknown> || undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({
        success: true,
        data: { ...setting, apiKey: setting.apiKey ? "[ENCRYPTED]" : null, apiSecret: setting.apiSecret ? "[ENCRYPTED]" : null },
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update API setting error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/backup/run",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const { exec } = require("child_process");
      exec("/usr/local/bin/instadeed-backup", { timeout: 120000 }, (error: any, stdout: string, stderr: string) => {
        if (error) {
          console.error("Backup error:", stderr);
          res.status(500).json({ success: false, error: "Backup failed: " + (stderr || error.message) });
          return;
        }
        const lines = stdout.split("\n").filter(l => l.includes(".gz") || l.includes("Complete"));
        res.json({
          success: true,
          data: {
            message: "Backup completed successfully",
            files: lines.map(l => l.trim()).filter(Boolean),
          },
        });
      });
    } catch (error) {
      console.error("Backup trigger error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
