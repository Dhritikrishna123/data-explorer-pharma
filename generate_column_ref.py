"""Generate COLUMN_REFERENCE.md from preset definitions."""

from pathlib import Path

import yaml

COLUMN_DESCRIPTIONS = {
    # ── Entry identiﬁers ──
    "entry.rcsb_id": ("string", "PDB entry identiﬁer (4-character code)"),
    "entry.rcsb_entry_container_identifiers.entry_id": ("string", "PDB entry identiﬁer (aliased)"),
    "entry.rcsb_entry_info.structure_determination_methodology": (
        "string",
        "Methodology used for structure determination",
    ),
    # ── Experimental method & resolution ──
    "entry.exptl.method": (
        "string",
        "Experimental technique (X-RAY DIFFRACTION, SOLUTION NMR, ELECTRON MICROSCOPY, etc.)",
    ),
    "entry.exptl.method_details": ("string", "Detailed experimental method description"),
    "entry.rcsb_entry_info.experimental_method": ("string", "Normalised experimental method classiﬁcation"),
    "entry.rcsb_entry_info.resolution_combined": ("float", "Structure resolution in ångströms (Å)"),
    "entry.refine.ls_d_res_high": ("float", "High-resolution limit from reﬁnement"),
    "entry.reflns.d_resolution_high": ("float", "High-resolution limit from reﬂection data"),
    # ── Structure composition ──
    "entry.rcsb_entry_info.deposited_polymer_entity_instance_count": (
        "int",
        "Number of polymer chains in deposited structure",
    ),
    "entry.rcsb_entry_info.deposited_nonpolymer_entity_instance_count": (
        "int",
        "Number of nonpolymer (ligand/solvent) instances",
    ),
    "entry.rcsb_entry_info.nonpolymer_entity_count": ("int", "Number of unique nonpolymer entities"),
    "entry.rcsb_entry_info.polymer_entity_count_protein": ("int", "Number of protein polymer entities"),
    "entry.rcsb_entry_info.deposited_atom_count": ("int", "Total number of deposited atoms"),
    "entry.rcsb_entry_info.molecular_weight": ("float", "Total molecular weight of deposited structure (Da)"),
    "entry.rcsb_entry_info.polymer_composition": ("string", "Polymer composition type (protein, RNA, DNA, etc.)"),
    "entry.rcsb_entry_info.assembly_count": ("int", "Number of assemblies in entry"),
    "entry.rcsb_entry_info.deposited_model_count": ("int", "Number of deposited models (NMR ensembles)"),
    "entry.rcsb_entry_info.disulfide_bond_count": ("int", "Number of disulﬁde bonds in structure"),
    # ── Structure features ──
    "entry.struct.title": ("string", "Structure title"),
    "entry.struct_keywords.text": ("string", "Structure keywords / classiﬁcation"),
    "entry.symmetry.space_group_name_H-M": ("string", "Space group (Hermann-Mauguin notation)"),
    "entry.cell.length_a": ("float", "Unit cell length a (Å)"),
    "entry.cell.length_b": ("float", "Unit cell length b (Å)"),
    "entry.cell.length_c": ("float", "Unit cell length c (Å)"),
    "entry.cell.angle_alpha": ("float", "Unit cell angle alpha (°)"),
    "entry.cell.angle_beta": ("float", "Unit cell angle beta (°)"),
    "entry.cell.angle_gamma": ("float", "Unit cell angle gamma (°)"),
    # ── Reﬁnement ──
    "entry.refine.ls_R_factor_R_work": ("float", "R-work crystallographic reﬁnement factor"),
    "entry.refine.ls_R_factor_R_free": ("float", "R-free crystallographic reﬁnement factor (cross-validation)"),
    "entry.refine.overall_SU_R_Cruickshank_DPI": ("float", "Cruickshank diﬀraction precision index (DPI)"),
    # ── Polymer entity data ──
    "entry.polymer_entities.rcsb_polymer_entity_container_identifiers.entity_id": (
        "string",
        "Polymer entity ID within entry",
    ),
    "entry.polymer_entities.rcsb_polymer_entity_container_identifiers.entry_id": (
        "string",
        "Entry ID for polymer entity",
    ),
    "entry.polymer_entities.rcsb_polymer_entity_container_identifiers.uniprot_ids": (
        "list[string]",
        "UniProt IDs associated with polymer entity",
    ),
    "entry.polymer_entities.entity_poly.pdbx_seq_one_letter_code": (
        "string",
        "Polymer entity sequence (one-letter code)",
    ),
    "entry.polymer_entities.entity_poly.pdbx_seq_one_letter_code_can": ("string", "Canonical polymer entity sequence"),
    "entry.polymer_entities.entity_poly.pdbx_target_identifier": ("string", "Target identiﬁer for the polymer entity"),
    "entry.polymer_entities.rcsb_entity_source_organism.organism_name": ("string", "Source organism scientiﬁc name"),
    "entry.polymer_entities.rcsb_entity_source_organism.taxonomy_lineage": (
        "list[string]",
        "Taxonomic lineage of source organism",
    ),
    "entry.polymer_entities.rcsb_entity_host_organism.organism_name": ("string", "Expression host organism name"),
    # ── Ligand / nonpolymer data ──
    "entry.nonpolymer_entities.rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id": (
        "string",
        "Nonpolymer component (ligand) identiﬁer (PDB CCD code)",
    ),
    "entry.nonpolymer_entities.rcsb_nonpolymer_entity_container_identifiers.entry_id": (
        "string",
        "Entry ID for nonpolymer entity",
    ),
    # ── Citations ──
    "entry.rcsb_primary_citation.title": ("string", "Primary citation title"),
    "entry.rcsb_primary_citation.journal_abbrev": ("string", "Journal abbreviation"),
    "entry.rcsb_primary_citation.pubmed_id": ("int", "PubMed identiﬁer"),
    "entry.rcsb_primary_citation.year": ("int", "Publication year"),
    # ── UniProt enhanced ──
    "uniprot.rcsb_uniprot_protein.sequence": ("string", "Full amino acid sequence"),
    "uniprot.rcsb_uniprot_protein.name": ("string", "Protein name (recommended name)"),
    "uniprot.rcsb_uniprot_protein.gene": ("list[dict]", "Gene name(s) — primary + synonyms"),
    "uniprot.rcsb_uniprot_protein.source_organism": ("dict", "Source organism (taxonomy ID + scientiﬁc name)"),
    "uniprot.rcsb_uniprot_protein.ec": ("list[string]", "Enzyme Commission (EC) numbers"),
    "uniprot.rcsb_uniprot_keyword.value": ("list[string]", "UniProt keyword values"),
    "uniprot.rcsb_uniprot_annotation.type": ("list[string]", "UniProt annotation type (GO, etc.)"),
    "uniprot.rcsb_uniprot_annotation.description": ("list[string]", "UniProt annotation description text"),
}


def path_to_column(path: str) -> str:
    parts = path.split(".")
    return "_".join(parts[1:]) if len(parts) > 1 else path


PRESETS_DIR = Path(__file__).parent / "rcsb_pipeline" / "presets"
OUT = Path(__file__).parent / "COLUMN_REFERENCE.md"

lines = [
    "# Column Reference — RCSB PDB Pipeline\n",
    "\n",
    "Maps every output column to its RCSB GraphQL source path, type, description,\n",
    "and which preset(s) include it.\n",
    "\n",
    "## Column naming convention\n",
    "\n",
    "Columns are derived from dot-paths by stripping the root type (`entry.` / `uniprot.`)\n",
    "and joining remaining segments with underscores:\n",
    "\n",
    "| Example Path | Output Column Name |\n",
    "|---|---|\n",
    "| `entry.exptl.method` | `exptl_method` |\n",
    "| `entry.rcsb_entry_info.resolution_combined` | `rcsb_entry_info_resolution_combined` |\n",
    "| `uniprot.rcsb_uniprot_protein.name` | `rcsb_uniprot_protein_name` |\n",
    "\n",
    "Three base columns are always added by the pipeline itself (not from any preset):\n",
    "\n",
    "| Column | Source | Type | Description |\n",
    "|---|---|---|---|\n",
    "| `uniprot_id` | CLI input | string | UniProt accession (primary key) |\n",
    "| `pdb_id` | `entry.rcsb_id` | string | PDB entry identiﬁer |\n",
    "| `structure_available` | derived | bool | True if a PDB structure exists for this (uniprot, pdb) pair |\n",
    "\n",
    "**Note:** `binding_site_count` is computed from `RcsbLigandNeighbors` data —\n",
    "it counts unique ligand components per chain. It is an approximation\ndocumented as such.\n",
    "\n",
]

# Collect which presets include which paths
preset_map: dict[str, set[str]] = {}
for preset_file in ["minimal.yaml", "standard.yaml", "full.yaml"]:
    with open(PRESETS_DIR / preset_file) as f:
        data = yaml.safe_load(f)
    preset_name = preset_file.replace(".yaml", "")
    for path in data.get("include", []):
        preset_map.setdefault(path, set()).add(preset_name)

# All paths sorted
all_paths = sorted(COLUMN_DESCRIPTIONS.keys())

lines.append("## All columns\n")
lines.append("| Column Name | Source Path | Type | Description | Presets |\n")
lines.append("|---|---|---|---|---|\n")

for path in all_paths:
    col = path_to_column(path)
    typ, desc = COLUMN_DESCRIPTIONS.get(path, ("", path))
    presets = ", ".join(sorted(preset_map.get(path, [])))
    if presets:
        presets = presets.replace("minimal", "min").replace("standard", "std").replace("full", "full")
    lines.append(f"| `{col}` | `{path}` | {typ} | {desc} | {presets} |\n")

lines.append("\n## Preset speciﬁc listings\n\n")

for preset_file in ["minimal.yaml", "standard.yaml"]:
    with open(PRESETS_DIR / preset_file) as f:
        data = yaml.safe_load(f)
    preset_name = preset_file.replace(".yaml", "").title()
    lines.append(f"### {preset_name} preset\n")
    lines.append("| # | Column Name | Type | Description |\n")
    lines.append("|---|-------------|------|-------------|\n")
    for i, path in enumerate(data.get("include", []), 1):
        col = path_to_column(path)
        typ, desc = COLUMN_DESCRIPTIONS.get(path, ("", path))
        lines.append(f"| {i} | `{col}` | {typ} | {desc} |\n")
    lines.append("\n")

with open(OUT, "w") as f:
    f.writelines(lines)

print(f"Written to {OUT}")
print(f"{len(all_paths)} columns documented")
