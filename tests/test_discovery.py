"""Tests for the discovery layer (discovery.py).

Uses mocked RCSB Search API and MyGene.info to avoid external calls."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from rcsb_pipeline.discovery import (
    discover_pdb_ids,
    resolve_gene_symbols,
    save_discovery_results,
)

# ── discover_pdb_ids ──


class TestDiscoverPdbIds:
    def test_discover_hits(self, tmp_cache: Any, mock_search_results: list[str]) -> None:
        mock_data = MagicMock()
        mock_data.return_value = iter(mock_search_results)

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )

        assert "P01116" in uniprot_to_pdbs
        assert uniprot_to_pdbs["P01116"] == ["4LPK", "5P21", "6Q21"]

    def test_discover_multiple_uniprots(self, tmp_cache: Any, mock_search_results: list[str]) -> None:
        mock_data = MagicMock()
        mock_data.return_value = iter(mock_search_results)

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116", "P04637"],
                cache=tmp_cache,
            )

        assert len(uniprot_to_pdbs) == 2

    def test_discover_with_cache_hit(self, tmp_cache: Any) -> None:
        """Cached results should be returned without calling the API."""
        tmp_cache.set("discover:P01116", ["4LPK", "5P21"])

        with patch("rcsbapi.search.NestedAttributeQuery") as mock_query:
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )
            mock_query.assert_not_called()

        assert uniprot_to_pdbs["P01116"] == ["4LPK", "5P21"]

    def test_discover_no_results(self, tmp_cache: Any) -> None:
        mock_data = MagicMock()
        mock_data.return_value = iter([])

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )

        assert uniprot_to_pdbs["P01116"] == []

    def test_discover_api_error(self, tmp_cache: Any) -> None:
        with patch("rcsbapi.search.AttributeQuery", side_effect=Exception("API Error")):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )

        # On error, should return empty list (bare except swallows)
        assert uniprot_to_pdbs["P01116"] == []

    def test_discover_deduplicates_across_uniprots(self, tmp_cache: Any) -> None:
        """If two UniProts return the same PDB ID, it should not be duplicated."""
        mock_data = MagicMock()
        mock_data.return_value = iter(["4LPK", "5P21"])

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116", "P04637"],
                cache=tmp_cache,
            )

        # First uniprot gets the PDB IDs, second has none left (deduplicated)
        assert set(uniprot_to_pdbs["P01116"]) == {"4LPK", "5P21"}
        assert uniprot_to_pdbs["P04637"] == []

    def test_discover_empty_uniprot_stripped(self, tmp_cache: Any) -> None:
        with patch("rcsbapi.search.AttributeQuery") as mock_query:
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["", "P01116", "  "],
                cache=tmp_cache,
            )
            assert mock_query.called

    def test_discover_dict_item_with_entry_id(self, tmp_cache: Any) -> None:
        """When search results contain dicts with entry_id key."""
        mock_data = MagicMock()
        mock_data.return_value = iter([{"entry_id": "4LPK"}, {"entry_id": "5P21"}])

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )

        assert uniprot_to_pdbs["P01116"] == ["4LPK", "5P21"]

    def test_discover_nonnlist_result(self, tmp_cache: Any) -> None:
        """If the API returns a non-list (e.g. the iterator exhausted), handle gracefully."""
        mock_data = MagicMock()
        mock_data.return_value = iter("STRING_NOT_A_LIST")

        with (
            patch("rcsbapi.search.AttributeQuery", return_value=MagicMock()),
            patch("rcsbapi.search.NestedAttributeQuery", return_value=mock_data),
        ):
            uniprot_to_pdbs, raw = discover_pdb_ids(
                uniprot_ids=["P01116"],
                cache=tmp_cache,
            )

        assert "P01116" in uniprot_to_pdbs


# ── resolve_gene_symbols ──


class TestResolveGeneSymbols:
    def test_resolve_gene_hit(self, tmp_cache: Any) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hits": [{"uniprot": {"Swiss-Prot": "P01116"}}],
        }

        with patch("requests.get", return_value=mock_response):
            result = resolve_gene_symbols(["KRAS"], tmp_cache)

        assert result == {"KRAS": "P01116"}

    def test_resolve_gene_multiple(self, tmp_cache: Any) -> None:
        def mock_get(_url, **kwargs):
            resp = MagicMock()
            params = kwargs.get("params", {})
            q = params.get("q", "")
            if q == "KRAS":
                resp.json.return_value = {"hits": [{"uniprot": {"Swiss-Prot": "P01116"}}]}
            elif q == "TP53":
                resp.json.return_value = {"hits": [{"uniprot": {"Swiss-Prot": "P04637"}}]}
            else:
                resp.json.return_value = {"hits": []}
            return resp

        with patch("requests.get", side_effect=mock_get):
            result = resolve_gene_symbols(["KRAS", "TP53"], tmp_cache)

        assert result == {"KRAS": "P01116", "TP53": "P04637"}

    def test_resolve_gene_no_hits(self, tmp_cache: Any) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"hits": []}

        with patch("requests.get", return_value=mock_response):
            result = resolve_gene_symbols(["NONEXISTENT"], tmp_cache)

        assert result == {}

    def test_resolve_gene_cached(self, tmp_cache: Any) -> None:
        tmp_cache.set("gene:KRAS", "P01116")

        with patch("requests.get") as mock_get:
            result = resolve_gene_symbols(["KRAS"], tmp_cache)
            mock_get.assert_not_called()

        assert result == {"KRAS": "P01116"}

    def test_resolve_gene_cached_empty(self, tmp_cache: Any) -> None:
        """When a gene was cached as empty (unresolvable), skip it."""
        tmp_cache.set("gene:NONEXISTENT", "")

        with patch("requests.get") as mock_get:
            result = resolve_gene_symbols(["NONEXISTENT"], tmp_cache)
            mock_get.assert_not_called()

        assert result == {}

    def test_resolve_gene_api_error(self, tmp_cache: Any) -> None:
        with patch("requests.get", side_effect=Exception("Network error")):
            result = resolve_gene_symbols(["KRAS"], tmp_cache)

        assert result == {}

    def test_resolve_empty_symbol_skipped(self, tmp_cache: Any) -> None:
        with patch("requests.get") as mock_get:
            resolve_gene_symbols(["", "KRAS"], tmp_cache)
            assert mock_get.called

    def test_resolve_gene_hit_with_trembl(self, tmp_cache: Any) -> None:
        """If Swiss-Prot is missing, fall back to TrEMBL."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hits": [{"uniprot": {"TrEMBL": "A0A0A0MRZ1"}}],
        }

        with patch("requests.get", return_value=mock_response):
            result = resolve_gene_symbols(["KRAS"], tmp_cache)

        assert result == {"KRAS": "A0A0A0MRZ1"}


# ── save_discovery_results ──


class TestSaveDiscoveryResults:
    def test_save_basic(self, tmp_path: Path) -> None:
        data = {"P01116": ["4LPK", "5P21"], "P04637": ["1TUP"]}
        save_discovery_results(data, str(tmp_path))

        # Check discovered_pdb_ids.json
        path = tmp_path / "discovered_pdb_ids.json"
        assert path.exists()
        with open(path) as f:
            loaded = json.load(f)
        assert loaded == data

        # Check all_pdb_ids.json
        all_path = tmp_path / "all_pdb_ids.json"
        assert all_path.exists()
        with open(all_path) as f:
            all_pdbs = json.load(f)
        assert all_pdbs == ["1TUP", "4LPK", "5P21"]  # sorted

        # Check discovery_summary.json
        summary_path = tmp_path / "discovery_summary.json"
        assert summary_path.exists()
        with open(summary_path) as f:
            summary = json.load(f)
        assert summary["total_uniprots"] == 2
        assert summary["total_pdb_ids"] == 3

    def test_save_empty_uniprots(self, tmp_path: Path) -> None:
        save_discovery_results({}, str(tmp_path))
        summary_path = tmp_path / "discovery_summary.json"
        with open(summary_path) as f:
            summary = json.load(f)
        assert summary["total_uniprots"] == 0
        assert summary["total_pdb_ids"] == 0

    def test_save_uniprots_without_structures(self, tmp_path: Path) -> None:
        data = {"P01116": ["4LPK"], "Q99999": []}
        save_discovery_results(data, str(tmp_path))
        summary_path = tmp_path / "discovery_summary.json"
        with open(summary_path) as f:
            summary = json.load(f)
        assert summary["uniprots_with_structures"] == 1
        assert summary["uniprots_without_structures"] == 1

    def test_save_creates_directory(self, tmp_path: Path) -> None:
        nested = tmp_path / "a" / "b" / "c"
        save_discovery_results({"P01116": ["4LPK"]}, str(nested))
        assert (nested / "discovered_pdb_ids.json").exists()
