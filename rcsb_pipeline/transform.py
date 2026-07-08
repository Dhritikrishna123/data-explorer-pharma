"""Transformation layer — deduplication, missing value handling, aggregation, sanitization."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import pandas as pd


def deduplicate(
    df: pd.DataFrame,
    strategy: str = "strict",
    keys: list[str] | None = None,
    sort_key: str | None = None,
    sort_ascending: bool = True,
) -> pd.DataFrame:
    """Remove duplicate rows according to the given strategy.

    Strategies:
        strict:     Drop rows where ALL columns are identical
        key-only:   Drop by composite key (default: all columns)
        keep-first: First occurrence wins
        keep-best:  Sort by sort_key, keep best (first after sort)
        keep-latest: Keep most recent (reverse sort by sort_key)
        none:       No deduplication
    """
    if strategy == "none" or df.empty:
        return df

    if strategy == "strict":
        return df.drop_duplicates(keep="first").reset_index(drop=True)

    if strategy == "key-only":
        dedup_keys = keys or df.columns.tolist()
        return df.drop_duplicates(subset=dedup_keys, keep="first").reset_index(drop=True)

    if strategy == "keep-first":
        return df.drop_duplicates(keep="first").reset_index(drop=True)

    if strategy in ("keep-best", "keep-latest"):
        if sort_key and sort_key in df.columns:
            ascending = sort_ascending if strategy == "keep-best" else (not sort_ascending)
            df = df.sort_values(sort_key, ascending=ascending)
        dedup_keys = keys or df.columns.tolist()
        return df.drop_duplicates(subset=dedup_keys, keep="first").reset_index(drop=True)

    return df


def handle_missing(
    df: pd.DataFrame,
    strategy: str = "fill-null",
    fill_value: Any = None,
) -> pd.DataFrame:
    """Handle missing values in the DataFrame.

    Strategies:
        drop:       Drop rows with any null values
        fill-null:  Leave as NaN (no change)
        fill-0:     Fill numeric with 0, string with ""
        fill-mean:  Fill numeric with column mean, string with mode
        fill-value: Fill with the provided fill_value
    """
    if df.empty:
        return df

    if strategy == "drop":
        return df.dropna().reset_index(drop=True)

    if strategy == "fill-null":
        return df

    if strategy == "fill-0":
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("")
        return df

    if strategy == "fill-mean":
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else "")
        return df

    if strategy == "fill-value":
        return df.fillna(fill_value)

    return df


def aggregate_protein_rows(
    df: pd.DataFrame,
    group_key: str = "uniprot_id",
    mode: str = "pick-best",
    sort_key: str | None = None,
    sort_ascending: bool = True,
) -> pd.DataFrame:
    """Aggregate multiple rows per protein into one.

    Modes:
        pick-best: Keep the best row (sorted by sort_key)
        mean:      Numeric mean, string mode
        min:       Numeric min, first alphabetically
        max:       Numeric max, last alphabetically
        concat:    Comma-separated list of all values
    """
    if df.empty or group_key not in df.columns:
        return df

    if mode == "pick-best":
        if sort_key and sort_key in df.columns:
            df = df.sort_values(sort_key, ascending=sort_ascending)
        return df.drop_duplicates(subset=[group_key], keep="first").reset_index(drop=True)

    if mode in ("mean", "min", "max"):
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        string_cols = df.select_dtypes(exclude="number").columns.tolist()

        agg_map: dict[str, str | Callable] = {}
        for c in numeric_cols:
            if c != group_key:
                agg_map[c] = mode
        for c in string_cols:
            if c != group_key:
                agg_map[c] = (
                    "first"
                    if mode == "pick-best"
                    else (lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
                )

        if agg_map:
            result = df.groupby(group_key).agg(agg_map).reset_index()
            return result

    if mode == "concat":
        return df.groupby(group_key).agg(lambda x: ", ".join(str(v) for v in x.unique() if pd.notna(v))).reset_index()

    return df


def compute_binding_site_count(
    df: pd.DataFrame,
    ligand_neighbor_col: str | None = None,
) -> pd.Series:
    """Compute approximate binding site count from ligand neighbor data.

    If a column with ligand neighbor info exists, count unique ligand_comp_id values.
    Otherwise return 0 for all rows.
    """
    if ligand_neighbor_col and ligand_neighbor_col in df.columns:
        return df[ligand_neighbor_col].apply(
            lambda x: len(set(str(x).split(","))) if pd.notna(x) and str(x).strip() else 0
        )
    return pd.Series([0] * len(df), index=df.index)


def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce string columns that look numeric to proper numeric types."""
    for col in df.columns:
        if df[col].dtype == object:
            try:
                numeric = pd.to_numeric(df[col], errors="coerce")
                if numeric.notna().sum() > len(df) * 0.5:
                    df[col] = numeric
            except (ValueError, TypeError):
                pass
    return df


def _flatten_unhashable(df: pd.DataFrame) -> pd.DataFrame:
    """Convert unhashable column types (dict, list) to JSON strings for dedup."""
    df = df.copy()
    for col in df.columns:
        sample = df[col].dropna()
        if len(sample) == 0:
            continue
        non_scalar_types = {type(v) for v in sample if not isinstance(v, str | int | float | bool | bytes | type(None))}
        if non_scalar_types:
            df[col] = df[col].apply(
                lambda x: json.dumps(x, default=str) if isinstance(x, dict | list | tuple | set) else x
            )
    return df


def sanitize(
    df: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """Full sanitization pipeline: coerce → flatten → dedup → missing → aggregate."""
    if df.empty:
        return df

    df = coerce_types(df)
    df = _flatten_unhashable(df)

    dedup_strategy = config.get("dedup_strategy", "strict")
    dedup_keys = config.get("dedup_keys", [])
    sort_key = config.get("aggregation_key")

    df = deduplicate(
        df,
        strategy=dedup_strategy,
        keys=dedup_keys if dedup_keys else None,
        sort_key=sort_key,
        sort_ascending=config.get("sort_ascending", True),
    )

    missing_action = config.get("missing_action", "fill-null")
    df = handle_missing(df, strategy=missing_action)

    granularity = config.get("granularity", "per-structure")
    if granularity == "per-protein":
        group_key = config.get("group_key", "uniprot_id")
        agg_mode = config.get("aggregation_mode", "pick-best")
        df = aggregate_protein_rows(
            df,
            group_key=group_key,
            mode=agg_mode,
            sort_key=sort_key,
        )

    return df
