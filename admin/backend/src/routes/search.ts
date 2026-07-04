import { Router, Request, Response } from "express";
import { prisma } from "../lib/prisma";
import { requireAuth } from "../middleware/auth";

const router = Router();

router.get("/api/admin/search", requireAuth, async (req: Request, res: Response) => {
  try {
    const q = (req.query.q as string)?.trim();
    if (!q || q.length < 2) { res.json({ success: true, data: { orders: [], customers: [], documents: [] } }); return; }

    const [orders, customers, documents] = await Promise.all([
      prisma.order.findMany({
        where: { OR: [{ orderNumber: { contains: q } }, { customerName: { contains: q } }, { customerPhone: { contains: q } }, { customerEmail: { contains: q } }] },
        take: 5, orderBy: { createdAt: "desc" },
        include: { service: { select: { name: true } } },
      }),
      prisma.user.findMany({
        where: { role: "CUSTOMER", OR: [{ name: { contains: q } }, { email: { contains: q } }, { phone: { contains: q } }] },
        take: 5, orderBy: { createdAt: "desc" },
        select: { id: true, name: true, email: true, phone: true, _count: { select: { orders: true } } },
      }),
      prisma.document.findMany({
        where: { OR: [{ documentNumber: { contains: q } }, { documentType: { contains: q } }] },
        take: 5, orderBy: { createdAt: "desc" },
        include: { service: { select: { name: true } }, order: { select: { orderNumber: true } } },
      }),
    ]);

    res.json({ success: true, data: { orders, customers, documents } });
  } catch (error) {
    console.error("Search error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
