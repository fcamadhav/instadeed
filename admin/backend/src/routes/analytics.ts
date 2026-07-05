import { Router, Request, Response } from "express";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";

const router = Router();

router.get(
  "/api/admin/analytics/dashboard",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const now = new Date();
      const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);

      const [
        totalOrders,
        todayOrders,
        monthOrders,
        totalRevenue,
        todayRevenue,
        monthRevenue,
        totalUsers,
        newUsersMonth,
        ordersByStatus,
        ordersByPayment,
        topServices,
      ] = await Promise.all([
        prisma.order.count(),
        prisma.order.count({ where: { createdAt: { gte: todayStart } } }),
        prisma.order.count({ where: { createdAt: { gte: monthStart } } }),
        prisma.order.aggregate({ where: { status: "COMPLETED" }, _sum: { total: true } }),
        prisma.order.aggregate({ where: { createdAt: { gte: todayStart }, status: "COMPLETED" }, _sum: { total: true } }),
        prisma.order.aggregate({ where: { createdAt: { gte: monthStart }, status: "COMPLETED" }, _sum: { total: true } }),
        prisma.user.count({ where: { role: "CUSTOMER" } }),
        prisma.user.count({ where: { role: "CUSTOMER", createdAt: { gte: monthStart } } }),
        prisma.order.groupBy({ by: ["status"], _count: true }),
        prisma.order.groupBy({ by: ["paymentStatus"], _count: true }),
        prisma.order.groupBy({ by: ["serviceId"], _count: true, _sum: { total: true } }),
      ]);

      const topServiceData = await Promise.all(
        topServices.slice(0, 10).map(async (s) => {
          const service = await prisma.service.findUnique({ where: { id: s.serviceId }, select: { id: true, name: true, slug: true } });
          return { ...service, orderCount: s._count, revenue: s._sum.total };
        })
      );

      res.json({
        success: true,
        data: {
          orders: { total: totalOrders, today: todayOrders, thisMonth: monthOrders },
          revenue: {
            total: totalRevenue._sum.total || 0,
            today: todayRevenue._sum.total || 0,
            thisMonth: monthRevenue._sum.total || 0,
          },
          customers: { total: totalUsers, newThisMonth: newUsersMonth },
          ordersByStatus,
          ordersByPayment,
          topServices: topServiceData,
        },
      });
    } catch (error) {
      console.error("Dashboard analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/analytics/revenue",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const dateFrom = req.query.dateFrom ? new Date(req.query.dateFrom as string) : new Date(new Date().getFullYear(), 0, 1);
      const dateTo = req.query.dateTo ? new Date(req.query.dateTo as string) : new Date();

      const orders = await prisma.order.findMany({
        where: { createdAt: { gte: dateFrom, lte: dateTo } },
        orderBy: { createdAt: "asc" },
        select: { id: true, orderNumber: true, total: true, tax: true, discount: true, status: true, paymentStatus: true, createdAt: true },
      });

      const totalRevenue = orders.reduce((s, o) => s + (o.status === "COMPLETED" ? o.total : 0), 0);
      const totalTax = orders.reduce((s, o) => s + (o.status === "COMPLETED" ? o.tax : 0), 0);
      const totalDiscount = orders.reduce((s, o) => s + o.discount, 0);
      const paidOrders = orders.filter((o) => o.paymentStatus === "PAID").length;

      res.json({
        success: true,
        data: {
          dateFrom: dateFrom.toISOString(),
          dateTo: dateTo.toISOString(),
          totalRevenue,
          totalTax,
          totalDiscount,
          totalOrders: orders.length,
          paidOrders,
          orders,
        },
      });
    } catch (error) {
      console.error("Revenue analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/analytics/orders",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const dateFrom = req.query.dateFrom ? new Date(req.query.dateFrom as string) : new Date(new Date().getFullYear(), 0, 1);
      const dateTo = req.query.dateTo ? new Date(req.query.dateTo as string) : new Date();

      const statusBreakdown = await prisma.order.groupBy({
        by: ["status"],
        where: { createdAt: { gte: dateFrom, lte: dateTo } },
        _count: true,
        _sum: { total: true },
      });

      const paymentBreakdown = await prisma.order.groupBy({
        by: ["paymentStatus"],
        where: { createdAt: { gte: dateFrom, lte: dateTo } },
        _count: true,
        _sum: { total: true },
      });

      res.json({
        success: true,
        data: { dateFrom: dateFrom.toISOString(), dateTo: dateTo.toISOString(), statusBreakdown, paymentBreakdown },
      });
    } catch (error) {
      console.error("Orders analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/analytics/customers",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES"),
  async (_req: Request, res: Response) => {
    try {
      const total = await prisma.user.count({ where: { role: "CUSTOMER" } });
      const active = await prisma.user.count({ where: { role: "CUSTOMER", isActive: true } });
      const withOrders = await prisma.user.count({ where: { role: "CUSTOMER", orders: { some: {} } } });
      const recent = await prisma.user.findMany({
        where: { role: "CUSTOMER" },
        orderBy: { createdAt: "desc" },
        take: 5,
        select: { id: true, name: true, email: true, createdAt: true, _count: { select: { orders: true } } },
      });

      res.json({ success: true, data: { total, active, withOrders, recentCustomers: recent } });
    } catch (error) {
      console.error("Customers analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/analytics/top-services",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const dateFrom = req.query.dateFrom ? new Date(req.query.dateFrom as string) : undefined;
      const dateTo = req.query.dateTo ? new Date(req.query.dateTo as string) : undefined;

      const where: Record<string, unknown> = { status: "COMPLETED" };
      if (dateFrom || dateTo) {
        where.createdAt = {};
        if (dateFrom) (where.createdAt as Record<string, unknown>).gte = dateFrom;
        if (dateTo) (where.createdAt as Record<string, unknown>).lte = dateTo;
      }

      const grouped = await prisma.order.groupBy({
        by: ["serviceId"],
        where,
        _count: true,
        _sum: { total: true },
        orderBy: { _count: { id: "desc" } },
        take: 20,
      });

      const services = await Promise.all(
        grouped.map(async (g) => {
          const service = await prisma.service.findUnique({ where: { id: g.serviceId }, select: { id: true, name: true, slug: true, categoryId: true } });
          return { ...service, orderCount: g._count, revenue: g._sum.total };
        })
      );

      res.json({ success: true, data: services });
    } catch (error) {
      console.error("Top services analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/analytics/monthly-growth",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const twelveMonthsAgo = new Date();
      twelveMonthsAgo.setMonth(twelveMonthsAgo.getMonth() - 12);

      const orders = await prisma.order.findMany({
        where: { createdAt: { gte: twelveMonthsAgo } },
        select: { total: true, createdAt: true, paymentStatus: true },
        orderBy: { createdAt: "asc" },
      });

      const monthlyMap: Record<string, { revenue: number; orders: number }> = {};
      orders.forEach((o) => {
        const key = `${o.createdAt.getFullYear()}-${String(o.createdAt.getMonth() + 1).padStart(2, "0")}`;
        if (!monthlyMap[key]) monthlyMap[key] = { revenue: 0, orders: 0 };
        monthlyMap[key].orders++;
        if (o.status === "COMPLETED") monthlyMap[key].revenue += o.total;
      });

      const monthlyGrowth = Object.entries(monthlyMap)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([month, data]) => ({ month, ...data }));

      res.json({ success: true, data: monthlyGrowth });
    } catch (error) {
      console.error("Monthly growth analytics error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get("/api/admin/analytics", requireAuth, requireRole("SUPER_ADMIN", "ADMIN"), async (_req: Request, res: Response) => {
  res.json({ success: true, data: { message: "Use /api/admin/analytics/dashboard for detailed analytics" } });
});

// Reports page compatibility
router.get("/api/admin/reports/:type", requireAuth, requireRole("SUPER_ADMIN", "ADMIN"), async (req: Request, res: Response) => {
  try {
    const startDate = req.query.startDate ? new Date(req.query.startDate as string) : new Date(Date.now() - 30*86400000);
    const endDate = req.query.endDate ? new Date(req.query.endDate as string) : new Date();
    const type = req.params.type;

    if (type === 'revenue' || type === 'orders' || type === 'customers' || type === 'monthly_growth') {
      const orders = await prisma.order.findMany({
        where: { createdAt: { gte: startDate, lte: endDate }, status: "COMPLETED" },
        select: { total: true, createdAt: true, status: true, service: { select: { name: true } } },
        orderBy: { createdAt: "asc" },
      });
      const months: Record<string,any> = {};
      orders.forEach(o => {
        const m = o.createdAt.toISOString().slice(0,7);
        if (!months[m]) months[m] = { month: new Date(o.createdAt).toLocaleString('en-IN',{month:'short'}), revenue:0, orders:0, customers:0 };
        if (o.status === "COMPLETED") { months[m].revenue += o.total; } months[m].orders += 1; months[m].customers += 1;
      });
      res.json({ success: true, data: { report: Object.values(months) } });
    } else if (type === 'top_services') {
      const grouped = await (prisma as any).order.groupBy({ by:["serviceId"], where:{createdAt:{gte:startDate,lte:endDate},status:"COMPLETED"}, _count:true, _sum:{total:true}, orderBy:{_sum:{total:"desc"}}, take:10 }) as { serviceId: string; _count: number; _sum: { total: number|null } }[];
      const svcs = await prisma.service.findMany({ where:{id:{in:grouped.map((g:any)=>g.serviceId)}}, select:{id:true,name:true} });
      const svcMap = new Map(svcs.map((s:any)=>[s.id,s]));
      res.json({ success: true, data: { report: grouped.map((g:any)=>({name:svcMap.get(g.serviceId)?.name||'Unknown',count:g._count,revenue:g._sum.total||0})) } });
    } else if (type === 'payments' || type === 'coupons') {
      res.json({ success: true, data: { report: [] } });
    } else {
      res.json({ success: true, data: { report: [] } });
    }
  } catch (e) { res.status(500).json({ success: false, error: "Internal server error" }); }
});

export default router;
