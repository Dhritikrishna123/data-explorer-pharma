"""CLI entry point for the RCSB PDB Pipeline."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import pandas as pd
import typer
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from rcsb_pipeline.cache import ResponseCache
from rcsb_pipeline.config import RcsbPipelineConfig, load_preset
from rcsb_pipeline.discovery import (
    discover_pdb_ids,
    resolve_gene_symbols,
    save_discovery_results,
)
from rcsb_pipeline.export import export_dataset, generate_all_reports
from rcsb_pipeline.fetch import fetch_entry_data, fetch_uniprot_data, save_raw_data
from rcsb_pipeline.schema_loader import SchemaLoader
from rcsb_pipeline.transform import compute_binding_site_count, sanitize

app = typer.Typer(
    name="rcsb-pipeline",
    help="RCSB PDB Pipeline — Fetch, transform, and export PDB structural data for drug target discovery",
    add_completion=False,
)
console = Console()
logger = logging.getLogger("rcsb-pipeline")

DEFAULT_CONFIG = """
pipeline:
  cache_dir: ~/.cache/rcsb-pipeline
  log_dir: ./logs
  checkpoint: ./checkpoint.json
  max_concurrent: 5
  rate_limit: 0.3
  batch_size: 50
  retry_max: 3
  retry_backoff: 2.0
input:
  uniprots: []
  uniprot_file: null
  pdb_ids: []
  gene_symbols: []
  gene_symbol_file: null
discovery:
  max_entries: 1000
  min_resolution: 0.0
  max_resolution: 10.0
  experimental_methods: []
  exclude_deprecated: true
fields:
  preset: standard
  include: []
  exclude: []
  custom_config: null
output:
  directory: ./rcsb_output
  formats: [csv, parquet]
  granularity: per-structure
  dedup_strategy: strict
  dedup_keys: []
  missing_action: fill-null
  aggregation_mode: pick-best
  aggregation_key: resolution_combined
"""


def _setup_logging(log_dir: str, verbose: bool, quiet: bool) -> None:
    level = logging.WARNING if quiet else (logging.DEBUG if verbose else logging.INFO)
    logger.setLevel(level)

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(str(log_path / "pipeline.log"), mode="a")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    if verbose:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(ch)


def _save_checkpoint(path: str, stage: str, data: dict) -> None:
    cp = {"stage": stage, "timestamp": datetime.now(timezone.utc).isoformat(), **data}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(cp, f, indent=2, default=str)
    logger.info("Checkpoint saved: stage=%s path=%s", stage, path)


def _load_checkpoint(path: str) -> Optional[dict]:
    p = Path(path)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return None


def _log_discovery(uniprot_to_pdbs: dict, log_dir: str) -> None:
    path = Path(log_dir) / "discovery.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        for uid, pdbs in uniprot_to_pdbs.items():
            f.write(json.dumps({"uniprot_id": uid, "pdb_ids": pdbs, "count": len(pdbs), "timestamp": datetime.now(timezone.utc).isoformat()}) + "\n")
    logger.info("Discovery log: %s (%d entries)", path, len(uniprot_to_pdbs))


def _log_fetch(batch_size: int, pdb_count: int, duration: float, log_dir: str) -> None:
    path = Path(log_dir) / "fetch.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps({
            "batch_size": batch_size, "pdb_count": pdb_count,
            "duration_seconds": round(duration, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }) + "\n")


def _resolve_uniprots(
    cfg: RcsbPipelineConfig, cache: ResponseCache, progress: Progress
) -> List[str]:
    """Resolve all input sources to a flat list of UniProt IDs."""
    uniprots: List[str] = []

    uniprots.extend(cfg.input.uniprots)

    if cfg.input.uniprot_file:
        path = Path(cfg.input.uniprot_file)
        if path.exists():
            with open(path) as f:
                for line in f:
                    uid = line.strip()
                    if uid and not uid.startswith("#"):
                        uniprots.append(uid)

    if cfg.input.gene_symbols or cfg.input.gene_symbol_file:
        symbols: List[str] = list(cfg.input.gene_symbols)
        if cfg.input.gene_symbol_file:
            spath = Path(cfg.input.gene_symbol_file)
            if spath.exists():
                with open(spath) as f:
                    for line in f:
                        s = line.strip()
                        if s and not s.startswith("#"):
                            symbols.append(s)

        if symbols:
            task = progress.add_task("[cyan]Resolving gene symbols...", total=len(symbols))
            resolved = resolve_gene_symbols(symbols, cache)
            for sym, uid in resolved.items():
                if uid:
                    uniprots.append(uid)
                else:
                    console.print(f"  [yellow]Could not resolve gene symbol: {sym}")
            progress.remove_task(task)

    return list(dict.fromkeys(uniprots))


@app.command()
def run(
    ctx: typer.Context,
    uniprots: Optional[str] = typer.Option(None, help="Comma-separated UniProt IDs"),
    uniprot_file: Optional[str] = typer.Option(None, help="File with one UniProt per line"),
    pdb_ids: Optional[str] = typer.Option(None, help="Comma-separated PDB IDs (skip discovery)"),
    gene_symbols: Optional[str] = typer.Option(None, help="Comma-separated gene symbols"),
    gene_symbol_file: Optional[str] = typer.Option(None, help="File with one gene symbol per line"),
    preset: str = typer.Option("standard", help="Field preset: minimal, standard, full, custom"),
    fields: Optional[str] = typer.Option(None, help="Path to custom field config YAML"),
    granularity: str = typer.Option("per-structure", help="Output granularity"),
    format: Optional[List[str]] = typer.Option(None, "-f", "--format", help="Output format(s)"),
    output: str = typer.Option("./rcsb_output", help="Output directory"),
    dedup_strategy: str = typer.Option("strict", help="Deduplication strategy"),
    dedup_keys: Optional[str] = typer.Option(None, help="Comma-separated dedup keys"),
    missing_action: str = typer.Option("fill-null", help="Missing value strategy"),
    aggregation: str = typer.Option("pick-best", help="Aggregation mode"),
    aggregation_key: str = typer.Option("resolution_combined", help="Sort key for aggregation"),
    max_entries: int = typer.Option(1000, help="Max PDB entries"),
    min_resolution: float = typer.Option(0.0, help="Min resolution filter"),
    max_resolution: float = typer.Option(10.0, help="Max resolution filter"),
    methods: Optional[str] = typer.Option(None, help="Comma-separated experimental methods"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Bypass cache"),
    resume: Optional[str] = typer.Option(None, help="Resume from checkpoint file"),
    config: Optional[str] = typer.Option(None, help="Path to YAML config file"),
) -> None:
    """Run the full pipeline: discover → fetch → transform → export."""
    # ── Load config ──
    cfg = RcsbPipelineConfig()
    if config:
        cfg = RcsbPipelineConfig.from_yaml(config)

    if uniprots:
        cfg.input.uniprots = [u.strip() for u in uniprots.split(",") if u.strip()]
    if uniprot_file:
        cfg.input.uniprot_file = uniprot_file
    if pdb_ids:
        cfg.input.pdb_ids = [p.strip() for p in pdb_ids.split(",") if p.strip()]
    if gene_symbols:
        cfg.input.gene_symbols = [g.strip() for g in gene_symbols.split(",") if g.strip()]
    if gene_symbol_file:
        cfg.input.gene_symbol_file = gene_symbol_file
    if preset:
        cfg.fields.preset = preset
    if fields:
        cfg.fields.custom_config = fields
    if granularity:
        cfg.output.granularity = granularity
    if format:
        cfg.output.formats = format
    if output:
        cfg.output.directory = output
    if dedup_strategy:
        cfg.output.dedup_strategy = dedup_strategy
    if dedup_keys:
        cfg.output.dedup_keys = [k.strip() for k in dedup_keys.split(",")]
    if missing_action:
        cfg.output.missing_action = missing_action
    if aggregation:
        cfg.output.aggregation_mode = aggregation
    if aggregation_key:
        cfg.output.aggregation_key = aggregation_key
    if max_entries:
        cfg.discovery.max_entries = max_entries
    if min_resolution:
        cfg.discovery.min_resolution = min_resolution
    if max_resolution:
        cfg.discovery.max_resolution = max_resolution
    if methods:
        cfg.discovery.experimental_methods = [m.strip() for m in methods.split(",")]

    cfg.resolve_paths()

    _setup_logging(cfg.pipeline.log_dir, verbose, quiet)
    logger.info("Pipeline run started — config: %s", cfg.pipeline.cache_dir)

    output_dir = cfg.output.directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cfg.to_yaml(str(Path(output_dir) / "run_config.yaml"))

    cache = ResponseCache(cfg.pipeline.cache_dir)
    if no_cache:
        cache.clear()

    # Check for resume
    checkpoint_data: Optional[dict] = None
    if resume:
        checkpoint_data = _load_checkpoint(resume)
        if checkpoint_data:
            logger.info("Resuming from checkpoint: stage=%s", checkpoint_data.get("stage"))
            console.print(f"[yellow]Resuming from checkpoint: stage={checkpoint_data.get('stage')}[/yellow]")

    console.print("[bold green]RCSB PDB Pipeline[/bold green]")
    console.print(f"  Output: {output_dir}")
    console.print(f"  Preset: {cfg.fields.preset}")
    console.print(f"  Granularity: {cfg.output.granularity}")
    console.print()

    all_uniprots: List[str] = []
    all_pdb_ids: List[str] = list(cfg.input.pdb_ids)
    uniprot_to_pdbs: dict = {}

    # Load previous state from checkpoint if resuming
    if checkpoint_data:
        all_uniprots = checkpoint_data.get("all_uniprots", [])
        all_pdb_ids = checkpoint_data.get("all_pdb_ids", [])
        uniprot_to_pdbs = checkpoint_data.get("uniprot_to_pdbs", {})

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        # ── Resolve inputs ──
        if not checkpoint_data:
            all_uniprots = _resolve_uniprots(cfg, cache, progress)
        if not all_uniprots and not all_pdb_ids:
            console.print("[red]No input provided. Use --uniprots, --uniprot-file, --pdb-ids, or --gene-symbols[/red]")
            raise typer.Exit(1)

        console.print(f"\n[bold]Input:[/bold] {len(all_uniprots)} UniProt IDs, {len(all_pdb_ids)} direct PDB IDs")
        logger.info("Input resolved: %d UniProts, %d PDB IDs", len(all_uniprots), len(all_pdb_ids))

        # ── Step 1: Discovery ──
        stage_discovery_done = checkpoint_data and checkpoint_data.get("stage") in ("discovery", "fetch", "transform", "export")
        if not all_pdb_ids and all_uniprots and not stage_discovery_done:
            console.print("\n[bold]Step 1: Discovery[/bold] — Finding PDB entries for UniProts...")
            uniprot_to_pdbs, raw_discovery = discover_pdb_ids(
                uniprot_ids=all_uniprots,
                cache=cache,
                max_entries=cfg.discovery.max_entries,
                min_resolution=cfg.discovery.min_resolution,
                max_resolution=cfg.discovery.max_resolution,
                experimental_methods=cfg.discovery.experimental_methods or None,
                exclude_deprecated=cfg.discovery.exclude_deprecated,
                progress=progress,
            )
            discovered_pdbs = set()
            for ids in uniprot_to_pdbs.values():
                discovered_pdbs.update(ids)
            all_pdb_ids = sorted(discovered_pdbs)
            save_discovery_results(uniprot_to_pdbs, output_dir)
            _log_discovery(uniprot_to_pdbs, cfg.pipeline.log_dir)
            console.print(f"  Found {len(all_pdb_ids)} unique PDB entries for {len(all_uniprots)} UniProts")
            logger.info("Discovery complete: %d PDB entries for %d UniProts", len(all_pdb_ids), len(all_uniprots))
            _save_checkpoint(cfg.pipeline.checkpoint, "discovery", {
                "all_uniprots": all_uniprots,
                "all_pdb_ids": all_pdb_ids,
                "uniprot_to_pdbs": {k: v for k, v in uniprot_to_pdbs.items()},
            })

        if not all_pdb_ids:
            console.print("[red]No PDB entries found for the given inputs[/red]")
            raise typer.Exit(1)

        # ── Step 2: Resolve field paths ──
        field_cfg = load_preset(cfg.fields.preset)
        if cfg.fields.custom_config:
            with open(cfg.fields.custom_config) as f:
                custom = yaml.safe_load(f)
                field_cfg.include = custom.get("include", [])

        entry_field_paths = [p for p in field_cfg.include if p.startswith("entry.")]
        uniprot_field_paths = [p for p in field_cfg.include if p.startswith("uniprot.")]

        if cfg.fields.preset == "full":
            loader = SchemaLoader()
            all_paths = []
            for type_name in loader.list_object_types():
                for f in loader.get_fields_for_type(type_name):
                    all_paths.append(f"{type_name}.{f['name']}")
            entry_field_paths = [p for p in all_paths if p.startswith("entry.")]
            uniprot_field_paths = [p for p in all_paths if p.startswith("uniprot.")]

        logger.info("Field paths: %d entry, %d uniprot", len(entry_field_paths), len(uniprot_field_paths))

        # ── Step 3: Fetch entry data ──
        stage_fetch_done = checkpoint_data and checkpoint_data.get("stage") in ("fetch", "transform", "export")
        entry_data: dict = {}
        if not stage_fetch_done:
            console.print(f"\n[bold]Step 2: Fetch[/bold] — Fetching {len(all_pdb_ids)} PDB entries...")
            if entry_field_paths:
                t0 = datetime.now(timezone.utc)
                entry_data = fetch_entry_data(
                    pdb_ids=all_pdb_ids,
                    field_paths=entry_field_paths[:50],
                    cache=cache,
                    max_concurrent=cfg.pipeline.max_concurrent,
                    rate_limit=cfg.pipeline.rate_limit,
                    retry_max=cfg.pipeline.retry_max,
                    progress=progress,
                )
                duration = (datetime.now(timezone.utc) - t0).total_seconds()
                _log_fetch(len(all_pdb_ids), len(entry_data), duration, cfg.pipeline.log_dir)
                logger.info("Fetch complete: %d entries in %.1fs", len(entry_data), duration)
            _save_checkpoint(cfg.pipeline.checkpoint, "fetch", {
                "all_uniprots": all_uniprots,
                "all_pdb_ids": all_pdb_ids,
                "uniprot_to_pdbs": {k: v for k, v in uniprot_to_pdbs.items()},
            })
        else:
            entry_data = {}

        # ── Step 4: Fetch UniProt data ──
        uniprot_data: dict = {}
        if not stage_fetch_done and uniprot_field_paths and all_uniprots:
            console.print(f"\n[bold]Step 3: UniProt Enhancement[/bold] — Fetching {len(all_uniprots)} UniProts...")
            t0 = datetime.now(timezone.utc)
            uniprot_data = fetch_uniprot_data(
                uniprot_ids=all_uniprots,
                field_paths=uniprot_field_paths[:50],
                cache=cache,
                max_concurrent=cfg.pipeline.max_concurrent,
                rate_limit=cfg.pipeline.rate_limit,
                progress=progress,
            )
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            logger.info("UniProt fetch complete: %d entries in %.1fs", len(uniprot_data), duration)

        save_raw_data(entry_data, uniprot_data, output_dir)

    # ── Step 5: Transform ──
    console.print("\n[bold]Step 4: Transform[/bold] — Building and sanitizing dataset...")
    logger.info("Starting transform — %d rows to build", len(all_uniprots) * max(len(all_pdb_ids), 1))

    rows = []
    for uid in all_uniprots:
        pdb_list = uniprot_to_pdbs.get(uid, all_pdb_ids if not uniprot_to_pdbs else [])
        if not pdb_list:
            pdb_list = [""]
        for pdb_id in pdb_list:
            row: dict = {
                "uniprot_id": uid,
                "pdb_id": pdb_id,
                "structure_available": bool(pdb_id),
            }
            entry = entry_data.get(pdb_id, {})
            if isinstance(entry, dict):
                for path in entry_field_paths:
                    parts = path.split(".")
                    val = entry
                    for p in parts[1:]:
                        if isinstance(val, dict):
                            val = val.get(p)
                        else:
                            val = None
                            break
                    col_name = "_".join(parts[1:]) if len(parts) > 1 else path
                    if val is not None:
                        row[col_name] = val

            up = uniprot_data.get(uid, {})
            if isinstance(up, dict):
                for path in uniprot_field_paths:
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
    logger.info("Raw DataFrame: %d rows × %d columns", len(df), len(df.columns))

    # Compute binding site count
    if entry_field_paths and "rcsb_ligand_neighbors" in str(entry_field_paths):
        df["binding_site_count"] = compute_binding_site_count(df)
        logger.info("Computed binding_site_count")

    manual_summary = {
        "Total UniProt IDs": len(all_uniprots),
        "Total PDB entries": len(all_pdb_ids),
        "Output granularity": cfg.output.granularity,
        "Final rows": len(df),
        "Final columns": len(df.columns),
    }
    with open(Path(output_dir) / "summary.json", "w") as f:
        json.dump(manual_summary, f, indent=2)

    # ── Step 6: Sanitize ──
    df = sanitize(df, {
        "dedup_strategy": cfg.output.dedup_strategy,
        "dedup_keys": cfg.output.dedup_keys,
        "missing_action": cfg.output.missing_action,
        "aggregation_mode": cfg.output.aggregation_mode,
        "aggregation_key": cfg.output.aggregation_key,
        "granularity": cfg.output.granularity,
    })
    logger.info("Sanitized DataFrame: %d rows × %d columns", len(df), len(df.columns))

    # ── Step 7: Export ──
    console.print("\n[bold]Step 5: Export[/bold] — Writing output files...")
    written = export_dataset(
        df,
        output_dir=output_dir,
        formats=cfg.output.formats,
    )
    for fmt, path in written.items():
        console.print(f"  [green]✓[/green] {fmt}: {path}")
        logger.info("Exported %s: %s", fmt, path)

    reports = generate_all_reports(df, uniprot_to_pdbs or {}, output_dir)
    for rtype, rpath in reports.items():
        console.print(f"  [green]✓[/green] Report ({rtype}): {rpath}")
        logger.info("Report %s: %s", rtype, rpath)

    field_config_path = Path(output_dir) / "field_config.yaml"
    field_config_path.write_text(yaml.dump(
        {"preset": cfg.fields.preset, "include": field_cfg.include}
    ) if field_cfg.include else "")

    _save_checkpoint(cfg.pipeline.checkpoint, "export", {
        "all_uniprots": all_uniprots,
        "all_pdb_ids": all_pdb_ids,
        "output_dir": output_dir,
        "rows": len(df),
        "columns": len(df.columns),
    })

    console.print(f"\n[bold green]Pipeline complete![/bold green] Output in: {output_dir}")
    console.print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
    logger.info("Pipeline complete — %d rows, %d columns in %s", len(df), len(df.columns), output_dir)


@app.command()
def discover(
    uniprots: Optional[str] = typer.Option(None, help="Comma-separated UniProt IDs"),
    uniprot_file: Optional[str] = typer.Option(None, help="File with one UniProt per line"),
    output: str = typer.Option("./rcsb_discovery", help="Output directory"),
    max_entries: int = typer.Option(1000, help="Max PDB entries"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
) -> None:
    """Discover PDB entries for given UniProt IDs (Step 1 only)."""
    _setup_logging(output, verbose, quiet)

    uniprot_list: list = []
    if uniprots:
        uniprot_list = [u.strip() for u in uniprots.split(",") if u.strip()]
    if uniprot_file:
        with open(uniprot_file) as f:
            uniprot_list.extend(line.strip() for line in f if line.strip() and not line.startswith("#"))

    if not uniprot_list:
        console.print("[red]No UniProt IDs provided[/red]")
        raise typer.Exit(1)

    logger.info("Discovering PDB entries for %d UniProts", len(uniprot_list))
    cache = ResponseCache("~/.cache/rcsb-pipeline")
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        uniprot_to_pdbs, raw = discover_pdb_ids(uniprot_list, cache, max_entries=max_entries)

    save_discovery_results(uniprot_to_pdbs, output)
    total_pdbs = sum(len(v) for v in uniprot_to_pdbs.values())
    console.print(f"[green]Discovered {total_pdbs} PDB entries for {len(uniprot_list)} UniProts[/green]")
    console.print(f"Output: {output}")
    logger.info("Discovery complete: %d PDB entries", total_pdbs)


@app.command()
def fetch(
    pdb_ids: Optional[str] = typer.Option(None, help="Comma-separated PDB IDs"),
    pdb_file: Optional[str] = typer.Option(None, help="JSON file with PDB ID list"),
    output: str = typer.Option("./rcsb_raw", help="Output directory"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
) -> None:
    """Fetch entry data for given PDB IDs (Step 2 only)."""
    _setup_logging(output, verbose, quiet)

    ids: list = []
    if pdb_ids:
        ids = [p.strip() for p in pdb_ids.split(",") if p.strip()]
    if pdb_file:
        with open(pdb_file) as f:
            data = json.load(f)
            if isinstance(data, list):
                ids.extend(data)
            elif isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        ids.extend(v)
                    else:
                        ids.append(v)

    ids = list(dict.fromkeys(ids))
    if not ids:
        console.print("[red]No PDB IDs provided[/red]")
        raise typer.Exit(1)

    logger.info("Fetching %d PDB entries", len(ids))
    cache = ResponseCache("~/.cache/rcsb-pipeline")
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        entry_data = fetch_entry_data(ids, ["entry.rcsb_id"], cache, progress=progress)

    save_raw_data(entry_data, {}, output)
    console.print(f"[green]Fetched {len(entry_data)} PDB entries[/green]")
    logger.info("Fetch complete: %d entries", len(entry_data))


@app.command()
def fields(
    search: Optional[str] = typer.Option(None, help="Search field names/descriptions"),
    category: Optional[str] = typer.Option(None, help="Filter by category"),
    list_categories: bool = typer.Option(False, "--list-categories", help="List all categories"),
    full: bool = typer.Option(False, "--full", help="Show all fields"),
) -> None:
    """Introspect available fields from the live RCSB schema."""
    loader = SchemaLoader()

    if list_categories:
        table = Table(title="Field Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Fields")
        cats = {
            "Entry": 150,
            "Polymer Entity": 100,
            "Polymer Entity Instance": 80,
            "Nonpolymer Entity": 60,
            "Assembly": 50,
            "Interface": 20,
            "Chemical Component": 70,
            "Experimental Data (X-ray)": 230,
            "Experimental Data (EM)": 180,
            "Experimental Data (NMR)": 70,
            "UniProt Integration": 70,
            "PubMed Integration": 30,
            "DrugBank Integration": 40,
            "Pfam Integration": 15,
        }
        for cat, count in sorted(cats.items()):
            table.add_row(cat, str(count))
        console.print(table)
        return

    if full:
        types = loader.list_object_types()
        for tname in types:
            fields_list = loader.get_fields_for_type(tname)
            if fields_list:
                console.print(f"\n[bold]{tname}[/bold] ({len(fields_list)} fields)")
                for f in fields_list[:20]:
                    console.print(f"  {f['name']:40s} {f['type']:25s} nullable={f['nullable']}")
                if len(fields_list) > 20:
                    console.print(f"  ... and {len(fields_list) - 20} more")
        return

    if search:
        results = loader.search_fields(search)
        if not results:
            console.print(f"[yellow]No fields matching '{search}'[/yellow]")
            return
        table = Table(title=f"Fields matching '{search}' ({len(results)})")
        table.add_column("Object", style="cyan")
        table.add_column("Field", style="green")
        table.add_column("Type")
        table.add_column("Path")
        for r in results[:50]:
            table.add_row(r["object_name"], r["field_name"], r["gql_type"], r["full_path"])
        if len(results) > 50:
            console.print(f"  ... and {len(results) - 50} more")
        console.print(table)
        return

    if category:
        loader = SchemaLoader()
        for tname in loader.list_object_types():
            if category.lower() in tname.lower():
                fields_list = loader.get_fields_for_type(tname)
                if fields_list:
                    console.print(f"\n[bold]{tname}[/bold] ({len(fields_list)} fields)")
                    for f in fields_list:
                        console.print(f"  {f['name']:40s} {f['type']:25s}")
        return


@app.command()
def categories() -> None:
    """List all available field categories."""
    ctx = typer.Context(fields)
    ctx.invoke(fields, list_categories=True)


@app.command()
def report(
    data: str = typer.Argument(..., help="Path to dataset CSV/Parquet"),
    output: str = typer.Option("./reports", help="Report output directory"),
    type: str = typer.Option("all", help="Report type: coverage, missing, duplicates, schema, all"),
) -> None:
    """Generate reports from an existing output dataset."""
    path = Path(data)
    if not path.exists():
        console.print(f"[red]File not found: {data}[/red]")
        raise typer.Exit(1)

    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_json(path)

    console.print(f"Loaded dataset: {len(df)} rows × {len(df.columns)} columns")

    from rcsb_pipeline.export import (
        report_coverage,
        report_duplicates,
        report_field_coverage,
        report_missing_data,
    )

    Path(output).mkdir(parents=True, exist_ok=True)

    if type in ("all", "coverage"):
        p = report_coverage(df, output_dir=output)
        console.print(f"  [green]✓[/green] Coverage: {p}")

    if type in ("all", "missing"):
        p = report_missing_data(df, output)
        console.print(f"  [green]✓[/green] Missing: {p}")

    if type in ("all", "duplicates"):
        p = report_duplicates(df, output)
        console.print(f"  [green]✓[/green] Duplicates: {p}")

    if type in ("all", "schema"):
        p = report_field_coverage(df, output)
        console.print(f"  [green]✓[/green] Field coverage: {p}")


@app.command()
def validate(
    data: str = typer.Argument(..., help="Path to dataset CSV/Parquet"),
) -> None:
    """Validate output dataset for data integrity."""
    path = Path(data)
    if not path.exists():
        console.print(f"[red]File not found: {data}[/red]")
        raise typer.Exit(1)

    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_json(path)

    issues = []

    expected_cols = ["uniprot_id", "pdb_id", "structure_available"]
    for col in expected_cols:
        if col not in df.columns:
            issues.append(f"Missing expected column: {col}")

    for col in df.columns:
        null_pct = df[col].isna().mean() * 100
        if null_pct > 90:
            issues.append(f"Column '{col}' is {null_pct:.0f}% null")

    total_dups = df.duplicated().sum()
    if total_dups > 0:
        issues.append(f"Found {total_dups} duplicate rows ({total_dups / len(df) * 100:.1f}%)")

    struct_field = df.get("structure_available")
    if struct_field is not None:
        bool_vals = struct_field.dropna().unique()
        if not all(v in (True, False, 1, 0, "True", "False", "Yes", "No", "true", "false") for v in bool_vals):
            issues.append("Column 'structure_available' has unexpected values")

    if issues:
        console.print("[red]Validation Issues:[/red]")
        for issue in issues:
            console.print(f"  [yellow]⚠[/yellow] {issue}")
    else:
        console.print("[green]✓ Dataset validation passed![/green]")

    console.print(f"\nDataset: {len(df)} rows × {len(df.columns)} columns")
    console.print(f"Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")


@app.command()
def init_config(
    path: str = typer.Argument("rcsb_pipeline.yaml", help="Output config path"),
) -> None:
    """Generate a default config file."""
    with open(path, "w") as f:
        f.write(DEFAULT_CONFIG.strip() + "\n")
    console.print(f"[green]✓[/green] Default config written to: {path}")


def _main() -> None:
    app()


if __name__ == "__main__":
    _main()
