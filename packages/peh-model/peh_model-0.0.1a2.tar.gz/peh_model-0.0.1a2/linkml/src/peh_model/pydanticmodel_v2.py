from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "0.0.1a2"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = None

class ValidationStatus(str, Enum):
    unvalidated = "unvalidated"
    in_progress = "in_progress"
    validated = "validated"
    deprecated = "deprecated"


class ValidationCommand(str, Enum):
    is_equal_to = "is_equal_to"
    is_equal_to_or_both_missing = "is_equal_to_or_both_missing"
    is_greater_than_or_equal_to = "is_greater_than_or_equal_to"
    is_greater_than = "is_greater_than"
    is_less_than_or_equal_to = "is_less_than_or_equal_to"
    is_less_than = "is_less_than"
    is_not_equal_to = "is_not_equal_to"
    is_not_equal_to_and_not_both_missing = "is_not_equal_to_and_not_both_missing"
    is_unique = "is_unique"
    is_duplicated = "is_duplicated"
    is_in = "is_in"
    is_null = "is_null"
    is_not_null = "is_not_null"
    conjunction = "conjunction"
    disjunction = "disjunction"


class ValidationErrorLevel(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    fatal = "fatal"


class DataLayoutElementStyle(str, Enum):
    standard = "standard"
    main_title = "main_title"
    section_title = "section_title"
    sub_title = "sub_title"
    comment = "comment"
    warning = "warning"
    alert = "alert"


class IndicatorType(str, Enum):
    effectmarker = "effectmarker"
    exposuremarker = "exposuremarker"
    geomarker = "geomarker"
    observation = "observation"


class BioChemEntityLinkType(str, Enum):
    exact_match = "exact_match"
    close_match = "close_match"
    broader = "broader"
    part_of = "part_of"
    group_contains = "group_contains"
    has_parent_compound = "has_parent_compound"
    branched_version_of = "branched_version_of"


class ResearchPopulationType(str, Enum):
    general_population = "general_population"
    person = "person"
    newborn = "newborn"
    adolescent = "adolescent"
    mother = "mother"
    parent = "parent"
    pregnant_person = "pregnant_person"
    household = "household"


class ObservableEntityType(str, Enum):
    project = "project"
    organisation = "organisation"
    study = "study"
    environment = "environment"
    location = "location"
    persongroup = "persongroup"
    person = "person"
    samplegroup = "samplegroup"
    sample = "sample"
    dataset = "dataset"
    collection_process = "collection_process"
    lab_analysis_process = "lab_analysis_process"
    model_execution_process = "model_execution_process"
    data_process = "data_process"


class ObservationType(str, Enum):
    sampling = "sampling"
    questionnaire = "questionnaire"
    geospatial = "geospatial"
    metadata = "metadata"


class ObservationResultType(str, Enum):
    measurement = "measurement"
    control = "control"
    calculation = "calculation"
    simulation = "simulation"


class DataLayoutSectionType(str, Enum):
    data_form = "data_form"
    data_table = "data_table"
    property_table = "property_table"


class DataLayoutElementType(str, Enum):
    text = "text"
    spacer = "spacer"
    data_field = "data_field"


class ObjectiveType(str, Enum):
    research_objective = "research_objective"
    project_result = "project_result"
    publication = "publication"


class LinkType(str, Enum):
    is_about = "is_about"
    is_same_as = "is_same_as"
    is_part_of = "is_part_of"
    is_located_at = "is_located_at"


class ContactRole(str, Enum):
    administrative = "administrative"
    data = "data"
    general = "general"
    lead = "lead"
    legal = "legal"
    technical = "technical"


class ProjectRole(str, Enum):
    member = "member"
    partner = "partner"
    funding_partner = "funding_partner"
    principal_investigator = "principal_investigator"
    data_governance = "data_governance"
    data_controller = "data_controller"
    data_processor = "data_processor"
    data_user = "data_user"
    lab = "lab"


class StudyRole(str, Enum):
    funding_partner = "funding_partner"
    principal_investigator = "principal_investigator"
    data_controller = "data_controller"
    data_processor = "data_processor"
    data_user = "data_user"
    lab = "lab"


class DataRole(str, Enum):
    main_stakeholder = "main_stakeholder"
    supplying_data_controller = "supplying_data_controller"
    receiving_data_controller = "receiving_data_controller"
    external_data_controller = "external_data_controller"


class QudtUnit(str, Enum):
    PERCENT = "PERCENT"
    KiloGM_PER_M3 = "KiloGM-PER-M3"
    DAY = "DAY"
    NanoGM = "NanoGM"
    GM = "GM"
    MilliGM_PER_KiloGM = "MilliGM-PER-KiloGM"
    MilliMOL_PER_MOL = "MilliMOL-PER-MOL"
    MicroGM_PER_MilliL = "MicroGM-PER-MilliL"
    MO = "MO"
    UNITLESS = "UNITLESS"
    NanoMOL_PER_L = "NanoMOL-PER-L"
    MIN = "MIN"
    NanoGM_PER_M3 = "NanoGM-PER-M3"
    GM_PER_DeciL = "GM-PER-DeciL"
    GM_PER_L = "GM-PER-L"
    MilliL = "MilliL"
    HR = "HR"
    PicoGM = "PicoGM"
    FemtoMOL_PER_KiloGM = "FemtoMOL-PER-KiloGM"
    NUM = "NUM"
    NanoGM_PER_MilliL = "NanoGM-PER-MilliL"
    MicroGM_PER_KiloGM = "MicroGM-PER-KiloGM"
    KiloGM = "KiloGM"
    NanoGM_PER_L = "NanoGM-PER-L"
    MicroMOL_PER_L = "MicroMOL-PER-L"
    CentiM = "CentiM"
    MicroGM_PER_GM = "MicroGM-PER-GM"
    WK = "WK"
    NanoGM_PER_DeciL = "NanoGM-PER-DeciL"
    MilliGM_PER_L = "MilliGM-PER-L"
    PicoGM_PER_GM = "PicoGM-PER-GM"
    L = "L"
    NanoGM_PER_M2 = "NanoGM-PER-M2"
    IU_PER_L = "IU-PER-L"
    NUM_PER_MilliL = "NUM-PER-MilliL"
    GM_PER_MOL = "GM-PER-MOL"
    PER_WK = "PER-WK"
    PicoGM_PER_MilliL = "PicoGM-PER-MilliL"
    YR = "YR"
    PER_DAY = "PER-DAY"
    PicoGM_PER_MilliGM = "PicoGM-PER-MilliGM"
    MicroGM_PER_L = "MicroGM-PER-L"
    KiloGM_PER_M2 = "KiloGM-PER-M2"
    MilliGM_PER_DeciL = "MilliGM-PER-DeciL"


class QudtQuantityKind(str, Enum):
    AmountOfSubstanceConcentration = "AmountOfSubstanceConcentration"
    AmountOfSubstancePerMass = "AmountOfSubstancePerMass"
    Count = "Count"
    Dimensionless = "Dimensionless"
    DimensionlessRatio = "DimensionlessRatio"
    Time = "Time"
    Frequency = "Frequency"
    Length = "Length"
    Mass = "Mass"
    MassPerArea = "MassPerArea"
    MassConcentration = "MassConcentration"
    MassRatio = "MassRatio"
    MolarMass = "MolarMass"
    MolarRatio = "MolarRatio"
    NumberDensity = "NumberDensity"
    Volume = "Volume"



class EntityList(ConfiguredBaseModel):
    """
    A generic top level object for collecting named entities under one root entity
    """
    matrices: Optional[list[Matrix]] = Field(default=None)
    metadata_fields: Optional[list[ObservablePropertyMetadataField]] = Field(default=None)
    biochementities: Optional[list[BioChemEntity]] = Field(default=None)
    groupings: Optional[list[Grouping]] = Field(default=None)
    indicators: Optional[list[Indicator]] = Field(default=None)
    units: Optional[list[Unit]] = Field(default=None)
    observable_properties: Optional[list[ObservableProperty]] = Field(default=None)
    stakeholders: Optional[list[Stakeholder]] = Field(default=None)
    projects: Optional[list[Project]] = Field(default=None)
    studies: Optional[list[Study]] = Field(default=None)
    study_entities: Optional[list[StudyEntity]] = Field(default=None)
    physical_entities: Optional[list[PhysicalEntity]] = Field(default=None)
    observation_groups: Optional[list[ObservationGroup]] = Field(default=None)
    observations: Optional[list[Observation]] = Field(default=None)
    observation_results: Optional[list[ObservationResult]] = Field(default=None)
    observed_values: Optional[list[ObservedValue]] = Field(default=None)
    layouts: Optional[list[DataLayout]] = Field(default=None)
    data_requests: Optional[list[DataRequest]] = Field(default=None)


class NamedThing(ConfiguredBaseModel):
    """
    An abstract model for any of the identifiable entities
    """
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class HasValidationStatus(ConfiguredBaseModel):
    """
    The capacity of including both a current validation status and a history of validation records
    """
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)


class ValidationHistoryRecord(ConfiguredBaseModel):
    """
    A list of events representing a historical record on the entity validation status
    """
    validation_datetime: Optional[datetime ] = Field(default=None)
    validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_actor: Optional[str] = Field(default=None)
    validation_institute: Optional[str] = Field(default=None)
    validation_remark: Optional[str] = Field(default=None)


class HasAliases(ConfiguredBaseModel):
    """
    The capacity of including one or more alternative naming terms (without qualifying the usage context)
    """
    aliases: Optional[list[str]] = Field(default=None)


class HasContextAliases(ConfiguredBaseModel):
    """
    The capacity of including a list of terms being used in known scopes or contexts
    """
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class ContextAlias(ConfiguredBaseModel):
    """
    An alternative term as it is used in a known scope or context (e.g. a community, project or study) for any of the entities and its properties
    """
    property_name: Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)


class HasTranslations(ConfiguredBaseModel):
    """
    The capacity of including a list of translated terms for one or more entity properties and languages
    """
    translations: Optional[list[Translation]] = Field(default=None)


class Grouping(HasTranslations, HasContextAliases, NamedThing):
    """
    A generic grouping entity that allows categorising entities in a hierarchical structure
    """
    sort_order: Optional[Decimal] = Field(default=None)
    abstract: Optional[bool] = Field(default=None)
    parent_grouping_id_list: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Translation(ConfiguredBaseModel):
    """
    A translation for any of the entity properties, defining the property, the language and the translated term
    """
    property_name: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    translated_value: Optional[str] = Field(default=None)


class Unit(HasTranslations, HasContextAliases, HasValidationStatus, NamedThing):
    """
    A unit of measurement, a quantity chosen as a standard in terms of which other quantities may be expressed
    """
    same_unit_as: Optional[QudtUnit] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemEntity(HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    grouping_id_list: Optional[list[str]] = Field(default=None)
    molweight_grampermol: Optional[Decimal] = Field(default=None)
    biochemidentifiers: Optional[list[BioChemIdentifier]] = Field(default=None)
    biochementity_links: Optional[list[BioChemEntityLink]] = Field(default=None)
    aliases: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemIdentifier(HasValidationStatus):
    """
    An identifier by which a biochemical entity is known in a schema (the BioChemIdentifierSchema) used by a certain community or system
    """
    identifier_schema: Optional[str] = Field(default=None)
    identifier_code: Optional[str] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)


class BioChemIdentifierSchema(NamedThing):
    """
    A well-defined schema used by a certain community or system, listing biochemical entities with individual identifiers 
    """
    web_uri: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Matrix(HasTranslations, HasContextAliases, NamedThing):
    """
    The physical medium or biological substrate from which a biomarker, or other analyte is quantified in observational studies
    """
    sort_order: Optional[Decimal] = Field(default=None)
    aggregation_target: Optional[bool] = Field(default=None)
    parent_matrix: Optional[str] = Field(default=None)
    secondary_parent_matrix_id_list: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Indicator(HasContextAliases, NamedThing):
    """
    Any measurable or observable variable that can describe data or context in the Personal Exposure and Health domain
    """
    indicator_type: Optional[IndicatorType] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    property: Optional[str] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    grouping_id_list: Optional[list[str]] = Field(default=None)
    relevant_observable_entity_types: Optional[list[ObservableEntityType]] = Field(default=None)
    biochementity_links: Optional[list[BioChemEntityLink]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemEntityLink(ConfiguredBaseModel):
    """
    A relational property that allows creating qualified links to biochemical entities
    """
    biochementity_linktype: Optional[BioChemEntityLinkType] = Field(default=None)
    biochementity: Optional[str] = Field(default=None)


class PhysicalEntity(NamedThing):
    """
    A digital placeholder for a physical entity as it exists in the real world, 
    """
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class PhysicalEntityLink(ConfiguredBaseModel):
    """
    A relational property that allows creating qualified links to physical entities
    """
    linktype: Optional[LinkType] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)


class Sample(PhysicalEntity):
    """
    A portion of a measurement matrix collected from a subject or environment for the purpose of lab analysis
    """
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    sampled_in_project: Optional[str] = Field(default=None)
    physical_label: Optional[str] = Field(default=None)
    collection_date: Optional[date] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Person(PhysicalEntity):
    """
    A human subject or stakeholder in Personal Exposure and Health research
    """
    recruited_in_project: Optional[str] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Geolocation(PhysicalEntity):
    """
    A geographic location relevant to the Personal Exposure and Health projects or studies
    """
    location: Optional[str] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Environment(PhysicalEntity):
    """
    An environment relevant to the research, typically related to the exposure of a person
    """
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class HomeEnvironment(Environment):
    """
    A home environment relevant to the research, typically related to the at-home exposure of a person
    """
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class WorkEnvironment(Environment):
    """
    A work environment relevant to the research, typically related to the at-work or commute exposure of a person
    """
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservableProperty(HasTranslations, HasContextAliases, NamedThing):
    """
    A fully defined variable that allows registering an observation about any of the entities relevant to Personal Exposure and Health research
    """
    value_type: Optional[str] = Field(default=None)
    categorical: Optional[bool] = Field(default=None)
    multivalued: Optional[bool] = Field(default=None)
    value_options: Optional[list[ObservablePropertyValueOption]] = Field(default=None)
    value_metadata: Optional[list[ObservablePropertyMetadataElement]] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    default_unit: Optional[str] = Field(default=None)
    default_unit_label: Optional[str] = Field(default=None)
    default_required: Optional[bool] = Field(default=None)
    default_zeroallowed: Optional[bool] = Field(default=None)
    default_significantdecimals: Optional[int] = Field(default=None)
    default_immutable: Optional[bool] = Field(default=None)
    grouping_id_list: Optional[list[str]] = Field(default=None)
    default_observation_result_type: Optional[ObservationResultType] = Field(default=None)
    relevant_observable_entity_types: Optional[list[ObservableEntityType]] = Field(default=None)
    relevant_observation_types: Optional[list[ObservationType]] = Field(default=None)
    indicator: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    calculation_designs: Optional[list[CalculationDesign]] = Field(default=None)
    validation_designs: Optional[list[ValidationDesign]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservablePropertyValueOption(HasContextAliases):
    """
    Potential selection choices for Observable Properties that are categorical variables
    """
    key: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class ObservablePropertyMetadataElement(ConfiguredBaseModel):
    """
    Key-value element that adds contextual metadata to an Observable Property instance
    """
    field: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)


class ObservablePropertyMetadataField(NamedThing):
    """
    Predefined contextual qualifier for Observable Property metadata
    """
    value_type: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class CalculationDesign(ConfiguredBaseModel):
    """
    Definition of a calculation method for deriving an observational value from other variables and/or contexts
    """
    calculation_name: Optional[str] = Field(default=None)
    calculation_implementation_as_json: Optional[str] = Field(default=None)
    calculation_implementation: Optional[CalculationImplementation] = Field(default=None)
    conditional: Optional[str] = Field(default=None)


class CalculationImplementation(ConfiguredBaseModel):
    """
    Reference and parameters mapping to the implementation that can perform the intended calculation
    """
    function_name: Optional[str] = Field(default=None)
    function_args: Optional[list[CalculationArgument]] = Field(default=None)
    function_kwargs: Optional[list[CalculationKeywordArgument]] = Field(default=None)
    function_results: Optional[list[CalculationResult]] = Field(default=None)


class CalculationArgument(ConfiguredBaseModel):
    """
    The definition of a positional argument used in the calculation, including the information needed to pick it from the project or study data structure
    """
    source_path: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    process_state: Optional[str] = Field(default=None)
    imputation_state: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class CalculationKeywordArgument(ConfiguredBaseModel):
    """
    The definition of a named argument used in the calculation, including the information needed to pick it from the project or study data structure
    """
    mapping_name: Optional[str] = Field(default=None)
    source_path: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    process_state: Optional[str] = Field(default=None)
    imputation_state: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class CalculationResult(ConfiguredBaseModel):
    """
    The definition for the output the calculation, optionally including mapping information
    """
    mapping_name: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    round_decimals: Optional[int] = Field(default=None)
    scale_factor: Optional[Decimal] = Field(default=None)
    destination_path: Optional[str] = Field(default=None)


class ValidationDesign(ConfiguredBaseModel):
    """
    Definition of a validation rule for automatically imposing business logic constraints
    """
    validation_name: Optional[str] = Field(default=None)
    validation_expression: Optional[ValidationExpression] = Field(default=None)
    validation_error_level: Optional[ValidationErrorLevel] = Field(default=None)
    validation_error_message_template: Optional[str] = Field(default=None)
    conditional: Optional[str] = Field(default=None)


class ValidationExpression(ConfiguredBaseModel):
    """
    A logical expression, allowing for combining arguments into more complex validation rules
    """
    validation_subject_source_paths: Optional[list[str]] = Field(default=None)
    validation_condition_expression: Optional[ValidationExpression] = Field(default=None)
    validation_command: Optional[ValidationCommand] = Field(default=None)
    validation_arg_values: Optional[list[str]] = Field(default=None)
    validation_arg_source_paths: Optional[list[str]] = Field(default=None)
    validation_arg_expressions: Optional[list[ValidationExpression]] = Field(default=None)


class Contact(HasContextAliases):
    """
    A stakeholder having a contact role in the research process
    """
    name: Optional[str] = Field(default=None)
    orcid: Optional[str] = Field(default=None)
    contact_roles: Optional[list[ContactRole]] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    contact_phone: Optional[str] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class Stakeholder(HasTranslations, NamedThing):
    """
    Any organisation involved in the research process
    """
    rorid: Optional[str] = Field(default=None)
    geographic_scope: Optional[str] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProjectStakeholder(HasTranslations):
    """
    An organisation collaborating in a Personal Exposure and Health research project
    """
    stakeholder: Optional[str] = Field(default=None)
    project_roles: Optional[list[ProjectRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)


class StudyEntity(NamedThing):
    """
    Any entity carrying data or context relevant to a Personal Exposure and Health research project or study
    """
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Project(StudyEntity, HasTranslations, HasContextAliases):
    """
    A collaborative effort in the Personal Exposure and Health research domain
    """
    default_language: Optional[str] = Field(default=None)
    project_stakeholders: Optional[list[ProjectStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    study_id_list: Optional[list[str]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyEntityLink(ConfiguredBaseModel):
    """
    A relational property that allows creating qualified links to study entities
    """
    linktype: Optional[LinkType] = Field(default=None)
    study_entity: Optional[str] = Field(default=None)


class Study(StudyEntity, HasTranslations, HasContextAliases):
    """
    A structured, goal-directed observational investigation designed to collect and analyze data on human subjects and their environments
    """
    default_language: Optional[str] = Field(default=None)
    study_stakeholders: Optional[list[StudyStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_group_id_list: Optional[list[str]] = Field(default=None)
    study_entity_id_list: Optional[list[str]] = Field(default=None)
    project_id_list: Optional[list[str]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyStakeholder(ConfiguredBaseModel):
    """
    An organisation collaborating in a Personal Exposure and Health research study
    """
    stakeholder: Optional[str] = Field(default=None)
    study_roles: Optional[list[StudyRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)


class ObservationGroup(StudyEntity):
    """
    A grouped collection of observations, intended and/or executed, as part of a Personal Exposure and Health research study
    """
    sort_order: Optional[Decimal] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyPopulation(StudyEntity):
    """
    A group of study entities that is itself also a study entity that observations can be recorded for
    """
    research_population_type: Optional[ResearchPopulationType] = Field(default=None)
    member_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class SampleCollection(StudyEntity):
    """
    A collection of samples that is itself also a study entity that observations can be recorded for
    """
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    sample_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudySubject(StudyEntity):
    """
    A study entity that is a main subject for the study
    """
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudySubjectGroup(StudyEntity):
    """
    A group of study subjects that is itself also a study entity that observations can be recorded for
    """
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Observation(NamedThing):
    """
    The registration of the intent to perform a set of observations as well as the resulting observed values
    """
    observation_type: Optional[ObservationType] = Field(default=None)
    observation_design: Optional[ObservationDesign] = Field(default=None)
    observation_result_id_list: Optional[list[str]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservationDesign(ConfiguredBaseModel):
    """
    The registration of the intent to perform a number of observations
    """
    observable_entity_property_sets: Optional[list[ObservableEntityPropertySet]] = Field(default=None)


class ObservableEntityPropertySet(ConfiguredBaseModel):
    """
    The list of properties being observed and the study entities they will be observed for (or, alternatively, the entity type all observed entities belong to)
    """
    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observable_entity_type: Optional[ObservableEntityType] = Field(default=None)
    observable_entity_id_list: Optional[list[str]] = Field(default=None)
    identifying_observable_property_id_list: Optional[list[str]] = Field(default=None)
    required_observable_property_id_list: Optional[list[str]] = Field(default=None)
    optional_observable_property_id_list: Optional[list[str]] = Field(default=None)


class ObservationResult(NamedThing):
    """
    The result of an observational effort in Personal Exposure and Health research
    """
    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observation_start_date: Optional[date] = Field(default=None)
    observation_end_date: Optional[date] = Field(default=None)
    observed_values: Optional[list[ObservedValue]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservedValue(ConfiguredBaseModel):
    """
    A single observational result value registering a specific property for a specific entity at a specific moment
    """
    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    default_unit: Optional[str] = Field(default=None)
    raw_value: Optional[str] = Field(default=None)
    raw_unit: Optional[str] = Field(default=None)
    imputed_value: Optional[str] = Field(default=None)
    imputed_unit: Optional[str] = Field(default=None)
    normalised_value: Optional[str] = Field(default=None)
    normalised_unit: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    value_as_string: Optional[str] = Field(default=None)
    quality_data: Optional[list[QualityData]] = Field(default=None)
    provenance_data: Optional[list[ProvenanceData]] = Field(default=None)


class QualityData(ConfiguredBaseModel):
    """
    Quality metadata, adding context to an Observed Value
    """
    quality_context_key: Optional[str] = Field(default=None)
    quality_value: Optional[str] = Field(default=None)


class ProvenanceData(ConfiguredBaseModel):
    """
    Provenance metadata, adding context to an Observed Value
    """
    provenance_context_key: Optional[str] = Field(default=None)
    provenance_value: Optional[str] = Field(default=None)


class DataLayout(NamedThing):
    """
    Layout, allowing the definition of templating sections for combining layout and data elements
    """
    sections: Optional[list[DataLayoutSection]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataLayoutSection(NamedThing):
    """
    Definition for an individual layout or data section, as part of a full layout
    """
    section_type: Optional[DataLayoutSectionType] = Field(default=None)
    observable_entity_types: Optional[list[ObservableEntityType]] = Field(default=None)
    observable_entity_grouping_id_list: Optional[list[str]] = Field(default=None)
    elements: Optional[list[DataLayoutElement]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataLayoutElement(ConfiguredBaseModel):
    """
    Definition for an individual layout or data element, as part of a layout section
    """
    label: Optional[str] = Field(default=None)
    element_type: Optional[DataLayoutElementType] = Field(default=None)
    element_style: Optional[DataLayoutElementStyle] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    is_observable_entity_key: Optional[bool] = Field(default=None)
    is_foreign_key: Optional[bool] = Field(default=None)


class DataRequest(NamedThing):
    """
    Registration of a request for data by a data user
    """
    contacts: Optional[list[Contact]] = Field(default=None)
    request_properties: Optional[str] = Field(default=None)
    data_stakeholders: Optional[list[str]] = Field(default=None)
    research_objectives: Optional[list[str]] = Field(default=None)
    processing_actions: Optional[list[str]] = Field(default=None)
    processing_steps: Optional[list[str]] = Field(default=None)
    remark_on_content: Optional[str] = Field(default=None)
    remark_on_methodology: Optional[str] = Field(default=None)
    observed_entity_properties: Optional[list[ObservedEntityProperty]] = Field(default=None)
    observable_entity_property_sets: Optional[list[ObservableEntityPropertySet]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservedEntityProperty(ConfiguredBaseModel):
    """
    Conceptual definition of the observation of a certain property for a certain entity in a study
    """
    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)


class DataStakeholder(NamedThing):
    """
    An organisation participating in a data process in Personal Exposure and Health research
    """
    stakeholder: Optional[str] = Field(default=None)
    data_roles: Optional[list[DataRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)
    processing_description: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ResearchObjective(NamedThing):
    """
    A research objective communicated in the request and used to evaluate if the request is valid and appropriate
    """
    objective_type: Optional[ObjectiveType] = Field(default=None)
    authors: Optional[list[str]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProcessingAction(NamedThing):
    """
    One action in the data request and processing flow
    """
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProcessingStep(NamedThing):
    """
    One step in the data request and processing flow
    """
    start_date: Optional[date] = Field(default=None)
    delivery_date: Optional[date] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataExtract(ConfiguredBaseModel):
    """
    A set of Observed Values, combined into a data extract
    """
    observed_values: Optional[list[ObservedValue]] = Field(default=None)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
EntityList.model_rebuild()
NamedThing.model_rebuild()
HasValidationStatus.model_rebuild()
ValidationHistoryRecord.model_rebuild()
HasAliases.model_rebuild()
HasContextAliases.model_rebuild()
ContextAlias.model_rebuild()
HasTranslations.model_rebuild()
Grouping.model_rebuild()
Translation.model_rebuild()
Unit.model_rebuild()
BioChemEntity.model_rebuild()
BioChemIdentifier.model_rebuild()
BioChemIdentifierSchema.model_rebuild()
Matrix.model_rebuild()
Indicator.model_rebuild()
BioChemEntityLink.model_rebuild()
PhysicalEntity.model_rebuild()
PhysicalEntityLink.model_rebuild()
Sample.model_rebuild()
Person.model_rebuild()
Geolocation.model_rebuild()
Environment.model_rebuild()
HomeEnvironment.model_rebuild()
WorkEnvironment.model_rebuild()
ObservableProperty.model_rebuild()
ObservablePropertyValueOption.model_rebuild()
ObservablePropertyMetadataElement.model_rebuild()
ObservablePropertyMetadataField.model_rebuild()
CalculationDesign.model_rebuild()
CalculationImplementation.model_rebuild()
CalculationArgument.model_rebuild()
CalculationKeywordArgument.model_rebuild()
CalculationResult.model_rebuild()
ValidationDesign.model_rebuild()
ValidationExpression.model_rebuild()
Contact.model_rebuild()
Stakeholder.model_rebuild()
ProjectStakeholder.model_rebuild()
StudyEntity.model_rebuild()
Project.model_rebuild()
StudyEntityLink.model_rebuild()
Study.model_rebuild()
StudyStakeholder.model_rebuild()
ObservationGroup.model_rebuild()
StudyPopulation.model_rebuild()
SampleCollection.model_rebuild()
StudySubject.model_rebuild()
StudySubjectGroup.model_rebuild()
Observation.model_rebuild()
ObservationDesign.model_rebuild()
ObservableEntityPropertySet.model_rebuild()
ObservationResult.model_rebuild()
ObservedValue.model_rebuild()
QualityData.model_rebuild()
ProvenanceData.model_rebuild()
DataLayout.model_rebuild()
DataLayoutSection.model_rebuild()
DataLayoutElement.model_rebuild()
DataRequest.model_rebuild()
ObservedEntityProperty.model_rebuild()
DataStakeholder.model_rebuild()
ResearchObjective.model_rebuild()
ProcessingAction.model_rebuild()
ProcessingStep.model_rebuild()
DataExtract.model_rebuild()

