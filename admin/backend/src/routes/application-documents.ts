import { Router, Request, Response } from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import { prisma } from "../lib/prisma";

const router = Router();

const STORAGE_ROOT = path.resolve(__dirname, "..", "..", "storage", "applications");

const ALLOWED_MIMES: Record<string, string[]> = {
  "sale-deed": ["application/pdf"],
  "aadhaar": ["application/pdf", "image/jpeg", "image/jpg", "image/png"],
  "pan": ["application/pdf", "image/jpeg", "image/jpg", "image/png"],
  "photo": ["image/jpeg", "image/jpg", "image/png"],
  "other": ["application/pdf", "image/jpeg", "image/jpg", "image/png"],
};

const DOCUMENT_TYPES: Record<string, string> = {
  "sale-deed": "Registered Sale Deed / Registry Copy",
  "aadhaar": "Aadhaar Card of the Applicant",
  "pan": "PAN Card",
  "photo": "Passport Size Photo",
  "other": "Other Document",
};

const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

const upload = multer({
  storage: multer.diskStorage({
    destination: (_req, _file, cb) => {
      ensureDir(STORAGE_ROOT);
      cb(null, STORAGE_ROOT);
    },
    filename: (_req, file, cb) => {
      const ext = path.extname(file.originalname);
      cb(null, `${Date.now()}-${Math.random().toString(36).substring(2, 8)}${ext}`);
    },
  }),
  limits: { fileSize: MAX_SIZE },
  fileFilter: (req, file, cb) => {
    const docType = (req.body as any)?.documentType || "other";
    const allowed = ALLOWED_MIMES[docType] || ALLOWED_MIMES["other"];
    if (allowed.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error(`Invalid file type. Allowed: ${allowed.join(", ")}`));
    }
  },
});

// Upload document
router.post("/api/applications/documents/upload", upload.single("file"), async (req: Request, res: Response) => {
  try {
    const file = req.file;
    if (!file) {
      res.status(400).json({ success: false, error: "No file uploaded" });
      return;
    }
    const { applicationId, documentType } = req.body;
    if (!applicationId || !documentType) {
      res.status(400).json({ success: false, error: "applicationId and documentType are required" });
      return;
    }

    const doc = await prisma.applicationDocument.create({
      data: {
        applicationId,
        documentType,
        fileName: file.originalname,
        fileUrl: file.path,
        mimeType: file.mimetype,
        size: file.size,
      },
    });

    res.status(201).json({ success: true, data: doc });
  } catch (error: any) {
    if (error.message?.includes("Invalid file type")) {
      res.status(400).json({ success: false, error: error.message });
      return;
    }
    console.error("Upload error:", error);
    res.status(500).json({ success: false, error: "Upload failed" });
  }
});

// Get documents for an application
router.get("/api/applications/:id/documents", async (req: Request, res: Response) => {
  try {
    const docs = await prisma.applicationDocument.findMany({
      where: { applicationId: req.params.id },
      orderBy: { uploadedAt: "asc" },
    });
    res.json({ success: true, data: docs });
  } catch (error) {
    console.error("Get docs error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Delete a document
router.delete("/api/applications/documents/:id", async (req: Request, res: Response) => {
  try {
    const doc = await prisma.applicationDocument.findUnique({ where: { id: req.params.id } });
    if (!doc) {
      res.status(404).json({ success: false, error: "Document not found" });
      return;
    }
    if (fs.existsSync(doc.fileUrl)) {
      fs.unlinkSync(doc.fileUrl);
    }
    await prisma.applicationDocument.delete({ where: { id: req.params.id } });
    res.json({ success: true, data: { message: "Document deleted" } });
  } catch (error) {
    console.error("Delete doc error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// Get required documents list for an application type
router.get("/api/applications/documents/required/:type", (_req: Request, res: Response) => {
  const type = _req.params.type;
  const required: { key: string; title: string; accept: string; required: boolean; maxSize: string }[] = [];

  if (type === "mutation") {
    required.push(
      { key: "sale-deed", title: "Registered Sale Deed / Registry Copy", accept: "application/pdf", required: true, maxSize: "10 MB" },
      { key: "aadhaar", title: "Aadhaar Card of the Applicant", accept: "application/pdf,image/jpeg,image/jpg,image/png", required: true, maxSize: "10 MB" },
    );
  }

  res.json({ success: true, data: required });
});

// Download/Preview a single application document
router.get("/api/applications/documents/:id/file", async (req: Request, res: Response) => {
  try {
    const doc = await prisma.applicationDocument.findUnique({ where: { id: req.params.id } });
    if (!doc || !fs.existsSync(doc.fileUrl)) {
      res.status(404).json({ success: false, error: "File not found" });
      return;
    }
    res.download(doc.fileUrl, doc.fileName);
  } catch (error) {
    console.error("Download doc error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

// List ALL application documents (for admin panel)
router.get("/api/admin/applications/documents", async (_req: Request, res: Response) => {
  try {
    const docs = await prisma.applicationDocument.findMany({
      orderBy: { uploadedAt: "desc" },
    });
    // Group by applicationId
    const grouped: Record<string, any[]> = {};
    docs.forEach(d => {
      if (!grouped[d.applicationId]) grouped[d.applicationId] = [];
      grouped[d.applicationId].push(d);
    });
    res.json({ success: true, data: { documents: docs, grouped, total: docs.length } });
  } catch (error) {
    console.error("List all docs error:", error);
    res.status(500).json({ success: false, error: "Internal server error" });
  }
});

export default router;
