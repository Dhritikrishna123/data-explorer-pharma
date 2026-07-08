"""Processed data registry — tracks which (uniprot_id, pdb_id) pairs
have been successfully exported so they are never re-sent downstream."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class RegistryError(Exception):
    pass


class ProcessedRegistry:
    """Persistent SQLite-backed ledger of exported entries.

    Records every (uniprot_id, pdb_id) pair that completed the pipeline,
    along with run metadata, so subsequent runs can skip already-processed
    targets and the team never receives duplicate data downstream.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = str(Path(db_path).expanduser().resolve())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._init_schema()
        return self._conn

    def _init_schema(self) -> None:
        conn = self.conn
        conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_registry (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                uniprot_id  TEXT NOT NULL,
                pdb_id      TEXT NOT NULL,
                run_id      TEXT NOT NULL,
                preset      TEXT,
                granularity TEXT,
                output_dir  TEXT,
                checksum    TEXT,
                stale       INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL,
                UNIQUE(uniprot_id, pdb_id, preset, granularity)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_registry_uniprot
            ON processed_registry(uniprot_id)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_registry_stale
            ON processed_registry(stale)
        """)
        conn.commit()

    def is_processed(
        self,
        uniprot_id: str,
        pdb_id: str,
        preset: str = "",
        granularity: str = "",
    ) -> bool:
        """Check if a specific (uniprot, pdb) pair has been exported."""
        row = self.conn.execute(
            """SELECT 1 FROM processed_registry
               WHERE uniprot_id=? AND pdb_id=? AND preset=? AND granularity=?
               AND stale=0""",
            (uniprot_id, pdb_id, preset, granularity),
        ).fetchone()
        return row is not None

    def filter_new(
        self,
        pairs: list[tuple[str, str]],
        preset: str = "",
        granularity: str = "",
    ) -> list[tuple[str, str]]:
        """Return only pairs that have NOT been processed yet (or are stale)."""
        if not pairs:
            return []
        new_pairs: list[tuple[str, str]] = []
        for uid, pid in pairs:
            if not self.is_processed(uid, pid, preset, granularity):
                new_pairs.append((uid, pid))
        return new_pairs

    def record(
        self,
        uniprot_id: str,
        pdb_id: str,
        run_id: str = "",
        preset: str = "",
        granularity: str = "",
        output_dir: str = "",
        checksum: str = "",
    ) -> None:
        """Record a processed (uniprot, pdb) pair."""
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            """INSERT OR REPLACE INTO processed_registry
               (uniprot_id, pdb_id, run_id, preset, granularity,
                output_dir, checksum, stale, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,0,
                       COALESCE((SELECT created_at FROM processed_registry
                                 WHERE uniprot_id=? AND pdb_id=? AND preset=? AND granularity=?), ?),
                       ?)""",
            (
                uniprot_id,
                pdb_id,
                run_id,
                preset,
                granularity,
                output_dir,
                checksum,
                uniprot_id,
                pdb_id,
                preset,
                granularity,
                now,
                now,
            ),
        )
        self.conn.commit()

    def record_batch(
        self,
        pairs: list[tuple[str, str]],
        run_id: str = "",
        preset: str = "",
        granularity: str = "",
        output_dir: str = "",
    ) -> int:
        """Record many pairs in a single transaction. Returns count."""
        now = datetime.now(timezone.utc).isoformat()
        rows = [
            (
                uid,
                pid,
                run_id,
                preset,
                granularity,
                output_dir,
                "",
                uid,
                pid,
                preset,
                granularity,
                now,
                now,
            )
            for uid, pid in pairs
        ]
        self.conn.executemany(
            """INSERT OR REPLACE INTO processed_registry
               (uniprot_id, pdb_id, run_id, preset, granularity,
                output_dir, checksum, stale, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,0,
                       COALESCE((SELECT created_at FROM processed_registry
                                 WHERE uniprot_id=? AND pdb_id=? AND preset=? AND granularity=?), ?),
                       ?)""",
            rows,
        )
        self.conn.commit()
        return len(rows)

    def mark_stale(self, uniprot_ids: list[str] | None = None) -> int:
        """Mark entries as stale so they'll be reprocessed.

        If uniprot_ids is None, marks ALL entries stale.
        Returns count of affected rows.
        """
        now = datetime.now(timezone.utc).isoformat()
        if uniprot_ids:
            placeholders = ",".join("?" for _ in uniprot_ids)
            cur = self.conn.execute(
                f"""UPDATE processed_registry SET stale=1, updated_at=?
                    WHERE uniprot_id IN ({placeholders})""",
                [now] + uniprot_ids,
            )
        else:
            cur = self.conn.execute(
                "UPDATE processed_registry SET stale=1, updated_at=?",
                (now,),
            )
        self.conn.commit()
        return cur.rowcount

    def mark_fresh(self, uniprot_ids: list[str] | None = None) -> int:
        """Reverse of mark_stale — mark entries as not stale."""
        now = datetime.now(timezone.utc).isoformat()
        if uniprot_ids:
            placeholders = ",".join("?" for _ in uniprot_ids)
            cur = self.conn.execute(
                f"""UPDATE processed_registry SET stale=0, updated_at=?
                    WHERE uniprot_id IN ({placeholders})""",
                [now] + uniprot_ids,
            )
        else:
            cur = self.conn.execute(
                "UPDATE processed_registry SET stale=0, updated_at=?",
                (now,),
            )
        self.conn.commit()
        return cur.rowcount

    def clear(self, uniprot_ids: list[str] | None = None) -> int:
        """Delete entries. If uniprot_ids is None, clears all."""
        if uniprot_ids:
            placeholders = ",".join("?" for _ in uniprot_ids)
            cur = self.conn.execute(
                f"DELETE FROM processed_registry WHERE uniprot_id IN ({placeholders})",
                uniprot_ids,
            )
        else:
            cur = self.conn.execute("DELETE FROM processed_registry")
        self.conn.commit()
        return cur.rowcount

    def status(self) -> dict[str, object]:
        """Summary statistics about the registry."""
        total = self.conn.execute("SELECT COUNT(*) FROM processed_registry").fetchone()[0]
        stale = self.conn.execute("SELECT COUNT(*) FROM processed_registry WHERE stale=1").fetchone()[0]
        unique_uniprots = self.conn.execute("SELECT COUNT(DISTINCT uniprot_id) FROM processed_registry").fetchone()[0]
        unique_pdbs = self.conn.execute("SELECT COUNT(DISTINCT pdb_id) FROM processed_registry").fetchone()[0]
        presets = [
            dict(r)
            for r in self.conn.execute(
                "SELECT preset, COUNT(*) as cnt FROM processed_registry GROUP BY preset ORDER BY cnt DESC"
            ).fetchall()
        ]
        latest = self.conn.execute("SELECT MAX(created_at) FROM processed_registry").fetchone()[0]
        return {
            "total_entries": total,
            "stale_entries": stale,
            "unique_uniprots": unique_uniprots,
            "unique_pdbs": unique_pdbs,
            "presets": presets,
            "latest_run": latest or "never",
        }

    def diff(
        self,
        pairs: list[tuple[str, str]],
        preset: str = "",
        granularity: str = "",
    ) -> dict[str, list]:
        """Compare a set of pairs against the registry.

        When pdb_id is empty, checks if *any* entry for that uniprot_id
        exists in the registry (regardless of PDB).

        Returns:
            {"new": [...], "already_processed": [...]}
        """
        new_list: list[tuple[str, str]] = []
        already: list[tuple[str, str]] = []
        for uid, pid in pairs:
            if not pid:
                row = self.conn.execute(
                    """SELECT 1 FROM processed_registry
                       WHERE uniprot_id=? AND preset=? AND granularity=?
                       AND stale=0 LIMIT 1""",
                    (uid, preset, granularity),
                ).fetchone()
                is_done = row is not None
            else:
                is_done = self.is_processed(uid, pid, preset, granularity)
            if is_done:
                already.append((uid, pid))
            else:
                new_list.append((uid, pid))
        return {"new": new_list, "already_processed": already}

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> ProcessedRegistry:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
