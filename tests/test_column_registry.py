"""Tests for the ColumnRegistry (column_registry.py)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from rcsb_pipeline.column_registry import ColumnRegistry
from rcsb_pipeline.config import FieldConfig


@pytest.fixture
def registry() -> ColumnRegistry:
    """Create a ColumnRegistry with minimal sample data only (no built-in)."""
    with patch("rcsb_pipeline.column_registry._builtin_path") as mock_path:
        mock_path.return_value = Path("/nonexistent/columns.yaml")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
columns:
  rcsb_id:
    path: entry.rcsb_id
    type: String
    category: Entry
    description: PDB identifier
  resolution:
    path: entry.rcsb_entry_info.resolution_combined
    type: Float
    category: Entry
    description: Resolution
  method:
    path: entry.rcsb_entry_info.experimental_method
    type: String
    is_list: true
    category: Experimental Data (X-ray)
    description: Experimental method
  sequence:
    path: uniprot.rcsb_uniprot_protein.sequence
    type: String
    category: UniProt Integration
    description: Protein sequence
""")
            yaml_path = f.name
        reg = ColumnRegistry(column_file=yaml_path)
        Path(yaml_path).unlink()
    return reg


class TestColumnRegistryInit:
    def test_init_with_custom_file(self, registry: ColumnRegistry) -> None:
        assert registry.count == 4

    def test_init_with_nonexistent_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            ColumnRegistry(column_file="/nonexistent/path.yaml")

    def test_init_with_invalid_file_raises(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("not_a_yaml: [")
            yaml_path = f.name
        with pytest.raises(yaml.YAMLError):
            ColumnRegistry(column_file=yaml_path)
        Path(yaml_path).unlink()

    def test_init_with_file_missing_columns_key(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("foo: bar\n")
            yaml_path = f.name
        with pytest.raises(ValueError, match="missing 'columns' key"):
            ColumnRegistry(column_file=yaml_path)
        Path(yaml_path).unlink()

    def test_available(self, registry: ColumnRegistry) -> None:
        names = registry.available
        assert "rcsb_id" in names
        assert "resolution" in names
        assert isinstance(names, list)
        # Must be sorted
        assert names == sorted(names)


class TestColumnRegistryResolve:
    def test_resolve_single(self, registry: ColumnRegistry) -> None:
        paths = registry.resolve(["rcsb_id"])
        assert paths == ["entry.rcsb_id"]

    def test_resolve_multiple(self, registry: ColumnRegistry) -> None:
        paths = registry.resolve(["rcsb_id", "resolution"])
        assert paths == ["entry.rcsb_id", "entry.rcsb_entry_info.resolution_combined"]

    def test_resolve_all(self, registry: ColumnRegistry) -> None:
        paths = registry.resolve(["rcsb_id", "resolution", "method", "sequence"])
        assert len(paths) == 4

    def test_resolve_unknown_raises(self, registry: ColumnRegistry) -> None:
        with pytest.raises(KeyError, match="Unknown column 'nonexistent'"):
            registry.resolve(["nonexistent"])

    def test_resolve_empty_list(self, registry: ColumnRegistry) -> None:
        assert registry.resolve([]) == []

    def test_get_existing(self, registry: ColumnRegistry) -> None:
        info = registry.get("rcsb_id")
        assert info is not None
        assert info["path"] == "entry.rcsb_id"

    def test_get_nonexistent(self, registry: ColumnRegistry) -> None:
        assert registry.get("nonexistent") is None


class TestColumnRegistrySearch:
    def test_search_by_name(self, registry: ColumnRegistry) -> None:
        results = registry.search("resolution")
        assert len(results) >= 1
        names = [r["name"] for r in results]
        assert "resolution" in names

    def test_search_by_path(self, registry: ColumnRegistry) -> None:
        results = registry.search("protein.sequence")
        assert len(results) >= 1
        assert any("sequence" in r["name"] for r in results)

    def test_search_by_description(self, registry: ColumnRegistry) -> None:
        results = registry.search("identifier")
        assert len(results) >= 1
        assert any(r["name"] == "rcsb_id" for r in results)

    def test_search_no_match(self, registry: ColumnRegistry) -> None:
        assert registry.search("zzz_nonexistent_zzz") == []

    def test_search_is_case_insensitive(self, registry: ColumnRegistry) -> None:
        upper = registry.search("RESOLUTION")
        lower = registry.search("resolution")
        assert len(upper) == len(lower)
        assert upper == lower


class TestColumnRegistryFilter:
    def test_filter_by_category(self, registry: ColumnRegistry) -> None:
        results = registry.filter_by_category("Entry")
        assert len(results) >= 2
        names = {r["name"] for r in results}
        assert "rcsb_id" in names
        assert "resolution" in names

    def test_filter_by_category_case_insensitive(self, registry: ColumnRegistry) -> None:
        upper = registry.filter_by_category("ENTRY")
        lower = registry.filter_by_category("entry")
        assert upper == lower

    def test_filter_by_category_nonexistent(self, registry: ColumnRegistry) -> None:
        assert registry.filter_by_category("NonexistentCategory") == []

    def test_list_categories(self, registry: ColumnRegistry) -> None:
        cats = registry.list_categories()
        assert isinstance(cats, list)
        assert len(cats) >= 1
        cat_names = {c["category"] for c in cats}
        assert "Entry" in cat_names
        for c in cats:
            assert "category" in c
            assert "count" in c
            assert c["count"] is not None


class TestColumnRegistryToFieldConfig:
    def test_to_field_config_sets_preset_custom(self, registry: ColumnRegistry) -> None:
        cfg = registry.to_field_config(["rcsb_id", "resolution"])
        assert isinstance(cfg, FieldConfig)
        assert cfg.preset == "custom"

    def test_to_field_config_populates_include(self, registry: ColumnRegistry) -> None:
        cfg = registry.to_field_config(["rcsb_id", "resolution"])
        expected = ["entry.rcsb_id", "entry.rcsb_entry_info.resolution_combined"]
        assert cfg.include == expected

    def test_to_field_config_stores_names(self, registry: ColumnRegistry) -> None:
        cfg = registry.to_field_config(["rcsb_id", "resolution"])
        assert cfg.columns == ["rcsb_id", "resolution"]

    def test_to_field_config_empty(self, registry: ColumnRegistry) -> None:
        cfg = registry.to_field_config([])
        assert cfg.include == []


class TestColumnRegistryOverlay:
    def test_custom_file_overrides_builtin(self) -> None:
        """When custom file provides same name, it should merge/override."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
columns:
  rcsb_id:
    path: entry.custom_id
    type: String
    category: Custom
    description: Overridden
""")
            yaml_path = f.name
        # This will load builtin columns first, then overlay
        reg = ColumnRegistry(column_file=yaml_path)
        info = reg.get("rcsb_id")
        # The overlay overwrites the built-in entry
        assert info is not None
        assert info["path"] == "entry.custom_id"
        Path(yaml_path).unlink()
