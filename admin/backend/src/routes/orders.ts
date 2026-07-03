import { Router, Request, Response } from "express";
import { z } from "zod";
import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

function extractQuotation(formData: string | null): Record<string, unknown> | null {
  if (!formData) return null;
  try {
    const parsed = JSON.parse(formData);
    if (parsed.quotation) return parsed.quotation;
    if (parsed.form_data?.quotation) return parsed.form_data.quotation;
  } catch { /* ignore */ }
  return null;
}

const createOrderSchema = z.object({
  customerId: z.string().uuid().optional(),
  customerName: z.string().optional(),
  customerPhone: z.string().optional(),
  customerEmail: z.string().email().optional(),
  serviceId: z.string().uuid(),
  amount: z.number().positive(),
  discount: z.number().min(0).optional(),
  tax: z.number().min(0).optional(),
  total: z.number().positive(),
  paymentGateway: z.enum(["RAZORPAY", "CASHFREE", "PHONEPE", "PAYU", "STRIPE", "MANUAL_UPI", "BANK_TRANSFER"]).optional(),
  paymentId: z.string().optional(),
  notes: z.string().optional(),
  formData: z.record(z.unknown()).optional(),
});

const statusSchema = z.object({
  status: z.enum(["PENDING", "COMPLETED", "CANCELLED", "REFUNDED"]),
});

const paymentSchema = z.object({
  paymentStatus: z.enum(["PENDING", "PAID", "FAILED", "REFUNDED"]),
  paymentGateway: z.enum(["RAZORPAY", "CASHFREE", "PHONEPE", "PAYU", "STRIPE", "MANUAL_UPI", "BANK_TRANSFER"]).optional(),
  paymentId: z.string().optional(),
});

const noteSchema = z.object({
  note: z.string().min(1),
});

const refundSchema = z.object({
  amount: z.number().positive(),
  reason: z.string().optional(),
});

const assignSchema = z.object({
  staffId: z.string().uuid(),
  role: z.string().optional(),
});

async function generateOrderNumber(): Promise<string> {
  const year = new Date().getFullYear().toString();
  const last = await prisma.order.findFirst({
    where: { orderNumber: { startsWith: `ORD-${year}-` } },
    orderBy: { createdAt: "desc" },
  });
  let seq = 1;
  if (last) {
    const parts = last.orderNumber.split("-");
    seq = parseInt(parts[parts.length - 1], 10) + 1;
  }
  return `ORD-${year}-${String(seq).padStart(6, "0")}`;
}

router.get("/api/orders", requireAuth, async (req: Request, res: Response) => {
  try {
    const page = Math.max(1, parseInt(req.query.page as string) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 20));
    const status = req.query.status as string;
    const paymentStatus = req.query.paymentStatus as string;
    const dateFrom = req.query.dateFrom as string;
    const dateTo = req.query.dateTo as string;
    const search = req.query.search as string;

    const where: Record<string, unknown> = {};
    if (status) where.status = status;
    if (paymentStatus) where.paymentStatus = paymentStatus;
    if (dateFrom || dateTo) {
      where.createdAt = {};
      if (dateFrom) (where.createdAt as Record<string, unknown>).gte = new Date(dateFrom);
      if (dateTo) (where.createdAt as Record<string, unknown>).lte = new Date(dateTo);
    }
    if (search) {
      where.OR = [
        { orderNumber: { contains: search } },
        { customerName: { contains: search } },
        { customerEmail: { contains: search } },
        { customerPhone: { contains: search } },
        { invoiceNumber: { contains: search } },
        { paymentId: { contains: search } },
      ];
    }

    if (req.user!.role === "CUSTOMER") {
      where.customerId = req.user!.userId;
    }

    const [orders, total] = await Promise.all([
      prisma.order.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { createdAt: "desc" },
        include: {
          service: { select: { id: true, name: true, slug: true } },
          customer: { select: { id: true, name: true, email: true } },
        },
      }),
      prisma.order.count({ where }),
    ]);

    const ordersWithQuotation = orders.map(o => ({ ...o, quotation: extractQuotation(o.formData) }));

    res.json({
      success: true,
      data: { orders: ordersWithQuotation, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } },
    });
  } catch (error) {
    console.error("List orders error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.get("/api/orders/:id", requireAuth, async (req: Request, res: Response) => {
  try {
    const order = await prisma.order.findUnique({
      where: { id: req.params.id },
      include: {
        service: { include: { category: true, pricing: true } },
        customer: { select: { id: true, name: true, email: true, phone: true } },
        invoices: true,
        refunds: true,
        orderNotes: { include: { author: { select: { id: true, name: true } } }, orderBy: { createdAt: "desc" } },
        assignments: { include: { staff: { select: { id: true, name: true, role: true } } } },
        orderTimeline: { orderBy: { createdAt: "asc" } },
        documentVersions: { include: { author: { select: { id: true, name: true } } }, orderBy: { version: "desc" } },
      },
    });
    if (!order) {
      res.status(404).json({ success: false, error: "Order not found" });
      return;
    }
    if (req.user!.role === "CUSTOMER" && order.customerId !== req.user!.userId) {
      res.status(403).json({ success: false, error: "Access denied" });
      return;
    }
    res.json({ success: true, data: { ...order, quotation: extractQuotation(order.formData) } });
  } catch (error) {
    console.error("Get order error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Public order tracking — no auth required
router.get("/api/track/:orderNumber", async (req: Request, res: Response) => {
  try {
    const order = await prisma.order.findFirst({
      where: { orderNumber: req.params.orderNumber },
      include: {
        service: { select: { name: true } },
        invoices: { select: { invoiceNumber: true, amount: true, status: true } },
        documents: { select: { documentNumber: true, documentType: true, pdfFilePath: true, status: true } },
        assignments: { include: { staff: { select: { name: true, phone: true } } }, take: 1 },
        orderTimeline: { orderBy: { createdAt: "desc" }, take: 1 },
      },
    });
    if (!order) {
      res.status(404).json({ success: false, error: "Order not found. Please check your Order ID." });
      return;
    }
    res.json({
      success: true,
      data: {
        orderNumber: order.orderNumber,
        customerName: order.customerName,
        customerPhone: order.customerPhone,
        customerEmail: order.customerEmail,
        service: order.service?.name,
        status: order.status,
        paymentStatus: order.paymentStatus,
        amount: order.total,
        createdAt: order.createdAt,
        assignedTo: order.assignments?.[0]?.staff?.name || null,
        invoice: order.invoices?.[0] || null,
        documents: order.documents || [],
        latestUpdate: order.orderTimeline?.[0]?.status || order.status,
      },
    });
  } catch (error) {
    console.error("Track order error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.post(
  "/api/admin/orders",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const data = createOrderSchema.parse(req.body);
      const orderNumber = await generateOrderNumber();
      const order = await prisma.order.create({
        data: {
          ...data,
          orderNumber,
          discount: data.discount ?? 0,
          tax: data.tax ?? 0,
          formData: JSON.stringify(data.formData),
        },
      });
      await logActionSync(req.user!.userId, "CREATE", "orders", order.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: order });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Create order error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/orders/:id/status",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const data = statusSchema.parse(req.body);
      const old = await prisma.order.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      const order = await prisma.order.update({ where: { id: req.params.id }, data: { status: data.status } });
      await prisma.orderTimeline.create({
        data: { orderId: req.params.id, status: data.status, note: `Status changed from ${old.status} to ${data.status}` },
      });
      await logActionSync(req.user!.userId, "UPDATE_STATUS", "orders", req.params.id, { status: old.status }, { status: data.status }, req.ip);
      res.json({ success: true, data: order });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update order status error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/orders/:id/payment",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const data = paymentSchema.parse(req.body);
      const old = await prisma.order.findUnique({ where: { id: req.params.id } });
      if (!old) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      const order = await prisma.order.update({ where: { id: req.params.id }, data });
      await logActionSync(req.user!.userId, "UPDATE_PAYMENT", "orders", req.params.id, { paymentStatus: old.paymentStatus }, { paymentStatus: data.paymentStatus }, req.ip);
      res.json({ success: true, data: order });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update payment error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/orders/:id/notes",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM", "SALES", "SUPPORT"),
  async (req: Request, res: Response) => {
    try {
      const data = noteSchema.parse(req.body);
      const order = await prisma.order.findUnique({ where: { id: req.params.id } });
      if (!order) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      const note = await prisma.orderNote.create({
        data: { orderId: req.params.id, note: data.note, authorId: req.user!.userId },
        include: { author: { select: { id: true, name: true } } },
      });
      res.status(201).json({ success: true, data: note });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Add note error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.get(
  "/api/admin/orders/:id/notes",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "LEGAL_TEAM", "DRAFTING_TEAM", "SALES", "SUPPORT", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const notes = await prisma.orderNote.findMany({
        where: { orderId: req.params.id },
        include: { author: { select: { id: true, name: true } } },
        orderBy: { createdAt: "desc" },
      });
      res.json({ success: true, data: notes });
    } catch (error) {
      console.error("Get notes error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/orders/:id/refund",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const data = refundSchema.parse(req.body);
      const order = await prisma.order.findUnique({ where: { id: req.params.id } });
      if (!order) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      if (order.paymentStatus !== "PAID") {
        res.status(400).json({ success: false, error: "Order payment must be PAID to process refund" });
        return;
      }
      const refund = await prisma.refund.create({
        data: {
          orderId: req.params.id,
          amount: data.amount,
          reason: data.reason,
          processedBy: req.user!.userId,
        },
      });
      await logActionSync(req.user!.userId, "REFUND", "orders", req.params.id, undefined, data as unknown as Record<string, unknown>, req.ip);
      res.status(201).json({ success: true, data: refund });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Process refund error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.post(
  "/api/admin/orders/:id/assign",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = assignSchema.parse(req.body);
      const order = await prisma.order.findUnique({ where: { id: req.params.id } });
      if (!order) {
        res.status(404).json({ success: false, error: "Order not found" });
        return;
      }
      const staff = await prisma.user.findUnique({ where: { id: data.staffId } });
      if (!staff) {
        res.status(404).json({ success: false, error: "Staff not found" });
        return;
      }
      const assignment = await prisma.orderAssignment.create({
        data: { orderId: req.params.id, staffId: data.staffId, role: data.role || "attorney" },
        include: { staff: { select: { id: true, name: true, role: true } } },
      });
      await logActionSync(req.user!.userId, "ASSIGN", "orders", req.params.id, undefined, { staffId: data.staffId, role: data.role }, req.ip);
      res.status(201).json({ success: true, data: assignment });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Assign order error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

export default router;
