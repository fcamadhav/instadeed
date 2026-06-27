import { Prisma } from "@prisma/client";
import { prisma } from "../lib/prisma";

interface AuditLogInput {
  userId?: string;
  action: string;
  module: string;
  recordId?: string;
  oldValue?: Prisma.InputJsonValue;
  newValue?: Prisma.InputJsonValue;
  ipAddress?: string;
}

export async function logAction(data: AuditLogInput): Promise<void> {
  try {
    await prisma.auditLog.create({
      data: {
        userId: data.userId,
        action: data.action,
        module: data.module,
        recordId: data.recordId,
        oldValue: data.oldValue ? JSON.stringify(data.oldValue) : null,
        newValue: data.newValue ? JSON.stringify(data.newValue) : null,
        ipAddress: data.ipAddress,
      },
    });
  } catch (error) {
    console.error("Failed to create audit log:", error);
  }
}

export async function logActionSync(
  userId: string | undefined,
  action: string,
  module: string,
  recordId?: string,
  oldValue?: Record<string, unknown>,
  newValue?: Record<string, unknown>,
  ipAddress?: string
): Promise<void> {
  await logAction({
    userId,
    action,
    module,
    recordId,
    oldValue: oldValue as Prisma.InputJsonValue,
    newValue: newValue as Prisma.InputJsonValue,
    ipAddress,
  });
}
