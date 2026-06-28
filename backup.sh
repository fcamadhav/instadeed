#!/bin/bash
# Instadeed Production Backup Script
# Backs up databases, uploaded documents, and Prisma schema
# Retention: 7 daily + 4 weekly (keeps Sunday backups as weekly)
# Off-site: Uploads to GCP Cloud Storage if gsutil is available

set -euo pipefail

# ─── Configuration ───
BACKUP_DIR="${BACKUP_DIR:-/app/backups}"
STORAGE_BUCKET="${STORAGE_BUCKET:-gs://instadeed-backups}"
RETENTION_DAYS=7
RETENTION_WEEKS=4
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DOW=$(date +%u)  # 1=Monday, 7=Sunday
LOG="/var/log/instadeed-backup.log"
LOCKFILE="/tmp/instadeed-backup.lock"

exec >> "$LOG" 2>&1

# ─── Lock (prevent concurrent runs) ───
if [ -f "$LOCKFILE" ] && kill -0 "$(cat "$LOCKFILE")" 2>/dev/null; then
    echo "[$(date)] ERROR: Previous backup still running (PID $(cat "$LOCKFILE"))"
    exit 1
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

echo ""
echo "========================================"
echo "[$(date)] Instadeed Backup Started"
echo "========================================"

mkdir -p "$BACKUP_DIR"/{daily,weekly}

# ─── 1. Admin SQLite Database ───
echo "[$(date)] Backing up admin database..."
if docker exec admin_backend_1 sh -c 'test -f /app/prisma/data/instadeed_admin.db' 2>/dev/null; then
    docker exec admin_backend_1 sh -c 'sqlite3 /app/prisma/data/instadeed_admin.db ".backup /tmp/instadeed_admin_backup.db"' 2>/dev/null || \
    docker cp admin_backend_1:/app/prisma/data/instadeed_admin.db /tmp/instadeed_admin_backup.db 2>/dev/null
    if [ -f /tmp/instadeed_admin_backup.db ]; then
        gzip -c /tmp/instadeed_admin_backup.db > "$BACKUP_DIR/daily/instadeed_admin_$TIMESTAMP.db.gz"
        rm -f /tmp/instadeed_admin_backup.db
        echo "[$(date)] Admin DB: OK ($(ls -lh "$BACKUP_DIR/daily/instadeed_admin_$TIMESTAMP.db.gz" | awk '{print $5}'))"
    fi
else
    echo "[$(date)] Admin DB container not running, skipping"
fi

# ─── 2. Old CRM Database ───
if [ -f /app/madhav_crm.db ]; then
    echo "[$(date)] Backing up CRM database..."
    gzip -c /app/madhav_crm.db > "$BACKUP_DIR/daily/madhav_crm_$TIMESTAMP.db.gz"
    echo "[$(date)] CRM DB: OK ($(ls -lh "$BACKUP_DIR/daily/madhav_crm_$TIMESTAMP.db.gz" | awk '{print $5}'))"
fi

# ─── 3. Uploaded Documents & PDFs ───
echo "[$(date)] Backing up uploaded documents..."
if docker ps --format '{{.Names}}' | grep -q admin_backend_1; then
    # The storage path in the container is /app/prisma/data/ (alongside the DB)
    # Documents are stored at admin/backend/storage/documents/
    docker exec admin_backend_1 sh -c 'test -d /app/storage/documents' 2>/dev/null && \
    tar czf "/tmp/documents_$TIMESTAMP.tar.gz" -C /app/storage documents 2>/dev/null || true
    if [ -f "/tmp/documents_$TIMESTAMP.tar.gz" ] && [ -s "/tmp/documents_$TIMESTAMP.tar.gz" ]; then
        mv "/tmp/documents_$TIMESTAMP.tar.gz" "$BACKUP_DIR/daily/documents_$TIMESTAMP.tar.gz"
        echo "[$(date)] Documents: OK ($(ls -lh "$BACKUP_DIR/daily/documents_$TIMESTAMP.tar.gz" | awk '{print $5}'))"
    else
        echo "[$(date)] Documents: none found"
        rm -f "/tmp/documents_$TIMESTAMP.tar.gz"
    fi
fi

# ─── 4. Prisma Schema (for migration reference) ───
echo "[$(date)] Backing up Prisma schema..."
if [ -f /app/admin/backend/prisma/schema.prisma ]; then
    cp /app/admin/backend/prisma/schema.prisma "$BACKUP_DIR/daily/schema_$TIMESTAMP.prisma"
    echo "[$(date)] Schema: OK"
fi

# ─── 5. Rotation: Keep 7 daily ───
echo "[$(date)] Cleaning daily backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR/daily" -name "*.gz" -mtime "+$RETENTION_DAYS" -delete
find "$BACKUP_DIR/daily" -name "*.prisma" -mtime "+$RETENTION_DAYS" -delete

# ─── 6. Weekly rotation: Keep Sunday backups as weekly ───
if [ "$DOW" = "7" ]; then
    echo "[$(date)] Sunday — creating weekly snapshot..."
    LATEST=$(ls -t "$BACKUP_DIR/daily/"*.gz 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        BASENAME=$(basename "$LATEST")
        cp "$LATEST" "$BACKUP_DIR/weekly/${BASENAME%.gz}_weekly.gz"
        echo "[$(date)] Weekly: $BASENAME"
    fi
    # Clean weekly older than $RETENTION_WEEKS weeks
    find "$BACKUP_DIR/weekly" -name "*.gz" -mtime "+$((RETENTION_WEEKS * 7))" -delete
fi

# ─── 7. Off-site: Upload to GCP Cloud Storage ───
if command -v gsutil &>/dev/null; then
    echo "[$(date)] Uploading to GCP Cloud Storage..."
    # Check if bucket exists, create if not
    gsutil ls "$STORAGE_BUCKET" &>/dev/null || gsutil mb "$STORAGE_BUCKET" &>/dev/null || true
    gsutil -q cp "$BACKUP_DIR/daily/"*.gz "$STORAGE_BUCKET/daily/" 2>/dev/null && \
    echo "[$(date)] Upload: OK" || \
    echo "[$(date)] Upload: skipped (gsutil unavailable or bucket inaccessible)"
else
    echo "[$(date)] Upload: gsutil not installed — backups stored locally at $BACKUP_DIR"
fi

# ─── 8. Summary ───
echo ""
echo "[$(date)] Backup Summary:"
echo "  Location: $BACKUP_DIR"
echo "  Daily backups: $(find "$BACKUP_DIR/daily" -name '*.gz' | wc -l) files"
echo "  Weekly backups: $(find "$BACKUP_DIR/weekly" -name '*.gz' | wc -l) files"
echo "  Total size: $(du -sh "$BACKUP_DIR" | awk '{print $1}')"
echo "========================================"
echo "[$(date)] Backup Complete"
echo "========================================"
