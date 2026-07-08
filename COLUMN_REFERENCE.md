# Column Reference — RCSB PDB Pipeline

Maps every output column to its RCSB GraphQL source path, type, description,
and which preset(s) include it.

## Column naming convention

Columns are derived from dot-paths by stripping the root type (`entry.` / `uniprot.`)
and joining remaining segments with underscores:

| Example Path | Output Column Name |
|---|---|
| `entry.exptl.method` | `exptl_method` |
| `entry.rcsb_entry_info.resolution_combined` | `rcsb_entry_info_resolution_combined` |
| `uniprot.rcsb_uniprot_protein.name` | `rcsb_uniprot_protein_name` |

Three base columns are always added by the pipeline itself (not from any preset):

| Column | Source | Type | Description |
|---|---|---|---|
| `uniprot_id` | CLI input | string | UniProt accession (primary key) |
| `pdb_id` | `entry.rcsb_id` | string | PDB entry identiﬁer |
| `structure_available` | derived | bool | True if a PDB structure exists for this (uniprot, pdb) pair |

**Note:** `binding_site_count` is computed from `RcsbLigandNeighbors` data —
it counts unique ligand components per chain. It is an approximation
documented as such.

## All columns
| Column Name | Source Path | Type | Description | Presets |
|---|---|---|---|---|
| `cell_angle_alpha` | `entry.cell.angle_alpha` | float | Unit cell angle alpha (°) | std |
| `cell_angle_beta` | `entry.cell.angle_beta` | float | Unit cell angle beta (°) | std |
| `cell_angle_gamma` | `entry.cell.angle_gamma` | float | Unit cell angle gamma (°) | std |
| `cell_length_a` | `entry.cell.length_a` | float | Unit cell length a (Å) | std |
| `cell_length_b` | `entry.cell.length_b` | float | Unit cell length b (Å) | std |
| `cell_length_c` | `entry.cell.length_c` | float | Unit cell length c (Å) | std |
| `exptl_method` | `entry.exptl.method` | string | Experimental technique (X-RAY DIFFRACTION, SOLUTION NMR, ELECTRON MICROSCOPY, etc.) | min, std |
| `exptl_method_details` | `entry.exptl.method_details` | string | Detailed experimental method description | std |
| `nonpolymer_entities_rcsb_nonpolymer_entity_container_identifiers_entry_id` | `entry.nonpolymer_entities.rcsb_nonpolymer_entity_container_identifiers.entry_id` | string | Entry ID for nonpolymer entity | std |
| `nonpolymer_entities_rcsb_nonpolymer_entity_container_identifiers_nonpolymer_comp_id` | `entry.nonpolymer_entities.rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id` | string | Nonpolymer component (ligand) identiﬁer (PDB CCD code) | std |
| `polymer_entities_entity_poly_pdbx_seq_one_letter_code` | `entry.polymer_entities.entity_poly.pdbx_seq_one_letter_code` | string | Polymer entity sequence (one-letter code) | std |
| `polymer_entities_entity_poly_pdbx_seq_one_letter_code_can` | `entry.polymer_entities.entity_poly.pdbx_seq_one_letter_code_can` | string | Canonical polymer entity sequence | std |
| `polymer_entities_entity_poly_pdbx_target_identifier` | `entry.polymer_entities.entity_poly.pdbx_target_identifier` | string | Target identiﬁer for the polymer entity | std |
| `polymer_entities_rcsb_entity_host_organism_organism_name` | `entry.polymer_entities.rcsb_entity_host_organism.organism_name` | string | Expression host organism name | std |
| `polymer_entities_rcsb_entity_source_organism_organism_name` | `entry.polymer_entities.rcsb_entity_source_organism.organism_name` | string | Source organism scientiﬁc name | std |
| `polymer_entities_rcsb_entity_source_organism_taxonomy_lineage` | `entry.polymer_entities.rcsb_entity_source_organism.taxonomy_lineage` | list[string] | Taxonomic lineage of source organism | std |
| `polymer_entities_rcsb_polymer_entity_container_identifiers_entity_id` | `entry.polymer_entities.rcsb_polymer_entity_container_identifiers.entity_id` | string | Polymer entity ID within entry | std |
| `polymer_entities_rcsb_polymer_entity_container_identifiers_entry_id` | `entry.polymer_entities.rcsb_polymer_entity_container_identifiers.entry_id` | string | Entry ID for polymer entity | std |
| `polymer_entities_rcsb_polymer_entity_container_identifiers_uniprot_ids` | `entry.polymer_entities.rcsb_polymer_entity_container_identifiers.uniprot_ids` | list[string] | UniProt IDs associated with polymer entity | std |
| `rcsb_entry_container_identifiers_entry_id` | `entry.rcsb_entry_container_identifiers.entry_id` | string | PDB entry identiﬁer (aliased) | std |
| `rcsb_entry_info_assembly_count` | `entry.rcsb_entry_info.assembly_count` | int | Number of assemblies in entry | std |
| `rcsb_entry_info_deposited_atom_count` | `entry.rcsb_entry_info.deposited_atom_count` | int | Total number of deposited atoms | std |
| `rcsb_entry_info_deposited_model_count` | `entry.rcsb_entry_info.deposited_model_count` | int | Number of deposited models (NMR ensembles) | std |
| `rcsb_entry_info_deposited_nonpolymer_entity_instance_count` | `entry.rcsb_entry_info.deposited_nonpolymer_entity_instance_count` | int | Number of nonpolymer (ligand/solvent) instances | std |
| `rcsb_entry_info_deposited_polymer_entity_instance_count` | `entry.rcsb_entry_info.deposited_polymer_entity_instance_count` | int | Number of polymer chains in deposited structure | min, std |
| `rcsb_entry_info_disulfide_bond_count` | `entry.rcsb_entry_info.disulfide_bond_count` | int | Number of disulﬁde bonds in structure | std |
| `rcsb_entry_info_experimental_method` | `entry.rcsb_entry_info.experimental_method` | string | Normalised experimental method classiﬁcation | min, std |
| `rcsb_entry_info_molecular_weight` | `entry.rcsb_entry_info.molecular_weight` | float | Total molecular weight of deposited structure (Da) | std |
| `rcsb_entry_info_nonpolymer_entity_count` | `entry.rcsb_entry_info.nonpolymer_entity_count` | int | Number of unique nonpolymer entities | min, std |
| `rcsb_entry_info_polymer_composition` | `entry.rcsb_entry_info.polymer_composition` | string | Polymer composition type (protein, RNA, DNA, etc.) | std |
| `rcsb_entry_info_polymer_entity_count_protein` | `entry.rcsb_entry_info.polymer_entity_count_protein` | int | Number of protein polymer entities | std |
| `rcsb_entry_info_resolution_combined` | `entry.rcsb_entry_info.resolution_combined` | float | Structure resolution in ångströms (Å) | min, std |
| `rcsb_entry_info_structure_determination_methodology` | `entry.rcsb_entry_info.structure_determination_methodology` | string | Methodology used for structure determination | std |
| `rcsb_id` | `entry.rcsb_id` | string | PDB entry identiﬁer (4-character code) | min, std |
| `rcsb_primary_citation_journal_abbrev` | `entry.rcsb_primary_citation.journal_abbrev` | string | Journal abbreviation | std |
| `rcsb_primary_citation_pubmed_id` | `entry.rcsb_primary_citation.pubmed_id` | int | PubMed identiﬁer | std |
| `rcsb_primary_citation_title` | `entry.rcsb_primary_citation.title` | string | Primary citation title | std |
| `rcsb_primary_citation_year` | `entry.rcsb_primary_citation.year` | int | Publication year | std |
| `refine_ls_R_factor_R_free` | `entry.refine.ls_R_factor_R_free` | float | R-free crystallographic reﬁnement factor (cross-validation) | std |
| `refine_ls_R_factor_R_work` | `entry.refine.ls_R_factor_R_work` | float | R-work crystallographic reﬁnement factor | std |
| `refine_ls_d_res_high` | `entry.refine.ls_d_res_high` | float | High-resolution limit from reﬁnement | std |
| `refine_overall_SU_R_Cruickshank_DPI` | `entry.refine.overall_SU_R_Cruickshank_DPI` | float | Cruickshank diﬀraction precision index (DPI) | std |
| `reflns_d_resolution_high` | `entry.reflns.d_resolution_high` | float | High-resolution limit from reﬂection data | std |
| `struct_title` | `entry.struct.title` | string | Structure title | std |
| `struct_keywords_text` | `entry.struct_keywords.text` | string | Structure keywords / classiﬁcation | std |
| `symmetry_space_group_name_H-M` | `entry.symmetry.space_group_name_H-M` | string | Space group (Hermann-Mauguin notation) | std |
| `rcsb_uniprot_annotation_description` | `uniprot.rcsb_uniprot_annotation.description` | list[string] | UniProt annotation description text | std |
| `rcsb_uniprot_annotation_type` | `uniprot.rcsb_uniprot_annotation.type` | list[string] | UniProt annotation type (GO, etc.) | std |
| `rcsb_uniprot_keyword_value` | `uniprot.rcsb_uniprot_keyword.value` | list[string] | UniProt keyword values | std |
| `rcsb_uniprot_protein_ec` | `uniprot.rcsb_uniprot_protein.ec` | list[string] | Enzyme Commission (EC) numbers | std |
| `rcsb_uniprot_protein_gene` | `uniprot.rcsb_uniprot_protein.gene` | list[dict] | Gene name(s) — primary + synonyms | min, std |
| `rcsb_uniprot_protein_name` | `uniprot.rcsb_uniprot_protein.name` | string | Protein name (recommended name) | min, std |
| `rcsb_uniprot_protein_sequence` | `uniprot.rcsb_uniprot_protein.sequence` | string | Full amino acid sequence | min, std |
| `rcsb_uniprot_protein_source_organism` | `uniprot.rcsb_uniprot_protein.source_organism` | dict | Source organism (taxonomy ID + scientiﬁc name) | min, std |

## Preset speciﬁc listings

### Minimal preset
| # | Column Name | Type | Description |
|---|-------------|------|-------------|
| 1 | `rcsb_id` | string | PDB entry identiﬁer (4-character code) |
| 2 | `exptl_method` | string | Experimental technique (X-RAY DIFFRACTION, SOLUTION NMR, ELECTRON MICROSCOPY, etc.) |
| 3 | `rcsb_entry_info_experimental_method` | string | Normalised experimental method classiﬁcation |
| 4 | `rcsb_entry_info_resolution_combined` | float | Structure resolution in ångströms (Å) |
| 5 | `rcsb_entry_info_deposited_polymer_entity_instance_count` | int | Number of polymer chains in deposited structure |
| 6 | `rcsb_entry_info_nonpolymer_entity_count` | int | Number of unique nonpolymer entities |
| 7 | `rcsb_uniprot_protein_sequence` | string | Full amino acid sequence |
| 8 | `rcsb_uniprot_protein_name` | string | Protein name (recommended name) |
| 9 | `rcsb_uniprot_protein_gene` | list[dict] | Gene name(s) — primary + synonyms |
| 10 | `rcsb_uniprot_protein_source_organism` | dict | Source organism (taxonomy ID + scientiﬁc name) |

### Standard preset
| # | Column Name | Type | Description |
|---|-------------|------|-------------|
| 1 | `rcsb_id` | string | PDB entry identiﬁer (4-character code) |
| 2 | `rcsb_entry_container_identifiers_entry_id` | string | PDB entry identiﬁer (aliased) |
| 3 | `rcsb_entry_info_structure_determination_methodology` | string | Methodology used for structure determination |
| 4 | `exptl_method` | string | Experimental technique (X-RAY DIFFRACTION, SOLUTION NMR, ELECTRON MICROSCOPY, etc.) |
| 5 | `exptl_method_details` | string | Detailed experimental method description |
| 6 | `rcsb_entry_info_experimental_method` | string | Normalised experimental method classiﬁcation |
| 7 | `rcsb_entry_info_resolution_combined` | float | Structure resolution in ångströms (Å) |
| 8 | `refine_ls_d_res_high` | float | High-resolution limit from reﬁnement |
| 9 | `reflns_d_resolution_high` | float | High-resolution limit from reﬂection data |
| 10 | `rcsb_entry_info_deposited_polymer_entity_instance_count` | int | Number of polymer chains in deposited structure |
| 11 | `rcsb_entry_info_deposited_nonpolymer_entity_instance_count` | int | Number of nonpolymer (ligand/solvent) instances |
| 12 | `rcsb_entry_info_nonpolymer_entity_count` | int | Number of unique nonpolymer entities |
| 13 | `rcsb_entry_info_polymer_entity_count_protein` | int | Number of protein polymer entities |
| 14 | `rcsb_entry_info_deposited_atom_count` | int | Total number of deposited atoms |
| 15 | `rcsb_entry_info_molecular_weight` | float | Total molecular weight of deposited structure (Da) |
| 16 | `rcsb_entry_info_polymer_composition` | string | Polymer composition type (protein, RNA, DNA, etc.) |
| 17 | `rcsb_entry_info_assembly_count` | int | Number of assemblies in entry |
| 18 | `rcsb_entry_info_deposited_model_count` | int | Number of deposited models (NMR ensembles) |
| 19 | `rcsb_entry_info_disulfide_bond_count` | int | Number of disulﬁde bonds in structure |
| 20 | `struct_title` | string | Structure title |
| 21 | `struct_keywords_text` | string | Structure keywords / classiﬁcation |
| 22 | `symmetry_space_group_name_H-M` | string | Space group (Hermann-Mauguin notation) |
| 23 | `cell_length_a` | float | Unit cell length a (Å) |
| 24 | `cell_length_b` | float | Unit cell length b (Å) |
| 25 | `cell_length_c` | float | Unit cell length c (Å) |
| 26 | `cell_angle_alpha` | float | Unit cell angle alpha (°) |
| 27 | `cell_angle_beta` | float | Unit cell angle beta (°) |
| 28 | `cell_angle_gamma` | float | Unit cell angle gamma (°) |
| 29 | `refine_ls_R_factor_R_work` | float | R-work crystallographic reﬁnement factor |
| 30 | `refine_ls_R_factor_R_free` | float | R-free crystallographic reﬁnement factor (cross-validation) |
| 31 | `refine_overall_SU_R_Cruickshank_DPI` | float | Cruickshank diﬀraction precision index (DPI) |
| 32 | `polymer_entities_rcsb_polymer_entity_container_identifiers_entity_id` | string | Polymer entity ID within entry |
| 33 | `polymer_entities_rcsb_polymer_entity_container_identifiers_entry_id` | string | Entry ID for polymer entity |
| 34 | `polymer_entities_rcsb_polymer_entity_container_identifiers_uniprot_ids` | list[string] | UniProt IDs associated with polymer entity |
| 35 | `polymer_entities_entity_poly_pdbx_seq_one_letter_code` | string | Polymer entity sequence (one-letter code) |
| 36 | `polymer_entities_entity_poly_pdbx_seq_one_letter_code_can` | string | Canonical polymer entity sequence |
| 37 | `polymer_entities_entity_poly_pdbx_target_identifier` | string | Target identiﬁer for the polymer entity |
| 38 | `polymer_entities_rcsb_entity_source_organism_organism_name` | string | Source organism scientiﬁc name |
| 39 | `polymer_entities_rcsb_entity_source_organism_taxonomy_lineage` | list[string] | Taxonomic lineage of source organism |
| 40 | `polymer_entities_rcsb_entity_host_organism_organism_name` | string | Expression host organism name |
| 41 | `nonpolymer_entities_rcsb_nonpolymer_entity_container_identifiers_nonpolymer_comp_id` | string | Nonpolymer component (ligand) identiﬁer (PDB CCD code) |
| 42 | `nonpolymer_entities_rcsb_nonpolymer_entity_container_identifiers_entry_id` | string | Entry ID for nonpolymer entity |
| 43 | `rcsb_primary_citation_title` | string | Primary citation title |
| 44 | `rcsb_primary_citation_journal_abbrev` | string | Journal abbreviation |
| 45 | `rcsb_primary_citation_pubmed_id` | int | PubMed identiﬁer |
| 46 | `rcsb_primary_citation_year` | int | Publication year |
| 47 | `rcsb_uniprot_protein_sequence` | string | Full amino acid sequence |
| 48 | `rcsb_uniprot_protein_name` | string | Protein name (recommended name) |
| 49 | `rcsb_uniprot_protein_gene` | list[dict] | Gene name(s) — primary + synonyms |
| 50 | `rcsb_uniprot_protein_source_organism` | dict | Source organism (taxonomy ID + scientiﬁc name) |
| 51 | `rcsb_uniprot_protein_ec` | list[string] | Enzyme Commission (EC) numbers |
| 52 | `rcsb_uniprot_keyword_value` | list[string] | UniProt keyword values |
| 53 | `rcsb_uniprot_annotation_type` | list[string] | UniProt annotation type (GO, etc.) |
| 54 | `rcsb_uniprot_annotation_description` | list[string] | UniProt annotation description text |

