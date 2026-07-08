"""Shared test fixtures for the rcsb-pipeline test suite."""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from rcsb_pipeline.cache import ResponseCache
from rcsb_pipeline.registry import ProcessedRegistry

# ── Registry fixtures ──


@pytest.fixture
def tmp_registry() -> Generator[ProcessedRegistry, None, None]:
    """Create a ProcessedRegistry backed by a temporary SQLite database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    reg = ProcessedRegistry(db_path)
    yield reg
    reg.close()
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def populated_registry(tmp_registry: ProcessedRegistry) -> ProcessedRegistry:
    """Registry with sample records pre-inserted."""
    pairs = [
        ("P01116", "4LPK"),
        ("P01116", "5P21"),
        ("P04637", "1TUP"),
        ("P04637", "2OCJ"),
    ]
    tmp_registry.record_batch(
        pairs,
        run_id="test-run-001",
        preset="standard",
        granularity="per-structure",
        output_dir="/tmp/test-out",
    )
    # Mark one stale
    tmp_registry.mark_stale(uniprot_ids=["P04637"])
    return tmp_registry


# ── Cache fixture ──


@pytest.fixture
def tmp_cache() -> Generator[ResponseCache, None, None]:
    """Create a ResponseCache with a temporary database."""
    with tempfile.NamedTemporaryFile(suffix=".cache.db", delete=False) as f:
        db_path = f.name
    cache = ResponseCache(db_path)
    yield cache
    cache.close()
    Path(db_path).unlink(missing_ok=True)


# ── Mock schema data ──


@pytest.fixture
def mock_raw_schema() -> dict[str, Any]:
    """A minimal GraphQL schema shape that exercises SchemaLoader."""
    return {
        "data": {
            "__schema": {
                "types": [
                    {
                        "name": "QueryRoot",
                        "kind": "OBJECT",
                        "description": "Root query type",
                        "fields": [
                            {
                                "name": "entry",
                                "description": "PDB entry",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "CoreEntry",
                                    "ofType": None,
                                },
                                "deprecation": None,
                            },
                            {
                                "name": "uniprot",
                                "description": "UniProt entry",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "CoreUniprot",
                                    "ofType": None,
                                },
                                "deprecation": None,
                            },
                        ],
                    },
                    {
                        "name": "CoreEntry",
                        "kind": "OBJECT",
                        "description": "Core PDB entry",
                        "fields": [
                            {
                                "name": "rcsb_id",
                                "description": "PDB ID",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
                                },
                            },
                            {
                                "name": "rcsb_entry_info",
                                "description": "Entry metadata",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "RcsbEntryInfo",
                                    "ofType": None,
                                },
                            },
                        ],
                    },
                    {
                        "name": "RcsbEntryInfo",
                        "kind": "OBJECT",
                        "description": "Entry info",
                        "fields": [
                            {
                                "name": "resolution_combined",
                                "description": "Resolution",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "Float",
                                    "ofType": None,
                                },
                            },
                            {
                                "name": "experimental_method",
                                "description": "Method",
                                "args": [],
                                "type": {
                                    "kind": "LIST",
                                    "name": None,
                                    "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
                                },
                            },
                        ],
                    },
                    {
                        "name": "CoreUniprot",
                        "kind": "OBJECT",
                        "description": "UniProt entry",
                        "fields": [
                            {
                                "name": "rcsb_id",
                                "description": "UniProt ID",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "ofType": {"kind": "SCALAR", "name": "String", "ofType": None},
                                },
                            },
                            {
                                "name": "rcsb_uniprot_protein",
                                "description": "Protein info",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "RcsbUniprotProtein",
                                    "ofType": None,
                                },
                            },
                        ],
                    },
                    {
                        "name": "RcsbUniprotProtein",
                        "kind": "OBJECT",
                        "description": "UniProt protein",
                        "fields": [
                            {
                                "name": "name",
                                "description": "Protein name",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                            },
                            {
                                "name": "sequence",
                                "description": "Sequence",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                            },
                        ],
                    },
                    {
                        "name": "String",
                        "kind": "SCALAR",
                        "description": "Built-in String",
                        "fields": None,
                    },
                    {
                        "name": "Float",
                        "kind": "SCALAR",
                        "description": "Built-in Float",
                        "fields": None,
                    },
                ],
            }
        }
    }


# ── Mock RCSB search / data API response data ──


@pytest.fixture
def mock_search_results() -> list[str]:
    return ["4LPK", "5P21", "6Q21"]


@pytest.fixture
def mock_entry_data() -> dict[str, Any]:
    return {
        "4LPK": {
            "rcsb_id": "4LPK",
            "rcsb_entry_info": {
                "resolution_combined": 1.5,
                "experimental_method": ["X-RAY DIFFRACTION"],
            },
        },
        "5P21": {
            "rcsb_id": "5P21",
            "rcsb_entry_info": {
                "resolution_combined": 2.0,
                "experimental_method": ["X-RAY DIFFRACTION"],
            },
        },
    }


@pytest.fixture
def mock_uniprot_data() -> dict[str, Any]:
    return {
        "P01116": {
            "rcsb_id": "P01116",
            "rcsb_uniprot_protein": {
                "name": "GTPase KRas",
                "sequence": "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQRVEDAFYTLVREIRQYRLKKISKEEKTPGCVKIKKCIIM",
            },
        },
    }


# ── Sample DataFrames ──


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "uniprot_id": ["P01116", "P01116", "P04637"],
            "pdb_id": ["4LPK", "5P21", "1TUP"],
            "resolution": [1.5, 2.0, 2.3],
        }
    )


# ── Column registry test data ──


@pytest.fixture
def sample_columns_yaml() -> str:
    return """
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
"""
