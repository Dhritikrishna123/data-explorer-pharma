"""Column Registry — resolve friendly column names to RCSB field paths.

Provides a ColumnRegistry that loads the built-in columns.yaml (or a
user-supplied file) and maps short names like "resolution" to RCSB
DataQuery field paths like "entry.rcsb_entry_info.resolution_combined".
"""

from __future__ import annotations

from pathlib import Path

import yaml

from rcsb_pipeline.config import FieldConfig


def _builtin_path() -> Path:
    return Path(__file__).resolve().parent / "columns.yaml"


class ColumnRegistry:
    """Maps friendly column names to RCSB DataQuery field paths.

    The built-in registry covers all ~10K scalar fields reachable from
    the `entry` and `uniprot` root types in the live RCSB GraphQL schema.
    Users can overlay their own column files to add aliases.
    """

    def __init__(self, column_file: str | None = None) -> None:
        self._columns: dict[str, dict] = {}
        self._load_builtin()
        if column_file:
            self._load_file(column_file)

    def _load_builtin(self) -> None:
        path = _builtin_path()
        if not path.exists():
            return
        with open(path) as f:
            data = yaml.safe_load(f)
        if data and "columns" in data:
            for name, info in data["columns"].items():
                self._columns[name] = info

    def _load_file(self, path: str) -> None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Column file not found: {path}")
        with open(p) as f:
            data = yaml.safe_load(f)
        if not data or "columns" not in data:
            raise ValueError(f"Column file missing 'columns' key: {path}")
        for name, info in data["columns"].items():
            if name in self._columns:
                self._columns[name] = {**self._columns[name], **info}
            else:
                self._columns[name] = info

    @property
    def available(self) -> list[str]:
        """Return all registered short names."""
        return sorted(self._columns.keys())

    @property
    def count(self) -> int:
        return len(self._columns)

    def get(self, name: str) -> dict | None:
        return self._columns.get(name)

    def resolve(self, names: list[str]) -> list[str]:
        """Convert a list of short names to RCSB field paths.

        Raises KeyError if any name is not found.
        """
        paths: list[str] = []
        for name in names:
            info = self._columns.get(name)
            if info is None:
                raise KeyError(
                    f"Unknown column '{name}'. Use 'rcsb-pipeline columns --search {name}' to find available columns."
                )
            path = info.get("path", "")
            if path:
                paths.append(path)
        return paths

    def search(self, query: str) -> list[dict]:
        """Search columns by name, path, description, or category."""
        q = query.lower()
        results = []
        for name, info in self._columns.items():
            combined = " ".join(str(v) for v in info.values())
            if q in name.lower() or q in combined.lower():
                results.append({"name": name, **info})
        return sorted(results, key=lambda r: r["name"])

    def filter_by_category(self, category: str) -> list[dict]:
        """Get all columns in a given category."""
        q = category.lower()
        results = []
        for name, info in self._columns.items():
            if info.get("category", "").lower() == q:
                results.append({"name": name, **info})
        return sorted(results, key=lambda r: r["name"])

    def list_categories(self) -> list[dict[str, object]]:
        """Return all categories with field counts."""
        counts: dict[str, int] = {}
        for info in self._columns.values():
            cat = info.get("category", "Other")
            counts[cat] = counts.get(cat, 0) + 1
        return [{"category": k, "count": v} for k, v in sorted(counts.items())]

    def to_field_config(self, names: list[str]) -> FieldConfig:
        """Build a FieldConfig from a list of short column names.

        This sets preset='custom' and populates the `include` list with
        the resolved RCSB field paths.
        """
        paths = self.resolve(names)
        return FieldConfig(
            preset="custom",
            columns=names,
            include=paths,
        )
