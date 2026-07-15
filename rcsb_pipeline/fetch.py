"""Data fetch layer — batch-fetch PDB entry data and UniProt enhanced data."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from rcsbapi.data import DataQuery
from rich.progress import Progress

from rcsb_pipeline.cache import ResponseCache

logger = logging.getLogger("rcsb-pipeline")


def _strip_prefix(path: str, prefix: str = "entry.") -> str:
    return path[len(prefix) :] if path.startswith(prefix) else path


def _execute_entry_query(pdb_ids: list[str], field_paths: list[str]) -> dict[str, Any]:
    clean = [_strip_prefix(p, "entry.") for p in field_paths]
    query = DataQuery(
        input_type="entry",
        input_ids=pdb_ids,
        return_data_list=clean,
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


def _execute_uniprot_query(uniprot_ids: list[str], field_paths: list[str]) -> dict[str, Any]:
    clean = [_strip_prefix(p, "uniprot.") for p in field_paths]
    query = DataQuery(
        input_type="uniprot",
        input_ids=uniprot_ids,
        return_data_list=clean,
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
    pdb_ids: list[str],
    field_paths: list[str],
    cache: ResponseCache,
    max_concurrent: int = 5,  # noqa: ARG001
    rate_limit: float = 0.3,
    retry_max: int = 3,  # noqa: ARG001
    progress: Progress | None = None,
) -> dict[str, dict[str, Any] | None]:
    """Fetch entry-level data for a list of PDB IDs.

    Returns:
        {pdb_id: response_dict_or_None}
    """
    results: dict[str, dict[str, Any] | None] = {}
    uncached_ids: list[str] = []

    task = None
    if progress:
        task = progress.add_task("[cyan]Fetching PDB entry data...", total=len(pdb_ids))
    task_id = task

    def _advance() -> None:
        if task_id is not None and progress is not None:
            progress.advance(task_id)

    for pdb_id in pdb_ids:
        cache_key = f"entry:{pdb_id}:{','.join(sorted(field_paths))}"
        cached = cache.get(cache_key)
        if cached is not None:
            results[pdb_id] = cached
            _advance()
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
            except Exception as e:  # noqa: BLE001
                logger.warning("Entry fetch failed for batch starting with %s: %s", batch[0], e, exc_info=True)
                for pdb_id in batch:
                    results[pdb_id] = {"rcsb_id": pdb_id, "error": str(e)}
            for _ in batch:
                _advance()

    return results


def fetch_uniprot_data(
    uniprot_ids: list[str],
    field_paths: list[str],
    cache: ResponseCache,
    max_concurrent: int = 5,  # noqa: ARG001
    rate_limit: float = 0.3,
    progress: Progress | None = None,
) -> dict[str, dict[str, Any] | None]:
    """Fetch UniProt enhanced data for a list of UniProt IDs."""
    results: dict[str, dict[str, Any] | None] = {}
    uncached_ids: list[str] = []

    task = None
    if progress:
        task = progress.add_task("[cyan]Fetching UniProt data...", total=len(uniprot_ids))

    def _advance() -> None:
        if task is not None and progress is not None:
            progress.advance(task)

    for uid in uniprot_ids:
        uid = uid.strip()
        if not uid:
            _advance()
            continue
        cache_key = f"uniprot:{uid}:{','.join(sorted(field_paths))}"
        cached = cache.get(cache_key)
        if cached is not None:
            results[uid] = cached
            _advance()
        else:
            uncached_ids.append(uid)

    if uncached_ids:
        for uid in uncached_ids:
            try:
                data = _execute_uniprot_query([uid], field_paths)
                if uid in data:
                    results[uid] = data[uid]
                    ck = f"uniprot:{uid}:{','.join(sorted(field_paths))}"
                    cache.set(ck, data[uid])
                else:
                    results[uid] = {"rcsb_id": uid, "_no_data": True}
                time.sleep(rate_limit)
            except Exception as e:  # noqa: BLE001
                logger.warning("UniProt fetch failed for %s: %s", uid, e, exc_info=True)
                results[uid] = {"rcsb_id": uid, "error": str(e)}
            _advance()

    return results


def save_raw_data(
    entry_data: dict[str, dict | None],
    uniprot_data: dict[str, dict | None],
    output_dir: str,
) -> None:
    """Save raw fetched data to JSON files."""
    out = Path(output_dir) / "raw"
    out.mkdir(parents=True, exist_ok=True)

    entry_path = out / "entry_data.json"
    with open(entry_path, "w") as f:
        json.dump(
            {k: v for k, v in entry_data.items() if v is not None},
            f,
            indent=2,
            default=str,
        )

    uniprot_path = out / "uniprot_data.json"
    with open(uniprot_path, "w") as f:
        json.dump(
            {k: v for k, v in uniprot_data.items() if v is not None},
            f,
            indent=2,
            default=str,
        )
