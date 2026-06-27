import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const pricingSchema = z.object({
  currentPrice: z.number().positive(),
  oldPrice: z.number().positive().optional(),
  discountPercent: z.number().min(0).max(100).optional(),
  discountAmount: z.number().min(0).optional(),
  gstPercent: z.number().min(0).optional(),
  convenienceFee: z.number().min(0).optional(),
  processingFee: z.number().min(0).optional(),
  deliveryCharge: z.number().min(0).optional(),
  minimumPrice: z.number().positive().optional(),
  offerBadge: z.string().optional(),
  isLimitedOffer: z.boolean().optional(),
  subscriptionPrice: z.number().positive().optional(),
  emiAvailable: z.boolean().optional(),
  currency: z.string().optional(),
});

router.get("/api/services/:serviceId/pricing", async (req: Request, res: Response) => {
  try {
    const pricing = await prisma.pricing.findUnique({
      where: { serviceId: req.params.serviceId },
    });
    if (!pricing) {
      res.status(404).json({ success: false, error: "Pricing not found" });
      return;
    }
    res.json({ success: true, data: pricing });
  } catch (error) {
    console.error("Get pricing error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.put(
  "/api/admin/services/:serviceId/pricing",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = pricingSchema.parse(req.body);
      const existing = await prisma.pricing.findUnique({ where: { serviceId: req.params.serviceId } });
      const service = await prisma.service.findUnique({ where: { id: req.params.serviceId } });
      if (!service) {
        res.status(404).json({ success: false, error: "Service not found" });
        return;
      }

      let pricing;
      if (existing) {
        await prisma.pricingHistory.create({
          data: {
            pricingId: existing.id,
            currentPrice: existing.currentPrice,
            oldPrice: existing.oldPrice,
            discountPercent: existing.discountPercent,
            gstPercent: existing.gstPercent,
          },
        });
        pricing = await prisma.pricing.update({ where: { serviceId: req.params.serviceId }, data });
      } else {
        pricing = await prisma.pricing.create({ data: { ...data, serviceId: req.params.serviceId } });
      }

      await logActionSync(req.user!.userId, "UPDATE", "pricing", req.params.serviceId, existing as unknown as Record<string, unknown> || undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: pricing });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update pricing error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/services/:serviceId/pricing/history",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));

      const pricing = await prisma.pricing.findUnique({ where: { serviceId: req.params.serviceId } });
      if (!pricing) {
        res.status(404).json({ success: false, error: "Pricing not found" });
        return;
      }

      const [history, total] = await Promise.all([
        prisma.pricingHistory.findMany({
          where: { pricingId: pricing.id },
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
        }),
        prisma.pricingHistory.count({ where: { pricingId: pricing.id } }),
      ]);

      res.json({
        success: true,
        data: { history, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("Get pricing history error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
