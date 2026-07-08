"""Live schema introspection — wraps the schema_explorer for field lookup."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from rcsbapi.data import DataSchema

SCHEMA_DIR = Path(__file__).resolve().parent.parent


def _resolve_type(type_dict: dict) -> tuple[str, str, bool, bool]:
    kind = type_dict.get("kind", "")
    type_name = type_dict.get("name")
    nullable = kind != "NON_NULL"
    is_list = False
    oftype = type_dict.get("ofType")
    if kind in ("LIST", "NON_NULL") and oftype:
        sub_name, sub_kind, sub_nullable, sub_list = _resolve_type(oftype)
        if not type_name or type_name == kind:
            type_name = sub_name
        if kind == "LIST" or sub_kind == "LIST":
            is_list = True
        return type_name, kind, nullable, is_list
    return type_name or "Unknown", kind, nullable, is_list


class SchemaLoader:
    """Loads and introspects the live RCSB GraphQL schema."""

    def __init__(self) -> None:
        self._schema = DataSchema()
        self._raw = self._schema.schema["data"]["__schema"]
        self._types = self._raw["types"]
        self._type_map: Dict[str, dict] = {}
        for t in self._types:
            self._type_map[t["name"]] = t

    def list_object_types(self) -> List[str]:
        return sorted(
            t["name"] for t in self._types
            if t.get("kind") == "OBJECT" and not t["name"].startswith("__")
        )

    def get_fields_for_type(self, type_name: str) -> List[dict]:
        t = self._type_map.get(type_name)
        if not t or not t.get("fields"):
            return []
        fields = []
        for f in t["fields"]:
            ret_type, kind, nullable, is_list = _resolve_type(f["type"])
            enum_vals = self._get_enum_values(ret_type)
            fields.append({
                "name": f["name"],
                "type": ret_type,
                "kind": kind,
                "nullable": nullable,
                "is_list": is_list,
                "description": f.get("description", "") or "",
                "enum_values": enum_vals,
            })
        return fields

    def _get_enum_values(self, type_name: str) -> List[str]:
        for t in self._types:
            if t.get("name") == type_name and t.get("kind") == "ENUM":
                return [v["name"] for v in t.get("enumValues") or []]
        return []

    def search_fields(self, query: str) -> List[dict]:
        q = query.lower()
        results = []
        for type_name in self.list_object_types():
            obj_desc = self._type_map.get(type_name, {}).get("description", "") or ""
            for f in self.get_fields_for_type(type_name):
                combined = f"{type_name} {f['name']} {f['description']}"
                if q in combined.lower():
                    results.append({
                        "object_name": type_name,
                        "object_description": obj_desc,
                        "field_name": f["name"],
                        "full_path": f"{type_name}.{f['name']}",
                        "gql_type": f["type"],
                    })
        return results

    def field_exists(self, path: str) -> bool:
        parts = path.split(".")
        if len(parts) < 2:
            return False
        type_name = parts[0]
        field_name = parts[1]
        fields = self.get_fields_for_type(type_name)
        return any(f["name"] == field_name for f in fields)

    def resolve_field_path(self, path: str) -> Optional[dict]:
        parts = path.split(".")
        if len(parts) < 2:
            return None
        type_name = parts[0]
        field_name = parts[1]
        for f in self.get_fields_for_type(type_name):
            if f["name"] == field_name:
                return {"object": type_name, "field": f}
        return None


def discover_available_fields(
    preset_name: str,
    custom_includes: Optional[List[str]] = None,
    custom_excludes: Optional[List[str]] = None,
) -> List[str]:
    """Resolve field paths from presets and custom overrides."""
    from rcsb_pipeline.config import load_preset

    if preset_name == "full":
        loader = SchemaLoader()
        paths = []
        for type_name in loader.list_object_types():
            for f in loader.get_fields_for_type(type_name):
                paths.append(f"{type_name}.{f['name']}")
        return paths

    cfg = load_preset(preset_name)
    includes = list(cfg.include)
    if custom_includes:
        includes.extend(custom_includes)

    excludes = set(cfg.exclude)
    if custom_excludes:
        excludes.update(custom_excludes)

    return [p for p in includes if p not in excludes]
