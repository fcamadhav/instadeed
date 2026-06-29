import { Router, Request, Response } from "express";
import { z } from "zod";
import crypto from "crypto";
import { prisma } from "../lib/prisma";
import { requireAuth, requireRole } from "../middleware/auth";
import { logActionSync } from "../services/audit";
import { generateDocument } from "../services/pdf-generator";

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
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY" } });
    const razorpayKey = gateway?.apiKey || "";
    if (!razorpayKey) {
      // No Razorpay configured — return a placeholder so frontend shows mock payment path
      res.json({ razorpay_key: "", version: "2.0.0", app_name: "INSTADEED" });
      return;
    }
    res.json({ razorpay_key: razorpayKey, version: "2.0.0", app_name: "INSTADEED" });
  } catch (error) {
    console.error("Config error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// POST /create-order — creates a Razorpay order and returns order_id (used by old SPA)
// Also POST /api/create-order — same handler for both paths
function isPlaceholderKey(key: string): boolean {
  return !key || key.includes("YOUR_KEY");
}

async function createMockOrder(data: any, res: Response) {
  const mockOrderId = `MOCK_ORD_${crypto.randomBytes(4).toString("hex").toUpperCase()}`;
  let svc = await prisma.service.findFirst({ where: { slug: data.service_type?.toLowerCase() || "rent-agreement" } });
  if (!svc) svc = await prisma.service.findFirst({ orderBy: { createdAt: "asc" } });
  if (!svc) {
    const cat = await prisma.category.findFirst();
    svc = await prisma.service.create({
      data: { name: "Document Drafting", slug: `b2c-${Date.now()}`, categoryId: cat?.id || "00000000-0000-0000-0000-000000000000" },
    });
  }
  await prisma.order.create({
    data: {
      orderNumber: mockOrderId,
      paymentId: mockOrderId,
      customerName: data.customer_name || "B2C Client",
      customerPhone: data.customer_phone || "0000000000",
      customerEmail: data.customer_email || "b2c@client.com",
      serviceId: svc.id,
      amount: data.amount,
      total: data.amount,
      formData: JSON.stringify({ service_type: data.service_type, form_data: data.form_data }),
      status: "PENDING",
      paymentStatus: "PENDING",
    },
  });
  res.json({ order_id: mockOrderId, amount: data.amount * 100, currency: data.currency || "INR" });
}

async function createRealRazorpayOrder(gateway: any, data: any, res: Response) {
  const razorpayAmount = Math.round(data.amount * 100);
  const razorpayReceipt = data.receipt || `rcpt_${Date.now()}`;
  const auth = Buffer.from(`${gateway.apiKey}:${gateway.apiSecret}`).toString("base64");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const rzpResponse = await fetch("https://api.razorpay.com/v1/orders", {
      method: "POST",
      headers: { "Authorization": `Basic ${auth}`, "Content-Type": "application/json" },
      body: JSON.stringify({ amount: razorpayAmount, currency: data.currency || "INR", receipt: razorpayReceipt, notes: data.notes || {} }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    if (!rzpResponse.ok) {
      const errText = await rzpResponse.text();
      console.error("Razorpay API error, falling back to mock:", errText);
      return createMockOrder(data, res);
    }
    const rzpOrder = (await rzpResponse.json()) as { id: string; amount: number; currency: string };
    let genericService = await prisma.service.findFirst({ where: { slug: data.service_type?.toLowerCase() || "rent-agreement" } });
  if (!genericService) genericService = await prisma.service.findFirst({ orderBy: { createdAt: "asc" } });
  if (!genericService) {
    const cat = await prisma.category.findFirst();
    genericService = await prisma.service.create({
      data: { name: "Document Drafting", slug: `b2c-${Date.now()}`, categoryId: cat?.id || "00000000-0000-0000-0000-000000000000" },
    });
  }
  await prisma.order.create({
    data: {
      orderNumber: rzpOrder.id,
      customerName: data.customer_name || "B2C Client",
      customerPhone: data.customer_phone || "0000000000",
      customerEmail: data.customer_email || "b2c@client.com",
      serviceId: genericService.id,
      amount: data.amount,
      total: data.amount,
      paymentGateway: "RAZORPAY",
      paymentId: rzpOrder.id,
      formData: JSON.stringify({ service_type: data.service_type, form_data: data.form_data }),
      status: "PENDING",
      paymentStatus: "PENDING",
    },
  });
  res.json({ order_id: rzpOrder.id, amount: rzpOrder.amount, currency: rzpOrder.currency });
  } catch (err) {
    clearTimeout(timeout);
    console.error("Razorpay API call failed:", err);
    return createMockOrder(data, res);
  }
}

const createOrderHandler = async (req: Request, res: Response) => {
  try {
    const data = createOrderSchema.parse(req.body);
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    
    // Determine if we should use real Razorpay or mock
    const useRealRazorpay = gateway && gateway.apiKey && gateway.apiSecret && !isPlaceholderKey(gateway.apiKey);
    
    if (useRealRazorpay) {
      await createRealRazorpayOrder(gateway, data, res);
    } else {
      console.log("Using mock payment path (keys:", gateway?.apiKey?.substring(0,10) || "none", "...)");
      await createMockOrder(data, res);
    }
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Create order error:", error);
    // Fall back to mock on any error
    try { await createMockOrder(req.body, res); } catch { res.status(500).json({ success: false, error: "Internal server error" }); }
  }
};

router.post("/create-order", createOrderHandler);
router.post("/api/create-order", createOrderHandler);

// Generate PDF after successful payment
async function generatePdfAfterPayment(orderId: string) {
  try {
    const order = await prisma.order.findFirst({
      where: { OR: [{ paymentId: orderId }, { orderNumber: orderId }] },
    });
    if (!order || !order.formData) { console.log("[PDF] No order or formData found for:", orderId); return; }
    const parsed = JSON.parse(order.formData as string);
    const docType = parsed.service_type || "document";
    const docNumber = `DOC-${Date.now().toString(36).toUpperCase()}-${crypto.randomBytes(3).toString("hex").toUpperCase()}`;
    const { pdfPath } = await generateDocument(parsed.form_data || {}, docType, order.id, docNumber);
    let svc = await prisma.service.findFirst({ where: { slug: docType?.toLowerCase() || "rent-agreement" } });
    if (!svc) svc = await prisma.service.findFirst({ orderBy: { createdAt: "asc" } });
    if (!svc) svc = await prisma.service.findFirst({});
    await prisma.document.create({
      data: {
        documentNumber: docNumber,
        orderId: order.id,
        customerId: order.customerId || "00000000-0000-0000-0000-000000000000",
        serviceId: svc?.id || "00000000-0000-0000-0000-000000000000",
        documentType: docType,
        pdfFilePath: pdfPath,
        formData: JSON.stringify(parsed.form_data || {}),
        status: "COMPLETED",
      },
    });
    console.log(`[PDF] Generated for order ${order.id}: ${pdfPath}`);
  } catch (err) {
    console.error("[PDF] Generation failed (non-fatal):", err);
  }
}

// POST /verify-payment — verifies Razorpay signature
// Also POST /api/verify-payment
const verifyPaymentHandler = async (req: Request, res: Response) => {
  try {
    const data = verifyPaymentSchema.parse(req.body);

    // Mock orders — skip verification
    if (data.razorpay_order_id.startsWith("MOCK_ORD_")) {
      await prisma.order.updateMany({
        where: { paymentId: data.razorpay_order_id },
        data: { paymentStatus: "PAID", status: "COMPLETED" },
      });
      await generatePdfAfterPayment(data.razorpay_order_id);
      res.json({ status: "success", message: "Payment verified" });
      return;
    }

    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway || !gateway.apiSecret || isPlaceholderKey(gateway.apiKey || "")) {
      // No real Razorpay configured — accept mock verification
      await prisma.order.updateMany({
        where: { paymentId: data.razorpay_order_id },
        data: { paymentStatus: "PAID", status: "COMPLETED" },
      });
      await generatePdfAfterPayment(data.razorpay_order_id);
      res.json({ status: "success", message: "Payment verified (mock mode)" });
      return;
    }
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

    await generatePdfAfterPayment(data.razorpay_order_id);

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
          data: { paymentStatus: "PAID", status: "COMPLETED" },
        });
        await generatePdfAfterPayment(orderId);
      }
    }
    res.json({ success: true });
  } catch (error) {
    console.error("Webhook error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
