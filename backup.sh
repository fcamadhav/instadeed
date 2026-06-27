#!/bin/bash
# Instadeed Database Backup Script
# Run daily via cron: 0 3 * * * /app/backup.sh

set -e

BACKUP_DIR="${BACKUP_DIR:-/app/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG="/var/log/instadeed-backup.log"

mkdir -p "$BACKUP_DIR"
exec >> "$LOG" 2>&1
echo "[$(date)] Starting backup..."

# Backup admin SQLite database
if docker exec admin_backend_1 test -f /app/prisma/data/instadeed_admin.db 2>/dev/null; then
  docker cp admin_backend_1:/app/prisma/data/instadeed_admin.db "$BACKUP_DIR/instadeed_admin_$TIMESTAMP.db"
  gzip "$BACKUP_DIR/instadeed_admin_$TIMESTAMP.db"
  echo "[$(date)] Admin DB backed up"
fi

# Backup old Python CRM database
if [ -f /app/madhav_crm.db ]; then
  cp /app/madhav_crm.db "$BACKUP_DIR/madhav_crm_$TIMESTAMP.db"
  gzip "$BACKUP_DIR/madhav_crm_$TIMESTAMP.db"
  echo "[$(date)] CRM DB backed up"
fi

# Clean old backups
find "$BACKUP_DIR" -name "*.gz" -mtime "+$RETENTION_DAYS" -delete
echo "[$(date)] Cleaned backups older than $RETENTION_DAYS days"

echo "[$(date)] Backup complete"
