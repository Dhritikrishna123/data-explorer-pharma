# RCSB Field Catalogue (Type Hierarchy)
_Generated on 2026-07-08 01:59:38_
This shows each GraphQL object type and its direct fields.
Object reference fields show the nested type name in brackets.

## AuditAuthor
```text
  ├── identifier_ORCID : String?  # The Open Researcher and Contributor ID (ORCID).  Examples: 0000-0002-6681-547X
  ├── name : String?  # The name of an author of this data block. If there are multiple  authors, _audit_author.name is looped with _audit_autho
  ├── pdbx_ordinal : Int  # This data item defines the order of the author's name in the  list of audit authors.
```

## Cell
```text
  ├── Z_PDB : Int?  # The number of the polymeric chains in a unit cell. In the case  of heteropolymers, Z is the number of occurrences of the
  ├── angle_alpha : Float?  # Unit-cell angle alpha of the reported structure in degrees.
  ├── angle_beta : Float?  # Unit-cell angle beta of the reported structure in degrees.
  ├── angle_gamma : Float?  # Unit-cell angle gamma of the reported structure in degrees.
  ├── formula_units_Z : Int?  # The number of the formula units in the unit cell as specified  by _chemical_formula.structural, _chemical_formula.moiety
  ├── length_a : Float?  # Unit-cell length a corresponding to the structure reported in angstroms.
  ├── length_b : Float?  # Unit-cell length b corresponding to the structure reported in  angstroms.
  ├── length_c : Float?  # Unit-cell length c corresponding to the structure reported in angstroms.
  ├── pdbx_unique_axis : String?  # To further identify unique axis if necessary.  E.g., P 21 with  an unique C axis will have 'C' in this field.
  ├── volume : Float?  # Cell volume V in angstroms cubed.   V = a b c (1 - cos^2^~alpha~ - cos^2^~beta~ - cos^2^~gamma~             + 2 cos~alph
```

## ChemComp
```text
  ├── formula : String?  # The formula for the chemical component. Formulae are written  according to the following rules:   (1) Only recognized el
  ├── formula_weight : Float?  # Formula mass of the chemical component.  Examples: null, null
  ├── id : String  # The value of _chem_comp.id must uniquely identify each item in  the CHEM_COMP list.   For protein polymer entities, this
  ├── mon_nstd_parent_comp_id : String[]?  # The identifier for the parent component of the nonstandard  component. May be be a comma separated list if this componen
  ├── name : String?  # The full name of the component.  Examples: alanine, valine, adenine, cytosine
  ├── one_letter_code : String?  # For standard polymer components, the one-letter code for  the component.   For non-standard polymer components, the  one
  ├── pdbx_ambiguous_flag : String?  # A preliminary classification used by PDB to indicate  that the chemistry of this component while described  as clearly a
  ├── pdbx_formal_charge : Int?  # The net integer charge assigned to this component. This is the  formal charge assignment normally found in chemical diag
  ├── pdbx_initial_date : Date?  # Date component was added to database.
  ├── pdbx_modified_date : Date?  # Date component was last modified.
  ├── pdbx_processing_site : String?  # This data item identifies the deposition site that processed  this chemical component defintion.  Allowable values: EBI,
  ├── pdbx_release_status : String?  # This data item holds the current release status for the component.  Allowable values: DEL, HOLD, HPUB, OBS, REF_ONLY, RE
  ├── pdbx_replaced_by : String?  # Identifies the _chem_comp.id of the component that  has replaced this component.  Examples: q11, tvx
  ├── pdbx_replaces : String?  # Identifies the _chem_comp.id's of the components  which have been replaced by this component.  Multiple id codes should 
  ├── pdbx_subcomponent_list : String?  # The list of subcomponents contained in this component.  Examples: TSM DPH HIS CHF EMR
  ├── three_letter_code : String?  # For standard polymer components, the common three-letter code for  the component.   Non-standard polymer components and 
  ├── type : String?  # For standard polymer components, the type of the monomer.  Note that monomers that will form polymers are of three types
```

## Citation
```text
  ├── book_id_ISBN : String?  # The International Standard Book Number (ISBN) code assigned to  the book cited; relevant for books or book chapters.
  ├── book_publisher : String?  # The name of the publisher of the citation; relevant  for books or book chapters.  Examples: John Wiley and Sons
  ├── book_publisher_city : String?  # The location of the publisher of the citation; relevant  for books or book chapters.  Examples: London
  ├── book_title : String?  # The title of the book in which the citation appeared; relevant  for books or book chapters.
  ├── coordinate_linkage : String?  # _citation.coordinate_linkage states whether this citation  is concerned with precisely the set of coordinates given in t
  ├── country : String?  # The country/region of publication; relevant for books  and book chapters.
  ├── id : String  # The value of _citation.id must uniquely identify a record in the  CITATION list.   The _citation.id 'primary' should be 
  ├── journal_abbrev : String?  # Abbreviated name of the cited journal as given in the  Chemical Abstracts Service Source Index.  Examples: J.Mol.Biol., 
  ├── journal_full : String?  # Full name of the cited journal; relevant for journal articles.  Examples: Journal of Molecular Biology
  ├── journal_id_ASTM : String?  # The American Society for Testing and Materials (ASTM) code  assigned to the journal cited (also referred to as the CODEN
  ├── journal_id_CSD : String?  # The Cambridge Structural Database (CSD) code assigned to the  journal cited; relevant for journal articles. This is also
  ├── journal_id_ISSN : String?  # The International Standard Serial Number (ISSN) code assigned to  the journal cited; relevant for journal articles.
  ├── journal_issue : String?  # Issue number of the journal cited; relevant for journal  articles.  Examples: 2
  ├── journal_volume : String?  # Volume number of the journal cited; relevant for journal  articles.  Examples: 174
  ├── language : String?  # Language in which the cited article is written.  Examples: German
  ├── page_first : String?  # The first page of the citation; relevant for journal  articles, books and book chapters.
  ├── page_last : String?  # The last page of the citation; relevant for journal  articles, books and book chapters.
  ├── pdbx_database_id_DOI : String?  # Document Object Identifier used by doi.org to uniquely  specify bibliographic entry.  Examples: 10.2345/S138410769700022
  ├── pdbx_database_id_PubMed : Int?  # Ascession number used by PubMed to categorize a specific  bibliographic entry.
  ├── rcsb_authors : String[]?  # Names of the authors of the citation; relevant for journal  articles, books and book chapters.  Names are separated by v
  ├── rcsb_is_primary : String?  # Flag to indicate a primary citation.  Allowable values: N, Y
  ├── rcsb_journal_abbrev : String?  # Normalized journal abbreviation.  Examples: Nat Struct Mol Biol
  ├── title : String?  # The title of the citation; relevant for journal articles, books  and book chapters.  Examples: Structure of diferric duc
  ├── unpublished_flag : String?  # Flag to indicate that this citation will not be published.  Allowable values: N, Y
  ├── year : Int?  # The year of the citation; relevant for journal articles, books  and book chapters.
```

## ClustersMembers
```text
  ├── asym_id : String  # Internal chain ID used in mmCIF files to uniquely identify structural elements in the asymmetric unit.
  ├── pdbx_struct_oper_list_ids : String[]?  # Optional list of operator ids (pdbx_struct_oper_list.id) as appears in pdbx_struct_assembly_gen.oper_expression.
```

## CoreAssembly  (from root query: assembly, assemblies)
```text
  ├── branched_entity_instances : CoreBranchedEntityInstance[]?  # Get a list of branched entity instances (sugars) that constitute this assembly.
  ├── entry : CoreEntry?  # Get entry that includes this assembly.
  ├── interfaces : CoreInterface[]?  # Get all pairwise polymer interfaces for this assembly.
  ├── nonpolymer_entity_instances : CoreNonpolymerEntityInstance[]?  # Get a list of non-polymer entity instances (ligands) that constitute this assembly.
  ├── pdbx_struct_assembly : PdbxStructAssembly?
  ├── pdbx_struct_assembly_auth_evidence : PdbxStructAssemblyAuthEvidence[]?
  ├── pdbx_struct_assembly_gen : PdbxStructAssemblyGen[]?
  ├── pdbx_struct_assembly_prop : PdbxStructAssemblyProp[]?
  ├── pdbx_struct_oper_list : PdbxStructOperList[]?
  ├── polymer_entity_instances : CorePolymerEntityInstance[]?  # Get a list of polymer entity instances (chains) that constitute this assembly.
  ├── rcsb_assembly_annotation : RcsbAssemblyAnnotation[]?
  ├── rcsb_assembly_container_identifiers : RcsbAssemblyContainerIdentifiers
  ├── rcsb_assembly_feature : RcsbAssemblyFeature[]?
  ├── rcsb_assembly_info : RcsbAssemblyInfo?
  ├── rcsb_id : String  # A unique identifier for each object in this assembly container formed by  a dash separated concatenation of entry and as
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_struct_symmetry : RcsbStructSymmetry[]?
  ├── rcsb_struct_symmetry_lineage : RcsbStructSymmetryLineage[]?
  ├── rcsb_struct_symmetry_provenance_code : String?  # The title and version of software package used for symmetry calculations.
```

## CoreBranchedEntity  (from root query: branched_entity, branched_entities)
```text
  ├── branched_entity_instances : CoreBranchedEntityInstance[]?  # Get all unique branched instances (chains) for this molecular entity.
  ├── chem_comp_monomers : CoreChemComp[]?  # Get all unique monomers described in this branched entity.
  ├── entry : CoreEntry?  # Get entry that contains this branched entity.
  ├── pdbx_entity_branch : PdbxEntityBranch?
  ├── pdbx_entity_branch_descriptor : PdbxEntityBranchDescriptor[]?
  ├── prd : CoreChemComp?  # Get a BIRD chemical components described in this branched entity.
  ├── rcsb_branched_entity : RcsbBranchedEntity?
  ├── rcsb_branched_entity_annotation : RcsbBranchedEntityAnnotation[]?
  ├── rcsb_branched_entity_container_identifiers : RcsbBranchedEntityContainerIdentifiers
  ├── rcsb_branched_entity_feature : RcsbBranchedEntityFeature[]?
  ├── rcsb_branched_entity_feature_summary : RcsbBranchedEntityFeatureSummary[]?
  ├── rcsb_branched_entity_keywords : RcsbBranchedEntityKeywords?
  ├── rcsb_branched_entity_name_com : RcsbBranchedEntityNameCom?
  ├── rcsb_branched_entity_name_sys : RcsbBranchedEntityNameSys[]?
  ├── rcsb_id : String  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── rcsb_latest_revision : RcsbLatestRevision?
```

## CoreBranchedEntityInstance  (from root query: branched_entity_instances, branched_entity_instance)
```text
  ├── branched_entity : CoreBranchedEntity?  # Get branched entity for this branched entity instance.
  ├── pdbx_struct_special_symmetry : PdbxStructSpecialSymmetry[]?
  ├── rcsb_branched_entity_instance_container_identifiers : RcsbBranchedEntityInstanceContainerIdentifiers?
  ├── rcsb_branched_instance_annotation : RcsbBranchedInstanceAnnotation[]?
  ├── rcsb_branched_instance_feature : RcsbBranchedInstanceFeature[]?
  ├── rcsb_branched_instance_feature_summary : RcsbBranchedInstanceFeatureSummary[]?
  ├── rcsb_branched_struct_conn : RcsbBranchedStructConn[]?
  ├── rcsb_id : String  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_ligand_neighbors : RcsbLigandNeighbors[]?
  ├── struct_asym : StructAsym?
```

## CoreChemComp  (from root query: chem_comps, chem_comp)
```text
  ├── chem_comp : ChemComp?
  ├── drugbank : CoreDrugbank?  # Get DrubBank entry associated with this chemical component.
  ├── pdbx_chem_comp_audit : PdbxChemCompAudit[]?
  ├── pdbx_chem_comp_descriptor : PdbxChemCompDescriptor[]?
  ├── pdbx_chem_comp_feature : PdbxChemCompFeature[]?
  ├── pdbx_chem_comp_identifier : PdbxChemCompIdentifier[]?
  ├── pdbx_family_prd_audit : PdbxFamilyPrdAudit[]?
  ├── pdbx_prd_audit : PdbxPrdAudit[]?
  ├── pdbx_reference_entity_list : PdbxReferenceEntityList[]?
  ├── pdbx_reference_entity_poly : PdbxReferenceEntityPoly[]?
  ├── pdbx_reference_entity_poly_link : PdbxReferenceEntityPolyLink[]?
  ├── pdbx_reference_entity_poly_seq : PdbxReferenceEntityPolySeq[]?
  ├── pdbx_reference_entity_sequence : PdbxReferenceEntitySequence[]?
  ├── pdbx_reference_entity_src_nat : PdbxReferenceEntitySrcNat[]?
  ├── pdbx_reference_molecule : PdbxReferenceMolecule?
  ├── pdbx_reference_molecule_annotation : PdbxReferenceMoleculeAnnotation[]?
  ├── pdbx_reference_molecule_details : PdbxReferenceMoleculeDetails[]?
  ├── pdbx_reference_molecule_family : PdbxReferenceMoleculeFamily?
  ├── pdbx_reference_molecule_features : PdbxReferenceMoleculeFeatures[]?
  ├── pdbx_reference_molecule_list : PdbxReferenceMoleculeList[]?
  ├── pdbx_reference_molecule_related_structures : PdbxReferenceMoleculeRelatedStructures[]?
  ├── pdbx_reference_molecule_synonyms : PdbxReferenceMoleculeSynonyms[]?
  ├── rcsb_bird_citation : RcsbBirdCitation[]?
  ├── rcsb_chem_comp_annotation : RcsbChemCompAnnotation[]?
  ├── rcsb_chem_comp_container_identifiers : RcsbChemCompContainerIdentifiers?
  ├── rcsb_chem_comp_descriptor : RcsbChemCompDescriptor?
  ├── rcsb_chem_comp_info : RcsbChemCompInfo?
  ├── rcsb_chem_comp_related : RcsbChemCompRelated[]?
  ├── rcsb_chem_comp_synonyms : RcsbChemCompSynonyms[]?
  ├── rcsb_chem_comp_target : RcsbChemCompTarget[]?
  ├── rcsb_id : String  # A unique identifier for the chemical definition in this container.  Examples: ATP, PRD_000010
  ├── rcsb_schema_container_identifiers : RcsbSchemaContainerIdentifiers[]?
```

## CoreDrugbank
```text
  ├── drugbank_container_identifiers : DrugbankContainerIdentifiers?
  ├── drugbank_info : DrugbankInfo?
  ├── drugbank_target : DrugbankTarget[]?
```

## CoreEntityAlignmentsAlignedRegions
```text
  ├── length : Int  # Aligned region length
  ├── query_begin : Int  # Entity seqeunce start position
  ├── target_begin : Int  # NCBI sequence start position
```

## CoreEntityAlignmentsCoreEntityIdentifiers
```text
  ├── entity_id : String
  ├── entry_id : String
```

## CoreEntityAlignmentsScores
```text
  ├── query_coverage : Int
  ├── query_length : Int
  ├── target_coverage : Int
  ├── target_length : Int
```

## CoreEntry  (from root query: entry, entries)
```text
  ├── assemblies : CoreAssembly[]?  # Get all assemblies for this entry.
  ├── audit_author : AuditAuthor[]?
  ├── branched_entities : CoreBranchedEntity[]?  # Get all branched entities for this entry.
  ├── cell : Cell?
  ├── citation : Citation[]?
  ├── database_2 : Database2[]?
  ├── diffrn : Diffrn[]?
  ├── diffrn_detector : DiffrnDetector[]?
  ├── diffrn_radiation : DiffrnRadiation[]?
  ├── diffrn_source : DiffrnSource[]?
  ├── em_2d_crystal_entity : Em2dCrystalEntity[]?
  ├── em_3d_crystal_entity : Em3dCrystalEntity[]?
  ├── em_3d_fitting : Em3dFitting[]?
  ├── em_3d_fitting_list : Em3dFittingList[]?
  ├── em_3d_reconstruction : Em3dReconstruction[]?
  ├── em_ctf_correction : EmCtfCorrection[]?
  ├── em_diffraction : EmDiffraction[]?
  ├── em_diffraction_shell : EmDiffractionShell[]?
  ├── em_diffraction_stats : EmDiffractionStats[]?
  ├── em_embedding : EmEmbedding[]?
  ├── em_entity_assembly : EmEntityAssembly[]?
  ├── em_experiment : EmExperiment?
  ├── em_helical_entity : EmHelicalEntity[]?
  ├── em_image_recording : EmImageRecording[]?
  ├── em_imaging : EmImaging[]?
  ├── em_particle_selection : EmParticleSelection[]?
  ├── em_single_particle_entity : EmSingleParticleEntity[]?
  ├── em_software : EmSoftware[]?
  ├── em_specimen : EmSpecimen[]?
  ├── em_staining : EmStaining[]?
  ├── em_vitrification : EmVitrification[]?
  ├── entry : Entry?
  ├── entry_groups : GroupEntry[]?  # Get all groups for this entry.
  ├── exptl : Exptl[]?
  ├── exptl_crystal : ExptlCrystal[]?
  ├── exptl_crystal_grow : ExptlCrystalGrow[]?
  ├── ihm_entry_collection_mapping : IhmEntryCollectionMapping[]?
  ├── ihm_external_reference_info : IhmExternalReferenceInfo[]?
  ├── ma_data : MaData[]?
  ├── nonpolymer_entities : CoreNonpolymerEntity[]?  # Get all non-polymer (non-solvent) entities for this entry.
  ├── pdbx_SG_project : PdbxSGProject[]?
  ├── pdbx_audit_revision_category : PdbxAuditRevisionCategory[]?
  ├── pdbx_audit_revision_details : PdbxAuditRevisionDetails[]?
  ├── pdbx_audit_revision_group : PdbxAuditRevisionGroup[]?
  ├── pdbx_audit_revision_history : PdbxAuditRevisionHistory[]?
  ├── pdbx_audit_revision_item : PdbxAuditRevisionItem[]?
  ├── pdbx_audit_support : PdbxAuditSupport[]?
  ├── pdbx_database_PDB_obs_spr : PdbxDatabasePDBObsSpr[]?
  ├── pdbx_database_related : PdbxDatabaseRelated[]?
  ├── pdbx_database_status : PdbxDatabaseStatus?
  ├── pdbx_deposit_group : PdbxDepositGroup[]?
  ├── pdbx_initial_refinement_model : PdbxInitialRefinementModel[]?
  ├── pdbx_molecule_features : PdbxMoleculeFeatures[]?
  ├── pdbx_nmr_details : PdbxNmrDetails?
  ├── pdbx_nmr_ensemble : PdbxNmrEnsemble?
  ├── pdbx_nmr_exptl : PdbxNmrExptl[]?
  ├── pdbx_nmr_exptl_sample_conditions : PdbxNmrExptlSampleConditions[]?
  ├── pdbx_nmr_refine : PdbxNmrRefine[]?
  ├── pdbx_nmr_representative : PdbxNmrRepresentative?
  ├── pdbx_nmr_sample_details : PdbxNmrSampleDetails[]?
  ├── pdbx_nmr_software : PdbxNmrSoftware[]?
  ├── pdbx_nmr_spectrometer : PdbxNmrSpectrometer[]?
  ├── pdbx_reflns_twin : PdbxReflnsTwin[]?
  ├── pdbx_related_exp_data_set : PdbxRelatedExpDataSet[]?
  ├── pdbx_serial_crystallography_data_reduction : PdbxSerialCrystallographyDataReduction[]?
  ├── pdbx_serial_crystallography_measurement : PdbxSerialCrystallographyMeasurement[]?
  ├── pdbx_serial_crystallography_sample_delivery : PdbxSerialCrystallographySampleDelivery[]?
  ├── pdbx_serial_crystallography_sample_delivery_fixed_target : PdbxSerialCrystallographySampleDeliveryFixedTarget[]?
  ├── pdbx_serial_crystallography_sample_delivery_injection : PdbxSerialCrystallographySampleDeliveryInjection[]?
  ├── pdbx_soln_scatter : PdbxSolnScatter[]?
  ├── pdbx_soln_scatter_model : PdbxSolnScatterModel[]?
  ├── pdbx_vrpt_summary : PdbxVrptSummary?
  ├── pdbx_vrpt_summary_diffraction : PdbxVrptSummaryDiffraction[]?
  ├── pdbx_vrpt_summary_em : PdbxVrptSummaryEm[]?
  ├── pdbx_vrpt_summary_geometry : PdbxVrptSummaryGeometry[]?
  ├── pdbx_vrpt_summary_nmr : PdbxVrptSummaryNmr[]?
  ├── polymer_entities : CorePolymerEntity[]?  # Get all polymer entities for this entry.
  ├── pubmed : CorePubmed?  # Get literature information from PubMed database.
  ├── rcsb_accession_info : RcsbAccessionInfo?
  ├── rcsb_associated_holdings : CurrentEntry?  # The list of content types associated with this entry.
  ├── rcsb_binding_affinity : RcsbBindingAffinity[]?
  ├── rcsb_comp_model_provenance : RcsbCompModelProvenance?
  ├── rcsb_entry_container_identifiers : RcsbEntryContainerIdentifiers
  ├── rcsb_entry_group_membership : RcsbEntryGroupMembership[]?
  ├── rcsb_entry_info : RcsbEntryInfo
  ├── rcsb_external_references : RcsbExternalReferences[]?
  ├── rcsb_id : String  # A unique identifier for each object in this entry container.  Examples: 1KIP
  ├── rcsb_ihm_dataset_list : RcsbIhmDatasetList[]?
  ├── rcsb_ihm_dataset_source_db_reference : RcsbIhmDatasetSourceDbReference[]?
  ├── rcsb_ma_qa_metric_global : RcsbMaQaMetricGlobal[]?
  ├── rcsb_primary_citation : RcsbPrimaryCitation?
  ├── refine : Refine[]?
  ├── refine_analyze : RefineAnalyze[]?
  ├── refine_hist : RefineHist[]?
  ├── refine_ls_restr : RefineLsRestr[]?
  ├── reflns : Reflns[]?
  ├── reflns_shell : ReflnsShell[]?
  ├── software : Software[]?
  ├── struct : Struct?
  ├── struct_keywords : StructKeywords?
  ├── symmetry : Symmetry?
```

## CoreInterface  (from root query: interface, interfaces)
```text
  ├── rcsb_id : String
  ├── rcsb_interface_container_identifiers : RcsbInterfaceContainerIdentifiers
  ├── rcsb_interface_info : RcsbInterfaceInfo?
  ├── rcsb_interface_operator : String[]  # List of operations for each interface partner.
  ├── rcsb_interface_partner : RcsbInterfacePartner[]
  ├── rcsb_latest_revision : RcsbLatestRevision?
```

## CoreNonpolymerEntity  (from root query: nonpolymer_entities, nonpolymer_entity)
```text
  ├── entry : CoreEntry?  # Get entry that contains this non-polymer entity.
  ├── nonpolymer_comp : CoreChemComp?  # Get a non-polymer chemical components described in this molecular entity.
  ├── nonpolymer_entity_instances : CoreNonpolymerEntityInstance[]?  # Get all unique non-polymer instances (chains) for this non-polymer entity.
  ├── pdbx_entity_nonpoly : PdbxEntityNonpoly?
  ├── prd : CoreChemComp?  # Get a BIRD chemical components described in this molecular entity.
  ├── rcsb_id : String  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_nonpolymer_entity : RcsbNonpolymerEntity?
  ├── rcsb_nonpolymer_entity_annotation : RcsbNonpolymerEntityAnnotation[]?
  ├── rcsb_nonpolymer_entity_container_identifiers : RcsbNonpolymerEntityContainerIdentifiers
  ├── rcsb_nonpolymer_entity_feature : RcsbNonpolymerEntityFeature[]?
  ├── rcsb_nonpolymer_entity_feature_summary : RcsbNonpolymerEntityFeatureSummary[]?
  ├── rcsb_nonpolymer_entity_keywords : RcsbNonpolymerEntityKeywords?
  ├── rcsb_nonpolymer_entity_name_com : RcsbNonpolymerEntityNameCom[]?
```

## CoreNonpolymerEntityInstance  (from root query: nonpolymer_entity_instance, nonpolymer_entity_instances)
```text
  ├── nonpolymer_entity : CoreNonpolymerEntity?  # Get non-polymer entity for this non-polymer entity instance.
  ├── pdbx_struct_special_symmetry : PdbxStructSpecialSymmetry[]?
  ├── pdbx_vrpt_summary_entity_fit_to_map : PdbxVrptSummaryEntityFitToMap[]?
  ├── pdbx_vrpt_summary_entity_geometry : PdbxVrptSummaryEntityGeometry[]?
  ├── rcsb_id : String  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_nonpolymer_entity_instance_container_identifiers : RcsbNonpolymerEntityInstanceContainerIdentifiers?
  ├── rcsb_nonpolymer_instance_annotation : RcsbNonpolymerInstanceAnnotation[]?
  ├── rcsb_nonpolymer_instance_feature : RcsbNonpolymerInstanceFeature[]?
  ├── rcsb_nonpolymer_instance_feature_summary : RcsbNonpolymerInstanceFeatureSummary[]?
  ├── rcsb_nonpolymer_instance_validation_score : RcsbNonpolymerInstanceValidationScore[]?
  ├── rcsb_nonpolymer_struct_conn : RcsbNonpolymerStructConn[]?
  ├── rcsb_target_neighbors : RcsbTargetNeighbors[]?
  ├── struct_asym : StructAsym?
```

## CorePfam
```text
  ├── rcsb_id : String  # Accession number of Pfam entry.
  ├── rcsb_pfam_accession : String  # The unique accession code of protein families and domains in the Pfam database.  Examples: PF00621, PF00637, PF00656
  ├── rcsb_pfam_clan_id : String?  # Details of the Pfam clan to which the entity belongs.
  ├── rcsb_pfam_comment : String?  # Textual description of the family.
  ├── rcsb_pfam_container_identifiers : RcsbPfamContainerIdentifiers
  ├── rcsb_pfam_description : String?  # A human-readable name of protein families and domains.  Examples: Lectin like domain, Cell division control protein 24, 
  ├── rcsb_pfam_identifier : String?  # The unique identifier of protein families and domains in the Pfam database.  Examples: RhoGEF, Clathrin, Peptidase_C14
  ├── rcsb_pfam_provenance_code : String?  # Pfam-A is the manually curated portion of the Pfam database.  Allowable values: Pfam-A
  ├── rcsb_pfam_seed_source : String?  # Pfam entries are classified into six different categories, depending on the length and nature of the sequence regions in
```

## CorePolymerEntity  (from root query: polymer_entities, polymer_entity)
```text
  ├── chem_comp_monomers : CoreChemComp[]?  # Get all unique monomers described in this molecular entity.
  ├── chem_comp_nstd_monomers : CoreChemComp[]?  # Get all unique non-standard monomers described in this molecular entity.
  ├── entity_poly : EntityPoly?
  ├── entity_src_gen : EntitySrcGen[]?
  ├── entity_src_nat : EntitySrcNat[]?
  ├── entry : CoreEntry?  # Get entry that contains this molecular entity.
  ├── pdbx_entity_src_syn : PdbxEntitySrcSyn[]?
  ├── pfams : CorePfam[]?  # Get all unique Pfam annotations associated with this molecular entity.
  ├── polymer_entity_groups : GroupPolymerEntity[]?  # Get all groups for this entity.
  ├── polymer_entity_instances : CorePolymerEntityInstance[]?  # Get all unique polymer instances (chains) for this molecular entity.
  ├── prd : CoreChemComp?  # Get a BIRD chemical components described in this molecular entity.
  ├── rcsb_cluster_flexibility : RcsbClusterFlexibility?
  ├── rcsb_cluster_membership : RcsbClusterMembership[]?
  ├── rcsb_entity_host_organism : RcsbEntityHostOrganism[]?
  ├── rcsb_entity_source_organism : RcsbEntitySourceOrganism[]?
  ├── rcsb_genomic_lineage : RcsbGenomicLineage[]?
  ├── rcsb_id : String  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_membrane_lineage : RcsbMembraneLineage[]?
  ├── rcsb_membrane_lineage_provenance_code : String?  # Mpstruc keyword denotes original annotation, Homology keyword denotes annotation inferred by homology.  Allowable values
  ├── rcsb_polymer_entity : RcsbPolymerEntity?
  ├── rcsb_polymer_entity_align : RcsbPolymerEntityAlign[]?
  ├── rcsb_polymer_entity_annotation : RcsbPolymerEntityAnnotation[]?
  ├── rcsb_polymer_entity_container_identifiers : RcsbPolymerEntityContainerIdentifiers
  ├── rcsb_polymer_entity_feature : RcsbPolymerEntityFeature[]?
  ├── rcsb_polymer_entity_feature_summary : RcsbPolymerEntityFeatureSummary[]?
  ├── rcsb_polymer_entity_group_membership : RcsbPolymerEntityGroupMembership[]?
  ├── rcsb_polymer_entity_keywords : RcsbPolymerEntityKeywords?
  ├── rcsb_polymer_entity_name_com : RcsbPolymerEntityNameCom[]?
  ├── rcsb_polymer_entity_name_sys : RcsbPolymerEntityNameSys[]?
  ├── rcsb_related_target_references : RcsbRelatedTargetReferences[]?
  ├── rcsb_target_cofactors : RcsbTargetCofactors[]?
  ├── uniprots : CoreUniprot[]?  # Get all unique UniProt KB annotations associated with this molecular entity.
```

## CorePolymerEntityInstance  (from root query: polymer_entity_instance, polymer_entity_instances)
```text
  ├── pdbx_struct_special_symmetry : PdbxStructSpecialSymmetry[]?
  ├── pdbx_vrpt_summary_entity_fit_to_map : PdbxVrptSummaryEntityFitToMap[]?
  ├── pdbx_vrpt_summary_entity_geometry : PdbxVrptSummaryEntityGeometry[]?
  ├── polymer_entity : CorePolymerEntity?  # Get polymer entity for this polymer entity instance.
  ├── rcsb_id : String  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
  ├── rcsb_latest_revision : RcsbLatestRevision?
  ├── rcsb_ligand_neighbors : RcsbLigandNeighbors[]?
  ├── rcsb_polymer_entity_instance_container_identifiers : RcsbPolymerEntityInstanceContainerIdentifiers?
  ├── rcsb_polymer_instance_annotation : RcsbPolymerInstanceAnnotation[]?
  ├── rcsb_polymer_instance_feature : RcsbPolymerInstanceFeature[]?
  ├── rcsb_polymer_instance_feature_summary : RcsbPolymerInstanceFeatureSummary[]?
  ├── rcsb_polymer_instance_info : RcsbPolymerInstanceInfo?
  ├── rcsb_polymer_struct_conn : RcsbPolymerStructConn[]?
  ├── struct_asym : StructAsym?
```

## CorePubmed  (from root query: pubmed)
```text
  ├── rcsb_id : String?  # Unique integer value assigned to each PubMed record.
  ├── rcsb_pubmed_abstract_text : String?  # A concise, accurate and factual mini-version of the paper contents.
  ├── rcsb_pubmed_affiliation_info : String[]?  # The institution(s) that the author is affiliated with. Multiple affiliations per author are allowed.
  ├── rcsb_pubmed_central_id : String?  # Unique integer value assigned to each PubMed Central record.
  ├── rcsb_pubmed_container_identifiers : RcsbPubmedContainerIdentifiers
  ├── rcsb_pubmed_doi : String?  # Persistent identifier used to provide a link to an article location on the Internet.
  ├── rcsb_pubmed_mesh_descriptors : String[]?  # NLM controlled vocabulary, Medical Subject Headings (MeSH), is used to characterize the content of the articles represen
  ├── rcsb_pubmed_mesh_descriptors_lineage : RcsbPubmedMeshDescriptorsLineage[]?  # Members of the MeSH classification lineage.
```

## CoreUniprot  (from root query: uniprot)
```text
  ├── rcsb_id : String?  # Primary accession number of a given UniProtKB entry.
  ├── rcsb_uniprot_accession : String[]?  # List of UniProtKB accession numbers where original accession numbers are retained as ‘secondary’ accession numbers.
  ├── rcsb_uniprot_alignments : RcsbUniprotAlignments?  # UniProt pairwise sequence alignments.
  ├── rcsb_uniprot_annotation : RcsbUniprotAnnotation[]?
  ├── rcsb_uniprot_container_identifiers : RcsbUniprotContainerIdentifiers
  ├── rcsb_uniprot_entry_name : String[]?  # A list of unique identifiers (former IDs), often containing biologically relevant information.
  ├── rcsb_uniprot_external_reference : RcsbUniprotExternalReference[]?
  ├── rcsb_uniprot_feature : RcsbUniprotFeature[]?
  ├── rcsb_uniprot_keyword : RcsbUniprotKeyword[]?  # Keywords constitute a controlled vocabulary that summarises the content of a UniProtKB entry.
  ├── rcsb_uniprot_protein : RcsbUniprotProtein?
```

## CurrentEntry
```text
  ├── rcsb_id : String  # The RCSB entry identifier.  Examples: 1KIP
  ├── rcsb_repository_holdings_current : RcsbRepositoryHoldingsCurrent?
  ├── rcsb_repository_holdings_current_entry_container_identifiers : RcsbRepositoryHoldingsCurrentEntryContainerIdentifiers?
```

## Database2
```text
  ├── database_code : String  # The code assigned by the database identified in  _database_2.database_id.  Examples: 4HHB, 3LTQ
  ├── database_id : String  # An abbreviation that identifies the database.  Allowable values: AlphaFoldDB, BMRB, EBI, EMDB, MODBASE, ModelArchive, ND
  ├── pdbx_DOI : String?  # Document Object Identifier (DOI) for this entry registered with http://crossref.org.  Examples: 10.2210/pdb6lu7/pdb
  ├── pdbx_database_accession : String?  # Extended accession code issued for for _database_2.database_code assigned by the database identified in  _database_2.dat
```

## Diffrn
```text
  ├── ambient_pressure : Float?  # The mean hydrostatic pressure in kilopascals at which the  intensities were measured.
  ├── ambient_temp : Float?  # The mean temperature in kelvins at which the intensities were  measured.
  ├── ambient_temp_details : String?  # A description of special aspects of temperature control during  data collection.
  ├── crystal_id : String?  # This data item is a pointer to _exptl_crystal.id in the  EXPTL_CRYSTAL category.
  ├── crystal_support : String?  # The physical device used to support the crystal during data  collection.  Examples: glass capillary, quartz capillary, f
  ├── details : String?  # Special details of the diffraction measurement process. Should  include information about source instability, crystal mo
  ├── id : String  # This data item uniquely identifies a set of diffraction  data.
  ├── pdbx_serial_crystal_experiment : String?  # Y/N if using serial crystallography experiment in which multiple crystals contribute to each diffraction frame in the ex
```

## DiffrnDetector
```text
  ├── details : String?  # A description of special aspects of the radiation detector.
  ├── detector : String?  # The general class of the radiation detector.  Examples: photographic film, scintillation counter, CCD plate, BF~3~ count
  ├── diffrn_id : String  # This data item is a pointer to _diffrn.id in the DIFFRN  category.
  ├── pdbx_collection_date : Date?  # The date of data collection.  Examples: 1996-12-25
  ├── pdbx_frequency : Float?  # The operating frequency of the detector (Hz) used in data collection.
  ├── type : String?  # The make, model or name of the detector device used.  Examples: DECTRIS PILATUS 12M, RAYONIX MX-325
```

## DiffrnRadiation
```text
  ├── collimation : String?  # The collimation or focusing applied to the radiation.  Examples: 0.3 mm double-pinhole, 0.5 mm, focusing mirrors
  ├── diffrn_id : String  # This data item is a pointer to _diffrn.id in the DIFFRN  category.
  ├── monochromator : String?  # The method used to obtain monochromatic radiation. If a mono-  chromator crystal is used, the material and the indices o
  ├── pdbx_diffrn_protocol : String?  # SINGLE WAVELENGTH, LAUE, or MAD.  Examples: SINGLE WAVELENGTH, MONOCHROMATIC, LAUE, MAD, OTHER
  ├── pdbx_monochromatic_or_laue_m_l : String?  # Monochromatic or Laue.  Allowable values: L, M
  ├── pdbx_scattering_type : String?  # The radiation scattering type for this diffraction data set.  Allowable values: electron, neutron, x-ray
  ├── pdbx_wavelength : String?  # Wavelength of radiation.
  ├── pdbx_wavelength_list : String?  # Comma separated list of wavelengths or wavelength range.
  ├── type : String?  # The nature of the radiation. This is typically a description  of the X-ray wavelength in Siegbahn notation.  Examples: C
  ├── wavelength_id : String?  # This data item is a pointer to _diffrn_radiation_wavelength.id  in the DIFFRN_RADIATION_WAVELENGTH category.
```

## DiffrnSource
```text
  ├── details : String?  # A description of special aspects of the radiation source used.
  ├── diffrn_id : String  # This data item is a pointer to _diffrn.id in the DIFFRN  category.
  ├── pdbx_synchrotron_beamline : String?  # Synchrotron beamline.  Examples: 17-ID-1, 19-ID
  ├── pdbx_synchrotron_site : String?  # Synchrotron site.  Examples: APS, NSLS-II
  ├── pdbx_wavelength : String?  # Wavelength of radiation.
  ├── pdbx_wavelength_list : String?  # Comma separated list of wavelengths or wavelength range.  Examples: 0.987 or 0.987, 0.988, 1.0 or 0.99-1.5
  ├── source : String?  # The general class of the radiation source.  Examples: sealed X-ray tube, nuclear reactor, spallation source, electron mi
  ├── type : String?  # The make, model or name of the source of radiation.  Examples: NSLS beamline X8C, Rigaku RU200
```

## DrugbankContainerIdentifiers
```text
  ├── drugbank_id : String  # The DrugBank accession code
```

## DrugbankInfo
```text
  ├── affected_organisms : String[]?  # The DrugBank drug affected organisms.
  ├── atc_codes : String[]?  # The Anatomical Therapeutic Chemical Classification System (ATC) codes.
  ├── brand_names : String[]?  # DrugBank drug brand names.
  ├── cas_number : String?  # The DrugBank assigned Chemical Abstracts Service identifier.  Examples: 56-65-5
  ├── description : String?  # The DrugBank drug description.
  ├── drug_categories : String[]?  # The DrugBank drug categories.
  ├── drug_groups : String[]?  # The DrugBank drug groups determine their drug development status.  Allowable values: approved, experimental, illicit, in
  ├── drug_products : DrugbankInfoDrugProducts[]?
  ├── drugbank_id : String  # The DrugBank accession code
  ├── indication : String?  # The DrugBank drug indication.  Examples: For nutritional supplementation, also for treating dietary shortage or imbalanc
  ├── mechanism_of_action : String?  # The DrugBank drug mechanism of actions.  Examples: ATP is able to store and transport chemical energy within cells.
  ├── name : String?  # The DrugBank drug name.
  ├── pharmacology : String?  # The DrugBank drug pharmacology.  Examples: Adenosine triphosphate (ATP) is the nucleotide known in biochemistry as the "
  ├── synonyms : String[]?  # DrugBank drug name synonyms.
```

## DrugbankInfoDrugProducts
```text
  ├── approved : String?  # Indicates whether this drug has been approved by the regulating government.  Allowable values: N, Y
  ├── country : String?  # The country where this commercially available drug has been approved.  Allowable values: Canada, EU, US
  ├── ended_marketing_on : Date?  # The ending date for market approval.  Examples: 2003-07-30
  ├── name : String?  # The proprietary name(s) provided by the manufacturer for any commercially available products containing this drug.  Exam
  ├── source : String?  # Source of this product information. For example, a value of DPD indicates this information was retrieved from the Canadi
  ├── started_marketing_on : Date?  # The starting date for market approval.  Examples: 1992-12-31
```

## DrugbankTarget
```text
  ├── interaction_type : String?  # The type of target interaction.
  ├── name : String?  # The target name.
  ├── ordinal : Int  # The value of _drugbank_target.ordinal distinguishes  related examples for each chemical component.
  ├── organism_common_name : String?  # The organism common name.
  ├── reference_database_accession_code : String?  # The reference identifier code for the target interaction reference.  Examples: Q9HD40
  ├── reference_database_name : String?  # The reference database name for the target interaction.  Allowable values: UniProt
  ├── seq_one_letter_code : String?  # Target sequence expressed as string of one-letter amino acid codes.  Examples: MAKQRSG...
  ├── target_actions : String[]?  # The actions of the target interaction.
```

## Em2dCrystalEntity
```text
  ├── angle_gamma : Float?  # Unit-cell angle gamma in degrees.
  ├── c_sampling_length : Float?  # Length used to sample the reciprocal lattice lines in the c-direction.
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String  # pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category.
  ├── length_a : Float?  # Unit-cell length a in angstroms.  Examples: null
  ├── length_b : Float?  # Unit-cell length b in angstroms.  Examples: null
  ├── length_c : Float?  # Thickness of 2D crystal  Examples: null
  ├── space_group_name_H_M : String?  # There are 17 plane groups classified as oblique, rectangular, square, and hexagonal.  To describe the symmetry of 2D cry
```

## Em3dCrystalEntity
```text
  ├── angle_alpha : Float?  # Unit-cell angle alpha in degrees.  Examples: null
  ├── angle_beta : Float?  # Unit-cell angle beta in degrees.  Examples: null
  ├── angle_gamma : Float?  # Unit-cell angle gamma in degrees.  Examples: null
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String  # pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category.
  ├── length_a : Float?  # Unit-cell length a in angstroms.  Examples: null
  ├── length_b : Float?  # Unit-cell length b in angstroms.  Examples: null
  ├── length_c : Float?  # Unit-cell length c in angstroms.  Examples: null
  ├── space_group_name : String?  # Space group name.  Examples: P 1, P 21 21 2, I 4, H 3
  ├── space_group_num : Int?  # Space group number.
```

## Em3dFitting
```text
  ├── details : String?  # Any additional details regarding fitting of atomic coordinates into  the 3DEM volume, including data and considerations 
  ├── id : String  # The value of _em_3d_fitting.id must uniquely identify  a fitting procedure of atomic coordinates  into 3dem reconstructe
  ├── method : String?  # The method used to fit atomic coordinates  into the 3dem reconstructed map.
  ├── overall_b_value : Float?  # The overall B (temperature factor) value for the 3d-em volume.
  ├── ref_protocol : String?  # The refinement protocol used.  Allowable values: AB INITIO MODEL, BACKBONE TRACE, FLEXIBLE FIT, OTHER, RIGID BODY FIT
  ├── ref_space : String?  # A flag to indicate whether fitting was carried out in real  or reciprocal refinement space.  Allowable values: REAL, REC
  ├── target_criteria : String?  # The measure used to assess quality of fit of the atomic coordinates in the  3DEM map volume.  Examples: Cross-correlatio
```

## Em3dFittingList
```text
  ├── _3d_fitting_id : String  # The value of _em_3d_fitting_list.3d_fitting_id is a pointer  to  _em_3d_fitting.id in the 3d_fitting category
  ├── details : String?  # Details about the model used in fitting.  Examples: The initial model consisted of the complete biological assembly for 
  ├── id : String  # PRIMARY KEY
  ├── pdb_chain_id : String?  # The ID of the biopolymer chain used for fitting, e.g., A.  Please note that only one chain can be specified per instance
  ├── pdb_chain_residue_range : String?  # Residue range for the identified chain.
  ├── pdb_entry_id : String?  # The PDB code for the entry used in fitting.  Examples: 1EHZ
```

## Em3dReconstruction
```text
  ├── actual_pixel_size : Float?  # The actual pixel size of the projection set of images in Angstroms.  Examples: null, null
  ├── algorithm : String?  # The reconstruction algorithm/technique used to generate the map.
  ├── details : String?  # Any additional details used in the 3d reconstruction.  Examples: a modified version of SPIDER program was used for the r
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String  # Foreign key to the EM_IMAGE_PROCESSING category
  ├── magnification_calibration : String?  # The magnification calibration method for the 3d reconstruction.  Examples: TMV images
  ├── method : String?  # The algorithm method used for the 3d-reconstruction.  Examples: cross-common lines, polar Fourier transform (PFT)
  ├── nominal_pixel_size : Float?  # The nominal pixel size of the projection set of images in Angstroms.  Examples: null, null
  ├── num_class_averages : Int?  # The number of classes used in the final 3d reconstruction
  ├── num_particles : Int?  # The number of 2D projections or 3D subtomograms used in the 3d reconstruction
  ├── refinement_type : String?  # Indicates details on how the half-map used for resolution determination (usually by FSC) have been generated.  Allowable
  ├── resolution : Float?  # The final resolution (in angstroms) of the 3D reconstruction.  Examples: null, null
  ├── resolution_method : String?  # The  method used to determine the final resolution  of the 3d reconstruction.  The Fourier Shell Correlation criterion a
  ├── symmetry_type : String?  # The type of symmetry applied to the reconstruction  Allowable values: 2D CRYSTAL, 3D CRYSTAL, HELICAL, POINT
```

## EmCtfCorrection
```text
  ├── details : String?  # Any additional details about CTF correction  Examples: CTF amplitude correction was performed following 3D reconstructio
  ├── em_image_processing_id : String?  # Foreign key to the EM_IMAGE_PROCESSING category
  ├── id : String  # PRIMARY KEY
  ├── type : String?  # Type of CTF correction applied
```

## EmDiffraction
```text
  ├── camera_length : Float?  # The camera length (in millimeters). The camera length is the  product of the objective focal length and the combined mag
  ├── id : String  # PRIMARY KEY
  ├── imaging_id : String?  # Foreign key to the EM_IMAGING category
  ├── tilt_angle_list : String?  # Comma-separated list of tilt angles (in degrees) used in the electron diffraction experiment.  Examples: 20,40,50,55
```

## EmDiffractionShell
```text
  ├── em_diffraction_stats_id : String?  # Pointer to EM CRYSTALLOGRAPHY STATS
  ├── fourier_space_coverage : Float?  # Completeness of the structure factor data within this resolution shell, in percent  Examples: null
  ├── high_resolution : Float?  # High resolution limit for this shell (angstroms)  Examples: null
  ├── id : String  # PRIMARY KEY
  ├── low_resolution : Float?  # Low resolution limit for this shell (angstroms)  Examples: null
  ├── multiplicity : Float?  # Multiplicity (average number of measurements) for the structure factors in this resolution shell  Examples: null
  ├── num_structure_factors : Int?  # Number of measured structure factors in this resolution shell
  ├── phase_residual : Float?  # Phase residual for this resolution shell, in degrees  Examples: null
```

## EmDiffractionStats
```text
  ├── details : String?  # Any addition details about the structure factor measurements  Examples: Phases were obtained from micrograph images of t
  ├── fourier_space_coverage : Float?  # Completeness of the structure factor data within the defined space group  at the reported resolution (percent).  Example
  ├── high_resolution : Float?  # High resolution limit of the structure factor data, in angstroms  Examples: null
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String?  # Pointer to _em_image_processing.id
  ├── num_intensities_measured : Int?  # Total number of diffraction intensities measured (before averaging)
  ├── num_structure_factors : Int?  # Number of structure factors obtained (merged amplitudes + phases)
  ├── overall_phase_error : Float?  # Overall phase error in degrees  Examples: null
  ├── overall_phase_residual : Float?  # Overall phase residual in degrees  Examples: null
  ├── phase_error_rejection_criteria : String?  # Criteria used to reject phases  Examples: Structure factors with phase errors higher than 20 degrees were omitted from r
  ├── r_merge : Float?  # Rmerge value (percent)  Examples: null
  ├── r_sym : Float?  # Rsym value (percent)  Examples: null
```

## EmEmbedding
```text
  ├── details : String?  # Staining procedure used in the specimen preparation.  Examples: The crystal suspension was injected into the lens of a d
  ├── id : String  # PRIMARY KEY
  ├── material : String?  # The embedding  material.  Examples: tannin and glucose
  ├── specimen_id : String?  # Foreign key relationship to the EM SPECIMEN category
```

## EmEntityAssembly
```text
  ├── details : String?  # Additional details about the sample or sample subcomponent.  Examples: Fab fragment generated by proteolytic cleavage of
  ├── entity_id_list : String[]?  # macromolecules associated with this component, if defined  as comma separated list of entity ids (integers).
  ├── id : String  # PRIMARY KEY
  ├── name : String?  # The name of the sample or sample subcomponent.  Examples: Ternary complex of alpha-tubulin with tubulin folding cofactor
  ├── oligomeric_details : String?  # oligomeric details
  ├── parent_id : Int?  # The parent of this assembly.  This data item is an internal category pointer to _em_entity_assembly.id.  By convention, 
  ├── source : String?  # The type of source (e.g., natural source) for the component (sample or sample subcomponent)  Allowable values: MULTIPLE 
  ├── synonym : String?  # Alternative name of the component.  Examples: FADV-1
  ├── type : String?  # The general type of the sample or sample subcomponent.
```

## EmExperiment
```text
  ├── aggregation_state : String?  # The aggregation/assembly state of the imaged specimen.  Allowable values: 2D ARRAY, 3D ARRAY, CELL, FILAMENT, HELICAL AR
  ├── entity_assembly_id : String?  # Foreign key to the EM_ENTITY_ASSEMBLY category
  ├── id : String?  # PRIMARY KEY
  ├── reconstruction_method : String?  # The reconstruction method used in the EM experiment.  Allowable values: CRYSTALLOGRAPHY, HELICAL, SINGLE PARTICLE, SUBTO
```

## EmHelicalEntity
```text
  ├── angular_rotation_per_subunit : Float?  # The angular rotation per helical subunit in degrees. Negative values indicate left-handed helices; positive values indic
  ├── axial_rise_per_subunit : Float?  # The axial rise per subunit in the helical assembly.  Examples: null
  ├── axial_symmetry : String?  # Symmetry of the helical axis, either cyclic (Cn) or dihedral (Dn), where n>=1.  Examples: C1, D2, C7
  ├── details : String?  # Any other details regarding the helical assembly  Examples: Dihedral symmetry
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String  # This data item is a pointer to _em_image_processing.id.
```

## EmImageRecording
```text
  ├── average_exposure_time : Float?  # The average exposure time for each image.  Examples: null
  ├── avg_electron_dose_per_image : Float?  # The electron dose received by the specimen per image (electrons per square angstrom).  Examples: null
  ├── details : String?  # Any additional details about image recording.  Examples: Images were collected in movie-mode at 17 frames per second
  ├── detector_mode : String?  # The detector mode used during image recording.  Allowable values: COUNTING, INTEGRATING, OTHER, SUPER-RESOLUTION
  ├── film_or_detector_model : String?  # The detector type used for recording images.  Usually film , CCD camera or direct electron detector.
  ├── id : String  # PRIMARY KEY
  ├── imaging_id : String  # This data item the id of the microscopy settings used in the imaging.
  ├── num_diffraction_images : Int?  # The number of diffraction images collected.
  ├── num_grids_imaged : Int?  # Number of grids in the microscopy session
  ├── num_real_images : Int?  # The number of micrograph images collected.
```

## EmImaging
```text
  ├── accelerating_voltage : Int?  # A value of accelerating voltage (in kV) used for imaging.
  ├── alignment_procedure : String?  # The type of procedure used to align the microscope electron beam.  Allowable values: BASIC, COMA FREE, NONE, OTHER, ZEML
  ├── astigmatism : String?  # astigmatism
  ├── c2_aperture_diameter : Float?  # The open diameter of the c2 condenser lens,  in microns.
  ├── calibrated_defocus_max : Float?  # The maximum calibrated defocus value of the objective lens (in nanometres) used  to obtain the recorded images. Negative
  ├── calibrated_defocus_min : Float?  # The minimum calibrated defocus value of the objective lens (in nanometres) used  to obtain the recorded images. Negative
  ├── calibrated_magnification : Int?  # The magnification value obtained for a known standard just  prior to, during or just after the imaging experiment.
  ├── cryogen : String?  # Cryogen type used to maintain the specimen stage temperature during imaging  in the microscope.  Allowable values: HELIU
  ├── date : Date?  # Date (YYYY-MM-DD) of imaging experiment or the date at which  a series of experiments began.  Examples: 2001-05-08
  ├── details : String?  # Any additional imaging details.  Examples: Preliminary grid screening was performed manually.
  ├── detector_distance : Float?  # The camera length (in millimeters). The camera length is the  product of the objective focal length and the combined mag
  ├── electron_beam_tilt_params : String?  # electron beam tilt params
  ├── electron_source : String?  # The source of electrons. The electron gun.
  ├── id : String  # PRIMARY KEY
  ├── illumination_mode : String?  # The mode of illumination.  Allowable values: FLOOD BEAM, OTHER, SPOT SCAN
  ├── microscope_model : String?  # The name of the model of microscope.  Allowable values: FEI MORGAGNI, FEI POLARA 300, FEI TALOS ARCTICA, FEI TECNAI 10, 
  ├── mode : String?  # The mode of imaging.  Allowable values: 4D-STEM, BRIGHT FIELD, DARK FIELD, DIFFRACTION, OTHER
  ├── nominal_cs : Float?  # The spherical aberration coefficient (Cs) in millimeters,  of the objective lens.  Examples: null
  ├── nominal_defocus_max : Float?  # The maximum defocus value of the objective lens (in nanometres) used  to obtain the recorded images. Negative values ref
  ├── nominal_defocus_min : Float?  # The minimum defocus value of the objective lens (in nanometres) used  to obtain the recorded images. Negative values ref
  ├── nominal_magnification : Int?  # The magnification indicated by the microscope readout.
  ├── recording_temperature_maximum : Float?  # The specimen temperature maximum (kelvin) for the duration  of imaging.
  ├── recording_temperature_minimum : Float?  # The specimen temperature minimum (kelvin) for the duration  of imaging.
  ├── residual_tilt : Float?  # Residual tilt of the electron beam (in miliradians)
  ├── specimen_holder_model : String?  # The name of the model of specimen holder used during imaging.  Allowable values: FEI TITAN KRIOS AUTOGRID HOLDER, FISCHI
  ├── specimen_holder_type : String?  # The type of specimen holder used during imaging.  Examples: cryo
  ├── specimen_id : String?  # Foreign key to the EM_SPECIMEN category
  ├── temperature : Float?  # The mean specimen stage temperature (in kelvin) during imaging  in the microscope.
  ├── tilt_angle_max : Float?  # The maximum angle at which the specimen was tilted to obtain  recorded images.
  ├── tilt_angle_min : Float?  # The minimum angle at which the specimen was tilted to obtain  recorded images.
```

## EmParticleSelection
```text
  ├── details : String?  # Additional detail such as description of filters used, if selection was manual or automated, and/or template details.  E
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String  # The value of _em_particle_selection.image_processing_id points to  the EM_IMAGE_PROCESSING category.
  ├── num_particles_selected : Int?  # The number of particles selected from the projection set of images.
```

## EmSingleParticleEntity
```text
  ├── id : Int  # PRIMARY KEY
  ├── image_processing_id : String  # pointer to _em_image_processing.id.
  ├── point_symmetry : String?  # Point symmetry symbol, either Cn, Dn, T, O, or I  Examples: C1, C5, C4
```

## EmSoftware
```text
  ├── category : String?  # The purpose of the software.  Allowable values: CLASSIFICATION, CRYSTALLOGRAPHY MERGING, CTF CORRECTION, DIFFRACTION IND
  ├── details : String?  # Details about the software used.  Examples: EMAN2 e2boxer.py was used to automatically select particle images.
  ├── fitting_id : String?  # pointer to _em_3d_fitting.id in the EM_3D_FITTING category.
  ├── id : String  # PRIMARY KEY
  ├── image_processing_id : String?  # pointer to _em_image_processing.id in the EM_IMAGE_PROCESSING category.
  ├── imaging_id : String?  # pointer to _em_imaging.id in the EM_IMAGING category.
  ├── name : String?  # The name of the software package used, e.g., RELION.  Depositors are strongly   encouraged to provide a value in this fi
  ├── version : String?  # The version of the software.  Examples: 9.03, 2.1
```

## EmSpecimen
```text
  ├── concentration : Float?  # The concentration (in milligrams per milliliter, mg/ml)  of the complex in the sample.  Examples: null
  ├── details : String?  # A description of any additional details of the specimen preparation.  Examples: This sample was monodisperse., Au was de
  ├── embedding_applied : String?  # 'YES' indicates that the specimen has been embedded.  Allowable values: NO, YES
  ├── experiment_id : String  # Pointer to _em_experiment.id.
  ├── id : String  # PRIMARY KEY
  ├── shadowing_applied : String?  # 'YES' indicates that the specimen has been shadowed.  Allowable values: NO, YES
  ├── staining_applied : String?  # 'YES' indicates that the specimen has been stained.  Allowable values: NO, YES
  ├── vitrification_applied : String?  # 'YES' indicates that the specimen was vitrified by cryopreservation.  Allowable values: NO, YES
```

## EmStaining
```text
  ├── details : String?  # Staining procedure used in the specimen preparation.  Examples: Negatively stained EM specimens were prepared using a ca
  ├── id : String  # PRIMARY KEY
  ├── material : String?  # The staining  material.  Examples: Uranyl Acetate
  ├── specimen_id : String?  # Foreign key relationship to the EM SPECIMEN category
  ├── type : String?  # type of staining  Allowable values: NEGATIVE, NONE, POSITIVE
```

## EmVitrification
```text
  ├── chamber_temperature : Float?  # The temperature (in kelvin) of the sample just prior to vitrification.
  ├── cryogen_name : String?  # This is the name of the cryogen.  Allowable values: ETHANE, ETHANE-PROPANE, FREON 12, FREON 22, HELIUM, METHANE, NITROGE
  ├── details : String?  # Any additional details relating to vitrification.  Examples: Vitrification carried out in argon atmosphere.
  ├── humidity : Float?  # Relative humidity (%) of air surrounding the specimen just prior to vitrification.
  ├── id : String  # PRIMARY KEY
  ├── instrument : String?  # The type of instrument used in the vitrification process.  Allowable values: CRYOSOL VITROJET, EMS-002 RAPID IMMERSION F
  ├── method : String?  # The procedure for vitrification.  Examples: plunge freezing
  ├── specimen_id : String  # This data item is a pointer to _em_specimen.id
  ├── temp : Float?  # The vitrification temperature (in kelvin), e.g.,   temperature of the plunge instrument cryogen bath.
  ├── time_resolved_state : String?  # The length of time after an event effecting the sample that  vitrification was induced and a description of the event.  
```

## EntityPoly
```text
  ├── nstd_linkage : String?  # A flag to indicate whether the polymer contains at least  one monomer-to-monomer link different from that implied by  _e
  ├── nstd_monomer : String?  # A flag to indicate whether the polymer contains at least  one monomer that is not considered standard.  Allowable values
  ├── pdbx_seq_one_letter_code : String?  # Sequence of protein or nucleic acid polymer in standard one-letter                codes of amino acids or nucleotides. N
  ├── pdbx_seq_one_letter_code_can : String?  # Canonical sequence of protein or nucleic acid polymer in standard                one-letter codes of amino acids or nucl
  ├── pdbx_sequence_evidence_code : String?  # Evidence for the assignment of the polymer sequence.  Allowable values: depositor provided, derived from coordinates
  ├── pdbx_strand_id : String?  # The PDB strand/chain id(s) corresponding to this polymer entity.  Examples: A,B, A, B, A,B,C
  ├── pdbx_target_identifier : String?  # For Structural Genomics entries, the sequence's target identifier registered at the TargetTrack database.  Examples: JCS
  ├── rcsb_artifact_monomer_count : Int?  # Number of regions in the sample sequence identified as expression tags, linkers, or  cloning artifacts.
  ├── rcsb_conflict_count : Int?  # Number of monomer conflicts relative to the reference sequence.
  ├── rcsb_deletion_count : Int?  # Number of monomer deletions relative to the reference sequence.
  ├── rcsb_entity_polymer_type : String?  # A coarse-grained polymer entity type.  Allowable values: DNA, NA-hybrid, Other, Protein, RNA
  ├── rcsb_insertion_count : Int?  # Number of monomer insertions relative to the reference sequence.
  ├── rcsb_mutation_count : Int?  # Number of engineered mutations engineered in the sample sequence.
  ├── rcsb_non_std_monomer_count : Int?  # Number of non-standard monomers in the sample sequence.
  ├── rcsb_non_std_monomers : String[]?  # Unique list of non-standard monomer chemical component identifiers in the sample sequence.
  ├── rcsb_prd_id : String?  # For polymer BIRD molecules the BIRD identifier for the entity.
  ├── rcsb_sample_sequence_length : Int?  # The monomer length of the sample sequence.
  ├── type : String?  # The type of the polymer.  Allowable values: cyclic-pseudo-peptide, other, peptide nucleic acid, polydeoxyribonucleotide,
```

## EntitySrcGen
```text
  ├── expression_system_id : String?  # A unique identifier for the expression system. This  should be extracted from a local list of expression  systems.
  ├── gene_src_common_name : String?  # The common name of the natural organism from which the gene was  obtained.  Examples: man, yeast, bacteria
  ├── gene_src_details : String?  # A description of special aspects of the natural organism from  which the gene was obtained.
  ├── gene_src_genus : String?  # The genus of the natural organism from which the gene was  obtained.  Examples: Homo, Saccharomyces, Escherichia
  ├── gene_src_species : String?  # The species of the natural organism from which the gene was  obtained.  Examples: sapiens, cerevisiae, coli
  ├── gene_src_strain : String?  # The strain of the natural organism from which the gene was  obtained, if relevant.  Examples: DH5a, BMH 71-18
  ├── gene_src_tissue : String?  # The tissue of the natural organism from which the gene was  obtained.  Examples: heart, liver, eye lens
  ├── gene_src_tissue_fraction : String?  # The subcellular fraction of the tissue of the natural organism  from which the gene was obtained.  Examples: mitochondri
  ├── host_org_common_name : String?  # The common name of the organism that served as host for the  production of the entity.  Where full details of the protei
  ├── host_org_details : String?  # A description of special aspects of the organism that served as  host for the production of the entity. Where full detai
  ├── host_org_genus : String?  # The genus of the organism that served as host for the production  of the entity.  Examples: Saccharomyces, Escherichia
  ├── host_org_species : String?  # The species of the organism that served as host for the  production of the entity.  Examples: cerevisiae, coli
  ├── pdbx_alt_source_flag : String?  # This data item identifies cases in which an alternative source  modeled.  Allowable values: model, sample
  ├── pdbx_beg_seq_num : Int?  # The beginning polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequ
  ├── pdbx_description : String?  # Information on the source which is not given elsewhere.
  ├── pdbx_end_seq_num : Int?  # The ending polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequenc
  ├── pdbx_gene_src_atcc : String?  # American Type Culture Collection tissue culture number.  Examples: 6051
  ├── pdbx_gene_src_cell : String?  # Cell type.  Examples: ENDOTHELIAL
  ├── pdbx_gene_src_cell_line : String?  # The specific line of cells.  Examples: HELA CELLS
  ├── pdbx_gene_src_cellular_location : String?  # Identifies the location inside (or outside) the cell.  Examples: CYTOPLASM, NUCLEUS
  ├── pdbx_gene_src_fragment : String?  # A domain or fragment of the molecule.  Examples: CYTOPLASM, NUCLEUS
  ├── pdbx_gene_src_gene : String?  # Identifies the gene.
  ├── pdbx_gene_src_ncbi_taxonomy_id : String?  # NCBI Taxonomy identifier for the gene source organism.   Reference:   Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden T
  ├── pdbx_gene_src_organ : String?  # Organized group of tissues that carries on a specialized function.  Examples: KIDNEY, LIVER, PANCREAS
  ├── pdbx_gene_src_organelle : String?  # Organized structure within cell.  Examples: MITOCHONDRIA
  ├── pdbx_gene_src_scientific_name : String?  # Scientific name of the organism.  Examples: Homo sapiens, Saccharomyces Cerevisiae
  ├── pdbx_gene_src_variant : String?  # Identifies the variant.  Examples: DELTAH1DELTATRP
  ├── pdbx_host_org_atcc : String?  # Americal Tissue Culture Collection of the expression system. Where  full details of the protein production are available
  ├── pdbx_host_org_cell : String?  # Cell type from which the gene is derived. Where  entity.target_id is provided this should be derived from  details of th
  ├── pdbx_host_org_cell_line : String?  # A specific line of cells used as the expression system. Where  full details of the protein production are available it w
  ├── pdbx_host_org_cellular_location : String?  # Identifies the location inside (or outside) the cell which  expressed the molecule.  Examples: CYTOPLASM, NUCLEUS
  ├── pdbx_host_org_culture_collection : String?  # Culture collection of the expression system. Where  full details of the protein production are available it would  be ex
  ├── pdbx_host_org_gene : String?  # Specific gene which expressed the molecule.  Examples: HIV-1 POL, GLNS7, U1A (2-98, Y31H, Q36R)
  ├── pdbx_host_org_ncbi_taxonomy_id : String?  # NCBI Taxonomy identifier for the expression system organism.   Reference:   Wheeler DL, Chappey C, Lash AE, Leipe DD, Ma
  ├── pdbx_host_org_organ : String?  # Specific organ which expressed the molecule.  Examples: KIDNEY
  ├── pdbx_host_org_organelle : String?  # Specific organelle which expressed the molecule.  Examples: MITOCHONDRIA
  ├── pdbx_host_org_scientific_name : String?  # The scientific name of the organism that served as host for the  production of the entity. Where full details of the pro
  ├── pdbx_host_org_strain : String?  # The strain of the organism in which the entity was expressed.  Examples: AR120
  ├── pdbx_host_org_tissue : String?  # The specific tissue which expressed the molecule. Where full details  of the protein production are available it would b
  ├── pdbx_host_org_tissue_fraction : String?  # The fraction of the tissue which expressed the molecule.  Examples: mitochondria, nucleus, membrane
  ├── pdbx_host_org_variant : String?  # Variant of the organism used as the expression system. Where  full details of the protein production are available it wo
  ├── pdbx_host_org_vector : String?  # Identifies the vector used. Where full details of the protein  production are available it would be expected that this i
  ├── pdbx_host_org_vector_type : String?  # Identifies the type of vector used (plasmid, virus, or cosmid).  Where full details of the protein production are availa
  ├── pdbx_seq_type : String?  # This data item povides additional information about the sequence type.  Allowable values: Biological sequence, C-termina
  ├── pdbx_src_id : Int  # This data item is an ordinal identifier for entity_src_gen data records.
  ├── plasmid_details : String?  # A description of special aspects of the plasmid that produced the  entity in the host organism. Where full details of th
  ├── plasmid_name : String?  # The name of the plasmid that produced the entity in the host  organism. Where full details of the protein production are
```

## EntitySrcNat
```text
  ├── common_name : String?  # The common name of the organism from which the entity  was isolated.  Examples: man, yeast, bacteria
  ├── details : String?  # A description of special aspects of the organism from which the  entity was isolated.
  ├── genus : String?  # The genus of the organism from which the entity was isolated.  Examples: Homo, Saccharomyces, Escherichia
  ├── pdbx_alt_source_flag : String?  # This data item identifies cases in which an alternative source  modeled.  Allowable values: model, sample
  ├── pdbx_atcc : String?  # Americal Tissue Culture Collection number.  Examples: 6051
  ├── pdbx_beg_seq_num : Int?  # The beginning polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequ
  ├── pdbx_cell : String?  # A particular cell type.  Examples: BHK-21
  ├── pdbx_cell_line : String?  # The specific line of cells.  Examples: HELA
  ├── pdbx_cellular_location : String?  # Identifies the location inside (or outside) the cell.
  ├── pdbx_end_seq_num : Int?  # The ending polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequenc
  ├── pdbx_fragment : String?  # A domain or fragment of the molecule.
  ├── pdbx_ncbi_taxonomy_id : String?  # NCBI Taxonomy identifier for the source organism.   Reference:   Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Sc
  ├── pdbx_organ : String?  # Organized group of tissues that carries on a specialized function.  Examples: KIDNEY
  ├── pdbx_organelle : String?  # Organized structure within cell.  Examples: MITOCHONDRIA
  ├── pdbx_organism_scientific : String?  # Scientific name of the organism of the natural source.  Examples: Bos taurus, BOS TAURUS, SUS SCROFA, ASPERGILLUS ORYZAE
  ├── pdbx_plasmid_details : String?  # Details about the plasmid.  Examples: PLC28 DERIVATIVE
  ├── pdbx_plasmid_name : String?  # The plasmid containing the gene.  Examples: pB322
  ├── pdbx_secretion : String?  # Identifies the secretion from which the molecule was isolated.  Examples: saliva, urine, venom
  ├── pdbx_src_id : Int  # This data item is an ordinal identifier for entity_src_nat data records.
  ├── pdbx_variant : String?  # Identifies the variant.
  ├── species : String?  # The species of the organism from which the entity was isolated.  Examples: sapiens, cerevisiae, coli
  ├── strain : String?  # The strain of the organism from which the entity was isolated.  Examples: DH5a, BMH 71-18
  ├── tissue : String?  # The tissue of the organism from which the entity was isolated.  Examples: heart, liver, eye lens
  ├── tissue_fraction : String?  # The subcellular fraction of the tissue of the organism from  which the entity was isolated.  Examples: mitochondria, nuc
```

## Entry
```text
  ├── id : String  # The value of _entry.id identifies the data block.   Note that this item need not be a number; it can be any unique  iden
  ├── ma_collection_id : String?  # An identifier for the model collection associated with the entry.
```

## Exptl
```text
  ├── crystals_number : Int?  # The total number of crystals used in the  measurement of  intensities.
  ├── details : String?  # Any special information about the experimental work prior to the  intensity measurement. See also _exptl_crystal.prepara
  ├── method : String  # The method used in the experiment.  Allowable values: ELECTRON CRYSTALLOGRAPHY, ELECTRON MICROSCOPY, EPR, FIBER DIFFRACT
  ├── method_details : String?  # A description of special aspects of the experimental method.  Examples: 29 structures, minimized average structure
```

## ExptlCrystal
```text
  ├── colour : String?  # The colour of the crystal.  Examples: dark green
  ├── density_Matthews : Float?  # The density of the crystal, expressed as the ratio of the  volume of the asymmetric unit to the molecular mass of a  mon
  ├── density_meas : Float?  # Density values measured using standard chemical and physical  methods. The units are megagrams per cubic metre (grams pe
  ├── density_percent_sol : Float?  # Density value P calculated from the crystal cell and contents,  expressed as per cent solvent.   P = 1 - (1.23 N MMass) 
  ├── description : String?  # A description of the quality and habit of the crystal.  The crystal dimensions should not normally be reported here;  us
  ├── id : String  # The value of _exptl_crystal.id must uniquely identify a record in  the EXPTL_CRYSTAL list.   Note that this item need no
  ├── pdbx_mosaicity : Float?  # Isotropic approximation of the distribution of mis-orientation angles specified in degrees of all the mosaic domain bloc
  ├── pdbx_mosaicity_esd : Float?  # The uncertainty in the mosaicity estimate for the crystal.
  ├── preparation : String?  # Details of crystal growth and preparation of the crystal (e.g.  mounting) prior to the intensity measurements.  Examples
```

## ExptlCrystalGrow
```text
  ├── crystal_id : String  # This data item is a pointer to _exptl_crystal.id in the  EXPTL_CRYSTAL category.
  ├── details : String?  # A description of special aspects of the crystal growth.  Examples: Solution 2 was prepared as a well solution and       
  ├── method : String?  # The method used to grow the crystals.  Examples: MICROBATCH, VAPOR DIFFUSION, HANGING DROP
  ├── pH : Float?  # The pH at which the crystal was grown. If more than one pH was  employed during the crystallization process, the final p
  ├── pdbx_details : String?  # Text description of crystal growth procedure.  Examples: PEG 4000, potassium phosphate, magnesium chloride, cacodylate
  ├── pdbx_pH_range : String?  # The range of pH values at which the crystal was grown.   Used when  a point estimate of pH is not appropriate.  Examples
  ├── temp : Float?  # The temperature in kelvins at which the crystal was grown.  If more than one temperature was employed during the  crysta
  ├── temp_details : String?  # A description of special aspects of temperature control during  crystal growth.
```

## GeneName
```text
  ├── type : String?  # Allowable values: PRIMARY, SYNONYM, ORDERED_LOCUS, ORF.
  ├── value : String?
```

## GroupEntry  (from root query: entry_group, entry_groups)
```text
  ├── group_provenance : GroupProvenance?  # Get provenance associated with this group.
  ├── rcsb_group_accession_info : RcsbGroupAccessionInfo?
  ├── rcsb_group_container_identifiers : RcsbGroupContainerIdentifiers
  ├── rcsb_group_info : RcsbGroupInfo
  ├── rcsb_group_related : RcsbGroupRelated[]?
  ├── rcsb_group_statistics : RcsbGroupStatistics?
  ├── rcsb_id : String  # A unique textual identifier for a group
```

## GroupMembersAlignmentScores
```text
  ├── query_coverage : Int
  ├── query_length : Int
  ├── target_coverage : Int
  ├── target_length : Int
```

## GroupNonPolymerEntity  (from root query: nonpolymer_entity_groups, nonpolymer_entity_group)
```text
  ├── rcsb_group_accession_info : RcsbGroupAccessionInfo?
  ├── rcsb_group_container_identifiers : RcsbGroupContainerIdentifiers
  ├── rcsb_group_info : RcsbGroupInfo
  ├── rcsb_group_related : RcsbGroupRelated[]?
  ├── rcsb_group_statistics : RcsbGroupStatistics?
  ├── rcsb_id : String  # A unique textual identifier for a group
```

## GroupPolymerEntity  (from root query: polymer_entity_groups, polymer_entity_group)
```text
  ├── group_provenance : GroupProvenance?  # Get provenance associated with this group.
  ├── rcsb_group_accession_info : RcsbGroupAccessionInfo?
  ├── rcsb_group_container_identifiers : RcsbGroupContainerIdentifiers
  ├── rcsb_group_info : RcsbGroupInfo
  ├── rcsb_group_related : RcsbGroupRelated[]?
  ├── rcsb_group_statistics : RcsbGroupStatistics?
  ├── rcsb_id : String  # A unique textual identifier for a group
  ├── rcsb_polymer_entity_group_members_rankings : RcsbPolymerEntityGroupMembersRankings[]?
  ├── rcsb_polymer_entity_group_sequence_alignment : RcsbPolymerEntityGroupSequenceAlignment?
```

## GroupProvenance  (from root query: group_provenance)
```text
  ├── rcsb_group_aggregation_method : RcsbGroupAggregationMethod?
  ├── rcsb_group_provenance_container_identifiers : RcsbGroupProvenanceContainerIdentifiers?
  ├── rcsb_id : String?  # A unique textual identifier for a group provenance
```

## IhmEntryCollectionMapping
```text
  ├── collection_id : String  # Identifier for the entry collection.   This data item is a pointer to _ihm_entry_collection.id in the   IHM_ENTRY_COLLEC
```

## IhmExternalReferenceInfo
```text
  ├── associated_url : String?  # The Uniform Resource Locator (URL) corresponding to the external reference (DOI).   This URL should link to the correspo
  ├── reference : String?  # The external reference or the Digital Object Identifier (DOI).  This field is not relevant for local files.  Examples: 1
  ├── reference_provider : String?  # The name of the reference provider.  Examples: Zenodo, Figshare, Crossref
```

## InterfacePartnerFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: TO_BE_DEFINED
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## InterfacePartnerFeatureFeaturePositions
```text
  ├── beg_seq_id : Int  # An identifier for the monomer at which this segment of the feature begins.
  ├── end_seq_id : Int?  # An identifier for the monomer at which this segment of the feature ends.
  ├── values : Float[]?  # The value(s) of the feature over the monomer segment.
```

## MaData
```text
  ├── content_type : String?  # The type of data held in the dataset.  Allowable values: coevolution MSA, input structure, model coordinates, other, pol
  ├── content_type_other_details : String?  # Details for other content types.
  ├── id : Int  # A unique identifier for the data.
  ├── name : String?  # An author-given name for the content held in the dataset.  Examples: NMR NOE Distances, Target Template Alignment, Coevo
```

## MethodDetails
```text
  ├── description : String?  # A description of special aspects of the clustering process
  ├── name : String?  # Defines the name of the description associated with the clustering process
  ├── type : String?  # Defines the type of the description associated with the clustering process
  ├── value : Float?  # Defines the value associated with the clustering process
```

## PdbxAuditRevisionCategory
```text
  ├── category : String?  # The category updated in the pdbx_audit_revision_category record.  Examples: audit_author, citation
  ├── data_content_type : String  # The type of file that the pdbx_audit_revision_history record refers to.  Allowable values: Additional map, Chemical comp
  ├── ordinal : Int  # A unique identifier for the pdbx_audit_revision_category record.
  ├── revision_ordinal : Int  # A pointer to  _pdbx_audit_revision_history.ordinal
```

## PdbxAuditRevisionDetails
```text
  ├── data_content_type : String  # The type of file that the pdbx_audit_revision_history record refers to.  Allowable values: Additional map, Chemical comp
  ├── description : String?  # Additional details describing the revision.
  ├── details : String?  # Further details describing the revision.
  ├── ordinal : Int  # A unique identifier for the pdbx_audit_revision_details record.
  ├── provider : String?  # The provider of the revision.  Allowable values: author, repository
  ├── revision_ordinal : Int  # A pointer to  _pdbx_audit_revision_history.ordinal
  ├── type : String?  # A type classification of the revision  Allowable values: Coordinate replacement, Data added, Data removed, Data updated,
```

## PdbxAuditRevisionGroup
```text
  ├── data_content_type : String  # The type of file that the pdbx_audit_revision_history record refers to.  Allowable values: Additional map, Chemical comp
  ├── group : String?  # The collection of categories updated with this revision.  Allowable values: Advisory, Atomic model, Author supporting ev
  ├── ordinal : Int  # A unique identifier for the pdbx_audit_revision_group record.
  ├── revision_ordinal : Int  # A pointer to  _pdbx_audit_revision_history.ordinal
```

## PdbxAuditRevisionHistory
```text
  ├── data_content_type : String  # The type of file that the pdbx_audit_revision_history record refers to.  Allowable values: Additional map, Chemical comp
  ├── major_revision : Int?  # The major version number of deposition release.
  ├── minor_revision : Int?  # The minor version number of deposition release.
  ├── ordinal : Int  # A unique identifier for the pdbx_audit_revision_history record.
  ├── revision_date : Date?  # The release date of the revision  Examples: 2017-03-08
```

## PdbxAuditRevisionItem
```text
  ├── data_content_type : String  # The type of file that the pdbx_audit_revision_history record refers to.  Allowable values: Additional map, Chemical comp
  ├── item : String?  # A high level explanation the author has provided for submitting a revision.  Examples: _atom_site.type_symbol
  ├── ordinal : Int  # A unique identifier for the pdbx_audit_revision_item record.
  ├── revision_ordinal : Int  # A pointer to  _pdbx_audit_revision_history.ordinal
```

## PdbxAuditSupport
```text
  ├── country : String?  # The country/region providing the funding support for the entry.  Funding information is optionally provided for entries 
  ├── funding_organization : String?  # The name of the organization providing funding support for the  entry. Funding information is optionally provided for en
  ├── grant_number : String?  # The grant number associated with this source of support.
  ├── ordinal : Int  # A unique sequential integer identifier for each source of support for this entry.
```

## PdbxChemCompAudit
```text
  ├── action_type : String?  # The action associated with this audit record.  Allowable values: Create component, Initial release, Modify PCM, Modify a
  ├── comp_id : String?  # This data item is a pointer to _chem_comp.id in the CHEM_COMP  category.
  ├── date : Date?  # The date associated with this audit record.
  ├── details : String?  # Additional details decribing this change.  Examples: Added C14 as a leaving atom.
  ├── ordinal : Int  # This data item is an ordinal index for the  PDBX_CHEM_COMP_AUDIT category.
```

## PdbxChemCompDescriptor
```text
  ├── comp_id : String  # This data item is a pointer to _chem_comp.id in the CHEM_COMP  category.
  ├── descriptor : String?  # This data item contains the descriptor value for this  component.
  ├── program : String  # This data item contains the name of the program  or library used to compute the descriptor.  Examples: OPENEYE, CACTVS, 
  ├── program_version : String  # This data item contains the version of the program  or library used to compute the descriptor.
  ├── type : String  # This data item contains the descriptor type.  Allowable values: InChI, InChIKey, InChI_CHARGE, InChI_FIXEDH, InChI_ISOTO
```

## PdbxChemCompFeature
```text
  ├── comp_id : String  # The component identifier for this feature.  Examples: ABC, ATP
  ├── source : String  # The information source for the component feature.  Examples: PDB, CHEBI, DRUGBANK, PUBCHEM
  ├── type : String  # The component feature type.  Allowable values: CARBOHYDRATE ANOMER, CARBOHYDRATE ISOMER, CARBOHYDRATE PRIMARY CARBONYL G
  ├── value : String  # The component feature value.
```

## PdbxChemCompIdentifier
```text
  ├── comp_id : String  # This data item is a pointer to _chem_comp.id in the CHEM_COMP  category.
  ├── identifier : String?  # This data item contains the identifier value for this  component.
  ├── program : String  # This data item contains the name of the program  or library used to compute the identifier.  Examples: OPENEYE, DAYLIGHT
  ├── program_version : String  # This data item contains the version of the program  or library used to compute the identifier.
  ├── type : String  # This data item contains the identifier type.  Allowable values: CAS REGISTRY NUMBER, COMMON NAME, CONDENSED IUPAC CARB S
```

## PdbxDatabasePDBObsSpr
```text
  ├── date : Date?  # The date of replacement.  Examples: 1997-03-30
  ├── details : String?  # Details related to the replaced or replacing entry.
  ├── id : String?  # Identifier for the type of obsolete entry to be added to this entry.  Allowable values: OBSLTE, SPRSDE
  ├── pdb_id : String  # The new PDB identifier for the replaced entry.  Examples: 2ABC
  ├── replace_pdb_id : String  # The PDB identifier for the replaced (OLD) entry/entries.  Examples: 3ABC
```

## PdbxDatabaseRelated
```text
  ├── content_type : String  # The identifying content type of the related entry.  Allowable values: associated EM volume, associated NMR restraints, a
  ├── db_id : String  # The identifying code in the related database.  Examples: 1ABC, BDL001
  ├── db_name : String  # The name of the database containing the related entry.  Allowable values: BIOISIS, BMCD, BMRB, EMDB, NDB, PDB, PDB-Dev, 
  ├── details : String?  # A description of the related entry.  Examples: 1ABC contains the same protein complexed with Netropsin.
```

## PdbxDatabaseStatus
```text
  ├── SG_entry : String?  # This code indicates whether the entry belongs to  Structural Genomics Project.  Allowable values: N, Y
  ├── deposit_site : String?  # The site where the file was deposited.  Allowable values: BMRB, BNL, NDB, PDBC, PDBE, PDBJ, RCSB
  ├── methods_development_category : String?  # The methods development category in which this  entry has been placed.  Allowable values: CAPRI, CASD-NMR, CASP, D3R, Fo
  ├── pdb_format_compatible : String?  # A flag indicating that the entry is compatible with the PDB format.   A value of 'N' indicates that the no PDB format da
  ├── process_site : String?  # The site where the file was deposited.  Allowable values: BNL, NDB, PDBC, PDBE, PDBJ, RCSB
  ├── recvd_initial_deposition_date : Date?  # The date of initial deposition.  (The first message for  deposition has been received.)  Examples: 1983-02-21
  ├── status_code : String?  # Code for status of file.  Allowable values: AUCO, AUTH, BIB, DEL, HOLD, HPUB, OBS, POLC, PROC, REFI, REL, REPL, REV, RMV
  ├── status_code_cs : String?  # Code for status of chemical shift data file.  Allowable values: AUCO, AUTH, HOLD, HPUB, OBS, POLC, PROC, REL, REPL, RMVD
  ├── status_code_mr : String?  # Code for status of NMR constraints file.  Allowable values: AUCO, AUTH, HOLD, HPUB, OBS, POLC, PROC, REL, REPL, RMVD, WA
  ├── status_code_sf : String?  # Code for status of structure factor file.  Allowable values: AUTH, HOLD, HPUB, OBS, POLC, PROC, REL, REPL, RMVD, WAIT, W
```

## PdbxDepositGroup
```text
  ├── group_description : String?  # A description of the contents of entries in the collection.
  ├── group_id : String  # A unique identifier for a group of entries deposited as a collection.  Examples: G_1002119, G_1002043
  ├── group_title : String?  # A title to describe the group of entries deposited in the collection.
  ├── group_type : String?  # Text to describe a grouping of entries in multiple collections  Allowable values: changed state, ground state, undefined
```

## PdbxEntityBranch
```text
  ├── rcsb_branched_component_count : Int?  # Number of constituent chemical components in the branched entity.
  ├── type : String?  # The type of this branched oligosaccharide.  Allowable values: oligosaccharide
```

## PdbxEntityBranchDescriptor
```text
  ├── descriptor : String?  # This data item contains the descriptor value for this  entity.
  ├── program : String?  # This data item contains the name of the program  or library used to compute the descriptor.  Examples: PDB-CARE, OTHER, 
  ├── program_version : String?  # This data item contains the version of the program  or library used to compute the descriptor.
  ├── type : String?  # This data item contains the descriptor type.  Allowable values: Glycam Condensed Core Sequence, Glycam Condensed Sequenc
```

## PdbxEntityNonpoly
```text
  ├── comp_id : String?  # This data item is a pointer to _chem_comp.id in the CHEM_COMP category.
  ├── entity_id : String  # This data item is a pointer to _entity.id in the ENTITY category.
  ├── name : String?  # A name for the non-polymer entity
  ├── rcsb_prd_id : String?  # For non-polymer BIRD molecules the BIRD identifier for the entity.
```

## PdbxEntitySrcSyn
```text
  ├── details : String?  # A description of special aspects of the source for the  synthetic entity.  Examples: This sequence occurs naturally in h
  ├── ncbi_taxonomy_id : String?  # NCBI Taxonomy identifier of the organism from which the sequence of  the synthetic entity was derived.   Reference:   Wh
  ├── organism_common_name : String?  # The common name of the organism from which the sequence of  the synthetic entity was derived.  Examples: house mouse
  ├── organism_scientific : String?  # The scientific name of the organism from which the sequence of  the synthetic entity was derived.  Examples: synthetic c
  ├── pdbx_alt_source_flag : String?  # This data item identifies cases in which an alternative source  modeled.  Allowable values: model, sample
  ├── pdbx_beg_seq_num : Int?  # The beginning polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequ
  ├── pdbx_end_seq_num : Int?  # The ending polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequenc
  ├── pdbx_src_id : Int  # This data item is an ordinal identifier for pdbx_entity_src_syn data records.
```

## PdbxFamilyPrdAudit
```text
  ├── action_type : String  # The action associated with this audit record.  Allowable values: Add PRD, Create family, Initial release, Modify annotat
  ├── annotator : String?  # The initials of the annotator creating of modifying the family.  Examples: JO, SJ, KB
  ├── date : Date  # The date associated with this audit record.
  ├── details : String?  # Additional details decribing this change.  Examples: Revise molecule sequence.
  ├── family_prd_id : String  # This data item is a pointer to _pdbx_reference_molecule_family.family_prd_id in the 	       pdbx_reference_molecule cate
  ├── processing_site : String?  # An identifier for the wwPDB site creating or modifying the family.  Examples: RCSB, PDBE, PDBJ, BMRB, PDBC
```

## PdbxInitialRefinementModel
```text
  ├── accession_code : String?  # This item identifies an accession code of the resource where the initial model  is used
  ├── details : String?  # A description of special aspects of the initial model
  ├── entity_id_list : String[]?  # A comma separated list of entities reflecting the initial model used for refinement
  ├── id : Int  # A unique identifier for the starting model record.
  ├── source_name : String?  # This item identifies the resource of initial model used for refinement  Allowable values: AlphaFold, ITasser, InsightII,
  ├── type : String?  # This item describes the type of the initial model was generated  Allowable values: experimental model, in silico model, 
```

## PdbxMoleculeFeatures
```text
  ├── class : String?  # Broadly defines the function of the molecule.  Allowable values: Antagonist, Anthelmintic, Antibiotic, Antibiotic, Anthe
  ├── details : String?  # Additional details describing the molecule.
  ├── name : String?  # A name of the molecule.  Examples: thiostrepton
  ├── prd_id : String  # The value of _pdbx_molecule_features.prd_id is the accession code for this  reference molecule.
  ├── type : String?  # Defines the structural classification of the molecule.  Allowable values: Amino acid, Aminoglycoside, Ansamycin, Anthrac
```

## PdbxNmrDetails
```text
  ├── text : String?  # Additional details describing the NMR experiment.  Examples: This structure was determined using standard 2D homonuclear
```

## PdbxNmrEnsemble
```text
  ├── average_constraint_violations_per_residue : Int?  # The average number of constraint violations on a per residue basis for  the ensemble.  Examples: null
  ├── average_constraints_per_residue : Int?  # The average number of constraints per residue for the ensemble  Examples: null
  ├── average_distance_constraint_violation : Float?  # The average distance restraint violation for the ensemble.  Examples: null
  ├── average_torsion_angle_constraint_violation : Float?  # The average torsion angle constraint violation for the ensemble.  Examples: null
  ├── conformer_selection_criteria : String?  # By highlighting the appropriate choice(s), describe how the submitted conformer (models) were selected.  Examples: struc
  ├── conformers_calculated_total_number : Int?  # The total number of conformer (models) that were calculated in the final round.
  ├── conformers_submitted_total_number : Int?  # The number of conformer (models) that are submitted for the ensemble.
  ├── distance_constraint_violation_method : String?  # Describe the method used to calculate the distance constraint violation statistics,  i.e. are they calculated over all t
  ├── maximum_distance_constraint_violation : Float?  # The maximum distance constraint violation for the ensemble.  Examples: null
  ├── maximum_lower_distance_constraint_violation : Float?  # The maximum lower distance constraint violation for the ensemble.  Examples: null
  ├── maximum_torsion_angle_constraint_violation : Float?  # The maximum torsion angle constraint violation for the ensemble.
  ├── maximum_upper_distance_constraint_violation : Float?  # The maximum upper distance constraint violation for the ensemble.  Examples: null
  ├── representative_conformer : Int?  # The number of the conformer identified as most representative.
  ├── torsion_angle_constraint_violation_method : String?  # This item describes the method used to calculate the torsion angle constraint violation statistics. i.e. are the entered
```

## PdbxNmrExptl
```text
  ├── conditions_id : String  # The number to identify the set of sample conditions.  Examples: 1, 2, 3
  ├── experiment_id : String  # A numerical ID for each experiment.  Examples: 1, 2, 3
  ├── sample_state : String?  # Physical state of the sample either anisotropic or isotropic.  Allowable values: anisotropic, isotropic
  ├── solution_id : String  # The solution_id from the Experimental Sample to identify the sample  that these conditions refer to.   [Remember to save
  ├── spectrometer_id : Int?  # Pointer to '_pdbx_nmr_spectrometer.spectrometer_id'
  ├── type : String?  # The type of NMR experiment.  Examples: 2D NOESY, 3D_15N-separated_NOESY, 3D_13C-separated_NOESY, 4D_13C-separated_NOESY,
```

## PdbxNmrExptlSampleConditions
```text
  ├── conditions_id : String  # The condition number as defined above.  Examples: 1, 2, 3
  ├── details : String?  # General details describing conditions of both the sample and the environment during measurements.  Examples: The high sa
  ├── ionic_strength : String?  # The ionic strength at which the NMR data were collected -in lieu of  this enter the concentration and identity of the sa
  ├── ionic_strength_err : Float?  # Estimate of the standard error for the value for the sample ionic strength.  Examples: null
  ├── ionic_strength_units : String?  # Units for the value of the sample condition ionic strength..  Allowable values: M, Not defined, mM
  ├── label : String?  # A descriptive label that uniquely identifies this set of sample conditions.  Examples: conditions_1
  ├── pH : String?  # The pH at which the NMR data were collected.  Examples: null, null
  ├── pH_err : Float?  # Estimate of the standard error for the value for the sample pH.  Examples: null
  ├── pH_units : String?  # Units for the value of the sample condition pH.  Allowable values: Not defined, pD, pH, pH*
  ├── pressure : String?  # The pressure at which NMR data were collected.  Examples: 1, ambient, 1atm
  ├── pressure_err : Float?  # Estimate of the standard error for the value for the sample pressure.  Examples: null
  ├── pressure_units : String?  # The units of pressure at which NMR data were collected.  Examples: Pa, atm, Torr
  ├── temperature : String?  # The temperature (in kelvin) at which NMR data were  collected.
  ├── temperature_err : Float?  # Estimate of the standard error for the value for the sample temperature.  Examples: null
  ├── temperature_units : String?  # Units for the value of the sample condition temperature.  Allowable values: C, K, Not defined
```

## PdbxNmrRefine
```text
  ├── details : String?  # Additional details about the NMR refinement.  Examples: Additional comments about the NMR refinement can be placed here,
  ├── method : String?  # The method used to determine the structure.  Examples: simulated annealing, distance geometry   simulated annealing   mo
  ├── software_ordinal : Int  # Pointer to _software.ordinal
```

## PdbxNmrRepresentative
```text
  ├── conformer_id : String?  # If a member of the ensemble has been selected as a representative  structure, identify it by its model number.  Examples
  ├── selection_criteria : String?  # By highlighting the appropriate choice(s), describe the criteria used to select this structure as a representative struc
```

## PdbxNmrSampleDetails
```text
  ├── contents : String?  # A complete description of each NMR sample. Include the concentration and concentration units for each component (include
  ├── details : String?  # Brief description of the sample providing additional information not captured by other items in the category.  Examples:
  ├── label : String?  # A value that uniquely identifies this sample from the other samples listed in the entry.  Examples: 15N_sample
  ├── solution_id : String  # The name (number) of the sample.  Examples: 1, 2, 3
  ├── solvent_system : String?  # The solvent system used for this sample.  Examples: 90% H2O, 10% D2O
  ├── type : String?  # A descriptive term for the sample that defines the general physical properties of the sample.  Allowable values: bicelle
```

## PdbxNmrSoftware
```text
  ├── authors : String?  # The name of the authors of the software used in this  procedure.  Examples: Brunger, Guentert
  ├── classification : String?  # The purpose of the software.  Examples: collection, processing, data analysis, structure solution, refinement, iterative
  ├── name : String?  # The name of the software used for the task.  Examples: ANSIG, AURELIA, AZARA, CHARMM, CoMAND, CORMA, DIANA, DYANA, DSPAC
  ├── ordinal : Int  # An ordinal index for this category
  ├── version : String?  # The version of the software.  Examples: 940501.3, 2.1
```

## PdbxNmrSpectrometer
```text
  ├── details : String?  # A text description of the NMR spectrometer.
  ├── field_strength : Float?  # The field strength in MHz of the spectrometer
  ├── manufacturer : String?  # The name of the manufacturer of the spectrometer.  Examples: Varian, Bruker, JEOL, GE
  ├── model : String?  # The model of the NMR spectrometer.  Examples: AVANCE, AVANCE II, AVANCE III, AVANCE III HD, WH, WM, AC+, Alpha, AM, AMX,
  ├── spectrometer_id : String  # Assign a numerical ID to each instrument.  Examples: 1, 2, 3
  ├── type : String?  # Select the instrument manufacturer(s) and the model(s) of the NMR(s) used for this work.  Examples: Bruker WH, Bruker WM
```

## PdbxPrdAudit
```text
  ├── action_type : String  # The action associated with this audit record.  Allowable values: Create molecule, Initial release, Modify audit, Modify 
  ├── annotator : String?  # The initials of the annotator creating of modifying the molecule.  Examples: JO, SJ, KB
  ├── date : Date  # The date associated with this audit record.
  ├── details : String?  # Additional details decribing this change.  Examples: Revise molecule sequence.
  ├── prd_id : String  # This data item is a pointer to _pdbx_reference_molecule.prd_id in the 	       pdbx_reference_molecule category.
  ├── processing_site : String?  # An identifier for the wwPDB site creating or modifying the molecule.  Allowable values: BMRB, PDBC, PDBE, PDBJ, RCSB
```

## PdbxReferenceEntityList
```text
  ├── component_id : Int  # The component number of this entity within the molecule.
  ├── details : String?  # Additional details about this entity.
  ├── prd_id : String  # The value of _pdbx_reference_entity_list.prd_id is a reference  _pdbx_reference_molecule.prd_id in the PDBX_REFERENCE_MO
  ├── ref_entity_id : String  # The value of _pdbx_reference_entity_list.ref_entity_id is a unique identifier  the a constituent entity within this refe
  ├── type : String?  # Defines the polymer characteristic of the entity.  Allowable values: branched, non-polymer, polymer, polymer-like
```

## PdbxReferenceEntityPoly
```text
  ├── db_code : String?  # The database code for this source information
  ├── db_name : String?  # The database name for this source information
  ├── prd_id : String  # The value of _pdbx_reference_entity_poly.prd_id is a reference 	       _pdbx_reference_entity_list.prd_id in the  PDBX_R
  ├── ref_entity_id : String  # The value of _pdbx_reference_entity_poly.ref_entity_id is a reference  to _pdbx_reference_entity_list.ref_entity_id in P
  ├── type : String?  # The type of the polymer.  Allowable values: nucleic-acid-like, oligosaccharide, peptide-like, polysaccharide-like
```

## PdbxReferenceEntityPolyLink
```text
  ├── atom_id_1 : String?  # The atom identifier/name in the first of the two components making  the linkage.
  ├── atom_id_2 : String?  # The atom identifier/name in the second of the two components making  the linkage.
  ├── comp_id_1 : String?  # The component identifier in the first of the two components making the  linkage.   This data item is a pointer to _pdbx_
  ├── comp_id_2 : String?  # The component identifier in the second of the two components making the  linkage.   This data item is a pointer to _pdbx
  ├── component_id : Int  # The entity component identifier entity containing the linkage.
  ├── entity_seq_num_1 : Int?  # For a polymer entity, the sequence number in the first of  the two components making the linkage.   This data item is a 
  ├── entity_seq_num_2 : Int?  # For a polymer entity, the sequence number in the second of  the two components making the linkage.   This data item is a
  ├── link_id : Int  # The value of _pdbx_reference_entity_poly_link.link_id uniquely identifies  a linkage within a polymer entity.
  ├── prd_id : String  # The value of _pdbx_reference_entity_poly_link.prd_id is a reference  _pdbx_reference_entity_list.prd_id in the PDBX_REFE
  ├── ref_entity_id : String  # The reference entity id of the polymer entity containing the linkage.   This data item is a pointer to _pdbx_reference_e
  ├── value_order : String?  # The bond order target for the non-standard linkage.  Allowable values: arom, delo, doub, pi, poly, quad, sing, trip
```

## PdbxReferenceEntityPolySeq
```text
  ├── hetero : String  # A flag to indicate that sequence heterogeneity at this monomer position.  Allowable values: N, Y
  ├── mon_id : String  # This data item is the chemical component identifier of monomer.
  ├── num : Int  # The value of _pdbx_reference_entity_poly_seq.num must uniquely and sequentially  identify a record in the PDBX_REFERENCE
  ├── observed : String?  # A flag to indicate that this monomer is observed in the instance example.  Allowable values: N, Y
  ├── parent_mon_id : String?  # This data item is the chemical component identifier for the parent component corresponding to this monomer.
  ├── prd_id : String  # The value of _pdbx_reference_entity_poly_seq.prd_id is a reference 	       _pdbx_reference_entity_poly.prd_id in the  PD
  ├── ref_entity_id : String  # The value of _pdbx_reference_entity_poly_seq.ref_entity_id is a reference  to _pdbx_reference_entity_poly.ref_entity_id 
```

## PdbxReferenceEntitySequence
```text
  ├── NRP_flag : String?  # A flag to indicate a non-ribosomal entity.  Allowable values: N, Y
  ├── one_letter_codes : String?  # The one-letter-code sequence for this entity.  Non-standard monomers are represented as 'X'.
  ├── prd_id : String  # The value of _pdbx_reference_entity_sequence.prd_id is a reference 	       _pdbx_reference_entity_list.prd_id in the  PD
  ├── ref_entity_id : String  # The value of _pdbx_reference_entity_sequence.ref_entity_id is a reference  to _pdbx_reference_entity_list.ref_entity_id 
  ├── type : String?  # The monomer type for the sequence.  Allowable values: peptide-like, saccharide
```

## PdbxReferenceEntitySrcNat
```text
  ├── atcc : String?  # The Americal Tissue Culture Collection code for organism from which the entity was isolated.
  ├── db_code : String?  # The database code for this source information
  ├── db_name : String?  # The database name for this source information
  ├── ordinal : Int  # The value of _pdbx_reference_entity_src_nat.ordinal distinguishes 	       source details for this entity.
  ├── organism_scientific : String?  # The scientific name of the organism from which the entity was isolated.  Examples: Mus musculus
  ├── prd_id : String  # The value of _pdbx_reference_entity_src_nat.prd_id is a reference 	       _pdbx_reference_entity_list.prd_id in the  PDB
  ├── ref_entity_id : String  # The value of _pdbx_reference_entity_src_nat.ref_entity_id is a reference  to _pdbx_reference_entity_list.ref_entity_id i
  ├── source : String?  # The data source for this information.
  ├── source_id : String?  # A identifier within the data source for this information.
  ├── taxid : String?  # The NCBI TaxId of the organism from which the entity was isolated.
```

## PdbxReferenceMolecule
```text
  ├── chem_comp_id : String?  # For entities represented as single molecules, the identifier  corresponding to the chemical definition for the molecule.
  ├── class : String?  # Broadly defines the function of the entity.  Allowable values: Antagonist, Anthelmintic, Antibiotic, Antibiotic, Anthelm
  ├── class_evidence_code : String?  # Evidence for the assignment of _pdbx_reference_molecule.class
  ├── compound_details : String?  # Special details about this molecule.
  ├── description : String?  # Description of this molecule.
  ├── formula : String?  # The formula for the reference entity. Formulae are written  according to the rules:   1. Only recognised element symbols
  ├── formula_weight : Float?  # Formula mass in daltons of the entity.
  ├── name : String?  # A name of the entity.  Examples: thiostrepton
  ├── prd_id : String  # The value of _pdbx_reference_molecule.prd_id is the unique identifier  for the reference molecule in this family.   By c
  ├── release_status : String?  # Defines the current PDB release status for this molecule definition.  Allowable values: HOLD, OBS, REL, WAIT
  ├── replaced_by : String?  # Assigns the identifier of the reference molecule that has replaced this molecule.
  ├── replaces : String?  # Assigns the identifier for the reference molecule which have been replaced  by this reference molecule.  Multiple molecu
  ├── represent_as : String?  # Defines how this entity is represented in PDB data files.  Allowable values: branched, polymer, single molecule
  ├── representative_PDB_id_code : String?  # The PDB accession code for the entry containing a representative example of this molecule.
  ├── type : String?  # Defines the structural classification of the entity.  Allowable values: Amino acid, Aminoglycoside, Ansamycin, Anthracyc
  ├── type_evidence_code : String?  # Evidence for the assignment of _pdbx_reference_molecule.type
```

## PdbxReferenceMoleculeAnnotation
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_annotation.family_prd_id is a reference to  _pdbx_reference_molecule_list.family_p
  ├── ordinal : Int  # This data item distinguishes anotations for this entity.
  ├── prd_id : String?  # This data item is a pointer to _pdbx_reference_molecule.prd_id in the  PDB_REFERENCE_MOLECULE category.
  ├── source : String?  # The source of the annoation for this entity.  Examples: depositor provided, from UniProt Entry P200311
  ├── text : String?  # Text describing the annotation for this entity.  Examples: antigen binding, glucose transporter activity
  ├── type : String?  # Type of annotation for this entity.  Examples: Function, Use, Pharmacology, Mechanism_of_Action, Biological_Activity, In
```

## PdbxReferenceMoleculeDetails
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_details.family_prd_id is a reference to  _pdbx_reference_molecule_list.family_prd_
  ├── ordinal : Int  # The value of _pdbx_reference_molecule_details.ordinal is an ordinal that  distinguishes each descriptive text for this e
  ├── source : String?  # A data source of this information (e.g. PubMed, Merck Index)
  ├── source_id : String?  # A identifier within the data source for this information.
  ├── text : String?  # The text of the description of special aspects of the entity.
```

## PdbxReferenceMoleculeFamily
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_entity.family_prd_id must uniquely identify a record in the  PDBX_REFERENCE_MOLECULE_FAMILY
  ├── name : String?  # The entity family name.  Examples: actinomycin, adriamycin
  ├── release_status : String?  # Assigns the current PDB release status for this family.  Allowable values: HOLD, OBS, REL, WAIT
  ├── replaced_by : String?  # Assigns the identifier of the family that has replaced this component.
  ├── replaces : String?  # Assigns the identifier for the family which have been replaced by this family.  Multiple family identifier codes should 
```

## PdbxReferenceMoleculeFeatures
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_features.family_prd_id is a reference to  _pdbx_reference_molecule_list.family_prd
  ├── ordinal : Int  # The value of _pdbx_reference_molecule_features.ordinal distinguishes 	       each feature for this entity.
  ├── prd_id : String  # The value of _pdbx_reference_molecule_features.prd_id is a reference 	       _pdbx_reference_molecule.prd_id in the  PDB
  ├── source : String?  # The information source for the component feature.  Examples: PDB, CHEBI, DRUGBANK, PUBCHEM
  ├── source_ordinal : Int?  # The value of _pdbx_reference_molecule_features.source_ordinal provides 	       the priority order of features from a par
  ├── type : String?  # The entity feature type.  Examples: FUNCTION, ENZYME INHIBITED, STRUCTURE IMAGE URL
  ├── value : String?  # The entity feature value.
```

## PdbxReferenceMoleculeList
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_list.family_prd_id is a reference to  _pdbx_reference_molecule_family.family_prd_i
  ├── prd_id : String  # The value of _pdbx_reference_molecule_list.prd_id is the unique identifier  for the reference molecule in this family.  
```

## PdbxReferenceMoleculeRelatedStructures
```text
  ├── citation_id : String?  # A link to related reference information in the citation category.
  ├── db_accession : String?  # The database accession code for the related structure reference.  Examples: 143108
  ├── db_code : String?  # The database identifier code for the related structure reference.  Examples: QEFHUE
  ├── db_name : String?  # The database name for the related structure reference.  Examples: CCDC
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_related_structures.family_prd_id is a reference to  _pdbx_reference_molecule_list.
  ├── formula : String?  # The formula for the reference entity. Formulae are written  according to the rules:   1. Only recognised element symbols
  ├── name : String?  # The chemical name for the structure entry in the related database  Examples: actinomycn
  ├── ordinal : Int  # The value of _pdbx_reference_molecule_related_structures.ordinal distinguishes  related structural data for each entity.
```

## PdbxReferenceMoleculeSynonyms
```text
  ├── family_prd_id : String  # The value of _pdbx_reference_molecule_synonyms.family_prd_id is a reference to  _pdbx_reference_molecule_list.family_prd
  ├── name : String?  # A synonym name for the entity.  Examples: thiostrepton
  ├── ordinal : Int  # The value of _pdbx_reference_molecule_synonyms.ordinal is an ordinal 	       to distinguish synonyms for this entity.
  ├── prd_id : String  # The value of _pdbx_reference_molecule_synonyms.prd_id is a reference 	       _pdbx_reference_molecule.prd_id in the  PDB
  ├── source : String?  # The source of this synonym name for the entity.  Examples: CAS
```

## PdbxReflnsTwin
```text
  ├── crystal_id : String  # The crystal identifier.  A reference to  _exptl_crystal.id in category EXPTL_CRYSTAL.
  ├── diffrn_id : String  # The diffraction data set identifier.  A reference to  _diffrn.id in category DIFFRN.
  ├── domain_id : String?  # An identifier for the twin domain.
  ├── fraction : Float?  # The twin fraction or twin factor represents a quantitative parameter for the crystal twinning.  The value 0 represents n
  ├── operator : String  # The possible merohedral or hemihedral twinning operators for different point groups are:  True point group  	Twin operat
  ├── type : String?  # There are two types of twinning: merohedral or hemihedral                                  non-merohedral or epitaxial  
```

## PdbxRelatedExpDataSet
```text
  ├── data_reference : String?  # A DOI reference to the related data set.  Examples: 10.000/10002/image_data/cif
  ├── data_set_type : String?  # The type of the experimenatal data set.  Examples: diffraction image data, NMR free induction decay data
  ├── db_source : String?  # For external sources, the name of the resource.  Allowable values: Apollo - University of Cambridge Repository, CXIDB, D
  ├── details : String?  # Additional details describing the content of the related data set and its application to  the current investigation.
  ├── metadata_reference : String?  # A DOI reference to the metadata decribing the related data set.  Examples: 10.000/10002/image_data/txt
```

## PdbxSGProject
```text
  ├── full_name_of_center : String?  # The value identifies the full name of center.  Allowable values: Accelerated Technologies Center for Gene to 3D Structur
  ├── id : Int  # A unique integer identifier for this center  Allowable values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
  ├── initial_of_center : String?  # The value identifies the full name of center.  Allowable values: ATCG3D, BIGS, BSGC, BSGI, CEBS, CELLMAT, CESG, CHSAM, C
  ├── project_name : String?  # The value identifies the Structural Genomics project.  Allowable values: Enzyme Function Initiative, NIAID, National Ins
```

## PdbxSerialCrystallographyDataReduction
```text
  ├── crystal_hits : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of frames collected  in which th
  ├── diffrn_id : String  # The data item is a pointer to _diffrn.id in the DIFFRN  category.  Examples: 1
  ├── droplet_hits : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of frames collected  in which a 
  ├── frame_hits : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of data frames collected  in whi
  ├── frames_failed_index : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of data frames collected  that c
  ├── frames_indexed : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of data frames collected  that w
  ├── frames_total : Int?  # The total number of data frames collected for this  data set.
  ├── lattices_indexed : Int?  # For experiments in which samples are provided in a  continuous stream, the total number of lattices indexed.
  ├── lattices_merged : Int?  # For experiments in which samples are provided in a             continuous stream, the total number of crystal lattices  
  ├── xfel_pulse_events : Int?  # For FEL experiments, the number of pulse events in the dataset.
  ├── xfel_run_numbers : String?  # For FEL experiments, in which data collection was performed 	       in batches, indicates which subset of the data colle
```

## PdbxSerialCrystallographyMeasurement
```text
  ├── collection_time_total : Float?  # The total number of hours required to measure this data set.  Examples: null
  ├── collimation : String?  # The collimation or type of focusing optics applied to the radiation.  Examples: Kirkpatrick-Baez mirrors, Beryllium comp
  ├── diffrn_id : String  # The data item is a pointer to _diffrn.id in the DIFFRN  category.  Examples: 1
  ├── focal_spot_size : Float?  # The focal spot size of the beam  impinging on the sample (micrometres squared).
  ├── photons_per_pulse : Float?  # The photons per pulse measured in  (tera photons (10^(12)^)/pulse units).
  ├── pulse_duration : Float?  # The average duration (femtoseconds) 	       of the pulse energy measured at the sample.
  ├── pulse_energy : Float?  # The energy/pulse of the X-ray pulse impacting the sample measured in microjoules.
  ├── pulse_photon_energy : Float?  # The photon energy of the X-ray pulse measured in KeV.
  ├── source_distance : Float?  # The distance from source to the sample along the optical axis (metres).
  ├── source_size : Float?  # The dimension of the source beam measured at the source (micrometres squared).
  ├── xfel_pulse_repetition_rate : Float?  # For FEL experiments, the pulse repetition rate measured in cycles per seconds.
```

## PdbxSerialCrystallographySampleDelivery
```text
  ├── description : String?  # The description of the mechanism by which the specimen in placed in the path  of the source.  Examples: fixed target, el
  ├── diffrn_id : String  # The data item is a pointer to _diffrn.id in the DIFFRN  category.  Examples: 1
  ├── method : String?  # The description of the mechanism by which the specimen in placed in the path  of the source.  Allowable values: fixed ta
```

## PdbxSerialCrystallographySampleDeliveryFixedTarget
```text
  ├── crystals_per_unit : Int?  # The number of crystals per dropplet or pore in fixed target
  ├── description : String?  # For a fixed target sample, a description of sample preparation
  ├── details : String?  # Any details pertinent to the fixed sample target
  ├── diffrn_id : String  # The data item is a pointer to _diffrn.id in the DIFFRN  category.  Examples: 1
  ├── motion_control : String?  # Device used to control movement of the fixed sample  Examples: DMC-4080
  ├── sample_dehydration_prevention : String?  # Method to prevent dehydration of sample  Examples: seal, humidifed gas, flash freezing
  ├── sample_holding : String?  # For a fixed target sample, mechanism to hold sample in the beam  Examples: mesh, loop, grid
  ├── sample_solvent : String?  # The sample solution content and concentration
  ├── sample_unit_size : Float?  # Size of pore in grid supporting sample. Diameter or length in micrometres,  e.g. pore diameter
  ├── support_base : String?  # Type of base holding the support  Examples: goniometer
  ├── velocity_horizontal : Float?  # Velocity of sample horizontally relative to a perpendicular beam in millimetres/second
  ├── velocity_vertical : Float?  # Velocity of sample vertically relative to a perpendicular beam in millimetres/second
```

## PdbxSerialCrystallographySampleDeliveryInjection
```text
  ├── carrier_solvent : String?  # For continuous sample flow experiments, the carrier buffer used  to move the sample into the beam. Should include protei
  ├── crystal_concentration : Float?  # For continuous sample flow experiments, the concentration of  crystals in the solution being injected.   The concentrati
  ├── description : String?  # For continuous sample flow experiments, a description of the injector used  to move the sample into the beam.  Examples:
  ├── diffrn_id : String  # The data item is a pointer to _diffrn.id in the DIFFRN  category.  Examples: 1
  ├── filter_size : Float?  # The size of filter in micrometres in filtering crystals
  ├── flow_rate : Float?  # For continuous sample flow experiments, the flow rate of  solution being injected  measured in ul/min.
  ├── injector_diameter : Float?  # For continuous sample flow experiments, the diameter of the  injector in micrometres.
  ├── injector_nozzle : String?  # The type of nozzle to deliver and focus sample jet  Examples: gas, GDVN
  ├── injector_pressure : Float?  # For continuous sample flow experiments, the mean pressure  in kilopascals at which the sample is injected into the beam.
  ├── injector_temperature : Float?  # For continuous sample flow experiments, the temperature in  Kelvins of the speciman injected. This may be different from
  ├── jet_diameter : Float?  # Diameter in micrometres of jet stream of sample delivery
  ├── power_by : String?  # Sample deliver driving force, e.g. Gas, Electronic Potential  Examples: syringe, gas, electronic potential
  ├── preparation : String?  # Details of crystal growth and preparation of the crystals  Examples: Crystals transfered to carrier solvent at room temp
```

## PdbxSolnScatter
```text
  ├── buffer_name : String?  # The name of the buffer used for the sample in the solution scattering  experiment.  Examples: acetic acid
  ├── concentration_range : String?  # The concentration range (mg/mL) of the complex in the  sample used in the solution scattering experiment to  determine t
  ├── data_analysis_software_list : String?  # A list of the software used in the data analysis  Examples: SCTPL5 GNOM
  ├── data_reduction_software_list : String?  # A list of the software used in the data reduction  Examples: OTOKO
  ├── detector_specific : String?  # The particular radiation detector. In general this will be a   manufacturer, description, model number or some combinati
  ├── detector_type : String?  # The general class of the radiation detector.
  ├── id : String  # The value of _pdbx_soln_scatter.id must  uniquely identify the sample in the category PDBX_SOLN_SCATTER
  ├── max_mean_cross_sectional_radii_gyration : Float?  # The maximum mean radius of structural elongation of the sample.  In a given solute-solvent contrast, the radius of gyrat
  ├── max_mean_cross_sectional_radii_gyration_esd : Float?  # The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-s
  ├── mean_guiner_radius : Float?  # The mean radius of structural elongation of the sample.  In a given solute-solvent contrast, the radius of gyration  R_G
  ├── mean_guiner_radius_esd : Float?  # The estimated standard deviation for the  mean radius of structural elongation of the sample.  In a given solute-solvent
  ├── min_mean_cross_sectional_radii_gyration : Float?  # The minimum mean radius of structural elongation of the sample. In a given solute-solvent contrast, the radius of gyrati
  ├── min_mean_cross_sectional_radii_gyration_esd : Float?  # The estimated standard deviation for the minimum mean radius of structural elongation of the sample. In a given solute-s
  ├── num_time_frames : Int?  # The number of time frame solution scattering images used.
  ├── protein_length : String?  # The length (or range) of the protein sample under study. If the solution structure is approximated as an elongated ellip
  ├── sample_pH : Float?  # The pH value of the buffered sample.
  ├── source_beamline : String?  # The beamline name used for the experiment
  ├── source_beamline_instrument : String?  # The instrumentation used on the beamline
  ├── source_class : String?  # The general class of the radiation source.  Examples: neutron source, synchrotron
  ├── source_type : String?  # The make, model, name or beamline of the source of radiation.
  ├── temperature : Float?  # The temperature in kelvins at which the experiment  was conducted
  ├── type : String?  # The type of solution scattering experiment carried out  Allowable values: modelling, neutron, x-ray
```

## PdbxSolnScatterModel
```text
  ├── conformer_selection_criteria : String?  # A description of the conformer selection criteria  used.  Examples: The modelled scattering curves were assessed by calc
  ├── details : String?  # A description of any additional details concerning the experiment.  Examples: Homology models were built for     the 17 
  ├── entry_fitting_list : String?  # A list of the entries used to fit the model  to the scattering data  Examples: PDB CODE 1HFI, 1HCC, 1HFH, 1VCC
  ├── id : String  # The value of _pdbx_soln_scatter_model.id must  uniquely identify the sample in the category PDBX_SOLN_SCATTER_MODEL
  ├── method : String?  # A description of the methods used in the modelling  Examples: Constrained scattering fitting of homology models
  ├── num_conformers_calculated : Int?  # The number of model conformers calculated.
  ├── num_conformers_submitted : Int?  # The number of model conformers submitted in the entry
  ├── representative_conformer : Int?  # The index of the representative conformer among the submitted conformers for the entry
  ├── scatter_id : String  # This data item is a pointer to  _pdbx_soln_scatter.id in the  PDBX_SOLN_SCATTER category.
  ├── software_author_list : String?  # A list of the software authors  Examples: MSI
  ├── software_list : String?  # A list of the software used in the modeeling  Examples: INSIGHT II, HOMOLOGY, DISCOVERY, BIOPOLYMER, DELPHI
```

## PdbxStructAssembly
```text
  ├── details : String?  # A description of special aspects of the macromolecular assembly.                 In the PDB, 'representative helical ass
  ├── id : String  # The value of _pdbx_struct_assembly.id must uniquely identify a record in  the PDBX_STRUCT_ASSEMBLY list.
  ├── method_details : String?  # Provides details of the method used to determine or  compute the assembly.
  ├── oligomeric_count : Int?  # The number of polymer molecules in the assembly.
  ├── oligomeric_details : String?  # Provides the details of the oligomeric state of the assembly.  Examples: monomer, octameric, tetradecameric, eicosameric
  ├── rcsb_candidate_assembly : String?  # Candidate macromolecular assembly.   Excludes the following cases classified in pdbx_struct_asembly.details:   'crystal 
  ├── rcsb_details : String?  # A filtered description of the macromolecular assembly.  Allowable values: author_and_software_defined_assembly, author_d
```

## PdbxStructAssemblyAuthEvidence
```text
  ├── assembly_id : String  # This item references an assembly in pdbx_struct_assembly
  ├── details : String?  # Provides any additional information regarding the evidence of this assembly  Examples: Homology to bacteriorhodopsin, He
  ├── experimental_support : String?  # Provides the experimental method to determine the state of this assembly  Allowable values: NMR Distance Restraints, NMR
  ├── id : String  # Identifies a unique record in pdbx_struct_assembly_auth_evidence.
```

## PdbxStructAssemblyGen
```text
  ├── assembly_id : String?  # This data item is a pointer to _pdbx_struct_assembly.id in the  PDBX_STRUCT_ASSEMBLY category.
  ├── asym_id_list : String[]?  # This data item is a pointer to _struct_asym.id in  the STRUCT_ASYM category.   This item may be expressed as a comma sep
  ├── oper_expression : String?  # Identifies the operation of collection of operations  from category PDBX_STRUCT_OPER_LIST.   Operation expressions may h
  ├── ordinal : Int  # This data item is an ordinal index for the  PDBX_STRUCT_ASSEMBLY category.
```

## PdbxStructAssemblyProp
```text
  ├── assembly_id : String?  # The identifier for the assembly used in category PDBX_STRUCT_ASSEMBLY.
  ├── biol_id : String  # The identifier for the assembly used in category PDBX_STRUCT_ASSEMBLY.
  ├── type : String  # The property type for the assembly.  ABSA (A^2) is the "Total buried surface area (A^2)"  SSA (A^2) is "Surface area for
  ├── value : String?  # The value of the assembly property.
```

## PdbxStructOperList
```text
  ├── id : String  # This identifier code must uniquely identify a  record in the PDBX_STRUCT_OPER_LIST list.
  ├── matrix_1_1 : Float?  # The [1][1] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_1_2 : Float?  # The [1][2] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_1_3 : Float?  # The [1][3] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_2_1 : Float?  # The [2][1] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_2_2 : Float?  # The [2][2] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_2_3 : Float?  # The [2][3] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_3_1 : Float?  # The [3][1] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_3_2 : Float?  # The [3][2] element of the 3x3 matrix component of the  transformation operation.
  ├── matrix_3_3 : Float?  # The [3][3] element of the 3x3 matrix component of the  transformation operation.
  ├── name : String?  # A descriptive name for the transformation operation.  Examples: 1_555, two-fold rotation
  ├── symmetry_operation : String?  # The symmetry operation corresponding to the transformation operation.  Examples: x,y,z, x+1/2,y,-z
  ├── type : String?  # A code to indicate the type of operator.  Allowable values: 2D crystal symmetry operation, 3D crystal symmetry operation
  ├── vector_1 : Float?  # The [1] element of the three-element vector component of the  transformation operation.
  ├── vector_2 : Float?  # The [2] element of the three-element vector component of the  transformation operation.
  ├── vector_3 : Float?  # The [3] element of the three-element vector component of the  transformation operation.
```

## PdbxStructSpecialSymmetry
```text
  ├── PDB_model_num : Int?  # Part of the identifier for the molecular component.  This data item is a pointer to _atom_site.pdbx_PDB_model_num in the
  ├── auth_seq_id : String?  # Part of the identifier for the molecular component.   This data item is a pointer to _atom_site.auth_seq_id in the  ATOM
  ├── id : Int  # The value of _pdbx_struct_special_symmetry.id must uniquely identify  each item in the PDBX_STRUCT_SPECIAL_SYMMETRY list
  ├── label_asym_id : String?  # Part of the identifier for the molecular component.   This data item is a pointer to _atom_site.label_asym_id in the  AT
  ├── label_comp_id : String?  # Part of the identifier for the molecular component.   This data item is a pointer to _atom_site.label_comp_id in the  AT
```

## PdbxVrptSummary
```text
  ├── RNA_suiteness : Float?  # The MolProbity conformer-match quality parameter for RNA structures. Low values are worse. Specific to structures that c
  ├── attempted_validation_steps : String?  # The steps that were attempted by the validation pipeline software.  A step typically involves running a 3rd party valida
  ├── ligands_for_buster_report : String?  # A flag indicating if there are ligands in the model used for detailed Buster analysis.  Allowable values: N, Y
  ├── report_creation_date : Date?  # The date, time and time-zone that the validation report  was created.  The string will be formatted like yyyy-mm-dd:hh:m
  ├── restypes_notchecked_for_bond_angle_geometry : String[]?  # This is a comma separated list of the residue types whose bond lengths and bond angles have  not been checked against "s
```

## PdbxVrptSummaryDiffraction
```text
  ├── B_factor_type : String?  # An indicator if isotropic B factors are partial or full values.  Allowable values: FULL, PARTIAL
  ├── Babinet_b : Float?  # REFMAC scaling parameter as reported in log output line starting 'bulk solvent: scale'. X-ray entry specific, obtained i
  ├── Babinet_k : Float?  # REFMAC scaling parameter as reported in log output line starting 'bulk solvent: scale'. X-ray entry specific, obtained i
  ├── CCP4_version : String?  # The version of CCP4 suite used in the analysis.
  ├── DCC_R : Float?  # The overall R-factor from a DCC recalculation of an electron density map. Currently value is rounded to 2 decimal places
  ├── DCC_Rfree : Float?  # Rfree as calculated by DCC.
  ├── EDS_R : Float?  # The overall R factor from the EDS REFMAC calculation (no free set is used in this). Currently value is rounded to 2 deci
  ├── EDS_R_warning : String?  # Warning message when EDS calculated R vs reported R is higher than a threshold
  ├── EDS_res_high : Float?  # The data high resolution diffraction limit, in Angstroms, found in the input structure factor file. X-ray entry specific
  ├── EDS_res_low : Float?  # The data low resolution diffraction limit, in Angstroms, found in the input structure factor file. X-ray entry specific,
  ├── Fo_Fc_correlation : Float?  # Fo,Fc correlation: The difference between the observed structure factors (Fo) and the  calculated structure factors (Fc)
  ├── I_over_sigma : String?  # Each reflection has an intensity (I) and an uncertainty in measurement  (sigma(I)), so I/sigma(I) is the signal-to-noise
  ├── Padilla_Yeates_L2_mean : Float?  # Padilla and Yeates twinning parameter <|L**2|>. Theoretical values is 0.333 in the untwinned case, and 0.2 in the perfec
  ├── Padilla_Yeates_L_mean : Float?  # Padilla and Yeates twinning parameter <|L|>. Theoretical values is 0.5 in the untwinned case, and 0.375 in the perfectly
  ├── Q_score : Float?  # The overall Q-score of the fit of coordinates to the electron map. The Q-score is defined in Pintilie, GH. et al., Natur
  ├── Wilson_B_aniso : String?  # Result of absolute likelihood based Wilson scaling,  The anisotropic B value of the data is determined using a likelihoo
  ├── Wilson_B_estimate : Float?  # An estimate of the overall B-value of the structure, calculated from the diffraction data.  Units Angstroms squared. It 
  ├── acentric_outliers : Int?  # The number of acentric reflections that Xtriage identifies as outliers on the basis  of Wilson statistics. Note that if 
  ├── bulk_solvent_b : Float?  # REFMAC scaling parameter as reported in log output file. X-ray entry specific, obtained in the EDS step from REFMAC calc
  ├── bulk_solvent_k : Float?  # REFMAC reported scaling parameter. X-ray entry specific, obtained in the EDS step from REFMAC calculation.
  ├── centric_outliers : Int?  # The number of centric reflections that Xtriage identifies as outliers. X-ray entry specific, calculated by Phenix Xtriag
  ├── data_anisotropy : Float?  # The ratio (Bmax - Bmin) / Bmean where Bmax, Bmin and Bmean are computed from the B-values  associated with the principal
  ├── data_completeness : Float?  # The percent completeness of diffraction data.
  ├── density_fitness_version : String?  # The version of density-fitness suite programs used in the analysis.
  ├── exp_method : String?  # Experimental method for statistics
  ├── num_miller_indices : Int?  # The number of Miller Indices reported by the Xtriage program. This should be the same as the number of _refln in the inp
  ├── number_reflns_R_free : Int?  # The number of reflections in the free set as defined in the input structure factor file supplied to the validation pipel
  ├── percent_RSRZ_outliers : Float?  # The percent of RSRZ outliers.
  ├── percent_free_reflections : Float?  # A percentage, Normally percent proportion of the total number. Between 0% and 100%.
  ├── servalcat_version : String?  # The version of Servalcat program used in the analysis.
  ├── trans_NCS_details : String?  # A sentence giving the result of Xtriage's analysis on translational NCS. X-ray entry specific, obtained from the Xtriage
  ├── twin_fraction : String?  # Estimated twinning fraction for operators as identified by Xtriage. A semicolon separated list of operators with fractio
```

## PdbxVrptSummaryEm
```text
  ├── Q_score : Float?  # The overall Q-score of the fit of coordinates to the electron map. The Q-score is defined in Pintilie, GH. et al., Natur
  ├── atom_inclusion_all_atoms : Float?  # The proportion of all non hydrogen atoms within density.
  ├── atom_inclusion_backbone : Float?  # The proportion of backbone atoms within density.
  ├── author_provided_fsc_resolution_by_cutoff_halfbit : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve halfbit.
  ├── author_provided_fsc_resolution_by_cutoff_onebit : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve onebit.
  ├── author_provided_fsc_resolution_by_cutoff_pt_143 : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve 0.143.
  ├── author_provided_fsc_resolution_by_cutoff_pt_333 : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve 0.333.
  ├── author_provided_fsc_resolution_by_cutoff_pt_5 : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve 0.5.
  ├── author_provided_fsc_resolution_by_cutoff_threesigma : Float?  # The resolution from the intersection of the author provided fsc and the indicator curve threesigma.
  ├── calculated_fsc_resolution_by_cutoff_halfbit : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve ha
  ├── calculated_fsc_resolution_by_cutoff_onebit : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve on
  ├── calculated_fsc_resolution_by_cutoff_pt_143 : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.
  ├── calculated_fsc_resolution_by_cutoff_pt_333 : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.
  ├── calculated_fsc_resolution_by_cutoff_pt_5 : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve 0.
  ├── calculated_fsc_resolution_by_cutoff_threesigma : Float?  # The resolution from the intersection of the fsc curve generated by from the provided halfmaps and the indicator curve th
  ├── contour_level_primary_map : Float?  # The recommended contour level for the primary map of this deposition.
  ├── exp_method : String?  # Experimental method for statistics
```

## PdbxVrptSummaryEntityFitToMap
```text
  ├── PDB_model_num : Int?  # The unique model number from _atom_site.pdbx_PDB_model_num.
  ├── Q_score : Float?  # The calculated average Q-score.
  ├── average_residue_inclusion : Float?  # The average of the residue inclusions for all residues in this instance
```

## PdbxVrptSummaryEntityGeometry
```text
  ├── PDB_model_num : Int?  # The unique model number from _atom_site.pdbx_PDB_model_num.
  ├── angles_RMSZ : Float?  # The overall root mean square of the Z-score for deviations of bond angles in comparison to  "standard geometry" made usi
  ├── average_residue_inclusion : Float?  # The average of the residue inclusions for all residues in this instance
  ├── bonds_RMSZ : Float?  # The overall root mean square of the Z-score for deviations of bond lengths in comparison to  "standard geometry" made us
  ├── num_angles_RMSZ : Int?  # The number of bond angles compared to "standard geometry" made using the MolProbity dangle program. Standard geometry pa
  ├── num_bonds_RMSZ : Int?  # The number of bond lengths compared to "standard geometry" made using the MolProbity dangle program. Standard geometry p
```

## PdbxVrptSummaryGeometry
```text
  ├── angles_RMSZ : Float?  # The overall root mean square of the Z-score for deviations of bond angles in comparison to  "standard geometry" made usi
  ├── bonds_RMSZ : Float?  # The overall root mean square of the Z-score for deviations of bond lengths in comparison to  "standard geometry" made us
  ├── clashscore : Float?  # This score is derived from the number of pairs of atoms in the PDB_model_num that are unusually close to each other.  It
  ├── clashscore_full_length : Float?  # Only given for structures determined by NMR. The MolProbity pdbx_vrpt_instance_clashes score for all label_atom_id pairs
  ├── num_H_reduce : Int?  # This is the number of hydrogen atoms added and optimized by the MolProbity reduce pdbx_vrpt_software as part of the all-
  ├── num_angles_RMSZ : Int?  # The number of bond angles compared to "standard geometry" made using the MolProbity dangle program. Standard geometry pa
  ├── num_bonds_RMSZ : Int?  # The number of bond lengths compared to "standard geometry" made using the MolProbity dangle program. Standard geometry p
  ├── percent_ramachandran_outliers : Float?  # The percentage of residues with Ramachandran outliers.
  ├── percent_ramachandran_outliers_full_length : Float?  # Only given for structures determined by NMR. The MolProbity Ramachandran outlier score for all atoms in the structure ra
  ├── percent_rotamer_outliers : Float?  # The MolProbity sidechain outlier score (a percentage). Protein sidechains mostly adopt certain (combinations of) preferr
  ├── percent_rotamer_outliers_full_length : Float?  # Only given for structures determined by NMR. The MolProbity sidechain outlier score for all atoms in the structure rathe
```

## PdbxVrptSummaryNmr
```text
  ├── chemical_shift_completeness : Float?  # Overall completeness of the chemical shift assignments for the well-defined  regions of the structure.
  ├── chemical_shift_completeness_full_length : Float?  # Overall completeness of the chemical shift assignments for the full  macromolecule or complex as suggested by the molecu
  ├── cyrange_error : String?  # Diagnostic message from the wrapper of Cyrange software which identifies the  well-defined cores (domains) of NMR protei
  ├── cyrange_number_of_domains : Int?  # Total number of well-defined cores (domains) identified by Cyrange
  ├── exp_method : String?  # Experimental method for statistics
  ├── medoid_model : Int?  # For each Cyrange well-defined core ("cyrange_domain") the id of the PDB_model_num which is most  similar to other models
  ├── nmr_models_consistency_flag : String?  # A flag indicating if all models in the NMR ensemble contain the exact  same atoms ("True") or if the models differ in th
  ├── nmrclust_error : String?  # Diagnostic message from the wrapper of NMRClust software which clusters NMR models.
  ├── nmrclust_number_of_clusters : Int?  # Total number of clusters in the NMR ensemble identified by NMRClust.
  ├── nmrclust_number_of_models : Int?  # Number of models analysed by NMRClust - should in almost all cases be the same as the number of models in the NMR ensemb
  ├── nmrclust_number_of_outliers : Int?  # Number of models that do not belong to any cluster as deemed by NMRClust.
  ├── nmrclust_representative_model : Int?  # Overall representative PDB_model_num of the NMR ensemble as identified by NMRClust.
```

## Query
```text
  ├── assemblies : CoreAssembly[]?  # Get a list of assemblies given the list of ASSEMBLY IDs. Here an ASSEMBLY ID is a compound identifier that includes entr
  ├── assembly : CoreAssembly?  # Get an assembly given the ENTRY ID and ASSEMBLY ID. Here ASSEMBLY ID is '1', '2', '3', etc. or 'deposited' for deposited
  ├── branched_entities : CoreBranchedEntity[]?  # Get a list of branched entities given a list of ENTITY IDs. Here ENTITY ID is a compound identifier that includes entry_
  ├── branched_entity : CoreBranchedEntity?  # Get a branched entity, given the ENTRY ID and ENTITY ID. Here ENTITY ID is a '1', '2', '3', etc.
  ├── branched_entity_instance : CoreBranchedEntityInstance?  # Get a branched entity instance (chain), given the ENTRY ID and ENTITY INSTANCE ID. Here ENTITY INSTANCE ID identifies st
  ├── branched_entity_instances : CoreBranchedEntityInstance[]?  # Get a list of branched entity instances (chains), given the list of ENTITY INSTANCE IDs. Here ENTITY INSTANCE ID identif
  ├── chem_comp : CoreChemComp?  # Get a chemical component given the CHEMICAL COMPONENT ID, e.g. 'CFF', 'HEM', 'FE'.For nucleic acid polymer entities, use
  ├── chem_comps : CoreChemComp[]?  # Get a list of chemical components given the list of CHEMICAL COMPONENT ID, e.g. 'CFF', 'HEM', 'FE'.For nucleic acid poly
  ├── entries : CoreEntry[]?  # Get a list of entries given a list of IDs.
  ├── entry : CoreEntry?  # Get entry given the id.
  ├── entry_group : GroupEntry?  # Given a group ID get a group object formed by aggregating individual structures that share a degree of similarity
  ├── entry_groups : GroupEntry[]?  # Given a list of group IDs get a list of group objects formed by aggregating structures that share a degree of similarity
  ├── group_provenance : GroupProvenance?  # Given a group provenance ID get an object that describes aggregation method used to create groups
  ├── interface : CoreInterface?  # Get a pairwise polymeric interface given the ENTRY ID, ASSEMBLY ID and INTERFACE ID.
  ├── interfaces : CoreInterface[]?  # Get a list of pairwise polymeric interfaces given a list of INTERFACE IDs. Here INTERFACE ID is a compound identifier th
  ├── nonpolymer_entities : CoreNonpolymerEntity[]?  # Get a list of non-polymer entities given a list of ENTITY IDs. Here ENTITY ID is a compound identifier that includes ent
  ├── nonpolymer_entity : CoreNonpolymerEntity?  # Get a non-polymer entity, given the ENTRY ID and ENTITY ID. Here ENTITY ID is a '1', '2', '3', etc.
  ├── nonpolymer_entity_group : GroupNonPolymerEntity?  # Given a group ID get a group object formed by aggregating non-polymer entities that share a degree of similarity
  ├── nonpolymer_entity_groups : GroupNonPolymerEntity[]?  # Given a list of group IDs get a list of group objects formed by aggregating non-polymer entities that share a degree of 
  ├── nonpolymer_entity_instance : CoreNonpolymerEntityInstance?  # Get a non-polymer entity instance (chain), given the ENTRY ID and ENTITY INSTANCE ID. Here ENTITY INSTANCE ID identifies
  ├── nonpolymer_entity_instances : CoreNonpolymerEntityInstance[]?  # Get a list of non-polymer entity instances (chains), given the list of ENTITY INSTANCE IDs. Here ENTITY INSTANCE ID iden
  ├── polymer_entities : CorePolymerEntity[]?  # Get a list of polymer entities given a list of ENTITY IDs. Here ENTITY ID is a compound identifier that includes entry_i
  ├── polymer_entity : CorePolymerEntity?  # Get a polymer entity, given the ENTRY ID and ENTITY ID. Here ENTITY ID is a '1', '2', '3', etc.
  ├── polymer_entity_group : GroupPolymerEntity?  # Given a group ID get a group object formed by aggregating polymer entities that share a degree of similarity
  ├── polymer_entity_groups : GroupPolymerEntity[]?  # Given a list of group IDs get a list of group objects formed by aggregating polymer entities that share a degree of simi
  ├── polymer_entity_instance : CorePolymerEntityInstance?  # Get a polymer entity instance (chain), given the ENTRY ID and ENTITY INSTANCE ID. Here ENTITY INSTANCE ID identifies str
  ├── polymer_entity_instances : CorePolymerEntityInstance[]?  # Get a list of polymer entity instances (chains), given the list of ENTITY INSTANCE IDs. Here ENTITY INSTANCE ID identifi
  ├── pubmed : CorePubmed?  # Get literature information from PubMed database given the PubMed identifier.
  ├── uniprot : CoreUniprot?  # Get UniProt KB entry given the UniProt primary accession.
```

## RcsbAccessionInfo
```text
  ├── deposit_date : Date?  # The entry deposition date.  Examples: 2020-07-11, 2013-10-01
  ├── has_released_experimental_data : String?  # A code indicating the current availibility of experimental data in the repository.  Allowable values: N, Y
  ├── initial_release_date : Date?  # The entry initial release date.  Examples: 2020-01-10, 2018-01-23
  ├── major_revision : Int?  # The latest entry major revision number.
  ├── minor_revision : Int?  # The latest entry minor revision number.
  ├── revision_date : Date?  # The latest entry revision date.  Examples: 2020-02-11, 2018-10-23
  ├── status_code : String?  # The release status for the entry.  Allowable values: AUCO, AUTH, HOLD, HPUB, POLC, PROC, REFI, REL, REPL, WAIT, WDRN
```

## RcsbAssemblyAnnotation
```text
  ├── additional_properties : RcsbAssemblyAnnotationAdditionalProperties[]?
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that assigned the annotation.  Examples: MCSA
  ├── type : String?  # A type or category of the annotation.  Allowable values: MCSA
```

## RcsbAssemblyAnnotationAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: MCSA_MOTIF_COMPATIBILITY
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbAssemblyContainerIdentifiers
```text
  ├── assembly_id : String  # Assembly identifier for the container.  Examples: 1, 5
  ├── entry_id : String  # Entry identifier for the container.
  ├── interface_ids : String[]?  # List of binary interface Ids within the assembly (it points to interface id collection).
  ├── rcsb_id : String?  # A unique identifier for each object in this assembly container formed by  a dash separated concatenation of entry and as
```

## RcsbAssemblyFeature
```text
  ├── additional_properties : RcsbAssemblyFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbAssemblyFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that assigned the feature.  Examples: MCSA
  ├── type : String?  # A type or category of the feature.  Allowable values: MCSA
```

## RcsbAssemblyFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: MCSA_MOTIF_COMPATIBILITY
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbAssemblyFeatureFeaturePositions
```text
  ├── asym_id : String  # An identifier of polymer chain (label_asym_id) corresponding to the feature assignment.  Examples: A, B
  ├── beg_seq_id : Int  # An identifier for the monomer at which this segment of the feature begins.
  ├── end_seq_id : Int?  # An identifier for the monomer at which this segment of the feature ends.
  ├── struct_oper_list : String[]  # Identifies the list of operations from the category pdbx_struct_oper_list. One item in array per operator applied. The o
  ├── values : Float[]?  # The value(s) of the feature over the monomer segment.
```

## RcsbAssemblyInfo
```text
  ├── assembly_id : String?  # Entity identifier for the container.
  ├── atom_count : Int?  # The assembly non-hydrogen atomic coordinate count.
  ├── branched_atom_count : Int?  # The assembly non-hydrogen branched entity atomic coordinate count.
  ├── branched_entity_count : Int?  # The number of distinct branched entities in the generated assembly.
  ├── branched_entity_instance_count : Int?  # The number of branched instances in the generated assembly data set.  This is the total count of branched entity instanc
  ├── deuterated_water_count : Int?  # The assembly deuterated water molecule count.
  ├── entry_id : String  # The PDB entry accession code.  Examples: 1KIP
  ├── formula_weight : Float?  # Formula mass (KDa) of the assembly.  Examples: null, null
  ├── hydrogen_atom_count : Int?  # The assembly hydrogen atomic coordinate count.
  ├── modeled_polymer_monomer_count : Int?  # The number of modeled polymer monomers in the assembly coordinate data.  This is the total count of monomers with report
  ├── na_polymer_entity_types : String?  # Nucleic acid polymer entity type categories describing the generated assembly.  Allowable values: DNA (only), DNA/RNA (o
  ├── nonpolymer_atom_count : Int?  # The assembly non-hydrogen non-polymer entity atomic coordinate count.
  ├── nonpolymer_entity_count : Int?  # The number of distinct non-polymer entities in the generated assembly exclusive of solvent.
  ├── nonpolymer_entity_instance_count : Int?  # The number of non-polymer instances in the generated assembly data set exclusive of solvent.  This is the total count of
  ├── num_heterologous_interface_entities : Int?  # Number of heterologous (both binding sites are different) interface entities
  ├── num_heteromeric_interface_entities : Int?  # Number of heteromeric (both partners are different polymeric entities) interface entities
  ├── num_homomeric_interface_entities : Int?  # Number of homomeric (both partners are the same polymeric entity) interface entities
  ├── num_interface_entities : Int?  # Number of polymer-polymer interface entities, grouping equivalent interfaces at the entity level (i.e. same entity_ids o
  ├── num_interfaces : Int?  # Number of geometrically equivalent (i.e. same asym_ids on either side) polymer-polymer interfaces in the assembly
  ├── num_isologous_interface_entities : Int?  # Number of isologous (both binding sites are same, i.e. interface is symmetric) interface entities
  ├── num_na_interface_entities : Int?  # Number of nucleic acid-nucleic acid interface entities
  ├── num_prot_na_interface_entities : Int?  # Number of protein-nucleic acid interface entities
  ├── num_protein_interface_entities : Int?  # Number of protein-protein interface entities
  ├── polymer_atom_count : Int?  # The assembly non-hydrogen polymer entity atomic coordinate count.
  ├── polymer_composition : String?  # Categories describing the polymer entity composition for the generated assembly.  Allowable values: DNA, DNA/RNA, NA-hyb
  ├── polymer_entity_count : Int?  # The number of distinct polymer entities in the generated assembly.
  ├── polymer_entity_count_DNA : Int?  # The number of distinct DNA polymer entities in the generated assembly.
  ├── polymer_entity_count_RNA : Int?  # The number of distinct RNA polymer entities in the generated assembly.
  ├── polymer_entity_count_nucleic_acid : Int?  # The number of distinct nucleic acid polymer entities (DNA or RNA) in the generated assembly.
  ├── polymer_entity_count_nucleic_acid_hybrid : Int?  # The number of distinct hybrid nucleic acid polymer entities in the generated assembly.
  ├── polymer_entity_count_protein : Int?  # The number of distinct protein polymer entities in the generated assembly.
  ├── polymer_entity_instance_count : Int?  # The number of polymer instances in the generated assembly data set.  This is the total count of polymer entity instances
  ├── polymer_entity_instance_count_DNA : Int?  # The number of DNA polymer instances in the generated assembly data set.  This is the total count of DNA polymer entity i
  ├── polymer_entity_instance_count_RNA : Int?  # The number of RNA polymer instances in the generated assembly data set.  This is the total count of RNA polymer entity i
  ├── polymer_entity_instance_count_nucleic_acid : Int?  # The number of nucleic acid polymer instances in the generated assembly data set.  This is the total count of nucleic aci
  ├── polymer_entity_instance_count_nucleic_acid_hybrid : Int?  # The number of hybrid nucleic acide polymer instances in the generated assembly data set.  This is the total count of hyb
  ├── polymer_entity_instance_count_protein : Int?  # The number of protein polymer instances in the generated assembly data set.  This is the total count of protein polymer 
  ├── polymer_monomer_count : Int?  # The number of polymer monomers in sample entity instances comprising the assembly data set.  This is the total count of 
  ├── selected_polymer_entity_types : String?  # Selected polymer entity type categories describing the generated assembly.  Allowable values: Nucleic acid (only), Other
  ├── solvent_atom_count : Int?  # The assembly non-hydrogen solvent atomic coordinate count.
  ├── solvent_entity_count : Int?  # The number of distinct solvent entities in the generated assembly.
  ├── solvent_entity_instance_count : Int?  # The number of solvent instances in the generated assembly data set.  This is the total count of solvent entity instances
  ├── total_assembly_buried_surface_area : Float?  # Total buried surface area calculated as the sum of buried surface areas over all interfaces
  ├── total_number_interface_residues : Int?  # Total number of interfacing residues in the assembly, calculated as the sum of interfacing residues over all interfaces
  ├── unmodeled_polymer_monomer_count : Int?  # The number of unmodeled polymer monomers in the assembly coordinate data. This is  the total count of monomers with unre
```

## RcsbBindingAffinity
```text
  ├── comp_id : String  # Ligand identifier.  Examples: 0WE, SPE, CL
  ├── link : String  # Link to external resource referencing the data.
  ├── provenance_code : String  # The resource name for the related binding affinity reference.  Allowable values: Binding MOAD, BindingDB, PDBBind
  ├── reference_sequence_identity : Int?  # Data point provided by BindingDB. Percent identity between PDB sequence and reference sequence.
  ├── symbol : String?  # Binding affinity symbol indicating approximate or precise strength of the binding.  Examples: ~, =, >, <, >=, <=
  ├── type : String  # Binding affinity measurement given in one of the following types:  The concentration constants: IC50: the concentration 
  ├── unit : String  # Binding affinity unit.  Dissociation constant Kd is normally in molar units (or millimolar , micromolar, nanomolar, etc)
  ├── value : Float  # Binding affinity value between a ligand and its target molecule.
```

## RcsbBirdCitation
```text
  ├── id : String  # The value of _rcsb_bird_citation.id must uniquely identify a record in the  rcsb_bird_citation list.  Examples: 1, 2
  ├── journal_abbrev : String?  # Abbreviated name of the cited journal as given in the  Chemical Abstracts Service Source Index.  Examples: J.Mol.Biol., 
  ├── journal_volume : String?  # Volume number of the journal cited; relevant for journal  articles.  Examples: 174
  ├── page_first : String?  # The first page of the rcsb_bird_citation; relevant for journal  articles, books and book chapters.
  ├── page_last : String?  # The last page of the rcsb_bird_citation; relevant for journal  articles, books and book chapters.
  ├── pdbx_database_id_DOI : String?  # Document Object Identifier used by doi.org to uniquely  specify bibliographic entry.  Examples: 10.2345/S138410769700022
  ├── pdbx_database_id_PubMed : Int?  # Ascession number used by PubMed to categorize a specific  bibliographic entry.
  ├── rcsb_authors : String[]?  # Names of the authors of the citation; relevant for journal  articles, books and book chapters.  Names are separated by v
  ├── title : String?  # The title of the rcsb_bird_citation; relevant for journal articles, books  and book chapters.  Examples: Structure of di
  ├── year : Int?  # The year of the rcsb_bird_citation; relevant for journal articles, books  and book chapters.
```

## RcsbBranchedEntity
```text
  ├── details : String?  # A description of special aspects of the branched entity.
  ├── formula_weight : Float?  # Formula mass (KDa) of the branched entity.  Examples: null, null
  ├── pdbx_description : String?  # A description of the branched entity.  Examples: alpha-D-glucopyranose-(1-6)-beta-D-glucopyranose, beta-D-xylopyranose-(
  ├── pdbx_number_of_molecules : Int?  # The number of molecules of the branched entity in the entry.
```

## RcsbBranchedEntityAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbBranchedEntityAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB
  ├── type : String?  # A type or category of the annotation.
```

## RcsbBranchedEntityAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbBranchedEntityContainerIdentifiers
```text
  ├── asym_ids : String[]?  # Instance identifiers corresponding to copies of the entity in this container.
  ├── auth_asym_ids : String[]?  # Author instance identifiers corresponding to copies of the entity in this container.
  ├── chem_comp_monomers : String[]?  # Unique list of monomer chemical component identifiers in the entity in this container.
  ├── chem_ref_def_id : String?  # The chemical reference definition identifier for the entity in this container.  Examples: PRD_000010
  ├── entity_id : String  # Entity identifier for the container.  Examples: 1, 2
  ├── entry_id : String  # Entry identifier for the container.  Examples: 1B5F, 2HYV
  ├── prd_id : String?  # The BIRD identifier for the entity in this container.  Examples: PRD_000010
  ├── rcsb_id : String?  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── reference_identifiers : RcsbBranchedEntityContainerIdentifiersReferenceIdentifiers[]?
```

## RcsbBranchedEntityContainerIdentifiersReferenceIdentifiers
```text
  ├── provenance_source : String?  # Source of the reference resource assignment  Allowable values: PDB, RCSB
  ├── resource_accession : String?  # Reference resource accession code  Examples: G07411ON, G42666HT
  ├── resource_name : String?  # Reference resource name  Allowable values: GlyCosmos, GlyGen, GlyTouCan
```

## RcsbBranchedEntityFeature
```text
  ├── additional_properties : RcsbBranchedEntityFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbBranchedEntityFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: PDB
  ├── reference_scheme : String?  # Code residue coordinate system for the assigned feature.  Allowable values: PDB entity
  ├── type : String?  # A type or category of the feature.  Allowable values: mutation
```

## RcsbBranchedEntityFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbBranchedEntityFeatureFeaturePositions
```text
  ├── beg_comp_id : String?  # An identifier for the leading monomer corresponding to the feature assignment.  Examples: NAG, MAN
  ├── beg_seq_id : Int  # An identifier for the leading monomer position of the feature.
  ├── end_seq_id : Int?  # An identifier for the leading monomer position of the feature.
  ├── value : Float?  # The value for the feature at this monomer.  Examples: null, null
```

## RcsbBranchedEntityFeatureSummary
```text
  ├── count : Int?  # The feature count.
  ├── coverage : Float?  # The fractional feature coverage relative to the full branched entity.  Examples: null, null
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: mutation
```

## RcsbBranchedEntityInstanceContainerIdentifiers
```text
  ├── asym_id : String  # Instance identifier for this container.
  ├── auth_asym_id : String?  # Author instance identifier for this container.
  ├── entity_id : String?  # Entity identifier for the container.
  ├── entry_id : String  # Entry identifier for the container.
  ├── rcsb_id : String?  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
```

## RcsbBranchedEntityKeywords
```text
  ├── text : String?  # Keywords describing this branched entity.
```

## RcsbBranchedEntityNameCom
```text
  ├── name : String?  # A common name for the branched entity.  Examples: HIV protease monomer, hemoglobin alpha chain
```

## RcsbBranchedEntityNameSys
```text
  ├── name : String  # The systematic name for the branched entity.
  ├── system : String?  # The system used to generate the systematic name of the branched entity.
```

## RcsbBranchedInstanceAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbBranchedInstanceAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── comp_id : String?  # Chemical component identifier.  Examples: ATP
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB
  ├── type : String?  # A type or category of the annotation.  Allowable values: CATH, SCOP
```

## RcsbBranchedInstanceAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbBranchedInstanceFeature
```text
  ├── additional_properties : RcsbBranchedInstanceFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbBranchedInstanceFeatureFeaturePositions[]?
  ├── feature_value : RcsbBranchedInstanceFeatureFeatureValue[]?
  ├── name : String?  # A name for the feature.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: PDB
  ├── reference_scheme : String?  # Code residue coordinate system for the assigned feature.  Allowable values: PDB entity, PDB entry
  ├── type : String  # A type or category of the feature.  Allowable values: BINDING_SITE, CATH, ECOD, MOGUL_ANGLE_OUTLIER, MOGUL_BOND_OUTLIER,
```

## RcsbBranchedInstanceFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Examples: bond_distance, bond_angle
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbBranchedInstanceFeatureFeaturePositions
```text
  ├── beg_comp_id : String?  # An identifier for the monomer(s) corresponding to the feature assignment.  Examples: NAG, MAN
  ├── beg_seq_id : Int  # An identifier for the leading monomer feature position.
  ├── end_seq_id : Int?  # An identifier for the terminal monomer feature position.
  ├── value : Float?  # The value of the feature at the monomer position.  Examples: null, null
  ├── values : Float[]?  # The value(s) of the feature at the monomer position.
```

## RcsbBranchedInstanceFeatureFeatureValue
```text
  ├── comp_id : String?  # The chemical component identifier for the instance of the feature value.  Examples: ATP,, STN
  ├── details : String?  # Specific details about the feature.  Examples: C1,C2, C1,C2,C3
  ├── reference : Float?  # The reference value of the feature.  Examples: null, null
  ├── reported : Float?  # The reported value of the feature.  Examples: null, null
  ├── uncertainty_estimate : Float?  # The estimated uncertainty of the reported feature value.  Examples: null, null
  ├── uncertainty_estimate_type : String?  # The type of estimated uncertainty for the reported feature value.  Allowable values: Z-Score
```

## RcsbBranchedInstanceFeatureSummary
```text
  ├── count : Int?  # The feature count.
  ├── coverage : Float?  # The fractional feature coverage relative to the full branched entity.  Examples: null, null
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: BINDING_SITE, CATH, MOGUL_ANGLE_OUTLIER, MOGUL_BOND_OUTLIER, RSCC_OU
```

## RcsbBranchedStructConn
```text
  ├── connect_partner : RcsbBranchedStructConnConnectPartner?
  ├── connect_target : RcsbBranchedStructConnConnectTarget?
  ├── connect_type : String?  # The connection type.  Allowable values: covalent bond, hydrogen bond, ionic interaction, metal coordination, mismatched 
  ├── description : String?  # A description of special details of the connection.  Examples: Watson-Crick base pair
  ├── dist_value : Float?  # Distance value for this contact.
  ├── id : String?  # The value of _rcsb_branched_struct_conn.id is an identifier for connection.
  ├── ordinal_id : Int  # The value of _rcsb_branched_struct_conn.id must uniquely identify a record in  the rcsb_branched_struct_conn list.
  ├── role : String?  # The chemical or structural role of the interaction  Allowable values: C-Mannosylation, N-Glycosylation, O-Glycosylation
  ├── value_order : String?  # The chemical bond order associated with the specified atoms in  this contact.  Allowable values: doub, quad, sing, trip
```

## RcsbBranchedStructConnConnectPartner
```text
  ├── label_alt_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_asym_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_atom_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _chem_comp_
  ├── label_comp_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_seq_id : Int?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_branched_struct_conn.connect
```

## RcsbBranchedStructConnConnectTarget
```text
  ├── auth_asym_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── auth_seq_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── label_alt_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_asym_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_atom_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_comp_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_seq_id : Int?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.c
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_branched_struct_conn.label* 
```

## RcsbChemCompAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbChemCompAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: RESID, UniProt, PDB
  ├── type : String?  # A type or category of the annotation.  Allowable values: ATC, Carbohydrate Anomer, Carbohydrate Isomer, Carbohydrate Pri
```

## RcsbChemCompAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbChemCompContainerIdentifiers
```text
  ├── atc_codes : String[]?  # The Anatomical Therapeutic Chemical (ATC) Classification System identifiers corresponding  to the chemical component.
  ├── comp_id : String  # The chemical component identifier.  Examples: ATP, STI
  ├── drugbank_id : String?  # The DrugBank identifier corresponding to the chemical component.  Examples: DB00781, DB15263
  ├── prd_id : String?  # The BIRD definition identifier.  Examples: PRD_000010
  ├── rcsb_id : String?  # A unique identifier for the chemical definition in this container.  Examples: ATP, PRD_000010
  ├── subcomponent_ids : String[]?  # The list of subcomponents contained in this component.
```

## RcsbChemCompDescriptor
```text
  ├── InChI : String?  # Standard IUPAC International Chemical Identifier (InChI) descriptor for the chemical component.     InChI, the IUPAC Int
  ├── InChIKey : String?  # Standard IUPAC International Chemical Identifier (InChI) descriptor key  for the chemical component   InChI, the IUPAC I
  ├── SMILES : String?  # Simplified molecular-input line-entry system (SMILES) descriptor for the chemical component.     Weininger D (February 1
  ├── SMILES_stereo : String?  # Simplified molecular-input line-entry system (SMILES) descriptor for the chemical  component including stereochemical fe
  ├── comp_id : String  # The chemical component identifier.
```

## RcsbChemCompInfo
```text
  ├── atom_count : Int?  # Chemical component total atom count
  ├── atom_count_chiral : Int?  # Chemical component chiral atom count
  ├── atom_count_heavy : Int?  # Chemical component heavy atom count
  ├── bond_count : Int?  # Chemical component total bond count
  ├── bond_count_aromatic : Int?  # Chemical component aromatic bond count
  ├── comp_id : String  # The chemical component identifier.
  ├── initial_deposition_date : Date?  # The date the chemical definition was first deposited in the PDB repository.  Examples: 2016-09-11
  ├── initial_release_date : Date?  # The initial date the chemical definition was released in the PDB repository.  Examples: 2016-09-11
  ├── release_status : String?  # The release status of the chemical definition.  Allowable values: DEL, HOLD, HPUB, OBS, REF_ONLY, REL
  ├── revision_date : Date?  # The date of last revision of the chemical definition.  Examples: 2016-10-12
```

## RcsbChemCompRelated
```text
  ├── comp_id : String  # The value of _rcsb_chem_comp_related.comp_id is a reference to  a chemical component definition.
  ├── ordinal : Int  # The value of _rcsb_chem_comp_related.ordinal distinguishes  related examples for each chemical component.
  ├── related_mapping_method : String?  # The method used to establish the resource correspondence.  Allowable values: assigned by DrugBank resource, assigned by 
  ├── resource_accession_code : String?  # The resource identifier code for the related chemical reference.  Examples: 124832
  ├── resource_name : String?  # The resource name for the related chemical reference.  Allowable values: CAS, CCDC/CSD, COD, ChEBI, ChEMBL, DrugBank, Ph
```

## RcsbChemCompSynonyms
```text
  ├── comp_id : String  # The chemical component to which this synonym applies.
  ├── name : String?  # The synonym of this particular chemical component.  Examples: Ursonic acid, Talotrexin, 4-oxodecanedioic acid
  ├── ordinal : Int  # This data item is an ordinal index for the  RCSB_CHEM_COMP_SYNONYMS category.
  ├── provenance_source : String?  # The provenance of this synonym.  Allowable values: ACDLabs, Author, ChEBI, ChEMBL, DrugBank, GMML, Lexichem, OpenEye OET
  ├── type : String?  # This data item contains the synonym type.  Allowable values: Brand Name, Common Name, Condensed IUPAC Carbohydrate Symbo
```

## RcsbChemCompTarget
```text
  ├── comp_id : String  # The value of _rcsb_chem_comp_target.comp_id is a reference to  a chemical component definition.
  ├── interaction_type : String?  # The type of target interaction.
  ├── name : String?  # The chemical component target name.
  ├── ordinal : Int  # The value of _rcsb_chem_comp_target.ordinal distinguishes  related examples for each chemical component.
  ├── provenance_source : String?  # A code indicating the provenance of the target interaction assignment  Allowable values: DrugBank, PDB Primary Data
  ├── reference_database_accession_code : String?  # The reference identifier code for the target interaction reference.  Examples: Q9HD40
  ├── reference_database_name : String?  # The reference database name for the target interaction.  Allowable values: UniProt
  ├── target_actions : String[]?  # The mechanism of action of the chemical component - target interaction.
```

## RcsbClusterFlexibility
```text
  ├── avg_rmsd : Float?  # Average RMSD refer to average pairwise RMSD (Root Mean Square Deviation of C-alpha atoms) between structures in the clus
  ├── label : String?  # Structural flexibility in the cluster (95% sequence identity) where a given entity belongs.
  ├── link : String?  # Link to the associated PDBFlex database entry.
  ├── max_rmsd : Float?  # Maximal RMSD refer to maximal pairwise RMSD (Root Mean Square Deviation of C-alpha atoms) between structures in the clus
  ├── provenance_code : String?  # Provenance code indicating the origin of the flexibility data.  Allowable values: PDBFlex
```

## RcsbClusterMembership
```text
  ├── cluster_id : Int  # Identifier for a cluster at the specified level of sequence identity within the cluster data set.
  ├── identity : Int  # Sequence identity expressed as an integer percent value.
```

## RcsbCompModelProvenance
```text
  ├── entry_id : String  # Entry identifier corresponding to the computed structure model.  Examples: AF-P60325-F1, ma-bak-cepc-0019
  ├── source_db : String?  # Source database for the computed structure model.  Allowable values: AlphaFoldDB, ModelArchive
  ├── source_filename : String?  # Source filename for the computed structure model.
  ├── source_pae_url : String?  # Source URL for computed structure model predicted aligned error (PAE) json file.
  ├── source_url : String?  # Source URL for computed structure model file.
```

## RcsbEntityHostOrganism
```text
  ├── beg_seq_num : Int?  # The beginning polymer sequence position for the polymer section corresponding  to this host organism.   A reference to t
  ├── common_name : String?  # The common name of the host organism
  ├── end_seq_num : Int?  # The ending polymer sequence position for the polymer section corresponding  to this host organism.   A reference to the 
  ├── ncbi_common_names : String[]?  # Common names associated with this taxonomy code obtained from NCBI Taxonomy Database.    These names correspond to the t
  ├── ncbi_parent_scientific_name : String?  # The parent scientific name in the NCBI taxonomy hierarchy (depth=1) associated with this taxonomy code.  References:  Sa
  ├── ncbi_scientific_name : String?  # The scientific name associated with this taxonomy code aggregated by the NCBI Taxonomy Database.    This name correspond
  ├── ncbi_taxonomy_id : Int?  # NCBI Taxonomy identifier for the host organism.    Reference:   Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Sch
  ├── pdbx_src_id : Int  # An identifier for an entity segment.
  ├── provenance_source : String?  # A code indicating the provenance of the host organism.  Allowable values: PDB Primary Data, Primary Data
  ├── scientific_name : String?  # The scientific name of the host organism
  ├── taxonomy_lineage : RcsbEntityHostOrganismTaxonomyLineage[]?
```

## RcsbEntityHostOrganismTaxonomyLineage
```text
  ├── depth : Int?  # Members of the NCBI Taxonomy lineage as parent taxonomy lineage depth (1-N)
  ├── id : String?  # Members of the NCBI Taxonomy lineage as parent taxonomy idcodes.  Examples: 469008, 10469
  ├── name : String?  # Members of the NCBI Taxonomy lineage as parent taxonomy names.  Examples: Escherichia coli BL21(DE3), Baculovirus
```

## RcsbEntitySourceOrganism
```text
  ├── beg_seq_num : Int?  # The beginning polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequ
  ├── common_name : String?  # The common name for the source organism assigned by the PDB depositor.
  ├── end_seq_num : Int?  # The ending polymer sequence position for the polymer section corresponding  to this source.   A reference to the sequenc
  ├── ncbi_common_names : String[]?  # Common names associated with this taxonomy code aggregated by the NCBI Taxonomy Database.    These name correspond to th
  ├── ncbi_parent_scientific_name : String?  # A parent scientific name in the NCBI taxonomy hierarchy of the source organism assigned by the PDB depositor.   For cell
  ├── ncbi_scientific_name : String?  # The scientific name associated with this taxonomy code aggregated by the NCBI Taxonomy Database.    This name correspond
  ├── ncbi_taxonomy_id : Int?  # NCBI Taxonomy identifier for the gene source organism assigned by the PDB depositor.   Reference:   Wheeler DL, Chappey 
  ├── pdbx_src_id : Int  # An identifier for the entity segment.
  ├── provenance_source : String?  # Reference to the provenance of the source organism details for the entity.   Primary data indicates information obtained
  ├── rcsb_gene_name : RcsbEntitySourceOrganismRcsbGeneName[]?
  ├── scientific_name : String?  # The scientific name of the source organism assigned by the PDB depositor.
  ├── source_type : String?  # The source type for the entity  Allowable values: genetically engineered, natural, synthetic
  ├── taxonomy_lineage : RcsbEntitySourceOrganismTaxonomyLineage[]?
```

## RcsbEntitySourceOrganismRcsbGeneName
```text
  ├── provenance_source : String?  # A code indicating the provenance of the source organism details for the entity  Allowable values: NCBI, PDB Primary Data
  ├── value : String?  # Gene name.  Examples: lacA, hemH
```

## RcsbEntitySourceOrganismTaxonomyLineage
```text
  ├── depth : Int?  # Members of the NCBI Taxonomy lineage as parent taxonomy lineage depth (1-N)
  ├── id : String?  # Members of the NCBI Taxonomy lineage as parent taxonomy idcodes.  Examples: 9606, 10090
  ├── name : String?  # Memebers of the NCBI Taxonomy lineage as parent taxonomy names.  Examples: Homo sapiens, Mus musculus
```

## RcsbEntryContainerIdentifiers
```text
  ├── assembly_ids : String[]?  # List of identifiers for assemblies generated from the entry.
  ├── branched_entity_ids : String[]?  # List of identifiers for the branched entity constituents for the entry.
  ├── emdb_ids : String[]?  # List of EMDB identifiers for the 3D electron microscopy density maps  used in the production of the structure model.
  ├── entity_ids : String[]?  # List of identifiers or the entity constituents for the entry.
  ├── entry_id : String  # Entry identifier for the container.  Examples: 4HHB, AF_AFP60325F1, MA_MABAKCEPC0019
  ├── model_ids : Int[]?  # List of PDB model identifiers for the entry.
  ├── non_polymer_entity_ids : String[]?  # List of identifiers for the non-polymer entity constituents for the entry.
  ├── polymer_entity_ids : String[]?  # List of identifiers for the polymer entity constituents for the entry.
  ├── pubmed_id : Int?  # Unique integer value assigned to each PubMed record.
  ├── rcsb_id : String?  # A unique identifier for each object in this entry container.  Examples: 1KIP
  ├── related_emdb_ids : String[]?  # List of EMDB identifiers for the 3D electron microscopy density maps  related to the structure model.
  ├── water_entity_ids : String[]?  # List of identifiers for the solvent/water entity constituents for the entry.
```

## RcsbEntryGroupMembership
```text
  ├── aggregation_method : String  # Method used to establish group membership  Allowable values: matching_deposit_group_id
  ├── group_id : String  # A unique identifier for a group of entries  Examples: G_1001001
```

## RcsbEntryInfo
```text
  ├── assembly_count : Int?  # The number of assemblies defined for this entry including the deposited assembly.
  ├── branched_entity_count : Int?  # The number of distinct branched entities in the structure entry.
  ├── branched_molecular_weight_maximum : Float?  # The maximum molecular mass (KDa) of a branched entity in the deposited structure entry.  Examples: null, null
  ├── branched_molecular_weight_minimum : Float?  # The minimum molecular mass (KDa) of a branched entity in the deposited structure entry.  Examples: null, null
  ├── cis_peptide_count : Int?  # The number of cis-peptide linkages per deposited structure model.
  ├── deposited_atom_count : Int?  # The number of heavy atom coordinates records per deposited structure model.
  ├── deposited_deuterated_water_count : Int?  # The number of deuterated water molecules per deposited structure model.
  ├── deposited_hydrogen_atom_count : Int?  # The number of hydrogen atom coordinates records per deposited structure model.
  ├── deposited_model_count : Int?  # The number of model structures deposited.
  ├── deposited_modeled_polymer_monomer_count : Int?  # The number of modeled polymer monomers in the deposited coordinate data.  This is the total count of monomers with repor
  ├── deposited_nonpolymer_entity_instance_count : Int?  # The number of non-polymer instances in the deposited data set.  This is the total count of non-polymer entity instances 
  ├── deposited_polymer_entity_instance_count : Int?  # The number of polymer instances in the deposited data set.  This is the total count of polymer entity instances reported
  ├── deposited_polymer_monomer_count : Int?  # The number of polymer monomers in sample entity instances in the deposited data set.  This is the total count of monomer
  ├── deposited_solvent_atom_count : Int?  # The number of heavy solvent atom coordinates records per deposited structure model.
  ├── deposited_unmodeled_polymer_monomer_count : Int?  # The number of unmodeled polymer monomers in the deposited coordinate data. This is  the total count of monomers with unr
  ├── diffrn_radiation_wavelength_maximum : Float?  # The maximum radiation wavelength in angstroms.
  ├── diffrn_radiation_wavelength_minimum : Float?  # The minimum radiation wavelength in angstroms.
  ├── diffrn_resolution_high : RcsbEntryInfoDiffrnResolutionHigh?
  ├── disulfide_bond_count : Int?  # The number of disulfide bonds per deposited structure model.
  ├── entity_count : Int?  # The number of distinct polymer, non-polymer, branched molecular, and solvent entities per deposited structure model.
  ├── experimental_method : String?  # The category of experimental method(s) used to determine the structure entry.  Allowable values: EM, Integrative, Multip
  ├── experimental_method_count : Int?  # The number of experimental methods contributing data to the structure determination.
  ├── ihm_multi_scale_flag : String?  # Multi-scale modeling flag for integrative structures.  Allowable values: N, Y
  ├── ihm_multi_state_flag : String?  # Multi-state modeling flag for integrative structures.  Allowable values: N, Y
  ├── ihm_ordered_state_flag : String?  # Ordered-state modeling flag for integrative structures.  Allowable values: N, Y
  ├── ihm_structure_description : String?  # Description of the integrative structure.
  ├── inter_mol_covalent_bond_count : Int?  # The number of intermolecular covalent bonds.
  ├── inter_mol_metalic_bond_count : Int?  # The number of intermolecular metalic bonds.
  ├── molecular_weight : Float?  # The molecular mass (KDa) of polymer and non-polymer entities (exclusive of solvent) in the deposited structure entry.  E
  ├── na_polymer_entity_types : String?  # Nucleic acid polymer entity type categories describing the entry.  Allowable values: DNA (only), DNA/RNA (only), NA-hybr
  ├── ndb_struct_conf_na_feature_combined : String[]?  # This data item identifies secondary structure  features of nucleic acids in the entry.  Allowable values: a-form double 
  ├── nonpolymer_bound_components : String[]?  # Bound nonpolymer components in this entry.
  ├── nonpolymer_entity_count : Int?  # The number of distinct non-polymer entities in the structure entry exclusive of solvent.
  ├── nonpolymer_molecular_weight_maximum : Float?  # The maximum molecular mass (KDa) of a non-polymer entity in the deposited structure entry.  Examples: null, null
  ├── nonpolymer_molecular_weight_minimum : Float?  # The minimum molecular mass (KDa) of a non-polymer entity in the deposited structure entry.  Examples: null, null
  ├── polymer_composition : String?  # Categories describing the polymer entity composition for the entry.  Allowable values: DNA, DNA/RNA, NA-hybrid, NA/oligo
  ├── polymer_entity_count : Int?  # The number of distinct polymer entities in the structure entry.
  ├── polymer_entity_count_DNA : Int?  # The number of distinct DNA polymer entities.
  ├── polymer_entity_count_RNA : Int?  # The number of distinct RNA polymer entities.
  ├── polymer_entity_count_nucleic_acid : Int?  # The number of distinct nucleic acid polymer entities (DNA or RNA).
  ├── polymer_entity_count_nucleic_acid_hybrid : Int?  # The number of distinct hybrid nucleic acid polymer entities.
  ├── polymer_entity_count_protein : Int?  # The number of distinct protein polymer entities.
  ├── polymer_entity_taxonomy_count : Int?  # The number of distinct taxonomies represented among the polymer entities in the entry.
  ├── polymer_molecular_weight_maximum : Float?  # The maximum molecular mass (KDa) of a polymer entity in the deposited structure entry.  Examples: null, null
  ├── polymer_molecular_weight_minimum : Float?  # The minimum molecular mass (KDa) of a polymer entity in the deposited structure entry.  Examples: null, null
  ├── polymer_monomer_count_maximum : Int?  # The maximum monomer count of a polymer entity per deposited structure model.
  ├── polymer_monomer_count_minimum : Int?  # The minimum monomer count of a polymer entity per deposited structure model.
  ├── representative_model : Int?  # The chosen representative model.
  ├── resolution_combined : Float[]?  # Combined estimates of experimental resolution contributing to the refined structural model.  Resolution reported in "ref
  ├── selected_polymer_entity_types : String?  # Selected polymer entity type categories describing the entry.  Allowable values: Nucleic acid (only), Oligosaccharide (o
  ├── software_programs_combined : String[]?  # Combined list of software programs names reported in connection with the production of this entry.
  ├── solvent_entity_count : Int?  # The number of distinct solvent entities per deposited structure model.
  ├── structure_determination_methodology : String  # Indicates if the structure was determined using experimental or computational methods.  Allowable values: computational,
  ├── structure_determination_methodology_priority : Int?  # Indicates the priority of the value in _rcsb_entry_info.structure_determination_methodology.  The lower the number the h
```

## RcsbEntryInfoDiffrnResolutionHigh
```text
  ├── provenance_source : String?  # The provenence source for the high resolution limit of data collection.  Allowable values: Depositor assigned, From refi
  ├── value : Float?  # The high resolution limit of data collection.
```

## RcsbExternalReferences
```text
  ├── id : String  # ID (accession) from external resource linked to this entry.  Examples: 1BMR
  ├── link : String?  # Link to this entry in external resource
  ├── type : String  # Internal identifier for external resources  Allowable values: BMRB, EM DATA RESOURCE, NAKB, NDB, OLDERADO, PROTEIN DIFFR
```

## RcsbGenomicLineage
```text
  ├── depth : Int?  # Classification hierarchy depth.
  ├── id : String?  # Automatically assigned ID that uniquely identifies taxonomy, chromosome or gene in the Genome Location Browser.  Example
  ├── name : String?  # A human-readable term name.  Examples: Homo sapiens, 8, defensin beta 103A
```

## RcsbGroupAccessionInfo
```text
  ├── version : Int  # Identifies the version of the groups solution
```

## RcsbGroupAggregationMethod
```text
  ├── method : RcsbGroupAggregationMethodMethod  # The details on a method used to calculate cluster solutions
  ├── similarity_criteria : RcsbGroupAggregationMethodSimilarityCriteria?
  ├── type : String  # Specifies the type of similarity criteria used to aggregate members into higher levels in the hierarchy  Allowable value
```

## RcsbGroupAggregationMethodMethod
```text
  ├── details : MethodDetails[]?  # Additional details describing the clustering process
  ├── name : String  # The name of the software or the method used to calculate cluster solutions  Allowable values: mmseqs2, matching_referenc
  ├── version : String?  # The version of the software.  Examples: v1.0, 3.1-2, unknown
```

## RcsbGroupAggregationMethodSimilarityCriteria
```text
  ├── similarity_function : String?  # A function or similarity measure that quantifies the similarity between two members  Allowable values: rmsd, sequence_id
```

## RcsbGroupContainerIdentifiers
```text
  ├── group_id : String  # A unique textual identifier for a group
  ├── group_member_ids : String[]  # Member identifiers representing a group
  ├── group_provenance_id : String  # A unique group provenance identifier  Allowable values: provenance_sequence_identity, provenance_matching_uniprot_access
  ├── parent_member_ids : String[]?  # Member identifiers representing a higher level in the groping hierarchy that has parent-child relationship
```

## RcsbGroupInfo
```text
  ├── group_description : String?
  ├── group_members_count : Int
  ├── group_members_granularity : String  # Granularity of group members identifiers  Allowable values: assembly, entry, polymer_entity, non_polymer_entity, polymer
  ├── group_name : String?
```

## RcsbGroupProvenanceContainerIdentifiers
```text
  ├── group_provenance_id : String  # A unique group provenance identifier  Allowable values: provenance_sequence_identity, provenance_matching_uniprot_access
```

## RcsbGroupRelated
```text
  ├── resource_accession_code : String?  # A unique code assigned to a reference related the group  Examples: P69905
  ├── resource_name : String?  # Defines the type of the resource describing related references  Examples: UniProt
```

## RcsbGroupStatistics
```text
  ├── similarity_cutoff : Float?  # The desired lower limit for the similarity between two members that belong to the same group
  ├── similarity_score_max : Float?  # Similarity score between two most similar group members
  ├── similarity_score_min : Float?  # Similarity score between two least similar group members
```

## RcsbIhmDatasetList
```text
  ├── count : Int?  # Number of input datasets used in integrative modeling.
  ├── name : String  # Name of input dataset used in integrative modeling.  Allowable values: 2DEM class average, 3DEM volume, CX-MS data, Comp
  ├── type : String?  # Type of input dataset used in integrative modeling.  Allowable values: Computed restraints, Experimental data, Other, St
```

## RcsbIhmDatasetSourceDbReference
```text
  ├── accession_code : String  # Accession code for the input dataset.  Examples: 5FM1, EMD-2799, SASDA82, PXD003381, MA-CO2KC
  ├── db_name : String  # Name of the source database for the input dataset.  Allowable values: AlphaFoldDB, BMRB, BMRbig, BioGRID, EMDB, EMPIAR, 
```

## RcsbInterfaceContainerIdentifiers
```text
  ├── assembly_id : String  # This item references an assembly in pdbx_struct_assembly
  ├── entry_id : String  # Entry identifier for the container.
  ├── interface_entity_id : String?  # Identifier for NCS-equivalent interfaces within the assembly (same entity_ids on both sides)  Examples: 1, 2
  ├── interface_id : String  # Identifier for the geometrically equivalent (same asym_ids on either side) interfaces within the assembly  Examples: 1, 
  ├── rcsb_id : String  # Unique identifier for the document  Examples: 2UZI-1.A.B?1
```

## RcsbInterfaceInfo
```text
  ├── interface_area : Float?  # Total interface buried surface area
  ├── interface_character : String?  # Allowable values: homo, hetero.
  ├── num_core_interface_residues : Int?  # Number of core interface residues, defined as those that bury >90% accessible surface area with respect to the unbound s
  ├── num_interface_residues : Int?  # Number of interface residues, defined as those with burial fraction > 0
  ├── polymer_composition : String?  # Allowable values: Nucleic acid (only), Protein (only), Protein/NA.
  ├── self_jaccard_contact_score : Float?  # The Jaccard score (intersection over union) of interface contacts in homomeric interfaces, comparing contact sets left-r
```

## RcsbInterfacePartner
```text
  ├── interface_partner_feature : RcsbInterfacePartnerInterfacePartnerFeature[]?
  ├── interface_partner_identifier : RcsbInterfacePartnerInterfacePartnerIdentifier?
```

## RcsbInterfacePartnerInterfacePartnerFeature
```text
  ├── additional_properties : InterfacePartnerFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : InterfacePartnerFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that assigned the feature.  Examples: NACCESS
  ├── type : String?  # A type or category of the feature.  Allowable values: ASA_UNBOUND, ASA_BOUND
```

## RcsbInterfacePartnerInterfacePartnerIdentifier
```text
  ├── asym_id : String  # Instance identifier for this container.
  ├── entity_id : String  # Polymer entity identifier for the container.
```

## RcsbLatestRevision
```text
  ├── major_revision : Int?  # The major version number of the latest revision.
  ├── minor_revision : Int?  # The minor version number of the latest revision.
  ├── revision_date : Date?  # The release date of the latest revision item.  Examples: 2020-02-11, 2018-10-23
```

## RcsbLigandNeighbors
```text
  ├── alt_id : String?  # Alternate conformer identifier for the target instance.
  ├── atom_id : String?  # The atom identifier for the target instance.  Examples: O1, N1, C1
  ├── auth_seq_id : Int?  # The author residue index for the target instance.
  ├── comp_id : String?  # Component identifier for the target instance.
  ├── distance : Float?  # Distance value for this ligand interaction.
  ├── ligand_alt_id : String?  # Alternate conformer identifier for the ligand interaction.
  ├── ligand_asym_id : String?  # The entity instance identifier for the ligand interaction.  Examples: A, B
  ├── ligand_atom_id : String?  # The atom identifier for the ligand interaction.  Examples: OG, OE1, CD1
  ├── ligand_comp_id : String?  # The chemical component identifier for the ligand interaction.  Examples: ASN, TRP, SER
  ├── ligand_entity_id : String?  # The entity identifier for the ligand of interaction.  Examples: 1, 2
  ├── ligand_is_bound : String?  # A flag to indicate the nature of the ligand interaction is covalent or metal-coordination.  Allowable values: N, Y
  ├── ligand_model_id : Int?  # Model identifier for the ligand interaction.
  ├── seq_id : Int?  # The sequence position for the target instance.
```

## RcsbMaQaMetricGlobal
```text
  ├── ma_qa_metric_global : RcsbMaQaMetricGlobalMaQaMetricGlobal[]?
  ├── model_id : Int  # The model identifier.
```

## RcsbMaQaMetricGlobalMaQaMetricGlobal
```text
  ├── description : String?  # Description of the global QA metric.  Examples: confidence score predicting accuracy according to the CA-only Local Dist
  ├── name : String  # Name of the global QA metric.  Examples: pLDDT
  ├── type : String  # The type of global QA metric.  Allowable values: PAE, contact probability, distance, energy, ipTM, normalized score, oth
  ├── type_other_details : String?  # Details for other type of global QA metric.
  ├── value : Float  # Value of the global QA metric.  Examples: null
```

## RcsbMembraneLineage
```text
  ├── depth : Int?  # Hierarchy depth.
  ├── id : String?  # Automatically assigned ID for membrane classification term in the Membrane Protein Browser.  Examples: MONOTOPIC MEMBRAN
  ├── name : String?  # Membrane protein classification term.
```

## RcsbNonpolymerEntity
```text
  ├── details : String?  # A description of special aspects of the entity.
  ├── formula_weight : Float?  # Formula mass (KDa) of the entity.
  ├── pdbx_description : String?  # A description of the nonpolymer entity.
  ├── pdbx_number_of_molecules : Int?  # The number of molecules of the nonpolymer entity in the entry.
```

## RcsbNonpolymerEntityAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbNonpolymerEntityAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── comp_id : String?  # Non-polymer(ligand) chemical component identifier for the entity.  Examples: GTP, STN
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB
  ├── type : String  # A type or category of the annotation.  Allowable values: SUBJECT_OF_INVESTIGATION
```

## RcsbNonpolymerEntityAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbNonpolymerEntityContainerIdentifiers
```text
  ├── asym_ids : String[]?  # Instance identifiers corresponding to copies of the entity in this container.
  ├── auth_asym_ids : String[]?  # Author instance identifiers corresponding to copies of the entity in this container.
  ├── chem_ref_def_id : String?  # The chemical reference definition identifier for the entity in this container.  Examples: PRD_000010
  ├── entity_id : String  # Entity identifier for the container.  Examples: 1, 2
  ├── entry_id : String  # Entry identifier for the container.  Examples: 4HHB, 1KIP
  ├── nonpolymer_comp_id : String?  # Non-polymer(ligand) chemical component identifier for the entity in this container.  Examples: GTP, STN
  ├── prd_id : String?  # The BIRD identifier for the entity in this container.  Examples: PRD_000010
  ├── rcsb_id : String?  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── reference_chemical_identifiers_provenance_source : String[]?  # Source of the reference database assignment  Allowable values: PDB, RCSB
  ├── reference_chemical_identifiers_resource_accession : String[]?  # Reference resource accession code
  ├── reference_chemical_identifiers_resource_name : String[]?  # Reference resource name  Allowable values: ChEBI, ChEMBL, DrugBank, PubChem
```

## RcsbNonpolymerEntityFeature
```text
  ├── additional_properties : RcsbNonpolymerEntityFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── comp_id : String?  # Non-polymer(ligand) chemical component identifier for the entity.  Examples: GTP, STN
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: PDB
  ├── type : String  # A type or category of the feature.  Allowable values: SUBJECT_OF_INVESTIGATION
  ├── value : Float?  # The feature value.
```

## RcsbNonpolymerEntityFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbNonpolymerEntityFeatureSummary
```text
  ├── comp_id : String?  # Non-polymer(ligand) chemical component identifier for the entity.  Examples: GTP, STN
  ├── count : Int?  # The feature count.
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: SUBJECT_OF_INVESTIGATION
```

## RcsbNonpolymerEntityInstanceContainerIdentifiers
```text
  ├── asym_id : String  # Instance identifier for this container.
  ├── auth_asym_id : String?  # Author instance identifier for this container.
  ├── auth_seq_id : String?  # Residue number for non-polymer entity instance.
  ├── comp_id : String?  # Component identifier for non-polymer entity instance.
  ├── entity_id : String?  # Entity identifier for the container.
  ├── entry_id : String  # Entry identifier for the container.
  ├── rcsb_id : String?  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
```

## RcsbNonpolymerEntityKeywords
```text
  ├── text : String?  # Keywords describing this non-polymer entity.
```

## RcsbNonpolymerEntityNameCom
```text
  ├── name : String  # A common name for the nonpolymer entity.
```

## RcsbNonpolymerInstanceAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbNonpolymerInstanceAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── comp_id : String?  # Non-polymer (ligand) chemical component identifier.  Examples: ATP
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB
  ├── type : String  # A type or category of the annotation.  Allowable values: HAS_COVALENT_LINKAGE, HAS_METAL_COORDINATION_LINKAGE, HAS_NO_CO
```

## RcsbNonpolymerInstanceAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbNonpolymerInstanceFeature
```text
  ├── additional_properties : RcsbNonpolymerInstanceFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── comp_id : String?  # Component identifier for non-polymer entity instance.
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_value : RcsbNonpolymerInstanceFeatureFeatureValue[]?
  ├── name : String?  # A name for the feature.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: PDB
  ├── type : String?  # A type or category of the feature.  Allowable values: HAS_COVALENT_LINKAGE, HAS_METAL_COORDINATION_LINKAGE, MODELED_ATOM
```

## RcsbNonpolymerInstanceFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Examples: bond_distance, bond_angle
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbNonpolymerInstanceFeatureFeatureValue
```text
  ├── comp_id : String?  # The chemical component identifier for the instance of the feature value.  Examples: ATP,, STN
  ├── details : String?  # Specific details about the feature.  Examples: C1,C2, C1,C2,C3
  ├── reference : Float?  # The reference value of the feature.  Examples: null, null
  ├── reported : Float?  # The reported value of the feature.  Examples: null, null
  ├── uncertainty_estimate : Float?  # The estimated uncertainty of the reported feature value.  Examples: null, null
  ├── uncertainty_estimate_type : String?  # The type of estimated uncertainty for the reported feature value.  Allowable values: Z-Score
```

## RcsbNonpolymerInstanceFeatureSummary
```text
  ├── comp_id : String?  # Component identifier for non-polymer entity instance.
  ├── count : Int?  # The feature count.
  ├── coverage : Float?  # The fractional feature coverage relative to the full entity sequence.  Examples: null, null
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: HAS_COVALENT_LINKAGE, HAS_METAL_COORDINATION_LINKAGE, MODELED_ATOMS,
```

## RcsbNonpolymerInstanceValidationScore
```text
  ├── Q_score : Float?  # The Q-score for the non-polymer instance.  Examples: null, null
  ├── RSCC : Float?  # The real space correlation coefficient (RSCC) for the non-polymer entity instance.  Examples: null, null
  ├── RSR : Float?  # The real space R-value (RSR) for the non-polymer entity instance.  Examples: null, null
  ├── alt_id : String?  # Alternate conformer identifier for the non-polymer entity instance.
  ├── average_occupancy : Float?  # The average heavy atom occupancy for coordinate records for the non-polymer entity instance.  Examples: null, null
  ├── completeness : Float?  # The reported fraction of atomic coordinate records for the non-polymer entity instance.  Examples: null, null
  ├── intermolecular_clashes : Int?  # The number of intermolecular MolProbity clashes cacluated for reported atomic coordinate records.
  ├── is_best_instance : String?  # This molecular instance is ranked as the best quality instance of this nonpolymer entity.  Allowable values: N, Y
  ├── is_subject_of_investigation : String?  # This molecular entity is identified as the subject of the current study.  Allowable values: N, Y
  ├── is_subject_of_investigation_provenance : String?  # The provenance for the selection of the molecular entity identified as the subject of the current study.  Allowable valu
  ├── mogul_angle_outliers : Int?  # Number of bond angle outliers obtained from a CCDC Mogul survey of bond angles  in the CSD small    molecule crystal str
  ├── mogul_angles_RMSZ : Float?  # The root-mean-square value of the Z-scores of bond angles for the non-polymer instance in degrees obtained from a CCDC M
  ├── mogul_bond_outliers : Int?  # Number of bond distance outliers obtained from a CCDC Mogul survey of bond lengths in the CSD small    molecule crystal 
  ├── mogul_bonds_RMSZ : Float?  # The root-mean-square value of the Z-scores of bond lengths for the nonpolymer instance in Angstroms obtained from a CCDC
  ├── natoms_eds : Int?  # The number of atoms in the non-polymer instance returned by the EDS software.
  ├── num_mogul_angles_RMSZ : Int?  # The number of bond angles compared to "standard geometry" made using the Mogul program.
  ├── num_mogul_bonds_RMSZ : Int?  # The number of bond lengths compared to "standard geometry" made using the Mogul program.
  ├── ranking_model_fit : Float?  # The ranking of the model fit score component.  Examples: null, null
  ├── ranking_model_geometry : Float?  # The ranking of the model geometry score component.  Examples: null, null
  ├── score_model_fit : Float?  # The value of the model fit score component.  Examples: null, null
  ├── score_model_geometry : Float?  # The value of the model geometry score component.  Examples: null, null
  ├── stereo_outliers : Int?  # Number of stereochemical/chirality errors.
  ├── type : String?  # Score type.  Allowable values: RCSB_LIGAND_QUALITY_SCORE_2021
```

## RcsbNonpolymerStructConn
```text
  ├── connect_partner : RcsbNonpolymerStructConnConnectPartner?
  ├── connect_target : RcsbNonpolymerStructConnConnectTarget?
  ├── connect_type : String?  # The connection type.  Allowable values: covalent bond, disulfide bridge, hydrogen bond, ionic interaction, metal coordin
  ├── description : String?  # A description of special details of the connection.  Examples: Watson-Crick base pair
  ├── dist_value : Float?  # Distance value for this contact.
  ├── id : String?  # The value of _rcsb_nonpolymer_struct_conn.id is an identifier for connection.   Note that this item need not be a number
  ├── ordinal_id : Int  # The value of _rcsb_nonpolymer_struct_conn.id must uniquely identify a record in  the rcsb_nonpolymer_struct_conn list.
  ├── role : String?  # The chemical or structural role of the interaction  Allowable values: C-Mannosylation, N-Glycosylation, O-Glycosylation,
  ├── value_order : String?  # The chemical bond order associated with the specified atoms in  this contact.  Allowable values: doub, quad, sing, trip
```

## RcsbNonpolymerStructConnConnectPartner
```text
  ├── label_alt_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_asym_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_atom_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _chem_comp_
  ├── label_comp_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_seq_id : Int?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_nonpolymer_struct_conn.conne
```

## RcsbNonpolymerStructConnConnectTarget
```text
  ├── auth_asym_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── auth_seq_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── label_alt_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_asym_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_atom_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_comp_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_seq_id : Int?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.c
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_nonpolymer_struct_conn.label
```

## RcsbPfamContainerIdentifiers
```text
  ├── pfam_id : String?  # Accession number of Pfam entry.
```

## RcsbPolymerEntity
```text
  ├── details : String?  # A description of special aspects of the entity.
  ├── formula_weight : Float?  # Formula mass (KDa) of the entity.  Examples: null, null
  ├── pdbx_description : String?  # A description of the polymer entity.  Examples: Green fluorescent protein, 23S ribosomal RNA, NAD-dependent protein deac
  ├── pdbx_ec : String?  # Enzyme Commission (EC) number(s)  Examples: 2.7.7.7
  ├── pdbx_fragment : String?  # Polymer entity fragment description(s).  Examples: KLENOW FRAGMENT, REPLICASE OPERATOR HAIRPIN, C-TERMINAL DOMAIN
  ├── pdbx_mutation : String?  # Details about any polymer entity mutation(s).  Examples: Y31H, DEL(298-323)
  ├── pdbx_number_of_molecules : Int?  # The number of molecules of the entity in the entry.
  ├── rcsb_ec_lineage : RcsbPolymerEntityRcsbEcLineage[]?
  ├── rcsb_enzyme_class_combined : RcsbPolymerEntityRcsbEnzymeClassCombined[]?
  ├── rcsb_macromolecular_names_combined : RcsbPolymerEntityRcsbMacromolecularNamesCombined[]?
  ├── rcsb_multiple_source_flag : String?  # A code indicating the entity has multiple biological sources.  Allowable values: N, Y
  ├── rcsb_polymer_name_combined : RcsbPolymerEntityRcsbPolymerNameCombined?
  ├── rcsb_source_part_count : Int?  # The number of biological sources for the polymer entity. Multiple source contributions  may come from the same organism 
  ├── rcsb_source_taxonomy_count : Int?  # The number of distinct source taxonomies for the polymer entity. Commonly used to identify chimeric polymers.
  ├── src_method : String?  # The method by which the sample for the polymer entity was produced.  Entities isolated directly from natural sources (ti
```

## RcsbPolymerEntityAlign
```text
  ├── aligned_regions : RcsbPolymerEntityAlignAlignedRegions[]?
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the reference sequence.  Examples: PDB, SIFTS, R
  ├── reference_database_accession : String?  # Reference sequence accession code.  Examples: Q9HD40
  ├── reference_database_isoform : String?  # Reference sequence isoform identifier.  Examples: P01116-2
  ├── reference_database_name : String?  # Reference sequence database name.  Allowable values: EMBL, GenBank, NDB, NORINE, PDB, PIR, PRF, RefSeq, UniProt
```

## RcsbPolymerEntityAlignAlignedRegions
```text
  ├── entity_beg_seq_id : Int?  # An identifier for the monomer in the entity sequence at which this segment of the alignment begins.
  ├── length : Int?  # The length of this segment of the alignment.
  ├── ref_beg_seq_id : Int?  # An identifier for the monomer in the reference sequence at which this segment of the alignment begins.
```

## RcsbPolymerEntityAnnotation
```text
  ├── additional_properties : RcsbPolymerEntityAnnotationAdditionalProperties[]?
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbPolymerEntityAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB, UniProt
  ├── type : String  # A type or category of the annotation.  Allowable values: CARD, GO, GlyCosmos, GlyGen, InterPro, MemProtMD, OPM, PDBTM, P
```

## RcsbPolymerEntityAnnotationAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: CARD_ARO_CATEGORY, CARD_ARO_CVTERM_ID, CARD_ARO_DRUG_CLASS, CARD_ARO_RE
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbPolymerEntityAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbPolymerEntityContainerIdentifiers
```text
  ├── asym_ids : String[]?  # Instance identifiers corresponding to copies of the entity in this container.
  ├── auth_asym_ids : String[]?  # Author instance identifiers corresponding to copies of the entity in this container.
  ├── chem_comp_monomers : String[]?  # Unique list of monomer chemical component identifiers in the polymer entity in this container.
  ├── chem_comp_nstd_monomers : String[]?  # Unique list of non-standard monomer chemical component identifiers in the polymer entity in this container.
  ├── chem_ref_def_id : String?  # The chemical reference definition identifier for the entity in this container.  Examples: PRD_000010
  ├── entity_id : String  # Entity identifier for the container.  Examples: 1, 2
  ├── entry_id : String  # Entry identifier for the container.  Examples: 4HHB, 1KIP
  ├── prd_id : String?  # The BIRD identifier for the entity in this container.  Examples: PRD_000010
  ├── rcsb_id : String?  # A unique identifier for each object in this entity container formed by  an underscore separated concatenation of entry a
  ├── reference_sequence_identifiers : RcsbPolymerEntityContainerIdentifiersReferenceSequenceIdentifiers[]?
  ├── uniprot_ids : String[]?  # Uniprot accession codes assigned to polymeric entities.
```

## RcsbPolymerEntityContainerIdentifiersReferenceSequenceIdentifiers
```text
  ├── database_accession : String?  # Reference database accession code  Examples: P01116, 55771382
  ├── database_isoform : String?  # Reference database identifier for the sequence isoform  Examples: P01116-2
  ├── database_name : String?  # Reference database name  Allowable values: EMBL, GenBank, NDB, NORINE, PDB, PIR, PRF, RefSeq, UniProt
  ├── entity_sequence_coverage : Float?  # Indicates what fraction of this polymer entity sequence is covered by the reference sequence.  Examples: null, null
  ├── provenance_source : String?  # Source of the reference database assignment  Allowable values: PDB, RCSB, SIFTS, UniProt
  ├── reference_sequence_coverage : Float?  # Indicates what fraction of the reference sequence is covered by this polymer entity sequence.  Examples: null, null
```

## RcsbPolymerEntityFeature
```text
  ├── additional_properties : RcsbPolymerEntityFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbPolymerEntityFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: PDB
  ├── reference_scheme : String?  # Code residue coordinate system for the assigned feature.  Allowable values: NCBI, PDB entity, UniProt
  ├── type : String  # A type or category of the feature.  Allowable values: CARD_MODEL, IMGT_ANTIBODY_DESCRIPTION, IMGT_ANTIBODY_DOMAIN_NAME, 
```

## RcsbPolymerEntityFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: CARD_MODEL_DESCRIPTION, CARD_MODEL_ORGANISM, PARENT_COMP_ID
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbPolymerEntityFeatureFeaturePositions
```text
  ├── beg_comp_id : String?  # An identifier for the leading monomer corresponding to the feature assignment.  Examples: TRP, VAL
  ├── beg_seq_id : Int  # An identifier for the monomer at which this segment of the feature begins.
  ├── end_seq_id : Int?  # An identifier for the monomer at which this segment of the feature ends.
  ├── value : Float?  # The value for the feature over this monomer segment.  Examples: null, null
  ├── values : Float[]?  # The value(s) for the feature over this monomer segment.
```

## RcsbPolymerEntityFeatureSummary
```text
  ├── count : Int?  # The feature count.
  ├── coverage : Float?  # The fractional feature coverage relative to the full entity sequence.  For instance, the fraction of features such as mu
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: CARD_MODEL, IMGT_ANTIBODY_DESCRIPTION, IMGT_ANTIBODY_DOMAIN_NAME, IM
```

## RcsbPolymerEntityGroupMembersRankings
```text
  ├── group_members : RcsbPolymerEntityGroupMembersRankingsGroupMembers[]
  ├── ranking_criteria_type : String  # Defines ranking option applicable to group members  Allowable values: coverage
```

## RcsbPolymerEntityGroupMembersRankingsGroupMembers
```text
  ├── member_id : String
  ├── original_score : Float?  # Quantifies the criteria used for ranking
  ├── rank : Int  # Reflects a relationship between group members such that, for any two members the first is ranked higher (smaller rank va
```

## RcsbPolymerEntityGroupMembership
```text
  ├── aggregation_method : String  # Method used to establish group membership  Allowable values: matching_uniprot_accession, sequence_identity
  ├── aligned_regions : RcsbPolymerEntityGroupMembershipAlignedRegions[]?
  ├── group_id : String  # A unique identifier for a group of entities  Examples: 1_100, P00003
  ├── similarity_cutoff : Float?  # Degree of similarity expressed as a floating-point number
```

## RcsbPolymerEntityGroupMembershipAlignedRegions
```text
  ├── entity_beg_seq_id : Int?  # An identifier for the monomer in the entity sequence at which this segment of the alignment begins.
  ├── length : Int?  # The length of this segment of the alignment.
  ├── ref_beg_seq_id : Int?  # An identifier for the monomer in the reference sequence at which this segment of the alignment begins.
```

## RcsbPolymerEntityGroupSequenceAlignment
```text
  ├── abstract_reference : RcsbPolymerEntityGroupSequenceAlignmentAbstractReference  # Abstract reference where group members can be aligned to generate a MSA
  ├── group_members_alignment : RcsbPolymerEntityGroupSequenceAlignmentGroupMembersAlignment[]  # Alignment with a core_entity canonical sequence
```

## RcsbPolymerEntityGroupSequenceAlignmentAbstractReference
```text
  ├── length : Int  # Abstract reference length
  ├── sequence : String?  # Sequence that represents the abstract reference
```

## RcsbPolymerEntityGroupSequenceAlignmentGroupMembersAlignment
```text
  ├── aligned_regions : Int[]  # Alignment region encoded as a triplet [query_begin, target_begin, length]
  ├── member_id : String
  ├── scores : GroupMembersAlignmentScores  # Alignment scores
```

## RcsbPolymerEntityInstanceContainerIdentifiers
```text
  ├── asym_id : String  # Instance identifier for this container.
  ├── auth_asym_id : String?  # Author instance identifier for this container.
  ├── auth_to_entity_poly_seq_mapping : String[]?  # Residue index mappings between author provided and entity polymer sequence positions.   Author residue indices (auth_seq
  ├── entity_id : String?  # Entity identifier for the container.
  ├── entry_id : String  # Entry identifier for the container.
  ├── rcsb_id : String?  # A unique identifier for each object in this entity instance container formed by  an 'dot' (.) separated concatenation of
```

## RcsbPolymerEntityKeywords
```text
  ├── text : String?  # Keywords describing this polymer entity.
```

## RcsbPolymerEntityNameCom
```text
  ├── name : String  # A common name for the polymer entity.  Examples: HIV protease monomer, hemoglobin alpha chain
```

## RcsbPolymerEntityNameSys
```text
  ├── name : String  # The systematic name for the polymer entity.
  ├── system : String?  # The system used to generate the systematic name of the polymer entity.  Examples: Chemical Abstracts conventions
```

## RcsbPolymerEntityRcsbEcLineage
```text
  ├── depth : Int?  # Members of the enzyme classification lineage as parent classification hierarchy depth (1-N).
  ├── id : String?  # Members of the enzyme classification lineage as parent classification codes.  Examples: 2, 2.7.1.153
  ├── name : String?  # Members of the enzyme classification lineage as parent classification names.  Examples: Transferases, phosphatidylinosit
```

## RcsbPolymerEntityRcsbEnzymeClassCombined
```text
  ├── depth : Int?  # The enzyme classification hierarchy depth (1-N).
  ├── ec : String?  # Combined list of enzyme class assignments.
  ├── provenance_source : String?  # Combined list of enzyme class associated provenance sources.  Allowable values: PDB Primary Data, UniProt
```

## RcsbPolymerEntityRcsbMacromolecularNamesCombined
```text
  ├── name : String?  # Combined list of macromolecular names.  Examples: Lysozyme C, Plasmid recombination enzyme, Pyruvate carboxylase
  ├── provenance_code : String?  # Combined list of macromolecular names associated provenance code.   ECO (https://github.com/evidenceontology/evidenceont
  ├── provenance_source : String?  # Combined list of macromolecular names associated name source.  Allowable values: PDB Preferred Name, PDB Synonym
```

## RcsbPolymerEntityRcsbPolymerNameCombined
```text
  ├── names : String[]?  # Protein name annotated by the UniProtKB or macromolecular name assigned by the PDB.
  ├── provenance_source : String?  # Provenance source for the combined protein names.  Allowable values: PDB Description, PDB Preferred Name, UniProt Name
```

## RcsbPolymerInstanceAnnotation
```text
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbPolymerInstanceAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.  Examples: PDB
  ├── type : String  # A type or category of the annotation.  Allowable values: CATH, ECOD, GlyGen, SCOP, SCOP2
```

## RcsbPolymerInstanceAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbPolymerInstanceFeature
```text
  ├── additional_properties : RcsbPolymerInstanceFeatureAdditionalProperties[]?
  ├── assignment_version : String?  # Identifies the version of the feature assignment.  Examples: V4_0_2
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbPolymerInstanceFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── ordinal : Int  # Ordinal identifier for this category
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.  Examples: CATH, SCOP
  ├── reference_scheme : String?  # Code residue coordinate system for the assigned feature.  Allowable values: NCBI, PDB entity, PDB entry, UniProt
  ├── type : String  # A type or category of the feature.  Allowable values: ANGLE_OUTLIER, ANGLE_OUTLIERS, ASA, AVERAGE_OCCUPANCY, BEND, BINDI
```

## RcsbPolymerInstanceFeatureAdditionalProperties
```text
  ├── name : String?  # The additional property name.  Allowable values: CATH_DOMAIN_ID, CATH_NAME, ECOD_DOMAIN_ID, ECOD_FAMILY_NAME, MODELCIF_M
  ├── values : ObjectScalar[]?  # The value(s) of the additional property.
```

## RcsbPolymerInstanceFeatureFeaturePositions
```text
  ├── beg_comp_id : String?  # An identifier for the monomer(s) corresponding to the feature assignment.  Examples: TRP, VAL
  ├── beg_seq_id : Int  # An identifier for the monomer at which this segment of the feature begins.
  ├── end_seq_id : Int?  # An identifier for the monomer at which this segment of the feature ends.
  ├── value : Float?  # The value of the feature over the monomer segment.  Examples: null, null
  ├── values : Float[]?  # The value(s) of the feature over the monomer segment.
```

## RcsbPolymerInstanceFeatureSummary
```text
  ├── count : Int?  # The feature count per polymer chain.
  ├── coverage : Float?  # The fractional feature coverage relative to the full entity sequence.  Examples: null, null
  ├── maximum_length : Int?  # The maximum feature length.
  ├── maximum_value : Float?  # The maximum feature value.  Examples: null, null
  ├── minimum_length : Int?  # The minimum feature length.
  ├── minimum_value : Float?  # The minimum feature value.  Examples: null, null
  ├── type : String?  # Type or category of the feature.  Allowable values: ANGLE_OUTLIER, ANGLE_OUTLIERS, AVERAGE_OCCUPANCY, BEND, BINDING_SITE
```

## RcsbPolymerInstanceInfo
```text
  ├── modeled_residue_count : Int?  # The number of modeled residues in the polymer instance.
```

## RcsbPolymerStructConn
```text
  ├── connect_partner : RcsbPolymerStructConnConnectPartner?
  ├── connect_target : RcsbPolymerStructConnConnectTarget?
  ├── connect_type : String?  # The connection type.  Allowable values: covalent bond, covalent modification of a nucleotide base, covalent modification
  ├── description : String?  # A description of special details of the connection.  Examples: Watson-Crick base pair
  ├── dist_value : Float?  # Distance value for this contact.
  ├── id : String?  # The value of _rcsb_polymer_struct_conn.id is an identifier for connection.   Note that this item need not be a number; i
  ├── ordinal_id : Int  # The value of _rcsb_polymer_struct_conn.id must uniquely identify a record in  the rcsb_polymer_struct_conn list.
  ├── role : String?  # The chemical or structural role of the interaction  Allowable values: C-Mannosylation, N-Glycosylation, O-Glycosylation,
  ├── value_order : String?  # The chemical bond order associated with the specified atoms in  this contact.  Allowable values: doub, quad, sing, trip
```

## RcsbPolymerStructConnConnectPartner
```text
  ├── label_alt_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_asym_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_atom_id : String?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _chem_comp_
  ├── label_comp_id : String  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── label_seq_id : Int?  # A component of the identifier for the partner in the structure  connection.   This data item is a pointer to _atom_site.
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_polymer_struct_conn.connect_
```

## RcsbPolymerStructConnConnectTarget
```text
  ├── auth_asym_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── auth_seq_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.a
  ├── label_alt_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_asym_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_atom_id : String?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_comp_id : String  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.l
  ├── label_seq_id : Int?  # A component of the identifier for the target of the structure  connection.   This data item is a pointer to _atom_site.c
  ├── symmetry : String?  # Describes the symmetry operation that should be applied to the  atom set specified by _rcsb_polymer_struct_conn.label* t
```

## RcsbPrimaryCitation
```text
  ├── book_id_ISBN : String?  # The International Standard Book Number (ISBN) code assigned to  the book cited; relevant for books or book chapters.
  ├── book_publisher : String?  # The name of the publisher of the citation; relevant  for books or book chapters.  Examples: John Wiley and Sons
  ├── book_publisher_city : String?  # The location of the publisher of the citation; relevant  for books or book chapters.  Examples: London
  ├── book_title : String?  # The title of the book in which the citation appeared; relevant  for books or book chapters.
  ├── coordinate_linkage : String?  # _rcsb_primary_citation.coordinate_linkage states whether this citation  is concerned with precisely the set of coordinat
  ├── country : String?  # The country/region of publication; relevant for books  and book chapters.
  ├── id : String  # The value of _rcsb_primary_citation.id must uniquely identify a record in the  CITATION list.   The _rcsb_primary_citati
  ├── journal_abbrev : String?  # Abbreviated name of the cited journal as given in the  Chemical Abstracts Service Source Index.  Examples: J.Mol.Biol., 
  ├── journal_id_ASTM : String?  # The American Society for Testing and Materials (ASTM) code  assigned to the journal cited (also referred to as the CODEN
  ├── journal_id_CSD : String?  # The Cambridge Structural Database (CSD) code assigned to the  journal cited; relevant for journal articles. This is also
  ├── journal_id_ISSN : String?  # The International Standard Serial Number (ISSN) code assigned to  the journal cited; relevant for journal articles.
  ├── journal_issue : String?  # Issue number of the journal cited; relevant for journal  articles.  Examples: 2
  ├── journal_volume : String?  # Volume number of the journal cited; relevant for journal  articles.  Examples: 174
  ├── language : String?  # Language in which the cited article is written.  Examples: German
  ├── page_first : String?  # The first page of the citation; relevant for journal  articles, books and book chapters.
  ├── page_last : String?  # The last page of the citation; relevant for journal  articles, books and book chapters.
  ├── pdbx_database_id_DOI : String?  # Document Object Identifier used by doi.org to uniquely  specify bibliographic entry.  Examples: 10.2345/S138410769700022
  ├── pdbx_database_id_PubMed : Int?  # Ascession number used by PubMed to categorize a specific  bibliographic entry.
  ├── rcsb_ORCID_identifiers : String[]?  # The Open Researcher and Contributor ID (ORCID) identifiers for the citation authors.
  ├── rcsb_authors : String[]?  # Names of the authors of the citation; relevant for journal  articles, books and book chapters.  Names are separated by v
  ├── rcsb_journal_abbrev : String?  # Normalized journal abbreviation.  Examples: Nat Struct Mol Biol
  ├── title : String?  # The title of the citation; relevant for journal articles, books  and book chapters.  Examples: Structure of diferric duc
  ├── year : Int?  # The year of the citation; relevant for journal articles, books  and book chapters.
```

## RcsbPubmedContainerIdentifiers
```text
  ├── pubmed_id : Int?  # UID assigned to each PubMed record.  Examples: null
```

## RcsbPubmedMeshDescriptorsLineage
```text
  ├── depth : Int?  # Hierarchy depth.
  ├── id : String?  # Identifier for MeSH classification term.  Examples: E01.370.225.500.388, H01.181
  ├── name : String?  # MeSH classification term.  Examples: Chemistry, Mammals, Therapeutic Uses
```

## RcsbRelatedTargetReferences
```text
  ├── aligned_target : RcsbRelatedTargetReferencesAlignedTarget[]?
  ├── related_resource_name : String?  # The related target data resource name.  Allowable values: ChEMBL, DrugBank, Pharos
  ├── related_resource_version : String?  # The version of the target data resource.  Examples: 6.11.0
  ├── related_target_id : String?  # An identifier for the target sequence in the related data resource.
  ├── target_taxonomy_id : Int?  # NCBI Taxonomy identifier for the target organism.   Reference:   Wheeler DL, Chappey C, Lash AE, Leipe DD, Madden TL, Sc
```

## RcsbRelatedTargetReferencesAlignedTarget
```text
  ├── entity_beg_seq_id : Int?  # The position of the monomer in the entity sequence at which the alignment begins.
  ├── length : Int?  # The length of the alignment.
  ├── target_beg_seq_id : Int?  # The position of the monomer in the target sequence at which the alignment begins.
```

## RcsbRepositoryHoldingsCurrent
```text
  ├── repository_content_types : String[]?  # The list of content types associated with this entry.  Allowable values: 2fo-fc Map, Combined NMR data (NEF), Combined N
```

## RcsbRepositoryHoldingsCurrentEntryContainerIdentifiers
```text
  ├── assembly_ids : String[]?  # The assembly id codes.
  ├── entry_id : String  # The PDB entry accession code.  Examples: 1KIP
  ├── rcsb_id : String?  # The RCSB entry identifier.  Examples: 1KIP
  ├── update_id : String?  # Identifier for the current data exchange status record.  Examples: 2018_23
```

## RcsbSchemaContainerIdentifiers
```text
  ├── collection_name : String  # Collection name associated with the data in the container.
  ├── collection_schema_version : String?  # Version string for the schema and collection.
  ├── schema_name : String  # Schema name associated with the data in the container.
```

## RcsbStructSymmetry
```text
  ├── clusters : RcsbStructSymmetryClusters[]  # Clusters describe grouping of identical subunits.
  ├── kind : String  # The granularity at which the symmetry calculation is performed. In 'Global Symmetry' all polymeric  subunits in assembly
  ├── oligomeric_state : String  # Oligomeric state refers to a composition of polymeric subunits in quaternary structure.  Quaternary structure may be com
  ├── rotation_axes : RcsbStructSymmetryRotationAxes[]?  # The orientation of the principal rotation (symmetry) axis.
  ├── stoichiometry : String[]  # Stoichiometry of a complex represents the quantitative description and composition of its subunits.
  ├── symbol : String  # Symmetry symbol refers to point group or helical symmetry of identical polymeric subunits in Schoenflies notation.  Cont
  ├── type : String  # Symmetry type refers to point group or helical symmetry of identical polymeric subunits.  Contains point group types (e.
```

## RcsbStructSymmetryClusters
```text
  ├── avg_rmsd : Float?  # Average RMSD between members of a given cluster.
  ├── members : ClustersMembers[]  # Subunits that belong to the cluster, identified by asym_id and optionally by assembly operator id(s).
```

## RcsbStructSymmetryLineage
```text
  ├── depth : Int?  # Hierarchy depth.
  ├── id : String?  # Automatically assigned ID to uniquely identify the symmetry term in the Protein Symmetry Browser.  Examples: Global Symm
  ├── name : String?  # A human-readable term describing protein symmetry.  Examples: Asymmetric, Global Symmetry, C1, Hetero 3-mer
```

## RcsbStructSymmetryRotationAxes
```text
  ├── end : Float[]  # coordinate
  ├── order : Int?  # The number of times (order of rotation) that a subunit can be repeated by a rotation operation,  being transformed into 
  ├── start : Float[]  # coordinate
```

## RcsbTargetCofactors
```text
  ├── binding_assay_value : Float?  # The value measured or determined by the assay.  Examples: null
  ├── binding_assay_value_type : String?  # The type of measurement or value determined by the assay.  Allowable values: pAC50, pEC50, pIC50, pKd, pKi
  ├── cofactor_InChIKey : String?  # Standard IUPAC International Chemical Identifier (InChI) descriptor key  for the cofactor.   InChI, the IUPAC Internatio
  ├── cofactor_SMILES : String?  # Simplified molecular-input line-entry system (SMILES) descriptor for the cofactor.     Weininger D (February 1988). "SMI
  ├── cofactor_chem_comp_id : String?  # The chemical component definition identifier for the cofactor.  Examples: 0Z3, CD9
  ├── cofactor_description : String?  # The cofactor description.  Examples: A synthetic naphthoquinone without the isoprenoid side chain and biological activit
  ├── cofactor_name : String?  # The cofactor name.  Examples: Menadione
  ├── cofactor_prd_id : String?  # The BIRD definition identifier for the cofactor.  Examples: PRD_000010
  ├── cofactor_resource_id : String?  # Identifier for the cofactor assigned by the resource.  Examples: CHEMBL1987, DB00170
  ├── mechanism_of_action : String?  # Mechanism of action describes the biochemical interaction through which the  cofactor produces a pharmacological effect.
  ├── neighbor_flag : String?  # A flag to indicate the cofactor is a structural neighbor of this  entity.  Allowable values: N, Y
  ├── patent_nos : String[]?  # Patent numbers reporting the pharmacology or activity data.
  ├── pubmed_ids : Int[]?  # PubMed identifiers for literature supporting the pharmacology or activity data.
  ├── resource_name : String?  # Resource providing target and cofactor data.  Allowable values: ChEMBL, DrugBank, Pharos
  ├── resource_version : String?  # Version of the information distributed by the data resource.  Examples: V4_0_2
  ├── target_resource_id : String?  # Identifier for the target assigned by the resource.  Examples: P00734, CHEMBL2242
```

## RcsbTargetNeighbors
```text
  ├── alt_id : String?  # Alternate conformer identifier for the non-polymer entity instance.
  ├── atom_id : String?  # The atom identifier for the non-polymer entity instance.  Examples: O1, N1, C1
  ├── comp_id : String?  # Component identifier for the non-polymer entity instance.
  ├── distance : Float?  # Distance value for this target interaction.
  ├── target_asym_id : String?  # The entity instance identifier for the target of interaction.  Examples: A, B
  ├── target_atom_id : String?  # The atom identifier for the target of interaction.  Examples: OG, OE1, CD1
  ├── target_auth_seq_id : Int?  # The author residue index for the target of interaction.
  ├── target_comp_id : String?  # The chemical component identifier for the target of interaction.  Examples: ASN, TRP, SER
  ├── target_entity_id : String?  # The entity identifier for the target of interaction.  Examples: 1, 2
  ├── target_is_bound : String?  # A flag to indicate the nature of the target interaction is covalent or metal-coordination.  Allowable values: N, Y
  ├── target_model_id : Int?  # Model identifier for the target of interaction.
  ├── target_seq_id : Int?  # The sequence position for the target of interaction.
```

## RcsbUniprotAlignments
```text
  ├── core_entity_alignments : RcsbUniprotAlignmentsCoreEntityAlignments[]?  # List of alignments with core_entity canonical sequences
```

## RcsbUniprotAlignmentsCoreEntityAlignments
```text
  ├── aligned_regions : CoreEntityAlignmentsAlignedRegions[]  # Aligned region
  ├── core_entity_identifiers : CoreEntityAlignmentsCoreEntityIdentifiers?  # core_entity identifiers
  ├── scores : CoreEntityAlignmentsScores  # Alignment scores
```

## RcsbUniprotAnnotation
```text
  ├── additional_properties : RcsbUniprotAnnotationAdditionalProperties[]?
  ├── annotation_id : String?  # An identifier for the annotation.
  ├── annotation_lineage : RcsbUniprotAnnotationAnnotationLineage[]?
  ├── assignment_version : String?  # Identifies the version of the annotation assignment.
  ├── description : String?  # A description for the annotation.
  ├── name : String?  # A name for the annotation.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the annotation.
  ├── type : String?  # A type or category of the annotation.  Allowable values: disease, phenotype, GO, InterPro
```

## RcsbUniprotAnnotationAdditionalProperties
```text
  ├── name : String?  # The additional property name  Allowable values: INTERPRO_TYPE
  ├── values : ObjectScalar[]?  # The value(s) of the additional property
```

## RcsbUniprotAnnotationAnnotationLineage
```text
  ├── depth : Int?  # Members of the annotation lineage as parent lineage depth (1-N)
  ├── id : String?  # Members of the annotation lineage as parent class identifiers.
  ├── name : String?  # Members of the annotation lineage as parent class names.
```

## RcsbUniprotContainerIdentifiers
```text
  ├── reference_sequence_identifiers : RcsbUniprotContainerIdentifiersReferenceSequenceIdentifiers[]?
  ├── uniprot_id : String?  # Primary accession number of a given UniProtKB entry.
```

## RcsbUniprotContainerIdentifiersReferenceSequenceIdentifiers
```text
  ├── database_accession : String?  # Reference database accession code
  ├── database_isoform : String?  # Reference database identifier for the sequence isoform
  ├── database_name : String?  # Reference database name
  ├── provenance_source : String?  # Source of the reference database assignment
```

## RcsbUniprotExternalReference
```text
  ├── provenance_source : String?
  ├── reference_id : String?
  ├── reference_name : String?  # Allowable values: IMPC, GTEX, PHAROS.
```

## RcsbUniprotFeature
```text
  ├── assignment_version : String?  # Identifies the version of the feature assignment.
  ├── description : String?  # A description for the feature.
  ├── feature_id : String?  # An identifier for the feature.
  ├── feature_positions : RcsbUniprotFeatureFeaturePositions[]?
  ├── name : String?  # A name for the feature.
  ├── provenance_source : String?  # Code identifying the individual, organization or program that  assigned the feature.
  ├── reference_scheme : String?  # Code residue coordinate system for the assigned feature.
  ├── type : String?  # A type or category of the feature.  Allowable values: ACTIVE_SITE, BINDING_SITE, CALCIUM_BINDING_REGION, CHAIN, COMPOSIT
```

## RcsbUniprotFeatureFeaturePositions
```text
  ├── beg_comp_id : String?  # An identifier for the monomer(s) corresponding to the feature assignment.
  ├── beg_seq_id : Int  # An identifier for the monomer at which this segment of the feature begins.
  ├── end_seq_id : Int?  # An identifier for the monomer at which this segment of the feature ends.
  ├── value : Float?  # The value for the feature over this monomer segment.
  ├── values : Float[]?  # The value(s) for the feature over this monomer segment.
```

## RcsbUniprotKeyword
```text
  ├── id : String?  # A unique keyword identifier.  Examples: KW-0275, KW-0597
  ├── value : String?  # Human-readable keyword term.  Examples: Lipid metabolism, Phosphoprotein, Fatty acid biosynthesis
```

## RcsbUniprotProtein
```text
  ├── ec : RcsbUniprotProteinEc[]?  # Enzyme Commission (EC) number(s).
  ├── function : RcsbUniprotProteinFunction?
  ├── gene : RcsbUniprotProteinGene[]?  # The name(s) of the gene(s) that code for the protein sequence(s) described in the entry.
  ├── name : RcsbUniprotProteinName?
  ├── sequence : String?  # Protein sequence data for canonical protein sequence.
  ├── source_organism : RcsbUniprotProteinSourceOrganism?  # Taxonomy information on the organism that is the source of the protein sequence.
```

## RcsbUniprotProteinEc
```text
  ├── number : String?
  ├── provenance_code : String?  # Historical record of the data attribute.
```

## RcsbUniprotProteinFunction
```text
  ├── details : String?  # General function(s) of a protein.
  ├── provenance_code : String?  # Historical record of the data attribute.
```

## RcsbUniprotProteinGene
```text
  ├── name : GeneName[]?
```

## RcsbUniprotProteinName
```text
  ├── provenance_code : String  # Historical record of the data attribute.
  ├── value : String  # Name that allows to unambiguously identify a protein.  Examples: Hemoglobin alpha
```

## RcsbUniprotProteinSourceOrganism
```text
  ├── provenance_code : String  # Historical record of the data attribute.
  ├── scientific_name : String  # The scientific name of the organism in which a protein occurs.
  ├── taxonomy_id : Int?  # NCBI Taxonomy identifier for the organism in which a protein occurs.
```

## Refine
```text
  ├── B_iso_max : Float?  # The maximum isotropic displacement parameter (B value)  found in the coordinate set.
  ├── B_iso_mean : Float?  # The mean isotropic displacement parameter (B value)  for the coordinate set.
  ├── B_iso_min : Float?  # The minimum isotropic displacement parameter (B value)  found in the coordinate set.
  ├── aniso_B_1_1 : Float?  # The [1][1] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── aniso_B_1_2 : Float?  # The [1][2] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── aniso_B_1_3 : Float?  # The [1][3] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── aniso_B_2_2 : Float?  # The [2][2] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── aniso_B_2_3 : Float?  # The [2][3] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── aniso_B_3_3 : Float?  # The [3][3] element of the matrix that defines the overall  anisotropic displacement model if one was refined for this  s
  ├── correlation_coeff_Fo_to_Fc : Float?  # The correlation coefficient between the observed and              calculated structure factors for reflections included 
  ├── correlation_coeff_Fo_to_Fc_free : Float?  # The correlation coefficient between the observed and              calculated structure factors for reflections not inclu
  ├── details : String?  # Description of special aspects of the refinement process.  Examples: HYDROGENS HAVE BEEN ADDED IN THE RIDING POSITIONS
  ├── ls_R_factor_R_free : Float?  # Residual factor R for reflections that satisfy the resolution  limits established by _refine.ls_d_res_high and  _refine.
  ├── ls_R_factor_R_free_error : Float?  # The estimated error in _refine.ls_R_factor_R_free.  The method used to estimate the error is described in the  item _ref
  ├── ls_R_factor_R_free_error_details : String?  # Special aspects of the method used to estimated the error in  _refine.ls_R_factor_R_free.
  ├── ls_R_factor_R_work : Float?  # Residual factor R for reflections that satisfy the resolution  limits established by _refine.ls_d_res_high and  _refine.
  ├── ls_R_factor_all : Float?  # Residual factor R for all reflections that satisfy the resolution  limits established by _refine.ls_d_res_high and  _ref
  ├── ls_R_factor_obs : Float?  # Residual factor R for reflections that satisfy the resolution  limits established by _refine.ls_d_res_high and  _refine.
  ├── ls_d_res_high : Float?  # The smallest value for the interplanar spacings for the  reflection data used in the refinement in angstroms. This is  c
  ├── ls_d_res_low : Float?  # The largest value for the interplanar spacings for  the reflection data used in the refinement in angstroms.  This is ca
  ├── ls_matrix_type : String?  # Type of matrix used to accumulate the least-squares derivatives.  Allowable values: atomblock, diagonal, full, fullcycle
  ├── ls_number_parameters : Int?  # The number of parameters refined in the least-squares process.  If possible, this number should include some contributio
  ├── ls_number_reflns_R_free : Int?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_number_reflns_R_work : Int?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_number_reflns_all : Int?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_number_reflns_obs : Int?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_number_restraints : Int?  # The number of restrained parameters. These are parameters which  are not directly dependent on another refined parameter
  ├── ls_percent_reflns_R_free : Float?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_percent_reflns_obs : Float?  # The number of reflections that satisfy the resolution limits  established by _refine.ls_d_res_high and _refine.ls_d_res_
  ├── ls_redundancy_reflns_all : Float?  # The ratio of the total number of observations of the  reflections that satisfy the resolution limits established by  _re
  ├── ls_redundancy_reflns_obs : Float?  # The ratio of the total number of observations of the  reflections that satisfy the resolution limits established by  _re
  ├── ls_wR_factor_R_free : Float?  # Weighted residual factor wR for reflections that satisfy the  resolution limits established by _refine.ls_d_res_high and
  ├── ls_wR_factor_R_work : Float?  # Weighted residual factor wR for reflections that satisfy the  resolution limits established by _refine.ls_d_res_high and
  ├── occupancy_max : Float?  # The maximum value for occupancy found in the coordinate set.
  ├── occupancy_min : Float?  # The minimum value for occupancy found in the coordinate set.
  ├── overall_FOM_free_R_set : Float?  # Average figure of merit of phases of reflections not included  in the refinement.   This value is derived from the likel
  ├── overall_FOM_work_R_set : Float?  # Average figure of merit of phases of reflections included in  the refinement.   This value is derived from the likelihoo
  ├── overall_SU_B : Float?  # The overall standard uncertainty (estimated standard deviation)            of the displacement parameters based on a max
  ├── overall_SU_ML : Float?  # The overall standard uncertainty (estimated standard deviation)            of the positional parameters based on a maxim
  ├── overall_SU_R_Cruickshank_DPI : Float?  # The overall standard uncertainty (estimated standard deviation)  of the displacement parameters based on the crystallogr
  ├── overall_SU_R_free : Float?  # The overall standard uncertainty (estimated standard deviation)  of the displacement parameters based on the free R valu
  ├── pdbx_R_Free_selection_details : String?  # Details of the manner in which the cross validation  reflections were selected.  Examples: Random selection
  ├── pdbx_TLS_residual_ADP_flag : String?  # A flag for TLS refinements identifying the type of atomic displacement parameters stored  in _atom_site.B_iso_or_equiv. 
  ├── pdbx_average_fsc_free : Float?  # Average Fourier Shell Correlation (avgFSC) between model and  observed structure factors for reflections not included in
  ├── pdbx_average_fsc_overall : Float?  # Overall average Fourier Shell Correlation (avgFSC) between model and  observed structure factors for all reflections.   
  ├── pdbx_average_fsc_work : Float?  # Average Fourier Shell Correlation (avgFSC) between model and  observed structure factors for reflections included in ref
  ├── pdbx_data_cutoff_high_absF : Float?  # Value of F at "high end" of data cutoff.
  ├── pdbx_data_cutoff_high_rms_absF : Float?  # Value of RMS |F| used as high data cutoff.  Examples: null
  ├── pdbx_data_cutoff_low_absF : Float?  # Value of F at "low end" of data cutoff.  Examples: null
  ├── pdbx_diffrn_id : String[]?  # An identifier for the diffraction data set used in this refinement.   Multiple diffraction data sets specified as a comm
  ├── pdbx_isotropic_thermal_model : String?  # Whether the structure was refined with indvidual isotropic, anisotropic or overall temperature factor.  Examples: Isotro
  ├── pdbx_ls_cross_valid_method : String?  # Whether the cross validataion method was used through out or only at the end.  Examples: FREE R-VALUE
  ├── pdbx_ls_sigma_F : Float?  # Data cutoff (SIGMA(F))
  ├── pdbx_ls_sigma_Fsqd : Float?  # Data cutoff (SIGMA(F^2))
  ├── pdbx_ls_sigma_I : Float?  # Data cutoff (SIGMA(I))
  ├── pdbx_method_to_determine_struct : String?  # Method(s) used to determine the structure.  Examples: AB INITIO PHASING, DM, ISAS, ISIR, ISIRAS, MAD, MIR, MIRAS, MR, SI
  ├── pdbx_overall_ESU_R : Float?  # Overall estimated standard uncertainties of positional  parameters based on R value.
  ├── pdbx_overall_ESU_R_Free : Float?  # Overall estimated standard uncertainties of positional parameters based on R free value.
  ├── pdbx_overall_SU_R_Blow_DPI : Float?  # The overall standard uncertainty (estimated standard deviation)  of the displacement parameters based on the crystallogr
  ├── pdbx_overall_SU_R_free_Blow_DPI : Float?  # The overall standard uncertainty (estimated standard deviation)  of the displacement parameters based on the crystallogr
  ├── pdbx_overall_SU_R_free_Cruickshank_DPI : Float?  # The overall standard uncertainty (estimated standard deviation)  of the displacement parameters based on the crystallogr
  ├── pdbx_overall_phase_error : Float?  # The overall phase error for all reflections after refinement using  the current refinement target.  Examples: null
  ├── pdbx_refine_id : String  # This data item uniquely identifies a refinement within an entry.  _refine.pdbx_refine_id can be used to distinguish the 
  ├── pdbx_solvent_ion_probe_radii : Float?  # For bulk solvent mask calculation, the amount that the ionic radii of atoms, which can be ions, are increased used.
  ├── pdbx_solvent_shrinkage_radii : Float?  # For bulk solvent mask calculation, amount mask is shrunk after taking away atoms with new radii and a constant value ass
  ├── pdbx_solvent_vdw_probe_radii : Float?  # For bulk solvent mask calculation, the value by which the vdw radii of non-ion atoms (like carbon) are increased and use
  ├── pdbx_starting_model : String?  # Starting model for refinement.  Starting model for  molecular replacement should refer to a previous  structure or exper
  ├── pdbx_stereochem_target_val_spec_case : String?  # Special case of stereochemistry target values used in SHELXL refinement.
  ├── pdbx_stereochemistry_target_values : String?  # Stereochemistry target values used in refinement.
  ├── solvent_model_details : String?  # Special aspects of the solvent model used during refinement.
  ├── solvent_model_param_bsol : Float?  # The value of the BSOL solvent-model parameter describing  the average isotropic displacement parameter of disordered  so
  ├── solvent_model_param_ksol : Float?  # The value of the KSOL solvent-model parameter describing  the ratio of the electron density in the bulk solvent to the  
```

## RefineAnalyze
```text
  ├── Luzzati_coordinate_error_free : Float?  # The estimated coordinate error obtained from the plot of  the R value versus sin(theta)/lambda for the reflections  trea
  ├── Luzzati_coordinate_error_obs : Float?  # The estimated coordinate error obtained from the plot of  the R value versus sin(theta)/lambda for reflections classifie
  ├── Luzzati_d_res_low_free : Float?  # The value of the low-resolution cutoff used in constructing the  Luzzati plot for reflections treated as a test set duri
  ├── Luzzati_d_res_low_obs : Float?  # The value of the low-resolution cutoff used in  constructing the Luzzati plot for reflections classified as  observed.  
  ├── Luzzati_sigma_a_free : Float?  # The value of sigma~a~ used in constructing the Luzzati plot for  the reflections treated as a test set during refinement
  ├── Luzzati_sigma_a_obs : Float?  # The value of sigma~a~ used in constructing the Luzzati plot for  reflections classified as observed. Details of the  est
  ├── number_disordered_residues : Float?  # The number of discretely disordered residues in the refined  model.
  ├── occupancy_sum_hydrogen : Float?  # The sum of the occupancies of the hydrogen atoms in the refined  model.
  ├── occupancy_sum_non_hydrogen : Float?  # The sum of the occupancies of the non-hydrogen atoms in the   refined model.
  ├── pdbx_Luzzati_d_res_high_obs : Float?  # record the high resolution for calculating Luzzati statistics.
  ├── pdbx_refine_id : String  # This data item uniquely identifies a refinement within an entry.  _refine_analyze.pdbx_refine_id can be used to distingu
```

## RefineHist
```text
  ├── cycle_id : String  # The value of _refine_hist.cycle_id must uniquely identify a  record in the REFINE_HIST list.   Note that this item need 
  ├── d_res_high : Float?  # The lowest value for the interplanar spacings for the  reflection data for this cycle of refinement. This is called  the
  ├── d_res_low : Float?  # The highest value for the interplanar spacings for the  reflection data for this cycle of refinement. This is  called th
  ├── number_atoms_solvent : Int?  # The number of solvent atoms that were included in the model at  this cycle of the refinement.
  ├── number_atoms_total : Int?  # The total number of atoms that were included in the model at  this cycle of the refinement.
  ├── pdbx_B_iso_mean_ligand : Float?  # Mean isotropic B-value for ligand molecules included in refinement.
  ├── pdbx_B_iso_mean_solvent : Float?  # Mean isotropic B-value for solvent molecules included in refinement.
  ├── pdbx_number_atoms_ligand : Int?  # Number of ligand atoms included in refinement
  ├── pdbx_number_atoms_nucleic_acid : Int?  # Number of nucleic atoms included in refinement
  ├── pdbx_number_atoms_protein : Int?  # Number of protein atoms included in refinement
  ├── pdbx_number_residues_total : Int?  # Total number of polymer residues included in refinement.
  ├── pdbx_refine_id : String  # This data item uniquely identifies a refinement within an entry.  _refine_hist.pdbx_refine_id can be used to distinguish
```

## RefineLsRestr
```text
  ├── dev_ideal : Float?  # For the given parameter type, the root-mean-square deviation  between the ideal values used as restraints in the least-s
  ├── dev_ideal_target : Float?  # For the given parameter type, the target root-mean-square  deviation between the ideal values used as restraints in the 
  ├── number : Int?  # The number of parameters of this type subjected to restraint in  least-squares refinement.
  ├── pdbx_refine_id : String  # This data item uniquely identifies a refinement within an entry.  _refine_ls_restr.pdbx_refine_id can be used to disting
  ├── pdbx_restraint_function : String?  # The functional form of the restraint function used in the least-squares  refinement.  Examples: SINUSOIDAL, HARMONIC, SE
  ├── type : String  # The type of the parameter being restrained.  Explicit sets of data values are provided for the programs  PROTIN/PROLSQ (
  ├── weight : Float?  # The weighting value applied to this type of restraint in  the least-squares refinement.
```

## Reflns
```text
  ├── B_iso_Wilson_estimate : Float?  # The value of the overall isotropic displacement parameter  estimated from the slope of the Wilson plot.
  ├── R_free_details : String?  # A description of the method by which a subset of reflections was  selected for exclusion from refinement so as to be use
  ├── Rmerge_F_all : Float?  # Residual factor Rmerge for all reflections that satisfy the  resolution limits established by _reflns.d_resolution_high 
  ├── Rmerge_F_obs : Float?  # Residual factor Rmerge for reflections that satisfy the  resolution limits established by _reflns.d_resolution_high  and
  ├── d_resolution_high : Float?  # The smallest value in angstroms for the interplanar spacings  for the reflection data. This is called the highest resolu
  ├── d_resolution_low : Float?  # The largest value in angstroms for the interplanar spacings  for the reflection data. This is called the lowest resoluti
  ├── data_reduction_details : String?  # A description of special aspects of the data-reduction  procedures.  Examples: Merging and scaling based on only those  
  ├── data_reduction_method : String?  # The method used for data reduction.   Note that this is not the computer program used, which is  described in the SOFTWA
  ├── details : String?  # A description of reflection data not covered by other data  names. This should include details of the Friedel pairs.
  ├── limit_h_max : Int?  # Maximum value of the Miller index h for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── limit_h_min : Int?  # Minimum value of the Miller index h for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── limit_k_max : Int?  # Maximum value of the Miller index k for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── limit_k_min : Int?  # Minimum value of the Miller index k for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── limit_l_max : Int?  # Maximum value of the Miller index l for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── limit_l_min : Int?  # Minimum value of the Miller index l for the reflection data. This  need not have the same value as _diffrn_reflns.limit_
  ├── number_all : Int?  # The total number of reflections in the REFLN list (not the  DIFFRN_REFLN list). This number may contain Friedel-equivale
  ├── number_obs : Int?  # The number of reflections in the REFLN list (not the DIFFRN_REFLN  list) classified as observed (see _reflns.observed_cr
  ├── observed_criterion : String?  # The criterion used to classify a reflection as 'observed'. This  criterion is usually expressed in terms of a sigma(I) o
  ├── observed_criterion_F_max : Float?  # The criterion used to classify a reflection as 'observed'  expressed as an upper limit for the value of F.
  ├── observed_criterion_F_min : Float?  # The criterion used to classify a reflection as 'observed'  expressed as a lower limit for the value of F.
  ├── observed_criterion_I_max : Float?  # The criterion used to classify a reflection as 'observed'  expressed as an upper limit for the value of I.
  ├── observed_criterion_I_min : Float?  # The criterion used to classify a reflection as 'observed'  expressed as a lower limit for the value of I.
  ├── observed_criterion_sigma_F : Float?  # The criterion used to classify a reflection as 'observed'  expressed as a multiple of the value of sigma(F).
  ├── observed_criterion_sigma_I : Float?  # The criterion used to classify a reflection as 'observed'  expressed as a multiple of the value of sigma(I).
  ├── pdbx_CC_half : Float?  # The Pearson's correlation coefficient expressed as a decimal value               between the average intensities from ra
  ├── pdbx_R_split : Float?  # R split measures the agreement between the sets of intensities created by merging               odd- and even-numbered i
  ├── pdbx_Rmerge_I_obs : Float?  # The R value for merging intensities satisfying the observed  criteria in this data set.
  ├── pdbx_Rpim_I_all : Float?  # The precision-indicating merging R factor value Rpim,  for merging all intensities in this data set.          sum~i~ [1/
  ├── pdbx_Rrim_I_all : Float?  # The redundancy-independent merging R factor value Rrim,               also denoted Rmeas, for merging all intensities in
  ├── pdbx_Rsym_value : Float?  # The R sym value as a decimal number.  Examples: null
  ├── pdbx_chi_squared : Float?  # Overall  Chi-squared statistic.
  ├── pdbx_diffrn_id : String[]?  # An identifier for the diffraction data set for this set of summary statistics.   Multiple diffraction data sets entered 
  ├── pdbx_netI_over_av_sigmaI : Float?  # The ratio of the average intensity to the average uncertainty,  <I>/<sigma(I)>.
  ├── pdbx_netI_over_sigmaI : Float?  # The mean of the ratio of the intensities to their  standard uncertainties, <I/sigma(I)>.
  ├── pdbx_number_measured_all : Int?  # Total number of measured reflections.
  ├── pdbx_ordinal : Int  # An ordinal identifier for this set of reflection statistics.
  ├── pdbx_redundancy : Float?  # Overall redundancy for this data set.
  ├── pdbx_scaling_rejects : Int?  # Number of reflections rejected in scaling operations.
  ├── percent_possible_obs : Float?  # The percentage of geometrically possible reflections represented  by reflections that satisfy the resolution limits esta
  ├── phase_calculation_details : String?  # The value of _reflns.phase_calculation_details describes a  special details about calculation of phases in _refln.phase_
```

## ReflnsShell
```text
  ├── Rmerge_F_all : Float?  # Residual factor Rmerge for all reflections that satisfy the  resolution limits established by _reflns_shell.d_res_high a
  ├── Rmerge_F_obs : Float?  # Residual factor Rmerge for reflections that satisfy the  resolution limits established by _reflns_shell.d_res_high and  
  ├── Rmerge_I_all : Float?  # The value of Rmerge(I) for all reflections in a given shell.               sum~i~(sum~j~|I~j~ - <I>|)  Rmerge(I) = -----
  ├── Rmerge_I_obs : Float?  # The value of Rmerge(I) for reflections classified as 'observed'  (see _reflns.observed_criterion) in a given shell.     
  ├── d_res_high : Float?  # The smallest value in angstroms for the interplanar spacings  for the reflections in this shell. This is called the high
  ├── d_res_low : Float?  # The highest value in angstroms for the interplanar spacings  for the reflections in this shell. This is called the lowes
  ├── meanI_over_sigI_all : Float?  # The ratio of the mean of the intensities of all reflections  in this shell to the mean of the standard uncertainties of 
  ├── meanI_over_sigI_obs : Float?  # The ratio of the mean of the intensities of the reflections  classified as 'observed' (see _reflns.observed_criterion) i
  ├── meanI_over_uI_all : Float?  # The ratio of the mean of the intensities of all reflections  in this shell to the mean of the standard uncertainties of 
  ├── number_measured_all : Int?  # The total number of reflections measured for this  shell.
  ├── number_measured_obs : Int?  # The number of reflections classified as 'observed'  (see _reflns.observed_criterion) for this  shell.
  ├── number_possible : Int?  # The number of unique reflections it is possible to measure in  this shell.
  ├── number_unique_all : Int?  # The total number of measured reflections which are symmetry-  unique after merging for this shell.
  ├── number_unique_obs : Int?  # The total number of measured reflections classified as 'observed'  (see _reflns.observed_criterion) which are symmetry-u
  ├── pdbx_CC_half : Float?  # The Pearson's correlation coefficient expressed as a decimal value               between the average intensities from ra
  ├── pdbx_R_split : Float?  # R split measures the agreement between the sets of intensities created by merging               odd- and even-numbered i
  ├── pdbx_Rpim_I_all : Float?  # The precision-indicating merging R factor value Rpim,  for merging all intensities in a given shell.          sum~i~ [1/
  ├── pdbx_Rrim_I_all : Float?  # The redundancy-independent merging R factor value Rrim,               also denoted Rmeas, for merging all intensities in
  ├── pdbx_Rsym_value : Float?  # R sym value in percent.
  ├── pdbx_chi_squared : Float?  # Chi-squared statistic for this resolution shell.
  ├── pdbx_diffrn_id : String[]?  # An identifier for the diffraction data set corresponding to this resolution shell.   Multiple diffraction data sets spec
  ├── pdbx_netI_over_sigmaI_all : Float?  # The mean of the ratio of the intensities to their  standard uncertainties of all reflections in the  resolution shell.  
  ├── pdbx_netI_over_sigmaI_obs : Float?  # The mean of the ratio of the intensities to their  standard uncertainties of observed reflections  (see _reflns.observed
  ├── pdbx_ordinal : Int  # An ordinal identifier for this resolution shell.
  ├── pdbx_redundancy : Float?  # Redundancy for the current shell.
  ├── pdbx_rejects : Int?  # The number of rejected reflections in the resolution  shell.  Reflections may be rejected from scaling  by setting the o
  ├── percent_possible_all : Float?  # The percentage of geometrically possible reflections represented  by all reflections measured for this shell.
  ├── percent_possible_obs : Float?  # The percentage of geometrically possible reflections represented  by reflections classified as 'observed' (see  _reflns.
```

## Software
```text
  ├── citation_id : String?  # This data item is a pointer to _citation.id in the CITATION  category.
  ├── classification : String?  # The classification of the program according to its  major function.  Examples: data collection, data reduction, phasing,
  ├── contact_author : String?  # The recognized contact author of the software. This could be  the original author, someone who has modified the code or 
  ├── contact_author_email : String?  # The e-mail address of the person specified in  _software.contact_author.  Examples: bourne@sdsc.edu
  ├── date : String?  # The date the software was released.  Examples: 1991-10-01, 1990-04-30
  ├── description : String?  # Description of the software.  Examples: Uses method of restrained least squares
  ├── language : String?  # The major computing language in which the software is  coded.  Allowable values: Ada, Awk, Basic, C, C++, C/C++, Fortran
  ├── location : String?  # The URL for an Internet address at which  details of the software can be found.  Examples: http://rosebud.sdsc.edu/proje
  ├── name : String?  # The name of the software.  Examples: Merlot, O, Xengen, X-plor
  ├── os : String?  # The name of the operating system under which the software  runs.  Examples: Ultrix, OpenVMS, DOS, Windows 95, Windows NT
  ├── pdbx_ordinal : Int  # An ordinal index for this category
  ├── type : String?  # The classification of the software according to the most  common types.  Allowable values: filter, jiffy, library, other
  ├── version : String?  # The version of the software.  Examples: v1.0, beta, 3.1-2, unknown
```

## Struct
```text
  ├── pdbx_CASP_flag : String?  # The item indicates whether the entry is a CASP target, a CASD-NMR target,  or similar target participating in methods de
  ├── pdbx_descriptor : String?  # An automatically generated descriptor for an NDB structure or  the unstructured content of the PDB COMPND record.  Examp
  ├── pdbx_model_details : String?  # Text description of the methodology which produced this  model structure.  Examples: This model was produced from a 10 n
  ├── pdbx_model_type_details : String?  # A description of the type of structure model.  Examples: MINIMIZED AVERAGE
  ├── title : String?  # A title for the data block. The author should attempt to convey  the essence of the structure archived in the CIF in the
```

## StructAsym
```text
  ├── pdbx_PDB_id : String?  # This data item is a pointer to _atom_site.pdbx_PDB_strand_id the  ATOM_SITE category.  Examples: 1ABC
  ├── pdbx_alt_id : String?  # This data item is a pointer to _atom_site.ndb_alias_strand_id the  ATOM_SITE category.
  ├── pdbx_order : Int?  # This data item gives the order of the structural elements in the  ATOM_SITE category.
  ├── pdbx_type : String?  # This data item describes the general type of the structural elements  in the ATOM_SITE category.  Allowable values: ATOM
```

## StructKeywords
```text
  ├── pdbx_keywords : String?  # Terms characterizing the macromolecular structure.  Examples: DNA, RNA, T-RNA, DNA/RNA, RIBOZYME, PROTEIN/DNA, PROTEIN/R
  ├── text : String?  # Keywords describing this structure.  Examples: Inhibitor, Complex, Isomerase..., serine protease, inhibited complex, hig
```

## Symmetry
```text
  ├── Int_Tables_number : Int?  # Space-group number from International Tables for Crystallography  Vol. A (2002).
  ├── cell_setting : String?  # The cell settings for this space-group symmetry.  Allowable values: cubic, hexagonal, monoclinic, orthorhombic, rhombohe
  ├── pdbx_full_space_group_name_H_M : String?  # Used for PDB space group:   Example: 'C 1 2 1'  (instead of C 2)           'P 1 2 1'  (instead of P 2)           'P 1 21
  ├── space_group_name_H_M : String?  # Hermann-Mauguin space-group symbol. Note that the  Hermann-Mauguin symbol does not necessarily contain complete  informa
  ├── space_group_name_Hall : String?  # Space-group symbol as described by Hall (1981). This symbol  gives the space-group setting explicitly. Leave spaces betw
```
