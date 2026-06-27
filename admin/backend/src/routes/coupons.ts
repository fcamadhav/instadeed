import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const couponSchema = z.object({
  code: z.string().min(1).transform((v) => v.toUpperCase()),
  type: z.enum(["PERCENTAGE", "FLAT", "REFERRAL"]),
  value: z.number().positive(),
  minOrderAmount: z.number().min(0).optional(),
  maxDiscount: z.number().positive().optional(),
  maxUses: z.number().int().min(0).optional(),
  perUserLimit: z.number().int().min(1).optional(),
  expiresAt: z.string().datetime().optional(),
  isActive: z.boolean().optional(),
  serviceIds: z.array(z.string().uuid()).optional(),
});

const validateSchema = z.object({
  code: z.string().min(1),
  serviceId: z.string().uuid().optional(),
  amount: z.number().positive().optional(),
});

router.get(
  "/api/admin/coupons",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const search = (req.query.search as string) || "";

      const where: Record<string, unknown> = {};
      if (search) {
        where.code = { contains: search, mode: "insensitive" };
      }

      const [coupons, total] = await Promise.all([
        prisma.coupon.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: { services: { include: { service: { select: { id: true, name: true } } } } },
        }),
        prisma.coupon.count({ where }),
      ]);

      res.json({
        success: true,
        data: { coupons, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List coupons error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/coupons",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = couponSchema.parse(req.body);
      const { serviceIds, ...couponData } = data;

      const coupon = await prisma.coupon.create({
        data: {
          ...couponData,
          expiresAt: couponData.expiresAt ? new Date(couponData.expiresAt) : null,
          services: serviceIds?.length
            ? { create: serviceIds.map((serviceId) => ({ serviceId })) }
            : undefined,
        },
        include: { services: { include: { service: { select: { id: true, name: true } } } } },
      });

      await logActionSync(req.user!.userId, "CREATE", "coupons", coupon.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: coupon });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      if ((error as { code?: string }).code === "P2002") {
        res.status(409).json({ success: false, error: "Coupon code already exists" });
        return;
      }
      console.error("Create coupon error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/coupons/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = couponSchema.partial().parse(req.body);
      const { serviceIds, ...couponData } = data;

      const old = await prisma.coupon.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Coupon not found" });
        return;
      }

      if (couponData.expiresAt) {
        (couponData as Record<string, unknown>).expiresAt = new Date(couponData.expiresAt);
      }

      if (serviceIds) {
        await prisma.couponService.deleteMany({ where: { couponId: req.params.id } });
        await prisma.couponService.createMany({
          data: serviceIds.map((sid) => ({ couponId: req.params.id, serviceId: sid })),
        });
      }

      const coupon = await prisma.coupon.update({
        where: { id: req.params.id },
        data: couponData,
        include: { services: { include: { service: { select: { id: true, name: true } } } } },
      });

      await logActionSync(req.user!.userId, "UPDATE", "coupons", req.params.id, old as unknown as Record<string, unknown>, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: coupon });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update coupon error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/coupons/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.coupon.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Coupon not found" });
        return;
      }
      await prisma.coupon.delete({ where: { id: req.params.id } });
      await logActionSync(req.user!.userId, "DELETE", "coupons", req.params.id, old as unknown as Record<string, unknown>, undefined, req.ip);
      res.json({ success: true, data: { message: "Coupon deleted" } });
    } catch (error) {
      console.error("Delete coupon error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post("/api/validate-coupon", async (req: Request, res: Response) => {
  try {
    const data = validateSchema.parse(req.body);
    const coupon = await prisma.coupon.findUnique({ where: { code: data.code.toUpperCase() } });

    if (!coupon || !coupon.isActive) {
      res.status(404).json({ success: false, error: "Invalid or expired coupon" });
      return;
    }

    if (coupon.expiresAt && new Date() > coupon.expiresAt) {
      res.status(400).json({ success: false, error: "Coupon has expired" });
      return;
    }

    if (coupon.maxUses > 0 && coupon.currentUses >= coupon.maxUses) {
      res.status(400).json({ success: false, error: "Coupon usage limit reached" });
      return;
    }

    if (data.serviceId) {
      const serviceCoupon = await prisma.couponService.findUnique({
        where: { couponId_serviceId: { couponId: coupon.id, serviceId: data.serviceId } },
      });
      if (!serviceCoupon) {
        res.status(400).json({ success: false, error: "Coupon not applicable for this service" });
        return;
      }
    }

    let discountAmount = 0;
    if (coupon.type === "PERCENTAGE") {
      discountAmount = ((data.amount || 0) * coupon.value) / 100;
      if (coupon.maxDiscount) {
        discountAmount = Math.min(discountAmount, coupon.maxDiscount);
      }
    } else if (coupon.type === "FLAT") {
      discountAmount = coupon.value;
    }

    res.json({
      success: true,
      data: {
        valid: true,
        coupon: { id: coupon.id, code: coupon.code, type: coupon.type, value: coupon.value },
        discountAmount,
        finalAmount: Math.max(0, (data.amount || 0) - discountAmount),
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Validate coupon error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
