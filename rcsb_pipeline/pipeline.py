"""Pipeline orchestrator — wires discovery, fetch, transform, and export into one runnable pipeline."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from rcsb_pipeline.cache import ResponseCache
from rcsb_pipeline.column_registry import ColumnRegistry
from rcsb_pipeline.config import RcsbPipelineConfig, load_preset
from rcsb_pipeline.discovery import (
    discover_pdb_ids,
    resolve_gene_symbols,
    save_discovery_results,
)
from rcsb_pipeline.export import export_dataset, generate_all_reports
from rcsb_pipeline.fetch import fetch_entry_data, fetch_uniprot_data, save_raw_data
from rcsb_pipeline.registry import ProcessedRegistry
from rcsb_pipeline.schema_loader import SchemaLoader
from rcsb_pipeline.transform import compute_binding_site_count, sanitize

logger = logging.getLogger("rcsb-pipeline")
console = Console()


class PipelineOrchestrator:
    """Orchestrates the full pipeline: resolve inputs → discover → fetch → transform → export."""

    def __init__(self, cfg: RcsbPipelineConfig) -> None:
        self.cfg = cfg
        self.cache = ResponseCache(cfg.pipeline.cache_dir)
        self.registry = ProcessedRegistry(cfg.pipeline.registry_db)

        self.all_uniprots: list[str] = []
        self.all_pdb_ids: list[str] = []
        self.uniprot_to_pdbs: dict[str, list[str]] = {}
        self.entry_data: dict[str, Any] = {}
        self.uniprot_data: dict[str, Any] = {}

        self.checkpoint: dict | None = None

    def run(
        self,
        *,
        skip_registered: bool = False,
        no_cache: bool = False,
        columns: str | None = None,
    ) -> dict[str, Any]:
        """Execute the full pipeline. Returns a summary dict."""
        if no_cache:
            self.cache.clear()

        self.cfg.resolve_paths()
        output_dir = self.cfg.output.directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.cfg.to_yaml(str(Path(output_dir) / "run_config.yaml"))

        self._print_header(output_dir)

        self._resolve_inputs()
        self._load_checkpoint_or_discover(output_dir)
        self._resolve_field_paths(columns)
        self._fetch_entry_data(output_dir)
        self._fetch_uniprot_data(output_dir)

        skipped = self._apply_registry_filter(skip_registered) if skip_registered else 0

        if not self.all_uniprots or not self.all_pdb_ids:
            console.print("[yellow]All entries already in registry — nothing to process[/yellow]")
            logger.info("All entries already in registry — nothing to process")
            self._save_checkpoint("export")
            return {"rows": 0, "columns": 0, "skipped_registered": skipped}

        df = self._build_dataframe()
        df = self._sanitize(df)
        written = self._export(df)

        self._save_checkpoint("export")

        self._print_footer(df, skipped)
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "written": written,
            "skipped_registered": skipped,
        }

    # ── Internal steps ──

    def _print_header(self, output_dir: str) -> None:
        console.print("[bold green]RCSB PDB Pipeline[/bold green]")
        console.print(f"  Output: {output_dir}")
        console.print(f"  Preset: {self.cfg.fields.preset}")
        console.print(f"  Granularity: {self.cfg.output.granularity}")
        console.print()

    def _resolve_inputs(self) -> None:
        """Resolve all input sources to flat UniProt and PDB ID lists."""
        self.all_pdb_ids = list(self.cfg.input.pdb_ids)

        cp = self.checkpoint
        if cp:
            self.all_uniprots = cp.get("all_uniprots", [])
            self.all_pdb_ids = cp.get("all_pdb_ids", [])
            self.uniprot_to_pdbs = cp.get("uniprot_to_pdbs", {})
            return

        self.all_uniprots = self._resolve_uniprots()

        if not self.all_uniprots and not self.all_pdb_ids:
            console.print("[red]No input provided. Use --uniprots, --uniprot-file, --pdb-ids, or --gene-symbols[/red]")
            raise SystemExit(1)

        console.print(
            f"\n[bold]Input:[/bold] {len(self.all_uniprots)} UniProt IDs, {len(self.all_pdb_ids)} direct PDB IDs"
        )
        logger.info("Input resolved: %d UniProts, %d PDB IDs", len(self.all_uniprots), len(self.all_pdb_ids))

    def _resolve_uniprots(self) -> list[str]:
        """Resolve all input sources to a flat list of UniProt IDs."""
        cfg = self.cfg
        uniprots: list[str] = list(cfg.input.uniprots)

        if cfg.input.uniprot_file:
            path = Path(cfg.input.uniprot_file)
            if path.exists():
                with open(path) as f:
                    for line in f:
                        uid = line.strip()
                        if uid and not uid.startswith("#"):
                            uniprots.append(uid)

        if cfg.input.gene_symbols or cfg.input.gene_symbol_file:
            symbols: list[str] = list(cfg.input.gene_symbols)
            if cfg.input.gene_symbol_file:
                spath = Path(cfg.input.gene_symbol_file)
                if spath.exists():
                    with open(spath) as f:
                        for line in f:
                            s = line.strip()
                            if s and not s.startswith("#"):
                                symbols.append(s)

            if symbols:
                with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
                    progress.add_task("[cyan]Resolving gene symbols...", total=len(symbols))
                    resolved = resolve_gene_symbols(symbols, self.cache)
                    for sym, uid in resolved.items():
                        if uid:
                            uniprots.append(uid)
                        else:
                            console.print(f"  [yellow]Could not resolve gene symbol: {sym}")

        return list(dict.fromkeys(uniprots))

    def _load_checkpoint_or_discover(self, output_dir: str) -> None:
        """If resuming, load checkpoint. Otherwise run discovery."""
        if self.checkpoint:
            stage = self.checkpoint.get("stage", "")
            if stage in ("discovery", "fetch", "transform", "export"):
                return

        if not self.all_pdb_ids and self.all_uniprots:
            console.print("\n[bold]Step 1: Discovery[/bold] — Finding PDB entries for UniProts...")
            with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
                self.uniprot_to_pdbs, raw_discovery = discover_pdb_ids(
                    uniprot_ids=self.all_uniprots,
                    cache=self.cache,
                    max_entries=self.cfg.discovery.max_entries,
                    min_resolution=self.cfg.discovery.min_resolution,
                    max_resolution=self.cfg.discovery.max_resolution,
                    experimental_methods=self.cfg.discovery.experimental_methods or None,
                    exclude_deprecated=self.cfg.discovery.exclude_deprecated,
                    progress=progress,
                )
            discovered = set()
            for ids in self.uniprot_to_pdbs.values():
                discovered.update(ids)
            self.all_pdb_ids = sorted(discovered)
            save_discovery_results(self.uniprot_to_pdbs, output_dir)
            self._log_discovery(output_dir)
            console.print(f"  Found {len(self.all_pdb_ids)} unique PDB entries for {len(self.all_uniprots)} UniProts")
            logger.info(
                "Discovery complete: %d PDB entries for %d UniProts", len(self.all_pdb_ids), len(self.all_uniprots)
            )
            self._save_checkpoint("discovery")

        if not self.all_pdb_ids:
            console.print("[red]No PDB entries found for the given inputs[/red]")
            raise SystemExit(1)

    def _log_discovery(self, output_dir: str) -> None:
        path = Path(output_dir) / "logs" / "discovery.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            for uid, pdbs in self.uniprot_to_pdbs.items():
                f.write(
                    json.dumps(
                        {
                            "uniprot_id": uid,
                            "pdb_ids": pdbs,
                            "count": len(pdbs),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                    + "\n"
                )

    def _resolve_field_paths(self, columns: str | None = None) -> None:
        """Resolve field config: column registry, preset, or custom."""
        cfg = self.cfg
        col_registry = ColumnRegistry(column_file=cfg.fields.column_file)

        if cfg.fields.columns or columns:
            col_names = cfg.fields.columns[:]
            if columns:
                col_names = [c.strip() for c in columns.split(",") if c.strip()]
            col_cfg = col_registry.to_field_config(col_names)
            cfg.fields.preset = "custom"
            field_cfg = col_cfg
        else:
            field_cfg = load_preset(cfg.fields.preset)

        if cfg.fields.custom_config:
            with open(cfg.fields.custom_config) as f:
                custom = yaml.safe_load(f)
                field_cfg.include = custom.get("include", [])

        self.entry_field_paths = [p for p in field_cfg.include if p.startswith("entry.")]
        self.uniprot_field_paths = [p for p in field_cfg.include if p.startswith("uniprot.")]

        if cfg.fields.preset == "full":
            loader = SchemaLoader()
            all_paths = []
            for type_name in loader.list_object_types():
                for field in loader.get_fields_for_type(type_name):
                    all_paths.append(f"{type_name}.{field['name']}")
            self.entry_field_paths = [p for p in all_paths if p.startswith("entry.")]
            self.uniprot_field_paths = [p for p in all_paths if p.startswith("uniprot.")]

        self._field_config = field_cfg
        logger.info("Field paths: %d entry, %d uniprot", len(self.entry_field_paths), len(self.uniprot_field_paths))

    def _fetch_entry_data(self, output_dir: str) -> None:
        if self.checkpoint and self.checkpoint.get("stage") in ("fetch", "transform", "export"):
            return

        console.print(f"\n[bold]Step 2: Fetch[/bold] — Fetching {len(self.all_pdb_ids)} PDB entries...")
        if self.entry_field_paths:
            t0 = datetime.now(timezone.utc)
            self.entry_data = fetch_entry_data(
                pdb_ids=self.all_pdb_ids,
                field_paths=self.entry_field_paths[:50],
                cache=self.cache,
                max_concurrent=self.cfg.pipeline.max_concurrent,
                rate_limit=self.cfg.pipeline.rate_limit,
                retry_max=self.cfg.pipeline.retry_max,
                progress=None,
            )
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            self._log_fetch(len(self.all_pdb_ids), len(self.entry_data), duration, output_dir)
            logger.info("Fetch complete: %d entries in %.1fs", len(self.entry_data), duration)
        self._save_checkpoint("fetch")

    def _fetch_uniprot_data(self, output_dir: str) -> None:
        if self.checkpoint and self.checkpoint.get("stage") in ("fetch", "transform", "export"):
            return

        if self.uniprot_field_paths and self.all_uniprots:
            console.print(f"\n[bold]Step 3: UniProt Enhancement[/bold] — Fetching {len(self.all_uniprots)} UniProts...")
            t0 = datetime.now(timezone.utc)
            self.uniprot_data = fetch_uniprot_data(
                uniprot_ids=self.all_uniprots,
                field_paths=self.uniprot_field_paths[:50],
                cache=self.cache,
                max_concurrent=self.cfg.pipeline.max_concurrent,
                rate_limit=self.cfg.pipeline.rate_limit,
                progress=None,
            )
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            logger.info("UniProt fetch complete: %d entries in %.1fs", len(self.uniprot_data), duration)

        save_raw_data(self.entry_data, self.uniprot_data, output_dir)

    def _log_fetch(self, pdb_count: int, entry_count: int, duration: float, output_dir: str) -> None:
        path = Path(output_dir) / "logs" / "fetch.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            f.write(
                json.dumps(
                    {
                        "batch_size": pdb_count,
                        "pdb_count": entry_count,
                        "duration_seconds": round(duration, 2),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
                + "\n"
            )

    def _apply_registry_filter(self, skip_registered: bool) -> int:
        """Filter out already-processed entries. Returns count skipped."""
        if not skip_registered:
            return 0

        skipped_pairs_count = 0
        new_rows: list[tuple[str, str]] = []
        for uid in self.all_uniprots:
            pdb_list = self.uniprot_to_pdbs.get(uid, self.all_pdb_ids if not self.uniprot_to_pdbs else [])
            if not pdb_list:
                pdb_list = [""]
            for pdb_id in pdb_list:
                if not self.registry.is_processed(uid, pdb_id, self.cfg.fields.preset, self.cfg.output.granularity):
                    new_rows.append((uid, pdb_id))
                else:
                    skipped_pairs_count += 1

        if skipped_pairs_count:
            console.print(f"\n[cyan]Registry skip:[/cyan] {skipped_pairs_count} already-processed entries filtered out")
            logger.info("Skipped %d already-registered entries", skipped_pairs_count)
            self.all_uniprots = list(dict.fromkeys(uid for uid, _ in new_rows))
            self.all_pdb_ids = list(dict.fromkeys(pid for _, pid in new_rows))
            self.uniprot_to_pdbs = {
                uid: [pid for u, pid in new_rows if u == uid] for uid in set(u for u, _ in new_rows)
            }

        return skipped_pairs_count

    def _build_dataframe(self) -> pd.DataFrame:
        console.print("\n[bold]Step 4: Transform[/bold] — Building and sanitizing dataset...")
        logger.info("Starting transform — %d rows to build", len(self.all_uniprots) * max(len(self.all_pdb_ids), 1))

        rows = []
        for uid in self.all_uniprots:
            pdb_list = self.uniprot_to_pdbs.get(uid, self.all_pdb_ids if not self.uniprot_to_pdbs else [])
            if not pdb_list:
                pdb_list = [""]
            for pdb_id in pdb_list:
                row: dict[str, Any] = {
                    "uniprot_id": uid,
                    "pdb_id": pdb_id,
                    "structure_available": bool(pdb_id),
                }
                entry = self.entry_data.get(pdb_id, {})
                if isinstance(entry, dict):
                    for path in self.entry_field_paths:
                        parts = path.split(".")
                        val: Any = entry
                        for p in parts[1:]:
                            if isinstance(val, dict):
                                val = val.get(p)
                            else:
                                val = None
                                break
                        col_name = "_".join(parts[1:]) if len(parts) > 1 else path
                        if val is not None:
                            row[col_name] = val

                up = self.uniprot_data.get(uid, {})
                if isinstance(up, dict):
                    for path in self.uniprot_field_paths:
                        parts = path.split(".")
                        val = up
                        for p in parts[1:]:
                            if isinstance(val, dict):
                                val = val.get(p)
                            else:
                                val = None
                                break
                        col_name = "_".join(parts[1:]) if len(parts) > 1 else path
                        if val is not None:
                            row[col_name] = val
                rows.append(row)

        df = pd.DataFrame(rows)
        logger.info("Raw DataFrame: %d rows x %d columns", len(df), len(df.columns))

        if self.entry_field_paths and "rcsb_ligand_neighbors" in str(self.entry_field_paths):
            df["binding_site_count"] = compute_binding_site_count(df)
            logger.info("Computed binding_site_count")

        output_dir = self.cfg.output.directory
        summary = {
            "Total UniProt IDs": len(self.all_uniprots),
            "Total PDB entries": len(self.all_pdb_ids),
            "Output granularity": self.cfg.output.granularity,
            "Final rows": len(df),
            "Final columns": len(df.columns),
        }
        with open(Path(output_dir) / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        return df

    def _sanitize(self, df: pd.DataFrame) -> pd.DataFrame:
        return sanitize(
            df,
            {
                "dedup_strategy": self.cfg.output.dedup_strategy,
                "dedup_keys": self.cfg.output.dedup_keys,
                "missing_action": self.cfg.output.missing_action,
                "aggregation_mode": self.cfg.output.aggregation_mode,
                "aggregation_key": self.cfg.output.aggregation_key,
                "granularity": self.cfg.output.granularity,
            },
        )

    def _export(self, df: pd.DataFrame) -> dict[str, str]:
        console.print("\n[bold]Step 5: Export[/bold] — Writing output files...")
        cfg = self.cfg
        output_dir = cfg.output.directory

        written = export_dataset(
            df,
            output_dir=output_dir,
            formats=cfg.output.formats,
            registry=self.registry,
            run_id=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
            preset=cfg.fields.preset,
            granularity=cfg.output.granularity,
        )
        for fmt, path in written.items():
            console.print(f"  [green]V[/green] {fmt}: {path}")
            logger.info("Exported %s: %s", fmt, path)

        reports = generate_all_reports(df, self.uniprot_to_pdbs or {}, output_dir)
        for rtype, rpath in reports.items():
            console.print(f"  [green]V[/green] Report ({rtype}): {rpath}")
            logger.info("Report %s: %s", rtype, rpath)

        field_config_path = Path(output_dir) / "field_config.yaml"
        field_cfg = getattr(self, "_field_config", None)
        include_list = field_cfg.include if field_cfg and field_cfg.include else []
        field_config_path.write_text(
            yaml.dump({"preset": cfg.fields.preset, "include": include_list}) if include_list else ""
        )

        return written

    def _save_checkpoint(self, stage: str) -> None:
        path = self.cfg.pipeline.checkpoint
        data = {
            "stage": stage,
            "all_uniprots": self.all_uniprots,
            "all_pdb_ids": self.all_pdb_ids,
            "uniprot_to_pdbs": {k: v for k, v in self.uniprot_to_pdbs.items()},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        logger.info("Checkpoint saved: stage=%s path=%s", stage, path)

    def close(self) -> None:
        self.cache.close()
        self.registry.close()

    def _print_footer(self, df: pd.DataFrame, skipped: int) -> None:
        console.print(f"\n[bold green]Pipeline complete![/bold green] Output in: {self.cfg.output.directory}")
        console.print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
        if skipped:
            console.print(f"  [cyan]Skipped (already in registry):[/cyan] {skipped}")
        logger.info(
            "Pipeline complete — %d rows, %d columns in %s", len(df), len(df.columns), self.cfg.output.directory
        )
