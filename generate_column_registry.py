#!/usr/bin/env python3
"""Generate the complete column registry (columns.yaml + COLUMN_REFERENCE.md)
from the live RCSB GraphQL schema.

Usage:
    python generate_column_registry.py
    python generate_column_registry.py --output-dir .
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ── Category classification (mirrors schema_explorer.py) ──

MAX_DEPTH = 4  # Max nesting depth for expanded paths

CATEGORY_MAP: list[tuple] = [
    ("Entry", lambda o: o in ("CoreEntry", "Entry", "CurrentEntry", "StructKeywords") or o.startswith("RcsbEntry")),
    (
        "Polymer Entity",
        lambda o: (
            (
                o == "CorePolymerEntity"
                or o.startswith("RcsbPolymerEntity")
                or o == "EntityPoly"
                or o == "GeneName"
                or o.startswith("RcsbEntitySource")
                or o.startswith("RcsbEntityHost")
                or o == "StructAsym"
            )
            and "Instance" not in o
        ),
    ),
    (
        "Polymer Entity Instance",
        lambda o: (
            "PolymerEntityInstance" in o
            or o == "CorePolymerEntityInstance"
            or o.startswith("RcsbPolymerInstance")
            or "PolymerInstanceFeature" in o
        ),
    ),
    ("Branched Entity", lambda o: o == "CoreBranchedEntity" or "BranchedEntity" in o or o == "PdbxEntityBranch"),
    (
        "Nonpolymer Entity",
        lambda o: (
            (o == "CoreNonpolymerEntity" or o.startswith("RcsbNonpolymerEntity") or o == "PdbxEntityNonpoly")
            and "Instance" not in o
            and "Annotation" not in o
        ),
    ),
    ("Nonpolymer Entity Instance", lambda o: "NonpolymerEntityInstance" in o or o.startswith("RcsbNonpolymerInstance")),
    (
        "Assembly",
        lambda o: (
            o == "CoreAssembly"
            or o.startswith("RcsbAssembly")
            or o.startswith("PdbxStructAssembly")
            or o == "PdbxStructOperList"
            or o == "PdbxStructSpecialSymmetry"
            or "StructSymmetry" in o
        ),
    ),
    ("Interface", lambda o: o == "CoreInterface" or o.startswith("RcsbInterface")),
    (
        "Chemical Component",
        lambda o: (
            o == "CoreChemComp"
            or o == "ChemComp"
            or o.startswith("RcsbChemComp")
            or o.startswith("PdbxChemComp")
            or o.startswith("PdbxReference")
        ),
    ),
    (
        "Experimental Data (X-ray)",
        lambda o: (
            o.startswith("Diffrn")
            or o in ("Cell", "Symmetry")
            or o == "Refine"
            or o.startswith("Refine")
            or o == "Reflns"
            or "Reflns" in o
            or o == "PdbxReflnsTwin"
        ),
    ),
    ("Experimental Data (EM)", lambda o: o.startswith("Em") or "Em" in o[:3]),
    ("Experimental Data (NMR)", lambda o: o.startswith("PdbxNmr")),
    ("Experimental Data (XFEL)", lambda o: o.startswith("PdbxSerialCrystallography") or o.startswith("PdbxSerial")),
    ("Experimental Data (SAXS)", lambda o: o.startswith("PdbxSolnScatter")),
    ("Validation Report", lambda o: o.startswith("PdbxVrpt")),
    ("Citation", lambda o: o == "Citation" or o == "RcsbPrimaryCitation" or o.startswith("RcsbBirdCitation")),
    ("PubMed Integration", lambda o: o == "CorePubmed" or o.startswith("RcsbPubmed") or "Pubmed" in o),
    ("DrugBank Integration", lambda o: o == "CoreDrugbank" or o.startswith("Drugbank") or "Drugbank" in o),
    ("Pfam Integration", lambda o: o == "CorePfam" or o.startswith("RcsbPfam") or "Pfam" in o),
    (
        "Target & Ligand Information",
        lambda o: (
            o.startswith("RcsbTarget")
            or o.startswith("RcsbLigand")
            or o.startswith("RcsbBinding")
            or "RcsbRelatedTarget" in o
        ),
    ),
    (
        "Computational Models",
        lambda o: (
            o.startswith("RcsbCompModel")
            or o.startswith("RcsbMaQaMetric")
            or o.startswith("RcsbIhm")
            or o.startswith("Ihm")
            or o == "MaData"
        ),
    ),
    (
        "Audit & Version History",
        lambda o: (
            o.startswith("PdbxAudit")
            or o.startswith("AuditAuthor")
            or o == "RcsbAccessionInfo"
            or o == "RcsbLatestRevision"
            or o == "CurrentEntry"
            or o.startswith("PdbxDatabase")
        ),
    ),
    ("Organism/Source", lambda o: o.startswith("EntitySrc") or o.startswith("PdbxEntitySrc")),
    (
        "Clusters & Groups",
        lambda o: (
            "ClustersMembers" in o
            or o.startswith("RcsbCluster")
            or o.startswith("RcsbGroup")
            or o.startswith("Group")
            or o.startswith("RcsbSchema")
        ),
    ),
    ("Software", lambda o: o == "Software" or "PdbxSoftware" in o),
    (
        "Database Cross-References",
        lambda o: o.startswith("RcsbExternalReferences") or o == "Database2" or o.startswith("PdbxDatabaseRelated"),
    ),
    ("Membrane & Genomic Context", lambda o: o.startswith("RcsbMembrane") or o.startswith("RcsbGenomic")),
    (
        "Sequence Features",
        lambda o: (
            "RcsbPolymerEntityAlign" in o
            or "RcsbPolymerEntityGroupSequenceAlignment" in o
            or "CoreEntityAlignments" in o
            or "AlignedRegion" in o
            or "Alignment" in o
            or "RcsbPolymerEntityContainerIdentifiersReferenceSequence" in o
        ),
    ),
]

DEFAULT_CATEGORY = "Other"
BUILTIN_TYPES = {"String", "Int", "Float", "Boolean", "Date", "ObjectScalar", "JSON", "ID"}


def find_category(obj_name: str) -> str:
    for cat, matcher in CATEGORY_MAP:
        if matcher(obj_name):
            return cat
    return DEFAULT_CATEGORY


def is_internal(name: str) -> bool:
    return name.startswith("__")


def resolve_type(type_dict: dict) -> tuple[str, str, bool, bool]:
    kind = type_dict.get("kind", "")
    type_name = type_dict.get("name")
    nullable = kind != "NON_NULL"
    is_list = False
    oftype = type_dict.get("ofType")
    if kind in ("LIST", "NON_NULL") and oftype:
        sub_name, sub_kind, sub_nullable, sub_list = resolve_type(oftype)
        if not type_name or type_name == kind:
            type_name = sub_name
        if kind == "LIST" or sub_kind == "LIST":
            is_list = True
        return type_name, kind, nullable, is_list
    return type_name or "Unknown", kind, nullable, is_list


def short_name_from_path(path: str) -> str:
    """Derive a unique short name from a dot-path.
    entry.rcsb_entry_info.resolution_combined → rcsb_entry_info_resolution_combined
    """
    parts = path.split(".")
    return "_".join(parts[1:]) if len(parts) > 1 else path


# ── Schema introspection ──


def introspect_schema() -> dict[str, Any]:
    try:
        from rcsbapi.data import DataSchema
    except ImportError:
        print("ERROR: rcsb-api required. Install: pip install rcsb-api")
        sys.exit(1)

    schema = DataSchema()
    raw = schema.schema["data"]["__schema"]
    types_list: list[dict] = raw["types"]

    type_map: dict[str, dict] = {}
    enum_names: set = set()
    object_names: set = set()
    for t in types_list:
        name = t.get("name", "")
        if is_internal(name):
            continue
        type_map[name] = t
        if t.get("kind") == "ENUM":
            enum_names.add(name)
        elif t.get("kind") == "OBJECT":
            object_names.add(name)

    query_type = next((t for t in types_list if t.get("name") == "Query"), None)

    root_fields: list[dict] = []
    if query_type:
        for f in query_type.get("fields") or []:
            ret_type, kind, nullable, is_list = resolve_type(f["type"])
            root_fields.append(
                {
                    "name": f["name"],
                    "type": ret_type,
                    "kind": kind,
                    "nullable": nullable,
                    "is_list": is_list,
                    "description": f.get("description", "") or "",
                }
            )

    obj_fields: dict[str, list[dict]] = {}
    for obj_name in object_names:
        type_entry = type_map.get(obj_name)
        if not type_entry or not type_entry.get("fields"):
            continue
        fields = []
        for f in type_entry["fields"]:
            ret_type, kind, nullable, is_list = resolve_type(f["type"])
            enum_vals = []
            if ret_type in enum_names:
                et = type_map.get(ret_type)
                if et:
                    enum_vals = [v["name"] for v in et.get("enumValues") or []]
            fields.append(
                {
                    "name": f["name"],
                    "type": ret_type,
                    "kind": kind,
                    "nullable": nullable,
                    "is_list": is_list,
                    "description": f.get("description", "") or "",
                    "enum_values": enum_vals,
                }
            )
        obj_fields[obj_name] = fields

    return {
        "type_map": type_map,
        "obj_fields": obj_fields,
        "object_names": sorted(object_names),
        "enum_names": sorted(enum_names),
        "root_fields": root_fields,
        "query_type": query_type,
    }


def expand_catalog(schema_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Build a flat catalog of all field paths under `entry` and `uniprot`
    root types using a depth-limited recursive walk.

    Each type is expanded once per unique parent path to capture all
    distinct columns. Depth limit + cycle prevention keeps the catalog
    to a practical size (~5K-8K entries).
    """
    obj_fields = schema_data["obj_fields"]
    type_map = schema_data["type_map"]

    root_names = {"entry", "uniprot"}
    catalog: list[dict[str, Any]] = []
    seen_paths: set = set()

    def walk(root_name: str, type_name: str, current_path: str, depth: int) -> None:
        if depth > MAX_DEPTH or type_name in BUILTIN_TYPES:
            return

        parent_desc = type_map.get(type_name, {}).get("description", "") or ""
        fields = obj_fields.get(type_name, [])

        for f in fields:
            if f["name"].startswith("__"):
                continue
            full_path = f"{current_path}.{f['name']}"
            if full_path in seen_paths:
                continue
            seen_paths.add(full_path)

            is_obj = f["type"] in obj_fields and f["type"] not in BUILTIN_TYPES and f["type"] != type_name
            catalog.append(
                {
                    "object_name": type_name,
                    "object_description": parent_desc,
                    "parent_object": current_path.split(".")[-1],
                    "full_path": full_path,
                    "field_name": f["name"],
                    "gql_type": f["type"],
                    "nullable": f["nullable"],
                    "is_list": f["is_list"],
                    "description": f["description"],
                    "category": find_category(type_name),
                    "sub_type": "object" if is_obj else "scalar",
                }
            )

            if is_obj:
                walk(root_name, f["type"], full_path, depth + 1)

    for root in schema_data["root_fields"]:
        if root["name"] in root_names:
            walk(root["name"], root["type"], root["name"], 0)

    return catalog


def build_columns_yaml(catalog: list[dict[str, Any]]) -> dict:
    columns: dict[str, Any] = {}
    dups: dict[str, list[str]] = {}
    for entry in catalog:
        # Include all field types — scalar, object, and list fields are
        # all valid DataQuery return_data_list items (object/list returns
        # nested JSON that the pipeline can flatten)
        if entry["field_name"].startswith("__"):
            continue
        name = short_name_from_path(entry["full_path"])
        path = entry["full_path"]

        if name in columns:
            existing_path = columns[name]["path"]
            existing_is_entry = existing_path.startswith("entry.")
            incoming_is_entry = path.startswith("entry.")
            dups.setdefault(name, []).append(path)
            # Prefer entry version over uniprot for same name
            if incoming_is_entry and not existing_is_entry:
                columns[name] = _make_column(name, entry)
            elif not incoming_is_entry and existing_is_entry:
                pass  # keep the existing entry version
            else:
                # Both are same root type — suffix to disambiguate
                suffix = path.split(".")[0]
                alt_name = f"{name}_{suffix}"
                columns[alt_name] = _make_column(alt_name, entry)
            continue

        columns[name] = _make_column(name, entry)

    return {
        "meta": {
            "version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_columns": len(columns),
            "duplicate_resolutions": {n: p for n, p in dups.items() if len(p) > 1},
            "description": "Complete RCSB PDB column registry. Generated from live GraphQL introspection.",
        },
        "columns": columns,
    }


def _make_column(name: str, entry: dict) -> dict:
    return {
        "name": name,
        "path": entry["full_path"],
        "type": entry["gql_type"],
        "nullable": entry["nullable"],
        "is_list": entry["is_list"],
        "sub_type": entry["sub_type"],
        "category": entry["category"],
        "description": entry["description"].strip() if entry.get("description") else "",
    }


def write_columns_yaml(data: dict, path: str) -> None:
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=True, allow_unicode=True, width=120)
    total = data["meta"]["total_columns"]
    with open(path, "w") as f:
        f.write(f"# RCSB PDB Column Registry — {total} columns\n")
        f.write(f"# Generated: {data['meta']['generated_at']}\n")
        f.write("#\n")
        f.write("# Usage:\n")
        f.write('#   rcsb-pipeline run --uniprots P01116 --columns "rcsb_id,resolution,sequence"\n')
        f.write("#   rcsb-pipeline columns --search resolution\n")
        f.write('#   rcsb-pipeline columns --category "Polymer Entity"\n')
        f.write("#\n")
        yaml_lines = yaml_str.split("\n")
        for line in yaml_lines:
            f.write(line + "\n")
    size = Path(path).stat().st_size / 1024
    print(f"  ✓ {path} ({total} columns, {size:.0f} KB)")


def build_column_reference(catalog: list[dict[str, Any]]) -> str:
    by_category: dict[str, list[dict]] = defaultdict(list)
    for entry in catalog:
        by_category[entry["category"]].append(entry)

    lines: list[str] = []
    lines.append("# Column Reference — RCSB PDB Pipeline\n")
    lines.append(f"*Generated from live RCSB GraphQL schema on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}*\n")
    lines.append(f"Total: **{len(catalog)}** fields across **{len(by_category)}** categories.\n")
    lines.append("## Column naming convention\n")
    lines.append("Columns are derived from dot-paths by stripping the root type (`entry.` / `uniprot.`)")
    lines.append("and joining remaining segments with underscores. The result is both the **short name**")
    lines.append("(used with `--columns`) and the **output column name** in the final dataset.\n")
    lines.append("| Example Path | Short Name |")
    lines.append("|---|---|")
    lines.append("| `entry.rcsb_id` | `rcsb_id` |")
    lines.append("| `entry.rcsb_entry_info.resolution_combined` | `rcsb_entry_info_resolution_combined` |")
    lines.append("| `uniprot.rcsb_uniprot_protein.name` | `rcsb_uniprot_protein_name` |")
    lines.append("")
    lines.append("## Base columns (always included)\n")
    lines.append("| Column | Source | Type | Description |")
    lines.append("|---|---|---|---|")
    lines.append("| `uniprot_id` | CLI input | string | UniProt accession |")
    lines.append("| `pdb_id` | `entry.rcsb_id` | string | PDB entry identifier |")
    lines.append("| `structure_available` | derived | bool | True if PDB structure exists for this pair |")
    lines.append("| `binding_site_count` | computed | int | Approximate unique ligand count per chain |")
    lines.append("")

    # Category index
    lines.append("## Categories\n")
    lines.append("| # | Category | Fields |")
    lines.append("|---|----------|-------|")
    for idx, (cat, entries) in enumerate(sorted(by_category.items()), 1):
        lines.append(f"| {idx} | {cat} | {len(entries)} |")
    lines.append("")
    lines.append("---\n")

    for cat, entries in sorted(by_category.items()):
        lines.append(f"### {cat}\n")
        lines.append("| Short Name | Path | Type | Nullable | List | Description |")
        lines.append("|---|---|---|---|---|---|")
        for entry in sorted(entries, key=lambda e: e["full_path"]):
            name = short_name_from_path(entry["full_path"])
            desc = entry["description"].strip().replace("\n", " ") if entry.get("description") else ""
            if len(desc) > 100:
                desc = desc[:97] + "..."
            lines.append(
                f"| `{name}` | `{entry['full_path']}` | `{entry['gql_type']}` | "
                f"{str(entry['nullable']):5s} | {str(entry['is_list']):5s} | {desc} |"
            )
        lines.append("")
    lines.append("---\n")
    lines.append("*End of column reference.*\n")
    return "\n".join(lines) + "\n"


def write_column_reference(md: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(md)
    size = Path(path).stat().st_size / 1024 if Path(path).exists() else 0
    entry_count = md.count("| `")
    print(f"  ✓ {path} ({entry_count} entries, {size:.0f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the complete RCSB PDB column registry")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current dir)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Introspecting RCSB GraphQL schema...")
    schema_data = introspect_schema()
    print(f"  {len(schema_data['object_names'])} object types, {len(schema_data['enum_names'])} enums")

    print("Building catalog...")
    catalog = expand_catalog(schema_data)
    print(f"  {len(catalog)} expanded field paths")

    print("Generating columns.yaml...")
    yaml_data = build_columns_yaml(catalog)
    yaml_path = output_dir / "columns.yaml"
    write_columns_yaml(yaml_data, str(yaml_path))

    print("Generating COLUMN_REFERENCE.md...")
    md = build_column_reference(catalog)
    md_path = output_dir / "COLUMN_REFERENCE.md"
    write_column_reference(md, str(md_path))

    # Also copy to package dir if applicable
    pkg_dir = output_dir / "rcsb_pipeline"
    if pkg_dir.is_dir():
        dest = pkg_dir / "columns.yaml"
        if not dest.exists():
            import shutil

            shutil.copy2(yaml_path, dest)
            print(f"  ✓ Copied to {dest}")
    else:
        # Maybe the package is at the parent
        parent_pkg = Path(__file__).resolve().parent / "rcsb_pipeline"
        if parent_pkg.is_dir():
            dest = parent_pkg / "columns.yaml"
            import shutil

            shutil.copy2(yaml_path, dest)
            print(f"  ✓ Copied to {dest}")

    print("\nDone!")


if __name__ == "__main__":
    main()
