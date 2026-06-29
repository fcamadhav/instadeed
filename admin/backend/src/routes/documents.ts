import { Router, Request, Response } from "express";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";
import path from "path";
import fs from "fs";

const router = Router();
const STORAGE_ROOT = path.resolve(path.join(__dirname, "..", "..", "..", "storage", "documents"));

function isPathSafe(targetPath: string): boolean {
  if (!targetPath) return false;
  const resolved = path.resolve(targetPath);
  return resolved.startsWith(STORAGE_ROOT + path.sep) || resolved === STORAGE_ROOT;
}

const PREFIXES: Record<string, string> = {
  "rent-agreement": "RA",
  "sale-deed": "SD",
  "will": "WILL",
  "legal-notice": "LN",
  "trademark": "TM",
  "gst-registration": "GST",
};

function getDocumentPrefix(documentType: string): string {
  return PREFIXES[documentType] || "DOC";
}

async function generateDocumentNumber(documentType: string): Promise<string> {
  const prefix = getDocumentPrefix(documentType);
  const year = new Date().getFullYear().toString();
  const last = await prisma.document.findFirst({
    where: { documentNumber: { startsWith: `${prefix}-${year}-` } },
    orderBy: { createdAt: "desc" },
  });
  let seq = 1;
  if (last) {
    const parts = last.documentNumber.split("-");
    seq = parseInt(parts[parts.length - 1], 10) + 1;
  }
  return `${prefix}-${year}-${String(seq).padStart(6, "0")}`;
}

const createSchema = z.object({
  orderId: z.string().uuid().optional(),
  customerId: z.string().uuid(),
  serviceId: z.string().uuid(),
  documentType: z.string().min(1),
  formData: z.string().optional(),
  htmlContent: z.string().optional(),
  pdfFilePath: z.string().optional(),
  docxFilePath: z.string().optional(),
});

const updateSchema = z.object({
  customerId: z.string().uuid().optional(),
  documentType: z.string().optional(),
  formData: z.string().optional(),
  htmlContent: z.string().optional(),
  status: z.string().optional(),
});

router.get(
  "/api/admin/documents",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const documentType = req.query.documentType as string;
      const customerId = req.query.customerId as string;
      const dateFrom = req.query.dateFrom as string;
      const dateTo = req.query.dateTo as string;
      const paymentStatus = req.query.paymentStatus as string;
      const orderId = req.query.orderId as string;
      const search = (req.query.search as string) || "";
      const sortBy = (req.query.sortBy as string) || "createdAt";
      const sortOrder = (req.query.sortOrder as string) === "asc" ? "asc" as const : "desc" as const;

      const where: Record<string, unknown> = {};
      if (documentType) where.documentType = documentType;
      if (customerId) where.customerId = customerId;
      if (orderId) where.orderId = orderId;
      if (dateFrom || dateTo) {
        where.createdAt = {};
        if (dateFrom) (where.createdAt as Record<string, unknown>).gte = new Date(dateFrom);
        if (dateTo) (where.createdAt as Record<string, unknown>).lte = new Date(dateTo);
      }
      if (paymentStatus) {
        where.order = { paymentStatus };
      }
      if (search) {
        where.OR = [
          { documentNumber: { contains: search } },
          { customer: { name: { contains: search } } },
          { customer: { email: { contains: search } } },
          { customer: { phone: { contains: search } } },
        ];
      }

      const [documents, total] = await Promise.all([
        prisma.document.findMany({
          where: where as any,
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { [sortBy]: sortOrder },
          include: {
            customer: { select: { id: true, name: true, email: true, phone: true } },
            service: { select: { id: true, name: true, slug: true } },
            order: { select: { id: true, orderNumber: true, paymentStatus: true, total: true } },
            auditLogs: { take: 1, orderBy: { createdAt: "desc" }, include: { user: { select: { name: true } } } },
          },
        }),
        prisma.document.count({ where: where as any }),
      ]);

      const totalSize = documents.reduce((sum: number, d: { fileSize?: number }) => sum + (d.fileSize || 0), 0);

      res.json({
        success: true,
        data: {
          documents,
          pagination: { page, limit, total, totalPages: Math.ceil(total / limit) },
          stats: { totalDocuments: total, totalStorageSize: totalSize },
        },
      });
    } catch (error) {
      console.error("List documents error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = createSchema.parse(req.body);
      const documentNumber = await generateDocumentNumber(data.documentType);
      const document = await prisma.document.create({
        data: {
          ...data,
          documentNumber,
          customerId: data.customerId,
          serviceId: data.serviceId,
        },
      });
      await prisma.documentAuditLog.create({
        data: {
          documentId: document.id,
          action: "CREATED",
          userId: req.user!.userId,
          ipAddress: req.ip,
          userAgent: req.headers["user-agent"] || null,
        },
      });
      await logActionSync(req.user!.userId, "CREATE", "documents", document.id, undefined, data as any, req.ip);
      res.status(201).json({ success: true, data: document });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/documents/stats",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (_req: Request, res: Response) => {
    try {
      const [total, aggr] = await Promise.all([
        prisma.document.count(),
        prisma.document.aggregate({ _sum: { fileSize: true } }),
      ]);
      const byType = await prisma.document.groupBy({ by: ["documentType"], _count: true });
      res.json({
        success: true,
        data: {
          totalDocuments: total,
          totalStorageSize: aggr._sum.fileSize || 0,
          byType: byType.map(b => ({ type: b.documentType, count: b._count })),
        },
      });
    } catch (error) {
      console.error("Document stats error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents/bulk/download",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const ids = z.array(z.string().uuid()).parse(req.body.ids);
      const documents = await prisma.document.findMany({
        where: { id: { in: ids }, pdfFilePath: { not: null } },
      });
      res.json({
        success: true,
        data: {
          message: `Bulk download prepared for ${documents.length} documents`,
          files: documents.map(d => ({ id: d.id, documentNumber: d.documentNumber, filePath: d.pdfFilePath })),
        },
      });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Bulk download error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents/bulk/delete",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const ids = z.array(z.string().uuid()).parse(req.body.ids);
      const docs = await prisma.document.findMany({ where: { id: { in: ids } } });
      for (const doc of docs) {
        if (doc.pdfFilePath && isPathSafe(doc.pdfFilePath)) try { fs.unlinkSync(doc.pdfFilePath); } catch {}
        if (doc.docxFilePath && isPathSafe(doc.docxFilePath)) try { fs.unlinkSync(doc.docxFilePath); } catch {}
      }
      await prisma.documentAuditLog.deleteMany({ where: { documentId: { in: ids } } });
      await prisma.document.deleteMany({ where: { id: { in: ids } } });
      await logActionSync(req.user!.userId, "BULK_DELETE", "documents", ids.join(","), undefined, { count: docs.length }, req.ip);
      res.json({ success: true, data: { message: `${docs.length} documents deleted` } });
    } catch (error) {
      if (error instanceof z.ZodError) { res.status(400).json({ success: false, error: error.errors }); return; }
      console.error("Bulk delete error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents/bulk/export",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const ids = z.array(z.string().uuid()).optional().parse(req.body.ids);
      const where = ids ? { id: { in: ids } } : {};
      const documents = await prisma.document.findMany({
        where,
        include: { customer: { select: { name: true, email: true, phone: true } }, service: { select: { name: true } } },
        orderBy: { createdAt: "desc" },
      });
      const rows = documents.map(d => ({
        "Document ID": d.documentNumber,
        "Customer Name": d.customer?.name || "",
        "Mobile": d.customer?.phone || "",
        "Email": d.customer?.email || "",
        "Document Type": d.documentType,
        "Created Date": d.createdAt.toISOString(),
        "Status": d.status,
        "Version": d.version,
      }));
      res.json({ success: true, data: { rows } });
    } catch (error) {
      console.error("Export error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/documents/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const document = await prisma.document.findUnique({
        where: { id: req.params.id },
        include: {
          customer: { select: { id: true, name: true, email: true, phone: true } },
          service: { select: { id: true, name: true, slug: true } },
          order: { select: { id: true, orderNumber: true, paymentStatus: true, total: true } },
          auditLogs: {
            orderBy: { createdAt: "desc" },
            include: { user: { select: { id: true, name: true } } },
          },
        },
      });
      if (!document) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      res.json({ success: true, data: document });
    } catch (error) {
      console.error("Get document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/documents/:id",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = updateSchema.parse(req.body);
      const old = await prisma.document.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      const updateData: Record<string, unknown> = { ...data };
      if (data.status === "REGENERATED") {
        updateData.version = old.version + 1;
      }
      const document = await prisma.document.update({
        where: { id: req.params.id },
        data: updateData,
      });
      await prisma.documentAuditLog.create({
        data: {
          documentId: document.id,
          action: data.status === "REGENERATED" ? "REGENERATED" : "EDITED",
          userId: req.user!.userId,
          ipAddress: req.ip,
          userAgent: req.headers["user-agent"] || null,
        },
      });
      await logActionSync(req.user!.userId, data.status === "REGENERATED" ? "REGENERATE" : "UPDATE", "documents", req.params.id, old as any, data as any, req.ip);
      res.json({ success: true, data: document });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.delete(
  "/api/admin/documents/:id",
  requireAuth,
  requireRole("SUPER_ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const old = await prisma.document.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      if (old.pdfFilePath && isPathSafe(old.pdfFilePath)) {
        try { fs.unlinkSync(old.pdfFilePath); } catch {}
      }
      if (old.docxFilePath && isPathSafe(old.docxFilePath)) {
        try { fs.unlinkSync(old.docxFilePath); } catch {}
      }
      await prisma.documentAuditLog.deleteMany({ where: { documentId: req.params.id } });
      await prisma.document.delete({ where: { id: req.params.id } });
      await logActionSync(req.user!.userId, "DELETE", "documents", req.params.id, old as any, undefined, req.ip);
      res.json({ success: true, data: { message: "Document deleted" } });
    } catch (error) {
      console.error("Delete document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/documents/:id/download/pdf",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const doc = await prisma.document.findUnique({ where: { id: req.params.id } });
      if (!doc || !doc.pdfFilePath || !isPathSafe(doc.pdfFilePath)) {
        res.status(404).json({ success: false, error: "PDF not found" });
        return;
      }
      if (!fs.existsSync(doc.pdfFilePath)) {
        res.status(404).json({ success: false, error: "PDF file missing from disk" });
        return;
      }
      await prisma.documentAuditLog.create({
        data: { documentId: doc.id, action: "DOWNLOADED", userId: req.user!.userId, ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
      });
      const filename = `${doc.documentNumber}.pdf`;
      res.download(doc.pdfFilePath, filename);
    } catch (error) {
      console.error("Download PDF error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/documents/:id/download/docx",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const doc = await prisma.document.findUnique({ where: { id: req.params.id } });
      if (!doc || !doc.docxFilePath || !isPathSafe(doc.docxFilePath)) {
        res.status(404).json({ success: false, error: "DOCX not found" });
        return;
      }
      if (!fs.existsSync(doc.docxFilePath)) {
        res.status(404).json({ success: false, error: "DOCX file missing from disk" });
        return;
      }
      await prisma.documentAuditLog.create({
        data: { documentId: doc.id, action: "DOWNLOADED", userId: req.user!.userId, ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
      });
      const filename = `${doc.documentNumber}.docx`;
      res.download(doc.docxFilePath, filename);
    } catch (error) {
      console.error("Download DOCX error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/documents/:id/preview",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const doc = await prisma.document.findUnique({ where: { id: req.params.id } });
      if (!doc || !doc.htmlContent) {
        res.status(404).json({ success: false, error: "Preview not available" });
        return;
      }
      res.setHeader("Content-Security-Policy", "default-src 'self'; script-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:;");
      res.send(doc.htmlContent);
    } catch (error) {
      console.error("Preview error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents/:id/email",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const doc = await prisma.document.findUnique({
        where: { id: req.params.id },
        include: { customer: true },
      });
      if (!doc) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      await prisma.documentAuditLog.create({
        data: { documentId: doc.id, action: "EMAILED", userId: req.user!.userId, ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
      });
      res.json({ success: true, data: { message: `Document emailed to ${doc.customer.email || "customer"}` } });
    } catch (error) {
      console.error("Email document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/documents/:id/whatsapp",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const doc = await prisma.document.findUnique({
        where: { id: req.params.id },
        include: { customer: true },
      });
      if (!doc) {
        res.status(404).json({ success: false, error: "Document not found" });
        return;
      }
      await prisma.documentAuditLog.create({
        data: { documentId: doc.id, action: "WHATSAPPED", userId: req.user!.userId, ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
      });
      res.json({ success: true, data: { message: `Document sent via WhatsApp to ${doc.customer.phone || "customer"}` } });
    } catch (error) {
      console.error("WhatsApp document error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/documents",
  requireAuth,
  async (req: Request, res: Response) => {
    try {
      const customerId = req.user!.userId;
      const page = Math.max(1, parseInt(req.query.page as string) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
      const [documents, total] = await Promise.all([
        prisma.document.findMany({
          where: { customerId },
          skip: (page - 1) * limit,
          take: limit,
          orderBy: { createdAt: "desc" },
          include: {
            service: { select: { id: true, name: true, slug: true } },
            order: { select: { orderNumber: true, paymentStatus: true } },
          },
        }),
        prisma.document.count({ where: { customerId } }),
      ]);
      res.json({
        success: true,
        data: { documents, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
      });
    } catch (error) {
      console.error("My documents error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// Customer-facing document download (used by old SPA after payment)
router.get(
  "/api/customer/documents/:orderId/download",
  async (req: Request, res: Response) => {
    try {
      const order = await prisma.order.findUnique({
        where: { orderNumber: req.params.orderId },
        include: { documents: true },
      });
      if (!order) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      // If there's a generated PDF, serve it
      if (order.documents && order.documents.length > 0) {
        const doc = order.documents[order.documents.length - 1];
        if (doc.pdfFilePath) {
          if (!fs.existsSync(doc.pdfFilePath)) {
            res.status(404).json({ success: false, error: "PDF file not found" });
            return;
          }
          await prisma.documentAuditLog.create({
            data: { documentId: doc.id, action: "DOWNLOADED", ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
          });
          res.download(doc.pdfFilePath, `${doc.documentNumber}.pdf`);
          return;
        }
      }
      // No PDF generated yet — return a placeholder
      res.status(404).json({ success: false, error: "Document not yet generated" });
    } catch (error) {
      console.error("Customer download error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
