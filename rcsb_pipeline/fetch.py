"""Data fetch layer — batch-fetch PDB entry data and UniProt enhanced data."""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from rich.progress import Progress
from rcsbapi.data import DataQuery

from rcsb_pipeline.cache import ResponseCache


def _execute_entry_query(
    pdb_ids: List[str], field_paths: List[str]
) -> Dict[str, Any]:
    query = DataQuery(
        input_type="entry",
        input_ids=pdb_ids,
        return_data_list=field_paths,
    )
    result = query.exec()
    data = {}
    if isinstance(result, dict):
        entries = result.get("data", {}).get("entries", [])
        for entry in entries:
            if isinstance(entry, dict):
                eid = entry.get("rcsb_id", "")
                if eid:
                    data[eid] = entry
    return data


def _execute_uniprot_query(
    uniprot_ids: List[str], field_paths: List[str]
) -> Dict[str, Any]:
    query = DataQuery(
        input_type="uniprot",
        input_ids=uniprot_ids,
        return_data_list=field_paths,
    )
    result = query.exec()
    data = {}
    if isinstance(result, dict):
        uniprot_data = result.get("data", {}).get("uniprot", {})
        uid = uniprot_data.get("rcsb_id", "")
        if uid:
            data[uid] = uniprot_data
        entries = result.get("data", {}).get("entries", [])
        # Some queries may return per-entry uniprot data
        for entry in entries:
            if isinstance(entry, dict):
                eid = entry.get("rcsb_id", "")
                if eid:
                    data[eid] = entry
    return data


def fetch_entry_data(
    pdb_ids: List[str],
    field_paths: List[str],
    cache: ResponseCache,
    max_concurrent: int = 5,
    rate_limit: float = 0.3,
    retry_max: int = 3,
    progress: Optional[Progress] = None,
) -> Dict[str, Optional[Dict[str, Any]]]:
    """Fetch entry-level data for a list of PDB IDs.

    Returns:
        {pdb_id: response_dict_or_None}
    """
    results: Dict[str, Optional[Dict[str, Any]]] = {}
    uncached_ids: List[str] = []

    task = None
    if progress:
        task = progress.add_task("[cyan]Fetching PDB entry data...", total=len(pdb_ids))

    for pdb_id in pdb_ids:
        cache_key = f"entry:{pdb_id}:{','.join(sorted(field_paths))}"
        cached = cache.get(cache_key)
        if cached is not None:
            results[pdb_id] = cached
            if task:
                progress.advance(task)
        else:
            uncached_ids.append(pdb_id)

    if uncached_ids:
        batch_size = 50
        for i in range(0, len(uncached_ids), batch_size):
            batch = uncached_ids[i : i + batch_size]
            try:
                data = _execute_entry_query(batch, field_paths)
                for pdb_id, entry_data in data.items():
                    results[pdb_id] = entry_data
                    ck = f"entry:{pdb_id}:{','.join(sorted(field_paths))}"
                    cache.set(ck, entry_data)
                for pdb_id in batch:
                    if pdb_id not in data:
                        results[pdb_id] = {"rcsb_id": pdb_id, "_no_data": True}
                time.sleep(rate_limit)
            except Exception as e:
                for pdb_id in batch:
                    results[pdb_id] = {"rcsb_id": pdb_id, "error": str(e)}
            if task:
                for _ in batch:
                    progress.advance(task)

    return results


def fetch_uniprot_data(
    uniprot_ids: List[str],
    field_paths: List[str],
    cache: ResponseCache,
    max_concurrent: int = 5,
    rate_limit: float = 0.3,
    progress: Optional[Progress] = None,
) -> Dict[str, Optional[Dict[str, Any]]]:
    """Fetch UniProt enhanced data for a list of UniProt IDs."""
    results: Dict[str, Optional[Dict[str, Any]]] = {}
    uncached_ids: List[str] = []

    task = None
    if progress:
        task = progress.add_task("[cyan]Fetching UniProt data...", total=len(uniprot_ids))

    for uid in uniprot_ids:
        uid = uid.strip()
        if not uid:
            if task:
                progress.advance(task)
            continue
        cache_key = f"uniprot:{uid}:{','.join(sorted(field_paths))}"
        cached = cache.get(cache_key)
        if cached is not None:
            results[uid] = cached
            if task:
                progress.advance(task)
        else:
            uncached_ids.append(uid)

    if uncached_ids:
        batch_size = 50
        for i in range(0, len(uncached_ids), batch_size):
            batch = uncached_ids[i : i + batch_size]
            try:
                data = _execute_uniprot_query(batch, field_paths)
                for uid, entry_data in data.items():
                    results[uid] = entry_data
                    ck = f"uniprot:{uid}:{','.join(sorted(field_paths))}"
                    cache.set(ck, entry_data)
                for uid in batch:
                    if uid not in data:
                        results[uid] = {"rcsb_id": uid, "_no_data": True}
                time.sleep(rate_limit)
            except Exception as e:
                for uid in batch:
                    results[uid] = {"rcsb_id": uid, "error": str(e)}
            if task:
                for _ in batch:
                    progress.advance(task)

    return results


def save_raw_data(
    entry_data: Dict[str, Optional[Dict]],
    uniprot_data: Dict[str, Optional[Dict]],
    output_dir: str,
) -> None:
    """Save raw fetched data to JSON files."""
    out = Path(output_dir) / "raw"
    out.mkdir(parents=True, exist_ok=True)

    entry_path = out / "entry_data.json"
    with open(entry_path, "w") as f:
        json.dump(
            {k: v for k, v in entry_data.items() if v is not None},
            f, indent=2, default=str,
        )

    uniprot_path = out / "uniprot_data.json"
    with open(uniprot_path, "w") as f:
        json.dump(
            {k: v for k, v in uniprot_data.items() if v is not None},
            f, indent=2, default=str,
        )
