"""Configuration models for the RCSB PDB pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    cache_dir: str = "~/.cache/rcsb-pipeline"
    log_dir: str = "./logs"
    checkpoint: str = "./checkpoint.json"
    max_concurrent: int = 5
    rate_limit: float = 0.3
    batch_size: int = 50
    retry_max: int = 3
    retry_backoff: float = 2.0


class InputConfig(BaseModel):
    uniprots: List[str] = Field(default_factory=list)
    uniprot_file: Optional[str] = None
    pdb_ids: List[str] = Field(default_factory=list)
    gene_symbols: List[str] = Field(default_factory=list)
    gene_symbol_file: Optional[str] = None


class DiscoveryConfig(BaseModel):
    max_entries: int = 1000
    min_resolution: float = 0.0
    max_resolution: float = 10.0
    experimental_methods: List[str] = Field(default_factory=list)
    exclude_deprecated: bool = True


class FieldConfig(BaseModel):
    preset: str = "standard"
    include: List[str] = Field(default_factory=list)
    exclude: List[str] = Field(default_factory=list)
    custom_config: Optional[str] = None


class OutputConfig(BaseModel):
    directory: str = "./rcsb_output"
    formats: List[str] = Field(default_factory=lambda: ["csv", "parquet"])
    granularity: str = "per-structure"
    dedup_strategy: str = "strict"
    dedup_keys: List[str] = Field(default_factory=list)
    missing_action: str = "fill-null"
    aggregation_mode: str = "pick-best"
    aggregation_key: str = "resolution_combined"


class RcsbPipelineConfig(BaseModel):
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    input: InputConfig = Field(default_factory=InputConfig)
    discovery: DiscoveryConfig = Field(default_factory=DiscoveryConfig)
    fields: FieldConfig = Field(default_factory=FieldConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "RcsbPipelineConfig":
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "RcsbPipelineConfig":
        return cls(**data)

    def to_yaml(self, path: str) -> None:
        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)

    def resolve_paths(self) -> None:
        self.pipeline.cache_dir = str(Path(self.pipeline.cache_dir).expanduser())
        self.output.directory = str(Path(self.output.directory).expanduser())
        self.pipeline.log_dir = str(Path(self.output.directory) / "logs")
        self.pipeline.checkpoint = str(Path(self.output.directory) / "checkpoint.json")


PRESET_DIR = Path(__file__).parent / "presets"


def load_preset(name: str) -> FieldConfig:
    name = name.lower()
    if name == "custom":
        return FieldConfig(preset="custom")
    path = PRESET_DIR / f"{name}.yaml"
    if not path.exists():
        raise ValueError(f"Unknown preset: {name}. Available: minimal, standard, full, custom")
    with open(path) as f:
        data = yaml.safe_load(f)
    return FieldConfig(**data)
