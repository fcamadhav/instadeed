import { Router, Request, Response } from "express";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";

const router = Router();

router.get(
  "/api/admin/customers",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const search = (req.query.search as string) || "";

      const where: Record<string, unknown> = { role: "CUSTOMER" };
      if (search) {
        where.OR = [
          { name: { contains: search, mode: "insensitive" } },
          { email: { contains: search, mode: "insensitive" } },
          { phone: { contains: search, mode: "insensitive" } },
        ];
      }

      const [customers, total] = await Promise.all([
        prisma.user.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          select: {
            id: true, name: true, email: true, phone: true, isActive: true, createdAt: true, lastLoginAt: true,
            _count: { select: { orders: true } },
            orders: { select: { total: true, paymentStatus: true } },
          },
        }),
        prisma.user.count({ where }),
      ]);

      const enriched = customers.map(c => ({
        ...c,
        totalSpent: c.orders.filter(o => o.paymentStatus === "PAID").reduce((s,o) => s + o.total, 0),
        orders: undefined,
      }));

      res.json({
        success: true,
        data: { customers: enriched, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List customers error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/customers/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const customer = await prisma.user.findFirst({
        where: { id: req.params.id, role: "CUSTOMER" },
        select: {
          id: true, name: true, email: true, phone: true, isActive: true, avatarUrl: true, lastLoginAt: true, createdAt: true, updatedAt: true,
          _count: { select: { orders: true, loginHistory: true } },
          loginHistory: { orderBy: { createdAt: "desc" }, take: 20, select: { id: true, ipAddress: true, userAgent: true, createdAt: true } },
        },
      });
      if (!customer) {
        res.status(404).json({ success: false, error: "Customer not found" });
        return;
      }
      res.json({ success: true, data: customer });
    } catch (error) {
      console.error("Get customer error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/customers/:id/orders",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));

      const [orders, total] = await Promise.all([
        prisma.order.findMany({
          where: { customerId: req.params.id },
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: { service: { select: { id: true, name: true, slug: true } } },
        }),
        prisma.order.count({ where: { customerId: req.params.id } }),
      ]);

      res.json({
        success: true,
        data: { orders, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("Get customer orders error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/customers/:id/documents",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM"),
  async (req: Request, res: Response) => {
    try {
      const documents = await prisma.documentVersion.findMany({
        where: { order: { customerId: req.params.id } },
        orderBy: { createdAt: "desc" },
        include: { order: { select: { id: true, orderNumber: true, service: { select: { name: true } } } } },
      });
      res.json({ success: true, data: documents });
    } catch (error) {
      console.error("Get customer documents error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
