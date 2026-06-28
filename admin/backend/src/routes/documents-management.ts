import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

// ─── Zod Schemas ───
const statusUpdateSchema = z.object({
  status: z.enum(["DRAFT","SUBMITTED","PAYMENT_PENDING","PAYMENT_SUCCESS","ASSIGNED","UNDER_REVIEW","READY_FOR_SUBMISSION","SUBMITTED_TO_AUTHORITY","COMPLETED","ARCHIVED"]),
});

const assignSchema = z.object({
  staffId: z.string().uuid(),
  role: z.enum(["EMPLOYEE","ADVOCATE","CASE_MANAGER","PROPERTY_EXECUTIVE"]).optional(),
});

const noteSchema = z.object({
  note: z.string().min(1),
});

const bulkActionSchema = z.object({
  ids: z.array(z.string().uuid()).min(1).max(100),
});

const bulkStatusSchema = bulkActionSchema.extend({
  status: z.enum(["DRAFT","SUBMITTED","PAYMENT_PENDING","PAYMENT_SUCCESS","ASSIGNED","UNDER_REVIEW","READY_FOR_SUBMISSION","SUBMITTED_TO_AUTHORITY","COMPLETED","ARCHIVED"]),
});

const bulkAssignSchema = bulkActionSchema.extend({
  staffId: z.string().uuid(),
  role: z.enum(["EMPLOYEE","ADVOCATE","CASE_MANAGER","PROPERTY_EXECUTIVE"]).optional(),
});

// ─── List all documents with lifecycle ───
router.get(
  "/api/admin/documents-management",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const status = req.query.status as string;
      const search = (req.query.search as string) || "";
      const staffId = req.query.staffId as string;
      const dateFrom = req.query.dateFrom as string;
      const dateTo = req.query.dateTo as string;

      const where: Record<string, unknown> = {};
      if (status) where.status = status;
      if (staffId) where.assignedToId = staffId;
      if (dateFrom || dateTo) {
        where.createdAt = {};
        if (dateFrom) (where.createdAt as Record<string, unknown>).gte = new Date(dateFrom);
        if (dateTo) (where.createdAt as Record<string, unknown>).lte = new Date(dateTo);
      }

      // For customers - only their own documents
      if (req.user!.role === "CUSTOMER") {
        where.document = { customerId: req.user!.userId };
      }

      const [lifecycles, total] = await Promise.all([
        prisma.documentLifecycle.findMany({
          where: where as any,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { updatedAt: "desc" },
          include: {
            document: {
              include: {
                customer: { select: { id: true, name: true, email: true, phone: true } },
                service: { select: { id: true, name: true, slug: true } },
                order: { select: { id: true, orderNumber: true, paymentStatus: true, total: true } },
              },
            },
            assignedTo: { select: { id: true, name: true, email: true, role: true } },
            versions: { take: 1, orderBy: { version: "desc" }, select: { version: true, createdAt: true } },
            timeline: { take: 3, orderBy: { createdAt: "desc" }, select: { event: true, createdAt: true } },
            _count: { select: { notes: true, versions: true } },
          },
        }),
        prisma.documentLifecycle.count({ where: where as any }),
      ]);

      res.json({
        success: true,
        data: {
          documents: lifecycles,
          pagination: { page, limit, total, totalPages: Math.ceil(total / limit) },
        },
      });
    } catch (error) {
      console.error("List document lifecycles error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Get single document lifecycle ───
router.get(
  "/api/admin/documents-management/:id",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const lifecycle = await prisma.documentLifecycle.findUnique({
        where: { id: req.params.id },
        include: {
          document: {
            include: {
              customer: { select: { id: true, name: true, email: true, phone: true } },
              service: { select: { id: true, name: true, slug: true, pricing: true } },
              order: { include: { invoices: true } },
            },
          },
          assignedTo: { select: { id: true, name: true, email: true, role: true } },
          versions: { orderBy: { version: "desc" }, include: { createdBy: { select: { name: true } } } },
          notes: { orderBy: { createdAt: "desc" }, include: { createdBy: { select: { name: true } } } },
          timeline: { orderBy: { createdAt: "desc" } },
        },
      });
      if (!lifecycle) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      // Customer can only view their own
      if (req.user!.role === "CUSTOMER" && lifecycle.document.customerId !== req.user!.userId) {
        res.status(403).json({ success: false, error: "Access denied" });
        return;
      }
      res.json({ success: true, data: lifecycle });
    } catch (error) {
      console.error("Get document lifecycle error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Update status ───
router.put(
  "/api/admin/documents-management/:id/status",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM"),
  async (req: Request, res: Response) => {
    try {
      const data = statusUpdateSchema.parse(req.body);
      const old = await prisma.documentLifecycle.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Document not found" }); return; }

      const lifecycle = await prisma.documentLifecycle.update({
        where: { id: req.params.id },
        data: {
          status: data.status,
          ...(data.status === "COMPLETED" ? { completedAt: new Date() } : {}),
          ...(data.status === "SUBMITTED_TO_AUTHORITY" ? { authoritySubAt: new Date() } : {}),
        },
      });

      await prisma.documentTimeline.create({
        data: { lifecycleId: req.params.id, event: "STATUS_CHANGED", description: `Status changed: ${old.status} → ${data.status}`, createdById: req.user!.userId },
      });
      await logActionSync(req.user!.userId, "UPDATE_STATUS", "documents_management", req.params.id, { status: old.status }, { status: data.status }, req.ip);
      res.json({ success: true, data: lifecycle });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Update status error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Assign staff ───
router.put(
  "/api/admin/documents-management/:id/assign",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = assignSchema.parse(req.body);
      const old = await prisma.documentLifecycle.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Document not found" }); return; }

      const lifecycle = await prisma.documentLifecycle.update({
        where: { id: req.params.id },
        data: { assignedToId: data.staffId, assignedRole: data.role || "EMPLOYEE", assignedAt: new Date(), status: old.status === "DRAFT" ? old.status : "ASSIGNED" },
      });

      await prisma.documentTimeline.create({
        data: { lifecycleId: req.params.id, event: "ASSIGNED", description: `Assigned to user ${data.staffId}`, createdById: req.user!.userId },
      });
      await logActionSync(req.user!.userId, "ASSIGN", "documents_management", req.params.id, { assignedTo: old.assignedToId }, { assignedTo: data.staffId }, req.ip);
      res.json({ success: true, data: lifecycle });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Assign error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Add internal note ───
router.post(
  "/api/admin/documents-management/:id/notes",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const data = noteSchema.parse(req.body);
      const lifecycle = await prisma.documentLifecycle.findUnique({ where: { id: req.params.id } });
      if (!lifecycle) { res.status(404).json({ success: false, error: "Document not found" }); return; }

      const note = await prisma.DocLifecycleNote.create({
        data: { lifecycleId: req.params.id, note: data.note, isInternal: true, createdById: req.user!.userId },
        include: { createdBy: { select: { name: true } } },
      });
      await prisma.documentTimeline.create({
        data: { lifecycleId: req.params.id, event: "NOTE_ADDED", description: "Internal note added", createdById: req.user!.userId },
      });
      res.status(201).json({ success: true, data: note });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Add note error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Get notes (internal only for admin) ───
router.get(
  "/api/admin/documents-management/:id/notes",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const lifecycle = await prisma.documentLifecycle.findUnique({ where: { id: req.params.id } });
      if (!lifecycle) { res.status(404).json({ success: false, error: "Document not found" }); return; }
      const notes = await prisma.DocLifecycleNote.findMany({
        where: { lifecycleId: req.params.id },
        orderBy: { createdAt: "desc" },
        include: { createdBy: { select: { name: true } } },
      });
      res.json({ success: true, data: notes });
    } catch (error) {
      console.error("Get notes error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Bulk status change ───
router.put(
  "/api/admin/documents-management/bulk/status",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = bulkStatusSchema.parse(req.body);
      const result = await prisma.documentLifecycle.updateMany({
        where: { id: { in: data.ids } },
        data: { status: data.status },
      });
      // Create timeline events for each
      for (const id of data.ids) {
        await prisma.documentTimeline.create({
          data: { lifecycleId: id, event: "STATUS_CHANGED", description: `Bulk status update to ${data.status}`, createdById: req.user!.userId },
        });
      }
      await logActionSync(req.user!.userId, "BULK_STATUS", "documents_management", data.ids.join(","), undefined, { status: data.status, count: result.count }, req.ip);
      res.json({ success: true, data: { message: `${result.count} documents updated` } });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Bulk status error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Bulk assign ───
router.put(
  "/api/admin/documents-management/bulk/assign",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = bulkAssignSchema.parse(req.body);
      const result = await prisma.documentLifecycle.updateMany({
        where: { id: { in: data.ids } },
        data: { assignedToId: data.staffId, assignedRole: data.role || "EMPLOYEE", assignedAt: new Date() },
      });
      for (const id of data.ids) {
        await prisma.documentTimeline.create({
          data: { lifecycleId: id, event: "ASSIGNED", description: `Bulk assigned to ${data.staffId}`, createdById: req.user!.userId },
        });
      }
      res.json({ success: true, data: { message: `${result.count} documents assigned` } });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Bulk assign error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Soft delete / archive ───
router.put(
  "/api/admin/documents-management/:id/archive",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.documentLifecycle.findUnique({ where: { id: req.params.id } });
      if (!old) { res.status(404).json({ success: false, error: "Document not found" }); return; }
      const newStatus = old.status === "ARCHIVED" ? "COMPLETED" : "ARCHIVED";
      const lifecycle = await prisma.documentLifecycle.update({
        where: { id: req.params.id },
        data: { status: newStatus },
      });
      await prisma.documentTimeline.create({
        data: { lifecycleId: req.params.id, event: "STATUS_CHANGED", description: `${newStatus === "ARCHIVED" ? "Archived" : "Restored from archive"}`, createdById: req.user!.userId },
      });
      res.json({ success: true, data: lifecycle });
    } catch (error) {
      console.error("Archive error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ─── Get staff list for assignment dropdown ───
router.get(
  "/api/admin/documents-management-staff",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const staff = await prisma.user.findMany({
        where: { role: { in: ["ADMIN", "SUPER_ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM", "SALES", "SUPPORT"] }, isActive: true },
        select: { id: true, name: true, email: true, role: true },
        orderBy: { name: "asc" },
      });
      res.json({ success: true, data: staff });
    } catch (error) {
      console.error("List staff error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
