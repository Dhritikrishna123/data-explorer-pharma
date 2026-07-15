# RCSB PDB Pipeline

> Turn protein targets into ML-ready structural datasets in one command.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-186-passing-green)](https://github.com/Dhritikrishna123/data-explorer-pharma)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A CLI tool that automatically discovers, fetches, and exports protein structural data from the [RCSB Protein Data Bank](https://www.rcsb.org) — no manual downloads, no spreadsheets, no scripts.

```bash
pip install -e . && rcsb-pipeline run --uniprots P68871,P69905 --preset drug_discovery --output ./output
```

---

## Why

Drug discovery needs protein structures. But getting clean structural data across multiple targets is tedious:
- Downloading individual PDB files manually
- Cross-referencing UniProt metadata
- Normalizing formats
- Handling missing data
- Keeping track of what you've already processed

This pipeline solves all of that.

---

## Quick Demo

```bash
rcsb-pipeline run \
  --uniprots P68871,P69905 \
  --preset drug_discovery \
  --max-entries 3 \
  --output ./demo
```

In ~10 seconds:

| uniprot_id | pdb_id | exptl_method | resolution | chains | binding_sites | protein_length |
|---|---|---|---|---|---|---|
| P68871 | 1A00 | X-RAY DIFFRACTION | 2.0 Å | 4 | 4 | 147 |
| P68871 | 1A01 | X-RAY DIFFRACTION | 1.8 Å | 4 | 4 | 147 |
| P69905 | 1A9W | X-RAY DIFFRACTION | 2.5 Å | 2 | 1 | 142 |

4 output files + 4 reports generated automatically.

---

## Features

**End-to-end pipeline** — Input UniProt IDs, get a clean dataset. No intermediate steps.
```bash
rcsb-pipeline run --uniprots P01116,P04637 --preset standard
```

**4 built-in presets** — From lightweight to comprehensive.
| Preset | Columns | Use Case |
|--------|---------|----------|
| `minimal` | 10 | Quick feasibility checks |
| `standard` | 54 | General structural analysis |
| `full` | 3000+ | Deep schema exploration |
| `drug_discovery` | 17 | Target screening (structure + ligands + derived fields) |

**Rich output** — CSV, Parquet, JSON, or Excel. Plus 4 automated reports.
```
output/
├── final_dataset.csv
├── final_dataset.parquet
├── summary.json
└── reports/
    ├── coverage_report.md
    ├── missing_data_report.md
    ├── duplicate_report.md
    └── field_coverage.md
```

**Production-grade** — Caching, checkpoints, registry, retries, rate limiting.
```bash
# Resume a partial run
rcsb-pipeline run --uniprots P68871 --preset standard --resume checkpoint.json
# Skip already-exported targets
rcsb-pipeline run --uniprots P68871 --preset standard --skip-registered
```

**186 tests** — pytest + mypy + ruff in CI.

---

## Architecture

```
UniProt IDs ──► Discovery ──► Fetch ──► Transform ──► Export ──► CSV / Parquet
                    │              │            │              │
                    ▼              ▼            ▼              ▼
              RCSB Search    RCSB Data    Pandas ops     4 reports
                API (REST)    API (GQL)   + computed      + registry
                                          columns         + checkpoint
```

- **Discovery**: Finds all PDB entries matching your UniProt IDs (RCSB Search API)
- **Fetch**: Downloads structural metadata via GraphQL with batching, caching, and retries
- **Transform**: Extracts fields, deduplicates, handles missing values, aggregates, adds computed columns
- **Export**: Writes final dataset + reports + run config + checkpoint

---

## Presets

### `drug_discovery` — Designed for target screening

| Category | Fields |
|----------|--------|
| **Structure** | PDB ID, method, resolution, molecular weight |
| **Chains** | number_of_chains (computed) |
| **Ligands** | ligand types, binding_site_count (computed) |
| **Sequence** | UniProt sequence, protein_length (computed), PDB sequence |
| **Metadata** | organism, protein name |

Derived fields like `protein_length`, `number_of_chains`, and `binding_site_count` are computed automatically — no manual calculation needed.

### Custom presets

Define your own field set in a YAML file:

```yaml
# my_preset.yaml
include:
  - entry.rcsb_id
  - entry.rcsb_entry_info.resolution_combined
  - uniprot.rcsb_uniprot_protein.sequence
```

```bash
rcsb-pipeline run --uniprots P68871 --fields my_preset.yaml
```

---

## Command Reference

| Command | What it does |
|---------|-------------|
| `rcsb-pipeline run` | Full pipeline: discover → fetch → transform → export |
| `rcsb-pipeline discover` | Just find PDB IDs (no fetch) |
| `rcsb-pipeline fetch` | Just download data for given PDB IDs |
| `rcsb-pipeline validate` | Check a completed dataset for integrity |
| `rcsb-pipeline report` | Generate reports from existing output |
| `rcsb-pipeline fields` | Browse all available RCSB schema fields |
| `rcsb-pipeline columns` | Search the 15K-entry column registry |
| `rcsb-pipeline init-config` | Generate a starter config file |

---

## Validation

Every dataset is automatically validated:
- **Null rates** (warns on columns >90% null)
- **Duplicates** (reports count and keys)
- **Derived fields** (checks computed values match source data)
- **Type consistency** (coerces numeric strings automatically)

For a detailed walkthrough of validation against ground truth RCSB and UniProt data, see the [validation notes](DEMO_GUIDE.md).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.10+ |
| **CLI** | Typer + Rich |
| **APIs** | RCSB PDB Search REST + Data GraphQL |
| **Data** | Pandas, PyArrow, OpenPyXL |
| **Config** | Pydantic + PyYAML |
| **Cache** | SQLite |
| **Quality** | Ruff (lint + format), MyPy (type check), pytest (186 tests) |

---

## Installation

```bash
git clone https://github.com/Dhritikrishna123/data-explorer-pharma.git
cd data-explorer-pharma
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Optional dev tools:
```bash
pip install -e ".[dev]"
pre-commit install
```

---

## License

MIT
