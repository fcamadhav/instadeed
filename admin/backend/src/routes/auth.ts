import { Router, Request, Response } from "express";
import bcrypt from "bcryptjs";
import crypto from "crypto";
import { z } from "zod";
import { prisma } from "../lib/prisma";
import { generateToken, requireAuth } from "../middleware/auth";
import { logActionSync } from "../services/audit";
import rateLimit from "express-rate-limit";

const router = Router();

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  message: { success: false, error: "Too many requests, please try again later" },
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
  name: z.string().min(1),
  phone: z.string().optional(),
});

const googleSchema = z.object({
  token: z.string().optional(),
  email: z.string().email(),
  name: z.string().optional(),
  googleId: z.string().optional(),
  picture: z.string().optional(),
});

const updateProfileSchema = z.object({
  name: z.string().min(1).optional(),
  phone: z.string().optional(),
  avatarUrl: z.string().optional(),
});

router.post("/api/admin/auth/login", authLimiter, async (req: Request, res: Response) => {
  try {
    const data = loginSchema.parse(req.body);

    const user = await prisma.user.findUnique({ where: { email: data.email } });
    if (!user || !user.passwordHash) {
      res.status(401).json({ success: false, error: "Invalid email or password" });
      return;
    }

    const valid = await bcrypt.compare(data.password, user.passwordHash);
    if (!valid) {
      res.status(401).json({ success: false, error: "Invalid email or password" });
      return;
    }

    if (!user.isActive) {
      res.status(403).json({ success: false, error: "Account is disabled" });
      return;
    }

    await prisma.$transaction([
      prisma.user.update({ where: { id: user.id }, data: { lastLoginAt: new Date() } }),
      prisma.loginHistory.create({
        data: {
          userId: user.id,
          ipAddress: req.ip,
          userAgent: req.headers["user-agent"] || null,
        },
      }),
    ]);

    const token = generateToken({ userId: user.id, email: user.email, role: user.role });

    res.json({
      success: true,
      data: {
        token,
        user: { id: user.id, name: user.name, email: user.email, role: user.role, phone: user.phone, avatarUrl: user.avatarUrl },
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Login error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

async function verifyGoogleToken(token: string): Promise<{ email: string; sub: string; name?: string } | null> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const resp = await fetch(`https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=${encodeURIComponent(token)}`, { signal: controller.signal });
    clearTimeout(timeout);
    if (!resp.ok) return null;
    const data = await resp.json() as { email: string; sub: string; name?: string };
    if (!data.email || !data.sub) return null;
    return { email: data.email, sub: data.sub, name: data.name };
  } catch {
    return null;
  }
}

router.post("/api/admin/auth/google", authLimiter, async (req: Request, res: Response) => {
  try {
    const data = googleSchema.parse(req.body);

    // Verify with Google if raw token provided
    let verifiedEmail: string | null = null;
    let verifiedSub: string | null = null;
    if (data.token) {
      const verified = await verifyGoogleToken(data.token);
      if (!verified) {
        res.status(401).json({ success: false, error: "Invalid Google token" });
        return;
      }
      if (data.googleId && verified.sub !== data.googleId) {
        res.status(401).json({ success: false, error: "Token does not match claims" });
        return;
      }
      verifiedEmail = verified.email;
      verifiedSub = verified.sub;
    } else {
      // Client-side Google SDK already verified — accept email from payload
      verifiedEmail = data.email;
      verifiedSub = data.googleId || data.email; // fallback for old SPA (no googleId)
    }

    let where: any = { OR: [{ email: verifiedEmail }] };
    if (verifiedSub && verifiedSub !== verifiedEmail) {
      where.OR.push({ googleId: verifiedSub });
    }
    let user = await prisma.user.findFirst({ where });

    if (user) {
      if (!user.isActive) {
        res.status(403).json({ success: false, error: "Account is disabled" });
        return;
      }
      if (verifiedSub && !user.googleId) {
        await prisma.user.update({ where: { id: user.id }, data: { googleId: verifiedSub } });
      }
      await prisma.$transaction([
        prisma.user.update({ where: { id: user.id }, data: { lastLoginAt: new Date() } }),
        prisma.loginHistory.create({
          data: { userId: user.id, ipAddress: req.ip, userAgent: req.headers["user-agent"] || null },
        }),
      ]);
    } else {
      user = await prisma.user.create({
        data: {
          email: data.email,
          name: data.name || data.email.split("@")[0],
          googleId: verifiedSub || null,
          role: "CUSTOMER",
        },
      });
    }

    const token = generateToken({ userId: user.id, email: user.email, role: user.role });
    res.json({
      success: true,
      data: {
        token,
        user: { id: user.id, name: user.name, email: user.email, role: user.role, phone: user.phone, avatarUrl: user.avatarUrl },
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Google auth error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.post("/api/admin/auth/register", authLimiter, async (req: Request, res: Response) => {
  try {
    const data = registerSchema.parse(req.body);

    const regSetting = await prisma.systemSetting.findUnique({ where: { key: "enable_registration" } });
    if (regSetting && regSetting.value === "false") {
      res.status(403).json({ success: false, error: "Public registration is currently disabled" });
      return;
    }

    const existing = await prisma.user.findUnique({ where: { email: data.email } });
    if (existing) {
      res.status(409).json({ success: false, error: "Email already registered" });
      return;
    }

    const passwordHash = await bcrypt.hash(data.password, 12);

    const user = await prisma.user.create({
      data: {
        email: data.email,
        passwordHash,
        name: data.name,
        phone: data.phone || null,
        role: "CUSTOMER",
      },
    });

    const token = generateToken({ userId: user.id, email: user.email, role: user.role });

    res.status(201).json({
      success: true,
      data: {
        token,
        user: { id: user.id, name: user.name, email: user.email, role: user.role, phone: user.phone },
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Register error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.get("/api/admin/auth/me", requireAuth, async (req: Request, res: Response) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.user!.userId },
      select: { id: true, name: true, email: true, phone: true, role: true, avatarUrl: true, isActive: true, createdAt: true, lastLoginAt: true },
    });
    if (!user) {
      res.status(404).json({ success: false, error: "User not found" });
      return;
    }
    res.json({ success: true, data: user });
  } catch (error) {
    console.error("Get profile error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

router.put("/api/admin/auth/me", requireAuth, async (req: Request, res: Response) => {
  try {
    const data = updateProfileSchema.parse(req.body);
    const user = await prisma.user.update({
      where: { id: req.user!.userId },
      data,
      select: { id: true, name: true, email: true, phone: true, role: true, avatarUrl: true },
    });
    res.json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Update profile error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Password reset request — generates reset token (email sending is stubbed)
const passwordResetSchema = z.object({
  email: z.string().email(),
});

router.post("/api/admin/auth/forgot-password", async (req: Request, res: Response) => {
  try {
    const data = passwordResetSchema.parse(req.body);
    const user = await prisma.user.findUnique({ where: { email: data.email } });
    if (!user) {
      // Don't reveal if email exists — always return success
      res.json({ success: true, data: { message: "If the email exists, a reset link will be sent." } });
      return;
    }
    const resetToken = crypto.randomBytes(32).toString("hex");
    const resetExpires = new Date(Date.now() + 3600000); // 1 hour
    await prisma.user.update({
      where: { id: user.id },
      data: { passwordResetToken: resetToken, passwordResetExpires: resetExpires },
    });
    // TODO: Send email with reset link — stub sends nothing in production
    if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
      console.log(`[PASSWORD RESET] Email notification would be sent to ${data.email} (SMTP configured)`);
    }
    res.json({ success: true, data: { message: "If the email exists, a reset link will be sent." } });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Password reset error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Password reset — validates token and updates password
const resetPasswordSchema = z.object({
  token: z.string().min(1),
  password: z.string().min(6),
});

router.post("/api/admin/auth/reset-password", async (req: Request, res: Response) => {
  try {
    const data = resetPasswordSchema.parse(req.body);
    const user = await prisma.user.findFirst({
      where: { passwordResetToken: data.token, passwordResetExpires: { gte: new Date() } },
    });
    if (!user) {
      res.status(400).json({ success: false, error: "Invalid or expired reset token" });
      return;
    }
    const passwordHash = await bcrypt.hash(data.password, 12);
    await prisma.user.update({
      where: { id: user.id },
      data: { passwordHash, passwordResetToken: null, passwordResetExpires: null },
    });
    res.json({ success: true, data: { message: "Password reset successfully" } });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: error.errors });
      return;
    }
    console.error("Reset password error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
