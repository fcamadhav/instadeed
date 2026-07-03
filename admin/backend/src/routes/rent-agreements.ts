import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const createSchema = z.object({
  customerId: z.string().uuid().optional(),
  customerName: z.string().min(1),
  mobile: z.string().min(1),
  email: z.string().email().optional().or(z.literal("")),
  landlordName: z.string().min(1),
  tenantName: z.string().min(1),
  propertyAddress: z.string().min(1),
  startDate: z.string().min(1),
  endDate: z.string().min(1),
  duration: z.number().int().positive(),
  securityDeposit: z.number().nonnegative(),
  monthlyRent: z.number().nonnegative(),
  registrationNumber: z.string().optional().or(z.literal("")),
  pdfFilePath: z.string().optional().or(z.literal("")),
  docxFilePath: z.string().optional().or(z.literal("")),
  paymentStatus: z.string().optional(),
  renewalStatus: z.string().optional(),
});

const updateSchema = createSchema.partial().omit({ renewalStatus: true });

async function generateAgreementId(): Promise<string> {
  const year = new Date().getFullYear().toString();
  const last = await prisma.rentAgreement.findFirst({
    where: { agreementId: { startsWith: `RA-${year}-` } },
    orderBy: { createdAt: "desc" },
  });
  let seq = 1;
  if (last) {
    const parts = last.agreementId.split("-");
    seq = parseInt(parts[parts.length - 1], 10) + 1;
  }
  return `RA-${year}-GN-${String(seq).padStart(6, "0")}`;
}

function daysBetween(a: Date, b: Date): number {
  return Math.ceil((a.getTime() - b.getTime()) / (1000 * 60 * 60 * 24));
}

// Stats
router.get(
  "/api/admin/rent-agreements/stats",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const agreements = await prisma.rentAgreement.findMany({
        where: { renewalStatus: { not: "ARCHIVED" } },
        select: { endDate: true, renewalStatus: true, startDate: true, monthlyRent: true, createdAt: true },
      });

      let active = 0, expired = 0, renewed = 0;
      let exp7 = 0, exp15 = 0, exp30 = 0, exp60 = 0, exp90 = 0;
      const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);

      for (const a of agreements) {
        const end = new Date(a.endDate);
        const daysLeft = daysBetween(end, today);
        if (a.renewalStatus === "RENEWED") { renewed++; continue; }
        if (daysLeft < 0) { expired++; continue; }
        active++;
        if (daysLeft <= 7) exp7++;
        else if (daysLeft <= 15) exp15++;
        else if (daysLeft <= 30) exp30++;
        else if (daysLeft <= 60) exp60++;
        else if (daysLeft <= 90) exp90++;
      }

      const renewedThisMonth = await prisma.rentAgreement.count({
        where: { renewalStatus: "RENEWED", updatedAt: { gte: thisMonth } },
      });

      res.json({
        success: true,
        data: {
          totalActive: active,
          expired,
          renewed,
          expiring7: exp7,
          expiring15: exp15,
          expiring30: exp30,
          expiring60: exp60,
          expiring90: exp90,
          renewedThisMonth,
          totalAgreements: agreements.length,
        },
      });
    } catch (error) {
      console.error("Rent stats error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Calendar
router.get(
  "/api/admin/rent-agreements/calendar",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const year = parseInt(req.query.year as string) || new Date().getFullYear();
      const month = parseInt(req.query.month as string) || new Date().getMonth() + 1;
      const start = new Date(year, month - 1, 1);
      const end = new Date(year, month, 0, 23, 59, 59);

      const agreements = await prisma.rentAgreement.findMany({
        where: { endDate: { gte: start, lte: end } },
        select: { id: true, agreementId: true, customerName: true, endDate: true, renewalStatus: true },
        orderBy: { endDate: "asc" },
      });

      res.json({ success: true, data: { agreements, year, month } });
    } catch (error) {
      console.error("Calendar error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reports
router.get(
  "/api/admin/rent-agreements/reports",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const type = (req.query.type as string) || "expiring-week";
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

      let where: Record<string, unknown> = {};
      const todayEnd = new Date(today.getTime() + 86400000);

      switch (type) {
        case "expiring-week": {
          const weekEnd = new Date(today.getTime() + 7 * 86400000);
          where = { endDate: { gte: today, lte: weekEnd }, renewalStatus: "ACTIVE" };
          break;
        }
        case "expiring-month": {
          const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);
          where = { endDate: { gte: today, lte: monthEnd }, renewalStatus: "ACTIVE" };
          break;
        }
        case "renewed-month": {
          const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
          where = { renewalStatus: "RENEWED", updatedAt: { gte: monthStart } };
          break;
        }
        case "pending-renewals": {
          where = { endDate: { lt: today }, renewalStatus: "ACTIVE" };
          break;
        }
        case "revenue-renewals": {
          const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
          where = { renewalStatus: "RENEWED", updatedAt: { gte: monthStart } };
          break;
        }
        default:
          where = { endDate: { gte: today, lte: new Date(today.getTime() + 7 * 86400000) }, renewalStatus: "ACTIVE" };
      }

      const agreements = await prisma.rentAgreement.findMany({
        where,
        orderBy: { endDate: "asc" },
        select: {
          id: true, agreementId: true, customerName: true, mobile: true, email: true,
          landlordName: true, tenantName: true, propertyAddress: true,
          startDate: true, endDate: true, duration: true,
          securityDeposit: true, monthlyRent: true, paymentStatus: true, renewalStatus: true,
        },
      });

      if (type === "revenue-renewals") {
        const totalRevenue = agreements.reduce((s, a) => s + a.monthlyRent * a.duration + a.securityDeposit, 0);
        res.json({ success: true, data: { type, agreements, totalRevenue, count: agreements.length } });
      } else {
        res.json({ success: true, data: { type, agreements, count: agreements.length } });
      }
    } catch (error) {
      console.error("Reports error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// List
router.get(
  "/api/admin/rent-agreements",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const search = req.query.search as string;
      const status = req.query.status as string;
      const expiryFilter = req.query.expiry as string;

      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

      const where: Record<string, unknown> = {};

      if (search) {
        where.OR = [
          { customerName: { contains: search } },
          { mobile: { contains: search } },
          { email: { contains: search } },
          { agreementId: { contains: search } },
          { landlordName: { contains: search } },
          { tenantName: { contains: search } },
          { propertyAddress: { contains: search } },
        ];
      }

      if (status) where.renewalStatus = status;

      if (expiryFilter) {
        switch (expiryFilter) {
          case "today": where.endDate = { gte: today, lt: new Date(today.getTime() + 86400000) }; break;
          case "7days": where.endDate = { gte: today, lt: new Date(today.getTime() + 7 * 86400000) }; break;
          case "15days": where.endDate = { gte: today, lt: new Date(today.getTime() + 15 * 86400000) }; break;
          case "30days": where.endDate = { gte: today, lt: new Date(today.getTime() + 30 * 86400000) }; break;
          case "60days": where.endDate = { gte: today, lt: new Date(today.getTime() + 60 * 86400000) }; break;
          case "90days": where.endDate = { gte: today, lt: new Date(today.getTime() + 90 * 86400000) }; break;
          case "expired": where.endDate = { lt: today }; where.renewalStatus = { not: "RENEWED" }; break;
          case "renewed": where.renewalStatus = "RENEWED"; break;
        }
      }

      const [agreements, total] = await Promise.all([
        prisma.rentAgreement.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: {
            reminders: { orderBy: { remindAt: "desc" }, take: 1 },
            timeline: { orderBy: { createdAt: "desc" }, take: 3 },
          },
        }),
        prisma.rentAgreement.count({ where }),
      ]);

      const enriched = agreements.map(a => ({
        ...a,
        daysLeft: daysBetween(new Date(a.endDate), today),
      }));

      res.json({
        success: true,
        data: { agreements: enriched, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List rent agreements error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Create
router.post(
  "/api/admin/rent-agreements",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = createSchema.parse(req.body);
      const agreementId = await generateAgreementId();
      const agreement = await prisma.rentAgreement.create({
        data: {
          ...data,
          agreementId,
          startDate: new Date(data.startDate),
          endDate: new Date(data.endDate),
          email: data.email || null,
          registrationNumber: data.registrationNumber || null,
          pdfFilePath: data.pdfFilePath || null,
          docxFilePath: data.docxFilePath || null,
        },
      });
      await prisma.rentAgreementTimeline.create({
        data: { agreementId: agreement.id, event: "CREATED", description: "Agreement created" },
      });
      await logActionSync(req.user!.userId, "CREATE", "rent-agreements", agreement.id, undefined, data as any, req.ip);
      res.status(201).json({ success: true, data: agreement });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Create rent agreement error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reminder settings - get
router.get(
  "/api/admin/rent-agreements/reminder-settings",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const settings = await prisma.systemSetting.findMany({
        where: { key: { startsWith: "rent_reminder_" } },
      });
      const defaults = {
        whatsapp: true, sms: true, email: true,
        days90: true, days60: true, days30: true, days15: true, days7: true, days3: true, days0: true,
      };
      const merged = { ...defaults };
      for (const s of settings) {
        const key = s.key.replace("rent_reminder_", "");
        merged[key as keyof typeof defaults] = s.value === "true";
      }
      res.json({ success: true, data: merged });
    } catch (error) {
      console.error("Reminder settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reminder settings - update
router.put(
  "/api/admin/rent-agreements/reminder-settings",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const body = req.body || {};
      for (const [key, value] of Object.entries(body)) {
        const existing = await prisma.systemSetting.findUnique({ where: { key: `rent_reminder_${key}` } });
        if (existing) {
          await prisma.systemSetting.update({ where: { key: `rent_reminder_${key}` }, data: { value: String(value) } });
        } else {
          await prisma.systemSetting.create({ data: { key: `rent_reminder_${key}`, value: String(value) } });
        }
      }
      res.json({ success: true, data: { message: "Settings updated" } });
    } catch (error) {
      console.error("Update reminder settings error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Get single
router.get(
  "/api/admin/rent-agreements/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const agreement = await prisma.rentAgreement.findUnique({
        where: { id: req.params.id },
        include: {
          reminders: { orderBy: { remindAt: "desc" } },
          timeline: { orderBy: { createdAt: "desc" } },
        },
      });
      if (!agreement) { res.status(404).json({ success: false, error: "Not found" }); return; }
      res.json({
        success: true,
        data: { ...agreement, daysLeft: daysBetween(new Date(agreement.endDate), today) },
      });
    } catch (error) {
      console.error("Get rent agreement error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Update
router.put(
  "/api/admin/rent-agreements/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = updateSchema.parse(req.body);
      const old = await prisma.rentAgreement.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Not found" }); return; }
      const updateData: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(data)) {
        if (v !== undefined) updateData[k] = v;
      }
      if (updateData.startDate) updateData.startDate = new Date(updateData.startDate as string);
      if (updateData.endDate) updateData.endDate = new Date(updateData.endDate as string);
      const agreement = await prisma.rentAgreement.update({ where: { id: req.params.id }, data: updateData });
      await logActionSync(req.user!.userId, "UPDATE", "rent-agreements", req.params.id, old as any, data as any, req.ip);
      res.json({ success: true, data: agreement });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Update rent agreement error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Delete
router.delete(
  "/api/admin/rent-agreements/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.rentAgreement.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Not found" }); return; }
      await prisma.rentAgreementTimeline.deleteMany({ where: { agreementId: req.params.id } });
      await prisma.rentAgreementReminder.deleteMany({ where: { agreementId: req.params.id } });
      await prisma.rentAgreement.delete({ where: { id: req.params.id } });
      await logActionSync(req.user!.userId, "DELETE", "rent-agreements", req.params.id, old as any, undefined, req.ip);
      res.json({ success: true, data: { message: "Deleted" } });
    } catch (error) {
      console.error("Delete rent agreement error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Renew
router.post(
  "/api/admin/rent-agreements/:id/renew",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.rentAgreement.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Not found" }); return; }
      if (old.renewalStatus === "ARCHIVED") { res.status(400).json({ success: false, error: "Already archived" }); return; }

      const body = req.body || {};
      const startDate = new Date(body.startDate || old.endDate);
      const endDate = new Date(body.endDate || new Date(startDate.getTime() + old.duration * 30 * 86400000));
      const duration = body.duration || old.duration;
      const monthlyRent = body.monthlyRent !== undefined ? body.monthlyRent : old.monthlyRent;
      const securityDeposit = body.securityDeposit !== undefined ? body.securityDeposit : old.securityDeposit;

      const newAgreement = await prisma.rentAgreement.create({
        data: {
          agreementId: await generateAgreementId(),
          customerId: old.customerId,
          customerName: body.customerName || old.customerName,
          mobile: body.mobile || old.mobile,
          email: body.email || old.email,
          landlordName: body.landlordName || old.landlordName,
          tenantName: body.tenantName || old.tenantName,
          propertyAddress: body.propertyAddress || old.propertyAddress,
          startDate,
          endDate,
          duration,
          securityDeposit,
          monthlyRent,
          previousAgreementId: old.id,
          paymentStatus: "PENDING",
          renewalStatus: "ACTIVE",
        },
      });

      await prisma.rentAgreement.update({
        where: { id: old.id },
        data: { renewalStatus: "RENEWED", renewedAgreementId: newAgreement.id },
      });

      await prisma.rentAgreementTimeline.createMany({
        data: [
          { agreementId: old.id, event: "RENEWED", description: `Renewed → ${newAgreement.agreementId}` },
          { agreementId: newAgreement.id, event: "CREATED", description: `Renewal of ${old.agreementId}` },
        ],
      });

      await logActionSync(req.user!.userId, "RENEW", "rent-agreements", old.id, old as any, { newAgreementId: newAgreement.id } as any, req.ip);
      res.status(201).json({ success: true, data: { old: { ...old, renewalStatus: "RENEWED" }, renewed: newAgreement } });
    } catch (error) {
      console.error("Renew error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reminders - schedule
router.post(
  "/api/admin/rent-agreements/:id/reminders",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const agreement = await prisma.rentAgreement.findUnique({ where: { id: req.params.id } });
      if (!agreement) { res.status(404).json({ success: false, error: "Not found" }); return; }

      const channels: string[] = req.body.channels || ["EMAIL"];
      const endDate = new Date(agreement.endDate);
      const intervals = [90, 60, 30, 15, 7, 3, 0];
      const reminders = [];

      for (const days of intervals) {
        const remindAt = new Date(endDate.getTime() - days * 86400000);
        if (remindAt > new Date()) {
          for (const channel of channels) {
            reminders.push({ agreementId: agreement.id, remindAt, channel, status: "SCHEDULED" });
          }
        }
      }

      if (reminders.length > 0) {
        await prisma.rentAgreementReminder.createMany({ data: reminders });
        await prisma.rentAgreementTimeline.create({
          data: {
            agreementId: agreement.id,
            event: "REMINDER_SCHEDULED",
            description: `${reminders.length} reminders scheduled (${channels.join(", ")})`,
          },
        });
      }

      res.json({ success: true, data: { scheduled: reminders.length } });
    } catch (error) {
      console.error("Schedule reminders error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reminders - list
router.get(
  "/api/admin/rent-agreements/:id/reminders",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const reminders = await prisma.rentAgreementReminder.findMany({
        where: { agreementId: req.params.id },
        orderBy: { remindAt: "asc" },
      });
      res.json({ success: true, data: reminders });
    } catch (error) {
      console.error("List reminders error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Reminders - update status
router.put(
  "/api/admin/rent-agreements/:id/reminders/:reminderId",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const { status } = z.object({ status: z.string().min(1) }).parse(req.body);
      const reminder = await prisma.rentAgreementReminder.update({
        where: { id: req.params.reminderId },
        data: { status, sentAt: status === "SENT" ? new Date() : undefined },
      });
      res.json({ success: true, data: reminder });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Update reminder error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Timeline
router.get(
  "/api/admin/rent-agreements/:id/timeline",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const timeline = await prisma.rentAgreementTimeline.findMany({
        where: { agreementId: req.params.id },
        orderBy: { createdAt: "desc" },
      });
      res.json({ success: true, data: timeline });
    } catch (error) {
      console.error("Timeline error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
