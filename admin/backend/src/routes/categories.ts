import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const categorySchema = z.object({
  name: z.string().min(1),
  slug: z.string().min(1),
  description: z.string().optional(),
  icon: z.string().optional(),
  displayOrder: z.number().int().optional(),
  showOnHomepage: z.boolean().optional(),
  isActive: z.boolean().optional(),
});

router.get("/api/categories", async (req: Request, res: Response) => {
  try {
    const categories = await prisma.category.findMany({
      orderBy: { displayOrder: "asc" },
      include: { _count: { select: { services: true } } },
    });
    res.json({ success: true, data: categories });
  } catch (error) {
    console.error("List categories error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.get("/api/admin/categories", requireAuth, requireRole("SUPER_ADMIN", "ADMIN"), async (req: Request, res: Response) => {
  try {
    const page = Math.max(1, parseInt(req.query.page as string) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
    const [categories, total] = await Promise.all([
      prisma.category.findMany({ skip: (page-1)*limit, take: limit, orderBy: { displayOrder: "asc" }, include: { _count: { select: { services: true } } } }),
      prisma.category.count(),
    ]);
    res.json({ success: true, data: { categories, pagination: { page, limit, total, totalPages: Math.ceil(total/limit) } } });
  } catch (error) {
    console.error("List admin categories error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.post(
  "/api/admin/categories",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = categorySchema.parse(req.body);
      const category = await prisma.category.create({ data });
      await logActionSync(req.user!.userId, "CREATE", "categories", category.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: category });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      if ((error as { code?: string }).code === "P2002") {
        res.status(409).json({ success: false, error: "Category with this name or slug already exists" });
        return;
      }
      console.error("Create category error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/categories/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = categorySchema.partial().parse(req.body);
      const old = await prisma.category.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Category not found" });
        return;
      }
      const category = await prisma.category.update({ where: { id: req.params.id }, data });
      await logActionSync(req.user!.userId, "UPDATE", "categories", req.params.id, old as unknown as Record<string, unknown>, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: category });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update category error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/categories/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.category.findUnique({ where: { id: req.params.id }, include: { _count: { select: { services: true } } } });
      if (!old) {
        res.status(404).json({ success: false, error: "Category not found" });
        return;
      }
      if (old._count.services > 0) {
        res.status(400).json({ success: false, error: "Cannot delete category with existing services" });
        return;
      }
      await prisma.category.delete({ where: { id: req.params.id } });
      await logActionSync(req.user!.userId, "DELETE", "categories", req.params.id, old as unknown as Record<string, unknown>, undefined, req.ip);
      res.json({ success: true, data: { message: "Category deleted" } });
    } catch (error) {
      console.error("Delete category error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
