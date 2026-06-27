import { Router, Request, Response } from "express";
import { z } from "zod";
import crypto from "crypto";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";

const router = Router();

const gatewaySchema = z.object({
  isEnabled: z.boolean().optional(),
  isTestMode: z.boolean().optional(),
  isDefault: z.boolean().optional(),
  apiKey: z.string().optional(),
  apiSecret: z.string().optional(),
  webhookSecret: z.string().optional(),
  successUrl: z.string().optional(),
  failureUrl: z.string().optional(),
  paymentTimeout: z.number().int().positive().optional(),
  sortOrder: z.number().int().optional(),
});

const createOrderSchema = z.object({
  amount: z.number().positive(),
  currency: z.string().default("INR"),
  receipt: z.string().optional(),
  notes: z.record(z.string()).optional(),
  service_type: z.string().optional(),
  customer_name: z.string().optional(),
  customer_phone: z.string().optional(),
  customer_email: z.string().optional(),
  form_data: z.any().optional(),
});

const verifyPaymentSchema = z.object({
  razorpay_order_id: z.string(),
  razorpay_payment_id: z.string(),
  razorpay_signature: z.string(),
});

router.get(
  "/api/admin/payment-gateways",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN", "ACCOUNTS"),
  async (req: Request, res: Response) => {
    try {
      const gateways = await prisma.paymentGatewayConfig.findMany({
        orderBy: { sortOrder: "asc" },
      });
      const sanitized = gateways.map((g) => ({
        ...g,
        apiSecret: g.apiSecret ? "[ENCRYPTED]" : null,
        webhookSecret: g.webhookSecret ? "[ENCRYPTED]" : null,
      }));
      res.json({ success: true, data: sanitized });
    } catch (error) {
      console.error("List gateways error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

router.put(
  "/api/admin/payment-gateways/:gateway",
  requireAuth,
  requireRole("SUPER_ADMIN", "ADMIN"),
  async (req: Request, res: Response) => {
    try {
      const data = gatewaySchema.parse(req.body);
      const gateway = req.params.gateway.toUpperCase();
      const old = await prisma.paymentGatewayConfig.findUnique({ where: { gateway: gateway as never } });

      let config;
      if (old) {
        config = await prisma.paymentGatewayConfig.update({ where: { gateway: gateway as never }, data });
      } else {
        config = await prisma.paymentGatewayConfig.create({ data: { gateway: gateway as never, ...data } });
      }

      await logActionSync(req.user!.userId, "UPDATE", "payment_gateways", gateway, old as unknown as Record<string, unknown> || undefined, data as unknown as Record<string, unknown>, req.ip);
      res.json({ success: true, data: { ...config, apiSecret: config.apiSecret ? "[ENCRYPTED]" : null } });
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ success: false, error: error.errors });
        return;
      }
      console.error("Update gateway error:", error);
      res.status(500).json({ success: false, error: "Internal server error" });
    }
  }
);

// ============ PUBLIC PAYMENT ENDPOINTS (used by the old SPA at /app/) ============

// GET /api/config — returns Razorpay public key for frontend
router.get("/api/config", async (_req: Request, res: Response) => {
  try {
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway || !gateway.apiKey) {
      res.status(503).json({ success: false, error: "Payment gateway not configured" });
      return;
    }
    res.json({ razorpay_key: gateway.apiKey, version: "2.0.0", app_name: "INSTADEED" });
  } catch (error) {
    console.error("Config error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// POST /create-order — creates a Razorpay order and returns order_id (used by old SPA)
// Also POST /api/create-order — same handler for both paths
const createOrderHandler = async (req: Request, res: Response) => {
  try {
    const data = createOrderSchema.parse(req.body);
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway || !gateway.apiKey || !gateway.apiSecret) {
      // No Razorpay configured — return mock order (same as old Python server behavior)
      const mockOrderId = `MOCK_ORD_${crypto.randomBytes(4).toString("hex").toUpperCase()}`;
      // Also save to our orders table
      const orderNumber = `ORD-${Date.now().toString(36).toUpperCase()}-${crypto.randomBytes(2).toString("hex").toUpperCase()}`;
      await prisma.order.create({
        data: {
          orderNumber,
          customerName: data.customer_name || "B2C Client",
          customerPhone: data.customer_phone || "0000000000",
          customerEmail: data.customer_email || "b2c@client.com",
          serviceId: "00000000-0000-0000-0000-000000000001", // generic
          amount: data.amount,
          total: data.amount,
          formData: JSON.stringify({ service_type: data.service_type, form_data: data.form_data }),
          status: "PENDING",
          paymentStatus: "PENDING",
        },
      });
      res.json({ order_id: mockOrderId, amount: data.amount * 100, currency: data.currency || "INR" });
      return;
    }

    // Call Razorpay API to create a real order
    const razorpayAmount = Math.round(data.amount * 100); // Convert to paise
    const razorpayReceipt = data.receipt || `rcpt_${Date.now()}`;
    
    const auth = Buffer.from(`${gateway.apiKey}:${gateway.apiSecret}`).toString("base64");
    const rzpResponse = await fetch("https://api.razorpay.com/v1/orders", {
      method: "POST",
      headers: {
        "Authorization": `Basic ${auth}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        amount: razorpayAmount,
        currency: data.currency || "INR",
        receipt: razorpayReceipt,
        notes: data.notes || {},
      }),
    });

    if (!rzpResponse.ok) {
      const errText = await rzpResponse.text();
      console.error("Razorpay order creation failed:", errText);
      res.status(502).json({ success: false, error: "Payment gateway error" });
      return;
    }

    const rzpOrder = (await rzpResponse.json()) as { id: string; amount: number; currency: string };

    // Save order to our database
    const orderNumber = `ORD-${Date.now().toString(36).toUpperCase()}-${crypto.randomBytes(2).toString("hex").toUpperCase()}`;
    await prisma.order.create({
      data: {
        orderNumber: rzpOrder.id,
        customerName: data.customer_name || "B2C Client",
        customerPhone: data.customer_phone || "0000000000",
        customerEmail: data.customer_email || "b2c@client.com",
        serviceId: "00000000-0000-0000-0000-000000000001",
        amount: data.amount,
        total: data.amount,
        paymentGateway: "RAZORPAY",
        paymentId: rzpOrder.id,
        formData: JSON.stringify({ service_type: data.service_type, form_data: data.form_data }),
        status: "PENDING",
        paymentStatus: "PENDING",
      },
    });

    res.json({
      order_id: rzpOrder.id,
      amount: rzpOrder.amount,
      currency: rzpOrder.currency,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Create order error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
};

router.post("/create-order", createOrderHandler);
router.post("/api/create-order", createOrderHandler);

// POST /verify-payment — verifies Razorpay signature
// Also POST /api/verify-payment
const verifyPaymentHandler = async (req: Request, res: Response) => {
  try {
    const data = verifyPaymentSchema.parse(req.body);

    // Mock orders — skip verification
    if (data.razorpay_order_id.startsWith("MOCK_ORD_")) {
      // Update order status
      await prisma.order.updateMany({
        where: { paymentId: data.razorpay_order_id },
        data: { paymentStatus: "PAID", status: "COMPLETED" },
      });
      res.json({ status: "success", message: "Payment verified" });
      return;
    }

    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway || !gateway.apiSecret) {
      res.status(503).json({ success: false, error: "Payment gateway not configured" });
      return;
    }

    const generatedSignature = crypto
      .createHmac("sha256", gateway.apiSecret)
      .update(`${data.razorpay_order_id}|${data.razorpay_payment_id}`)
      .digest("hex");

    if (generatedSignature !== data.razorpay_signature) {
      res.status(400).json({ success: false, error: "Invalid payment signature" });
      return;
    }

    // Update order status
    await prisma.order.updateMany({
      where: { paymentId: data.razorpay_order_id },
      data: { paymentStatus: "PAID", status: "COMPLETED" },
    });

    res.json({ status: "success", message: "Payment verified successfully" });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Verify payment error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
};

router.post("/verify-payment", verifyPaymentHandler);
router.post("/api/verify-payment", verifyPaymentHandler);

// POST /api/track — simple event tracking (used by old SPA)
router.post("/api/track", async (req: Request, res: Response) => {
  try {
    const body = req.body;
    // Just log and return success — no elaborate tracking needed
    if (body.event === "payment_initiated" || body.event === "payment_complete") {
      console.log(`[TRACK] ${body.event} | doc: ${body.page} | order: ${body.detail || ""}`);
    }
    res.json({ ok: true });
  } catch {
    res.json({ ok: true }); // Swallow errors — tracking is non-critical
  }
});

router.post("/api/admin/payments/webhook", async (req: Request, res: Response) => {
  try {
    const signature = req.headers["x-razorpay-signature"] as string;
    if (!signature) {
      res.status(400).json({ success: false, error: "Missing webhook signature" });
      return;
    }
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway || !gateway.webhookSecret) {
      res.status(503).json({ success: false, error: "Payment gateway webhook not configured" });
      return;
    }
    const expectedSig = crypto.createHmac("sha256", gateway.webhookSecret).update(JSON.stringify(req.body)).digest("hex");
    if (signature !== expectedSig) {
      res.status(400).json({ success: false, error: "Invalid webhook signature" });
      return;
    }
    const event = req.body.event;
    if (event === "payment.captured" || event === "order.paid") {
      const orderId = req.body.payload?.order?.entity?.id || req.body.payload?.payment?.entity?.order_id;
      if (orderId) {
        await prisma.order.updateMany({
          where: { paymentId: orderId },
          data: { paymentStatus: "PAID", status: "COMPLETED", paymentId: req.body.payload?.payment?.entity?.id },
        });
      }
    }
    res.json({ success: true });
  } catch (error) {
    console.error("Webhook error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
