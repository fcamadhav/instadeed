import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const updateUserSchema = z.object({
  name: z.string().min(1).optional(),
  role: z.enum(["SUPER_ADMIN", "ADMIN", "ACCOUNTS", "LEGAL_TEAM", "DRAFTING_TEAM", "SALES", "SUPPORT", "CUSTOMER"]).optional(),
  isActive: z.boolean().optional(),
  phone: z.string().optional(),
  avatarUrl: z.string().nullable().optional(),
});

router.get(
  "/api/admin/users",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const search = (req.query.search as string) || "";
      const role = req.query.role as string;
      const isActive = req.query.isActive as string;

      const where: Record<string, unknown> = {};
      if (search) {
        where.OR = [
          { name: { contains: search, mode: "insensitive" } },
          { email: { contains: search, mode: "insensitive" } },
          { phone: { contains: search, mode: "insensitive" } },
        ];
      }
      if (role) where.role = role;
      if (isActive === "true") where.isActive = true;
      else if (isActive === "false") where.isActive = false;

      const [users, total] = await Promise.all([
        prisma.user.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          select: { id: true, name: true, email: true, phone: true, role: true, isActive: true, avatarUrl: true, lastLoginAt: true, createdAt: true },
        }),
        prisma.user.count({ where }),
      ]);

      res.json({
        success: true,
        data: { users, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List users error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/users/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const user = await prisma.user.findUnique({
  where: { id: req.params.id as string },
        select: {
          id: true, name: true, email: true, phone: true, role: true, isActive: true,
          avatarUrl: true, googleId: true, lastLoginAt: true, createdAt: true, updatedAt: true,
          _count: { select: { orders: true, loginHistory: true } },
          orders: { take: 5, orderBy: { createdAt: "desc" }, select: { id: true, orderNumber: true, total: true, status: true, paymentStatus: true, createdAt: true } },
          loginHistory: { take: 10, orderBy: { createdAt: "desc" }, select: { id: true, ipAddress: true, userAgent: true, createdAt: true } },
        },
      });
      if (!user) {
        res.status(404).json({ success: false, error: "User not found" });
        return;
      }
      res.json({ success: true, data: user });
    } catch (error) {
      console.error("Get user error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/users/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = updateUserSchema.parse(req.body);
      const oldUser = await prisma.user.findUnique({ where: { id: req.params.id } });
      if (!oldUser) {
        res.status(404).json({ success: false, error: "User not found" });
        return;
      }

      const user = await prisma.user.update({
        where: { id: req.params.id as string },
        data,
        select: { id: true, name: true, email: true, phone: true, role: true, isActive: true, avatarUrl: true, updatedAt: true },
      });

      await logActionSync(req.user!.userId, "UPDATE", "users", req.params.id, oldUser as unknown as Record<string, unknown>, user as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: user });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update user error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/users/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const oldUser = await prisma.user.findUnique({ where: { id: req.params.id } });
      if (!oldUser) {
        res.status(404).json({ success: false, error: "User not found" });
        return;
      }

      const user = await prisma.user.update({
        where: { id: req.params.id as string },
        data: { isActive: false },
        select: { id: true, name: true, email: true, isActive: true },
      });

      await logActionSync(req.user!.userId, "DELETE", "users", req.params.id, oldUser as unknown as Record<string, unknown>, user as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: user });
    } catch (error) {
      console.error("Delete user error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/users/:id/login-history",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));

      const [history, total] = await Promise.all([
        prisma.loginHistory.findMany({
          where: { userId: req.params.id as string },
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
        }),
        prisma.loginHistory.count({ where: { userId: req.params.id } }),
      ]);

      res.json({
        success: true,
        data: { history, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("Get login history error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
