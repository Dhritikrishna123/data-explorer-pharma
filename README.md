# RCSB PDB Pipeline

> **Fetch, transform, and export PDB structural data for drug target discovery.**
> Turns UniProt-identified proteins into ML-ready datasets via the official RCSB APIs.

```text
UniProt IDs ──► Search API ──► PDB IDs ──► Data API ──► Transform ──► CSV / Parquet / JSON / XLSX
                                                                         └── Reports + Logs + Checkpoints
```

---

## Quick Start

```bash
# 1. Install
cd data-explorer-pharma
python -m venv venv && source venv/bin/activate
pip install -e .

# 2. Run with two cancer targets (KRAS + TP53)
rcsb-pipeline run --uniprots P01116,P04637 --preset minimal --output ./training_data
```

**What happens:**
1. Discovers **~1300+ PDB entries** across both proteins
2. Fetches structural metadata from RCSB
3. Enhances with UniProt annotations (sequence, names, organism)
4. Deduplicates and sanitizes
5. Writes `final_dataset.csv` + `final_dataset.parquet`
6. Generates 4 reports (coverage, missing data, duplicates, field coverage)
7. Saves checkpoint + logs + run config

```text
training_data/
├── final_dataset.csv             # Ready for pandas: df = pd.read_csv("training_data/final_dataset.csv")
├── final_dataset.parquet         # Same data, 5-10x smaller, type-preserving
├── dataset_summary.json
├── logs/pipeline.log
├── reports/                      # Coverage, missing data, duplicates, field coverage
├── run_config.yaml               # Frozen config — fully reproducible
├── checkpoint.json               # Resume if interrupted
└── raw/                          # Raw API responses
```

**Total time:** ~2-3 minutes for 1000+ entries. Subsequent runs on the same targets take seconds (SQLite cache).

---

## Table of Contents

- [Quick Start](#quick-start)
- [Why This Pipeline](#why-this-pipeline)
- [Installation](#installation)
- [CLI Reference](#cli-reference)
  - [run — Full Pipeline](#run--full-pipeline)
  - [discover — Step 1 Only](#discover--step-1-only)
  - [fetch — Step 2 Only](#fetch--step-2-only)
  - [fields — Schema Introspection](#fields--schema-introspection)
  - [categories — Field Categories](#categories--field-categories)
  - [report — Generate Reports](#report--generate-reports)
  - [validate — Validate Dataset](#validate--validate-dataset)
  - [init-config — Generate Config](#init-config--generate-config)
- [Workflows](#workflows)
  - [Single Target Protein](#single-target-protein)
  - [Multi-Target Screening](#multi-target-screening)
  - [Custom Field Selection](#custom-field-selection)
  - [Quality-Focused (Best Resolution)](#quality-focused-best-resolution)
  - [Protein-Level Aggregation](#protein-level-aggregation)
  - [Gene Symbols as Input](#gene-symbols-as-input)
  - [Resume Interrupted Run](#resume-interrupted-run)
- [Understanding the Pipeline](#understanding-the-pipeline)
  - [Step 1: Discovery](#step-1-discovery)
  - [Step 2: Fetch](#step-2-fetch)
  - [Step 3: UniProt Enhancement](#step-3-uniprot-enhancement)
  - [Step 4: Transformation](#step-4-transformation)
  - [Step 5: Export](#step-5-export)
- [Field Presets](#field-presets)
  - [minimal](#minimal)
  - [standard](#standard)
  - [full](#full)
  - [custom](#custom)
- [Field Selection](#field-selection)
- [Granularity Modes](#granularity-modes)
- [Deduplication Strategies](#deduplication-strategies)
- [Missing Value Handling](#missing-value-handling)
- [Aggregation Modes](#aggregation-modes)
- [Column Reference](#column-reference)
- [Output Formats](#output-formats)
- [Configuration](#configuration)
- [Output Artifacts](#output-artifacts)
- [Caching](#caching)
- [Checkpoints & Resume](#checkpoints--resume)
- [Architecture](#architecture)
- [Extending](#extending)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)

---

## Why This Pipeline

| Problem | Solution |
|---------|----------|
| UniProt IDs don't directly map to PDB entries | Uses RCSB Search API with `NestedAttributeQuery` to find all matching structures |
| RCSB GraphQL schema has **317 types, 2398 fields** | Schema explorer + 4 field presets (minimal/standard/full/custom) |
| Raw API responses have duplicates, nulls, nested dicts, inconsistent types | Configurable sanitization: dedup, missing value handling, type coercion, aggregation |
| Need different data shapes for different ML tasks | 5 granularity modes × 5 dedup strategies × 5 aggregation modes |
| Team needs reproducibility and audit | Checkpoint system + full run logs + config snapshots + coverage/missing/duplicate reports |
| API calls are slow and rate-limited | SQLite cache, batched GraphQL queries, concurrent fetching, resume support |

---

## Installation

### Prerequisites
- Python 3.10+
- pip
- Internet access to `https://data.rcsb.org` and `https://search.rcsb.org`

### Setup

```bash
# Clone or navigate to the project root
cd data-explorer-pharma

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install the package and all dependencies
pip install -e .

# Verify installation
rcsb-pipeline --help
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `rcsb-api>=1.7.0` | Official RCSB Python client — Search API + Data API (GraphQL) |
| `typer>=0.12.0` | CLI framework with auto-generated help |
| `pydantic>=2.0` | Configuration validation with YAML serialization |
| `pyyaml>=6.0` | YAML config files and preset definitions |
| `pandas>=2.0` | DataFrame core for all data transformations |
| `pyarrow>=14.0` | Parquet export (5-10x smaller than CSV) |
| `openpyxl>=3.1.0` | Excel export |
| `rich>=13.0` | CLI output formatting, progress bars, tables |
| `httpx>=0.27.0` | HTTP client (used by rcsb-api internally) |
| `requests>=2.31.0` | MyGene.info API for gene symbol resolution |

---

## CLI Reference

### Global Flags

All commands accept:

| Flag | Description |
|------|-------------|
| `--help` | Show help message and exit |
| `--verbose`, `-v` | Enable debug-level logging to stdout + file |
| `--quiet`, `-q` | Suppress all output except errors |

### `run` — Full Pipeline

The main entry point. Runs discovery → fetch → transform → export.

```bash
rcsb-pipeline run [OPTIONS]
```

#### Input options (at least one required)

| Option | Type | Description |
|--------|------|-------------|
| `--uniprots` | TEXT | Comma-separated UniProt accessions, e.g. `P01116,P04637` |
| `--uniprot-file` | PATH | File with one UniProt per line (`#` for comments) |
| `--pdb-ids` | TEXT | Comma-separated PDB IDs (skips discovery) |
| `--gene-symbols` | TEXT | Comma-separated gene symbols (auto-resolved to UniProt via MyGene.info) |
| `--gene-symbol-file` | PATH | File with one gene symbol per line |

#### Field selection

| Option | Default | Description |
|--------|---------|-------------|
| `--preset` | `standard` | `minimal`, `standard`, `full`, `custom` |
| `--fields` | — | Path to custom field config YAML (used with `--preset custom`) |

#### Output configuration

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | `./rcsb_output` | Output directory |
| `--format`, `-f` | `csv`, `parquet` | Repeatable: `-f csv -f parquet -f json -f xlsx` |
| `--granularity` | `per-structure` | `per-protein`, `per-structure`, `per-chain` |
| `--dedup-strategy` | `strict` | `strict`, `key-only`, `keep-first`, `keep-best`, `keep-latest`, `none` |
| `--dedup-keys` | — | Comma-separated column names for `key-only`/`keep-best` |
| `--missing-action` | `fill-null` | `drop`, `fill-null`, `fill-0`, `fill-mean`, `fill-value` |
| `--aggregation` | `pick-best` | `pick-best`, `mean`, `min`, `max`, `concat` |
| `--aggregation-key` | `resolution_combined` | Sort key for `pick-best` aggregation |

#### Filters

| Option | Default | Description |
|--------|---------|-------------|
| `--max-entries` | `1000` | Maximum PDB entries per UniProt |
| `--min-resolution` | `0.0` | Minimum resolution in Å |
| `--max-resolution` | `10.0` | Maximum resolution in Å |
| `--methods` | — | Comma-separated experimental methods, e.g. `X-RAY DIFFRACTION,SOLUTION NMR` |

#### Run control

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass SQLite cache (fetch fresh data) |
| `--resume` | Path to checkpoint file from a previous run |
| `--config` | Path to YAML config file |

### `discover` — Step 1 Only

Find PDB entries for UniProt IDs without fetching data.

```bash
rcsb-pipeline discover --uniprots P01116 --output ./discovery_output
```

Outputs:
- `discovered_pdb_ids.json` — `{uniprot_id: [pdb_id, ...]}`
- `all_pdb_ids.json` — flat list of unique PDB IDs
- `discovery_summary.json` — counts

### `fetch` — Step 2 Only

Fetch raw data for PDB IDs without discovery.

```bash
rcsb-pipeline fetch --pdb-ids 4HHB,1TIM --output ./raw_data
# Or from a JSON file:
rcsb-pipeline fetch --pdb-file ./discovery_output/all_pdb_ids.json --output ./raw_data
```

### `fields` — Schema Introspection

Explore the RCSB GraphQL schema live.

```bash
# Search by keyword
rcsb-pipeline fields --search resolution

# List fields in a category
rcsb-pipeline fields --category "Polymer Entity"

# Show all categories with field counts
rcsb-pipeline fields --list-categories

# Dump every field (317 types, 2398 fields)
rcsb-pipeline fields --full
```

The schema is queried live from `https://data.rcsb.org/graphql`. Results include field name, GraphQL type, nullability, and full dot-path.

### `categories` — Field Categories

Quick overview of all field categories:

```bash
rcsb-pipeline categories
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Category                           ┃ Fields┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Chemical Component                 │ 70    │
│ DrugBank Integration               │ 40    │
│ Entry                              │ 150   │
│ Experimental Data (EM)             │ 180   │
│ ...                                │       │
└━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━━┘
```

### `report` — Generate Reports

Generate reports from an already-completed run's output.

```bash
# All report types
rcsb-pipeline report ./output/final_dataset.csv

# Specific type
rcsb-pipeline report ./output/final_dataset.parquet --type coverage
```

| `--type` | Report | Content |
|----------|--------|---------|
| `coverage` | Coverage report | UniProt → PDB mapping, success rate |
| `missing` | Missing data | Per-column null counts and percentages |
| `duplicates` | Duplicate report | Summary of duplicate rows per column |
| `schema` | Field coverage | Per-field: type, non-null count, unique values |
| `all` | All of the above | (default) |

### `validate` — Validate Dataset

Check a completed dataset for data integrity.

```bash
rcsb-pipeline validate ./output/final_dataset.csv
```

Checks:
- Expected columns exist (`uniprot_id`, `pdb_id`, `structure_available`)
- Columns with >90% null values
- Duplicate rows
- Unexpected values in `structure_available`

### `init-config` — Generate Config

Generate a default YAML config file to customize.

```bash
rcsb-pipeline init-config ./my_custom_config.yaml
```

---

## Workflows

### Single Target Protein

```bash
rcsb-pipeline run \
  --uniprots P01116 \
  --preset minimal \
  --output ./kras_data
```

- **Input:** KRAS (UniProt P01116)
- **Result:** 522 PDB entries, 8 columns
- **Time:** ~30 seconds

### Multi-Target Screening

```bash
rcsb-pipeline run \
  --uniprot-file targets.txt \
  --preset standard \
  --dedup-strategy keep-best \
  --aggregation-key resolution_combined \
  --output ./screening_output
```

`targets.txt`:
```
P01116    # KRAS
P04637    # TP53
P21802    # FGFR2
```

### Custom Field Selection

```bash
# 1. Find available fields
rcsb-pipeline fields --search affinity

# 2. Create custom field config
cat > my_fields.yaml << 'EOF'
preset: custom
include:
  - entry.rcsb_id
  - entry.rcsb_entry_info.resolution_combined
  - entry.rcsb_entry_info.experimental_method
  - entry.rcsb_entry_info.deposited_polymer_entity_instance_count
  - entry.rcsb_entry_info.nonpolymer_entity_count
  - entry.rcsb_entry_info.molecular_weight
  - entry.polymer_entities.entity_poly.pdbx_seq_one_letter_code
  - uniprot.rcsb_uniprot_protein.sequence
  - uniprot.rcsb_uniprot_protein.name
exclude: []
EOF

# 3. Run with custom config
rcsb-pipeline run \
  --uniprots P01116 \
  --preset custom \
  --fields my_fields.yaml \
  --output ./custom_output
```

### Quality-Focused (Best Resolution)

For ML training where you want the single best structure per protein:

```bash
rcsb-pipeline run \
  --uniprot-file targets.txt \
  --preset standard \
  --granularity per-protein \
  --dedup-strategy keep-best \
  --aggregation-key resolution_combined \
  --aggregation pick-best \
  --no-cache \
  --output ./best_per_protein
```

- Deduplicates across all columns within each (uniprot_id) group
- Sorts by `resolution_combined`, keeps the best
- **Result:** One row per protein

### Protein-Level Aggregation

```bash
rcsb-pipeline run \
  --uniprots P01116,P04637 \
  --preset full \
  --granularity per-protein \
  --aggregation mean \
  --format parquet \
  --output ./aggregated_proteins
```

- Groups all structures per protein
- Numeric fields → mean; string fields → mode
- **Result:** One row per protein with averaged structural properties

### Gene Symbols as Input

```bash
rcsb-pipeline run \
  --gene-symbols KRAS,TP53,FGFR2 \
  --preset minimal \
  --output ./gene_symbols_output
```

- Resolves `KRAS` → `P01116`, `TP53` → `P04637`, `FGFR2` → `P21802`
- Uses MyGene.info REST API (cached)
- Then runs normal pipeline

### Resume Interrupted Run

```bash
# Start a large run
rcsb-pipeline run \
  --uniprot-file large_target_set.txt \
  --preset standard \
  --output ./large_run

# If interrupted (network failure, Ctrl+C, etc.):
rcsb-pipeline run \
  --resume ./large_run/checkpoint.json \
  --output ./large_run
```

Checkpoints are saved after:
- Discovery completes → skips re-discovery on resume
- Fetch completes → skips re-fetch on resume

---

## Understanding the Pipeline

### Step 1: Discovery

Maps UniProt IDs to PDB entries using the RCSB Search API.

```python
# Internally uses:
from rcsbapi.search import NestedAttributeQuery, AttributeQuery

q1 = AttributeQuery(
    "rcsb_polymer_entity_container_identifiers."
    "reference_sequence_identifiers.database_accession",
    "exact_match", "P01116"
)
q2 = AttributeQuery(
    "rcsb_polymer_entity_container_identifiers."
    "reference_sequence_identifiers.database_name",
    "exact_match", "UniProt"
)
query = NestedAttributeQuery(q1, q2)
results = list(query(return_type="entry"))  # ["4HHB", "1TIM", ...]
```

**Filters applied:**
- Resolution range (`min-resolution`, `max-resolution`)
- Experimental method (`--methods X-RAY DIFFRACTION,SOLUTION NMR`)
- Max entries per UniProt (`--max-entries`)
- Deprecated entries excluded

**Output:** Deduplicated list of PDB entry IDs.

### Step 2: Fetch

Fetches structural data from the RCSB Data API (GraphQL).

**Batching:**
- PDB IDs grouped in batches of 50
- Each batch → single GraphQL query
- Configurable concurrency (default: 5 workers)
- Rate-limited (default: 0.3s between batches)
- Exponential backoff on failure (3 retries)

```python
# Internally constructs:
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="entry",
    input_ids=["4HHB", "1TIM", ...],
    return_data_list=["rcsb_id", "exptl.method", ...]
)
result = query.exec()
# → {"data": {"entries": [{"rcsb_id": "4HHB", ...}, ...]}}
```

**Output:** Nested dict `{pdb_id: {field: value}}`.

### Step 3: UniProt Enhancement

Fetches UniProt annotations via the RCSB Data API.

```python
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="uniprot",
    input_ids=["P01116"],
    return_data_list=["rcsb_uniprot_protein.sequence", ...]
)
result = query.exec()
```

**Data fetched:**
- Amino acid sequence
- Protein name (recommended + alternative)
- Gene names (primary + synonyms)
- Source organism
- Keywords
- Features/motifs

### Step 4: Transformation

The transform layer applies a configurable pipeline:

```
Raw dicts
  │
  ├──► Field extraction (dot-path navigation)
  ├──► Type coercion (string→float where possible)
  ├──► Unhashable flattening (dict/list → JSON strings)
  ├──► Deduplication (6 strategies)
  ├──► Missing value handling (5 strategies)
  └──► Aggregation (5 modes, if per-protein or per-chain granularity)
```

**Sanitization pipeline** (in order):
1. `coerce_types` — Strings that look numeric → float
2. `_flatten_unhashable` — Dict/list values → JSON strings (enables pandas dedup)
3. `deduplicate` — Per configured strategy
4. `handle_missing` — Per configured strategy
5. `aggregate_protein_rows` — If granularity is `per-protein`

**Binding site count:** Approximated by counting unique `ligand_comp_id` values in `RcsbLigandNeighbors`. Documented as approximate.

### Step 5: Export

Writes the final DataFrame and generates all artifacts.

**Formats:**
- CSV — universally readable, large
- Parquet — compressed, type-preserving, fast to load
- JSON lines — flexible, easy to inspect
- XLSX — Excel-readable (limited rows)

**Reports:**
- **Coverage:** Which UniProts matched how many PDB entries
- **Missing data:** Per-column null counts
- **Duplicates:** Summary of duplicate rows
- **Field coverage:** Per-field data type, non-null %, unique values

---

## Field Presets

### `minimal`

The essential columns for target discovery — 6 PDB fields + 4 UniProt fields:

| Column | RCSB Path | Type |
|--------|-----------|------|
| pdb_id | `entry.rcsb_id` | string |
| experimental_method | `entry.exptl.method` | string |
| resolution | `entry.rcsb_entry_info.resolution_combined` | float |
| chain_count | `entry.rcsb_entry_info.deposited_polymer_entity_instance_count` | int |
| ligand_count | `entry.rcsb_entry_info.nonpolymer_entity_count` | int |
| sequence | `uniprot.rcsb_uniprot_protein.sequence` | string |
| protein_name | `uniprot.rcsb_uniprot_protein.name` | string |
| gene_symbol | `uniprot.rcsb_uniprot_protein.gene` | string |
| organism | `uniprot.rcsb_uniprot_protein.source_organism` | string |
| binding_site_count | computed from ligand neighbors | int |

**Use when:** You need a quick overview of which structures exist for your targets.

### `standard`

Minimal + ~40 additional fields covering:
- Molecular weight, polymer composition, atom counts
- Disulfide bonds, structure keywords
- Polymer entity identifiers and sequence
- Full UniProt annotations (EC numbers, keywords, features)

**Use when:** You need comprehensive structural metadata for feature engineering.

### `full`

Every field from the live RCSB GraphQL schema. Expands all 317 object types through all reachable paths.

```
~3000+ columns per row
```

**Use when:** You're exploring what's available or need maximum data.
**Always use with `--format parquet`** — CSV will be unwieldy.
**Performance note:** Fetching all fields takes significantly longer.

### `custom`

Define exactly which fields you want:

```yaml
# custom_fields.yaml
preset: custom
include:
  - entry.rcsb_id
  - entry.rcsb_entry_info.resolution_combined
  - entry.rcsb_entry_info.deposited_polymer_entity_instance_count
  - entry.rcsb_entry_info.experimental_method
  - entry.polymer_entities.rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession
  - uniprot.rcsb_uniprot_protein.sequence
  - uniprot.rcsb_uniprot_protein.name
exclude: []
```

```bash
rcsb-pipeline run \
  --uniprots P01116 \
  --preset custom \
  --fields custom_fields.yaml \
  --output ./custom_output
```

**Discover fields with:**
```bash
rcsb-pipeline fields --search resolution
rcsb-pipeline fields --category "Entry"
```

---

## Field Selection

Use the `fields` command to explore available fields interactively:

```bash
# Search by keyword
rcsb-pipeline fields --search ligand
# → 24 fields: rcsb_binding_affinity, rcsb_ligand_neighbors, ...

# Browse category
rcsb-pipeline fields --category "Polymer Entity"
# → Polymer Entity: entity_poly, rcsb_entity_host_organism, ...

# Count by category
rcsb-pipeline fields --list-categories
# → Entry: 150, Polymer Entity: 100, UniProt Integration: 70, ...

# Full dump
rcsb-pipeline fields --full | less
```

**Field path convention:**
```
entry.rcsb_entry_info.resolution_combined
│     │                      │
│     │                      └── field name
│     └── GraphQL object type
└── root query type (entry / uniprot / polymer_entity / etc.)
```

---

## Granularity Modes

Controls how many rows each input protein produces:

| Mode | Group Key | Rows per Protein | Use Case |
|------|-----------|:----------------:|----------|
| `per-protein` | `uniprot_id` | 1 | Protein-level ML (classification, regression) |
| `per-structure` | `uniprot_id` + `pdb_id` | N (one per PDB entry) | Structure-level analysis (default) |
| `per-chain` | `uniprot_id` + `pdb_id` + `asym_id` | N × chains | Chain-level features |

**`per-protein`** — When a protein has multiple PDB entries, they are aggregated using the configured aggregation mode (`pick-best`, `mean`, `concat`, etc.). Good for:
- "Does this protein have a structure at all?"
- Training a classifier per target
- Reducing dataset size

**`per-structure`** — Each PDB entry is a separate row. A protein with 522 entries → 522 rows. Good for:
- Training on structural features
- Analyzing resolution distributions
- Comparing methods across structures

**`per-chain`** — Each polymer chain matching the UniProt is a separate row. Good for:
- Chain-level feature analysis
- Analyzing interface/ligand per chain

---

## Deduplication Strategies

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `strict` | Drop identical rows (all columns match) | Safe default, no information loss |
| `key-only` | Drop by composite key (specify with `--dedup-keys`) | Merging multiple data sources |
| `keep-first` | First occurrence wins | Quick dedup without priorities |
| `keep-best` | Sort by key column, keep first after sort | ML training — keep highest resolution |
| `keep-latest` | Reverse sort by key column, keep first | Keeping most recent structures |
| `none` | Keep all rows | Debugging, seeing raw duplication |

**ML best practice:**
```bash
rcsb-pipeline run \
  --uniprots P01116 \
  --granularity per-protein \
  --dedup-strategy keep-best \
  --aggregation-key resolution_combined \
  --output ./ml_dataset
```
This keeps the highest-resolution structure per protein.

---

## Missing Value Handling

| Strategy | Numeric | String/Other | When To Use |
|----------|---------|--------------|-------------|
| `drop` | Drop row | Drop row | Small datasets, complete-case analysis |
| `fill-null` | Leave NaN | Leave as-is | Default — downstream model handles nulls |
| `fill-0` | 0 | `""` (empty string) | Null = absence (e.g., ligand count) |
| `fill-mean` | Column mean | Column mode (most frequent) | Safe imputation, preserves distribution |
| `fill-value` | User-defined | User-defined | Custom default (not yet exposed via CLI) |

---

## Aggregation Modes

Used when `--granularity per-protein` to collapse multiple PDB entries into one row.

| Mode | Numeric Fields | String/ID Fields | Use Case |
|------|---------------|------------------|----------|
| `pick-best` | Keep best row (sorted by key) | Keep best row | Default — keep best structure |
| `mean` | Mean | Mode | Average structural properties |
| `min` | Min | First alphabetically | Conservative estimates |
| `max` | Max | Last alphabetically | Upper bounds |
| `concat` | Comma-separated | Comma-separated | Preserve all values |

---

## Column Reference

A comprehensive mapping of every output column to its RCSB GraphQL source path,
data type, description, and preset inclusion is maintained in a standalone document:

> **[`COLUMN_REFERENCE.md`](./COLUMN_REFERENCE.md)**

It covers:
- **Column naming convention** — how dot-paths become column names
- **Base columns** — `uniprot_id`, `pdb_id`, `structure_available` (always present)
- **All 54 columns** across both presets, with full type and description
- **Per-preset listings** — exact column set for `minimal` (10) and `standard` (54)
- **`binding_site_count`** — documented as an approximate computed value

Generated automatically from the preset YAML files — stays in sync with the code.

---

## Output Formats

| Format | Extension | Size | Type-Preserving | Human-Readable | Load Time (1M rows) |
|--------|-----------|:----:|:---------------:|:--------------:|:-------------------:|
| CSV | `.csv` | Large | No (strings only) | Yes | ~2s |
| Parquet | `.parquet` | Small (5-10x) | Yes | No | ~0.3s |
| JSON Lines | `.json` | Largest | Partial | Yes | ~3s |
| Excel | `.xlsx` | Large | Partial | Yes (filters) | N/A (>1M rows) |

**Default:** `csv` + `parquet`. Both are produced unless you override with `-f`.

**Recommendation for ML:**
```python
# Load Parquet — fast, type-preserving
import pandas as pd
df = pd.read_parquet("output/final_dataset.parquet")
# vs CSV — slower, needs type coercion
df = pd.read_csv("output/final_dataset.csv")
```

---

## Configuration

The pipeline is configured via YAML, CLI flags, or a mix. CLI flags override YAML values.

### Generate a default config

```bash
rcsb-pipeline init-config rcsb_pipeline.yaml
```

### Full config reference

```yaml
pipeline:
  cache_dir: ~/.cache/rcsb-pipeline    # SQLite cache location
  log_dir: ./logs                       # Pipeline logs (auto-set to {output_dir}/logs)
  checkpoint: ./checkpoint.json         # Resume checkpoint (auto-set to {output_dir}/checkpoint.json)
  max_concurrent: 5                     # Parallel API workers
  rate_limit: 0.3                       # Seconds between batches
  batch_size: 50                        # PDB IDs per GraphQL query
  retry_max: 3                          # API retry attempts
  retry_backoff: 2.0                    # Exponential backoff multiplier

input:
  uniprots: []                          # List of UniProt IDs
  uniprot_file: null                    # Path to UniProt file
  pdb_ids: []                           # Direct PDB IDs (skip discovery)
  gene_symbols: []                      # Gene symbols to resolve
  gene_symbol_file: null                # Path to gene symbols file

discovery:
  max_entries: 1000                     # Max PDBs per UniProt
  min_resolution: 0.0                   # Min resolution filter
  max_resolution: 10.0                  # Max resolution filter
  experimental_methods: []              # e.g. ["X-RAY DIFFRACTION"]
  exclude_deprecated: true              # Skip deprecated entries

fields:
  preset: standard                      # minimal / standard / full / custom
  include: []                           # Custom field paths (for custom preset)
  exclude: []                           # Fields to exclude (not yet implemented)
  custom_config: null                   # Path to custom YAML (for custom preset)

output:
  directory: ./rcsb_output              # Output directory
  formats: [csv, parquet]               # Output formats
  granularity: per-structure            # per-protein / per-structure / per-chain
  dedup_strategy: strict                # Deduplication strategy
  dedup_keys: []                        # Keys for key-only / keep-best
  missing_action: fill-null             # Missing value strategy
  aggregation_mode: pick-best           # Aggregation for per-protein
  aggregation_key: resolution_combined  # Sort key for pick-best
```

### Running with a config file

```bash
rcsb-pipeline run --config rcsb_pipeline.yaml
```

---

## Output Artifacts

```
training_data/
├── final_dataset.csv              # ML-ready dataset (CSV)
├── final_dataset.parquet          # Same data (Parquet, 5-10x smaller)
├── dataset_summary.json           # Rows, columns, dtypes, null counts
├── summary.json                   # High-level run summary
│
├── logs/
│   ├── pipeline.log               # Full structured log (all levels)
│   ├── discovery.jsonl            # Each UniProt → PDB mapping (JSONL)
│   └── fetch.jsonl                # Each batch fetch + timing (JSONL)
│
├── reports/
│   ├── coverage_report.md         # Which UniProts mapped to how many PDBs
│   ├── field_coverage.md          # % non-null per field
│   ├── duplicate_report.md        # Duplicate row summary
│   └── missing_data_report.md     # Null counts per column
│
├── raw/
│   ├── entry_data.json            # Raw Data API responses per entry
│   └── uniprot_data.json          # Raw UniProt responses
│
├── discovered_pdb_ids.json        # {uniprot_id: [pdb_id, ...]}
├── all_pdb_ids.json               # Deduplicated flat list
├── discovery_summary.json         # Counts
├── run_config.yaml                # Frozen config for this run
├── field_config.yaml              # Frozen field selection
└── checkpoint.json                # Resume checkpoint
```

---

## Caching

All RCSB API responses are cached in a local SQLite database.

| Feature | Detail |
|---------|--------|
| **Location** | `~/.cache/rcsb-pipeline/rcsb_cache.db` (default) |
| **Scope** | Per (query_type, arguments) hash |
| **TTL** | Indefinite — schema rarely changes |
| **Benefits** | Re-running same targets: seconds instead of minutes |
| **Invalidation** | `--no-cache` flag, or delete the cache DB manually |
| **Storage** | Typically <50MB for 1000+ entries |

```bash
# Bypass cache for one run
rcsb-pipeline run --uniprots P01116 --no-cache --output ./fresh

# Clear all cache
rm -f ~/.cache/rcsb-pipeline/rcsb_cache.db
```

---

## Checkpoints & Resume

The pipeline saves checkpoints after each major stage to enable resume.

### Checkpoint locations

| Stage | Saved After | Resume Skips |
|-------|-------------|--------------|
| `discovery` | Discovery complete | Re-discovery |
| `fetch` | Entry data fetched | Re-fetching entries |
| `export` | Pipeline complete | (no next stage) |

### Resume behavior

```bash
# Initial run (interrupted during fetch)
rcsb-pipeline run --uniprots P01116 --output ./my_run --no-cache

# Resume — skips discovery, starts from fetch
rcsb-pipeline run --resume ./my_run/checkpoint.json --output ./my_run
```

**Important:** Resume requires the same output directory and cache. Discovery and fetch results are loaded from the checkpoint, not re-executed.

---

## Architecture

```text
                     ┌──────────────────────┐
                     │       Input           │
                     │  UniProt / Gene / PDB │
                     └──────────┬───────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│                 1. Discovery Layer                        │
│  ┌──────────────────────────────────────────────────┐    │
│  │  RCSB Search API (NestedAttributeQuery)           │    │
│  │  ┌─ database_accession: P01116                  │    │
│  │  └─ database_name: "UniProt"                     │    │
│  │  → Returns list of PDB entry IDs (strings)       │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Filter: resolution, method, max_entries         │    │
│  │  Dedup: merge PDB IDs across all input UniProts  │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                 2. Fetch Layer                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  RCSB Data API — Entry Query (GraphQL)           │    │
│  │  • Batch PDB IDs (50 per query)                  │    │
│  │  • 5 concurrent workers                          │    │
│  │  • Rate-limited (0.3s between batches)           │    │
│  │  • Exponential backoff retry (3 attempts)        │    │
│  │  • SQLite response cache                         │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐    │
│  │  RCSB Data API — UniProt Query (GraphQL)         │    │
│  │  • Fetches sequence, names, organism, GO terms   │    │
│  │  • Cached via SQLite                             │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                 3. Transform Layer                        │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Field Extraction   (dot-path → nested dict)     │    │
│  │  Type Coercion      (string → float)             │    │
│  │  Unhashable Flatten (dict/list → JSON string)    │    │
│  │  Deduplication      (6 strategies)               │    │
│  │  Missing Values     (5 strategies)               │    │
│  │  Aggregation        (5 modes, per granularity)   │    │
│  │  Binding Site Count (computed from neighbors)    │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                 4. Export Layer                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │  CSV      → final_dataset.csv                   │    │
│  │  Parquet  → final_dataset.parquet               │    │
│  │  JSON     → final_dataset.json                  │    │
│  │  Excel    → final_dataset.xlsx                  │    │
│  ├──────────────────────────────────────────────────┤    │
│  │  Reports → coverage, missing, duplicates, schema │    │
│  │  Logs    → pipeline.log, discovery.jsonl, fetch  │    │
│  │  Config  → run_config.yaml, field_config.yaml    │    │
│  │  Checkpoint → checkpoint.json                    │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### Module Map

| Module | File | Purpose | Key Dependencies |
|--------|------|---------|-----------------|
| **Config** | `config.py` | Pydantic models, YAML loading, preset resolution | `pydantic`, `pyyaml` |
| **Schema Loader** | `schema_loader.py` | Live GraphQL introspection of RCSB schema | `rcsbapi.data` |
| **Discovery** | `discovery.py` | Search API → PDB IDs per UniProt | `rcsbapi.search` |
| **Cache** | `cache.py` | SQLite-backed response cache with TTL | `sqlite3` (stdlib) |
| **Fetch** | `fetch.py` | Batched Data API queries (entry + uniprot) | `rcsbapi.data`, `cache` |
| **Transform** | `transform.py` | Dedup, missing values, aggregation, type coercion | `pandas` |
| **Export** | `export.py` | All output formats + report generation | `pandas`, `pyarrow`, `openpyxl` |
| **CLI** | `cli.py` | Typer CLI wiring all modules | `typer`, `rich` |

---

## Extending

### Adding new fields to a preset

Edit the YAML files in `rcsb_pipeline/presets/`:

```yaml
# rcsb_pipeline/presets/standard.yaml
include:
  - entry.rcsb_id
  - entry.rcsb_entry_info.resolution_combined
  + - entry.rcsb_entry_info.structure_determination_methodology  # new field
```

### Adding custom computed columns

Add a function in `transform.py`:

```python
def compute_mutation_count(
    df: pd.DataFrame,
    sequence_col: str = "sequence",
    reference_col: str = "uniprot_reference_sequence"
) -> pd.Series:
    """Count mutations per structure vs canonical UniProt sequence."""
    return df.apply(
        lambda row: _count_diff(row[sequence_col], row.get(reference_col, "")),
        axis=1
    )
```

Then wire it in `cli.py`'s transform step.

### Custom field config

Define selected fields + computed columns in YAML:

```yaml
preset: custom
include:
  - entry.rcsb_id
  - entry.rcsb_entry_info.resolution_combined
  - entry.polymer_entities.rcsb_entity_poly_sequence.pdbx_seq_one_letter_code
computed:
  binding_site_count:
    type: int
    depends_on:
      - entry.polymer_entity_instances.rcsb_ligand_neighbors
```

---

## Troubleshooting

### "No PDB entries found"

Possible causes:
- The UniProt ID is incorrect. Verify at https://www.uniprot.org
- The protein has no solved structures in the PDB
- Network issues reaching `https://search.rcsb.org`
- The `max_entries` filter is too restrictive

**Check:** Run `rcsb-pipeline discover --uniprots YOUR_ID` to isolate the discovery step.

### "400 Bad Request" from Search API

The attribute path is incorrect or search is not enabled on it. Run the pipeline with `--verbose` to see the exact error.

**Verified correct attribute:** `rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession`

### Rate limiting

The pipeline respects RCSB's rate limits (default 0.3s between requests). If you see 429 errors:
- Increase `rate_limit` in config (e.g., `rate_limit: 1.0`)
- Reduce `max_concurrent` (e.g., `max_concurrent: 2`)

### Cache corruption

If you get stale or corrupt data:
```bash
# Clear all caches
rm -rf ~/.cache/rcsb-pipeline

# Or bypass for one run
rcsb-pipeline run --uniprots P01116 --no-cache --output ./fresh
```

### Slow performance

- **Use Parquet:** `--format parquet` — 5-10x faster to read/write
- **Bypass cache:** Only if data is stale (cache makes re-runs fast)
- **Reduce field count:** Use `minimal` or `custom` preset
- **Limit entries:** `--max-entries 100` for quick tests

### Large datasets

For runs with 5000+ entries:
- Use `--format parquet` only (CSV will be very large)
- Use `--granularity per-protein` to reduce row count
- Increase `batch_size` to 100
- Monitor disk space — raw JSON can be >100MB for 5000 entries

---

## Development

```bash
# Install in development mode
pip install -e .

# Run tests (25 smoke tests)
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=rcsb_pipeline

# Run on a small test set
rcsb-pipeline run --uniprots P01116 --max-entries 5 --preset minimal --output /tmp/test_run

# Validate output
rcsb-pipeline validate /tmp/test_run/final_dataset.csv
```

### Test structure

| Test File | Tests |
|-----------|-------|
| `tests/test_pipeline.py` | 25 tests covering config, cache, dedup, missing values, aggregation, sanitization, export, reports, unhashable type handling, CLI commands |

---

## License

Internal use — Target Discovery Platform.

---

*Generated by the RCSB PDB Pipeline team. Questions? Contact the platform maintainers.*
