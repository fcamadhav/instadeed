import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const notificationSchema = z.object({
  userId: z.string().uuid().optional(),
  type: z.enum(["EMAIL", "WHATSAPP", "SMS", "PUSH", "WEBHOOK"]),
  title: z.string().min(1),
  message: z.string().min(1),
  referenceType: z.string().optional(),
  referenceId: z.string().optional(),
});

const emailTemplateSchema = z.object({
  name: z.string().min(1),
  subject: z.string().min(1),
  body: z.string().min(1),
  variables: z.string().optional(),
  isActive: z.boolean().optional(),
});

const whatsappTemplateSchema = z.object({
  name: z.string().min(1),
  templateId: z.string().optional(),
  body: z.string().min(1),
  variables: z.string().optional(),
  isActive: z.boolean().optional(),
});

router.get(
  "/api/admin/notifications",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const type = req.query.type as string;

      const where: Record<string, unknown> = {};
      if (type) where.type = type;

      const [notifications, total] = await Promise.all([
        prisma.notification.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: { user: { select: { id: true, name: true, email: true } } },
        }),
        prisma.notification.count({ where }),
      ]);

      res.json({
        success: true,
        data: { notifications, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List notifications error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/notifications",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const data = notificationSchema.parse(req.body);
      const notification = await prisma.notification.create({ data });
      await logActionSync(req.user!.userId, "CREATE", "notifications", notification.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: notification });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create notification error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/email-templates",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const templates = await prisma.emailTemplate.findMany({ orderBy: { name: "asc" } });
      res.json({ success: true, data: templates });
    } catch (error) {
      console.error("List email templates error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/email-templates",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = emailTemplateSchema.parse(req.body);
      const template = await prisma.emailTemplate.create({ data });
      await logActionSync(req.user!.userId, "CREATE", "email_templates", template.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: template });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      if ((error as { code?: string }).code === "P2002") {
        res.status(409).json({ success: false, error: "Template name already exists" });
        return;
      }
      console.error("Create email template error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/email-templates/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = emailTemplateSchema.partial().parse(req.body);
      const old = await prisma.emailTemplate.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Email template not found" });
        return;
      }
      const template = await prisma.emailTemplate.update({ where: { id: req.params.id }, data });
      await logActionSync(req.user!.userId, "UPDATE", "email_templates", req.params.id, old as unknown as Record<string, unknown>, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: template });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update email template error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/whatsapp-templates",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const templates = await prisma.whatsAppTemplate.findMany({ orderBy: { name: "asc" } });
      res.json({ success: true, data: templates });
    } catch (error) {
      console.error("List WhatsApp templates error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/whatsapp-templates",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = whatsappTemplateSchema.parse(req.body);
      const template = await prisma.whatsAppTemplate.create({ data });
      await logActionSync(req.user!.userId, "CREATE", "whatsapp_templates", template.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: template });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      if ((error as { code?: string }).code === "P2002") {
        res.status(409).json({ success: false, error: "Template name already exists" });
        return;
      }
      console.error("Create WhatsApp template error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/whatsapp-templates/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = whatsappTemplateSchema.partial().parse(req.body);
      const old = await prisma.whatsAppTemplate.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "WhatsApp template not found" });
        return;
      }
      const template = await prisma.whatsAppTemplate.update({ where: { id: req.params.id }, data });
      await logActionSync(req.user!.userId, "UPDATE", "whatsapp_templates", req.params.id, old as unknown as Record<string, unknown>, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: template });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update WhatsApp template error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
