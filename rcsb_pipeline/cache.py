"""SQLite-based response cache for RCSB API calls."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class ResponseCache:
    """Persistent SQLite cache for API responses."""

    def __init__(self, db_path: str, ttl: int = 86400 * 30) -> None:
        self._path = Path(db_path).expanduser()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path))
        self._conn.execute("CREATE TABLE IF NOT EXISTS cache (  key TEXT PRIMARY KEY,  value TEXT,  created_at REAL)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_key ON cache(key)")
        self._conn.commit()
        self._ttl = ttl

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    def get(self, key: str) -> Any | None:
        hkey = self._hash_key(key)
        cursor = self._conn.execute("SELECT value, created_at FROM cache WHERE key = ?", (hkey,))
        row = cursor.fetchone()
        if row is None:
            return None
        value_json, created_at = row
        if time.time() - created_at > self._ttl:
            self._conn.execute("DELETE FROM cache WHERE key = ?", (hkey,))
            self._conn.commit()
            return None
        return json.loads(value_json)

    def set(self, key: str, value: Any) -> None:
        hkey = self._hash_key(key)
        value_json = json.dumps(value, default=str)
        self._conn.execute(
            "INSERT OR REPLACE INTO cache (key, value, created_at) VALUES (?, ?, ?)",
            (hkey, value_json, time.time()),
        )
        self._conn.commit()

    def clear(self) -> None:
        self._conn.execute("DELETE FROM cache")
        self._conn.commit()

    def size(self) -> int:
        cursor = self._conn.execute("SELECT COUNT(*) FROM cache")
        return cursor.fetchone()[0]

    def close(self) -> None:
        self._conn.close()
