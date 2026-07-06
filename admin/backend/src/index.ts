import express, { Request, Response, NextFunction } from "express";
import helmet from "helmet";
import cors from "cors";
import morgan from "morgan";
import rateLimit from "express-rate-limit";
import path from "path";
import fs from "fs";

import authRoutes from "./routes/auth";
import { prisma } from "./lib/prisma";
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
import documentsManagementRoutes from "./routes/documents-management";
import applicationDocumentsRoutes from "./routes/application-documents";
import searchRoutes from "./routes/search";

const app = express();
const PORT = parseInt(process.env.PORT || "4000", 10);

app.use(helmet());
app.use(cors());
app.use(morgan("combined"));
app.use(express.json({ limit: "10mb" }));

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 300,
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
app.use(documentsManagementRoutes);
app.use(applicationDocumentsRoutes);
app.use(searchRoutes);

app.get("/api/health", async (_req: Request, res: Response) => {
  let dbOk = false;
  try { await prisma.$queryRaw`SELECT 1`; dbOk = true; } catch {}
  res.json({
    success: true,
    data: {
      status: "ok",
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      database: dbOk ? "connected" : "error",
    },
  });
});

// Serve the old Madhav_Drafting_Hub.html SPA internally (no ?doc= exposure in browser URL)
// Try multiple possible locations for the SPA file
const DRAFT_SPA_CANDIDATES = [
  path.resolve(__dirname, "..", "..", "..", "..", "Madhav_Drafting_Hub.html"),  // host project root
  path.resolve("/app", "Madhav_Drafting_Hub.html"),                              // Docker volume mount
  path.resolve(__dirname, "..", "..", "Madhav_Drafting_Hub.html"),              // alt nesting
];
let DRAFT_SPA_PATH = "";
for (const p of DRAFT_SPA_CANDIDATES) {
  if (fs.existsSync(p)) { DRAFT_SPA_PATH = p; break; }
}
app.get("/api/draft-serve", (req: Request, res: Response) => {
  const rawDoc = typeof req.query.doc === "string" ? req.query.doc : "";
  const allowedDocs = new Set([
    "rent-agreement",
    "leave-and-license",
    "affidavit",
    "notarized-affidavit",
    "power-of-attorney",
  ]);
  const doc = allowedDocs.has(rawDoc) ? rawDoc : "rent-agreement";
  if (!fs.existsSync(DRAFT_SPA_PATH)) {
    res.status(404).json({ success: false, error: "Draft SPA not found" });
    return;
  }
  let html = fs.readFileSync(DRAFT_SPA_PATH, "utf-8");
  // Inject a script that selects the document without URL params
  const injectedScript = `<script>window.DOC_TYPE=${JSON.stringify(doc)};document.addEventListener('DOMContentLoaded',function(){const p=new URLSearchParams(window.location.search);if(!p.get('doc')){const u=new URL(window.location.href);u.searchParams.set('doc',window.DOC_TYPE);window.history.replaceState({},'',u.toString());}});</script>`;
  html = html.replace("</head>", `${injectedScript}</head>`);
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  // Override CSP to allow the old SPA's inline scripts and CDN resources
  res.setHeader("Content-Security-Policy", "default-src 'self' 'unsafe-inline' 'unsafe-eval'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdnjs.cloudflare.com https://accounts.google.com https://cdn.tailwindcss.com https://checkout.razorpay.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com https://cdn.tailwindcss.com; font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://*.razorpay.com https://api.razorpay.com; frame-ancestors 'self'");
  res.send(html);
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
