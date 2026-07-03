import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const createServiceSchema = z.object({
  name: z.string().min(1),
  slug: z.string().min(1),
  categoryId: z.string().uuid(),
  shortDescription: z.string().optional(),
  longDescription: z.string().optional(),
  icon: z.string().optional(),
  banner: z.string().optional(),
  deliveryTime: z.string().optional(),
  processingTime: z.string().optional(),
  sortOrder: z.number().int().optional(),
  isFeatured: z.boolean().optional(),
  showOnHomepage: z.boolean().optional(),
  seoTitle: z.string().optional(),
  seoDescription: z.string().optional(),
  urlSlug: z.string().optional(),
  status: z.enum(["ACTIVE", "INACTIVE"]).optional(),
});

router.get("/api/services", async (req: Request, res: Response) => {
  try {
    const page = Math.max(1, parseInt(req.query.page as string) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
    const categorySlug = req.query.category as string;

    const where: Record<string, unknown> = { status: "ACTIVE" };
    if (categorySlug) {
      where.category = { slug: categorySlug };
    }

    const [services, total] = await Promise.all([
      prisma.service.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { sortOrder: "asc" },
        include: { category: { select: { id: true, name: true, slug: true } }, pricing: true },
      }),
      prisma.service.count({ where }),
    ]);

    res.json({
      success: true,
      data: { services, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
    });
  } catch (error) {
    console.error("List services error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.get("/api/services/:slug", async (req: Request, res: Response) => {
  try {
    const service = await prisma.service.findUnique({
      where: { slug: req.params.slug },
      include: { category: true, pricing: true },
    });
    if (!service || service.status === "INACTIVE") {
      res.status(404).json({ success: false, error: "Service not found" });
      return;
    }
    res.json({ success: true, data: service });
  } catch (error) {
    console.error("Get service error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.get(
  "/api/admin/services",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const search = req.query.search as string;
      const status = req.query.status as string;

      const where: Record<string, unknown> = {};
      if (search) { where.OR = [{ name: { contains: search } }, { slug: { contains: search } }]; }
      if (status) { where.status = status; }

      const [services, total] = await Promise.all([
        prisma.service.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { sortOrder: "asc" },
          include: { category: { select: { id: true, name: true, slug: true } }, pricing: true, _count: { select: { orders: true } } },
        }),
        prisma.service.count({ where }),
      ]);

      res.json({
        success: true,
        data: { services, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("Admin list services error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/services/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const service = await prisma.service.findUnique({
        where: { id: req.params.id },
        include: { category: true, pricing: true, formTemplate: true, workflowTemplate: true, requiredDocs: true, _count: { select: { orders: true } } },
      });
      if (!service) { res.status(404).json({ success: false, error: "Service not found" }); return; }
      res.json({ success: true, data: service });
    } catch (error) {
      console.error("Get service error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/services/:id/status",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.service.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Service not found" });
        return;
      }
      const newStatus = old.status === "ACTIVE" ? "INACTIVE" : "ACTIVE";
      const service = await prisma.service.update({
        where: { id: req.params.id },
        data: { status: newStatus },
      });
      await logActionSync(req.user!.userId, "TOGGLE_STATUS", "services", req.params.id, { status: old.status }, { status: newStatus }, req.ip);
      res.json({ success: true, data: service });
    } catch (error) {
      console.error("Toggle service status error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/services",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = createServiceSchema.parse(req.body);
      const service = await prisma.service.create({ data });
      await logActionSync(req.user!.userId, "CREATE", "services", service.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: service });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create service error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/services/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const body = req.body;
      const old = await prisma.service.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Service not found" });
        return;
      }
      const serviceData: any = {};
      if (body.name !== undefined) serviceData.name = body.name;
      if (body.slug !== undefined) serviceData.slug = body.slug;
      if (body.categoryId !== undefined) serviceData.categoryId = body.categoryId;
      if (body.shortDescription !== undefined) serviceData.shortDescription = body.shortDescription;
      if (body.longDescription !== undefined) serviceData.longDescription = body.longDescription;
      if (body.deliveryTime !== undefined) serviceData.deliveryTime = body.deliveryTime;
      if (body.processingTime !== undefined) serviceData.processingTime = body.processingTime;
      if (body.sortOrder !== undefined) serviceData.sortOrder = body.sortOrder;
      if (body.isFeatured !== undefined) serviceData.isFeatured = body.isFeatured;
      if (body.showOnHomepage !== undefined) serviceData.showOnHomepage = body.showOnHomepage;
      if (body.status !== undefined) serviceData.status = body.status;

      const service = await prisma.service.update({ where: { id: req.params.id }, data: serviceData });

      if (body.price !== undefined) {
        const existing = await prisma.pricing.findUnique({ where: { serviceId: service.id } });
        if (existing) {
          await prisma.pricing.update({ where: { serviceId: service.id }, data: { currentPrice: body.price } });
        } else {
          await prisma.pricing.create({ data: { serviceId: service.id, currentPrice: body.price, gstPercent: 18, currency: "INR" } });
        }
      }

      await logActionSync(req.user!.userId, "UPDATE", "services", req.params.id, old as unknown as Record<string, unknown>, serviceData as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: service });
    } catch (error) {
      console.error("Update service error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/services/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.service.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Service not found" });
        return;
      }
      await prisma.service.delete({ where: { id: req.params.id } });
      await logActionSync(req.user!.userId, "DELETE", "services", req.params.id, old as unknown as Record<string, unknown>, undefined, req.ip);
      res.json({ success: true, data: { message: "Service deleted" } });
    } catch (error) {
      console.error("Delete service error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
