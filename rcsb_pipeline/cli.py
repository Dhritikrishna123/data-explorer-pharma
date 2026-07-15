"""CLI entry point for the RCSB PDB Pipeline."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

from rcsb_pipeline.cache import ResponseCache
from rcsb_pipeline.column_registry import ColumnRegistry
from rcsb_pipeline.config import RcsbPipelineConfig
from rcsb_pipeline.pipeline import PipelineOrchestrator
from rcsb_pipeline.registry import ProcessedRegistry
from rcsb_pipeline.schema_loader import SchemaLoader

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
  registry_db: ~/.cache/rcsb-pipeline-registry.db
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
  columns: []
  column_file: null
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


# ── Main pipeline command ──


@app.command()
def run(
    uniprots: str | None = typer.Option(None, help="Comma-separated UniProt IDs"),
    uniprot_file: str | None = typer.Option(None, help="File with one UniProt per line"),
    pdb_ids: str | None = typer.Option(None, help="Comma-separated PDB IDs (skip discovery)"),
    gene_symbols: str | None = typer.Option(None, help="Comma-separated gene symbols"),
    gene_symbol_file: str | None = typer.Option(None, help="File with one gene symbol per line"),
    preset: str = typer.Option("standard", help="Field preset: minimal, standard, full, custom, drug_discovery"),
    columns: str | None = typer.Option(None, help="Comma-separated column short names"),
    column_file: str | None = typer.Option(None, help="Path to custom column YAML file"),
    fields: str | None = typer.Option(None, help="Path to custom field config YAML"),
    granularity: str = typer.Option("per-structure", help="Output granularity"),
    format: list[str] | None = typer.Option(None, "-f", "--format", help="Output format(s)"),  # noqa: B008
    output: str = typer.Option("./rcsb_output", help="Output directory"),
    dedup_strategy: str = typer.Option("strict", help="Deduplication strategy"),
    dedup_keys: str | None = typer.Option(None, help="Comma-separated dedup keys"),
    missing_action: str = typer.Option("fill-null", help="Missing value strategy"),
    aggregation: str = typer.Option("pick-best", help="Aggregation mode"),
    aggregation_key: str = typer.Option("resolution_combined", help="Sort key for aggregation"),
    max_entries: int = typer.Option(1000, help="Max PDB entries"),
    min_resolution: float = typer.Option(0.0, help="Min resolution filter"),
    max_resolution: float = typer.Option(10.0, help="Max resolution filter"),
    methods: str | None = typer.Option(None, help="Comma-separated experimental methods"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Bypass cache"),
    resume: str | None = typer.Option(None, help="Resume from checkpoint file"),
    skip_registered: bool = typer.Option(False, "--skip-registered", help="Skip entries already in registry"),
    config: str | None = typer.Option(None, help="Path to YAML config file"),
) -> None:
    """Run the full pipeline: discover -> fetch -> transform -> export."""
    # Build config from CLI args
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
    if columns:
        cfg.fields.columns = [c.strip() for c in columns.split(",") if c.strip()]
    if column_file:
        cfg.fields.column_file = column_file
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

    _setup_logging(cfg.pipeline.log_dir, verbose, quiet)
    logger.info("Pipeline run started")

    if resume:
        cfg.pipeline.checkpoint = resume

    orchestrator = PipelineOrchestrator(cfg)
    try:
        orchestrator.run(
            skip_registered=skip_registered,
            no_cache=no_cache,
            columns=columns,
        )
    finally:
        orchestrator.close()


# ── Subcommands ──


@app.command()
def discover(
    uniprots: str | None = typer.Option(None, help="Comma-separated UniProt IDs"),
    uniprot_file: str | None = typer.Option(None, help="File with one UniProt per line"),
    output: str = typer.Option("./rcsb_discovery", help="Output directory"),
    max_entries: int = typer.Option(1000, help="Max PDB entries"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
) -> None:
    """Discover PDB entries for given UniProt IDs (Step 1 only)."""
    from rcsb_pipeline.discovery import discover_pdb_ids, save_discovery_results

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
    from rich.progress import Progress, SpinnerColumn, TextColumn

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console):
        uniprot_to_pdbs, raw = discover_pdb_ids(uniprot_list, cache, max_entries=max_entries)

    save_discovery_results(uniprot_to_pdbs, output)
    total_pdbs = sum(len(v) for v in uniprot_to_pdbs.values())
    console.print(f"[green]Discovered {total_pdbs} PDB entries for {len(uniprot_list)} UniProts[/green]")
    console.print(f"Output: {output}")
    logger.info("Discovery complete: %d PDB entries", total_pdbs)


@app.command()
def fetch(
    pdb_ids: str | None = typer.Option(None, help="Comma-separated PDB IDs"),
    pdb_file: str | None = typer.Option(None, help="JSON file with PDB ID list"),
    output: str = typer.Option("./rcsb_raw", help="Output directory"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress output"),
) -> None:
    """Fetch entry data for given PDB IDs (Step 2 only)."""
    from rcsb_pipeline.fetch import fetch_entry_data, save_raw_data

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
    from rich.progress import Progress, SpinnerColumn, TextColumn

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        entry_data = fetch_entry_data(ids, ["entry.rcsb_id"], cache, progress=progress)

    save_raw_data(entry_data, {}, output)
    console.print(f"[green]Fetched {len(entry_data)} PDB entries[/green]")
    logger.info("Fetch complete: %d entries", len(entry_data))


@app.command()
def fields(
    search: str | None = typer.Option(None, help="Search field names/descriptions"),
    category: str | None = typer.Option(None, help="Filter by category"),
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
    fields(None, None, list_categories=True, full=False)


@app.command()
def columns(
    search: str | None = typer.Option(None, help="Search column names, paths, or descriptions"),
    category: str | None = typer.Option(None, help="Filter by category"),
    list_categories: bool = typer.Option(False, "--list-categories", help="List all categories with field counts"),
    column_file: str | None = typer.Option(None, help="Custom column YAML file"),
    limit: int = typer.Option(50, help="Max results to show (0 = all)"),
) -> None:
    """List and search available columns from the built-in column registry."""
    reg = ColumnRegistry(column_file=column_file)

    if list_categories:
        table = Table(title="Column Categories", title_style="bold cyan")
        table.add_column("Category", style="cyan")
        table.add_column("Columns")
        for c in reg.list_categories():
            table.add_row(str(c["category"]), str(c["count"]))
        console.print(table)
        console.print(f"\nTotal: [bold]{reg.count}[/bold] columns")
        return

    if category:
        entries = reg.filter_by_category(category)
        if not entries:
            console.print(f"[yellow]No columns in category '{category}'[/yellow]")
            return
        table = Table(title=f"Columns in '{category}' ({len(entries)})", title_style="bold cyan")
        table.add_column("Short Name", style="green")
        table.add_column("Path", style="dim")
        table.add_column("Type")
        table.add_column("List")
        table.add_column("Description")
        for e in entries[:limit] if limit else entries:
            desc = (e.get("description") or "")[:80]
            table.add_row(e["name"], e.get("path", ""), e.get("type", ""), str(e.get("is_list", "")), desc)
        if limit and len(entries) > limit:
            console.print(f"[dim]... and {len(entries) - limit} more[/dim]")
        console.print(table)
        return

    if search:
        entries = reg.search(search)
        if not entries:
            console.print(f"[yellow]No columns matching '{search}'[/yellow]")
            return
        table = Table(title=f"Columns matching '{search}' ({len(entries)})", title_style="bold cyan")
        table.add_column("Short Name", style="green")
        table.add_column("Path", style="dim")
        table.add_column("Type")
        table.add_column("Category")
        table.add_column("Description")
        for e in entries[:limit] if limit else entries:
            desc = (e.get("description") or "")[:80]
            table.add_row(e["name"], e.get("path", ""), e.get("type", ""), e.get("category", ""), desc)
        if limit and len(entries) > limit:
            console.print(f"[dim]... and {len(entries) - limit} more[/dim]")
        console.print(table)
        return

    cats = reg.list_categories()
    console.print(f"[bold]Column Registry[/bold] — {reg.count} columns\n")
    table = Table(title=f"Categories ({len(cats)})")
    table.add_column("Category", style="cyan")
    table.add_column("Columns")
    for c in cats:
        table.add_row(str(c["category"]), str(c["count"]))
    console.print(table)
    console.print("\n[dim]Use --search or --category to explore. Use --list-categories for all categories.[/dim]")


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

    console.print(f"Loaded dataset: {len(df)} rows x {len(df.columns)} columns")

    from rcsb_pipeline.export import (
        report_coverage,
        report_duplicates,
        report_field_coverage,
        report_missing_data,
    )

    Path(output).mkdir(parents=True, exist_ok=True)

    if type in ("all", "coverage"):
        p = report_coverage(df, output_dir=output)
        console.print(f"  [green]V[/green] Coverage: {p}")

    if type in ("all", "missing"):
        p = report_missing_data(df, output)
        console.print(f"  [green]V[/green] Missing: {p}")

    if type in ("all", "duplicates"):
        p = report_duplicates(df, output)
        console.print(f"  [green]V[/green] Duplicates: {p}")

    if type in ("all", "schema"):
        p = report_field_coverage(df, output)
        console.print(f"  [green]V[/green] Field coverage: {p}")


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
        valid_bools = {True, False, "True", "False", "Yes", "No", "true", "false"}
        if not all(v in valid_bools for v in bool_vals):
            issues.append("Column 'structure_available' has unexpected values")

    if issues:
        console.print("[red]Validation Issues:[/red]")
        for issue in issues:
            console.print(f"  [yellow]W[/yellow] {issue}")
    else:
        console.print("[green]V Dataset validation passed![/green]")

    console.print(f"\nDataset: {len(df)} rows x {len(df.columns)} columns")
    console.print(f"Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")


@app.command()
def init_config(
    path: str = typer.Argument("rcsb_pipeline.yaml", help="Output config path"),
) -> None:
    """Generate a default config file."""
    with open(path, "w") as f:
        f.write(DEFAULT_CONFIG.strip() + "\n")
    console.print(f"[green]V[/green] Default config written to: {path}")


# -- Registry sub-commands --


registry_app = typer.Typer(name="registry", help="Manage the processed-data registry")


@registry_app.command("status")
def registry_status_cmd(
    registry_db: str = typer.Option("~/.cache/rcsb-pipeline-registry.db", help="Path to registry database"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed breakdown"),
) -> None:
    """Show statistics for the processed-data registry."""
    reg = ProcessedRegistry(registry_db)
    s = reg.status()
    console.print("[bold]Processed Data Registry[/bold]")
    console.print(f"  Total entries:         {s['total_entries']}")
    console.print(f"  Stale entries:         {s['stale_entries']}")
    console.print(f"  Unique UniProt IDs:    {s['unique_uniprots']}")
    console.print(f"  Unique PDB IDs:        {s['unique_pdbs']}")
    console.print(f"  Latest run:            {s['latest_run']}")
    presets: list[Any] = s.get("presets") or []  # type: ignore[assignment]
    if verbose and presets:
        console.print("\n[bold]By preset:[/bold]")
        for p in presets:
            console.print(f"  {p['preset'] or '(none)':20s} {p['cnt']} entries")
    reg.close()


@registry_app.command("diff")
def registry_diff_cmd(
    uniprots: str = typer.Option(..., help="Comma-separated UniProt IDs"),
    pdb_ids: str | None = typer.Option(None, help="Comma-separated PDB IDs (optional)"),
    preset: str = typer.Option("standard", help="Preset to check against"),
    granularity: str = typer.Option("per-structure", help="Granularity to check against"),
    registry_db: str = typer.Option("~/.cache/rcsb-pipeline-registry.db", help="Path to registry database"),
) -> None:
    """Show which targets are new vs already processed, without running the pipeline."""
    reg = ProcessedRegistry(registry_db)
    uid_list = [u.strip() for u in uniprots.split(",") if u.strip()]
    pid_list = [p.strip() for p in pdb_ids.split(",")] if pdb_ids else []
    pairs = [(u, "") for u in uid_list]
    if pid_list:
        pairs = [(uid, pid) for uid in uid_list for pid in pid_list]
    result = reg.diff(pairs, preset=preset, granularity=granularity)
    console.print("[bold]Registry diff[/bold]")
    console.print(f"  New:                 {len(result['new'])}")
    console.print(f"  Already processed:   {len(result['already_processed'])}")
    if result["already_processed"]:
        console.print("\n[yellow]Already in registry (first 20):[/yellow]")
        for uid, pid in result["already_processed"][:20]:
            console.print(f"  {uid} {'/' + pid if pid else '(any structure)'}")
        if len(result["already_processed"]) > 20:
            console.print(f"  ... and {len(result['already_processed']) - 20} more")
    reg.close()


@registry_app.command("mark")
def registry_mark_cmd(
    stale: bool = typer.Option(True, "--stale/--fresh", help="Mark as stale (will reprocess) or fresh"),
    uniprots: str | None = typer.Option(None, help="Comma-separated UniProt IDs (all if omitted)"),
    registry_db: str = typer.Option("~/.cache/rcsb-pipeline-registry.db", help="Path to registry database"),
) -> None:
    """Mark entries as stale (will be reprocessed on next run) or fresh."""
    reg = ProcessedRegistry(registry_db)
    ids = [u.strip() for u in uniprots.split(",")] if uniprots else None
    if stale:
        count = reg.mark_stale(ids)
        label = "stale"
    else:
        count = reg.mark_fresh(ids)
        label = "fresh"
    console.print(f"[green]Marked {count} entries as {label}[/green]")
    reg.close()


@registry_app.command("clear")
def registry_clear_cmd(
    uniprots: str | None = typer.Option(None, help="Comma-separated UniProt IDs (all if omitted)"),
    registry_db: str = typer.Option("~/.cache/rcsb-pipeline-registry.db", help="Path to registry database"),
    force: bool = typer.Option(False, "--force", help="Confirm deletion"),
) -> None:
    """Delete entries from the registry. Requires --force."""
    if not force:
        console.print("[red]Use --force to confirm deletion[/red]")
        raise typer.Exit(1)
    reg = ProcessedRegistry(registry_db)
    ids = [u.strip() for u in uniprots.split(",")] if uniprots else None
    count = reg.clear(ids)
    label = f"for {', '.join(ids)}" if ids else "(all)"
    console.print(f"[green]Deleted {count} entries {label}[/green]")
    reg.close()


app.add_typer(registry_app)


def _main() -> None:
    app()


if __name__ == "__main__":
    _main()
