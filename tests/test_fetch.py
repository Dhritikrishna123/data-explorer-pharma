"""Tests for the fetch layer (fetch.py).

Uses mocked DataQuery to avoid hitting the live RCSB Data API."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from rcsb_pipeline.fetch import (
    _execute_entry_query,
    _execute_uniprot_query,
    fetch_entry_data,
    fetch_uniprot_data,
    save_raw_data,
)

# ── Mock response helpers ──


def _mock_entry_response(pdb_ids: list) -> dict:
    return {
        "data": {
            "entries": [
                {
                    "rcsb_id": pid,
                    "rcsb_entry_info": {
                        "resolution_combined": 1.5,
                    },
                }
                for pid in pdb_ids
            ]
        }
    }


def _mock_uniprot_response(uniprot_ids: list) -> dict:
    return {
        "data": {
            "uniprot": {
                "rcsb_id": uniprot_ids[0] if uniprot_ids else "",
            }
        }
    }


# ── _execute_entry_query ──


class TestExecuteEntryQuery:
    def test_execute_query(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = _mock_entry_response(["4LPK", "5P21"])

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_entry_query(
                pdb_ids=["4LPK", "5P21"],
                field_paths=["entry.rcsb_id", "entry.rcsb_entry_info.resolution_combined"],
            )

        assert "4LPK" in data
        assert "5P21" in data
        assert data["4LPK"]["rcsb_entry_info"]["resolution_combined"] == 1.5

    def test_execute_query_empty_result(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = {}

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_entry_query(pdb_ids=["4LPK"], field_paths=["entry.rcsb_id"])

        assert data == {}

    def test_execute_query_non_dict_result(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = "not a dict"

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_entry_query(pdb_ids=["4LPK"], field_paths=["entry.rcsb_id"])

        assert data == {}

    def test_execute_query_no_rcsb_id(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = {"data": {"entries": [{"some_key": "value"}]}}

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_entry_query(pdb_ids=["4LPK"], field_paths=["entry.rcsb_id"])

        assert data == {}

    def test_execute_entry_constructs_query(self) -> None:
        with patch("rcsb_pipeline.fetch.DataQuery") as mock_query_class:
            mock_instance = MagicMock()
            mock_instance.exec.return_value = _mock_entry_response(["4LPK"])
            mock_query_class.return_value = mock_instance

            _execute_entry_query(
                pdb_ids=["4LPK"],
                field_paths=["entry.rcsb_id"],
            )

            mock_query_class.assert_called_once_with(
                input_type="entry",
                input_ids=["4LPK"],
                return_data_list=["entry.rcsb_id"],
            )


# ── _execute_uniprot_query ──


class TestExecuteUniprotQuery:
    def test_execute_query(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = _mock_uniprot_response(["P01116"])

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_uniprot_query(
                uniprot_ids=["P01116"],
                field_paths=["uniprot.rcsb_id"],
            )

        assert "P01116" in data

    def test_execute_query_empty(self) -> None:
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = {}

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_uniprot_query(uniprot_ids=["P01116"], field_paths=[])

        assert data == {}

    def test_execute_query_entries_fallback(self) -> None:
        """When data comes back in entries rather than uniprot key."""
        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = {
            "data": {
                "entries": [{"rcsb_id": "4LPK", "rcsb_entry_info": {}}],
            }
        }

        with patch("rcsb_pipeline.fetch.DataQuery", return_value=mock_query_instance):
            data = _execute_uniprot_query(uniprot_ids=["P01116"], field_paths=[])

        assert "4LPK" in data


# ── fetch_entry_data ──


class TestFetchEntryData:
    def test_all_cached(self, tmp_cache: Any) -> None:
        # Cache key uses sorted field paths
        cache_key = "entry:4LPK:entry.rcsb_entry_info.resolution_combined,entry.rcsb_id"
        tmp_cache.set(cache_key, {"rcsb_id": "4LPK"})

        with patch("rcsb_pipeline.fetch._execute_entry_query") as mock_exec:
            results = fetch_entry_data(
                pdb_ids=["4LPK"],
                field_paths=["entry.rcsb_id", "entry.rcsb_entry_info.resolution_combined"],
                cache=tmp_cache,
            )
            mock_exec.assert_not_called()

        assert "4LPK" in results

    def test_some_cached(self, tmp_cache: Any) -> None:
        tmp_cache.set("entry:4LPK:entry.rcsb_id,entry.rcsb_entry_info.resolution_combined", {"rcsb_id": "4LPK"})

        mock_query_instance = MagicMock()
        mock_query_instance.exec.return_value = _mock_entry_response(["5P21"])

        with patch("rcsb_pipeline.fetch._execute_entry_query", return_value={"5P21": {"rcsb_id": "5P21"}}):
            results = fetch_entry_data(
                pdb_ids=["4LPK", "5P21"],
                field_paths=["entry.rcsb_id", "entry.rcsb_entry_info.resolution_combined"],
                cache=tmp_cache,
            )

        assert "4LPK" in results
        assert "5P21" in results

    def test_api_error(self, tmp_cache: Any) -> None:
        with patch("rcsb_pipeline.fetch._execute_entry_query", side_effect=Exception("API Error")):
            results = fetch_entry_data(
                pdb_ids=["4LPK"],
                field_paths=["entry.rcsb_id"],
                cache=tmp_cache,
            )

        assert "4LPK" in results
        assert results["4LPK"] is not None
        assert "error" in results["4LPK"]

    def test_no_pdb_ids(self, tmp_cache: Any) -> None:
        results = fetch_entry_data([], [], cache=tmp_cache)
        assert results == {}

    def test_batch_handling(self, tmp_cache: Any) -> None:
        """Should batch IDs into groups of 50."""
        many_ids = [f"{i:04d}" for i in range(100)]

        with patch("rcsb_pipeline.fetch._execute_entry_query", return_value={}) as mock_exec:
            fetch_entry_data(many_ids, ["entry.rcsb_id"], cache=tmp_cache)
            # Should have been called at least twice (100 ids / 50 batch)
            assert mock_exec.call_count >= 2

    def test_invalid_pdb_ids_handled(self, tmp_cache: Any) -> None:
        """Non-responsive PDB IDs should get _no_data markers."""
        with patch("rcsb_pipeline.fetch._execute_entry_query", return_value={}):
            results = fetch_entry_data(
                pdb_ids=["NONEXISTENT"],
                field_paths=["entry.rcsb_id"],
                cache=tmp_cache,
            )

        assert "NONEXISTENT" in results
        assert results["NONEXISTENT"] is not None
        assert results["NONEXISTENT"].get("_no_data") is True


# ── fetch_uniprot_data ──


class TestFetchUniprotData:
    def test_all_cached(self, tmp_cache: Any) -> None:
        tmp_cache.set("uniprot:P01116:uniprot.rcsb_id,uniprot.rcsb_uniprot_protein.sequence", {"rcsb_id": "P01116"})

        with patch("rcsb_pipeline.fetch._execute_uniprot_query") as mock_exec:
            results = fetch_uniprot_data(
                uniprot_ids=["P01116"],
                field_paths=["uniprot.rcsb_id", "uniprot.rcsb_uniprot_protein.sequence"],
                cache=tmp_cache,
            )
            mock_exec.assert_not_called()

        assert "P01116" in results

    def test_api_hit(self, tmp_cache: Any) -> None:
        with patch("rcsb_pipeline.fetch._execute_uniprot_query", return_value={"P01116": {"rcsb_id": "P01116"}}):
            results = fetch_uniprot_data(
                uniprot_ids=["P01116"],
                field_paths=["uniprot.rcsb_id"],
                cache=tmp_cache,
            )

        assert "P01116" in results

    def test_api_error(self, tmp_cache: Any) -> None:
        with patch("rcsb_pipeline.fetch._execute_uniprot_query", side_effect=Exception("API Error")):
            results = fetch_uniprot_data(
                uniprot_ids=["P01116"],
                field_paths=["uniprot.rcsb_id"],
                cache=tmp_cache,
            )

        assert "P01116" in results
        assert results["P01116"] is not None
        assert "error" in results["P01116"]

    def test_empty_id_skipped(self, tmp_cache: Any) -> None:
        with patch("rcsb_pipeline.fetch._execute_uniprot_query") as mock_exec:
            results = fetch_uniprot_data(
                uniprot_ids=["", "P01116"],
                field_paths=["uniprot.rcsb_id"],
                cache=tmp_cache,
            )

        mock_exec.assert_called_once()
        assert "" not in results
        assert "P01116" in results

    def test_no_uniprot_ids(self, tmp_cache: Any) -> None:
        results = fetch_uniprot_data([], [], cache=tmp_cache)
        assert results == {}

    def test_progress_callback(self, tmp_cache: Any) -> None:
        from rich.progress import Progress

        with (
            patch("rcsb_pipeline.fetch._execute_uniprot_query", return_value={"P01116": {"rcsb_id": "P01116"}}),
            Progress() as progress,
        ):
            results = fetch_uniprot_data(
                uniprot_ids=["P01116"],
                field_paths=["uniprot.rcsb_id"],
                cache=tmp_cache,
                progress=progress,
            )

        assert "P01116" in results


# ── save_raw_data ──


class TestSaveRawData:
    def test_save_basic(self, tmp_path: Path) -> None:
        entry_data = {"4LPK": {"rcsb_id": "4LPK"}}
        uniprot_data = {"P01116": {"rcsb_id": "P01116"}}

        save_raw_data(entry_data, uniprot_data, str(tmp_path))  # type: ignore[arg-type]

        entry_path = tmp_path / "raw" / "entry_data.json"
        uniprot_path = tmp_path / "raw" / "uniprot_data.json"

        assert entry_path.exists()
        assert uniprot_path.exists()

        with open(entry_path) as f:
            assert json.load(f) == entry_data
        with open(uniprot_path) as f:
            assert json.load(f) == uniprot_data

    def test_save_none_values_filtered(self, tmp_path: Path) -> None:
        entry_data = {"4LPK": None, "5P21": {"rcsb_id": "5P21"}}
        save_raw_data(entry_data, {}, str(tmp_path))

        entry_path = tmp_path / "raw" / "entry_data.json"
        with open(entry_path) as f:
            loaded = json.load(f)
        assert "4LPK" not in loaded  # None values filtered
        assert "5P21" in loaded

    def test_save_creates_directory(self, tmp_path: Path) -> None:
        nested = tmp_path / "a" / "b"
        save_raw_data({"4LPK": {"rcsb_id": "4LPK"}}, {}, str(nested))
        assert (nested / "raw" / "entry_data.json").exists()

    def test_save_empty(self, tmp_path: Path) -> None:
        save_raw_data({}, {}, str(tmp_path))
        entry_path = tmp_path / "raw" / "entry_data.json"
        uniprot_path = tmp_path / "raw" / "uniprot_data.json"
        assert entry_path.exists()
        assert uniprot_path.exists()
        with open(entry_path) as f:
            assert json.load(f) == {}
