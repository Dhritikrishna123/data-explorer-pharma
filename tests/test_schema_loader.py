"""Tests for the SchemaLoader (schema_loader.py).

Uses a mock schema to avoid hitting the live RCSB GraphQL API."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rcsb_pipeline.schema_loader import SchemaLoader, _resolve_type, discover_available_fields


class TestResolveType:
    def test_simple_scalar(self) -> None:
        t = {"kind": "SCALAR", "name": "String", "ofType": None}
        name, kind, nullable, is_list = _resolve_type(t)
        assert name == "String"
        assert kind == "SCALAR"
        assert nullable is True
        assert is_list is False

    def test_non_null_scalar(self) -> None:
        t = {
            "kind": "NON_NULL",
            "name": None,
            "ofType": {"kind": "SCALAR", "name": "Float", "ofType": None},
        }
        name, kind, nullable, is_list = _resolve_type(t)
        assert name == "Float"
        assert nullable is False

    def test_list_of_scalar(self) -> None:
        t = {
            "kind": "LIST",
            "name": None,
            "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
        }
        name, kind, nullable, is_list = _resolve_type(t)
        assert name == "String"
        assert is_list is True

    def test_non_null_list_of_non_null_scalar(self) -> None:
        t = {
            "kind": "NON_NULL",
            "name": None,
            "ofType": {
                "kind": "LIST",
                "name": None,
                "ofType": {
                    "kind": "NON_NULL",
                    "name": None,
                    "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
                },
            },
        }
        name, kind, nullable, is_list = _resolve_type(t)
        assert name == "String"
        assert nullable is False
        assert is_list is True


class TestSchemaLoader:
    @pytest.fixture
    def loader(self, mock_raw_schema: dict[str, Any]) -> SchemaLoader:
        with patch("rcsb_pipeline.schema_loader.DataSchema") as mock_schema_class:
            mock_schema = MagicMock()
            mock_schema.schema = mock_raw_schema
            mock_schema_class.return_value = mock_schema
            loader = SchemaLoader()
        return loader

    def test_list_object_types(self, loader: SchemaLoader) -> None:
        types = loader.list_object_types()
        assert "CoreEntry" in types
        assert "CoreUniprot" in types
        assert "RcsbEntryInfo" in types
        assert "RcsbUniprotProtein" in types
        # Built-in types and __ prefixed should be excluded
        assert "String" not in types
        assert "Float" not in types

    def test_get_fields_for_type_found(self, loader: SchemaLoader) -> None:
        fields = loader.get_fields_for_type("CoreEntry")
        assert len(fields) == 2
        names = {f["name"] for f in fields}
        assert "rcsb_id" in names
        assert "rcsb_entry_info" in names

    def test_get_fields_for_type_not_found(self, loader: SchemaLoader) -> None:
        fields = loader.get_fields_for_type("NonExistentType")
        assert fields == []

    def test_get_fields_resolved_types(self, loader: SchemaLoader) -> None:
        fields = loader.get_fields_for_type("CoreEntry")
        field_map = {f["name"]: f for f in fields}
        rcsb_id = field_map["rcsb_id"]
        assert rcsb_id["type"] == "String"
        assert rcsb_id["nullable"] is False
        assert rcsb_id["is_list"] is False

        entry_info = field_map["rcsb_entry_info"]
        assert entry_info["type"] == "RcsbEntryInfo"
        assert entry_info["nullable"] is True

    def test_get_fields_list_type(self, loader: SchemaLoader) -> None:
        fields = loader.get_fields_for_type("RcsbEntryInfo")
        field_map = {f["name"]: f for f in fields}
        meth = field_map["experimental_method"]
        assert meth["is_list"] is True
        assert meth["type"] == "String"

    def test_search_fields_hit(self, loader: SchemaLoader) -> None:
        results = loader.search_fields("resolution")
        assert len(results) >= 1
        assert any(r["field_name"] == "resolution_combined" for r in results)

    def test_search_fields_miss(self, loader: SchemaLoader) -> None:
        results = loader.search_fields("zzz_nonexistent_zzz")
        assert results == []

    def test_search_fields_is_case_insensitive(self, loader: SchemaLoader) -> None:
        results_upper = loader.search_fields("RESOLUTION")
        results_lower = loader.search_fields("resolution")
        assert len(results_upper) == len(results_lower)

    def test_field_exists_true(self, loader: SchemaLoader) -> None:
        assert loader.field_exists("CoreEntry.rcsb_id")

    def test_field_exists_false(self, loader: SchemaLoader) -> None:
        assert not loader.field_exists("CoreEntry.nonexistent")

    def test_field_exists_short_path(self, loader: SchemaLoader) -> None:
        assert not loader.field_exists("rcsb_id")  # need at least 2 parts

    def test_resolve_field_path_found(self, loader: SchemaLoader) -> None:
        result = loader.resolve_field_path("CoreEntry.rcsb_id")
        assert result is not None
        assert result["object"] == "CoreEntry"
        assert result["field"]["name"] == "rcsb_id"

    def test_resolve_field_path_not_found(self, loader: SchemaLoader) -> None:
        assert loader.resolve_field_path("CoreEntry.garbage") is None

    def test_resolve_field_path_short(self, loader: SchemaLoader) -> None:
        assert loader.resolve_field_path("rcsb_id") is None


class TestDiscoverAvailableFields:
    def test_full_preset_uses_schema_loader(self, mock_raw_schema: dict[str, Any]) -> None:
        with patch("rcsb_pipeline.schema_loader.DataSchema") as mock_schema_class:
            mock_schema = MagicMock()
            mock_schema.schema = mock_raw_schema
            mock_schema_class.return_value = mock_schema
            paths = discover_available_fields("full")
        # Should include all fields from all object types
        assert "CoreEntry.rcsb_id" in paths
        assert "RcsbEntryInfo.resolution_combined" in paths

    def test_standard_preset_returns_includes(self) -> None:
        paths = discover_available_fields("standard")
        assert isinstance(paths, list)
        assert len(paths) > 0

    def test_custom_includes_merged(self) -> None:
        paths = discover_available_fields("standard", custom_includes=["entry.test_field"])
        assert "entry.test_field" in paths

    def test_custom_excludes_filtered(self) -> None:
        paths = discover_available_fields("standard", custom_excludes=["entry.rcsb_id"])
        assert "entry.rcsb_id" not in paths
