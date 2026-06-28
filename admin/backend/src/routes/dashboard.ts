import { Router, Request, Response } from "express";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";

const router = Router();

router.get(
  "/api/admin/dashboard",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS", "SALES", "LEGAL_TEAM", "DRAFTING_TEAM", "SUPPORT"),
  async (_req: Request, res: Response) => {
    try {
      const now = new Date();
      const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);

      const [
        todayOrders,
        todayRevenueAgg,
        monthRevenueAgg,
        totalOrders,
        pendingOrders,
        completedOrders,
        cancelledOrders,
        refundedOrders,
        activeCustomers,
        newCustomersMonth,
        topServices,
        recentOrders,
        latestActivity,
        aiSettings,
        documentStats,
        rentAgreementStats,
      ] = await Promise.all([
        prisma.order.count({ where: { createdAt: { gte: todayStart } } }),
        prisma.order.aggregate({ where: { createdAt: { gte: todayStart }, paymentStatus: "PAID" }, _sum: { total: true } }),
        prisma.order.aggregate({ where: { createdAt: { gte: monthStart }, paymentStatus: "PAID" }, _sum: { total: true } }),
        prisma.order.count(),
        prisma.order.count({ where: { status: "PENDING" } }),
        prisma.order.count({ where: { status: "COMPLETED" } }),
        prisma.order.count({ where: { status: "CANCELLED" } }),
        prisma.order.count({ where: { status: "REFUNDED" } }),
        prisma.user.count({ where: { role: "CUSTOMER", isActive: true } }),
        prisma.user.count({ where: { role: "CUSTOMER", createdAt: { gte: monthStart } } }),
        (async () => {
          const grouped = await prisma.order.groupBy({
            by: ["serviceId"],
            _count: true,
            _sum: { total: true },
            orderBy: { _count: { id: "desc" } },
            take: 10,
          });
          const serviceIds = grouped.map(g => g.serviceId);
          const services = await prisma.service.findMany({
            where: { id: { in: serviceIds } },
            select: { id: true, name: true, slug: true },
          });
          const serviceMap = new Map(services.map(s => [s.id, s]));
          return grouped.map(g => ({ ...serviceMap.get(g.serviceId), orderCount: g._count, revenue: g._sum.total }));
        })(),
        prisma.order.findMany({
          take: 10,
          orderBy: { createdAt: "desc" },
          include: { service: { select: { id: true, name: true } }, customer: { select: { id: true, name: true } } },
        }),
        prisma.auditLog.findMany({
          take: 20,
          orderBy: { createdAt: "desc" },
          include: { user: { select: { id: true, name: true } } },
        }),
        prisma.aiSetting.findFirst({ select: { isEnabled: true, provider: true, model: true } }),
        prisma.document.aggregate({ _count: true, _sum: { fileSize: true } }),
        (async () => {
          const now = new Date();
          const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
          const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
          const all = await prisma.rentAgreement.findMany({
            where: { renewalStatus: { not: "ARCHIVED" } },
            select: { endDate: true, renewalStatus: true, updatedAt: true },
          });
          let active = 0, expired = 0;
          let exp7 = 0, exp15 = 0, exp30 = 0, exp60 = 0, exp90 = 0;
          for (const a of all) {
            const end = new Date(a.endDate);
            const days = Math.ceil((end.getTime() - today.getTime()) / 86400000);
            if (a.renewalStatus === "RENEWED") continue;
            if (days < 0) { expired++; continue; }
            active++;
            if (days <= 7) exp7++;
            else if (days <= 15) exp15++;
            else if (days <= 30) exp30++;
            else if (days <= 60) exp60++;
            else if (days <= 90) exp90++;
          }
          const renewedThisMonth = all.filter(a => a.renewalStatus === "RENEWED" && a.updatedAt >= thisMonth).length;
          return { active, expired, expiring7: exp7, expiring15: exp15, expiring30: exp30, expiring60: exp60, expiring90: exp90, renewedThisMonth, total: all.length };
        })(),
      ]);

      const apiUsage = await prisma.activityLog.count({
        where: { createdAt: { gte: monthStart } },
      });

      res.json({
        success: true,
        data: {
          today: {
            orders: todayOrders,
            revenue: todayRevenueAgg._sum.total || 0,
          },
          monthly: {
            revenue: monthRevenueAgg._sum.total || 0,
            newCustomers: newCustomersMonth,
          },
          totalOrders,
          ordersByStatus: {
            pending: pendingOrders,
            completed: completedOrders,
            cancelled: cancelledOrders,
            refunded: refundedOrders,
          },
          customers: {
            active: activeCustomers,
            newThisMonth: newCustomersMonth,
          },
          ai: aiSettings
            ? { enabled: aiSettings.isEnabled, provider: aiSettings.provider, model: aiSettings.model }
            : null,
          apiUsage,
          topServices: topServices.filter((s) => s.name),
          recentOrders,
          latestActivity,
          documents: {
            total: documentStats._count,
            storageSize: documentStats._sum.fileSize || 0,
          },
          rentAgreements: rentAgreementStats,
        },
      });
    } catch (error) {
      console.error("Dashboard error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
