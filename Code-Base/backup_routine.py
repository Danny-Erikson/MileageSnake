from pathlib import Path
from datetime import datetime
import hashlib
import sqlite3


DB_PATH = Path("Data/Cars.db")
BACKUP_DIR = Path("Backups")
HASH_FILE = BACKUP_DIR / "last_hash.txt"

MAX_BACKUPS = 10


def file_hash(path):
    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def sqlite_backup(source_db, backup_db):
    source = sqlite3.connect(source_db)
    backup = sqlite3.connect(backup_db)

    try:
        source.backup(backup)
    finally:
        backup.close()
        source.close()


def cleanup_old_backups():
    backups = sorted(
        BACKUP_DIR.glob("Cars_*.db"),
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )

    old_backups = backups[MAX_BACKUPS:]

    for backup in old_backups:
        backup.unlink()


def back_routine():
    BACKUP_DIR.mkdir(exist_ok=True)

    current_hash = file_hash(DB_PATH)

    if HASH_FILE.exists():
        last_hash = HASH_FILE.read_text().strip()
    else:
        last_hash = None

    if current_hash != last_hash:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = BACKUP_DIR / f"Cars_{timestamp}.db"

        sqlite_backup(DB_PATH, backup_path)

        HASH_FILE.write_text(current_hash)
