import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

async function main() {
  console.log("🌱 Seeding database...");

  // ─── Super Admin ───
  const adminEmail = "admin@instadeed.local";
  const existingAdmin = await prisma.user.findUnique({
    where: { email: adminEmail },
  });

  if (!existingAdmin) {
    const adminPass = process.env.ADMIN_SEED_PASSWORD || process.env.ADMIN_PASSWORD || "admin123";
    const passwordHash = await bcrypt.hash(adminPass, 12);
    await prisma.user.create({
      data: {
        email: adminEmail,
        passwordHash,
        name: "Super Admin",
        phone: "+91-9999999999",
        role: "SUPER_ADMIN",
        isActive: true,
      },
    });
    if (!process.env.ADMIN_SEED_PASSWORD && !process.env.ADMIN_PASSWORD) {
      console.log("  ⚠ Super admin created with default password. Set ADMIN_SEED_PASSWORD env var in production.");
    } else {
      console.log("  ✔ Super admin created");
    }
  } else {
    console.log("  – Super admin already exists, skipping");
  }

  // ─── Categories ───
  const categoryData = [
    { name: "IPR", description: "Intellectual Property Rights services including trademarks, copyrights, and patents", icon: "shield", displayOrder: 1 },
    { name: "Property", description: "Property-related legal documentation and registration services", icon: "home", displayOrder: 2 },
    { name: "Tax", description: "Tax registration, filing, and compliance services", icon: "calculator", displayOrder: 3 },
    { name: "Corporate", description: "Business registration and corporate compliance services", icon: "building", displayOrder: 4 },
    { name: "Documentation", description: "Legal document drafting and notary services", icon: "file-text", displayOrder: 5 },
    { name: "Compliance", description: "Regulatory compliance and verification services", icon: "check-circle", displayOrder: 6 },
    { name: "Property Documents", description: "GNIDA-approved property document drafting services", icon: "file-text", displayOrder: 7 },
  ];

  const categories: Record<string, string> = {};
  for (const cat of categoryData) {
    const slug = slugify(cat.name);
    const existing = await prisma.category.findUnique({ where: { slug } });
    if (!existing) {
      const created = await prisma.category.create({
        data: { ...cat, slug },
      });
      categories[cat.name] = created.id;
      console.log(`  ✔ Category created: ${cat.name}`);
    } else {
      categories[cat.name] = existing.id;
      console.log(`  – Category already exists: ${cat.name}`);
    }
  }

  // ─── Services & Pricing ───
  interface ServiceSeed {
    name: string;
    category: string;
    shortDescription: string;
    deliveryTime: string;
    processingTime: string;
    sortOrder: number;
    isFeatured: boolean;
    currentPrice: number;
    oldPrice: number | null;
    gstPercent: number;
    offerBadge?: string;
  }

  const serviceData: ServiceSeed[] = [
    { name: "Trademark Filing", category: "IPR", shortDescription: "Register your trademark to protect your brand identity", deliveryTime: "3-4 months", processingTime: "5-7 working days", sortOrder: 1, isFeatured: true, currentPrice: 3499, oldPrice: 4999, gstPercent: 18, offerBadge: "30% OFF" },
    { name: "Copyright Registration", category: "IPR", shortDescription: "Protect your original creative works with copyright", deliveryTime: "2-3 months", processingTime: "3-5 working days", sortOrder: 2, isFeatured: false, currentPrice: 2499, oldPrice: 3500, gstPercent: 18 },
    { name: "Patent Filing", category: "IPR", shortDescription: "File provisional or complete patent for your invention", deliveryTime: "12-18 months", processingTime: "7-10 working days", sortOrder: 3, isFeatured: false, currentPrice: 14999, oldPrice: 19999, gstPercent: 18, offerBadge: "25% OFF" },
    { name: "Design Registration", category: "IPR", shortDescription: "Register industrial design to protect visual appeal", deliveryTime: "4-6 months", processingTime: "5-7 working days", sortOrder: 4, isFeatured: false, currentPrice: 3999, oldPrice: 5500, gstPercent: 18 },
    { name: "Rent Agreement", category: "Property", shortDescription: "Legally valid rent agreement drafting and registration", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 1, isFeatured: true, currentPrice: 999, oldPrice: 1499, gstPercent: 18, offerBadge: "33% OFF" },
    { name: "Gift Deed", category: "Property", shortDescription: "Draft and register gift deed for property transfer", deliveryTime: "5-7 working days", processingTime: "2-3 working days", sortOrder: 2, isFeatured: false, currentPrice: 2999, oldPrice: 4500, gstPercent: 18 },
    { name: "Sale Deed", category: "Property", shortDescription: "Comprehensive sale deed drafting for property transactions", deliveryTime: "7-10 working days", processingTime: "3-5 working days", sortOrder: 3, isFeatured: true, currentPrice: 4999, oldPrice: 7500, gstPercent: 18, offerBadge: "33% OFF" },
    { name: "Lease Deed", category: "Property", shortDescription: "Commercial and residential lease deed documentation", deliveryTime: "5-7 working days", processingTime: "2-3 working days", sortOrder: 4, isFeatured: false, currentPrice: 1999, oldPrice: 3000, gstPercent: 18 },
    { name: "GST Registration", category: "Tax", shortDescription: "Get your business registered under GST", deliveryTime: "5-7 working days", processingTime: "24 hours", sortOrder: 1, isFeatured: true, currentPrice: 599, oldPrice: 999, gstPercent: 18, offerBadge: "40% OFF" },
    { name: "Income Tax Filing", category: "Tax", shortDescription: "File your income tax returns with expert assistance", deliveryTime: "3-5 working days", processingTime: "24 hours", sortOrder: 2, isFeatured: false, currentPrice: 1499, oldPrice: 2499, gstPercent: 18 },
    { name: "TDS Filing", category: "Tax", shortDescription: "TDS return filing and compliance services", deliveryTime: "3-5 working days", processingTime: "24 hours", sortOrder: 3, isFeatured: false, currentPrice: 999, oldPrice: 1500, gstPercent: 18 },
    { name: "Company Registration", category: "Corporate", shortDescription: "Register your private limited company online", deliveryTime: "10-15 working days", processingTime: "3-5 working days", sortOrder: 1, isFeatured: true, currentPrice: 7999, oldPrice: 12999, gstPercent: 18, offerBadge: "38% OFF" },
    { name: "LLP Registration", category: "Corporate", shortDescription: "Limited Liability Partnership registration services", deliveryTime: "7-10 working days", processingTime: "2-3 working days", sortOrder: 2, isFeatured: false, currentPrice: 4999, oldPrice: 7999, gstPercent: 18 },
    { name: "Partnership Registration", category: "Corporate", shortDescription: "Register your partnership firm with ease", deliveryTime: "5-7 working days", processingTime: "2-3 working days", sortOrder: 3, isFeatured: false, currentPrice: 2999, oldPrice: 4500, gstPercent: 18 },
    { name: "Legal Notice", category: "Documentation", shortDescription: "Draft and send professional legal notices", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 1, isFeatured: true, currentPrice: 1499, oldPrice: 2499, gstPercent: 18, offerBadge: "40% OFF" },
    { name: "Affidavit", category: "Documentation", shortDescription: "Notarized affidavit drafting and execution", deliveryTime: "24 hours", processingTime: "4-6 hours", sortOrder: 2, isFeatured: false, currentPrice: 499, oldPrice: 999, gstPercent: 18 },
    { name: "Power of Attorney", category: "Documentation", shortDescription: "General and special power of attorney drafting", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 3, isFeatured: false, currentPrice: 1999, oldPrice: 2999, gstPercent: 18 },
    { name: "Police Verification", category: "Compliance", shortDescription: "Police verification certificate for various purposes", deliveryTime: "7-10 working days", processingTime: "2-3 working days", sortOrder: 1, isFeatured: false, currentPrice: 499, oldPrice: 999, gstPercent: 18, offerBadge: "50% OFF" },
    { name: "FSSAI License", category: "Compliance", shortDescription: "Food Safety and Standards Authority of India license", deliveryTime: "10-15 working days", processingTime: "3-5 working days", sortOrder: 2, isFeatured: false, currentPrice: 2999, oldPrice: 4499, gstPercent: 18 },
    { name: "MSME Registration", category: "Compliance", shortDescription: "Udyam registration for micro, small & medium enterprises", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 3, isFeatured: false, currentPrice: 499, oldPrice: 999, gstPercent: 18 },

    // ─── Property Document Services (used by the drafting SPA) ───
    { name: "Registered Rent Agreement", category: "Property Documents", shortDescription: "Notarized and registered rental agreement with full legal validity", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 5, isFeatured: false, currentPrice: 2000, oldPrice: 3500, gstPercent: 18 },
    { name: "Agreement to Sell / ATS", category: "Property Documents", shortDescription: "Legally enforceable promise to sell a property between buyer and seller", deliveryTime: "2-3 working days", processingTime: "24 hours", sortOrder: 6, isFeatured: false, currentPrice: 150, oldPrice: 500, gstPercent: 18 },
    { name: "Transfer Memorandum / TM", category: "Property Documents", shortDescription: "Official document recording the transfer of property ownership rights (TM-48)", deliveryTime: "3-5 working days", processingTime: "24 hours", sortOrder: 7, isFeatured: false, currentPrice: 2000, oldPrice: 3500, gstPercent: 18 },
    { name: "GNIDA Registry Deed", category: "Property Documents", shortDescription: "Full property sale deed registration with sub-registrar office", deliveryTime: "5-7 working days", processingTime: "2-3 working days", sortOrder: 8, isFeatured: false, currentPrice: 10000, oldPrice: 15000, gstPercent: 18 },
    { name: "Permission to Mortgage / PTM", category: "Property Documents", shortDescription: "Authority permission document for mortgaging a property against a loan", deliveryTime: "5-7 working days", processingTime: "2-3 working days", sortOrder: 9, isFeatured: false, currentPrice: 7500, oldPrice: 12000, gstPercent: 18 },
    { name: "Mutation", category: "Property Documents", shortDescription: "Updating property title records with the local municipal authority", deliveryTime: "7-10 working days", processingTime: "3-5 working days", sortOrder: 10, isFeatured: false, currentPrice: 3500, oldPrice: 5000, gstPercent: 18 },
    { name: "GNIDA 5-in-1 Package", category: "Property Documents", shortDescription: "Complete GNIDA document package: Registry, PTM, Mutation, ATS & Transfer Deed", deliveryTime: "7-10 working days", processingTime: "3-5 working days", sortOrder: 11, isFeatured: true, currentPrice: 40000, oldPrice: 55000, gstPercent: 18, offerBadge: "27% OFF" },
    { name: "Know Your Allottee (KYA)", category: "Property Documents", shortDescription: "Greater Noida Authority official allottee verification datasheet", deliveryTime: "24 hours", processingTime: "1-2 hours", sortOrder: 12, isFeatured: false, currentPrice: 0, oldPrice: null, gstPercent: 0 },
    { name: "Transfer Memo Application", category: "Property Documents", shortDescription: "Application for transfer of leasehold rights under GNIDA authority rules", deliveryTime: "3-5 working days", processingTime: "24 hours", sortOrder: 13, isFeatured: false, currentPrice: 2000, oldPrice: 3000, gstPercent: 18 },
    { name: "Noida Transfer Application", category: "Property Documents", shortDescription: "Transfer of leasehold rights under Noida Authority rules", deliveryTime: "3-5 working days", processingTime: "24 hours", sortOrder: 14, isFeatured: false, currentPrice: 2000, oldPrice: 3000, gstPercent: 18 },
    { name: "TM-48 Trademark Proxy", category: "Property Documents", shortDescription: "Official authorisation form to represent clients before the Indian Trademark Registry", deliveryTime: "24 hours", processingTime: "1-2 hours", sortOrder: 15, isFeatured: false, currentPrice: 500, oldPrice: 1000, gstPercent: 18 },
  ];

  for (const svc of serviceData) {
    const slug = slugify(svc.name);
    const existing = await prisma.service.findUnique({ where: { slug } });
    if (!existing) {
      const service = await prisma.service.create({
        data: {
          name: svc.name,
          slug,
          categoryId: categories[svc.category],
          shortDescription: svc.shortDescription,
          longDescription: `${svc.shortDescription}. Our expert team handles the entire process end-to-end with real-time status updates.`,
          deliveryTime: svc.deliveryTime,
          processingTime: svc.processingTime,
          sortOrder: svc.sortOrder,
          isFeatured: svc.isFeatured,
          showOnHomepage: true,
          status: "ACTIVE",
        },
      });

      const discountPercent = svc.oldPrice
        ? Math.round(((svc.oldPrice - svc.currentPrice) / svc.oldPrice) * 100)
        : null;
      const discountAmount = svc.oldPrice ? svc.oldPrice - svc.currentPrice : null;

      await prisma.pricing.create({
        data: {
          serviceId: service.id,
          currentPrice: svc.currentPrice,
          oldPrice: svc.oldPrice,
          discountPercent,
          discountAmount,
          gstPercent: svc.gstPercent,
          convenienceFee: 0,
          processingFee: 0,
          deliveryCharge: 0,
          currency: "INR",
          emiAvailable: svc.currentPrice >= 5000,
          offerBadge: svc.offerBadge || null,
          isLimitedOffer: !!svc.offerBadge,
        },
      });

      await prisma.pricingHistory.create({
        data: {
          pricingId: (await prisma.pricing.findUnique({ where: { serviceId: service.id } }))!.id,
          currentPrice: svc.currentPrice,
          oldPrice: svc.oldPrice,
          discountPercent,
          gstPercent: svc.gstPercent,
        },
      });

      console.log(`  ✔ Service created: ${svc.name}`);
    } else {
      console.log(`  – Service already exists: ${svc.name}`);
    }
  }

  // ─── System Settings ───
  const systemSettings: { key: string; value: string }[] = [
    { key: "site_name", value: "InstaDeed" },
    { key: "site_tagline", value: "Your Legal Partner, Instantly" },
    { key: "timezone", value: "Asia/Kolkata" },
    { key: "currency", value: "INR" },
    { key: "currency_symbol", value: "₹" },
    { key: "support_email", value: "support@instadeed.local" },
    { key: "support_phone", value: "+91-1800-123-4567" },
    { key: "admin_email", value: "admin@instadeed.local" },
    { key: "order_prefix", value: "ORD" },
    { key: "invoice_prefix", value: "INV" },
    { key: "default_gst_rate", value: "18" },
    { key: "max_file_upload_size", value: "10" },
    { key: "enable_registration", value: "true" },
    { key: "maintenance_mode", value: "false" },
  ];

  for (const setting of systemSettings) {
    const existing = await prisma.systemSetting.findUnique({
      where: { key: setting.key },
    });
    if (!existing) {
      await prisma.systemSetting.create({ data: setting });
      console.log(`  ✔ System setting created: ${setting.key}`);
    }
  }

  // ─── GST Config ───
  const existingGst = await prisma.gstConfig.findFirst();
  if (!existingGst) {
    await prisma.gstConfig.create({
      data: {
        gstNumber: "27AABCU9603R1ZM",
        gstRate: 18,
        sacCode: "9983",
        invoicePrefix: "INV",
        invoiceFooter: "This is a computer-generated invoice and does not require a physical signature.",
        bankName: "State Bank of India",
        bankAccount: "1234567890123456",
        bankIfsc: "SBIN0001234",
        bankBranch: "Connaught Place, New Delhi",
      },
    });
    console.log("  ✔ GST config created");
  } else {
    console.log("  – GST config already exists");
  }

  // ─── Email Templates ───
  const emailTemplates: { name: string; subject: string; body: string; variables: string }[] = [
    {
      name: "Order Confirmation",
      subject: "Order Confirmed – {{orderNumber}}",
      body: `<h2>Thank you for your order!</h2>
<p>Dear {{customerName}},</p>
<p>Your order <strong>{{orderNumber}}</strong> for <strong>{{serviceName}}</strong> has been confirmed.</p>
<p><strong>Order Details:</strong></p>
<ul>
  <li>Order Number: {{orderNumber}}</li>
  <li>Service: {{serviceName}}</li>
  <li>Amount: ₹{{amount}}</li>
  <li>Status: {{status}}</li>
</ul>
<p>We will keep you updated on the progress.</p>
<p>Regards,<br>Team InstaDeed</p>`,
      variables: "customerName,orderNumber,serviceName,amount,status",
    },
    {
      name: "Payment Success",
      subject: "Payment Successful – {{orderNumber}}",
      body: `<h2>Payment Received</h2>
<p>Dear {{customerName}},</p>
<p>Your payment of <strong>₹{{amount}}</strong> for order <strong>{{orderNumber}}</strong> has been successfully processed.</p>
<p>Payment ID: {{paymentId}}</p>
<p>We are now processing your request.</p>
<p>Regards,<br>Team InstaDeed</p>`,
      variables: "customerName,orderNumber,amount,paymentId",
    },
    {
      name: "Payment Failed",
      subject: "Payment Failed – {{orderNumber}}",
      body: `<h2>Payment Failed</h2>
<p>Dear {{customerName}},</p>
<p>Unfortunately, your payment of <strong>₹{{amount}}</strong> for order <strong>{{orderNumber}}</strong> has failed.</p>
<p>Please try again or use a different payment method. If the amount was deducted, it will be refunded within 3-5 working days.</p>
<p>Reason: {{failureReason}}</p>
<p>Regards,<br>Team InstaDeed</p>`,
      variables: "customerName,orderNumber,amount,failureReason",
    },
    {
      name: "Welcome Email",
      subject: "Welcome to InstaDeed!",
      body: `<h2>Welcome to InstaDeed!</h2>
<p>Dear {{customerName}},</p>
<p>Thank you for registering with InstaDeed – your trusted legal documentation partner.</p>
<p>With InstaDeed, you can:</p>
<ul>
  <li>Draft legal documents online</li>
  <li>Track your order status in real-time</li>
  <li>Get expert legal assistance</li>
  <li>Download completed documents</li>
</ul>
<p>Get started by exploring our services.</p>
<p>Regards,<br>Team InstaDeed</p>`,
      variables: "customerName,email",
    },
  ];

  for (const tmpl of emailTemplates) {
    const existing = await prisma.emailTemplate.findUnique({
      where: { name: tmpl.name },
    });
    if (!existing) {
      await prisma.emailTemplate.create({
        data: {
          name: tmpl.name,
          subject: tmpl.subject,
          body: tmpl.body,
          variables: tmpl.variables,
          isActive: true,
        },
      });
      console.log(`  ✔ Email template created: ${tmpl.name}`);
    } else {
      console.log(`  – Email template already exists: ${tmpl.name}`);
    }
  }

  // ─── Payment Gateway Defaults ───
  const gateways = [
    { gateway: "RAZORPAY" as const, isDefault: true, sortOrder: 1 },
    { gateway: "CASHFREE" as const, sortOrder: 2 },
    { gateway: "PHONEPE" as const, sortOrder: 3 },
    { gateway: "PAYU" as const, sortOrder: 4 },
    { gateway: "STRIPE" as const, sortOrder: 5 },
    { gateway: "MANUAL_UPI" as const, sortOrder: 6 },
    { gateway: "BANK_TRANSFER" as const, sortOrder: 7 },
  ];

  for (const gw of gateways) {
    const existing = await prisma.paymentGatewayConfig.findUnique({
      where: { gateway: gw.gateway },
    });
    if (!existing) {
      await prisma.paymentGatewayConfig.create({
        data: {
          gateway: gw.gateway,
          isEnabled: gw.gateway === "RAZORPAY",
          isTestMode: true,
          isDefault: gw.isDefault || false,
          paymentTimeout: 300,
          sortOrder: gw.sortOrder,
        },
      });
      console.log(`  ✔ Payment gateway created: ${gw.gateway}`);
    }
  }

  console.log("\n✅ Seeding complete!");
}

main()
  .catch((e) => {
    console.error("❌ Seed failed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
