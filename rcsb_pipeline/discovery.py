"""Discovery layer — uses RCSB Search API to find PDB entries for UniProts."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from rich.progress import Progress

from rcsb_pipeline.cache import ResponseCache

logger = logging.getLogger("rcsb-pipeline")


def discover_pdb_ids(
    uniprot_ids: list[str],
    cache: ResponseCache,
    max_entries: int = 1000,  # noqa: ARG001
    min_resolution: float = 0.0,  # noqa: ARG001
    max_resolution: float = 10.0,  # noqa: ARG001
    experimental_methods: list[str] | None = None,  # noqa: ARG001
    exclude_deprecated: bool = True,  # noqa: ARG001
    progress: Progress | None = None,
) -> tuple[dict[str, list[str]], list[dict[str, Any]]]:
    """For each UniProt ID, find matching PDB entries via RCSB Search API.

    Returns:
        (uniprot_to_pdbs, raw_results):
            uniprot_to_pdbs: {uniprot_id: [pdb_id, ...]}
            raw_results: list of raw search response dicts
    """
    from rcsbapi.search import AttributeQuery, NestedAttributeQuery

    uniprot_to_pdbs: dict[str, list[str]] = {}
    all_raw: list[dict[str, Any]] = []
    seen_pdbs: set[str] = set()

    task = None
    if progress:
        task = progress.add_task("[cyan]Discovering PDB entries...", total=len(uniprot_ids))

    for uid in uniprot_ids:
        uid = uid.strip()
        if not uid:
            continue

        cache_key = f"discover:{uid}"
        cached = cache.get(cache_key)
        if cached is not None:
            result = cached
        else:
            try:
                q1 = AttributeQuery(
                    attribute="rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                    operator="exact_match",
                    value=uid,
                )
                q2 = AttributeQuery(
                    attribute="rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_name",
                    operator="exact_match",
                    value="UniProt",
                )
                query = NestedAttributeQuery(q1, q2)
                result = list(query(return_type="entry"))
                cache.set(cache_key, result)
                time.sleep(0.3)
            except Exception:  # noqa: BLE001
                result = []
                logger.warning("Discovery failed for %s", uid, exc_info=True)

        all_raw.append({"uniprot_id": uid, "result": result})

        pdb_ids = []
        if isinstance(result, list):
            for item in result:
                if isinstance(item, str):
                    pdb_id = item.strip().upper()
                    if pdb_id and pdb_id not in seen_pdbs:
                        pdb_ids.append(pdb_id)
                        seen_pdbs.add(pdb_id)
                elif isinstance(item, dict):
                    pdb_id = item.get("entry_id") or item.get("id", "")
                    if pdb_id and pdb_id not in seen_pdbs:
                        pdb_ids.append(pdb_id)
                        seen_pdbs.add(pdb_id)

        uniprot_to_pdbs[uid] = pdb_ids
        if task is not None and progress is not None:
            progress.advance(task)

    return uniprot_to_pdbs, all_raw


def resolve_gene_symbols(
    gene_symbols: list[str],
    cache: ResponseCache,
) -> dict[str, str]:
    """Resolve gene symbols to UniProt IDs using MyGene.info."""
    import requests

    result: dict[str, str] = {}
    for gene in gene_symbols:
        gene = gene.strip()
        if not gene:
            continue
        cache_key = f"gene:{gene}"
        cached = cache.get(cache_key)
        if cached is not None:
            if cached:
                result[gene] = cached
            continue
        try:
            resp = requests.get(
                "https://mygene.info/v3/query",
                params={"q": gene, "species": "human", "fields": "uniprot", "size": "1"},
                timeout=10,
            )
            data = resp.json()
            uniprot = None
            hits = data.get("hits", [])
            if hits:
                uniprot_info = hits[0].get("uniprot", {})
                if isinstance(uniprot_info, dict):
                    uniprot = uniprot_info.get("Swiss-Prot") or uniprot_info.get("TrEMBL")
            if uniprot:
                result[gene] = uniprot
                cache.set(cache_key, uniprot)
            else:
                cache.set(cache_key, "")
            time.sleep(0.1)
        except Exception:  # noqa: BLE001
            logger.warning("Gene symbol resolution failed for %s", gene, exc_info=True)
            cache.set(cache_key, "")
    return result


def save_discovery_results(
    uniprot_to_pdbs: dict[str, list[str]],
    output_dir: str,
) -> None:
    """Save discovery results to JSON."""
    path = Path(output_dir) / "discovered_pdb_ids.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(uniprot_to_pdbs, f, indent=2)

    all_pdbs = sorted(set(p for ids in uniprot_to_pdbs.values() for p in ids))
    pdb_path = Path(output_dir) / "all_pdb_ids.json"
    with open(pdb_path, "w") as f:
        json.dump(all_pdbs, f, indent=2)

    summary = {
        "total_uniprots": len(uniprot_to_pdbs),
        "total_pdb_ids": len(all_pdbs),
        "uniprots_with_structures": sum(1 for v in uniprot_to_pdbs.values() if v),
        "uniprots_without_structures": sum(1 for v in uniprot_to_pdbs.values() if not v),
    }
    summary_path = Path(output_dir) / "discovery_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
