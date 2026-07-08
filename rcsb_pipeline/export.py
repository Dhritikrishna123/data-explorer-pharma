"""Export layer — write final dataset to CSV, Parquet, JSON, Excel, and generate reports."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from rcsb_pipeline.registry import ProcessedRegistry


def export_dataset(
    df: pd.DataFrame,
    output_dir: str,
    formats: list[str],
    dataset_name: str = "final_dataset",
    registry: ProcessedRegistry | None = None,
    run_id: str = "",
    preset: str = "",
    granularity: str = "",
) -> dict[str, str]:
    """Write the DataFrame to each requested format.

    If a registry is provided, records every (uniprot_id, pdb_id) pair
    from the dataset so it is never re-processed downstream.

    Returns:
        {format: filepath}
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    if "csv" in formats:
        path = out / f"{dataset_name}.csv"
        df.to_csv(path, index=False)
        written["csv"] = str(path)

    if "parquet" in formats:
        try:
            path = out / f"{dataset_name}.parquet"
            df.to_parquet(path, index=False)
            written["parquet"] = str(path)
        except Exception as e:
            written["parquet"] = f"ERROR: {e}"

    if "json" in formats:
        path = out / f"{dataset_name}.json"
        df.to_json(path, orient="records", lines=True)
        written["json"] = str(path)

    if "xlsx" in formats or "excel" in formats:
        try:
            path = out / f"{dataset_name}.xlsx"
            df.to_excel(path, index=False, engine="openpyxl")
            written["xlsx"] = str(path)
        except Exception as e:
            written["xlsx"] = f"ERROR: {e}"

    summary_path = out / "dataset_summary.json"
    _write_summary(df, summary_path)

    # ── Record in registry ──
    _record_in_registry(df, registry, run_id, preset, granularity, output_dir)

    return written


def _record_in_registry(
    df: pd.DataFrame,
    registry: ProcessedRegistry | None,
    run_id: str,
    preset: str,
    granularity: str,
    output_dir: str,
) -> int:
    """Record all (uniprot_id, pdb_id) pairs in the registry.

    Returns count of recorded pairs.
    """
    if registry is None:
        return 0

    if "uniprot_id" not in df.columns or "pdb_id" not in df.columns:
        return 0

    pairs: list[tuple] = []
    seen: set = set()
    for _, row in df.iterrows():
        uid = str(row.get("uniprot_id", "") or "")
        pid = str(row.get("pdb_id", "") or "")
        key = (uid, pid)
        if key not in seen and uid and pid:
            seen.add(key)
            pairs.append((uid, pid))

    if not pairs:
        return 0

    count = registry.record_batch(
        pairs,
        run_id=run_id,
        preset=preset,
        granularity=granularity,
        output_dir=output_dir,
    )
    return count


def _write_summary(df: pd.DataFrame, path: Path) -> None:
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "null_counts": {col: int(df[col].isna().sum()) for col in df.columns},
        "null_pcts": {col: round(float(df[col].isna().mean() * 100), 2) for col in df.columns},
        "memory_bytes": int(df.memory_usage(deep=True).sum()),
    }
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)


def report_coverage(
    df: pd.DataFrame,
    uniprot_to_pdbs: dict[str, list[str]] | None = None,
    output_dir: str = ".",
) -> str:
    """Generate coverage report as Markdown."""
    lines = [
        "# Coverage Report\n",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
    ]

    if uniprot_to_pdbs:
        total_uniprots = len(uniprot_to_pdbs)
        uniprots_with = sum(1 for v in uniprot_to_pdbs.values() if v)
        uniprots_without = total_uniprots - uniprots_with
        total_pdbs = len(set(p for ids in uniprot_to_pdbs.values() for p in ids))

        lines.append(f"**Input UniProts:** {total_uniprots}\n")
        lines.append(
            f"**With PDB structures:** {uniprots_with} ({uniprots_with / total_uniprots * 100:.1f}%)\n"
            if total_uniprots
            else ""
        )
        lines.append(f"**Without PDB structures:** {uniprots_without}\n")
        lines.append(f"**Unique PDB entries:** {total_pdbs}\n")
        lines.append(f"**Final dataset rows:** {len(df)}\n")
        lines.append(f"**Final dataset columns:** {len(df.columns)}\n\n")

        lines.append("## UniProt → PDB Mapping\n\n")
        lines.append("| UniProt ID | PDB Count | PDB IDs |\n")
        lines.append("|------------|----------:|--------|\n")
        for uid, pdbs in sorted(uniprot_to_pdbs.items()):
            lines.append(f"| {uid} | {len(pdbs)} | {', '.join(pdbs[:10])}{'...' if len(pdbs) > 10 else ''} |\n")
    else:
        total_uniprots = df["uniprot_id"].nunique() if "uniprot_id" in df.columns else 0
        total_pdbs = df["pdb_id"].nunique() if "pdb_id" in df.columns else 0
        lines.append(f"**Unique UniProts in dataset:** {total_uniprots}\n")
        lines.append(f"**Unique PDB entries:** {total_pdbs}\n")
        lines.append(f"**Total rows:** {len(df)}\n")
        lines.append(f"**Total columns:** {len(df.columns)}\n\n")

    path = Path(output_dir) / "reports" / "coverage_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.writelines(lines)
    return str(path)


def report_missing_data(df: pd.DataFrame, output_dir: str) -> str:
    """Generate missing data report."""
    lines = [
        "# Missing Data Report\n",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
        "| Column | Type | Null Count | Null % |\n",
        "|--------|------|-----------:|------:|\n",
    ]
    for col in df.columns:
        null_count = int(df[col].isna().sum())
        null_pct = round(null_count / len(df) * 100, 2) if len(df) > 0 else 0
        lines.append(f"| {col} | {df[col].dtype} | {null_count} | {null_pct}% |\n")

    path = Path(output_dir) / "reports" / "missing_data_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.writelines(lines)
    return str(path)


def report_duplicates(df: pd.DataFrame, output_dir: str, keys: list[str] | None = None) -> str:
    """Generate duplicate report."""
    lines = [
        "# Duplicate Report\n",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
        f"**Total rows:** {len(df)}\n\n",
    ]

    dedup_keys = keys or df.columns.tolist()
    dup_count = int(df.duplicated(subset=dedup_keys, keep=False).sum())
    lines.append(f"**Duplicate rows (by {dedup_keys}):** {dup_count}\n")
    if dup_count > 0:
        dups = df[df.duplicated(subset=dedup_keys, keep=False)].sort_values(by=dedup_keys)
        lines.append("\n## Duplicate Details\n\n")
        lines.append("```\n")
        lines.append(dups.to_string(max_rows=50))
        lines.append("\n```\n")

    path = Path(output_dir) / "reports" / "duplicate_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.writelines(lines)
    return str(path)


def report_field_coverage(df: pd.DataFrame, output_dir: str) -> str:
    """Generate per-field coverage report."""
    lines = [
        "# Field Coverage Report\n",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
        "| Field | Type | Non-null Count | Non-null % | Unique Values |\n",
        "|-------|------|--------------:|----------:|-------------:|\n",
    ]
    for col in df.columns:
        non_null = int(df[col].notna().sum())
        pct = round(non_null / len(df) * 100, 2) if len(df) > 0 else 0
        unique = int(df[col].nunique())
        lines.append(f"| {col} | {df[col].dtype} | {non_null} | {pct}% | {unique} |\n")

    path = Path(output_dir) / "reports" / "field_coverage.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.writelines(lines)
    return str(path)


def generate_all_reports(
    df: pd.DataFrame,
    uniprot_to_pdbs: dict[str, list[str]],
    output_dir: str,
) -> dict[str, str]:
    """Generate all standard reports."""
    reports = {}
    reports["coverage"] = report_coverage(df, uniprot_to_pdbs, output_dir)
    reports["missing_data"] = report_missing_data(df, output_dir)
    reports["duplicates"] = report_duplicates(df, output_dir)
    reports["field_coverage"] = report_field_coverage(df, output_dir)
    return reports
