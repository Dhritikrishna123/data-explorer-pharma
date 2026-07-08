"""Smoke tests for the rcsb-pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from rcsb_pipeline.cache import ResponseCache
from rcsb_pipeline.config import RcsbPipelineConfig, load_preset
from rcsb_pipeline.export import (
    export_dataset,
    report_coverage,
    report_duplicates,
    report_field_coverage,
    report_missing_data,
)
from rcsb_pipeline.transform import (
    aggregate_protein_rows,
    deduplicate,
    handle_missing,
    sanitize,
)


def test_load_minimal_preset() -> None:
    cfg = load_preset("minimal")
    assert cfg is not None
    assert "entry.rcsb_id" in cfg.include


def test_load_standard_preset() -> None:
    cfg = load_preset("standard")
    assert cfg is not None
    assert len(cfg.include) > 0


def test_load_full_preset() -> None:
    cfg = load_preset("full")
    assert cfg is not None
    assert cfg.preset == "full"
    assert cfg.include == []


def test_config_from_yaml(tmp_path: Path) -> None:
    p = tmp_path / "test.yaml"
    p.write_text("""
pipeline:
  max_concurrent: 3
  rate_limit: 0.5
input:
  uniprots: ["P01116"]
discovery:
  max_entries: 50
output:
  directory: /tmp/out
  formats: [csv]
""")
    cfg = RcsbPipelineConfig.from_yaml(str(p))
    assert cfg.pipeline.max_concurrent == 3
    assert cfg.input.uniprots == ["P01116"]
    assert cfg.discovery.max_entries == 50
    assert cfg.output.formats == ["csv"]


def test_cache(tmp_path: Path) -> None:
    cache = ResponseCache(str(tmp_path / "cache"))
    cache.set("test_key", {"foo": "bar"})
    result = cache.get("test_key")
    assert result == {"foo": "bar"}
    assert cache.get("nonexistent") is None


def test_deduplicate_strict() -> None:
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = deduplicate(df, strategy="strict")
    assert len(result) == 2


def test_deduplicate_key_only() -> None:
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "y", "z"]})
    result = deduplicate(df, strategy="key-only", keys=["a"])
    assert len(result) == 2


def test_deduplicate_none() -> None:
    df = pd.DataFrame({"a": [1, 1, 2]})
    result = deduplicate(df, strategy="none")
    assert len(result) == 3


def test_handle_missing_drop() -> None:
    df = pd.DataFrame({"a": [1, None, 3]})
    result = handle_missing(df, strategy="drop")
    assert len(result) == 2


def test_handle_missing_fill_zero() -> None:
    df = pd.DataFrame({"a": [1, None, 3]})
    result = handle_missing(df, strategy="fill-0")
    assert result["a"].iloc[1] == 0


def test_handle_missing_fill_null() -> None:
    df = pd.DataFrame({"a": [1, None, 3]})
    result = handle_missing(df, strategy="fill-null")
    assert pd.isna(result["a"].iloc[1])


def test_aggregate_pick_best() -> None:
    df = pd.DataFrame(
        {
            "uniprot_id": ["P1", "P1", "P2"],
            "resolution": [2.0, 1.5, 3.0],
        }
    )
    result = aggregate_protein_rows(df, group_key="uniprot_id", mode="pick-best", sort_key="resolution")
    assert len(result) == 2
    p1_row = result[result["uniprot_id"] == "P1"]
    assert p1_row["resolution"].iloc[0] == 1.5


def test_aggregate_concat() -> None:
    df = pd.DataFrame(
        {
            "uniprot_id": ["P1", "P1"],
            "chain": ["A", "B"],
        }
    )
    result = aggregate_protein_rows(df, group_key="uniprot_id", mode="concat")
    assert len(result) == 1
    assert "A" in result["chain"].iloc[0]
    assert "B" in result["chain"].iloc[0]


def test_sanitize_basic() -> None:
    df = pd.DataFrame(
        {
            "uniprot_id": ["P1", "P1", "P2"],
            "pdb_id": ["1ABC", "1ABC", "2XYZ"],
            "resolution": [2.0, 2.0, 3.0],
        }
    )
    result = sanitize(df, {"dedup_strategy": "strict", "missing_action": "fill-null", "granularity": "per-structure"})
    assert len(result) == 2
    assert result.columns.tolist() == ["uniprot_id", "pdb_id", "resolution"]


def test_export_csv(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    result = export_dataset(df, str(tmp_path), formats=["csv"])
    assert "csv" in result
    assert Path(result["csv"]).exists()


def test_export_parquet(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    result = export_dataset(df, str(tmp_path), formats=["parquet"])
    assert "parquet" in result
    assert Path(result["parquet"]).exists()


def test_export_json(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    result = export_dataset(df, str(tmp_path), formats=["json"])
    assert "json" in result
    assert Path(result["json"]).exists()


def test_export_xlsx(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    result = export_dataset(df, str(tmp_path), formats=["xlsx"])
    assert "xlsx" in result
    assert Path(result["xlsx"]).exists()


def test_report_missing_data(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", None]})
    path = report_missing_data(df, str(tmp_path))
    assert Path(path).exists()


def test_report_duplicates(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    path = report_duplicates(df, str(tmp_path))
    assert Path(path).exists()


def test_report_field_coverage(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    path = report_field_coverage(df, str(tmp_path))
    assert Path(path).exists()


def test_report_coverage(tmp_path: Path) -> None:
    df = pd.DataFrame({"uniprot_id": ["P1", "P1"], "pdb_id": ["1ABC", "2XYZ"]})
    path = report_coverage(df, output_dir=str(tmp_path))
    assert Path(path).exists()


def test_sanitize_with_unhashable() -> None:
    df = pd.DataFrame(
        {
            "uniprot_id": ["P1", "P1"],
            "nested": [{"foo": "bar"}, {"foo": "bar"}],
        }
    )
    result = sanitize(df, {"dedup_strategy": "strict", "missing_action": "fill-null", "granularity": "per-structure"})
    assert len(result) == 1


def test_cli_help() -> None:
    from typer.testing import CliRunner

    from rcsb_pipeline.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output
    assert "discover" in result.output


def test_cli_init_config(tmp_path: Path) -> None:
    from typer.testing import CliRunner

    from rcsb_pipeline.cli import app

    p = tmp_path / "test_config.yaml"
    runner = CliRunner()
    result = runner.invoke(app, ["init-config", str(p)])
    assert result.exit_code == 0
    assert p.exists()
