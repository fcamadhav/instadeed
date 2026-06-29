import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";
import { generateDocument } from "../services/pdf-generator";
import path from "path";
import fs from "fs";

const router = Router();

const gstConfigSchema = z.object({
  gstNumber: z.string().optional(),
  gstRate: z.number().min(0).max(100).optional(),
  sacCode: z.string().optional(),
  invoicePrefix: z.string().optional(),
  invoiceFooter: z.string().optional(),
  invoiceLogo: z.string().optional(),
  bankName: z.string().optional(),
  bankAccount: z.string().optional(),
  bankIfsc: z.string().optional(),
  bankBranch: z.string().optional(),
  qrCode: z.string().optional(),
});

router.get("/api/admin/gst-config", requireAuth, requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"), async (req: Request, res: Response) => {
    try {
      let config = await prisma.gstConfig.findFirst();
      if (!config) {
        config = await prisma.gstConfig.create({ data: {} });
      }
      res.json({ success: true, data: config });
    } catch (error) {
      console.error("Get GST config error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Alias for frontend
router.get("/api/admin/gst", requireAuth, requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"), async (req: Request, res: Response) => {
    try {
      let config = await prisma.gstConfig.findFirst();
      if (!config) {
        config = await prisma.gstConfig.create({ data: {} });
      }
      res.json({ success: true, data: { settings: config } });
    } catch (error) {
      console.error("Get GST error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put("/api/admin/gst-config", requireAuth, requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"), async (req: Request, res: Response) => {
    try {
      const data = gstConfigSchema.parse(req.body);
      let config = await prisma.gstConfig.findFirst();
      if (config) {
        config = await prisma.gstConfig.update({ where: { id: config.id }, data });
      } else {
        config = await prisma.gstConfig.create({ data });
      }
      await logActionSync(req.user!.userId, "UPDATE", "gst_config", config.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: config });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update GST config error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Alias for frontend
router.put("/api/admin/gst", requireAuth, requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"), async (req: Request, res: Response) => {
    try {
      const data = req.body;
      let config = await prisma.gstConfig.findFirst();
      if (config) {
        config = await prisma.gstConfig.update({ where: { id: config.id }, data });
      } else {
        config = await prisma.gstConfig.create({ data });
      }
      res.json({ success: true, data: config });
    } catch (error) {
      console.error("Update GST error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/invoices",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS", "CUSTOMER"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const status = req.query.status as string;

      const where: Record<string, unknown> = {};
      if (status) where.status = status;
      if (req.user!.role === "CUSTOMER") {
        where.order = { customerId: req.user!.userId };
      }

      const [invoices, total] = await Promise.all([
        prisma.invoice.findMany({
          where,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: { order: { select: { id: true, orderNumber: true, customerName: true, customerEmail: true } } },
        }),
        prisma.invoice.count({ where }),
      ]);

      res.json({
        success: true,
        data: { invoices, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("List invoices error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/invoices/:id/download",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS", "CUSTOMER"),
  async (req: Request, res: Response) => {
    try {
      const invoice = await prisma.invoice.findUnique({
        where: { id: req.params.id },
        include: {
          order: {
            include: {
              customer: { select: { name: true, email: true, phone: true } },
              service: { select: { name: true } },
            },
          },
        },
      });
      if (!invoice) {
        res.status(404).json({ success: false, error: "Invoice not found" });
        return;
      }
      if (req.user!.role === "CUSTOMER" && invoice.order.customerId !== req.user!.userId) {
        res.status(403).json({ success: false, error: "Access denied" });
        return;
      }
      // Generate PDF if not yet generated
      let pdfUrl = invoice.pdfUrl;
      if (!pdfUrl) {
        const pdfDir = path.resolve(__dirname, "..", "..", "storage", "invoices");
        if (!fs.existsSync(pdfDir)) fs.mkdirSync(pdfDir, { recursive: true });
        const pdfName = `${invoice.invoiceNumber || `INV-${invoice.id}`}.pdf`;
        const pdfPath = path.join(pdfDir, pdfName);
        const payload = {
          invoiceNumber: invoice.invoiceNumber,
          customerName: invoice.order.customer?.name || invoice.order.customerName || "",
          customerEmail: invoice.order.customer?.email || "",
          serviceName: invoice.order.service?.name || "",
          orderNumber: invoice.order.orderNumber,
          amount: invoice.order.total,
          taxAmount: invoice.gstAmount || 0,
          totalAmount: invoice.total || invoice.order.total,
          createdAt: invoice.createdAt?.toISOString(),
        };
        await generateDocument(payload, "invoice", invoice.order.id, pdfName);
        pdfUrl = pdfPath;
        await prisma.invoice.update({ where: { id: invoice.id }, data: { pdfUrl: pdfPath } });
      }
      if (pdfUrl && fs.existsSync(pdfUrl)) {
        res.download(pdfUrl, path.basename(pdfUrl));
        return;
      }
      res.status(404).json({ success: false, error: "Invoice PDF not available" });
    } catch (error) {
      console.error("Download invoice error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/gst-report",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const dateFrom = req.query.dateFrom ? new Date(req.query.dateFrom as string) : new Date(new Date().getFullYear(), new Date().getMonth(), 1);
      const dateTo = req.query.dateTo ? new Date(req.query.dateTo as string) : new Date();

      const invoices = await prisma.invoice.findMany({
        where: { createdAt: { gte: dateFrom, lte: dateTo }, status: "PAID" },
        include: { order: true },
      });

      const totalRevenue = invoices.reduce((sum, inv) => sum + inv.total, 0);
      const totalGst = invoices.reduce((sum, inv) => sum + inv.gstAmount, 0);
      const totalInvoices = invoices.length;

      res.json({
        success: true,
        data: {
          dateFrom: dateFrom.toISOString(),
          dateTo: dateTo.toISOString(),
          totalInvoices,
          totalRevenue,
          totalGst,
          taxableAmount: totalRevenue - totalGst,
          invoices,
        },
      });
    } catch (error) {
      console.error("GST report error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
