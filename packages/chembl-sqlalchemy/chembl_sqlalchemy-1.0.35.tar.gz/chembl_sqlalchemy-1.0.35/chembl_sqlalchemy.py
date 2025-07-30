"""ORM schema."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    Numeric,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__version__ = "1.0.35"


class Base(DeclarativeBase):
    """ORM base class."""


class ActionType(Base):
    """ORM class for action_type."""

    __tablename__ = "action_type"
    __table_args__ = (PrimaryKeyConstraint("action_type", name="action_type_pk"),)
    action_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    parent_type: Mapped[str | None] = mapped_column(String(50))


class AssayType(Base):
    """ORM class for assay_type."""

    __tablename__ = "assay_type"
    __table_args__ = (PrimaryKeyConstraint("assay_type", name="pk_assaytype_assay_type"),)
    assay_type: Mapped[str] = mapped_column(String(1))
    assay_desc: Mapped[str | None] = mapped_column(String(250))


class ChemblIdLookup(Base):
    """ORM class for chembl_id_lookup."""

    __tablename__ = "chembl_id_lookup"
    __table_args__ = (
        PrimaryKeyConstraint("chembl_id", name="chembl_id_lookup_pk"),
        CheckConstraint(
            "status IN ('ACTIVE', 'INACTIVE', 'OBS')", name="ck_chembl_id_lookup_status"
        ),
        UniqueConstraint("entity_type", "entity_id", name="chembl_id_lookup_uk"),
    )
    chembl_id: Mapped[str] = mapped_column(String(20))
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[int] = mapped_column(BigInteger())
    status: Mapped[str] = mapped_column(String(10))
    last_active: Mapped[int | None]


class ConfidenceScoreLookup(Base):
    """ORM class for confidence_score_lookup."""

    __tablename__ = "confidence_score_lookup"
    __table_args__ = (PrimaryKeyConstraint("confidence_score", name="confidence_score_lookup_pk"),)
    confidence_score: Mapped[int] = mapped_column(SmallInteger())
    description: Mapped[str] = mapped_column(String(100))
    target_mapping: Mapped[str] = mapped_column(String(30))


class CurationLookup(Base):
    """ORM class for curation_lookup."""

    __tablename__ = "curation_lookup"
    __table_args__ = (PrimaryKeyConstraint("curated_by", name="pf_curlu_cur_by"),)
    curated_by: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(100))


class ChemblRelease(Base):
    """ORM class for chembl_release."""

    __tablename__ = "chembl_release"
    __table_args__ = (PrimaryKeyConstraint("chembl_release_id", name="pk_chembl_release"),)
    chembl_release_id: Mapped[int]
    chembl_release: Mapped[str | None] = mapped_column(String(20))
    creation_date: Mapped[datetime | None]


class Source(Base):
    """ORM class for source."""

    __tablename__ = "source"
    __table_args__ = (PrimaryKeyConstraint("src_id", name="pk_source_src_id"),)
    src_id: Mapped[int]
    src_description: Mapped[str | None] = mapped_column(String(500))
    src_short_name: Mapped[str | None] = mapped_column(String(20))
    src_comment: Mapped[str | None] = mapped_column(String(1200))
    src_url: Mapped[str | None] = mapped_column(String(200))


class RelationshipType(Base):
    """ORM class for relationship_type."""

    __tablename__ = "relationship_type"
    __table_args__ = (
        PrimaryKeyConstraint("relationship_type", name="pk_reltype_relationship_type"),
        Index("pk_rt_rt", "relationship_type", unique=True),
    )
    relationship_type: Mapped[str] = mapped_column(String(1))
    relationship_desc: Mapped[str | None] = mapped_column(String(250))


class TargetType(Base):
    """ORM class for target_type."""

    __tablename__ = "target_type"
    __table_args__ = (
        PrimaryKeyConstraint("target_type", name="pk_targtype_target_type"),
        Index("pk_tt_tt", "target_type", unique=True),
    )
    target_type: Mapped[str] = mapped_column(String(30))
    target_desc: Mapped[str | None] = mapped_column(String(250))
    parent_type: Mapped[str | None] = mapped_column(String(25))


class VariantSequences(Base):
    """ORM class for variant_sequences."""

    __tablename__ = "variant_sequences"
    __table_args__ = (
        PrimaryKeyConstraint("variant_id", name="pk_varseq_variant_id"),
        UniqueConstraint("mutation", "accession", name="uk_varseq_mut_acc"),
    )
    variant_id: Mapped[int] = mapped_column(BigInteger())
    mutation: Mapped[str | None] = mapped_column(String(2000))
    accession: Mapped[str | None] = mapped_column(String(25))
    version: Mapped[int | None] = mapped_column(BigInteger())
    isoform: Mapped[int | None] = mapped_column(BigInteger())
    sequence: Mapped[str | None] = mapped_column(Text())
    organism: Mapped[str | None] = mapped_column(String(200))
    tax_id: Mapped[int | None] = mapped_column(BigInteger())


class BioassayOntology(Base):
    """ORM class for bioassay_ontology."""

    __tablename__ = "bioassay_ontology"
    __table_args__ = (PrimaryKeyConstraint("bao_id", name="bioassay_ontology_pk"),)
    bao_id: Mapped[str] = mapped_column(String(11))
    label: Mapped[str] = mapped_column(String(100))


class DataValidityLookup(Base):
    """ORM class for data_validity_lookup."""

    __tablename__ = "data_validity_lookup"
    __table_args__ = (PrimaryKeyConstraint("data_validity_comment", name="sys_c00167991"),)
    data_validity_comment: Mapped[str] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(String(200))


class ActivitySmid(Base):
    """ORM class for activity_smid."""

    __tablename__ = "activity_smid"
    __table_args__ = (PrimaryKeyConstraint("smid", name="pk_actsamid"),)
    smid: Mapped[int] = mapped_column(BigInteger())


class ActivityStdsLookup(Base):
    """ORM class for activity_stds_lookup."""

    __tablename__ = "activity_stds_lookup"
    __table_args__ = (
        PrimaryKeyConstraint("std_act_id", name="pk_actstds_stdactid"),
        UniqueConstraint("standard_type", "standard_units", name="uk_actstds_typeunits"),
    )
    std_act_id: Mapped[int] = mapped_column(BigInteger())
    standard_type: Mapped[str] = mapped_column(String(250))
    definition: Mapped[str | None] = mapped_column(String(500))
    standard_units: Mapped[str] = mapped_column(String(100))
    normal_range_min: Mapped[float | None] = mapped_column(Numeric(24, 12))
    normal_range_max: Mapped[float | None] = mapped_column(Numeric(24, 12))


class AssayClassification(Base):
    """ORM class for assay_classification."""

    __tablename__ = "assay_classification"
    __table_args__ = (
        PrimaryKeyConstraint("assay_class_id", name="pk_assay_class"),
        UniqueConstraint("l3", name="uk_assay_class_l3"),
        Index("assay_classification_pk", "assay_class_id", unique=True),
    )
    assay_class_id: Mapped[int] = mapped_column(BigInteger())
    l1: Mapped[str | None] = mapped_column(String(100))
    l2: Mapped[str | None] = mapped_column(String(100))
    l3: Mapped[str | None] = mapped_column(String(1000))
    class_type: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str | None] = mapped_column(String(50))


class AtcClassification(Base):
    """ORM class for atc_classification."""

    __tablename__ = "atc_classification"
    __table_args__ = (PrimaryKeyConstraint("level5", name="pk_atc_code"),)
    who_name: Mapped[str | None] = mapped_column(String(2000))
    level1: Mapped[str | None] = mapped_column(String(10))
    level2: Mapped[str | None] = mapped_column(String(10))
    level3: Mapped[str | None] = mapped_column(String(10))
    level4: Mapped[str | None] = mapped_column(String(10))
    level5: Mapped[str] = mapped_column(String(10))
    level1_description: Mapped[str | None] = mapped_column(String(2000))
    level2_description: Mapped[str | None] = mapped_column(String(2000))
    level3_description: Mapped[str | None] = mapped_column(String(2000))
    level4_description: Mapped[str | None] = mapped_column(String(2000))


class BioComponentSequences(Base):
    """ORM class for bio_component_sequences."""

    __tablename__ = "bio_component_sequences"
    __table_args__ = (
        PrimaryKeyConstraint("component_id", name="pk_biocomp_seqs_compid"),
        Index("bio_component_seqs_pk", "component_id", unique=True),
    )
    component_id: Mapped[int] = mapped_column(BigInteger())
    component_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(200))
    sequence: Mapped[str | None] = mapped_column(Text())
    sequence_md5sum: Mapped[str | None] = mapped_column(String(32))
    tax_id: Mapped[int | None] = mapped_column(BigInteger())
    organism: Mapped[str | None] = mapped_column(String(150))


class ComponentSequences(Base):
    """ORM class for component_sequences."""

    __tablename__ = "component_sequences"
    __table_args__ = (
        PrimaryKeyConstraint("component_id", name="pk_targcomp_seqs_compid"),
        CheckConstraint(
            "db_source IN ('SWISS-PROT', 'TREMBL', 'Manual')", name="ck_targcomp_seqs_src"
        ),
        CheckConstraint("tax_id > 0", name="ck_targcomp_seqs_taxid"),
        CheckConstraint(
            "component_type IN ('PROTEIN', 'DNA', 'RNA')", name="ck_targcomp_seqs_type"
        ),
        UniqueConstraint("accession", name="uk_targcomp_seqs_acc"),
    )
    component_id: Mapped[int] = mapped_column(BigInteger())
    component_type: Mapped[str | None] = mapped_column(String(50))
    accession: Mapped[str | None] = mapped_column(String(25))
    sequence: Mapped[str | None] = mapped_column(Text())
    sequence_md5sum: Mapped[str | None] = mapped_column(String(32))
    description: Mapped[str | None] = mapped_column(String(200))
    tax_id: Mapped[int | None] = mapped_column(BigInteger())
    organism: Mapped[str | None] = mapped_column(String(150))
    db_source: Mapped[str | None] = mapped_column(String(25))
    db_version: Mapped[str | None] = mapped_column(String(10))


class ProteinClassification(Base):
    """ORM class for protein_classification."""

    __tablename__ = "protein_classification"
    __table_args__ = (
        PrimaryKeyConstraint("protein_class_id", name="prot_class_pk"),
        CheckConstraint("class_level >= 0 AND class_level <= 10", name="ck_prot_class_level"),
        Index("protclass_pk", "protein_class_id", unique=True),
    )
    protein_class_id: Mapped[int] = mapped_column(BigInteger())
    parent_id: Mapped[int | None] = mapped_column(BigInteger())
    pref_name: Mapped[str | None] = mapped_column(String(500))
    short_name: Mapped[str | None] = mapped_column(String(50))
    protein_class_desc: Mapped[str] = mapped_column(String(410))
    definition: Mapped[str | None] = mapped_column(String(4000))
    class_level: Mapped[int] = mapped_column(BigInteger())


class Domains(Base):
    """ORM class for domains."""

    __tablename__ = "domains"
    __table_args__ = (
        PrimaryKeyConstraint("domain_id", name="pk_domain_id"),
        CheckConstraint("domain_type IN ('Pfam-A', 'Pfam-B')", name="ck_domain_type"),
    )
    domain_id: Mapped[int] = mapped_column(BigInteger())
    domain_type: Mapped[str] = mapped_column(String(20))
    source_domain_id: Mapped[str] = mapped_column(String(20))
    domain_name: Mapped[str | None] = mapped_column(String(100))
    domain_description: Mapped[str | None] = mapped_column(String(500))


class GoClassification(Base):
    """ORM class for go_classification."""

    __tablename__ = "go_classification"
    __table_args__ = (PrimaryKeyConstraint("go_id", name="go_classification_pk"),)
    go_id: Mapped[str] = mapped_column(String(10))
    parent_go_id: Mapped[str | None] = mapped_column(String(10))
    pref_name: Mapped[str | None] = mapped_column(String(200))
    class_level: Mapped[int | None] = mapped_column(SmallInteger())
    aspect: Mapped[str | None] = mapped_column(String(1))
    path: Mapped[str | None] = mapped_column(String(1000))


class StructuralAlertSets(Base):
    """ORM class for structural_alert_sets."""

    __tablename__ = "structural_alert_sets"
    __table_args__ = (
        PrimaryKeyConstraint("alert_set_id", name="pk_str_alert_set_id"),
        UniqueConstraint("set_name", name="uk_str_alert_name"),
        Index("structural_alert_set_pk", "alert_set_id", unique=True),
    )
    alert_set_id: Mapped[int] = mapped_column(BigInteger())
    set_name: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(SmallInteger())


class Products(Base):
    """ORM class for products."""

    __tablename__ = "products"
    __table_args__ = (
        PrimaryKeyConstraint("product_id", name="pk_products_id"),
        CheckConstraint("ad_type IN ('OTC', 'RX', 'DISCN')", name="ck_products_adtype"),
        CheckConstraint("black_box_warning IN (0, 1)", name="ck_products_bbw"),
        CheckConstraint("innovator_company IN (0, 1)", name="ck_products_inn"),
        CheckConstraint("NDA_TYPE IN ('N', 'A')", name="ck_products_nda"),
        CheckConstraint("oral IN (0, 1)", name="ck_products_oral"),
        CheckConstraint("parenteral IN (0, 1)", name="ck_products_par"),
        CheckConstraint("topical IN (0, 1)", name="ck_products_top"),
    )
    dosage_form: Mapped[str | None] = mapped_column(String(200))
    route: Mapped[str | None] = mapped_column(String(200))
    trade_name: Mapped[str | None] = mapped_column(String(200))
    approval_date: Mapped[datetime | None]
    ad_type: Mapped[str | None] = mapped_column(String(5))
    oral: Mapped[int | None] = mapped_column(SmallInteger())
    topical: Mapped[int | None] = mapped_column(SmallInteger())
    parenteral: Mapped[int | None] = mapped_column(SmallInteger())
    black_box_warning: Mapped[int | None] = mapped_column(SmallInteger())
    applicant_full_name: Mapped[str | None] = mapped_column(String(200))
    innovator_company: Mapped[int | None] = mapped_column(SmallInteger())
    product_id: Mapped[str] = mapped_column(String(30))
    nda_type: Mapped[str | None] = mapped_column(String(10))


class FracClassification(Base):
    """ORM class for frac_classification."""

    __tablename__ = "frac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("frac_class_id", name="frac_classification_pk"),
        UniqueConstraint("level5", name="uk_frac_class_l5"),
    )
    frac_class_id: Mapped[int] = mapped_column(BigInteger())
    active_ingredient: Mapped[str] = mapped_column(String(500))
    level1: Mapped[str] = mapped_column(String(2))
    level1_description: Mapped[str] = mapped_column(String(2000))
    level2: Mapped[str] = mapped_column(String(2))
    level2_description: Mapped[str | None] = mapped_column(String(2000))
    level3: Mapped[str] = mapped_column(String(6))
    level3_description: Mapped[str | None] = mapped_column(String(2000))
    level4: Mapped[str] = mapped_column(String(7))
    level4_description: Mapped[str | None] = mapped_column(String(2000))
    level5: Mapped[str] = mapped_column(String(8))
    frac_code: Mapped[str] = mapped_column(String(4))


class HracClassification(Base):
    """ORM class for hrac_classification."""

    __tablename__ = "hrac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("hrac_class_id", name="hrac_classification_pk"),
        UniqueConstraint("level3", name="uk_hrac_class_l3"),
    )
    hrac_class_id: Mapped[int] = mapped_column(BigInteger())
    active_ingredient: Mapped[str] = mapped_column(String(500))
    level1: Mapped[str] = mapped_column(String(2))
    level1_description: Mapped[str] = mapped_column(String(2000))
    level2: Mapped[str] = mapped_column(String(3))
    level2_description: Mapped[str | None] = mapped_column(String(2000))
    level3: Mapped[str] = mapped_column(String(5))
    hrac_code: Mapped[str] = mapped_column(String(2))


class IracClassification(Base):
    """ORM class for irac_classification."""

    __tablename__ = "irac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("irac_class_id", name="irac_classification_pk"),
        UniqueConstraint("level4", name="uk_irac_class_l4"),
    )
    irac_class_id: Mapped[int] = mapped_column(BigInteger())
    active_ingredient: Mapped[str] = mapped_column(String(500))
    level1: Mapped[str] = mapped_column(String(1))
    level1_description: Mapped[str] = mapped_column(String(2000))
    level2: Mapped[str] = mapped_column(String(3))
    level2_description: Mapped[str] = mapped_column(String(2000))
    level3: Mapped[str] = mapped_column(String(6))
    level3_description: Mapped[str] = mapped_column(String(2000))
    level4: Mapped[str] = mapped_column(String(8))
    irac_code: Mapped[str] = mapped_column(String(3))


class ResearchStem(Base):
    """ORM class for research_stem."""

    __tablename__ = "research_stem"
    __table_args__ = (
        PrimaryKeyConstraint("res_stem_id", name="pk_res_stem_id"),
        UniqueConstraint("research_stem", name="uk_res_stem"),
    )
    res_stem_id: Mapped[int] = mapped_column(BigInteger())
    research_stem: Mapped[str | None] = mapped_column(String(20))


class OrganismClass(Base):
    """ORM class for organism_class."""

    __tablename__ = "organism_class"
    __table_args__ = (
        PrimaryKeyConstraint("oc_id", name="pk_orgclass_oc_id"),
        UniqueConstraint("tax_id", name="uk_orgclass_tax_id"),
        Index("organism_class_pk", "oc_id", unique=True),
    )
    oc_id: Mapped[int] = mapped_column(BigInteger())
    tax_id: Mapped[int | None] = mapped_column(BigInteger())
    l1: Mapped[str | None] = mapped_column(String(200))
    l2: Mapped[str | None] = mapped_column(String(200))
    l3: Mapped[str | None] = mapped_column(String(200))


class PatentUseCodes(Base):
    """ORM class for patent_use_codes."""

    __tablename__ = "patent_use_codes"
    __table_args__ = (
        PrimaryKeyConstraint("patent_use_code", name="patent_use_codes_pk"),
        CheckConstraint("patent_use_code LIKE ('U-%')", name="ck_patent_use_code"),
    )
    patent_use_code: Mapped[str] = mapped_column(String(8))
    definition: Mapped[str] = mapped_column(String(500))


class UsanStems(Base):
    """ORM class for usan_stems."""

    __tablename__ = "usan_stems"
    __table_args__ = (
        PrimaryKeyConstraint("usan_stem_id", name="pk_usan_stems"),
        CheckConstraint(
            "major_class IN ('GPCR', 'NR', 'PDE', 'kinase', 'ion channel', 'protease')",
            name="ck_usan_stems_mc",
        ),
        UniqueConstraint("stem", "subgroup", name="uk_usan_stems_stemsub"),
    )
    usan_stem_id: Mapped[int] = mapped_column(BigInteger())
    stem: Mapped[str] = mapped_column(String(100))
    subgroup: Mapped[str | None] = mapped_column(String(100))
    annotation: Mapped[str | None] = mapped_column(String(2000))
    stem_class: Mapped[str | None] = mapped_column(String(100))
    major_class: Mapped[str | None] = mapped_column(String(100))


class Version(Base):
    """ORM class for version."""

    __tablename__ = "version"
    __table_args__ = (PrimaryKeyConstraint("name", name="pk_version_name"),)
    name: Mapped[str] = mapped_column(String(50))
    creation_date: Mapped[datetime | None]
    comments: Mapped[str | None] = mapped_column(String(2000))


class CellDictionary(Base):
    """ORM class for cell_dictionary."""

    __tablename__ = "cell_dictionary"
    __table_args__ = (
        PrimaryKeyConstraint("cell_id", name="pk_celldict_cellid"),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_celldict_chembl_id",
            ondelete="CASCADE",
        ),
        CheckConstraint("CL_LINCS_ID LIKE ('LCL-%')", name="ck_cell_dict_lincs"),
        UniqueConstraint("cell_name", "cell_source_tax_id", name="uk_celldict"),
        UniqueConstraint("chembl_id", name="uk_cell_chembl_id"),
    )
    cell_id: Mapped[int] = mapped_column(BigInteger())
    cell_name: Mapped[str] = mapped_column(String(50))
    cell_description: Mapped[str | None] = mapped_column(String(200))
    cell_source_tissue: Mapped[str | None] = mapped_column(String(50))
    cell_source_organism: Mapped[str | None] = mapped_column(String(150))
    cell_source_tax_id: Mapped[int | None] = mapped_column(BigInteger())
    clo_id: Mapped[str | None] = mapped_column(String(11))
    efo_id: Mapped[str | None] = mapped_column(String(12))
    cellosaurus_id: Mapped[str | None] = mapped_column(String(15))
    cl_lincs_id: Mapped[str | None] = mapped_column(String(8))
    chembl_id: Mapped[str | None] = mapped_column(String(20))
    cell_ontology_id: Mapped[str | None] = mapped_column(String(10))


class Docs(Base):
    """ORM class for docs."""

    __tablename__ = "docs"
    __table_args__ = (
        PrimaryKeyConstraint("doc_id", name="pk_docs_doc_id"),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_docs_chembl_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["chembl_release_id"],
            ["chembl_release.chembl_release_id"],
            name="fk_docs_chembl_release_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["src_id"], ["source.src_id"], name="fk_docs_src_id", ondelete="CASCADE"
        ),
        CheckConstraint("chembl_id LIKE ('CHEMBL%')", name="ck_docs_chemblid"),
        CheckConstraint(
            "doc_type IN ('PUBLICATION', 'BOOK', 'DATASET', 'PATENT')", name="ck_docs_doctype"
        ),
        CheckConstraint("year < 2050 AND year > 1900", name="ck_docs_year"),
        UniqueConstraint("chembl_id", name="uk_docs_chemblid"),
        Index("bmx_doc_iss", "issue"),
        Index("idx_docs_pmid", "pubmed_id"),
        Index("bmx_doc_year", "year"),
        Index("pk_doc_doc_id", "doc_id", unique=True),
        Index("bmx_doc_jrnl", "journal"),
        Index("bmx_doc_vol", "volume"),
    )
    doc_id: Mapped[int] = mapped_column(BigInteger())
    journal: Mapped[str | None] = mapped_column(String(50))
    year: Mapped[int | None]
    volume: Mapped[str | None] = mapped_column(String(50))
    issue: Mapped[str | None] = mapped_column(String(50))
    first_page: Mapped[str | None] = mapped_column(String(50))
    last_page: Mapped[str | None] = mapped_column(String(50))
    pubmed_id: Mapped[int | None] = mapped_column(BigInteger())
    doi: Mapped[str | None] = mapped_column(String(100))
    chembl_id: Mapped[str] = mapped_column(String(20))
    title: Mapped[str | None] = mapped_column(String(500))
    doc_type: Mapped[str] = mapped_column(String(50))
    authors: Mapped[str | None] = mapped_column(String(4000))
    abstract: Mapped[str | None] = mapped_column(Text())
    patent_id: Mapped[str | None] = mapped_column(String(20))
    ridx: Mapped[str] = mapped_column(String(200))
    src_id: Mapped[int]
    chembl_release_id: Mapped[int | None]
    contact: Mapped[str | None] = mapped_column(String(200))


class TargetDictionary(Base):
    """ORM class for target_dictionary."""

    __tablename__ = "target_dictionary"
    __table_args__ = (
        PrimaryKeyConstraint("tid", name="pk_targdict_tid"),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_targdict_chembl_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["target_type"],
            ["target_type.target_type"],
            name="fk_targdict_target_type",
            ondelete="CASCADE",
        ),
        CheckConstraint("species_group_flag IN (0, 1)", name="ck_targdict_species"),
        UniqueConstraint("chembl_id", name="uk_targdict_chemblid"),
        Index("idx_td_pname", "pref_name"),
        Index("idx_td_taxid", "tax_id"),
        Index("idx_td_t_type", "target_type"),
        Index("idx_td_org", "organism"),
        Index("idx_td_chembl_id", "chembl_id"),
    )
    tid: Mapped[int] = mapped_column(BigInteger())
    target_type: Mapped[str | None] = mapped_column(String(30))
    pref_name: Mapped[str] = mapped_column(String(200))
    tax_id: Mapped[int | None] = mapped_column(BigInteger())
    organism: Mapped[str | None] = mapped_column(String(150))
    chembl_id: Mapped[str] = mapped_column(String(20))
    species_group_flag: Mapped[int] = mapped_column(SmallInteger())


class TissueDictionary(Base):
    """ORM class for tissue_dictionary."""

    __tablename__ = "tissue_dictionary"
    __table_args__ = (
        PrimaryKeyConstraint("tissue_id", name="pk_tissue_dict_tissue_id"),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_tissue_chembl_id",
            ondelete="CASCADE",
        ),
        CheckConstraint("uberon_id LIKE ('UBERON:%')", name="ck_tissue_uberon_id"),
        UniqueConstraint("chembl_id", name="uk_tissue_chembl_id"),
        UniqueConstraint("uberon_id", "efo_id", name="uk_tissue_dict_uberon_efo"),
        UniqueConstraint("pref_name", name="uk_tissue_pref_name"),
        Index("tissue_dictionary_pk", "tissue_id", unique=True),
    )
    tissue_id: Mapped[int] = mapped_column(BigInteger())
    uberon_id: Mapped[str | None] = mapped_column(String(15))
    pref_name: Mapped[str] = mapped_column(String(200))
    efo_id: Mapped[str | None] = mapped_column(String(20))
    chembl_id: Mapped[str] = mapped_column(String(20))
    bto_id: Mapped[str | None] = mapped_column(String(20))
    caloha_id: Mapped[str | None] = mapped_column(String(7))


class MoleculeDictionary(Base):
    """ORM class for molecule_dictionary."""

    __tablename__ = "molecule_dictionary"
    __table_args__ = (
        PrimaryKeyConstraint("molregno", name="pk_moldict_molregno"),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_moldict_chembl_id",
            ondelete="CASCADE",
        ),
        CheckConstraint("first_approval < 2050 AND first_approval > 1900", name="ck_moldict_app"),
        CheckConstraint("black_box_warning IN (-1, 0, 1)", name="ck_moldict_bbw"),
        CheckConstraint("chirality IN (-1, 0, 1, 2)", name="ck_moldict_chi"),
        CheckConstraint("dosed_ingredient IN (0, 1)", name="ck_moldict_dosed"),
        CheckConstraint("first_in_class IN (-1, 0, 1)", name="ck_moldict_fic"),
        CheckConstraint("inorganic_flag IN (-1, 0, 1)", name="ck_moldict_inor"),
        CheckConstraint("natural_product IN (-1, 0, 1)", name="ck_moldict_np"),
        CheckConstraint("oral IN (0, 1)", name="ck_moldict_oral"),
        CheckConstraint("parenteral IN (0, 1)", name="ck_moldict_par"),
        CheckConstraint("polymer_flag IN (0, 1, NULL)", name="ck_moldict_polyflag"),
        CheckConstraint("prodrug IN (-1, 0, 1)", name="ck_moldict_pro"),
        CheckConstraint(
            "structure_type IN ('NONE', 'MOL', 'SEQ', 'BOTH')", name="ck_moldict_strtype"
        ),
        CheckConstraint("therapeutic_flag IN (0, 1)", name="ck_moldict_theraflag"),
        CheckConstraint("topical IN (0, 1)", name="ck_moldict_top"),
        CheckConstraint("usan_year > 1900 AND usan_year < 2050", name="ck_moldict_usanyear"),
        CheckConstraint("WITHDRAWN_FLAG IN (0, 1)", name="ck_moldict_withd"),
        UniqueConstraint("chembl_id", name="uk_moldict_chemblid"),
        Index("idx_moldict_ther_flag", "therapeutic_flag"),
        Index("idx_moldict_max_phase", "max_phase"),
        Index("idx_moldict_pref_name", "pref_name"),
        Index("idx_moldict_chembl_id", "chembl_id", unique=True),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    pref_name: Mapped[str | None] = mapped_column(String(255))
    chembl_id: Mapped[str] = mapped_column(String(20))
    max_phase: Mapped[float | None] = mapped_column(Numeric(2, 1))
    therapeutic_flag: Mapped[int] = mapped_column(SmallInteger())
    dosed_ingredient: Mapped[int] = mapped_column(SmallInteger())
    structure_type: Mapped[str] = mapped_column(String(10))
    chebi_par_id: Mapped[int | None] = mapped_column(BigInteger())
    molecule_type: Mapped[str | None] = mapped_column(String(30))
    first_approval: Mapped[int | None]
    oral: Mapped[int] = mapped_column(SmallInteger())
    parenteral: Mapped[int] = mapped_column(SmallInteger())
    topical: Mapped[int] = mapped_column(SmallInteger())
    black_box_warning: Mapped[int] = mapped_column(SmallInteger())
    natural_product: Mapped[int] = mapped_column(SmallInteger())
    first_in_class: Mapped[int] = mapped_column(SmallInteger())
    chirality: Mapped[int] = mapped_column(SmallInteger())
    prodrug: Mapped[int] = mapped_column(SmallInteger())
    inorganic_flag: Mapped[int] = mapped_column(SmallInteger())
    usan_year: Mapped[int | None]
    availability_type: Mapped[int | None] = mapped_column(SmallInteger())
    usan_stem: Mapped[str | None] = mapped_column(String(50))
    polymer_flag: Mapped[int | None] = mapped_column(SmallInteger())
    usan_substem: Mapped[str | None] = mapped_column(String(50))
    usan_stem_definition: Mapped[str | None] = mapped_column(String(1000))
    indication_class: Mapped[str | None] = mapped_column(String(1000))
    withdrawn_flag: Mapped[int] = mapped_column(SmallInteger())
    chemical_probe: Mapped[int] = mapped_column(SmallInteger())
    orphan: Mapped[int] = mapped_column(SmallInteger())


class ActivitySupp(Base):
    """ORM class for activity_supp."""

    __tablename__ = "activity_supp"
    __table_args__ = (
        PrimaryKeyConstraint("as_id", name="pk_actsupp_as_id"),
        ForeignKeyConstraint(
            ["smid"], ["activity_smid.smid"], name="fk_act_smids", ondelete="CASCADE"
        ),
        UniqueConstraint("rgid", "type", name="uk_actsupp_rgid_type"),
        Index("idx_actsupp_std_val", "standard_value"),
        Index("idx_actsupp_text", "text_value"),
        Index("idx_actsupp_type", "type"),
        Index("idx_actsupp_units", "units"),
        Index("idx_actsupp_val", "value"),
        Index("idx_actsupp_std_units", "standard_units"),
        Index("idx_actsupp_std_rel", "standard_relation"),
        Index("idx_actsupp_rel", "relation"),
        Index("idx_actsupp_std_type", "standard_type"),
        Index("idx_actsupp_std_text", "standard_text_value"),
    )
    as_id: Mapped[int] = mapped_column(BigInteger())
    rgid: Mapped[int] = mapped_column(BigInteger())
    smid: Mapped[int | None] = mapped_column(BigInteger())
    type: Mapped[str] = mapped_column(String(250))
    relation: Mapped[str | None] = mapped_column(String(50))
    value: Mapped[float | None]
    units: Mapped[str | None] = mapped_column(String(100))
    text_value: Mapped[str | None] = mapped_column(String(1000))
    standard_type: Mapped[str | None] = mapped_column(String(250))
    standard_relation: Mapped[str | None] = mapped_column(String(50))
    standard_value: Mapped[float | None]
    standard_units: Mapped[str | None] = mapped_column(String(100))
    standard_text_value: Mapped[str | None] = mapped_column(String(1000))
    comments: Mapped[str | None] = mapped_column(String(4000))


class ComponentClass(Base):
    """ORM class for component_class."""

    __tablename__ = "component_class"
    __table_args__ = (
        PrimaryKeyConstraint("comp_class_id", name="pk_comp_class_id"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_comp_class_compid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["protein_class_id"],
            ["protein_classification.protein_class_id"],
            name="fk_comp_class_pcid",
            ondelete="CASCADE",
        ),
        UniqueConstraint("component_id", "protein_class_id", name="uk_comp_class"),
    )
    component_id: Mapped[int] = mapped_column(BigInteger())
    protein_class_id: Mapped[int] = mapped_column(BigInteger())
    comp_class_id: Mapped[int] = mapped_column(BigInteger())


class ComponentDomains(Base):
    """ORM class for component_domains."""

    __tablename__ = "component_domains"
    __table_args__ = (
        PrimaryKeyConstraint("compd_id", name="pk_compd_id"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_compd_compid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["domain_id"], ["domains.domain_id"], name="fk_compd_domainid", ondelete="CASCADE"
        ),
        CheckConstraint("end_position > 0", name="ck_compd_end"),
        CheckConstraint("start_position > 0", name="ck_compd_start"),
        UniqueConstraint("domain_id", "component_id", "start_position", name="uk_compd_start"),
    )
    compd_id: Mapped[int] = mapped_column(BigInteger())
    domain_id: Mapped[int | None] = mapped_column(BigInteger())
    component_id: Mapped[int] = mapped_column(BigInteger())
    start_position: Mapped[int | None] = mapped_column(BigInteger())
    end_position: Mapped[int | None] = mapped_column(BigInteger())


class ComponentGo(Base):
    """ORM class for component_go."""

    __tablename__ = "component_go"
    __table_args__ = (
        PrimaryKeyConstraint("comp_go_id", name="pk_comp_go"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_comp_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["go_id"], ["go_classification.go_id"], name="fk_go_id", ondelete="CASCADE"
        ),
        UniqueConstraint("component_id", "go_id", name="uk_comp_go"),
    )
    comp_go_id: Mapped[int] = mapped_column(BigInteger())
    component_id: Mapped[int] = mapped_column(BigInteger())
    go_id: Mapped[str] = mapped_column(String(10))


class ComponentSynonyms(Base):
    """ORM class for component_synonyms."""

    __tablename__ = "component_synonyms"
    __table_args__ = (
        PrimaryKeyConstraint("compsyn_id", name="pk_compsyn_synid"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_compsyn_compid",
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "syn_type IN ('GENE_SYMBOL', 'GENE_SYMBOL_OTHER', 'UNIPROT', 'MANUAL', 'OTHER', 'EC_NUMBER')",
            name="ck_compsyn_syntype",
        ),
        UniqueConstraint("component_id", "component_synonym", "syn_type", name="uk_compsyn"),
    )
    compsyn_id: Mapped[int] = mapped_column(BigInteger())
    component_id: Mapped[int] = mapped_column(BigInteger())
    component_synonym: Mapped[str | None] = mapped_column(String(500))
    syn_type: Mapped[str | None] = mapped_column(String(20))


class StructuralAlerts(Base):
    """ORM class for structural_alerts."""

    __tablename__ = "structural_alerts"
    __table_args__ = (
        PrimaryKeyConstraint("alert_id", name="pk_str_alert_id"),
        ForeignKeyConstraint(
            ["alert_set_id"],
            ["structural_alert_sets.alert_set_id"],
            name="fk_str_alert_set_id",
            ondelete="CASCADE",
        ),
        UniqueConstraint("alert_set_id", "alert_name", "smarts", name="uk_str_alert_smarts"),
    )
    alert_id: Mapped[int] = mapped_column(BigInteger())
    alert_set_id: Mapped[int] = mapped_column(BigInteger())
    alert_name: Mapped[str] = mapped_column(String(100))
    smarts: Mapped[str] = mapped_column(String(4000))


class DefinedDailyDose(Base):
    """ORM class for defined_daily_dose."""

    __tablename__ = "defined_daily_dose"
    __table_args__ = (
        PrimaryKeyConstraint("ddd_id", name="pk_ddd_id"),
        ForeignKeyConstraint(
            ["atc_code"], ["atc_classification.level5"], name="fk_ddd_atccode", ondelete="CASCADE"
        ),
    )
    atc_code: Mapped[str] = mapped_column(String(10))
    ddd_units: Mapped[str | None] = mapped_column(String(200))
    ddd_admr: Mapped[str | None] = mapped_column(String(1000))
    ddd_comment: Mapped[str | None] = mapped_column(String(2000))
    ddd_id: Mapped[int] = mapped_column(BigInteger())
    ddd_value: Mapped[float | None]


class ProductPatents(Base):
    """ORM class for product_patents."""

    __tablename__ = "product_patents"
    __table_args__ = (
        PrimaryKeyConstraint("prod_pat_id", name="pk_prod_pat_id"),
        ForeignKeyConstraint(
            ["product_id"],
            ["products.product_id"],
            name="fk_prod_pat_product_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["patent_use_code"],
            ["patent_use_codes.patent_use_code"],
            name="fk_prod_pat_use_code",
            ondelete="CASCADE",
        ),
        CheckConstraint("delist_flag IN (0, 1)", name="ck_patents_delistflag"),
        CheckConstraint("drug_product_flag IN (0, 1)", name="ck_patents_prodflag"),
        CheckConstraint("drug_substance_flag IN (0, 1)", name="ck_patents_subsflag"),
        UniqueConstraint(
            "product_id", "patent_no", "patent_expire_date", "patent_use_code", name="uk_prod_pat"
        ),
    )
    prod_pat_id: Mapped[int] = mapped_column(BigInteger())
    product_id: Mapped[str] = mapped_column(String(30))
    patent_no: Mapped[str] = mapped_column(String(20))
    patent_expire_date: Mapped[datetime]
    drug_substance_flag: Mapped[int] = mapped_column(SmallInteger())
    drug_product_flag: Mapped[int] = mapped_column(SmallInteger())
    patent_use_code: Mapped[str | None] = mapped_column(String(10))
    delist_flag: Mapped[int] = mapped_column(SmallInteger())
    submission_date: Mapped[datetime | None]


class ProteinClassSynonyms(Base):
    """ORM class for protein_class_synonyms."""

    __tablename__ = "protein_class_synonyms"
    __table_args__ = (
        PrimaryKeyConstraint("protclasssyn_id", name="pk_protclasssyn_synid"),
        ForeignKeyConstraint(
            ["protein_class_id"],
            ["protein_classification.protein_class_id"],
            name="fk_protclasssyn_protclass_id",
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "syn_type IN ('CHEMBL', 'CONCEPT_WIKI', 'UMLS', 'CW_XREF', 'MESH_XREF')",
            name="ck_protclasssyn_syntype",
        ),
        UniqueConstraint(
            "protein_class_id", "protein_class_synonym", "syn_type", name="uk_protclasssyn"
        ),
    )
    protclasssyn_id: Mapped[int] = mapped_column(BigInteger())
    protein_class_id: Mapped[int] = mapped_column(BigInteger())
    protein_class_synonym: Mapped[str | None] = mapped_column(String(1000))
    syn_type: Mapped[str | None] = mapped_column(String(20))


class ResearchCompanies(Base):
    """ORM class for research_companies."""

    __tablename__ = "research_companies"
    __table_args__ = (
        PrimaryKeyConstraint("co_stem_id", name="pk_resco_co_stem_id"),
        ForeignKeyConstraint(
            ["res_stem_id"],
            ["research_stem.res_stem_id"],
            name="fk_resco_res_stem_id",
            ondelete="CASCADE",
        ),
        UniqueConstraint("res_stem_id", "company", name="uk_resco_stem_co"),
    )
    co_stem_id: Mapped[int] = mapped_column(BigInteger())
    res_stem_id: Mapped[int | None] = mapped_column(BigInteger())
    company: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(50))
    previous_company: Mapped[str | None] = mapped_column(String(100))


class Assays(Base):
    """ORM class for assays."""

    __tablename__ = "assays"
    __table_args__ = (
        PrimaryKeyConstraint("assay_id", name="pk_assays_assay_id"),
        ForeignKeyConstraint(
            ["assay_type"],
            ["assay_type.assay_type"],
            name="fk_assays_assaytype",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["cell_id"], ["cell_dictionary.cell_id"], name="fk_assays_cell_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["chembl_id"],
            ["chembl_id_lookup.chembl_id"],
            name="fk_assays_chembl_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["confidence_score"],
            ["confidence_score_lookup.confidence_score"],
            name="fk_assays_confscore",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["curated_by"],
            ["curation_lookup.curated_by"],
            name="fk_assays_cur_by",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["doc_id"], ["docs.doc_id"], name="fk_assays_doc_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["relationship_type"],
            ["relationship_type.relationship_type"],
            name="fk_assays_reltype",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["src_id"], ["source.src_id"], name="fk_assays_src_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["tid"], ["target_dictionary.tid"], name="fk_assays_tid", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["tissue_id"],
            ["tissue_dictionary.tissue_id"],
            name="fk_assays_tissue_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["variant_id"],
            ["variant_sequences.variant_id"],
            name="fk_assays_variant_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["bao_format"],
            ["bioassay_ontology.bao_id"],
            name="fk_chembl_bao_format",
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "assay_category IN ('screening', 'panel', 'confirmatory', 'summary', 'other', 'Thermal shift assay QC liability', 'Thermal shift assay', 'Affinity biochemical assay', 'Incucyte cell viability', 'Affinity phenotypic cellular assay', 'HTRF assay', 'Selectivity assay', 'Cell health data', 'NanoBRET assay', 'Alphascreen assay', 'Affinity on-target cellular assay', 'ITC assay', 'GPCR beta-arrestin recruitment assay', 'PDSP assay')",
            name="ck_assays_category",
        ),
        CheckConstraint("chembl_id LIKE ('CHEMBL%')", name="ck_assays_chemblid"),
        CheckConstraint(
            "assay_test_type IN ('In vivo', 'In vitro', 'Ex vivo')", name="ck_assays_testtype"
        ),
        UniqueConstraint("chembl_id", name="uk_assays_chemblid"),
        Index("idx_assays_desc", "description"),
        Index("tmp_bao_format", "bao_format"),
        Index("idx_assays_chembl_id", "chembl_id", unique=True),
        Index("idx_assay_assay_id", "assay_type"),
        Index("idx_assays_src_id", "src_id"),
        Index("idx_assays_doc_id", "doc_id"),
    )
    assay_id: Mapped[int] = mapped_column(BigInteger())
    doc_id: Mapped[int] = mapped_column(BigInteger())
    description: Mapped[str | None] = mapped_column(String(4000))
    assay_type: Mapped[str | None] = mapped_column(String(1))
    assay_test_type: Mapped[str | None] = mapped_column(String(20))
    assay_category: Mapped[str | None] = mapped_column(String(50))
    assay_organism: Mapped[str | None] = mapped_column(String(250))
    assay_tax_id: Mapped[int | None] = mapped_column(BigInteger())
    assay_strain: Mapped[str | None] = mapped_column(String(200))
    assay_tissue: Mapped[str | None] = mapped_column(String(100))
    assay_cell_type: Mapped[str | None] = mapped_column(String(100))
    assay_subcellular_fraction: Mapped[str | None] = mapped_column(String(100))
    tid: Mapped[int | None] = mapped_column(BigInteger())
    relationship_type: Mapped[str | None] = mapped_column(String(1))
    confidence_score: Mapped[int | None] = mapped_column(SmallInteger())
    curated_by: Mapped[str | None] = mapped_column(String(32))
    src_id: Mapped[int]
    src_assay_id: Mapped[str | None] = mapped_column(String(50))
    chembl_id: Mapped[str] = mapped_column(String(20))
    cell_id: Mapped[int | None] = mapped_column(BigInteger())
    bao_format: Mapped[str | None] = mapped_column(String(11))
    tissue_id: Mapped[int | None] = mapped_column(BigInteger())
    variant_id: Mapped[int | None] = mapped_column(BigInteger())
    aidx: Mapped[str] = mapped_column(String(200))
    assay_group: Mapped[str | None] = mapped_column(String(200))


class CompoundRecords(Base):
    """ORM class for compound_records."""

    __tablename__ = "compound_records"
    __table_args__ = (
        PrimaryKeyConstraint("record_id", name="pk_cmpdrec_record_id"),
        ForeignKeyConstraint(
            ["doc_id"], ["docs.doc_id"], name="fk_cmpdrec_doc_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_cmpdrec_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["src_id"], ["source.src_id"], name="fk_cmpdrec_src_id", ondelete="CASCADE"
        ),
        Index("fk_comp_rec_docid", "doc_id"),
        Index("idx_comp_rec_ckey", "compound_key"),
        Index("idx_comp_rec_cidx", "cidx"),
        Index("idx_comp_rec_srccpid", "src_compound_id"),
        Index("idx_comp_rec_srcid", "src_id"),
        Index("fk_comp_rec_molregno", "molregno"),
        Index("pk_comp_rec_recid", "record_id", unique=True),
    )
    record_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    doc_id: Mapped[int] = mapped_column(BigInteger())
    compound_key: Mapped[str | None] = mapped_column(String(250))
    compound_name: Mapped[str | None] = mapped_column(String(4000))
    src_id: Mapped[int]
    src_compound_id: Mapped[str | None] = mapped_column(String(150))
    cidx: Mapped[str] = mapped_column(String(200))


class BindingSites(Base):
    """ORM class for binding_sites."""

    __tablename__ = "binding_sites"
    __table_args__ = (
        PrimaryKeyConstraint("site_id", name="pk_bindsite_id"),
        ForeignKeyConstraint(
            ["tid"], ["target_dictionary.tid"], name="fk_bindsite_tid", ondelete="CASCADE"
        ),
    )
    site_id: Mapped[int] = mapped_column(BigInteger())
    site_name: Mapped[str | None] = mapped_column(String(200))
    tid: Mapped[int | None] = mapped_column(BigInteger())


class Biotherapeutics(Base):
    """ORM class for biotherapeutics."""

    __tablename__ = "biotherapeutics"
    __table_args__ = (
        PrimaryKeyConstraint("molregno", name="pk_biother_molregno"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_biother_molregno",
            ondelete="CASCADE",
        ),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    description: Mapped[str | None] = mapped_column(String(2000))
    helm_notation: Mapped[str | None] = mapped_column(String(4000))


class CompoundProperties(Base):
    """ORM class for compound_properties."""

    __tablename__ = "compound_properties"
    __table_args__ = (
        PrimaryKeyConstraint("molregno", name="pk_cmpdprop_molregno"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_cmpdprop_molregno",
            ondelete="CASCADE",
        ),
        CheckConstraint("aromatic_rings >= 0", name="ck_cmpdprop_aromatic"),
        CheckConstraint("CX_MOST_BPKA >= 0", name="ck_cmpdprop_bpka"),
        CheckConstraint("full_mwt > 0", name="ck_cmpdprop_fullmw"),
        CheckConstraint("hba >= 0", name="ck_cmpdprop_hba"),
        CheckConstraint("hba_lipinski >= 0", name="ck_cmpdprop_hba_lip"),
        CheckConstraint("hbd >= 0", name="ck_cmpdprop_hbd"),
        CheckConstraint("hbd_lipinski >= 0", name="ck_cmpdprop_hbd_lip"),
        CheckConstraint("heavy_atoms >= 0", name="ck_cmpdprop_heavy"),
        CheckConstraint(
            "num_lipinski_ro5_violations IN (0, 1, 2, 3, 4)", name="ck_cmpdprop_lip_ro5"
        ),
        CheckConstraint("mw_freebase > 0", name="ck_cmpdprop_mwfree"),
        CheckConstraint("psa >= 0", name="ck_cmpdprop_psa"),
        CheckConstraint("qed_weighted >= 0", name="ck_cmpdprop_qed"),
        CheckConstraint("ro3_pass IN ('Y', 'N')", name="ck_cmpdprop_ro3"),
        CheckConstraint("num_ro5_violations IN (0, 1, 2, 3, 4)", name="ck_cmpdprop_ro5"),
        CheckConstraint("rtb >= 0", name="ck_cmpdprop_rtb"),
        CheckConstraint(
            "molecular_species IN ('ACID', 'BASE', 'ZWITTERION', 'NEUTRAL')",
            name="ck_cmpdprop_species",
        ),
        Index("pk_com_molreg", "molregno", unique=True),
        Index("idx_cp_mw", "mw_freebase"),
        Index("idx_cp_hba", "hba"),
        Index("idx_cp_alogp", "alogp"),
        Index("idx_cp_ro5", "num_ro5_violations"),
        Index("idx_cp_rtb", "rtb"),
        Index("idx_cp_hbd", "hbd"),
        Index("idx_cp_psa", "psa"),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    mw_freebase: Mapped[float | None] = mapped_column(Numeric(9, 2))
    alogp: Mapped[float | None] = mapped_column(Numeric(9, 2))
    hba: Mapped[int | None]
    hbd: Mapped[int | None]
    psa: Mapped[float | None] = mapped_column(Numeric(9, 2))
    rtb: Mapped[int | None]
    ro3_pass: Mapped[str | None] = mapped_column(String(3))
    num_ro5_violations: Mapped[int | None] = mapped_column(SmallInteger())
    cx_most_apka: Mapped[float | None] = mapped_column(Numeric(9, 2))
    cx_most_bpka: Mapped[float | None] = mapped_column(Numeric(9, 2))
    cx_logp: Mapped[float | None] = mapped_column(Numeric(9, 2))
    cx_logd: Mapped[float | None] = mapped_column(Numeric(9, 2))
    molecular_species: Mapped[str | None] = mapped_column(String(50))
    full_mwt: Mapped[float | None] = mapped_column(Numeric(9, 2))
    aromatic_rings: Mapped[int | None]
    heavy_atoms: Mapped[int | None]
    qed_weighted: Mapped[float | None] = mapped_column(Numeric(3, 2))
    mw_monoisotopic: Mapped[float | None] = mapped_column(Numeric(11, 4))
    full_molformula: Mapped[str | None] = mapped_column(String(100))
    hba_lipinski: Mapped[int | None]
    hbd_lipinski: Mapped[int | None]
    num_lipinski_ro5_violations: Mapped[int | None] = mapped_column(SmallInteger())
    np_likeness_score: Mapped[float | None] = mapped_column(Numeric(3, 2))


class CompoundStructuralAlerts(Base):
    """ORM class for compound_structural_alerts."""

    __tablename__ = "compound_structural_alerts"
    __table_args__ = (
        PrimaryKeyConstraint("cpd_str_alert_id", name="pk_cpd_str_alert_id"),
        ForeignKeyConstraint(
            ["alert_id"],
            ["structural_alerts.alert_id"],
            name="fk_cpd_str_alert_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_cpd_str_alert_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("molregno", "alert_id", name="uk_cpd_str_alert"),
    )
    cpd_str_alert_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int] = mapped_column(BigInteger())
    alert_id: Mapped[int] = mapped_column(BigInteger())


class CompoundStructures(Base):
    """ORM class for compound_structures."""

    __tablename__ = "compound_structures"
    __table_args__ = (
        PrimaryKeyConstraint("molregno", name="pk_cmpdstr_molregno"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_cmpdstr_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("standard_inchi", name="uk_cmpdstr_stdinch"),
        UniqueConstraint("standard_inchi_key", name="uk_cmpdstr_stdinchkey"),
        Index("compound_structures_pk", "molregno", unique=True),
        Index("idx_cmpdstr_stdinchi", "standard_inchi"),
        Index("idx_cmpdstr_smiles", "canonical_smiles"),
        Index("idx_cmpdstr_stdkey", "standard_inchi_key"),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    molfile: Mapped[str | None] = mapped_column(Text())
    standard_inchi: Mapped[str | None] = mapped_column(String(4000))
    standard_inchi_key: Mapped[str] = mapped_column(String(27))
    canonical_smiles: Mapped[str | None] = mapped_column(String(4000))


class MoleculeAtcClassification(Base):
    """ORM class for molecule_atc_classification."""

    __tablename__ = "molecule_atc_classification"
    __table_args__ = (
        PrimaryKeyConstraint("mol_atc_id", name="pk_molatc_mol_atc_id"),
        ForeignKeyConstraint(
            ["level5"], ["atc_classification.level5"], name="fk_molatc_level5", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_molatc_molregno",
            ondelete="CASCADE",
        ),
    )
    mol_atc_id: Mapped[int] = mapped_column(BigInteger())
    level5: Mapped[str] = mapped_column(String(10))
    molregno: Mapped[int] = mapped_column(BigInteger())


class MoleculeFracClassification(Base):
    """ORM class for molecule_frac_classification."""

    __tablename__ = "molecule_frac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("mol_frac_id", name="molecule_frac_classificationpk"),
        ForeignKeyConstraint(
            ["frac_class_id"],
            ["frac_classification.frac_class_id"],
            name="fk_frac_class_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_frac_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("frac_class_id", "molregno", name="uk_mol_frac_class"),
    )
    mol_frac_id: Mapped[int] = mapped_column(BigInteger())
    frac_class_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int] = mapped_column(BigInteger())


class MoleculeHierarchy(Base):
    """ORM class for molecule_hierarchy."""

    __tablename__ = "molecule_hierarchy"
    __table_args__ = (
        PrimaryKeyConstraint("molregno", name="pk_molhier_molregno"),
        ForeignKeyConstraint(
            ["active_molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_molhier_active_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_molhier_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["parent_molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_molhier_parent_molregno",
            ondelete="CASCADE",
        ),
        Index("idx_molhier_parent", "parent_molregno"),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    parent_molregno: Mapped[int | None] = mapped_column(BigInteger())
    active_molregno: Mapped[int | None] = mapped_column(BigInteger())


class MoleculeHracClassification(Base):
    """ORM class for molecule_hrac_classification."""

    __tablename__ = "molecule_hrac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("mol_hrac_id", name="molecule_hrac_classificationpk"),
        ForeignKeyConstraint(
            ["hrac_class_id"],
            ["hrac_classification.hrac_class_id"],
            name="fk_hrac_class_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_hrac_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("hrac_class_id", "molregno", name="uk_mol_hrac_class"),
    )
    mol_hrac_id: Mapped[int] = mapped_column(BigInteger())
    hrac_class_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int] = mapped_column(BigInteger())


class MoleculeIracClassification(Base):
    """ORM class for molecule_irac_classification."""

    __tablename__ = "molecule_irac_classification"
    __table_args__ = (
        PrimaryKeyConstraint("mol_irac_id", name="molecule_irac_classificationpk"),
        ForeignKeyConstraint(
            ["irac_class_id"],
            ["irac_classification.irac_class_id"],
            name="fk_irac_class_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_irac_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("irac_class_id", "molregno", name="uk_mol_irac_class"),
    )
    mol_irac_id: Mapped[int] = mapped_column(BigInteger())
    irac_class_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int] = mapped_column(BigInteger())


class MoleculeSynonyms(Base):
    """ORM class for molecule_synonyms."""

    __tablename__ = "molecule_synonyms"
    __table_args__ = (
        PrimaryKeyConstraint("molsyn_id", name="pk_cmpdsyns_synid"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_cmpdsyns_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["res_stem_id"],
            ["research_stem.res_stem_id"],
            name="fk_cmpdsyns_resstem",
            ondelete="CASCADE",
        ),
        UniqueConstraint("molregno", "syn_type", "synonyms", name="uk_cmpdsyns"),
    )
    molregno: Mapped[int] = mapped_column(BigInteger())
    syn_type: Mapped[str] = mapped_column(String(50))
    molsyn_id: Mapped[int] = mapped_column(BigInteger())
    res_stem_id: Mapped[int | None] = mapped_column(BigInteger())
    synonyms: Mapped[str | None] = mapped_column(String(250))


class TargetComponents(Base):
    """ORM class for target_components."""

    __tablename__ = "target_components"
    __table_args__ = (
        PrimaryKeyConstraint("targcomp_id", name="pk_targcomp_id"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_targcomp_compid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["tid"], ["target_dictionary.tid"], name="fk_targcomp_tid", ondelete="CASCADE"
        ),
        CheckConstraint("homologue IN (0, 1, 2)", name="ck_targcomp_hom"),
        UniqueConstraint("tid", "component_id", name="uk_targcomp_tid_compid"),
    )
    tid: Mapped[int] = mapped_column(BigInteger())
    component_id: Mapped[int] = mapped_column(BigInteger())
    targcomp_id: Mapped[int] = mapped_column(BigInteger())
    homologue: Mapped[int] = mapped_column(SmallInteger())


class TargetRelations(Base):
    """ORM class for target_relations."""

    __tablename__ = "target_relations"
    __table_args__ = (
        PrimaryKeyConstraint("targrel_id", name="target_relations_pk"),
        ForeignKeyConstraint(
            ["related_tid"], ["target_dictionary.tid"], name="fk_targrel_reltid", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["tid"], ["target_dictionary.tid"], name="fk_targrel_tid", ondelete="CASCADE"
        ),
        CheckConstraint(
            "relationship IN ('EQUIVALENT TO', 'OVERLAPS WITH', 'SUBSET OF', 'SUPERSET OF')",
            name="ck_targrel_rel",
        ),
    )
    tid: Mapped[int] = mapped_column(BigInteger())
    relationship: Mapped[str] = mapped_column(String(20))
    related_tid: Mapped[int] = mapped_column(BigInteger())
    targrel_id: Mapped[int] = mapped_column(BigInteger())


class Activities(Base):
    """ORM class for activities."""

    __tablename__ = "activities"
    __table_args__ = (
        PrimaryKeyConstraint("activity_id", name="pk_act_activity_id"),
        ForeignKeyConstraint(
            ["action_type"],
            ["action_type.action_type"],
            name="fk_act_action_type",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["assay_id"], ["assays.assay_id"], name="fk_act_assay_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["bao_endpoint"],
            ["bioassay_ontology.bao_id"],
            name="fk_act_bao_endpoint",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(["doc_id"], ["docs.doc_id"], name="fk_act_doc_id", ondelete="CASCADE"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_act_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["record_id"],
            ["compound_records.record_id"],
            name="fk_act_record_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["src_id"], ["source.src_id"], name="fk_act_src_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["data_validity_comment"],
            ["data_validity_lookup.data_validity_comment"],
            name="fk_data_val_comm",
            ondelete="CASCADE",
        ),
        CheckConstraint("POTENTIAL_DUPLICATE IN (0, 1)", name="ck_potential_dup"),
        CheckConstraint("standard_flag IN (0, 1)", name="ck_stand_flag"),
        CheckConstraint(
            "standard_relation IN ('>', '<', '=', '~', '<=', '>=', '<<', '>>')",
            name="ck_stand_relation",
        ),
        Index("fk_act_doc_id", "doc_id"),
        Index("idx_act_val", "value"),
        Index("idx_act_units", "units"),
        Index("fk_act_molregno", "molregno"),
        Index("fk_act_record_id", "record_id"),
        Index("idx_act_text", "text_value"),
        Index("idx_act_type", "type"),
        Index("idx_acc_relation", "standard_relation"),
        Index("fk_act_assay_id", "assay_id"),
        Index("idx_act_pchembl", "pchembl_value"),
        Index("idx_act_rel", "relation"),
        Index("idx_act_src_id", "src_id"),
        Index("idx_act_std_text", "standard_text_value"),
        Index("idx_act_std_type", "standard_type"),
        Index("idx_act_std_unit", "standard_units"),
        Index("idx_act_std_upper", "standard_upper_value"),
        Index("idx_act_std_val", "standard_value"),
        Index("idx_act_upper", "upper_value"),
    )
    activity_id: Mapped[int] = mapped_column(BigInteger())
    assay_id: Mapped[int] = mapped_column(BigInteger())
    doc_id: Mapped[int | None] = mapped_column(BigInteger())
    record_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    standard_relation: Mapped[str | None] = mapped_column(String(50))
    standard_value: Mapped[float | None]
    standard_units: Mapped[str | None] = mapped_column(String(100))
    standard_flag: Mapped[int | None] = mapped_column(SmallInteger())
    standard_type: Mapped[str | None] = mapped_column(String(250))
    activity_comment: Mapped[str | None] = mapped_column(String(4000))
    data_validity_comment: Mapped[str | None] = mapped_column(String(30))
    potential_duplicate: Mapped[int | None] = mapped_column(SmallInteger())
    pchembl_value: Mapped[float | None] = mapped_column(Numeric(4, 2))
    bao_endpoint: Mapped[str | None] = mapped_column(String(11))
    uo_units: Mapped[str | None] = mapped_column(String(10))
    qudt_units: Mapped[str | None] = mapped_column(String(70))
    toid: Mapped[int | None]
    upper_value: Mapped[float | None]
    standard_upper_value: Mapped[float | None]
    src_id: Mapped[int | None]
    type: Mapped[str] = mapped_column(String(250))
    relation: Mapped[str | None] = mapped_column(String(50))
    value: Mapped[float | None]
    units: Mapped[str | None] = mapped_column(String(100))
    text_value: Mapped[str | None] = mapped_column(String(1000))
    standard_text_value: Mapped[str | None] = mapped_column(String(1000))
    action_type: Mapped[str | None] = mapped_column(String(50))


class AssayClassMap(Base):
    """ORM class for assay_class_map."""

    __tablename__ = "assay_class_map"
    __table_args__ = (
        PrimaryKeyConstraint("ass_cls_map_id", name="pk_assay_cls_map"),
        ForeignKeyConstraint(
            ["assay_id"], ["assays.assay_id"], name="fk_ass_cls_map_assay", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["assay_class_id"],
            ["assay_classification.assay_class_id"],
            name="fk_ass_cls_map_class",
            ondelete="CASCADE",
        ),
        UniqueConstraint("assay_id", "assay_class_id", name="uk_ass_cls_map"),
    )
    ass_cls_map_id: Mapped[int] = mapped_column(BigInteger())
    assay_id: Mapped[int] = mapped_column(BigInteger())
    assay_class_id: Mapped[int] = mapped_column(BigInteger())


class AssayParameters(Base):
    """ORM class for assay_parameters."""

    __tablename__ = "assay_parameters"
    __table_args__ = (
        PrimaryKeyConstraint("assay_param_id", name="pk_assay_param"),
        ForeignKeyConstraint(
            ["assay_id"], ["assays.assay_id"], name="fk_assay_param_assayid", ondelete="CASCADE"
        ),
        UniqueConstraint("assay_id", "type", name="uk_assay_param"),
        Index("idx_assay_param_std_type", "standard_type"),
        Index("idx_assay_param_std_rel", "standard_relation"),
        Index("idx_assay_param_std_val", "standard_value"),
        Index("idx_assay_param_text", "text_value"),
        Index("idx_assay_param_rel", "relation"),
        Index("idx_assay_param_std_text", "standard_text_value"),
        Index("idx_assay_param_type", "type"),
        Index("idx_assay_param_units", "units"),
        Index("idx_assay_param_std_units", "standard_units"),
        Index("idx_assay_param_val", "value"),
    )
    assay_param_id: Mapped[int] = mapped_column(BigInteger())
    assay_id: Mapped[int] = mapped_column(BigInteger())
    type: Mapped[str] = mapped_column(String(250))
    relation: Mapped[str | None] = mapped_column(String(50))
    value: Mapped[float | None]
    units: Mapped[str | None] = mapped_column(String(100))
    text_value: Mapped[str | None] = mapped_column(String(4000))
    standard_type: Mapped[str | None] = mapped_column(String(250))
    standard_relation: Mapped[str | None] = mapped_column(String(50))
    standard_value: Mapped[float | None]
    standard_units: Mapped[str | None] = mapped_column(String(100))
    standard_text_value: Mapped[str | None] = mapped_column(String(4000))
    comments: Mapped[str | None] = mapped_column(String(4000))


class BiotherapeuticComponents(Base):
    """ORM class for biotherapeutic_components."""

    __tablename__ = "biotherapeutic_components"
    __table_args__ = (
        PrimaryKeyConstraint("biocomp_id", name="pk_biocomp_id"),
        ForeignKeyConstraint(
            ["component_id"],
            ["bio_component_sequences.component_id"],
            name="fk_biocomp_compid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["biotherapeutics.molregno"],
            name="fk_biocomp_molregno",
            ondelete="CASCADE",
        ),
        UniqueConstraint("molregno", "component_id", name="uk_biocomp"),
    )
    biocomp_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int] = mapped_column(BigInteger())
    component_id: Mapped[int] = mapped_column(BigInteger())


class DrugIndication(Base):
    """ORM class for drug_indication."""

    __tablename__ = "drug_indication"
    __table_args__ = (
        PrimaryKeyConstraint("drugind_id", name="drugind_pk"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="drugind_molregno_fk",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["record_id"], ["compound_records.record_id"], name="drugind_rec_fk", ondelete="CASCADE"
        ),
        UniqueConstraint("record_id", "mesh_id", "efo_id", name="drugind_uk"),
        Index("drug_indication_pk", "drugind_id", unique=True),
    )
    drugind_id: Mapped[int] = mapped_column(BigInteger())
    record_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    max_phase_for_ind: Mapped[float | None] = mapped_column(Numeric(2, 1))
    mesh_id: Mapped[str] = mapped_column(String(20))
    mesh_heading: Mapped[str] = mapped_column(String(200))
    efo_id: Mapped[str | None] = mapped_column(String(20))
    efo_term: Mapped[str | None] = mapped_column(String(200))


class DrugMechanism(Base):
    """ORM class for drug_mechanism."""

    __tablename__ = "drug_mechanism"
    __table_args__ = (
        PrimaryKeyConstraint("mec_id", name="molecule_mechanism_pk"),
        ForeignKeyConstraint(
            ["action_type"],
            ["action_type.action_type"],
            name="fk_drugmec_actiontype",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_drugmec_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["record_id"],
            ["compound_records.record_id"],
            name="fk_drugmec_rec_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["site_id"], ["binding_sites.site_id"], name="fk_drugmec_site_id", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["tid"], ["target_dictionary.tid"], name="fk_drugmec_tid", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["variant_id"],
            ["variant_sequences.variant_id"],
            name="fk_drugmec_varid",
            ondelete="CASCADE",
        ),
        CheckConstraint("direct_interaction IN (0, 1)", name="ck_drugmec_direct"),
        CheckConstraint("disease_efficacy IN (0, 1)", name="ck_drugmec_efficacy"),
        CheckConstraint("molecular_mechanism IN (0, 1)", name="ck_drugmec_molecular"),
    )
    mec_id: Mapped[int] = mapped_column(BigInteger())
    record_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    mechanism_of_action: Mapped[str | None] = mapped_column(String(250))
    tid: Mapped[int | None] = mapped_column(BigInteger())
    site_id: Mapped[int | None] = mapped_column(BigInteger())
    action_type: Mapped[str | None] = mapped_column(String(50))
    direct_interaction: Mapped[int | None] = mapped_column(SmallInteger())
    molecular_mechanism: Mapped[int | None] = mapped_column(SmallInteger())
    disease_efficacy: Mapped[int | None] = mapped_column(SmallInteger())
    mechanism_comment: Mapped[str | None] = mapped_column(String(2000))
    selectivity_comment: Mapped[str | None] = mapped_column(String(1000))
    binding_site_comment: Mapped[str | None] = mapped_column(String(1000))
    variant_id: Mapped[int | None] = mapped_column(BigInteger())


class DrugWarning(Base):
    """ORM class for drug_warning."""

    __tablename__ = "drug_warning"
    __table_args__ = (
        PrimaryKeyConstraint("warning_id", name="sys_c00167957"),
        ForeignKeyConstraint(
            ["record_id"],
            ["compound_records.record_id"],
            name="fk_warning_record_id",
            ondelete="CASCADE",
        ),
    )
    warning_id: Mapped[int] = mapped_column(BigInteger())
    record_id: Mapped[int | None] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    warning_type: Mapped[str | None] = mapped_column(String(20))
    warning_class: Mapped[str | None] = mapped_column(String(100))
    warning_description: Mapped[str | None] = mapped_column(String(4000))
    warning_country: Mapped[str | None] = mapped_column(String(1000))
    warning_year: Mapped[int | None]
    efo_term: Mapped[str | None] = mapped_column(String(200))
    efo_id: Mapped[str | None] = mapped_column(String(20))
    efo_id_for_warning_class: Mapped[str | None] = mapped_column(String(20))


class Formulations(Base):
    """ORM class for formulations."""

    __tablename__ = "formulations"
    __table_args__ = (
        PrimaryKeyConstraint("formulation_id", name="pk_formulations_id"),
        ForeignKeyConstraint(
            ["molregno"],
            ["molecule_dictionary.molregno"],
            name="fk_formulations_molregno",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["product_id"],
            ["products.product_id"],
            name="fk_formulations_productid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["record_id"],
            ["compound_records.record_id"],
            name="fk_formulations_recid",
            ondelete="CASCADE",
        ),
        UniqueConstraint("product_id", "record_id", name="uk_formulations"),
    )
    product_id: Mapped[str] = mapped_column(String(30))
    ingredient: Mapped[str | None] = mapped_column(String(200))
    strength: Mapped[str | None] = mapped_column(String(300))
    record_id: Mapped[int] = mapped_column(BigInteger())
    molregno: Mapped[int | None] = mapped_column(BigInteger())
    formulation_id: Mapped[int] = mapped_column(BigInteger())


class Metabolism(Base):
    """ORM class for metabolism."""

    __tablename__ = "metabolism"
    __table_args__ = (
        PrimaryKeyConstraint("met_id", name="pk_rec_met_id"),
        ForeignKeyConstraint(
            ["drug_record_id"],
            ["compound_records.record_id"],
            name="fk_recmet_drug_recid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["metabolite_record_id"],
            ["compound_records.record_id"],
            name="fk_recmet_met_recid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["substrate_record_id"],
            ["compound_records.record_id"],
            name="fk_recmet_sub_recid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["enzyme_tid"], ["target_dictionary.tid"], name="fk_recmet_tid", ondelete="CASCADE"
        ),
        UniqueConstraint(
            "drug_record_id",
            "substrate_record_id",
            "metabolite_record_id",
            "pathway_id",
            "enzyme_name",
            "enzyme_tid",
            "tax_id",
            name="uk_recmet",
        ),
    )
    met_id: Mapped[int] = mapped_column(BigInteger())
    drug_record_id: Mapped[int | None] = mapped_column(BigInteger())
    substrate_record_id: Mapped[int | None] = mapped_column(BigInteger())
    metabolite_record_id: Mapped[int | None] = mapped_column(BigInteger())
    pathway_id: Mapped[int | None] = mapped_column(BigInteger())
    pathway_key: Mapped[str | None] = mapped_column(String(50))
    enzyme_name: Mapped[str | None] = mapped_column(String(200))
    enzyme_tid: Mapped[int | None] = mapped_column(BigInteger())
    met_conversion: Mapped[str | None] = mapped_column(String(200))
    organism: Mapped[str | None] = mapped_column(String(100))
    tax_id: Mapped[int | None] = mapped_column(BigInteger())
    met_comment: Mapped[str | None] = mapped_column(String(1000))


class SiteComponents(Base):
    """ORM class for site_components."""

    __tablename__ = "site_components"
    __table_args__ = (
        PrimaryKeyConstraint("sitecomp_id", name="pk_sitecomp_id"),
        ForeignKeyConstraint(
            ["component_id"],
            ["component_sequences.component_id"],
            name="fk_sitecomp_compid",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["domain_id"], ["domains.domain_id"], name="fk_sitecomp_domainid", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["site_id"], ["binding_sites.site_id"], name="fk_sitecomp_siteid", ondelete="CASCADE"
        ),
        UniqueConstraint("site_id", "component_id", "domain_id", name="uk_sitecomp"),
    )
    sitecomp_id: Mapped[int] = mapped_column(BigInteger())
    site_id: Mapped[int] = mapped_column(BigInteger())
    component_id: Mapped[int | None] = mapped_column(BigInteger())
    domain_id: Mapped[int | None] = mapped_column(BigInteger())
    site_residues: Mapped[str | None] = mapped_column(String(2000))


class ActivityProperties(Base):
    """ORM class for activity_properties."""

    __tablename__ = "activity_properties"
    __table_args__ = (
        PrimaryKeyConstraint("ap_id", name="pk_actprop_ap_id"),
        ForeignKeyConstraint(
            ["activity_id"],
            ["activities.activity_id"],
            name="fk_activity_property",
            ondelete="CASCADE",
        ),
        UniqueConstraint("activity_id", "type", name="uk_actprop_id_type"),
        Index("idx_actprop_type", "standard_type"),
        Index("idx_act_prop_text", "standard_text_value"),
        Index("idx_actprop_val", "standard_value"),
        Index("idx_actprop_resflag", "result_flag"),
        Index("idx_actprop_relation", "standard_relation"),
        Index("idx_actprop_units", "standard_units"),
    )
    ap_id: Mapped[int] = mapped_column(BigInteger())
    activity_id: Mapped[int] = mapped_column(BigInteger())
    type: Mapped[str] = mapped_column(String(250))
    relation: Mapped[str | None] = mapped_column(String(50))
    value: Mapped[float | None]
    units: Mapped[str | None] = mapped_column(String(100))
    text_value: Mapped[str | None] = mapped_column(String(2000))
    standard_type: Mapped[str | None] = mapped_column(String(250))
    standard_relation: Mapped[str | None] = mapped_column(String(50))
    standard_value: Mapped[float | None]
    standard_units: Mapped[str | None] = mapped_column(String(100))
    standard_text_value: Mapped[str | None] = mapped_column(String(2000))
    comments: Mapped[str | None] = mapped_column(String(2000))
    result_flag: Mapped[int] = mapped_column(SmallInteger())


class ActivitySuppMap(Base):
    """ORM class for activity_supp_map."""

    __tablename__ = "activity_supp_map"
    __table_args__ = (
        PrimaryKeyConstraint("actsm_id", name="pk_actsm_id"),
        ForeignKeyConstraint(
            ["smid"], ["activity_smid.smid"], name="fk_act_smid", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["activity_id"], ["activities.activity_id"], name="fk_supp_act", ondelete="CASCADE"
        ),
        Index("pk_actsmid", "actsm_id", unique=True),
    )
    actsm_id: Mapped[int] = mapped_column(BigInteger())
    activity_id: Mapped[int] = mapped_column(BigInteger())
    smid: Mapped[int] = mapped_column(BigInteger())


class IndicationRefs(Base):
    """ORM class for indication_refs."""

    __tablename__ = "indication_refs"
    __table_args__ = (
        PrimaryKeyConstraint("indref_id", name="indication_refs_pk"),
        ForeignKeyConstraint(
            ["drugind_id"],
            ["drug_indication.drugind_id"],
            name="indref_drugind_fk",
            ondelete="CASCADE",
        ),
        UniqueConstraint("drugind_id", "ref_type", "ref_id", name="indref_uk"),
    )
    indref_id: Mapped[int] = mapped_column(BigInteger())
    drugind_id: Mapped[int] = mapped_column(BigInteger())
    ref_type: Mapped[str] = mapped_column(String(50))
    ref_id: Mapped[str] = mapped_column(String(4000))
    ref_url: Mapped[str] = mapped_column(String(4000))


class LigandEff(Base):
    """ORM class for ligand_eff."""

    __tablename__ = "ligand_eff"
    __table_args__ = (
        PrimaryKeyConstraint("activity_id", name="pk_ligeff_actid"),
        ForeignKeyConstraint(
            ["activity_id"], ["activities.activity_id"], name="fk_ligeff_actid", ondelete="CASCADE"
        ),
        CheckConstraint("bei > 0", name="ck_ligeff_bei"),
        CheckConstraint("sei > 0", name="ck_ligeff_sei"),
    )
    activity_id: Mapped[int] = mapped_column(BigInteger())
    bei: Mapped[float | None] = mapped_column(Numeric(9, 2))
    sei: Mapped[float | None] = mapped_column(Numeric(9, 2))
    le: Mapped[float | None] = mapped_column(Numeric(9, 2))
    lle: Mapped[float | None] = mapped_column(Numeric(9, 2))


class MechanismRefs(Base):
    """ORM class for mechanism_refs."""

    __tablename__ = "mechanism_refs"
    __table_args__ = (
        PrimaryKeyConstraint("mecref_id", name="pk_mechanism_refs"),
        ForeignKeyConstraint(
            ["mec_id"],
            ["drug_mechanism.mec_id"],
            name="fk_mechanism_refs_mecid",
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "ref_type IN ('PMDA', 'ISBN', 'IUPHAR', 'DOI', 'EMA', 'PubMed', 'USPO', 'DailyMed', 'FDA', 'Expert', 'Other', 'InterPro', 'Wikipedia', 'UniProt', 'KEGG', 'PMC', 'ClinicalTrials', 'PubChem', 'Patent', 'BNF', 'HMA')",
            name="ck_mechanism_ref_type",
        ),
        UniqueConstraint("mec_id", "ref_type", "ref_id", name="uk_mechanism_refs"),
        Index("mechanism_refs_pk", "mecref_id", unique=True),
        Index("mechanism_refs_uk", "mec_id", "ref_type", "ref_id", unique=True),
    )
    mecref_id: Mapped[int] = mapped_column(BigInteger())
    mec_id: Mapped[int] = mapped_column(BigInteger())
    ref_type: Mapped[str] = mapped_column(String(50))
    ref_id: Mapped[str | None] = mapped_column(String(200))
    ref_url: Mapped[str | None] = mapped_column(String(400))


class MetabolismRefs(Base):
    """ORM class for metabolism_refs."""

    __tablename__ = "metabolism_refs"
    __table_args__ = (
        PrimaryKeyConstraint("metref_id", name="pk_metref_id"),
        ForeignKeyConstraint(
            ["met_id"], ["metabolism.met_id"], name="fk_metref_met_id", ondelete="CASCADE"
        ),
        UniqueConstraint("met_id", "ref_type", "ref_id", name="uk_metref"),
    )
    metref_id: Mapped[int] = mapped_column(BigInteger())
    met_id: Mapped[int] = mapped_column(BigInteger())
    ref_type: Mapped[str] = mapped_column(String(50))
    ref_id: Mapped[str | None] = mapped_column(String(200))
    ref_url: Mapped[str | None] = mapped_column(String(400))


class PredictedBindingDomains(Base):
    """ORM class for predicted_binding_domains."""

    __tablename__ = "predicted_binding_domains"
    __table_args__ = (
        PrimaryKeyConstraint("predbind_id", name="pk_predbinddom_predbind_id"),
        ForeignKeyConstraint(
            ["activity_id"],
            ["activities.activity_id"],
            name="fk_predbinddom_act_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["site_id"],
            ["binding_sites.site_id"],
            name="fk_predbinddom_site_id",
            ondelete="CASCADE",
        ),
        CheckConstraint("confidence IN ('high', 'medium', 'low')", name="ck_predbinddom_conf"),
        CheckConstraint(
            "prediction_method IN ('Manual', 'Single domain', 'Multi domain')",
            name="ck_predbinddom_method",
        ),
    )
    predbind_id: Mapped[int] = mapped_column(BigInteger())
    activity_id: Mapped[int | None] = mapped_column(BigInteger())
    site_id: Mapped[int | None] = mapped_column(BigInteger())
    prediction_method: Mapped[str | None] = mapped_column(String(50))
    confidence: Mapped[str | None] = mapped_column(String(10))


class WarningRefs(Base):
    """ORM class for warning_refs."""

    __tablename__ = "warning_refs"
    __table_args__ = (
        PrimaryKeyConstraint("warnref_id", name="sys_c00167958"),
        ForeignKeyConstraint(
            ["warning_id"],
            ["drug_warning.warning_id"],
            name="fk_warnref_warn_id",
            ondelete="CASCADE",
        ),
    )
    warnref_id: Mapped[int] = mapped_column(BigInteger())
    warning_id: Mapped[int | None] = mapped_column(BigInteger())
    ref_type: Mapped[str | None] = mapped_column(String(50))
    ref_id: Mapped[str | None] = mapped_column(String(4000))
    ref_url: Mapped[str | None] = mapped_column(String(4000))
