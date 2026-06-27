import { Router, Request, Response } from "express";
import bcrypt from "bcryptjs";
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
  token: z.string().min(1),
  email: z.string().email(),
  name: z.string().optional(),
  googleId: z.string().min(1),
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

router.post("/api/admin/auth/google", authLimiter, async (req: Request, res: Response) => {
  try {
    const data = googleSchema.parse(req.body);
    let user = await prisma.user.findFirst({ where: { OR: [{ email: data.email }, { googleId: data.googleId }] } });

    if (user) {
      if (!user.isActive) {
        res.status(403).json({ success: false, error: "Account is disabled" });
        return;
      }
      if (!user.googleId) {
        await prisma.user.update({ where: { id: user.id }, data: { googleId: data.googleId } });
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
          googleId: data.googleId,
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

export default router;
