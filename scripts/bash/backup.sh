#!/usr/bin/env bash
set -Eeuo pipefail

SOURCE_DIR="${1:?Usage: backup.sh SOURCE_DIR BACKUP_DIR}"
BACKUP_DIR="${2:?Usage: backup.sh SOURCE_DIR BACKUP_DIR}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="${BACKUP_DIR}/support-backup-${TIMESTAMP}.tar.gz"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: source directory does not exist: $SOURCE_DIR" >&2
  exit 2
fi

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "ERROR: backup directory does not exist: $BACKUP_DIR" >&2
  exit 3
fi

if [[ ! -w "$BACKUP_DIR" ]]; then
  echo "ERROR: backup destination is not writable: $BACKUP_DIR" >&2
  exit 13
fi

echo "INFO: creating backup from $SOURCE_DIR"
tar -czf "$ARCHIVE" -C "$SOURCE_DIR" .
sha256sum "$ARCHIVE" > "${ARCHIVE}.sha256"
echo "SUCCESS: $ARCHIVE"
