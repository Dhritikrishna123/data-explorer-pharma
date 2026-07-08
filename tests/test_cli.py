"""Tests for CLI commands (cli.py).

Uses typer.testing.CliRunner with mocked API/RCSB calls."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from typer.testing import CliRunner

from rcsb_pipeline import discovery as disc_mod
from rcsb_pipeline import fetch as fetch_mod
from rcsb_pipeline.cli import app


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ── Mock helpers ──


def _mock_discover(*_args, **_kwargs):
    return {"P01116": ["4LPK", "5P21"]}, [{"uniprot_id": "P01116", "result": ["4LPK", "5P21"]}]


def _mock_fetch_entry(*_args, **_kwargs):
    return {"4LPK": {"rcsb_id": "4LPK"}, "5P21": {"rcsb_id": "5P21"}}


def _mock_fetch_uniprot(*_args, **_kwargs):
    return {"P01116": {"rcsb_id": "P01116"}}


def _mock_fetch_entry_with_data(*_args, **_kwargs):
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


def _mock_fetch_uniprot_with_data(*_args, **_kwargs):
    return {
        "P01116": {
            "rcsb_id": "P01116",
            "rcsb_uniprot_protein": {
                "name": "GTPase KRas",
                "sequence": "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQRVEDAFYTLVREIRQYRLKKISKEEKTPGCVKIKKCIIM",
            },
        },
    }


# ── CLI test class ──


class TestCliHelp:
    def test_main_help(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "run" in result.output
        assert "discover" in result.output
        assert "fetch" in result.output
        assert "columns" in result.output
        assert "report" in result.output
        assert "validate" in result.output
        assert "init-config" in result.output
        assert "registry" in result.output

    def test_invalid_command(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["nonexistent"])
        assert result.exit_code != 0


class TestCliRun:
    def test_run_no_input(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["run"])
        assert result.exit_code != 0
        assert "No input provided" in result.output

    def test_run_with_uniprots(self, runner: CliRunner, tmp_path: Path) -> None:
        output = str(tmp_path / "output")
        with (
            patch.object(disc_mod, "discover_pdb_ids", side_effect=_mock_discover),
            patch.object(fetch_mod, "fetch_entry_data", side_effect=_mock_fetch_entry),
            patch.object(fetch_mod, "fetch_uniprot_data", side_effect=_mock_fetch_uniprot),
        ):
            result = runner.invoke(
                app,
                [
                    "run",
                    "--uniprots",
                    "P01116",
                    "--output",
                    output,
                    "--preset",
                    "standard",
                ],
            )

        assert Path(output).exists()
        assert (Path(output) / "final_dataset.csv").exists() or "complete" in result.output.lower()

    def test_run_with_columns(self, runner: CliRunner, tmp_path: Path) -> None:
        """Run with --columns flag to test column resolution."""
        output = str(tmp_path / "columns_out")
        with (
            patch.object(disc_mod, "discover_pdb_ids", side_effect=_mock_discover),
            patch.object(fetch_mod, "fetch_entry_data", side_effect=_mock_fetch_entry_with_data),
            patch.object(fetch_mod, "fetch_uniprot_data", side_effect=_mock_fetch_uniprot_with_data),
        ):
            result = runner.invoke(
                app,
                [
                    "run",
                    "--uniprots",
                    "P01116",
                    "--output",
                    output,
                    "--columns",
                    "rcsb_id,rcsb_entry_info_resolution_combined,rcsb_entry_info_experimental_method,rcsb_uniprot_protein_sequence",
                    "--max-entries",
                    "1",
                ],
            )

        assert result.exit_code == 0 or "Pipeline complete" in result.output

    def test_run_with_resume(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test the resume from checkpoint path."""
        output = str(tmp_path / "resume_out")
        checkpoint_path = tmp_path / "checkpoint.json"
        checkpoint_path.write_text(
            json.dumps(
                {
                    "stage": "export",
                    "all_uniprots": ["P01116"],
                    "all_pdb_ids": ["4LPK"],
                    "uniprot_to_pdbs": {"P01116": ["4LPK"]},
                    "output_dir": str(output),
                    "rows": 1,
                    "columns": 5,
                    "timestamp": "2025-01-01T00:00:00",
                }
            )
        )

        with (
            patch.object(fetch_mod, "fetch_entry_data", side_effect=_mock_fetch_entry),
            patch.object(fetch_mod, "fetch_uniprot_data", side_effect=_mock_fetch_uniprot),
        ):
            result = runner.invoke(
                app,
                [
                    "run",
                    "--uniprots",
                    "P01116",
                    "--output",
                    output,
                    "--resume",
                    str(checkpoint_path),
                ],
            )

        # Should complete without errors
        assert result.exit_code in (0,)

    def test_run_with_config_file(self, runner: CliRunner, tmp_path: Path) -> None:
        config_path = tmp_path / "config.yaml"
        output = str(tmp_path / "config_out")
        config_path.write_text(f"""
pipeline:
  cache_dir: {tmp_path}/cache
input:
  uniprots: ["P01116"]
output:
  directory: {output}
  formats: [csv]
discovery:
  max_entries: 5
""")
        with (
            patch.object(disc_mod, "discover_pdb_ids", side_effect=_mock_discover),
            patch.object(fetch_mod, "fetch_entry_data", side_effect=_mock_fetch_entry),
            patch.object(fetch_mod, "fetch_uniprot_data", side_effect=_mock_fetch_uniprot),
        ):
            result = runner.invoke(
                app,
                [
                    "run",
                    "--config",
                    str(config_path),
                ],
            )

        assert result.exit_code == 0 or "Pipeline complete" in result.output


class TestCliDiscover:
    def test_discover_no_input(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["discover"])
        assert result.exit_code != 0
        assert "No UniProt IDs provided" in result.output

    def test_discover_with_uniprots(self, runner: CliRunner, tmp_path: Path) -> None:
        with patch.object(disc_mod, "discover_pdb_ids", side_effect=_mock_discover):
            result = runner.invoke(
                app,
                [
                    "discover",
                    "--uniprots",
                    "P01116",
                    "--output",
                    str(tmp_path),
                ],
            )

        assert Path(tmp_path / "discovered_pdb_ids.json").exists()
        assert result.exit_code == 0


class TestCliFetch:
    def test_fetch_no_input(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["fetch"])
        assert result.exit_code != 0
        assert "No PDB IDs provided" in result.output

    def test_fetch_with_pdb_ids(self, runner: CliRunner, tmp_path: Path) -> None:
        with patch.object(fetch_mod, "fetch_entry_data", side_effect=_mock_fetch_entry):
            result = runner.invoke(
                app,
                [
                    "fetch",
                    "--pdb-ids",
                    "4LPK,5P21",
                    "--output",
                    str(tmp_path),
                ],
            )

        assert Path(tmp_path / "raw" / "entry_data.json").exists()
        assert result.exit_code == 0


class TestCliFields:
    def test_fields_list_categories(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["fields", "--list-categories"])
        assert result.exit_code == 0
        assert "Category" in result.output

    def test_fields_search(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["fields", "--search", "resolution"])
        # Uses live SchemaLoader — should succeed without crash
        assert result.exit_code == 0


class TestCliColumns:
    def test_columns_default_shows_summary(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns"])
        assert result.exit_code == 0
        assert "Column Registry" in result.output
        assert "Categories" in result.output

    def test_columns_list_categories(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns", "--list-categories"])
        assert result.exit_code == 0
        assert "Category" in result.output

    def test_columns_search(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns", "--search", "resolution"])
        assert result.exit_code == 0
        assert "resolution" in result.output.lower()

    def test_columns_search_no_match(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns", "--search", "zzz_nonexistent_zzz"])
        assert result.exit_code == 0
        assert "No columns matching" in result.output

    def test_columns_with_nonexistent_category(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns", "--category", "Nonexistent"])
        assert result.exit_code == 0
        assert "No columns in category" in result.output

    def test_columns_with_limit(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["columns", "--search", "a", "--limit", "5"])
        assert result.exit_code == 0


class TestCliRegistry:
    def test_registry_status_empty(self, runner: CliRunner) -> None:
        with patch(
            "rcsb_pipeline.cli.ProcessedRegistry.status",
            return_value={
                "total_entries": 0,
                "stale_entries": 0,
                "unique_uniprots": 0,
                "unique_pdbs": 0,
                "presets": [],
                "latest_run": "never",
            },
        ):
            result = runner.invoke(app, ["registry", "status"])
            assert result.exit_code == 0
            assert "0" in result.output

    def test_registry_clear_no_force(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["registry", "clear"])
        assert result.exit_code != 0
        assert "--force" in result.output

    def test_registry_diff(self, runner: CliRunner) -> None:
        with patch(
            "rcsb_pipeline.cli.ProcessedRegistry.diff",
            return_value={"new": [("P01116", "4LPK")], "already_processed": []},
        ):
            result = runner.invoke(
                app,
                [
                    "registry",
                    "diff",
                    "--uniprots",
                    "P01116",
                    "--pdb-ids",
                    "4LPK",
                ],
            )
            assert result.exit_code == 0
            assert "New:" in result.output

    def test_registry_mark_stale(self, runner: CliRunner) -> None:
        with patch("rcsb_pipeline.cli.ProcessedRegistry.mark_stale", return_value=3):
            result = runner.invoke(
                app,
                [
                    "registry",
                    "mark",
                    "--stale",
                    "--uniprots",
                    "P01116,P04637",
                ],
            )
            assert result.exit_code == 0
            assert "stale" in result.output

    def test_registry_mark_fresh(self, runner: CliRunner) -> None:
        with patch("rcsb_pipeline.cli.ProcessedRegistry.mark_fresh", return_value=2):
            result = runner.invoke(
                app,
                [
                    "registry",
                    "mark",
                    "--fresh",
                    "--uniprots",
                    "P01116",
                ],
            )
            assert result.exit_code == 0
            assert "fresh" in result.output

    def test_registry_help(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["registry", "--help"])
        assert result.exit_code == 0
        assert "status" in result.output
        assert "diff" in result.output
        assert "mark" in result.output
        assert "clear" in result.output

    def test_registry_diff_uniprots_required(self, runner: CliRunner) -> None:
        """diff command requires --uniprots."""
        result = runner.invoke(app, ["registry", "diff"])
        assert result.exit_code != 0


class TestCliReport:
    def test_report_nonexistent_file(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["report", "/nonexistent/path.csv"])
        assert result.exit_code != 0
        assert "File not found" in result.output

    def test_report_from_csv(self, runner: CliRunner, tmp_path: Path) -> None:
        csv_path = tmp_path / "test.csv"
        df = pd.DataFrame({"uniprot_id": ["P01116"], "pdb_id": ["4LPK"], "resolution": [1.5]})
        df.to_csv(csv_path, index=False)

        result = runner.invoke(app, ["report", str(csv_path), "--output", str(tmp_path / "reports")])
        assert result.exit_code == 0
        assert (tmp_path / "reports" / "coverage_report.md").exists() or "Coverage" in result.output


class TestCliValidate:
    def test_validate_nonexistent_file(self, runner: CliRunner) -> None:
        result = runner.invoke(app, ["validate", "/nonexistent/path.csv"])
        assert result.exit_code != 0
        assert "File not found" in result.output

    def test_validate_pass(self, runner: CliRunner, tmp_path: Path) -> None:
        csv_path = tmp_path / "test.csv"
        df = pd.DataFrame(
            {
                "uniprot_id": ["P01116"],
                "pdb_id": ["4LPK"],
                "structure_available": [True],
                "resolution": [1.5],
            }
        )
        df.to_csv(csv_path, index=False)

        result = runner.invoke(app, ["validate", str(csv_path)])
        # Should complete without crash
        assert result.exit_code in (0,)


class TestCliInitConfig:
    def test_init_config_creates_file(self, runner: CliRunner, tmp_path: Path) -> None:
        p = tmp_path / "config.yaml"
        result = runner.invoke(app, ["init-config", str(p)])
        assert result.exit_code == 0
        assert p.exists()

    def test_init_config_content(self, runner: CliRunner, tmp_path: Path) -> None:
        p = tmp_path / "config.yaml"
        runner.invoke(app, ["init-config", str(p)])
        content = p.read_text()
        assert "pipeline:" in content
        assert "fields:" in content
        assert "output:" in content
        assert "registry_db:" in content
