"""Tests for the ProcessedData registry (registry.py)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from rcsb_pipeline.registry import ProcessedRegistry


class TestProcessedRegistryInit:
    def test_init_creates_db_file(self, tmp_registry: ProcessedRegistry) -> None:
        assert Path(tmp_registry.db_path).exists()

    def test_init_creates_tables(self, tmp_registry: ProcessedRegistry) -> None:
        # Trigger lazy schema init
        _ = tmp_registry.conn
        conn = sqlite3.connect(tmp_registry.db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_registry'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_init_creates_indexes(self, tmp_registry: ProcessedRegistry) -> None:
        # Trigger lazy schema init
        _ = tmp_registry.conn
        conn = sqlite3.connect(tmp_registry.db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_registry_%'")
        indexes = {row[0] for row in cursor.fetchall()}
        assert "idx_registry_uniprot" in indexes
        assert "idx_registry_stale" in indexes
        conn.close()

    def test_init_with_expanded_path(self) -> None:
        reg = ProcessedRegistry("~/test_registry.db")
        assert "~" not in reg.db_path
        assert reg.db_path.endswith("/test_registry.db")
        reg.close()
        Path(reg.db_path).unlink(missing_ok=True)


class TestProcessedRegistryOperations:
    def test_record_and_is_processed(self, tmp_registry: ProcessedRegistry) -> None:
        assert not tmp_registry.is_processed("P01116", "4LPK")
        tmp_registry.record("P01116", "4LPK", run_id="run1", preset="standard", granularity="per-structure")
        assert tmp_registry.is_processed("P01116", "4LPK", preset="standard", granularity="per-structure")

    def test_is_processed_respects_preset(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK", preset="minimal")
        assert tmp_registry.is_processed("P01116", "4LPK", preset="minimal")
        assert not tmp_registry.is_processed("P01116", "4LPK", preset="standard")

    def test_is_processed_respects_granularity(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK", granularity="per-structure")
        assert tmp_registry.is_processed("P01116", "4LPK", granularity="per-structure")
        assert not tmp_registry.is_processed("P01116", "4LPK", granularity="per-protein")

    def test_is_processed_stale_returns_false(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK")
        assert tmp_registry.is_processed("P01116", "4LPK")
        tmp_registry.mark_stale(uniprot_ids=["P01116"])
        assert not tmp_registry.is_processed("P01116", "4LPK")

    def test_record_batch(self, tmp_registry: ProcessedRegistry) -> None:
        pairs = [("P01116", "4LPK"), ("P01116", "5P21"), ("P04637", "1TUP")]
        count = tmp_registry.record_batch(pairs, run_id="batch1")
        assert count == 3
        assert tmp_registry.is_processed("P01116", "4LPK")
        assert tmp_registry.is_processed("P04637", "1TUP")

    def test_record_batch_dedup_unique(self, tmp_registry: ProcessedRegistry) -> None:
        """INSERT OR REPLACE — same (uniprot, pdb, preset, granularity) updates."""
        tmp_registry.record_batch([("P01116", "4LPK")], run_id="first")
        tmp_registry.record_batch([("P01116", "4LPK")], run_id="second")
        assert tmp_registry.is_processed("P01116", "4LPK")
        s = tmp_registry.status()
        assert s["total_entries"] == 1  # replaced, not duplicated

    def test_filter_new_all_processed(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK")
        pairs = [("P01116", "4LPK")]
        new = tmp_registry.filter_new(pairs)
        assert new == []

    def test_filter_new_some_unprocessed(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK")
        pairs = [("P01116", "4LPK"), ("P01116", "5P21")]
        new = tmp_registry.filter_new(pairs)
        assert new == [("P01116", "5P21")]

    def test_filter_new_empty_input(self, tmp_registry: ProcessedRegistry) -> None:
        assert tmp_registry.filter_new([]) == []

    def test_filter_new_stale_included(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK")
        tmp_registry.mark_stale(uniprot_ids=["P01116"])
        new = tmp_registry.filter_new([("P01116", "4LPK")])
        assert new == [("P01116", "4LPK")]


class TestProcessedRegistryLifecycle:
    def test_mark_stale_all(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.mark_stale()
        assert count == 4
        s = populated_registry.status()
        assert s["stale_entries"] == 4

    def test_mark_stale_specific(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.mark_stale(uniprot_ids=["P01116"])
        assert count == 2
        s = populated_registry.status()
        assert s["stale_entries"] == 2 + 2  # 2 fresh from P04637 were already stale

    def test_mark_stale_idempotent(self, populated_registry: ProcessedRegistry) -> None:
        populated_registry.mark_stale(uniprot_ids=["P04637"])
        count = populated_registry.mark_stale(uniprot_ids=["P04637"])
        assert count == 2  # still matches, already stale

    def test_mark_fresh_all(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.mark_fresh()
        assert count == 4
        s = populated_registry.status()
        assert s["stale_entries"] == 0

    def test_mark_fresh_specific(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.mark_fresh(uniprot_ids=["P04637"])
        assert count == 2
        s = populated_registry.status()
        assert s["stale_entries"] == 0  # P04637 was stale, now fresh

    def test_clear_all(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.clear()
        assert count == 4
        s = populated_registry.status()
        assert s["total_entries"] == 0

    def test_clear_specific(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.clear(uniprot_ids=["P01116"])
        assert count == 2
        s = populated_registry.status()
        assert s["total_entries"] == 2

    def test_clear_nonexistent(self, populated_registry: ProcessedRegistry) -> None:
        count = populated_registry.clear(uniprot_ids=["Q99999"])
        assert count == 0


class TestProcessedRegistryStatus:
    def test_status_empty(self, tmp_registry: ProcessedRegistry) -> None:
        s = tmp_registry.status()
        assert s["total_entries"] == 0
        assert s["stale_entries"] == 0
        assert s["unique_uniprots"] == 0
        assert s["unique_pdbs"] == 0
        assert s["presets"] == []

    def test_status_populated(self, populated_registry: ProcessedRegistry) -> None:
        s = populated_registry.status()
        assert s["total_entries"] == 4
        assert s["stale_entries"] == 2  # P04637 marked stale
        assert s["unique_uniprots"] == 2
        assert s["unique_pdbs"] == 4
        presets: list[dict[str, object]] = s["presets"]  # type: ignore[assignment]
        assert len(presets) == 1
        assert presets[0]["preset"] == "standard"
        assert presets[0]["cnt"] == 4

    def test_status_latest_run(self, populated_registry: ProcessedRegistry) -> None:
        s = populated_registry.status()
        assert s["latest_run"] != "never"

    def test_status_no_runs(self, tmp_registry: ProcessedRegistry) -> None:
        s = tmp_registry.status()
        assert s["latest_run"] == "never"


class TestProcessedRegistryDiff:
    def test_diff_all_new(self, populated_registry: ProcessedRegistry) -> None:
        pairs = [("Q99999", "1ABC")]
        result = populated_registry.diff(pairs)
        assert len(result["new"]) == 1
        assert len(result["already_processed"]) == 0

    def test_diff_all_processed(self, populated_registry: ProcessedRegistry) -> None:
        pairs = [("P01116", "4LPK")]
        result = populated_registry.diff(pairs, preset="standard", granularity="per-structure")
        assert len(result["already_processed"]) == 1
        assert len(result["new"]) == 0

    def test_diff_mixed(self, populated_registry: ProcessedRegistry) -> None:
        pairs = [("P01116", "4LPK"), ("Q99999", "1ABC")]
        result = populated_registry.diff(pairs, preset="standard", granularity="per-structure")
        assert result["new"] == [("Q99999", "1ABC")]
        assert result["already_processed"] == [("P01116", "4LPK")]

    def test_diff_with_empty_pdb_id(self, populated_registry: ProcessedRegistry) -> None:
        """When pdb_id is empty, checks if any entry exists for that uniprot."""
        result = populated_registry.diff(
            [("P01116", "")],
            preset="standard",
            granularity="per-structure",
        )
        # P01116 has entries in registry
        assert len(result["already_processed"]) == 1
        result2 = populated_registry.diff(
            [("Q99999", "")],
            preset="standard",
            granularity="per-structure",
        )
        assert len(result2["new"]) == 1

    def test_diff_respects_preset(self, populated_registry: ProcessedRegistry) -> None:
        pairs = [("P01116", "4LPK")]
        # Recorded with preset="standard", so different preset should show as new
        result = populated_registry.diff(pairs, preset="minimal")
        assert len(result["new"]) == 1


class TestProcessedRegistryContextManager:
    def test_context_manager(self) -> None:
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        with ProcessedRegistry(db_path) as reg:
            reg.record("P01116", "4LPK", run_id="ctx-test")
            assert reg.is_processed("P01116", "4LPK")
        # Connection should be closed after exit
        assert reg._conn is None
        Path(db_path).unlink(missing_ok=True)

    def test_conn_reopened_after_close(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.close()
        assert tmp_registry.is_processed("P01116", "4LPK") is False
        tmp_registry.close()


class TestProcessedRegistryEdgeCases:
    def test_empty_uniprot_id(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("", "4LPK")
        assert tmp_registry.is_processed("", "4LPK")

    def test_special_chars(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116_A", "4LPK-B")
        assert tmp_registry.is_processed("P01116_A", "4LPK-B")

    def test_clear_then_re_record(self, tmp_registry: ProcessedRegistry) -> None:
        tmp_registry.record("P01116", "4LPK")
        tmp_registry.clear()
        assert not tmp_registry.is_processed("P01116", "4LPK")
        tmp_registry.record("P01116", "4LPK")
        assert tmp_registry.is_processed("P01116", "4LPK")
