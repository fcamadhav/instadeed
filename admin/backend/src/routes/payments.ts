import { Router, Request, Response } from "express";
import { z } from "zod";
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

router.post("/api/create-order", async (req: Request, res: Response) => {
  try {
    const data = createOrderSchema.parse(req.body);
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway) {
      res.status(503).json({ success: false, error: "Payment gateway not configured" });
      return;
    }
    res.json({
      success: true,
      data: {
        amount: data.amount * 100,
        currency: data.currency,
        receipt: data.receipt || `rcpt_${Date.now()}`,
        key: gateway.apiKey,
        gatewayId: gateway.id,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Create payment order error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.post("/api/verify-payment", async (req: Request, res: Response) => {
  try {
    const data = verifyPaymentSchema.parse(req.body);
    const crypto = require("crypto");
    const gateway = await prisma.paymentGatewayConfig.findFirst({ where: { gateway: "RAZORPAY", isEnabled: true } });
    if (!gateway) {
      res.status(503).json({ success: false, error: "Payment gateway not configured" });
      return;
    }
    const generatedSignature = crypto
      .createHmac("sha256", gateway.apiSecret || "")
      .update(`${data.razorpay_order_id}|${data.razorpay_payment_id}`)
      .digest("hex");

    if (generatedSignature !== data.razorpay_signature) {
      res.status(400).json({ success: false, error: "Invalid payment signature" });
      return;
    }

    res.json({ success: true, data: { verified: true, message: "Payment verified successfully" } });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Verify payment error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
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
    const crypto = require("crypto");
    const expectedSig = crypto.createHmac("sha256", gateway.webhookSecret).update(JSON.stringify(req.body)).digest("hex");
    if (signature !== expectedSig) {
      res.status(400).json({ success: false, error: "Invalid webhook signature" });
      return;
    }
    const event = req.body.event;
    if (event === "payment.captured" || event === "order.paid") {
      const orderId = req.body.payload?.order?.entity?.id || req.body.payload?.payment?.entity?.order_id;
      if (orderId) {
        await prisma.order.update({
          where: { orderNumber: orderId },
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
