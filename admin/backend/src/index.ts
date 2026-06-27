import express, { Request, Response, NextFunction } from "express";
import helmet from "helmet";
import cors from "cors";
import morgan from "morgan";
import rateLimit from "express-rate-limit";

import authRoutes from "./routes/auth";
import userRoutes from "./routes/users";
import serviceRoutes from "./routes/services";
import categoryRoutes from "./routes/categories";
import pricingRoutes from "./routes/pricing";
import orderRoutes from "./routes/orders";
import customerRoutes from "./routes/customers";
import paymentRoutes from "./routes/payments";
import couponRoutes from "./routes/coupons";
import gstRoutes from "./routes/gst";
import notificationRoutes from "./routes/notifications";
import aiRoutes from "./routes/ai";
import workflowRoutes from "./routes/workflow";
import websiteRoutes from "./routes/website";
import settingsRoutes from "./routes/settings";
import analyticsRoutes from "./routes/analytics";
import auditRoutes from "./routes/audit";
import dashboardRoutes from "./routes/dashboard";
import documentRoutes from "./routes/documents";
import rentAgreementRoutes from "./routes/rent-agreements";

const app = express();
const PORT = parseInt(process.env.PORT || "4000", 10);

app.use(helmet());
app.use(cors());
app.use(morgan("combined"));
app.use(express.json({ limit: "10mb" }));

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 1000,
  message: { success: false, error: "Too many requests, please try again later" },
});
app.use(globalLimiter);

app.use(authRoutes);
app.use(userRoutes);
app.use(serviceRoutes);
app.use(categoryRoutes);
app.use(pricingRoutes);
app.use(orderRoutes);
app.use(customerRoutes);
app.use(paymentRoutes);
app.use(couponRoutes);
app.use(gstRoutes);
app.use(notificationRoutes);
app.use(aiRoutes);
app.use(workflowRoutes);
app.use(websiteRoutes);
app.use(settingsRoutes);
app.use(analyticsRoutes);
app.use(auditRoutes);
app.use(dashboardRoutes);
app.use(documentRoutes);
app.use(rentAgreementRoutes);

app.get("/api/health", (_req: Request, res: Response) => {
  res.json({ success: true, data: { status: "ok", timestamp: new Date().toISOString() } });
});

app.use((_req: Request, res: Response) => {
  res.status(404).json({ success: false, error: "Route not found" });
});

app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ success: false, error: process.env.NODE_ENV === "production" ? "Internal server error" : err.message });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
