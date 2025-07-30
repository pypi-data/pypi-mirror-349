# Auto generated from peh.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-05-20T06:42:40
# Schema: PEH-Model
#
# id: https://w3id.org/peh/peh-model
# description: Entity and relation ontology and datamodel for Personal Exposure and Health data
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Decimal, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, Decimal, XSDDate, XSDDateTime

metamodel_version = "1.7.0"
version = "0.0.1a2"

# Namespaces
IOP = CurieNamespace('iop', 'https://w3id.org/iadopt/ont/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PEH = CurieNamespace('peh', 'https://w3id.org/peh/')
PEHTERMS = CurieNamespace('pehterms', 'https://w3id.org/peh/terms/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUDT = CurieNamespace('qudt', 'http://qudt.org/2.1/schema/qudt')
QUDTQK = CurieNamespace('qudtqk', 'http://qudt.org/2.1/vocab/quantitykind')
QUDTUNIT = CurieNamespace('qudtunit', 'https://qudt.org/vocab/unit/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
DEFAULT_ = PEHTERMS


# Types

# Class references
class NamedThingId(extended_str):
    pass


class GroupingId(NamedThingId):
    pass


class UnitId(NamedThingId):
    pass


class BioChemEntityId(NamedThingId):
    pass


class BioChemIdentifierSchemaId(NamedThingId):
    pass


class MatrixId(NamedThingId):
    pass


class IndicatorId(NamedThingId):
    pass


class PhysicalEntityId(NamedThingId):
    pass


class SampleId(PhysicalEntityId):
    pass


class PersonId(PhysicalEntityId):
    pass


class GeolocationId(PhysicalEntityId):
    pass


class EnvironmentId(PhysicalEntityId):
    pass


class HomeEnvironmentId(EnvironmentId):
    pass


class WorkEnvironmentId(EnvironmentId):
    pass


class ObservablePropertyId(NamedThingId):
    pass


class ObservablePropertyMetadataFieldId(NamedThingId):
    pass


class StakeholderId(NamedThingId):
    pass


class StudyEntityId(NamedThingId):
    pass


class ProjectId(StudyEntityId):
    pass


class StudyId(StudyEntityId):
    pass


class ObservationGroupId(StudyEntityId):
    pass


class StudyPopulationId(StudyEntityId):
    pass


class SampleCollectionId(StudyEntityId):
    pass


class StudySubjectId(StudyEntityId):
    pass


class StudySubjectGroupId(StudyEntityId):
    pass


class ObservationId(NamedThingId):
    pass


class ObservationResultId(NamedThingId):
    pass


class DataLayoutId(NamedThingId):
    pass


class DataLayoutSectionId(NamedThingId):
    pass


class DataRequestId(NamedThingId):
    pass


class DataStakeholderId(NamedThingId):
    pass


class ResearchObjectiveId(NamedThingId):
    pass


class ProcessingActionId(NamedThingId):
    pass


class ProcessingStepId(NamedThingId):
    pass


@dataclass(repr=False)
class EntityList(YAMLRoot):
    """
    A generic top level object for collecting named entities under one root entity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["EntityList"]
    class_class_curie: ClassVar[str] = "pehterms:EntityList"
    class_name: ClassVar[str] = "EntityList"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.EntityList

    matrices: Optional[Union[dict[Union[str, MatrixId], Union[dict, "Matrix"]], list[Union[dict, "Matrix"]]]] = empty_dict()
    metadata_fields: Optional[Union[dict[Union[str, ObservablePropertyMetadataFieldId], Union[dict, "ObservablePropertyMetadataField"]], list[Union[dict, "ObservablePropertyMetadataField"]]]] = empty_dict()
    biochementities: Optional[Union[dict[Union[str, BioChemEntityId], Union[dict, "BioChemEntity"]], list[Union[dict, "BioChemEntity"]]]] = empty_dict()
    groupings: Optional[Union[dict[Union[str, GroupingId], Union[dict, "Grouping"]], list[Union[dict, "Grouping"]]]] = empty_dict()
    indicators: Optional[Union[dict[Union[str, IndicatorId], Union[dict, "Indicator"]], list[Union[dict, "Indicator"]]]] = empty_dict()
    units: Optional[Union[dict[Union[str, UnitId], Union[dict, "Unit"]], list[Union[dict, "Unit"]]]] = empty_dict()
    observable_properties: Optional[Union[dict[Union[str, ObservablePropertyId], Union[dict, "ObservableProperty"]], list[Union[dict, "ObservableProperty"]]]] = empty_dict()
    stakeholders: Optional[Union[dict[Union[str, StakeholderId], Union[dict, "Stakeholder"]], list[Union[dict, "Stakeholder"]]]] = empty_dict()
    projects: Optional[Union[dict[Union[str, ProjectId], Union[dict, "Project"]], list[Union[dict, "Project"]]]] = empty_dict()
    studies: Optional[Union[dict[Union[str, StudyId], Union[dict, "Study"]], list[Union[dict, "Study"]]]] = empty_dict()
    study_entities: Optional[Union[dict[Union[str, StudyEntityId], Union[dict, "StudyEntity"]], list[Union[dict, "StudyEntity"]]]] = empty_dict()
    physical_entities: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]]] = empty_dict()
    observation_groups: Optional[Union[dict[Union[str, ObservationGroupId], Union[dict, "ObservationGroup"]], list[Union[dict, "ObservationGroup"]]]] = empty_dict()
    observations: Optional[Union[dict[Union[str, ObservationId], Union[dict, "Observation"]], list[Union[dict, "Observation"]]]] = empty_dict()
    observation_results: Optional[Union[dict[Union[str, ObservationResultId], Union[dict, "ObservationResult"]], list[Union[dict, "ObservationResult"]]]] = empty_dict()
    observed_values: Optional[Union[Union[dict, "ObservedValue"], list[Union[dict, "ObservedValue"]]]] = empty_list()
    layouts: Optional[Union[dict[Union[str, DataLayoutId], Union[dict, "DataLayout"]], list[Union[dict, "DataLayout"]]]] = empty_dict()
    data_requests: Optional[Union[dict[Union[str, DataRequestId], Union[dict, "DataRequest"]], list[Union[dict, "DataRequest"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="matrices", slot_type=Matrix, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="metadata_fields", slot_type=ObservablePropertyMetadataField, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="biochementities", slot_type=BioChemEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="groupings", slot_type=Grouping, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="indicators", slot_type=Indicator, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="units", slot_type=Unit, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="observable_properties", slot_type=ObservableProperty, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="stakeholders", slot_type=Stakeholder, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="projects", slot_type=Project, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="studies", slot_type=Study, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="study_entities", slot_type=StudyEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="physical_entities", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="observation_groups", slot_type=ObservationGroup, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="observations", slot_type=Observation, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="observation_results", slot_type=ObservationResult, key_name="id", keyed=True)

        if not isinstance(self.observed_values, list):
            self.observed_values = [self.observed_values] if self.observed_values is not None else []
        self.observed_values = [v if isinstance(v, ObservedValue) else ObservedValue(**as_dict(v)) for v in self.observed_values]

        self._normalize_inlined_as_list(slot_name="layouts", slot_type=DataLayout, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="data_requests", slot_type=DataRequest, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NamedThing(YAMLRoot):
    """
    An abstract model for any of the identifiable entities
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["NamedThing"]
    class_class_curie: ClassVar[str] = "pehterms:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.NamedThing

    id: Union[str, NamedThingId] = None
    unique_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    remark: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.unique_name is not None and not isinstance(self.unique_name, str):
            self.unique_name = str(self.unique_name)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.remark is not None and not isinstance(self.remark, str):
            self.remark = str(self.remark)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Grouping(NamedThing):
    """
    A generic grouping entity that allows categorising entities in a hierarchical structure
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Grouping"]
    class_class_curie: ClassVar[str] = "pehterms:Grouping"
    class_name: ClassVar[str] = "Grouping"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Grouping

    id: Union[str, GroupingId] = None
    sort_order: Optional[Decimal] = None
    abstract: Optional[Union[bool, Bool]] = None
    parent_grouping_id_list: Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, "ContextAlias"], list[Union[dict, "ContextAlias"]]]] = empty_list()
    translations: Optional[Union[Union[dict, "Translation"], list[Union[dict, "Translation"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GroupingId):
            self.id = GroupingId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.abstract is not None and not isinstance(self.abstract, Bool):
            self.abstract = Bool(self.abstract)

        if not isinstance(self.parent_grouping_id_list, list):
            self.parent_grouping_id_list = [self.parent_grouping_id_list] if self.parent_grouping_id_list is not None else []
        self.parent_grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.parent_grouping_id_list]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HasValidationStatus(YAMLRoot):
    """
    The capacity of including both a current validation status and a history of validation records
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["HasValidationStatus"]
    class_class_curie: ClassVar[str] = "pehterms:HasValidationStatus"
    class_name: ClassVar[str] = "HasValidationStatus"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.HasValidationStatus

    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, "ValidationHistoryRecord"], list[Union[dict, "ValidationHistoryRecord"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationHistoryRecord(YAMLRoot):
    """
    A list of events representing a historical record on the entity validation status
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ValidationHistoryRecord"]
    class_class_curie: ClassVar[str] = "pehterms:ValidationHistoryRecord"
    class_name: ClassVar[str] = "ValidationHistoryRecord"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ValidationHistoryRecord

    validation_datetime: Optional[Union[str, XSDDateTime]] = None
    validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_actor: Optional[str] = None
    validation_institute: Optional[str] = None
    validation_remark: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.validation_datetime is not None and not isinstance(self.validation_datetime, XSDDateTime):
            self.validation_datetime = XSDDateTime(self.validation_datetime)

        if self.validation_status is not None and not isinstance(self.validation_status, ValidationStatus):
            self.validation_status = ValidationStatus(self.validation_status)

        if self.validation_actor is not None and not isinstance(self.validation_actor, str):
            self.validation_actor = str(self.validation_actor)

        if self.validation_institute is not None and not isinstance(self.validation_institute, str):
            self.validation_institute = str(self.validation_institute)

        if self.validation_remark is not None and not isinstance(self.validation_remark, str):
            self.validation_remark = str(self.validation_remark)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HasAliases(YAMLRoot):
    """
    The capacity of including one or more alternative naming terms (without qualifying the usage context)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["HasAliases"]
    class_class_curie: ClassVar[str] = "pehterms:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.HasAliases

    aliases: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HasContextAliases(YAMLRoot):
    """
    The capacity of including a list of terms being used in known scopes or contexts
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["HasContextAliases"]
    class_class_curie: ClassVar[str] = "pehterms:HasContextAliases"
    class_name: ClassVar[str] = "HasContextAliases"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.HasContextAliases

    context_aliases: Optional[Union[Union[dict, "ContextAlias"], list[Union[dict, "ContextAlias"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContextAlias(YAMLRoot):
    """
    An alternative term as it is used in a known scope or context (e.g. a community, project or study) for any of the
    entities and its properties
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ContextAlias"]
    class_class_curie: ClassVar[str] = "pehterms:ContextAlias"
    class_name: ClassVar[str] = "ContextAlias"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ContextAlias

    property_name: Optional[str] = None
    context: Optional[Union[str, NamedThingId]] = None
    alias: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.property_name is not None and not isinstance(self.property_name, str):
            self.property_name = str(self.property_name)

        if self.context is not None and not isinstance(self.context, NamedThingId):
            self.context = NamedThingId(self.context)

        if self.alias is not None and not isinstance(self.alias, str):
            self.alias = str(self.alias)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HasTranslations(YAMLRoot):
    """
    The capacity of including a list of translated terms for one or more entity properties and languages
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["HasTranslations"]
    class_class_curie: ClassVar[str] = "pehterms:HasTranslations"
    class_name: ClassVar[str] = "HasTranslations"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.HasTranslations

    translations: Optional[Union[Union[dict, "Translation"], list[Union[dict, "Translation"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Translation(YAMLRoot):
    """
    A translation for any of the entity properties, defining the property, the language and the translated term
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Translation"]
    class_class_curie: ClassVar[str] = "pehterms:Translation"
    class_name: ClassVar[str] = "Translation"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Translation

    property_name: Optional[str] = None
    language: Optional[str] = None
    translated_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.property_name is not None and not isinstance(self.property_name, str):
            self.property_name = str(self.property_name)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.translated_value is not None and not isinstance(self.translated_value, str):
            self.translated_value = str(self.translated_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Unit(NamedThing):
    """
    A unit of measurement, a quantity chosen as a standard in terms of which other quantities may be expressed
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Unit"]
    class_class_curie: ClassVar[str] = "pehterms:Unit"
    class_name: ClassVar[str] = "Unit"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Unit

    id: Union[str, UnitId] = None
    same_unit_as: Optional[Union[str, "QudtUnit"]] = None
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()
    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, ValidationHistoryRecord], list[Union[dict, ValidationHistoryRecord]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UnitId):
            self.id = UnitId(self.id)

        if self.same_unit_as is not None and not isinstance(self.same_unit_as, QudtUnit):
            self.same_unit_as = QudtUnit(self.same_unit_as)

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioChemEntity(NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["BioChemEntity"]
    class_class_curie: ClassVar[str] = "schema:BioChemEntity"
    class_name: ClassVar[str] = "BioChemEntity"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.BioChemEntity

    id: Union[str, BioChemEntityId] = None
    grouping_id_list: Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]] = empty_list()
    molweight_grampermol: Optional[Decimal] = None
    biochemidentifiers: Optional[Union[Union[dict, "BioChemIdentifier"], list[Union[dict, "BioChemIdentifier"]]]] = empty_list()
    biochementity_links: Optional[Union[Union[dict, "BioChemEntityLink"], list[Union[dict, "BioChemEntityLink"]]]] = empty_list()
    aliases: Optional[Union[str, list[str]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()
    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, ValidationHistoryRecord], list[Union[dict, ValidationHistoryRecord]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioChemEntityId):
            self.id = BioChemEntityId(self.id)

        if not isinstance(self.grouping_id_list, list):
            self.grouping_id_list = [self.grouping_id_list] if self.grouping_id_list is not None else []
        self.grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.grouping_id_list]

        if self.molweight_grampermol is not None and not isinstance(self.molweight_grampermol, Decimal):
            self.molweight_grampermol = Decimal(self.molweight_grampermol)

        if not isinstance(self.biochemidentifiers, list):
            self.biochemidentifiers = [self.biochemidentifiers] if self.biochemidentifiers is not None else []
        self.biochemidentifiers = [v if isinstance(v, BioChemIdentifier) else BioChemIdentifier(**as_dict(v)) for v in self.biochemidentifiers]

        if not isinstance(self.biochementity_links, list):
            self.biochementity_links = [self.biochementity_links] if self.biochementity_links is not None else []
        self.biochementity_links = [v if isinstance(v, BioChemEntityLink) else BioChemEntityLink(**as_dict(v)) for v in self.biochementity_links]

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioChemIdentifier(YAMLRoot):
    """
    An identifier by which a biochemical entity is known in a schema (the BioChemIdentifierSchema) used by a certain
    community or system
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["BioChemIdentifier"]
    class_class_curie: ClassVar[str] = "pehterms:BioChemIdentifier"
    class_name: ClassVar[str] = "BioChemIdentifier"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.BioChemIdentifier

    identifier_schema: Optional[Union[str, BioChemIdentifierSchemaId]] = None
    identifier_code: Optional[str] = None
    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, ValidationHistoryRecord], list[Union[dict, ValidationHistoryRecord]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.identifier_schema is not None and not isinstance(self.identifier_schema, BioChemIdentifierSchemaId):
            self.identifier_schema = BioChemIdentifierSchemaId(self.identifier_schema)

        if self.identifier_code is not None and not isinstance(self.identifier_code, str):
            self.identifier_code = str(self.identifier_code)

        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioChemIdentifierSchema(NamedThing):
    """
    A well-defined schema used by a certain community or system, listing biochemical entities with individual
    identifiers
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["BioChemIdentifierSchema"]
    class_class_curie: ClassVar[str] = "pehterms:BioChemIdentifierSchema"
    class_name: ClassVar[str] = "BioChemIdentifierSchema"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.BioChemIdentifierSchema

    id: Union[str, BioChemIdentifierSchemaId] = None
    web_uri: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioChemIdentifierSchemaId):
            self.id = BioChemIdentifierSchemaId(self.id)

        if self.web_uri is not None and not isinstance(self.web_uri, str):
            self.web_uri = str(self.web_uri)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Matrix(NamedThing):
    """
    The physical medium or biological substrate from which a biomarker, or other analyte is quantified in
    observational studies
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Matrix"]
    class_class_curie: ClassVar[str] = "pehterms:Matrix"
    class_name: ClassVar[str] = "Matrix"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Matrix

    id: Union[str, MatrixId] = None
    sort_order: Optional[Decimal] = None
    aggregation_target: Optional[Union[bool, Bool]] = None
    parent_matrix: Optional[Union[str, MatrixId]] = None
    secondary_parent_matrix_id_list: Optional[Union[Union[str, MatrixId], list[Union[str, MatrixId]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MatrixId):
            self.id = MatrixId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.aggregation_target is not None and not isinstance(self.aggregation_target, Bool):
            self.aggregation_target = Bool(self.aggregation_target)

        if self.parent_matrix is not None and not isinstance(self.parent_matrix, MatrixId):
            self.parent_matrix = MatrixId(self.parent_matrix)

        if not isinstance(self.secondary_parent_matrix_id_list, list):
            self.secondary_parent_matrix_id_list = [self.secondary_parent_matrix_id_list] if self.secondary_parent_matrix_id_list is not None else []
        self.secondary_parent_matrix_id_list = [v if isinstance(v, MatrixId) else MatrixId(v) for v in self.secondary_parent_matrix_id_list]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Indicator(NamedThing):
    """
    Any measurable or observable variable that can describe data or context in the Personal Exposure and Health domain
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Indicator"]
    class_class_curie: ClassVar[str] = "pehterms:Indicator"
    class_name: ClassVar[str] = "Indicator"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Indicator

    id: Union[str, IndicatorId] = None
    indicator_type: Optional[Union[str, "IndicatorType"]] = None
    varname: Optional[str] = None
    property: Optional[str] = None
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, list[str]]] = empty_list()
    grouping_id_list: Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]] = empty_list()
    relevant_observable_entity_types: Optional[Union[Union[str, "ObservableEntityType"], list[Union[str, "ObservableEntityType"]]]] = empty_list()
    biochementity_links: Optional[Union[Union[dict, "BioChemEntityLink"], list[Union[dict, "BioChemEntityLink"]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndicatorId):
            self.id = IndicatorId(self.id)

        if self.indicator_type is not None and not isinstance(self.indicator_type, IndicatorType):
            self.indicator_type = IndicatorType(self.indicator_type)

        if self.varname is not None and not isinstance(self.varname, str):
            self.varname = str(self.varname)

        if self.property is not None and not isinstance(self.property, str):
            self.property = str(self.property)

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        if not isinstance(self.grouping_id_list, list):
            self.grouping_id_list = [self.grouping_id_list] if self.grouping_id_list is not None else []
        self.grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.grouping_id_list]

        if not isinstance(self.relevant_observable_entity_types, list):
            self.relevant_observable_entity_types = [self.relevant_observable_entity_types] if self.relevant_observable_entity_types is not None else []
        self.relevant_observable_entity_types = [v if isinstance(v, ObservableEntityType) else ObservableEntityType(v) for v in self.relevant_observable_entity_types]

        if not isinstance(self.biochementity_links, list):
            self.biochementity_links = [self.biochementity_links] if self.biochementity_links is not None else []
        self.biochementity_links = [v if isinstance(v, BioChemEntityLink) else BioChemEntityLink(**as_dict(v)) for v in self.biochementity_links]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioChemEntityLink(YAMLRoot):
    """
    A relational property that allows creating qualified links to biochemical entities
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["BioChemEntityLink"]
    class_class_curie: ClassVar[str] = "pehterms:BioChemEntityLink"
    class_name: ClassVar[str] = "BioChemEntityLink"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.BioChemEntityLink

    biochementity_linktype: Optional[Union[str, "BioChemEntityLinkType"]] = None
    biochementity: Optional[Union[str, BioChemEntityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.biochementity_linktype is not None and not isinstance(self.biochementity_linktype, BioChemEntityLinkType):
            self.biochementity_linktype = BioChemEntityLinkType(self.biochementity_linktype)

        if self.biochementity is not None and not isinstance(self.biochementity, BioChemEntityId):
            self.biochementity = BioChemEntityId(self.biochementity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhysicalEntity(NamedThing):
    """
    A digital placeholder for a physical entity as it exists in the real world,
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["PhysicalEntity"]
    class_class_curie: ClassVar[str] = "pehterms:PhysicalEntity"
    class_name: ClassVar[str] = "PhysicalEntity"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.PhysicalEntity

    id: Union[str, PhysicalEntityId] = None
    physical_entity_links: Optional[Union[Union[dict, "PhysicalEntityLink"], list[Union[dict, "PhysicalEntityLink"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.physical_entity_links, list):
            self.physical_entity_links = [self.physical_entity_links] if self.physical_entity_links is not None else []
        self.physical_entity_links = [v if isinstance(v, PhysicalEntityLink) else PhysicalEntityLink(**as_dict(v)) for v in self.physical_entity_links]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhysicalEntityLink(YAMLRoot):
    """
    A relational property that allows creating qualified links to physical entities
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["PhysicalEntityLink"]
    class_class_curie: ClassVar[str] = "pehterms:PhysicalEntityLink"
    class_name: ClassVar[str] = "PhysicalEntityLink"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.PhysicalEntityLink

    linktype: Optional[Union[str, "LinkType"]] = None
    physical_entity: Optional[Union[str, PhysicalEntityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.linktype is not None and not isinstance(self.linktype, LinkType):
            self.linktype = LinkType(self.linktype)

        if self.physical_entity is not None and not isinstance(self.physical_entity, PhysicalEntityId):
            self.physical_entity = PhysicalEntityId(self.physical_entity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sample(PhysicalEntity):
    """
    A portion of a measurement matrix collected from a subject or environment for the purpose of lab analysis
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Sample"]
    class_class_curie: ClassVar[str] = "pehterms:Sample"
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Sample

    id: Union[str, SampleId] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, list[str]]] = empty_list()
    sampled_in_project: Optional[Union[str, ProjectId]] = None
    physical_label: Optional[str] = None
    collection_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SampleId):
            self.id = SampleId(self.id)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        if self.sampled_in_project is not None and not isinstance(self.sampled_in_project, ProjectId):
            self.sampled_in_project = ProjectId(self.sampled_in_project)

        if self.physical_label is not None and not isinstance(self.physical_label, str):
            self.physical_label = str(self.physical_label)

        if self.collection_date is not None and not isinstance(self.collection_date, XSDDate):
            self.collection_date = XSDDate(self.collection_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(PhysicalEntity):
    """
    A human subject or stakeholder in Personal Exposure and Health research
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Person"]
    class_class_curie: ClassVar[str] = "pehterms:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Person

    id: Union[str, PersonId] = None
    recruited_in_project: Optional[Union[str, ProjectId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.recruited_in_project is not None and not isinstance(self.recruited_in_project, ProjectId):
            self.recruited_in_project = ProjectId(self.recruited_in_project)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Geolocation(PhysicalEntity):
    """
    A geographic location relevant to the Personal Exposure and Health projects or studies
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Geolocation"]
    class_class_curie: ClassVar[str] = "pehterms:Geolocation"
    class_name: ClassVar[str] = "Geolocation"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Geolocation

    id: Union[str, GeolocationId] = None
    location: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeolocationId):
            self.id = GeolocationId(self.id)

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Environment(PhysicalEntity):
    """
    An environment relevant to the research, typically related to the exposure of a person
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Environment"]
    class_class_curie: ClassVar[str] = "pehterms:Environment"
    class_name: ClassVar[str] = "Environment"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Environment

    id: Union[str, EnvironmentId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentId):
            self.id = EnvironmentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HomeEnvironment(Environment):
    """
    A home environment relevant to the research, typically related to the at-home exposure of a person
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["HomeEnvironment"]
    class_class_curie: ClassVar[str] = "pehterms:HomeEnvironment"
    class_name: ClassVar[str] = "HomeEnvironment"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.HomeEnvironment

    id: Union[str, HomeEnvironmentId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HomeEnvironmentId):
            self.id = HomeEnvironmentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WorkEnvironment(Environment):
    """
    A work environment relevant to the research, typically related to the at-work or commute exposure of a person
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["WorkEnvironment"]
    class_class_curie: ClassVar[str] = "pehterms:WorkEnvironment"
    class_name: ClassVar[str] = "WorkEnvironment"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.WorkEnvironment

    id: Union[str, WorkEnvironmentId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, WorkEnvironmentId):
            self.id = WorkEnvironmentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservableProperty(NamedThing):
    """
    A fully defined variable that allows registering an observation about any of the entities relevant to Personal
    Exposure and Health research
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservableProperty"]
    class_class_curie: ClassVar[str] = "pehterms:ObservableProperty"
    class_name: ClassVar[str] = "ObservableProperty"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservableProperty

    id: Union[str, ObservablePropertyId] = None
    value_type: Optional[str] = None
    categorical: Optional[Union[bool, Bool]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    value_options: Optional[Union[Union[dict, "ObservablePropertyValueOption"], list[Union[dict, "ObservablePropertyValueOption"]]]] = empty_list()
    value_metadata: Optional[Union[Union[dict, "ObservablePropertyMetadataElement"], list[Union[dict, "ObservablePropertyMetadataElement"]]]] = empty_list()
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    default_unit: Optional[str] = None
    default_unit_label: Optional[str] = None
    default_required: Optional[Union[bool, Bool]] = None
    default_zeroallowed: Optional[Union[bool, Bool]] = None
    default_significantdecimals: Optional[int] = None
    default_immutable: Optional[Union[bool, Bool]] = None
    grouping_id_list: Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]] = empty_list()
    default_observation_result_type: Optional[Union[str, "ObservationResultType"]] = None
    relevant_observable_entity_types: Optional[Union[Union[str, "ObservableEntityType"], list[Union[str, "ObservableEntityType"]]]] = empty_list()
    relevant_observation_types: Optional[Union[Union[str, "ObservationType"], list[Union[str, "ObservationType"]]]] = empty_list()
    indicator: Optional[Union[str, IndicatorId]] = None
    varname: Optional[str] = None
    calculation_designs: Optional[Union[Union[dict, "CalculationDesign"], list[Union[dict, "CalculationDesign"]]]] = empty_list()
    validation_designs: Optional[Union[Union[dict, "ValidationDesign"], list[Union[dict, "ValidationDesign"]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObservablePropertyId):
            self.id = ObservablePropertyId(self.id)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        if self.categorical is not None and not isinstance(self.categorical, Bool):
            self.categorical = Bool(self.categorical)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if not isinstance(self.value_options, list):
            self.value_options = [self.value_options] if self.value_options is not None else []
        self.value_options = [v if isinstance(v, ObservablePropertyValueOption) else ObservablePropertyValueOption(**as_dict(v)) for v in self.value_options]

        if not isinstance(self.value_metadata, list):
            self.value_metadata = [self.value_metadata] if self.value_metadata is not None else []
        self.value_metadata = [v if isinstance(v, ObservablePropertyMetadataElement) else ObservablePropertyMetadataElement(**as_dict(v)) for v in self.value_metadata]

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if self.default_unit is not None and not isinstance(self.default_unit, str):
            self.default_unit = str(self.default_unit)

        if self.default_unit_label is not None and not isinstance(self.default_unit_label, str):
            self.default_unit_label = str(self.default_unit_label)

        if self.default_required is not None and not isinstance(self.default_required, Bool):
            self.default_required = Bool(self.default_required)

        if self.default_zeroallowed is not None and not isinstance(self.default_zeroallowed, Bool):
            self.default_zeroallowed = Bool(self.default_zeroallowed)

        if self.default_significantdecimals is not None and not isinstance(self.default_significantdecimals, int):
            self.default_significantdecimals = int(self.default_significantdecimals)

        if self.default_immutable is not None and not isinstance(self.default_immutable, Bool):
            self.default_immutable = Bool(self.default_immutable)

        if not isinstance(self.grouping_id_list, list):
            self.grouping_id_list = [self.grouping_id_list] if self.grouping_id_list is not None else []
        self.grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.grouping_id_list]

        if self.default_observation_result_type is not None and not isinstance(self.default_observation_result_type, ObservationResultType):
            self.default_observation_result_type = ObservationResultType(self.default_observation_result_type)

        if not isinstance(self.relevant_observable_entity_types, list):
            self.relevant_observable_entity_types = [self.relevant_observable_entity_types] if self.relevant_observable_entity_types is not None else []
        self.relevant_observable_entity_types = [v if isinstance(v, ObservableEntityType) else ObservableEntityType(v) for v in self.relevant_observable_entity_types]

        if not isinstance(self.relevant_observation_types, list):
            self.relevant_observation_types = [self.relevant_observation_types] if self.relevant_observation_types is not None else []
        self.relevant_observation_types = [v if isinstance(v, ObservationType) else ObservationType(v) for v in self.relevant_observation_types]

        if self.indicator is not None and not isinstance(self.indicator, IndicatorId):
            self.indicator = IndicatorId(self.indicator)

        if self.varname is not None and not isinstance(self.varname, str):
            self.varname = str(self.varname)

        if not isinstance(self.calculation_designs, list):
            self.calculation_designs = [self.calculation_designs] if self.calculation_designs is not None else []
        self.calculation_designs = [v if isinstance(v, CalculationDesign) else CalculationDesign(**as_dict(v)) for v in self.calculation_designs]

        if not isinstance(self.validation_designs, list):
            self.validation_designs = [self.validation_designs] if self.validation_designs is not None else []
        self.validation_designs = [v if isinstance(v, ValidationDesign) else ValidationDesign(**as_dict(v)) for v in self.validation_designs]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservablePropertyValueOption(YAMLRoot):
    """
    Potential selection choices for Observable Properties that are categorical variables
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservablePropertyValueOption"]
    class_class_curie: ClassVar[str] = "pehterms:ObservablePropertyValueOption"
    class_name: ClassVar[str] = "ObservablePropertyValueOption"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservablePropertyValueOption

    key: Optional[str] = None
    value: Optional[str] = None
    label: Optional[str] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.key is not None and not isinstance(self.key, str):
            self.key = str(self.key)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservablePropertyMetadataElement(YAMLRoot):
    """
    Key-value element that adds contextual metadata to an Observable Property instance
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservablePropertyMetadataElement"]
    class_class_curie: ClassVar[str] = "pehterms:ObservablePropertyMetadataElement"
    class_name: ClassVar[str] = "ObservablePropertyMetadataElement"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservablePropertyMetadataElement

    field: Optional[Union[str, ObservablePropertyMetadataFieldId]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.field is not None and not isinstance(self.field, ObservablePropertyMetadataFieldId):
            self.field = ObservablePropertyMetadataFieldId(self.field)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservablePropertyMetadataField(NamedThing):
    """
    Predefined contextual qualifier for Observable Property metadata
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservablePropertyMetadataField"]
    class_class_curie: ClassVar[str] = "pehterms:ObservablePropertyMetadataField"
    class_name: ClassVar[str] = "ObservablePropertyMetadataField"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservablePropertyMetadataField

    id: Union[str, ObservablePropertyMetadataFieldId] = None
    value_type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObservablePropertyMetadataFieldId):
            self.id = ObservablePropertyMetadataFieldId(self.id)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CalculationDesign(YAMLRoot):
    """
    Definition of a calculation method for deriving an observational value from other variables and/or contexts
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["CalculationDesign"]
    class_class_curie: ClassVar[str] = "pehterms:CalculationDesign"
    class_name: ClassVar[str] = "CalculationDesign"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.CalculationDesign

    calculation_name: Optional[str] = None
    calculation_implementation_as_json: Optional[str] = None
    calculation_implementation: Optional[Union[dict, "CalculationImplementation"]] = None
    conditional: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.calculation_name is not None and not isinstance(self.calculation_name, str):
            self.calculation_name = str(self.calculation_name)

        if self.calculation_implementation_as_json is not None and not isinstance(self.calculation_implementation_as_json, str):
            self.calculation_implementation_as_json = str(self.calculation_implementation_as_json)

        if self.calculation_implementation is not None and not isinstance(self.calculation_implementation, CalculationImplementation):
            self.calculation_implementation = CalculationImplementation(**as_dict(self.calculation_implementation))

        if self.conditional is not None and not isinstance(self.conditional, str):
            self.conditional = str(self.conditional)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CalculationImplementation(YAMLRoot):
    """
    Reference and parameters mapping to the implementation that can perform the intended calculation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["CalculationImplementation"]
    class_class_curie: ClassVar[str] = "pehterms:CalculationImplementation"
    class_name: ClassVar[str] = "CalculationImplementation"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.CalculationImplementation

    function_name: Optional[str] = None
    function_args: Optional[Union[Union[dict, "CalculationArgument"], list[Union[dict, "CalculationArgument"]]]] = empty_list()
    function_kwargs: Optional[Union[Union[dict, "CalculationKeywordArgument"], list[Union[dict, "CalculationKeywordArgument"]]]] = empty_list()
    function_results: Optional[Union[Union[dict, "CalculationResult"], list[Union[dict, "CalculationResult"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.function_name is not None and not isinstance(self.function_name, str):
            self.function_name = str(self.function_name)

        if not isinstance(self.function_args, list):
            self.function_args = [self.function_args] if self.function_args is not None else []
        self.function_args = [v if isinstance(v, CalculationArgument) else CalculationArgument(**as_dict(v)) for v in self.function_args]

        if not isinstance(self.function_kwargs, list):
            self.function_kwargs = [self.function_kwargs] if self.function_kwargs is not None else []
        self.function_kwargs = [v if isinstance(v, CalculationKeywordArgument) else CalculationKeywordArgument(**as_dict(v)) for v in self.function_kwargs]

        if not isinstance(self.function_results, list):
            self.function_results = [self.function_results] if self.function_results is not None else []
        self.function_results = [v if isinstance(v, CalculationResult) else CalculationResult(**as_dict(v)) for v in self.function_results]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CalculationArgument(YAMLRoot):
    """
    The definition of a positional argument used in the calculation, including the information needed to pick it from
    the project or study data structure
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["CalculationArgument"]
    class_class_curie: ClassVar[str] = "pehterms:CalculationArgument"
    class_name: ClassVar[str] = "CalculationArgument"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.CalculationArgument

    source_path: Optional[str] = None
    varname: Optional[str] = None
    process_state: Optional[str] = None
    imputation_state: Optional[str] = None
    value_type: Optional[str] = None
    unit: Optional[Union[str, UnitId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.source_path is not None and not isinstance(self.source_path, str):
            self.source_path = str(self.source_path)

        if self.varname is not None and not isinstance(self.varname, str):
            self.varname = str(self.varname)

        if self.process_state is not None and not isinstance(self.process_state, str):
            self.process_state = str(self.process_state)

        if self.imputation_state is not None and not isinstance(self.imputation_state, str):
            self.imputation_state = str(self.imputation_state)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CalculationKeywordArgument(YAMLRoot):
    """
    The definition of a named argument used in the calculation, including the information needed to pick it from the
    project or study data structure
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["CalculationKeywordArgument"]
    class_class_curie: ClassVar[str] = "pehterms:CalculationKeywordArgument"
    class_name: ClassVar[str] = "CalculationKeywordArgument"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.CalculationKeywordArgument

    mapping_name: Optional[str] = None
    source_path: Optional[str] = None
    varname: Optional[str] = None
    process_state: Optional[str] = None
    imputation_state: Optional[str] = None
    value_type: Optional[str] = None
    unit: Optional[Union[str, UnitId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mapping_name is not None and not isinstance(self.mapping_name, str):
            self.mapping_name = str(self.mapping_name)

        if self.source_path is not None and not isinstance(self.source_path, str):
            self.source_path = str(self.source_path)

        if self.varname is not None and not isinstance(self.varname, str):
            self.varname = str(self.varname)

        if self.process_state is not None and not isinstance(self.process_state, str):
            self.process_state = str(self.process_state)

        if self.imputation_state is not None and not isinstance(self.imputation_state, str):
            self.imputation_state = str(self.imputation_state)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CalculationResult(YAMLRoot):
    """
    The definition for the output the calculation, optionally including mapping information
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["CalculationResult"]
    class_class_curie: ClassVar[str] = "pehterms:CalculationResult"
    class_name: ClassVar[str] = "CalculationResult"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.CalculationResult

    mapping_name: Optional[str] = None
    value_type: Optional[str] = None
    unit: Optional[Union[str, UnitId]] = None
    round_decimals: Optional[int] = None
    scale_factor: Optional[Decimal] = None
    destination_path: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mapping_name is not None and not isinstance(self.mapping_name, str):
            self.mapping_name = str(self.mapping_name)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        if self.round_decimals is not None and not isinstance(self.round_decimals, int):
            self.round_decimals = int(self.round_decimals)

        if self.scale_factor is not None and not isinstance(self.scale_factor, Decimal):
            self.scale_factor = Decimal(self.scale_factor)

        if self.destination_path is not None and not isinstance(self.destination_path, str):
            self.destination_path = str(self.destination_path)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationDesign(YAMLRoot):
    """
    Definition of a validation rule for automatically imposing business logic constraints
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ValidationDesign"]
    class_class_curie: ClassVar[str] = "pehterms:ValidationDesign"
    class_name: ClassVar[str] = "ValidationDesign"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ValidationDesign

    validation_name: Optional[str] = None
    validation_expression: Optional[Union[dict, "ValidationExpression"]] = None
    validation_error_level: Optional[Union[str, "ValidationErrorLevel"]] = None
    validation_error_message_template: Optional[str] = None
    conditional: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.validation_name is not None and not isinstance(self.validation_name, str):
            self.validation_name = str(self.validation_name)

        if self.validation_expression is not None and not isinstance(self.validation_expression, ValidationExpression):
            self.validation_expression = ValidationExpression(**as_dict(self.validation_expression))

        if self.validation_error_level is not None and not isinstance(self.validation_error_level, ValidationErrorLevel):
            self.validation_error_level = ValidationErrorLevel(self.validation_error_level)

        if self.validation_error_message_template is not None and not isinstance(self.validation_error_message_template, str):
            self.validation_error_message_template = str(self.validation_error_message_template)

        if self.conditional is not None and not isinstance(self.conditional, str):
            self.conditional = str(self.conditional)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationExpression(YAMLRoot):
    """
    A logical expression, allowing for combining arguments into more complex validation rules
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ValidationExpression"]
    class_class_curie: ClassVar[str] = "pehterms:ValidationExpression"
    class_name: ClassVar[str] = "ValidationExpression"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ValidationExpression

    validation_subject_source_paths: Optional[Union[str, list[str]]] = empty_list()
    validation_condition_expression: Optional[Union[dict, "ValidationExpression"]] = None
    validation_command: Optional[Union[str, "ValidationCommand"]] = None
    validation_arg_values: Optional[Union[str, list[str]]] = empty_list()
    validation_arg_source_paths: Optional[Union[str, list[str]]] = empty_list()
    validation_arg_expressions: Optional[Union[Union[dict, "ValidationExpression"], list[Union[dict, "ValidationExpression"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.validation_subject_source_paths, list):
            self.validation_subject_source_paths = [self.validation_subject_source_paths] if self.validation_subject_source_paths is not None else []
        self.validation_subject_source_paths = [v if isinstance(v, str) else str(v) for v in self.validation_subject_source_paths]

        if self.validation_condition_expression is not None and not isinstance(self.validation_condition_expression, ValidationExpression):
            self.validation_condition_expression = ValidationExpression(**as_dict(self.validation_condition_expression))

        if self.validation_command is not None and not isinstance(self.validation_command, ValidationCommand):
            self.validation_command = ValidationCommand(self.validation_command)

        if not isinstance(self.validation_arg_values, list):
            self.validation_arg_values = [self.validation_arg_values] if self.validation_arg_values is not None else []
        self.validation_arg_values = [v if isinstance(v, str) else str(v) for v in self.validation_arg_values]

        if not isinstance(self.validation_arg_source_paths, list):
            self.validation_arg_source_paths = [self.validation_arg_source_paths] if self.validation_arg_source_paths is not None else []
        self.validation_arg_source_paths = [v if isinstance(v, str) else str(v) for v in self.validation_arg_source_paths]

        if not isinstance(self.validation_arg_expressions, list):
            self.validation_arg_expressions = [self.validation_arg_expressions] if self.validation_arg_expressions is not None else []
        self.validation_arg_expressions = [v if isinstance(v, ValidationExpression) else ValidationExpression(**as_dict(v)) for v in self.validation_arg_expressions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Contact(YAMLRoot):
    """
    A stakeholder having a contact role in the research process
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Contact"]
    class_class_curie: ClassVar[str] = "pehterms:Contact"
    class_name: ClassVar[str] = "Contact"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Contact

    name: Optional[str] = None
    orcid: Optional[str] = None
    contact_roles: Optional[Union[Union[str, "ContactRole"], list[Union[str, "ContactRole"]]]] = empty_list()
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.orcid is not None and not isinstance(self.orcid, str):
            self.orcid = str(self.orcid)

        if not isinstance(self.contact_roles, list):
            self.contact_roles = [self.contact_roles] if self.contact_roles is not None else []
        self.contact_roles = [v if isinstance(v, ContactRole) else ContactRole(v) for v in self.contact_roles]

        if self.contact_email is not None and not isinstance(self.contact_email, str):
            self.contact_email = str(self.contact_email)

        if self.contact_phone is not None and not isinstance(self.contact_phone, str):
            self.contact_phone = str(self.contact_phone)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Stakeholder(NamedThing):
    """
    Any organisation involved in the research process
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Stakeholder"]
    class_class_curie: ClassVar[str] = "pehterms:Stakeholder"
    class_name: ClassVar[str] = "Stakeholder"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Stakeholder

    id: Union[str, StakeholderId] = None
    rorid: Optional[str] = None
    geographic_scope: Optional[str] = None
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StakeholderId):
            self.id = StakeholderId(self.id)

        if self.rorid is not None and not isinstance(self.rorid, str):
            self.rorid = str(self.rorid)

        if self.geographic_scope is not None and not isinstance(self.geographic_scope, str):
            self.geographic_scope = str(self.geographic_scope)

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProjectStakeholder(YAMLRoot):
    """
    An organisation collaborating in a Personal Exposure and Health research project
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ProjectStakeholder"]
    class_class_curie: ClassVar[str] = "pehterms:ProjectStakeholder"
    class_name: ClassVar[str] = "ProjectStakeholder"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ProjectStakeholder

    stakeholder: Optional[Union[str, StakeholderId]] = None
    project_roles: Optional[Union[Union[str, "ProjectRole"], list[Union[str, "ProjectRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], list[Union[dict, Contact]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.project_roles, list):
            self.project_roles = [self.project_roles] if self.project_roles is not None else []
        self.project_roles = [v if isinstance(v, ProjectRole) else ProjectRole(v) for v in self.project_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyEntity(NamedThing):
    """
    Any entity carrying data or context relevant to a Personal Exposure and Health research project or study
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudyEntity"]
    class_class_curie: ClassVar[str] = "pehterms:StudyEntity"
    class_name: ClassVar[str] = "StudyEntity"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudyEntity

    id: Union[str, StudyEntityId] = None
    physical_entity: Optional[Union[str, PhysicalEntityId]] = None
    study_entity_links: Optional[Union[Union[dict, "StudyEntityLink"], list[Union[dict, "StudyEntityLink"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.physical_entity is not None and not isinstance(self.physical_entity, PhysicalEntityId):
            self.physical_entity = PhysicalEntityId(self.physical_entity)

        if not isinstance(self.study_entity_links, list):
            self.study_entity_links = [self.study_entity_links] if self.study_entity_links is not None else []
        self.study_entity_links = [v if isinstance(v, StudyEntityLink) else StudyEntityLink(**as_dict(v)) for v in self.study_entity_links]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Project(StudyEntity):
    """
    A collaborative effort in the Personal Exposure and Health research domain
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Project"]
    class_class_curie: ClassVar[str] = "pehterms:Project"
    class_name: ClassVar[str] = "Project"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Project

    id: Union[str, ProjectId] = None
    default_language: Optional[str] = None
    project_stakeholders: Optional[Union[Union[dict, ProjectStakeholder], list[Union[dict, ProjectStakeholder]]]] = empty_list()
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    study_id_list: Optional[Union[Union[str, StudyId], list[Union[str, StudyId]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProjectId):
            self.id = ProjectId(self.id)

        if self.default_language is not None and not isinstance(self.default_language, str):
            self.default_language = str(self.default_language)

        if not isinstance(self.project_stakeholders, list):
            self.project_stakeholders = [self.project_stakeholders] if self.project_stakeholders is not None else []
        self.project_stakeholders = [v if isinstance(v, ProjectStakeholder) else ProjectStakeholder(**as_dict(v)) for v in self.project_stakeholders]

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if not isinstance(self.study_id_list, list):
            self.study_id_list = [self.study_id_list] if self.study_id_list is not None else []
        self.study_id_list = [v if isinstance(v, StudyId) else StudyId(v) for v in self.study_id_list]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyEntityLink(YAMLRoot):
    """
    A relational property that allows creating qualified links to study entities
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudyEntityLink"]
    class_class_curie: ClassVar[str] = "pehterms:StudyEntityLink"
    class_name: ClassVar[str] = "StudyEntityLink"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudyEntityLink

    linktype: Optional[Union[str, "LinkType"]] = None
    study_entity: Optional[Union[str, StudyEntityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.linktype is not None and not isinstance(self.linktype, LinkType):
            self.linktype = LinkType(self.linktype)

        if self.study_entity is not None and not isinstance(self.study_entity, StudyEntityId):
            self.study_entity = StudyEntityId(self.study_entity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Study(StudyEntity):
    """
    A structured, goal-directed observational investigation designed to collect and analyze data on human subjects and
    their environments
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Study"]
    class_class_curie: ClassVar[str] = "pehterms:Study"
    class_name: ClassVar[str] = "Study"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Study

    id: Union[str, StudyId] = None
    default_language: Optional[str] = None
    study_stakeholders: Optional[Union[Union[dict, "StudyStakeholder"], list[Union[dict, "StudyStakeholder"]]]] = empty_list()
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    observation_group_id_list: Optional[Union[Union[str, ObservationGroupId], list[Union[str, ObservationGroupId]]]] = empty_list()
    study_entity_id_list: Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]] = empty_list()
    project_id_list: Optional[Union[Union[str, ProjectId], list[Union[str, ProjectId]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudyId):
            self.id = StudyId(self.id)

        if self.default_language is not None and not isinstance(self.default_language, str):
            self.default_language = str(self.default_language)

        if not isinstance(self.study_stakeholders, list):
            self.study_stakeholders = [self.study_stakeholders] if self.study_stakeholders is not None else []
        self.study_stakeholders = [v if isinstance(v, StudyStakeholder) else StudyStakeholder(**as_dict(v)) for v in self.study_stakeholders]

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if not isinstance(self.observation_group_id_list, list):
            self.observation_group_id_list = [self.observation_group_id_list] if self.observation_group_id_list is not None else []
        self.observation_group_id_list = [v if isinstance(v, ObservationGroupId) else ObservationGroupId(v) for v in self.observation_group_id_list]

        if not isinstance(self.study_entity_id_list, list):
            self.study_entity_id_list = [self.study_entity_id_list] if self.study_entity_id_list is not None else []
        self.study_entity_id_list = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.study_entity_id_list]

        if not isinstance(self.project_id_list, list):
            self.project_id_list = [self.project_id_list] if self.project_id_list is not None else []
        self.project_id_list = [v if isinstance(v, ProjectId) else ProjectId(v) for v in self.project_id_list]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyStakeholder(YAMLRoot):
    """
    An organisation collaborating in a Personal Exposure and Health research study
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudyStakeholder"]
    class_class_curie: ClassVar[str] = "pehterms:StudyStakeholder"
    class_name: ClassVar[str] = "StudyStakeholder"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudyStakeholder

    stakeholder: Optional[Union[str, StakeholderId]] = None
    study_roles: Optional[Union[Union[str, "StudyRole"], list[Union[str, "StudyRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], list[Union[dict, Contact]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.study_roles, list):
            self.study_roles = [self.study_roles] if self.study_roles is not None else []
        self.study_roles = [v if isinstance(v, StudyRole) else StudyRole(v) for v in self.study_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservationGroup(StudyEntity):
    """
    A grouped collection of observations, intended and/or executed, as part of a Personal Exposure and Health research
    study
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservationGroup"]
    class_class_curie: ClassVar[str] = "pehterms:ObservationGroup"
    class_name: ClassVar[str] = "ObservationGroup"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservationGroup

    id: Union[str, ObservationGroupId] = None
    sort_order: Optional[Decimal] = None
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    observation_id_list: Optional[Union[Union[str, ObservationId], list[Union[str, ObservationId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObservationGroupId):
            self.id = ObservationGroupId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if not isinstance(self.observation_id_list, list):
            self.observation_id_list = [self.observation_id_list] if self.observation_id_list is not None else []
        self.observation_id_list = [v if isinstance(v, ObservationId) else ObservationId(v) for v in self.observation_id_list]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyPopulation(StudyEntity):
    """
    A group of study entities that is itself also a study entity that observations can be recorded for
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudyPopulation"]
    class_class_curie: ClassVar[str] = "pehterms:StudyPopulation"
    class_name: ClassVar[str] = "StudyPopulation"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudyPopulation

    id: Union[str, StudyPopulationId] = None
    research_population_type: Optional[Union[str, "ResearchPopulationType"]] = None
    member_id_list: Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudyPopulationId):
            self.id = StudyPopulationId(self.id)

        if self.research_population_type is not None and not isinstance(self.research_population_type, ResearchPopulationType):
            self.research_population_type = ResearchPopulationType(self.research_population_type)

        if not isinstance(self.member_id_list, list):
            self.member_id_list = [self.member_id_list] if self.member_id_list is not None else []
        self.member_id_list = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.member_id_list]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SampleCollection(StudyEntity):
    """
    A collection of samples that is itself also a study entity that observations can be recorded for
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["SampleCollection"]
    class_class_curie: ClassVar[str] = "pehterms:SampleCollection"
    class_name: ClassVar[str] = "SampleCollection"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.SampleCollection

    id: Union[str, SampleCollectionId] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, list[str]]] = empty_list()
    sample_id_list: Optional[Union[Union[str, SampleId], list[Union[str, SampleId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SampleCollectionId):
            self.id = SampleCollectionId(self.id)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        if not isinstance(self.sample_id_list, list):
            self.sample_id_list = [self.sample_id_list] if self.sample_id_list is not None else []
        self.sample_id_list = [v if isinstance(v, SampleId) else SampleId(v) for v in self.sample_id_list]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudySubject(StudyEntity):
    """
    A study entity that is a main subject for the study
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudySubject"]
    class_class_curie: ClassVar[str] = "pehterms:StudySubject"
    class_name: ClassVar[str] = "StudySubject"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudySubject

    id: Union[str, StudySubjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudySubjectId):
            self.id = StudySubjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudySubjectGroup(StudyEntity):
    """
    A group of study subjects that is itself also a study entity that observations can be recorded for
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["StudySubjectGroup"]
    class_class_curie: ClassVar[str] = "pehterms:StudySubjectGroup"
    class_name: ClassVar[str] = "StudySubjectGroup"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.StudySubjectGroup

    id: Union[str, StudySubjectGroupId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudySubjectGroupId):
            self.id = StudySubjectGroupId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Observation(NamedThing):
    """
    The registration of the intent to perform a set of observations as well as the resulting observed values
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["Observation"]
    class_class_curie: ClassVar[str] = "pehterms:Observation"
    class_name: ClassVar[str] = "Observation"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.Observation

    id: Union[str, ObservationId] = None
    observation_type: Optional[Union[str, "ObservationType"]] = None
    observation_design: Optional[Union[dict, "ObservationDesign"]] = None
    observation_result_id_list: Optional[Union[Union[str, ObservationResultId], list[Union[str, ObservationResultId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.observation_type is not None and not isinstance(self.observation_type, ObservationType):
            self.observation_type = ObservationType(self.observation_type)

        if self.observation_design is not None and not isinstance(self.observation_design, ObservationDesign):
            self.observation_design = ObservationDesign(**as_dict(self.observation_design))

        if not isinstance(self.observation_result_id_list, list):
            self.observation_result_id_list = [self.observation_result_id_list] if self.observation_result_id_list is not None else []
        self.observation_result_id_list = [v if isinstance(v, ObservationResultId) else ObservationResultId(v) for v in self.observation_result_id_list]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservationDesign(YAMLRoot):
    """
    The registration of the intent to perform a number of observations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservationDesign"]
    class_class_curie: ClassVar[str] = "pehterms:ObservationDesign"
    class_name: ClassVar[str] = "ObservationDesign"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservationDesign

    observable_entity_property_sets: Optional[Union[Union[dict, "ObservableEntityPropertySet"], list[Union[dict, "ObservableEntityPropertySet"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.observable_entity_property_sets, list):
            self.observable_entity_property_sets = [self.observable_entity_property_sets] if self.observable_entity_property_sets is not None else []
        self.observable_entity_property_sets = [v if isinstance(v, ObservableEntityPropertySet) else ObservableEntityPropertySet(**as_dict(v)) for v in self.observable_entity_property_sets]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservableEntityPropertySet(YAMLRoot):
    """
    The list of properties being observed and the study entities they will be observed for (or, alternatively, the
    entity type all observed entities belong to)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservableEntityPropertySet"]
    class_class_curie: ClassVar[str] = "pehterms:ObservableEntityPropertySet"
    class_name: ClassVar[str] = "ObservableEntityPropertySet"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservableEntityPropertySet

    observation_result_type: Optional[Union[str, "ObservationResultType"]] = None
    observable_entity_type: Optional[Union[str, "ObservableEntityType"]] = None
    observable_entity_id_list: Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]] = empty_list()
    identifying_observable_property_id_list: Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]] = empty_list()
    required_observable_property_id_list: Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]] = empty_list()
    optional_observable_property_id_list: Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.observation_result_type is not None and not isinstance(self.observation_result_type, ObservationResultType):
            self.observation_result_type = ObservationResultType(self.observation_result_type)

        if self.observable_entity_type is not None and not isinstance(self.observable_entity_type, ObservableEntityType):
            self.observable_entity_type = ObservableEntityType(self.observable_entity_type)

        if not isinstance(self.observable_entity_id_list, list):
            self.observable_entity_id_list = [self.observable_entity_id_list] if self.observable_entity_id_list is not None else []
        self.observable_entity_id_list = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.observable_entity_id_list]

        if not isinstance(self.identifying_observable_property_id_list, list):
            self.identifying_observable_property_id_list = [self.identifying_observable_property_id_list] if self.identifying_observable_property_id_list is not None else []
        self.identifying_observable_property_id_list = [v if isinstance(v, ObservablePropertyId) else ObservablePropertyId(v) for v in self.identifying_observable_property_id_list]

        if not isinstance(self.required_observable_property_id_list, list):
            self.required_observable_property_id_list = [self.required_observable_property_id_list] if self.required_observable_property_id_list is not None else []
        self.required_observable_property_id_list = [v if isinstance(v, ObservablePropertyId) else ObservablePropertyId(v) for v in self.required_observable_property_id_list]

        if not isinstance(self.optional_observable_property_id_list, list):
            self.optional_observable_property_id_list = [self.optional_observable_property_id_list] if self.optional_observable_property_id_list is not None else []
        self.optional_observable_property_id_list = [v if isinstance(v, ObservablePropertyId) else ObservablePropertyId(v) for v in self.optional_observable_property_id_list]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservationResult(NamedThing):
    """
    The result of an observational effort in Personal Exposure and Health research
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservationResult"]
    class_class_curie: ClassVar[str] = "pehterms:ObservationResult"
    class_name: ClassVar[str] = "ObservationResult"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservationResult

    id: Union[str, ObservationResultId] = None
    observation_result_type: Optional[Union[str, "ObservationResultType"]] = None
    observation_start_date: Optional[Union[str, XSDDate]] = None
    observation_end_date: Optional[Union[str, XSDDate]] = None
    observed_values: Optional[Union[Union[dict, "ObservedValue"], list[Union[dict, "ObservedValue"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.observation_result_type is not None and not isinstance(self.observation_result_type, ObservationResultType):
            self.observation_result_type = ObservationResultType(self.observation_result_type)

        if self.observation_start_date is not None and not isinstance(self.observation_start_date, XSDDate):
            self.observation_start_date = XSDDate(self.observation_start_date)

        if self.observation_end_date is not None and not isinstance(self.observation_end_date, XSDDate):
            self.observation_end_date = XSDDate(self.observation_end_date)

        if not isinstance(self.observed_values, list):
            self.observed_values = [self.observed_values] if self.observed_values is not None else []
        self.observed_values = [v if isinstance(v, ObservedValue) else ObservedValue(**as_dict(v)) for v in self.observed_values]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservedValue(YAMLRoot):
    """
    A single observational result value registering a specific property for a specific entity at a specific moment
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservedValue"]
    class_class_curie: ClassVar[str] = "pehterms:ObservedValue"
    class_name: ClassVar[str] = "ObservedValue"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservedValue

    observable_entity: Optional[Union[str, StudyEntityId]] = None
    observable_property: Optional[Union[str, ObservablePropertyId]] = None
    default_unit: Optional[str] = None
    raw_value: Optional[str] = None
    raw_unit: Optional[str] = None
    imputed_value: Optional[str] = None
    imputed_unit: Optional[str] = None
    normalised_value: Optional[str] = None
    normalised_unit: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[Union[str, UnitId]] = None
    value_as_string: Optional[str] = None
    quality_data: Optional[Union[Union[dict, "QualityData"], list[Union[dict, "QualityData"]]]] = empty_list()
    provenance_data: Optional[Union[Union[dict, "ProvenanceData"], list[Union[dict, "ProvenanceData"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.observable_entity is not None and not isinstance(self.observable_entity, StudyEntityId):
            self.observable_entity = StudyEntityId(self.observable_entity)

        if self.observable_property is not None and not isinstance(self.observable_property, ObservablePropertyId):
            self.observable_property = ObservablePropertyId(self.observable_property)

        if self.default_unit is not None and not isinstance(self.default_unit, str):
            self.default_unit = str(self.default_unit)

        if self.raw_value is not None and not isinstance(self.raw_value, str):
            self.raw_value = str(self.raw_value)

        if self.raw_unit is not None and not isinstance(self.raw_unit, str):
            self.raw_unit = str(self.raw_unit)

        if self.imputed_value is not None and not isinstance(self.imputed_value, str):
            self.imputed_value = str(self.imputed_value)

        if self.imputed_unit is not None and not isinstance(self.imputed_unit, str):
            self.imputed_unit = str(self.imputed_unit)

        if self.normalised_value is not None and not isinstance(self.normalised_value, str):
            self.normalised_value = str(self.normalised_value)

        if self.normalised_unit is not None and not isinstance(self.normalised_unit, str):
            self.normalised_unit = str(self.normalised_unit)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        if self.value_as_string is not None and not isinstance(self.value_as_string, str):
            self.value_as_string = str(self.value_as_string)

        if not isinstance(self.quality_data, list):
            self.quality_data = [self.quality_data] if self.quality_data is not None else []
        self.quality_data = [v if isinstance(v, QualityData) else QualityData(**as_dict(v)) for v in self.quality_data]

        if not isinstance(self.provenance_data, list):
            self.provenance_data = [self.provenance_data] if self.provenance_data is not None else []
        self.provenance_data = [v if isinstance(v, ProvenanceData) else ProvenanceData(**as_dict(v)) for v in self.provenance_data]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QualityData(YAMLRoot):
    """
    Quality metadata, adding context to an Observed Value
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["QualityData"]
    class_class_curie: ClassVar[str] = "pehterms:QualityData"
    class_name: ClassVar[str] = "QualityData"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.QualityData

    quality_context_key: Optional[str] = None
    quality_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.quality_context_key is not None and not isinstance(self.quality_context_key, str):
            self.quality_context_key = str(self.quality_context_key)

        if self.quality_value is not None and not isinstance(self.quality_value, str):
            self.quality_value = str(self.quality_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProvenanceData(YAMLRoot):
    """
    Provenance metadata, adding context to an Observed Value
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ProvenanceData"]
    class_class_curie: ClassVar[str] = "pehterms:ProvenanceData"
    class_name: ClassVar[str] = "ProvenanceData"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ProvenanceData

    provenance_context_key: Optional[str] = None
    provenance_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.provenance_context_key is not None and not isinstance(self.provenance_context_key, str):
            self.provenance_context_key = str(self.provenance_context_key)

        if self.provenance_value is not None and not isinstance(self.provenance_value, str):
            self.provenance_value = str(self.provenance_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataLayout(NamedThing):
    """
    Layout, allowing the definition of templating sections for combining layout and data elements
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataLayout"]
    class_class_curie: ClassVar[str] = "pehterms:DataLayout"
    class_name: ClassVar[str] = "DataLayout"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataLayout

    id: Union[str, DataLayoutId] = None
    sections: Optional[Union[dict[Union[str, DataLayoutSectionId], Union[dict, "DataLayoutSection"]], list[Union[dict, "DataLayoutSection"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataLayoutId):
            self.id = DataLayoutId(self.id)

        self._normalize_inlined_as_list(slot_name="sections", slot_type=DataLayoutSection, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataLayoutSection(NamedThing):
    """
    Definition for an individual layout or data section, as part of a full layout
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataLayoutSection"]
    class_class_curie: ClassVar[str] = "pehterms:DataLayoutSection"
    class_name: ClassVar[str] = "DataLayoutSection"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataLayoutSection

    id: Union[str, DataLayoutSectionId] = None
    section_type: Optional[Union[str, "DataLayoutSectionType"]] = None
    observable_entity_types: Optional[Union[Union[str, "ObservableEntityType"], list[Union[str, "ObservableEntityType"]]]] = empty_list()
    observable_entity_grouping_id_list: Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]] = empty_list()
    elements: Optional[Union[Union[dict, "DataLayoutElement"], list[Union[dict, "DataLayoutElement"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataLayoutSectionId):
            self.id = DataLayoutSectionId(self.id)

        if self.section_type is not None and not isinstance(self.section_type, DataLayoutSectionType):
            self.section_type = DataLayoutSectionType(self.section_type)

        if not isinstance(self.observable_entity_types, list):
            self.observable_entity_types = [self.observable_entity_types] if self.observable_entity_types is not None else []
        self.observable_entity_types = [v if isinstance(v, ObservableEntityType) else ObservableEntityType(v) for v in self.observable_entity_types]

        if not isinstance(self.observable_entity_grouping_id_list, list):
            self.observable_entity_grouping_id_list = [self.observable_entity_grouping_id_list] if self.observable_entity_grouping_id_list is not None else []
        self.observable_entity_grouping_id_list = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.observable_entity_grouping_id_list]

        if not isinstance(self.elements, list):
            self.elements = [self.elements] if self.elements is not None else []
        self.elements = [v if isinstance(v, DataLayoutElement) else DataLayoutElement(**as_dict(v)) for v in self.elements]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataLayoutElement(YAMLRoot):
    """
    Definition for an individual layout or data element, as part of a layout section
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataLayoutElement"]
    class_class_curie: ClassVar[str] = "pehterms:DataLayoutElement"
    class_name: ClassVar[str] = "DataLayoutElement"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataLayoutElement

    label: Optional[str] = None
    element_type: Optional[Union[str, "DataLayoutElementType"]] = None
    element_style: Optional[Union[str, "DataLayoutElementStyle"]] = None
    varname: Optional[str] = None
    observable_property: Optional[Union[str, ObservablePropertyId]] = None
    is_observable_entity_key: Optional[Union[bool, Bool]] = None
    is_foreign_key: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.element_type is not None and not isinstance(self.element_type, DataLayoutElementType):
            self.element_type = DataLayoutElementType(self.element_type)

        if self.element_style is not None and not isinstance(self.element_style, DataLayoutElementStyle):
            self.element_style = DataLayoutElementStyle(self.element_style)

        if self.varname is not None and not isinstance(self.varname, str):
            self.varname = str(self.varname)

        if self.observable_property is not None and not isinstance(self.observable_property, ObservablePropertyId):
            self.observable_property = ObservablePropertyId(self.observable_property)

        if self.is_observable_entity_key is not None and not isinstance(self.is_observable_entity_key, Bool):
            self.is_observable_entity_key = Bool(self.is_observable_entity_key)

        if self.is_foreign_key is not None and not isinstance(self.is_foreign_key, Bool):
            self.is_foreign_key = Bool(self.is_foreign_key)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataRequest(NamedThing):
    """
    Registration of a request for data by a data user
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataRequest"]
    class_class_curie: ClassVar[str] = "pehterms:DataRequest"
    class_name: ClassVar[str] = "DataRequest"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataRequest

    id: Union[str, DataRequestId] = None
    contacts: Optional[Union[Union[dict, Contact], list[Union[dict, Contact]]]] = empty_list()
    request_properties: Optional[str] = None
    data_stakeholders: Optional[Union[Union[str, DataStakeholderId], list[Union[str, DataStakeholderId]]]] = empty_list()
    research_objectives: Optional[Union[Union[str, ResearchObjectiveId], list[Union[str, ResearchObjectiveId]]]] = empty_list()
    processing_actions: Optional[Union[Union[str, ProcessingActionId], list[Union[str, ProcessingActionId]]]] = empty_list()
    processing_steps: Optional[Union[Union[str, ProcessingStepId], list[Union[str, ProcessingStepId]]]] = empty_list()
    remark_on_content: Optional[str] = None
    remark_on_methodology: Optional[str] = None
    observed_entity_properties: Optional[Union[Union[dict, "ObservedEntityProperty"], list[Union[dict, "ObservedEntityProperty"]]]] = empty_list()
    observable_entity_property_sets: Optional[Union[Union[dict, ObservableEntityPropertySet], list[Union[dict, ObservableEntityPropertySet]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataRequestId):
            self.id = DataRequestId(self.id)

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if self.request_properties is not None and not isinstance(self.request_properties, str):
            self.request_properties = str(self.request_properties)

        if not isinstance(self.data_stakeholders, list):
            self.data_stakeholders = [self.data_stakeholders] if self.data_stakeholders is not None else []
        self.data_stakeholders = [v if isinstance(v, DataStakeholderId) else DataStakeholderId(v) for v in self.data_stakeholders]

        if not isinstance(self.research_objectives, list):
            self.research_objectives = [self.research_objectives] if self.research_objectives is not None else []
        self.research_objectives = [v if isinstance(v, ResearchObjectiveId) else ResearchObjectiveId(v) for v in self.research_objectives]

        if not isinstance(self.processing_actions, list):
            self.processing_actions = [self.processing_actions] if self.processing_actions is not None else []
        self.processing_actions = [v if isinstance(v, ProcessingActionId) else ProcessingActionId(v) for v in self.processing_actions]

        if not isinstance(self.processing_steps, list):
            self.processing_steps = [self.processing_steps] if self.processing_steps is not None else []
        self.processing_steps = [v if isinstance(v, ProcessingStepId) else ProcessingStepId(v) for v in self.processing_steps]

        if self.remark_on_content is not None and not isinstance(self.remark_on_content, str):
            self.remark_on_content = str(self.remark_on_content)

        if self.remark_on_methodology is not None and not isinstance(self.remark_on_methodology, str):
            self.remark_on_methodology = str(self.remark_on_methodology)

        if not isinstance(self.observed_entity_properties, list):
            self.observed_entity_properties = [self.observed_entity_properties] if self.observed_entity_properties is not None else []
        self.observed_entity_properties = [v if isinstance(v, ObservedEntityProperty) else ObservedEntityProperty(**as_dict(v)) for v in self.observed_entity_properties]

        if not isinstance(self.observable_entity_property_sets, list):
            self.observable_entity_property_sets = [self.observable_entity_property_sets] if self.observable_entity_property_sets is not None else []
        self.observable_entity_property_sets = [v if isinstance(v, ObservableEntityPropertySet) else ObservableEntityPropertySet(**as_dict(v)) for v in self.observable_entity_property_sets]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObservedEntityProperty(YAMLRoot):
    """
    Conceptual definition of the observation of a certain property for a certain entity in a study
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ObservedEntityProperty"]
    class_class_curie: ClassVar[str] = "pehterms:ObservedEntityProperty"
    class_name: ClassVar[str] = "ObservedEntityProperty"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ObservedEntityProperty

    observable_entity: Optional[Union[str, StudyEntityId]] = None
    observable_property: Optional[Union[str, ObservablePropertyId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.observable_entity is not None and not isinstance(self.observable_entity, StudyEntityId):
            self.observable_entity = StudyEntityId(self.observable_entity)

        if self.observable_property is not None and not isinstance(self.observable_property, ObservablePropertyId):
            self.observable_property = ObservablePropertyId(self.observable_property)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataStakeholder(NamedThing):
    """
    An organisation participating in a data process in Personal Exposure and Health research
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataStakeholder"]
    class_class_curie: ClassVar[str] = "pehterms:DataStakeholder"
    class_name: ClassVar[str] = "DataStakeholder"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataStakeholder

    id: Union[str, DataStakeholderId] = None
    stakeholder: Optional[Union[str, StakeholderId]] = None
    data_roles: Optional[Union[Union[str, "DataRole"], list[Union[str, "DataRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], list[Union[dict, Contact]]]] = empty_list()
    processing_description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataStakeholderId):
            self.id = DataStakeholderId(self.id)

        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.data_roles, list):
            self.data_roles = [self.data_roles] if self.data_roles is not None else []
        self.data_roles = [v if isinstance(v, DataRole) else DataRole(v) for v in self.data_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if self.processing_description is not None and not isinstance(self.processing_description, str):
            self.processing_description = str(self.processing_description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResearchObjective(NamedThing):
    """
    A research objective communicated in the request and used to evaluate if the request is valid and appropriate
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ResearchObjective"]
    class_class_curie: ClassVar[str] = "pehterms:ResearchObjective"
    class_name: ClassVar[str] = "ResearchObjective"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ResearchObjective

    id: Union[str, ResearchObjectiveId] = None
    objective_type: Optional[Union[str, "ObjectiveType"]] = None
    authors: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResearchObjectiveId):
            self.id = ResearchObjectiveId(self.id)

        if self.objective_type is not None and not isinstance(self.objective_type, ObjectiveType):
            self.objective_type = ObjectiveType(self.objective_type)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, str) else str(v) for v in self.authors]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProcessingAction(NamedThing):
    """
    One action in the data request and processing flow
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ProcessingAction"]
    class_class_curie: ClassVar[str] = "pehterms:ProcessingAction"
    class_name: ClassVar[str] = "ProcessingAction"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ProcessingAction

    id: Union[str, ProcessingActionId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessingActionId):
            self.id = ProcessingActionId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProcessingStep(NamedThing):
    """
    One step in the data request and processing flow
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["ProcessingStep"]
    class_class_curie: ClassVar[str] = "pehterms:ProcessingStep"
    class_name: ClassVar[str] = "ProcessingStep"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.ProcessingStep

    id: Union[str, ProcessingStepId] = None
    start_date: Optional[Union[str, XSDDate]] = None
    delivery_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessingStepId):
            self.id = ProcessingStepId(self.id)

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.delivery_date is not None and not isinstance(self.delivery_date, XSDDate):
            self.delivery_date = XSDDate(self.delivery_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataExtract(YAMLRoot):
    """
    A set of Observed Values, combined into a data extract
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEHTERMS["DataExtract"]
    class_class_curie: ClassVar[str] = "pehterms:DataExtract"
    class_name: ClassVar[str] = "DataExtract"
    class_model_uri: ClassVar[URIRef] = PEHTERMS.DataExtract

    observed_values: Optional[Union[Union[dict, ObservedValue], list[Union[dict, ObservedValue]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.observed_values, list):
            self.observed_values = [self.observed_values] if self.observed_values is not None else []
        self.observed_values = [v if isinstance(v, ObservedValue) else ObservedValue(**as_dict(v)) for v in self.observed_values]

        super().__post_init__(**kwargs)


# Enumerations
class ValidationStatus(EnumDefinitionImpl):

    unvalidated = PermissibleValue(text="unvalidated")
    in_progress = PermissibleValue(text="in_progress")
    validated = PermissibleValue(text="validated")
    deprecated = PermissibleValue(text="deprecated")

    _defn = EnumDefinition(
        name="ValidationStatus",
    )

class ValidationCommand(EnumDefinitionImpl):

    is_equal_to = PermissibleValue(text="is_equal_to")
    is_equal_to_or_both_missing = PermissibleValue(text="is_equal_to_or_both_missing")
    is_greater_than_or_equal_to = PermissibleValue(text="is_greater_than_or_equal_to")
    is_greater_than = PermissibleValue(text="is_greater_than")
    is_less_than_or_equal_to = PermissibleValue(text="is_less_than_or_equal_to")
    is_less_than = PermissibleValue(text="is_less_than")
    is_not_equal_to = PermissibleValue(text="is_not_equal_to")
    is_not_equal_to_and_not_both_missing = PermissibleValue(text="is_not_equal_to_and_not_both_missing")
    is_unique = PermissibleValue(text="is_unique")
    is_duplicated = PermissibleValue(text="is_duplicated")
    is_in = PermissibleValue(text="is_in")
    is_null = PermissibleValue(text="is_null")
    is_not_null = PermissibleValue(text="is_not_null")
    conjunction = PermissibleValue(text="conjunction")
    disjunction = PermissibleValue(text="disjunction")

    _defn = EnumDefinition(
        name="ValidationCommand",
    )

class ValidationErrorLevel(EnumDefinitionImpl):

    info = PermissibleValue(text="info")
    warning = PermissibleValue(text="warning")
    error = PermissibleValue(text="error")
    fatal = PermissibleValue(text="fatal")

    _defn = EnumDefinition(
        name="ValidationErrorLevel",
    )

class DataLayoutElementStyle(EnumDefinitionImpl):

    standard = PermissibleValue(text="standard")
    main_title = PermissibleValue(text="main_title")
    section_title = PermissibleValue(text="section_title")
    sub_title = PermissibleValue(text="sub_title")
    comment = PermissibleValue(text="comment")
    warning = PermissibleValue(text="warning")
    alert = PermissibleValue(text="alert")

    _defn = EnumDefinition(
        name="DataLayoutElementStyle",
    )

class IndicatorType(EnumDefinitionImpl):

    effectmarker = PermissibleValue(text="effectmarker")
    exposuremarker = PermissibleValue(text="exposuremarker")
    geomarker = PermissibleValue(text="geomarker")
    observation = PermissibleValue(text="observation")

    _defn = EnumDefinition(
        name="IndicatorType",
    )

class BioChemEntityLinkType(EnumDefinitionImpl):

    exact_match = PermissibleValue(text="exact_match")
    close_match = PermissibleValue(text="close_match")
    broader = PermissibleValue(text="broader")
    part_of = PermissibleValue(text="part_of")
    group_contains = PermissibleValue(text="group_contains")
    has_parent_compound = PermissibleValue(text="has_parent_compound")
    branched_version_of = PermissibleValue(text="branched_version_of")

    _defn = EnumDefinition(
        name="BioChemEntityLinkType",
    )

class ResearchPopulationType(EnumDefinitionImpl):

    general_population = PermissibleValue(text="general_population")
    person = PermissibleValue(text="person")
    newborn = PermissibleValue(text="newborn")
    adolescent = PermissibleValue(text="adolescent")
    mother = PermissibleValue(text="mother")
    parent = PermissibleValue(text="parent")
    pregnant_person = PermissibleValue(text="pregnant_person")
    household = PermissibleValue(text="household")

    _defn = EnumDefinition(
        name="ResearchPopulationType",
    )

class ObservableEntityType(EnumDefinitionImpl):

    project = PermissibleValue(text="project")
    organisation = PermissibleValue(text="organisation")
    study = PermissibleValue(text="study")
    environment = PermissibleValue(text="environment")
    location = PermissibleValue(text="location")
    persongroup = PermissibleValue(text="persongroup")
    person = PermissibleValue(text="person")
    samplegroup = PermissibleValue(text="samplegroup")
    sample = PermissibleValue(text="sample")
    dataset = PermissibleValue(text="dataset")
    collection_process = PermissibleValue(text="collection_process")
    lab_analysis_process = PermissibleValue(text="lab_analysis_process")
    model_execution_process = PermissibleValue(text="model_execution_process")
    data_process = PermissibleValue(text="data_process")

    _defn = EnumDefinition(
        name="ObservableEntityType",
    )

class ObservationType(EnumDefinitionImpl):

    sampling = PermissibleValue(text="sampling")
    questionnaire = PermissibleValue(text="questionnaire")
    geospatial = PermissibleValue(text="geospatial")
    metadata = PermissibleValue(text="metadata")

    _defn = EnumDefinition(
        name="ObservationType",
    )

class ObservationResultType(EnumDefinitionImpl):

    measurement = PermissibleValue(text="measurement")
    control = PermissibleValue(text="control")
    calculation = PermissibleValue(text="calculation")
    simulation = PermissibleValue(text="simulation")

    _defn = EnumDefinition(
        name="ObservationResultType",
    )

class DataLayoutSectionType(EnumDefinitionImpl):

    data_form = PermissibleValue(text="data_form")
    data_table = PermissibleValue(text="data_table")
    property_table = PermissibleValue(text="property_table")

    _defn = EnumDefinition(
        name="DataLayoutSectionType",
    )

class DataLayoutElementType(EnumDefinitionImpl):

    text = PermissibleValue(text="text")
    spacer = PermissibleValue(text="spacer")
    data_field = PermissibleValue(text="data_field")

    _defn = EnumDefinition(
        name="DataLayoutElementType",
    )

class ObjectiveType(EnumDefinitionImpl):

    research_objective = PermissibleValue(text="research_objective")
    project_result = PermissibleValue(text="project_result")
    publication = PermissibleValue(text="publication")

    _defn = EnumDefinition(
        name="ObjectiveType",
    )

class LinkType(EnumDefinitionImpl):

    is_about = PermissibleValue(text="is_about")
    is_same_as = PermissibleValue(text="is_same_as")
    is_part_of = PermissibleValue(text="is_part_of")
    is_located_at = PermissibleValue(text="is_located_at")

    _defn = EnumDefinition(
        name="LinkType",
    )

class ContactRole(EnumDefinitionImpl):

    administrative = PermissibleValue(text="administrative")
    data = PermissibleValue(text="data")
    general = PermissibleValue(text="general")
    lead = PermissibleValue(text="lead")
    legal = PermissibleValue(text="legal")
    technical = PermissibleValue(text="technical")

    _defn = EnumDefinition(
        name="ContactRole",
    )

class ProjectRole(EnumDefinitionImpl):

    member = PermissibleValue(text="member")
    partner = PermissibleValue(text="partner")
    funding_partner = PermissibleValue(text="funding_partner")
    principal_investigator = PermissibleValue(text="principal_investigator")
    data_governance = PermissibleValue(text="data_governance")
    data_controller = PermissibleValue(text="data_controller")
    data_processor = PermissibleValue(text="data_processor")
    data_user = PermissibleValue(text="data_user")
    lab = PermissibleValue(text="lab")

    _defn = EnumDefinition(
        name="ProjectRole",
    )

class StudyRole(EnumDefinitionImpl):

    funding_partner = PermissibleValue(text="funding_partner")
    principal_investigator = PermissibleValue(text="principal_investigator")
    data_controller = PermissibleValue(text="data_controller")
    data_processor = PermissibleValue(text="data_processor")
    data_user = PermissibleValue(text="data_user")
    lab = PermissibleValue(text="lab")

    _defn = EnumDefinition(
        name="StudyRole",
    )

class DataRole(EnumDefinitionImpl):

    main_stakeholder = PermissibleValue(text="main_stakeholder")
    supplying_data_controller = PermissibleValue(text="supplying_data_controller")
    receiving_data_controller = PermissibleValue(text="receiving_data_controller")
    external_data_controller = PermissibleValue(text="external_data_controller")

    _defn = EnumDefinition(
        name="DataRole",
    )

class QudtUnit(EnumDefinitionImpl):

    PERCENT = PermissibleValue(text="PERCENT")
    DAY = PermissibleValue(
        text="DAY",
        meaning=QUDTUNIT["DAY"])
    NanoGM = PermissibleValue(
        text="NanoGM",
        meaning=QUDTUNIT["NanoGM"])
    GM = PermissibleValue(
        text="GM",
        meaning=QUDTUNIT["GM"])
    MO = PermissibleValue(
        text="MO",
        meaning=QUDTUNIT["MO"])
    UNITLESS = PermissibleValue(
        text="UNITLESS",
        meaning=QUDTUNIT["UNITLESS"])
    MIN = PermissibleValue(
        text="MIN",
        meaning=QUDTUNIT["MIN"])
    MilliL = PermissibleValue(
        text="MilliL",
        meaning=QUDTUNIT["MilliL"])
    HR = PermissibleValue(
        text="HR",
        meaning=QUDTUNIT["HR"])
    PicoGM = PermissibleValue(
        text="PicoGM",
        meaning=QUDTUNIT["PicoGM"])
    NUM = PermissibleValue(
        text="NUM",
        meaning=QUDTUNIT["NUM"])
    KiloGM = PermissibleValue(
        text="KiloGM",
        meaning=QUDTUNIT["KiloGM"])
    CentiM = PermissibleValue(
        text="CentiM",
        meaning=QUDTUNIT["CentiM"])
    WK = PermissibleValue(
        text="WK",
        meaning=QUDTUNIT["WK"])
    L = PermissibleValue(
        text="L",
        meaning=QUDTUNIT["L"])
    YR = PermissibleValue(
        text="YR",
        meaning=QUDTUNIT["YR"])

    _defn = EnumDefinition(
        name="QudtUnit",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "KiloGM-PER-M3",
            PermissibleValue(
                text="KiloGM-PER-M3",
                meaning=QUDTUNIT["KiloGM-PER-M3"]))
        setattr(cls, "MilliGM-PER-KiloGM",
            PermissibleValue(
                text="MilliGM-PER-KiloGM",
                meaning=QUDTUNIT["MilliGM-PER-KiloGM"]))
        setattr(cls, "MilliMOL-PER-MOL",
            PermissibleValue(
                text="MilliMOL-PER-MOL",
                meaning=QUDTUNIT["MilliMOL-PER-MOL"]))
        setattr(cls, "MicroGM-PER-MilliL",
            PermissibleValue(
                text="MicroGM-PER-MilliL",
                meaning=QUDTUNIT["MicroGM-PER-MilliL"]))
        setattr(cls, "NanoMOL-PER-L",
            PermissibleValue(
                text="NanoMOL-PER-L",
                meaning=QUDTUNIT["NanoMOL-PER-L"]))
        setattr(cls, "NanoGM-PER-M3",
            PermissibleValue(
                text="NanoGM-PER-M3",
                meaning=QUDTUNIT["NanoGM-PER-M3"]))
        setattr(cls, "GM-PER-DeciL",
            PermissibleValue(
                text="GM-PER-DeciL",
                meaning=QUDTUNIT["GM-PER-DeciL"]))
        setattr(cls, "GM-PER-L",
            PermissibleValue(
                text="GM-PER-L",
                meaning=QUDTUNIT["GM-PER-L"]))
        setattr(cls, "FemtoMOL-PER-KiloGM",
            PermissibleValue(
                text="FemtoMOL-PER-KiloGM",
                meaning=QUDTUNIT["FemtoMOL-PER-KiloGM"]))
        setattr(cls, "NanoGM-PER-MilliL",
            PermissibleValue(
                text="NanoGM-PER-MilliL",
                meaning=QUDTUNIT["NanoGM-PER-MilliL"]))
        setattr(cls, "MicroGM-PER-KiloGM",
            PermissibleValue(
                text="MicroGM-PER-KiloGM",
                meaning=QUDTUNIT["MicroGM-PER-KiloGM"]))
        setattr(cls, "NanoGM-PER-L",
            PermissibleValue(
                text="NanoGM-PER-L",
                meaning=QUDTUNIT["NanoGM-PER-L"]))
        setattr(cls, "MicroMOL-PER-L",
            PermissibleValue(
                text="MicroMOL-PER-L",
                meaning=QUDTUNIT["MicroMOL-PER-L"]))
        setattr(cls, "MicroGM-PER-GM",
            PermissibleValue(
                text="MicroGM-PER-GM",
                meaning=QUDTUNIT["MicroGM-PER-GM"]))
        setattr(cls, "NanoGM-PER-DeciL",
            PermissibleValue(
                text="NanoGM-PER-DeciL",
                meaning=QUDTUNIT["NanoGM-PER-DeciL"]))
        setattr(cls, "MilliGM-PER-L",
            PermissibleValue(
                text="MilliGM-PER-L",
                meaning=QUDTUNIT["MilliGM-PER-L"]))
        setattr(cls, "PicoGM-PER-GM",
            PermissibleValue(
                text="PicoGM-PER-GM",
                meaning=QUDTUNIT["PicoGM-PER-GM"]))
        setattr(cls, "NanoGM-PER-M2",
            PermissibleValue(
                text="NanoGM-PER-M2",
                meaning=QUDTUNIT["NanoGM-PER-M2"]))
        setattr(cls, "IU-PER-L",
            PermissibleValue(
                text="IU-PER-L",
                meaning=QUDTUNIT["IU-PER-L"]))
        setattr(cls, "NUM-PER-MilliL",
            PermissibleValue(
                text="NUM-PER-MilliL",
                meaning=QUDTUNIT["NUM-PER-MilliL"]))
        setattr(cls, "GM-PER-MOL",
            PermissibleValue(
                text="GM-PER-MOL",
                meaning=QUDTUNIT["GM-PER-MOL"]))
        setattr(cls, "PER-WK",
            PermissibleValue(
                text="PER-WK",
                meaning=QUDTUNIT["PER-WK"]))
        setattr(cls, "PicoGM-PER-MilliL",
            PermissibleValue(
                text="PicoGM-PER-MilliL",
                meaning=QUDTUNIT["PicoGM-PER-MilliL"]))
        setattr(cls, "PER-DAY",
            PermissibleValue(
                text="PER-DAY",
                meaning=QUDTUNIT["PER-DAY"]))
        setattr(cls, "PicoGM-PER-MilliGM",
            PermissibleValue(
                text="PicoGM-PER-MilliGM",
                meaning=QUDTUNIT["PicoGM-PER-MilliGM"]))
        setattr(cls, "MicroGM-PER-L",
            PermissibleValue(
                text="MicroGM-PER-L",
                meaning=QUDTUNIT["MicroGM-PER-L"]))
        setattr(cls, "KiloGM-PER-M2",
            PermissibleValue(
                text="KiloGM-PER-M2",
                meaning=QUDTUNIT["KiloGM-PER-M2"]))
        setattr(cls, "MilliGM-PER-DeciL",
            PermissibleValue(
                text="MilliGM-PER-DeciL",
                meaning=QUDTUNIT["MilliGM-PER-DeciL"]))

class QudtQuantityKind(EnumDefinitionImpl):

    AmountOfSubstanceConcentration = PermissibleValue(
        text="AmountOfSubstanceConcentration",
        meaning=QUDTQK["AmountOfSubstanceConcentration"])
    AmountOfSubstancePerMass = PermissibleValue(
        text="AmountOfSubstancePerMass",
        meaning=QUDTQK["AmountOfSubstancePerMass"])
    Count = PermissibleValue(
        text="Count",
        meaning=QUDTQK["Count"])
    Dimensionless = PermissibleValue(
        text="Dimensionless",
        meaning=QUDTQK["Dimensionless"])
    DimensionlessRatio = PermissibleValue(
        text="DimensionlessRatio",
        meaning=QUDTQK["DimensionlessRatio"])
    Time = PermissibleValue(
        text="Time",
        meaning=QUDTQK["Time"])
    Frequency = PermissibleValue(
        text="Frequency",
        meaning=QUDTQK["Frequency"])
    Length = PermissibleValue(
        text="Length",
        meaning=QUDTQK["Length"])
    Mass = PermissibleValue(
        text="Mass",
        meaning=QUDTQK["Mass"])
    MassPerArea = PermissibleValue(
        text="MassPerArea",
        meaning=QUDTQK["MassPerArea"])
    MassConcentration = PermissibleValue(
        text="MassConcentration",
        meaning=QUDTQK["MassConcentration"])
    MassRatio = PermissibleValue(
        text="MassRatio",
        meaning=QUDTQK["MassRatio"])
    MolarMass = PermissibleValue(
        text="MolarMass",
        meaning=QUDTQK["MolarMass"])
    MolarRatio = PermissibleValue(
        text="MolarRatio",
        meaning=QUDTQK["MolarRatio"])
    NumberDensity = PermissibleValue(
        text="NumberDensity",
        meaning=QUDTQK["NumberDensity"])
    Volume = PermissibleValue(
        text="Volume",
        meaning=QUDTQK["Volume"])

    _defn = EnumDefinition(
        name="QudtQuantityKind",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=PEHTERMS.id, domain=None, range=URIRef)

slots.unique_name = Slot(uri=SCHEMA.alternateName, name="unique_name", curie=SCHEMA.curie('alternateName'),
                   model_uri=PEHTERMS.unique_name, domain=None, range=Optional[str])

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=PEHTERMS.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=PEHTERMS.description, domain=None, range=Optional[str])

slots.label = Slot(uri=SKOS.prefLabel, name="label", curie=SKOS.curie('prefLabel'),
                   model_uri=PEHTERMS.label, domain=None, range=Optional[str])

slots.remark = Slot(uri=SCHEMA.comment, name="remark", curie=SCHEMA.curie('comment'),
                   model_uri=PEHTERMS.remark, domain=None, range=Optional[str])

slots.orcid = Slot(uri=SCHEMA.identifier, name="orcid", curie=SCHEMA.curie('identifier'),
                   model_uri=PEHTERMS.orcid, domain=None, range=Optional[str])

slots.rorid = Slot(uri=SCHEMA.identifier, name="rorid", curie=SCHEMA.curie('identifier'),
                   model_uri=PEHTERMS.rorid, domain=None, range=Optional[str])

slots.alias = Slot(uri=PEHTERMS.alias, name="alias", curie=PEHTERMS.curie('alias'),
                   model_uri=PEHTERMS.alias, domain=None, range=Optional[str])

slots.aliases = Slot(uri=PEHTERMS.aliases, name="aliases", curie=PEHTERMS.curie('aliases'),
                   model_uri=PEHTERMS.aliases, domain=None, range=Optional[Union[str, list[str]]])

slots.context_aliases = Slot(uri=PEHTERMS.context_aliases, name="context_aliases", curie=PEHTERMS.curie('context_aliases'),
                   model_uri=PEHTERMS.context_aliases, domain=None, range=Optional[Union[Union[dict, ContextAlias], list[Union[dict, ContextAlias]]]])

slots.context = Slot(uri=PEHTERMS.context, name="context", curie=PEHTERMS.curie('context'),
                   model_uri=PEHTERMS.context, domain=None, range=Optional[Union[str, NamedThingId]])

slots.translations = Slot(uri=PEHTERMS.translations, name="translations", curie=PEHTERMS.curie('translations'),
                   model_uri=PEHTERMS.translations, domain=None, range=Optional[Union[Union[dict, Translation], list[Union[dict, Translation]]]])

slots.property_name = Slot(uri=SCHEMA.identifier, name="property_name", curie=SCHEMA.curie('identifier'),
                   model_uri=PEHTERMS.property_name, domain=None, range=Optional[str])

slots.language = Slot(uri=PEHTERMS.language, name="language", curie=PEHTERMS.curie('language'),
                   model_uri=PEHTERMS.language, domain=None, range=Optional[str])

slots.translated_value = Slot(uri=PEHTERMS.translated_value, name="translated_value", curie=PEHTERMS.curie('translated_value'),
                   model_uri=PEHTERMS.translated_value, domain=None, range=Optional[str])

slots.validation_history = Slot(uri=PEHTERMS.validation_history, name="validation_history", curie=PEHTERMS.curie('validation_history'),
                   model_uri=PEHTERMS.validation_history, domain=None, range=Optional[Union[Union[dict, ValidationHistoryRecord], list[Union[dict, ValidationHistoryRecord]]]])

slots.units = Slot(uri=PEHTERMS.units, name="units", curie=PEHTERMS.curie('units'),
                   model_uri=PEHTERMS.units, domain=None, range=Optional[Union[dict[Union[str, UnitId], Union[dict, Unit]], list[Union[dict, Unit]]]])

slots.same_unit_as = Slot(uri=PEHTERMS.same_unit_as, name="same_unit_as", curie=PEHTERMS.curie('same_unit_as'),
                   model_uri=PEHTERMS.same_unit_as, domain=None, range=Optional[Union[str, "QudtUnit"]])

slots.quantity_kind = Slot(uri=PEHTERMS.quantity_kind, name="quantity_kind", curie=PEHTERMS.curie('quantity_kind'),
                   model_uri=PEHTERMS.quantity_kind, domain=None, range=Optional[Union[str, "QudtQuantityKind"]])

slots.groupings = Slot(uri=PEHTERMS.groupings, name="groupings", curie=PEHTERMS.curie('groupings'),
                   model_uri=PEHTERMS.groupings, domain=None, range=Optional[Union[dict[Union[str, GroupingId], Union[dict, Grouping]], list[Union[dict, Grouping]]]])

slots.grouping_id_list = Slot(uri=PEHTERMS.grouping_id_list, name="grouping_id_list", curie=PEHTERMS.curie('grouping_id_list'),
                   model_uri=PEHTERMS.grouping_id_list, domain=None, range=Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]])

slots.parent_grouping_id_list = Slot(uri=SKOS.broader, name="parent_grouping_id_list", curie=SKOS.curie('broader'),
                   model_uri=PEHTERMS.parent_grouping_id_list, domain=None, range=Optional[Union[Union[str, GroupingId], list[Union[str, GroupingId]]]])

slots.biochemidentifiers = Slot(uri=PEHTERMS.biochemidentifiers, name="biochemidentifiers", curie=PEHTERMS.curie('biochemidentifiers'),
                   model_uri=PEHTERMS.biochemidentifiers, domain=None, range=Optional[Union[Union[dict, BioChemIdentifier], list[Union[dict, BioChemIdentifier]]]])

slots.biochementities = Slot(uri=PEHTERMS.biochementities, name="biochementities", curie=PEHTERMS.curie('biochementities'),
                   model_uri=PEHTERMS.biochementities, domain=None, range=Optional[Union[dict[Union[str, BioChemEntityId], Union[dict, BioChemEntity]], list[Union[dict, BioChemEntity]]]])

slots.indicators = Slot(uri=PEHTERMS.indicators, name="indicators", curie=PEHTERMS.curie('indicators'),
                   model_uri=PEHTERMS.indicators, domain=None, range=Optional[Union[dict[Union[str, IndicatorId], Union[dict, Indicator]], list[Union[dict, Indicator]]]])

slots.web_uri = Slot(uri=PEHTERMS.web_uri, name="web_uri", curie=PEHTERMS.curie('web_uri'),
                   model_uri=PEHTERMS.web_uri, domain=None, range=Optional[str])

slots.identifier_schema = Slot(uri=PEHTERMS.identifier_schema, name="identifier_schema", curie=PEHTERMS.curie('identifier_schema'),
                   model_uri=PEHTERMS.identifier_schema, domain=None, range=Optional[Union[str, BioChemIdentifierSchemaId]])

slots.identifier_code = Slot(uri=PEHTERMS.identifier_code, name="identifier_code", curie=PEHTERMS.curie('identifier_code'),
                   model_uri=PEHTERMS.identifier_code, domain=None, range=Optional[str])

slots.current_validation_status = Slot(uri=PEHTERMS.current_validation_status, name="current_validation_status", curie=PEHTERMS.curie('current_validation_status'),
                   model_uri=PEHTERMS.current_validation_status, domain=None, range=Optional[Union[str, "ValidationStatus"]])

slots.validation_datetime = Slot(uri=PEHTERMS.validation_datetime, name="validation_datetime", curie=PEHTERMS.curie('validation_datetime'),
                   model_uri=PEHTERMS.validation_datetime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.validation_status = Slot(uri=PEHTERMS.validation_status, name="validation_status", curie=PEHTERMS.curie('validation_status'),
                   model_uri=PEHTERMS.validation_status, domain=None, range=Optional[Union[str, "ValidationStatus"]])

slots.validation_actor = Slot(uri=PEHTERMS.validation_actor, name="validation_actor", curie=PEHTERMS.curie('validation_actor'),
                   model_uri=PEHTERMS.validation_actor, domain=None, range=Optional[str])

slots.validation_institute = Slot(uri=PEHTERMS.validation_institute, name="validation_institute", curie=PEHTERMS.curie('validation_institute'),
                   model_uri=PEHTERMS.validation_institute, domain=None, range=Optional[str])

slots.validation_remark = Slot(uri=PEHTERMS.validation_remark, name="validation_remark", curie=PEHTERMS.curie('validation_remark'),
                   model_uri=PEHTERMS.validation_remark, domain=None, range=Optional[str])

slots.sort_order = Slot(uri=PEHTERMS.sort_order, name="sort_order", curie=PEHTERMS.curie('sort_order'),
                   model_uri=PEHTERMS.sort_order, domain=None, range=Optional[Decimal])

slots.aggregation_target = Slot(uri=PEHTERMS.aggregation_target, name="aggregation_target", curie=PEHTERMS.curie('aggregation_target'),
                   model_uri=PEHTERMS.aggregation_target, domain=None, range=Optional[Union[bool, Bool]])

slots.parent_matrix = Slot(uri=SKOS.broader, name="parent_matrix", curie=SKOS.curie('broader'),
                   model_uri=PEHTERMS.parent_matrix, domain=None, range=Optional[Union[str, MatrixId]])

slots.secondary_parent_matrix_id_list = Slot(uri=PEHTERMS.secondary_parent_matrix_id_list, name="secondary_parent_matrix_id_list", curie=PEHTERMS.curie('secondary_parent_matrix_id_list'),
                   model_uri=PEHTERMS.secondary_parent_matrix_id_list, domain=None, range=Optional[Union[Union[str, MatrixId], list[Union[str, MatrixId]]]])

slots.indicator_type = Slot(uri=PEHTERMS.indicator_type, name="indicator_type", curie=PEHTERMS.curie('indicator_type'),
                   model_uri=PEHTERMS.indicator_type, domain=None, range=Optional[Union[str, "IndicatorType"]])

slots.varname = Slot(uri=PEHTERMS.varname, name="varname", curie=PEHTERMS.curie('varname'),
                   model_uri=PEHTERMS.varname, domain=None, range=Optional[str])

slots.property = Slot(uri=PEHTERMS.property, name="property", curie=PEHTERMS.curie('property'),
                   model_uri=PEHTERMS.property, domain=None, range=Optional[str])

slots.matrices = Slot(uri=PEHTERMS.matrices, name="matrices", curie=PEHTERMS.curie('matrices'),
                   model_uri=PEHTERMS.matrices, domain=None, range=Optional[Union[dict[Union[str, MatrixId], Union[dict, Matrix]], list[Union[dict, Matrix]]]])

slots.matrix = Slot(uri=PEHTERMS.matrix, name="matrix", curie=PEHTERMS.curie('matrix'),
                   model_uri=PEHTERMS.matrix, domain=None, range=Optional[Union[str, MatrixId]])

slots.constraints = Slot(uri=PEHTERMS.constraints, name="constraints", curie=PEHTERMS.curie('constraints'),
                   model_uri=PEHTERMS.constraints, domain=None, range=Optional[Union[str, list[str]]])

slots.default_observation_result_type = Slot(uri=PEHTERMS.default_observation_result_type, name="default_observation_result_type", curie=PEHTERMS.curie('default_observation_result_type'),
                   model_uri=PEHTERMS.default_observation_result_type, domain=None, range=Optional[Union[str, "ObservationResultType"]])

slots.relevant_observable_entity_types = Slot(uri=PEHTERMS.relevant_observable_entity_types, name="relevant_observable_entity_types", curie=PEHTERMS.curie('relevant_observable_entity_types'),
                   model_uri=PEHTERMS.relevant_observable_entity_types, domain=None, range=Optional[Union[Union[str, "ObservableEntityType"], list[Union[str, "ObservableEntityType"]]]])

slots.molweight_grampermol = Slot(uri=PEHTERMS.molweight_grampermol, name="molweight_grampermol", curie=PEHTERMS.curie('molweight_grampermol'),
                   model_uri=PEHTERMS.molweight_grampermol, domain=None, range=Optional[Decimal])

slots.biochementity_links = Slot(uri=PEHTERMS.biochementity_links, name="biochementity_links", curie=PEHTERMS.curie('biochementity_links'),
                   model_uri=PEHTERMS.biochementity_links, domain=None, range=Optional[Union[Union[dict, BioChemEntityLink], list[Union[dict, BioChemEntityLink]]]])

slots.biochementity_linktype = Slot(uri=PEHTERMS.biochementity_linktype, name="biochementity_linktype", curie=PEHTERMS.curie('biochementity_linktype'),
                   model_uri=PEHTERMS.biochementity_linktype, domain=None, range=Optional[Union[str, "BioChemEntityLinkType"]])

slots.biochementity = Slot(uri=PEHTERMS.biochementity, name="biochementity", curie=PEHTERMS.curie('biochementity'),
                   model_uri=PEHTERMS.biochementity, domain=None, range=Optional[Union[str, BioChemEntityId]])

slots.categorical = Slot(uri=PEHTERMS.categorical, name="categorical", curie=PEHTERMS.curie('categorical'),
                   model_uri=PEHTERMS.categorical, domain=None, range=Optional[Union[bool, Bool]])

slots.multivalued = Slot(uri=PEHTERMS.multivalued, name="multivalued", curie=PEHTERMS.curie('multivalued'),
                   model_uri=PEHTERMS.multivalued, domain=None, range=Optional[Union[bool, Bool]])

slots.abstract = Slot(uri=PEHTERMS.abstract, name="abstract", curie=PEHTERMS.curie('abstract'),
                   model_uri=PEHTERMS.abstract, domain=None, range=Optional[Union[bool, Bool]])

slots.value_type = Slot(uri=PEHTERMS.value_type, name="value_type", curie=PEHTERMS.curie('value_type'),
                   model_uri=PEHTERMS.value_type, domain=None, range=Optional[str])

slots.value_metadata = Slot(uri=PEHTERMS.value_metadata, name="value_metadata", curie=PEHTERMS.curie('value_metadata'),
                   model_uri=PEHTERMS.value_metadata, domain=None, range=Optional[Union[Union[dict, ObservablePropertyMetadataElement], list[Union[dict, ObservablePropertyMetadataElement]]]])

slots.value_options = Slot(uri=PEHTERMS.value_options, name="value_options", curie=PEHTERMS.curie('value_options'),
                   model_uri=PEHTERMS.value_options, domain=None, range=Optional[Union[Union[dict, ObservablePropertyValueOption], list[Union[dict, ObservablePropertyValueOption]]]])

slots.default_required = Slot(uri=PEHTERMS.default_required, name="default_required", curie=PEHTERMS.curie('default_required'),
                   model_uri=PEHTERMS.default_required, domain=None, range=Optional[Union[bool, Bool]])

slots.default_zeroallowed = Slot(uri=PEHTERMS.default_zeroallowed, name="default_zeroallowed", curie=PEHTERMS.curie('default_zeroallowed'),
                   model_uri=PEHTERMS.default_zeroallowed, domain=None, range=Optional[Union[bool, Bool]])

slots.default_significantdecimals = Slot(uri=PEHTERMS.default_significantdecimals, name="default_significantdecimals", curie=PEHTERMS.curie('default_significantdecimals'),
                   model_uri=PEHTERMS.default_significantdecimals, domain=None, range=Optional[int])

slots.default_unit = Slot(uri=PEHTERMS.default_unit, name="default_unit", curie=PEHTERMS.curie('default_unit'),
                   model_uri=PEHTERMS.default_unit, domain=None, range=Optional[str])

slots.default_unit_label = Slot(uri=PEHTERMS.default_unit_label, name="default_unit_label", curie=PEHTERMS.curie('default_unit_label'),
                   model_uri=PEHTERMS.default_unit_label, domain=None, range=Optional[str])

slots.default_immutable = Slot(uri=PEHTERMS.default_immutable, name="default_immutable", curie=PEHTERMS.curie('default_immutable'),
                   model_uri=PEHTERMS.default_immutable, domain=None, range=Optional[Union[bool, Bool]])

slots.relevant_observation_types = Slot(uri=PEHTERMS.relevant_observation_types, name="relevant_observation_types", curie=PEHTERMS.curie('relevant_observation_types'),
                   model_uri=PEHTERMS.relevant_observation_types, domain=None, range=Optional[Union[Union[str, "ObservationType"], list[Union[str, "ObservationType"]]]])

slots.indicator = Slot(uri=PEHTERMS.indicator, name="indicator", curie=PEHTERMS.curie('indicator'),
                   model_uri=PEHTERMS.indicator, domain=None, range=Optional[Union[str, IndicatorId]])

slots.calculation_designs = Slot(uri=PEHTERMS.calculation_designs, name="calculation_designs", curie=PEHTERMS.curie('calculation_designs'),
                   model_uri=PEHTERMS.calculation_designs, domain=None, range=Optional[Union[Union[dict, CalculationDesign], list[Union[dict, CalculationDesign]]]])

slots.calculation_name = Slot(uri=PEHTERMS.calculation_name, name="calculation_name", curie=PEHTERMS.curie('calculation_name'),
                   model_uri=PEHTERMS.calculation_name, domain=None, range=Optional[str])

slots.conditional = Slot(uri=PEHTERMS.conditional, name="conditional", curie=PEHTERMS.curie('conditional'),
                   model_uri=PEHTERMS.conditional, domain=None, range=Optional[str])

slots.calculation_implementation_as_json = Slot(uri=PEHTERMS.calculation_implementation_as_json, name="calculation_implementation_as_json", curie=PEHTERMS.curie('calculation_implementation_as_json'),
                   model_uri=PEHTERMS.calculation_implementation_as_json, domain=None, range=Optional[str])

slots.calculation_implementation = Slot(uri=PEHTERMS.calculation_implementation, name="calculation_implementation", curie=PEHTERMS.curie('calculation_implementation'),
                   model_uri=PEHTERMS.calculation_implementation, domain=None, range=Optional[Union[dict, CalculationImplementation]])

slots.function_name = Slot(uri=PEHTERMS.function_name, name="function_name", curie=PEHTERMS.curie('function_name'),
                   model_uri=PEHTERMS.function_name, domain=None, range=Optional[str])

slots.function_args = Slot(uri=PEHTERMS.function_args, name="function_args", curie=PEHTERMS.curie('function_args'),
                   model_uri=PEHTERMS.function_args, domain=None, range=Optional[Union[Union[dict, CalculationArgument], list[Union[dict, CalculationArgument]]]])

slots.function_kwargs = Slot(uri=PEHTERMS.function_kwargs, name="function_kwargs", curie=PEHTERMS.curie('function_kwargs'),
                   model_uri=PEHTERMS.function_kwargs, domain=None, range=Optional[Union[Union[dict, CalculationKeywordArgument], list[Union[dict, CalculationKeywordArgument]]]])

slots.function_results = Slot(uri=PEHTERMS.function_results, name="function_results", curie=PEHTERMS.curie('function_results'),
                   model_uri=PEHTERMS.function_results, domain=None, range=Optional[Union[Union[dict, CalculationResult], list[Union[dict, CalculationResult]]]])

slots.validation_designs = Slot(uri=PEHTERMS.validation_designs, name="validation_designs", curie=PEHTERMS.curie('validation_designs'),
                   model_uri=PEHTERMS.validation_designs, domain=None, range=Optional[Union[Union[dict, ValidationDesign], list[Union[dict, ValidationDesign]]]])

slots.validation_name = Slot(uri=PEHTERMS.validation_name, name="validation_name", curie=PEHTERMS.curie('validation_name'),
                   model_uri=PEHTERMS.validation_name, domain=None, range=Optional[str])

slots.validation_expression = Slot(uri=PEHTERMS.validation_expression, name="validation_expression", curie=PEHTERMS.curie('validation_expression'),
                   model_uri=PEHTERMS.validation_expression, domain=None, range=Optional[Union[dict, ValidationExpression]])

slots.validation_condition_expression = Slot(uri=PEHTERMS.validation_condition_expression, name="validation_condition_expression", curie=PEHTERMS.curie('validation_condition_expression'),
                   model_uri=PEHTERMS.validation_condition_expression, domain=None, range=Optional[Union[dict, ValidationExpression]])

slots.validation_error_level = Slot(uri=PEHTERMS.validation_error_level, name="validation_error_level", curie=PEHTERMS.curie('validation_error_level'),
                   model_uri=PEHTERMS.validation_error_level, domain=None, range=Optional[Union[str, "ValidationErrorLevel"]])

slots.validation_error_message_template = Slot(uri=PEHTERMS.validation_error_message_template, name="validation_error_message_template", curie=PEHTERMS.curie('validation_error_message_template'),
                   model_uri=PEHTERMS.validation_error_message_template, domain=None, range=Optional[str])

slots.validation_subject_source_paths = Slot(uri=PEHTERMS.validation_subject_source_paths, name="validation_subject_source_paths", curie=PEHTERMS.curie('validation_subject_source_paths'),
                   model_uri=PEHTERMS.validation_subject_source_paths, domain=None, range=Optional[Union[str, list[str]]])

slots.validation_command = Slot(uri=PEHTERMS.validation_command, name="validation_command", curie=PEHTERMS.curie('validation_command'),
                   model_uri=PEHTERMS.validation_command, domain=None, range=Optional[Union[str, "ValidationCommand"]])

slots.validation_arg_values = Slot(uri=PEHTERMS.validation_arg_values, name="validation_arg_values", curie=PEHTERMS.curie('validation_arg_values'),
                   model_uri=PEHTERMS.validation_arg_values, domain=None, range=Optional[Union[str, list[str]]])

slots.validation_arg_source_paths = Slot(uri=PEHTERMS.validation_arg_source_paths, name="validation_arg_source_paths", curie=PEHTERMS.curie('validation_arg_source_paths'),
                   model_uri=PEHTERMS.validation_arg_source_paths, domain=None, range=Optional[Union[str, list[str]]])

slots.validation_arg_expressions = Slot(uri=PEHTERMS.validation_arg_expressions, name="validation_arg_expressions", curie=PEHTERMS.curie('validation_arg_expressions'),
                   model_uri=PEHTERMS.validation_arg_expressions, domain=None, range=Optional[Union[Union[dict, ValidationExpression], list[Union[dict, ValidationExpression]]]])

slots.process_state = Slot(uri=PEHTERMS.process_state, name="process_state", curie=PEHTERMS.curie('process_state'),
                   model_uri=PEHTERMS.process_state, domain=None, range=Optional[str])

slots.imputation_state = Slot(uri=PEHTERMS.imputation_state, name="imputation_state", curie=PEHTERMS.curie('imputation_state'),
                   model_uri=PEHTERMS.imputation_state, domain=None, range=Optional[str])

slots.mapping_name = Slot(uri=PEHTERMS.mapping_name, name="mapping_name", curie=PEHTERMS.curie('mapping_name'),
                   model_uri=PEHTERMS.mapping_name, domain=None, range=Optional[str])

slots.source_path = Slot(uri=PEHTERMS.source_path, name="source_path", curie=PEHTERMS.curie('source_path'),
                   model_uri=PEHTERMS.source_path, domain=None, range=Optional[str])

slots.destination_path = Slot(uri=PEHTERMS.destination_path, name="destination_path", curie=PEHTERMS.curie('destination_path'),
                   model_uri=PEHTERMS.destination_path, domain=None, range=Optional[str])

slots.round_decimals = Slot(uri=PEHTERMS.round_decimals, name="round_decimals", curie=PEHTERMS.curie('round_decimals'),
                   model_uri=PEHTERMS.round_decimals, domain=None, range=Optional[int])

slots.scale_factor = Slot(uri=PEHTERMS.scale_factor, name="scale_factor", curie=PEHTERMS.curie('scale_factor'),
                   model_uri=PEHTERMS.scale_factor, domain=None, range=Optional[Decimal])

slots.field = Slot(uri=PEHTERMS.field, name="field", curie=PEHTERMS.curie('field'),
                   model_uri=PEHTERMS.field, domain=None, range=Optional[Union[str, ObservablePropertyMetadataFieldId]])

slots.key = Slot(uri=PEHTERMS.key, name="key", curie=PEHTERMS.curie('key'),
                   model_uri=PEHTERMS.key, domain=None, range=Optional[str])

slots.value = Slot(uri=PEHTERMS.value, name="value", curie=PEHTERMS.curie('value'),
                   model_uri=PEHTERMS.value, domain=None, range=Optional[str])

slots.metadata_fields = Slot(uri=PEHTERMS.metadata_fields, name="metadata_fields", curie=PEHTERMS.curie('metadata_fields'),
                   model_uri=PEHTERMS.metadata_fields, domain=None, range=Optional[Union[dict[Union[str, ObservablePropertyMetadataFieldId], Union[dict, ObservablePropertyMetadataField]], list[Union[dict, ObservablePropertyMetadataField]]]])

slots.stakeholders = Slot(uri=PEHTERMS.stakeholders, name="stakeholders", curie=PEHTERMS.curie('stakeholders'),
                   model_uri=PEHTERMS.stakeholders, domain=None, range=Optional[Union[dict[Union[str, StakeholderId], Union[dict, Stakeholder]], list[Union[dict, Stakeholder]]]])

slots.project_id_list = Slot(uri=PEHTERMS.project_id_list, name="project_id_list", curie=PEHTERMS.curie('project_id_list'),
                   model_uri=PEHTERMS.project_id_list, domain=None, range=Optional[Union[Union[str, ProjectId], list[Union[str, ProjectId]]]])

slots.study_id_list = Slot(uri=PEHTERMS.study_id_list, name="study_id_list", curie=PEHTERMS.curie('study_id_list'),
                   model_uri=PEHTERMS.study_id_list, domain=None, range=Optional[Union[Union[str, StudyId], list[Union[str, StudyId]]]])

slots.observation_group_id_list = Slot(uri=PEHTERMS.observation_group_id_list, name="observation_group_id_list", curie=PEHTERMS.curie('observation_group_id_list'),
                   model_uri=PEHTERMS.observation_group_id_list, domain=None, range=Optional[Union[Union[str, ObservationGroupId], list[Union[str, ObservationGroupId]]]])

slots.observation_id_list = Slot(uri=PEHTERMS.observation_id_list, name="observation_id_list", curie=PEHTERMS.curie('observation_id_list'),
                   model_uri=PEHTERMS.observation_id_list, domain=None, range=Optional[Union[Union[str, ObservationId], list[Union[str, ObservationId]]]])

slots.member_id_list = Slot(uri=PEHTERMS.member_id_list, name="member_id_list", curie=PEHTERMS.curie('member_id_list'),
                   model_uri=PEHTERMS.member_id_list, domain=None, range=Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]])

slots.sample_id_list = Slot(uri=PEHTERMS.sample_id_list, name="sample_id_list", curie=PEHTERMS.curie('sample_id_list'),
                   model_uri=PEHTERMS.sample_id_list, domain=None, range=Optional[Union[Union[str, SampleId], list[Union[str, SampleId]]]])

slots.projects = Slot(uri=PEHTERMS.projects, name="projects", curie=PEHTERMS.curie('projects'),
                   model_uri=PEHTERMS.projects, domain=None, range=Optional[Union[dict[Union[str, ProjectId], Union[dict, Project]], list[Union[dict, Project]]]])

slots.geographic_scope = Slot(uri=PEHTERMS.geographic_scope, name="geographic_scope", curie=PEHTERMS.curie('geographic_scope'),
                   model_uri=PEHTERMS.geographic_scope, domain=None, range=Optional[str])

slots.project = Slot(uri=SCHEMA.ResearchProject, name="project", curie=SCHEMA.curie('ResearchProject'),
                   model_uri=PEHTERMS.project, domain=None, range=Optional[str])

slots.default_language = Slot(uri=PEHTERMS.default_language, name="default_language", curie=PEHTERMS.curie('default_language'),
                   model_uri=PEHTERMS.default_language, domain=None, range=Optional[str])

slots.stakeholder = Slot(uri=PEHTERMS.stakeholder, name="stakeholder", curie=PEHTERMS.curie('stakeholder'),
                   model_uri=PEHTERMS.stakeholder, domain=None, range=Optional[Union[str, StakeholderId]])

slots.project_stakeholders = Slot(uri=PEHTERMS.project_stakeholders, name="project_stakeholders", curie=PEHTERMS.curie('project_stakeholders'),
                   model_uri=PEHTERMS.project_stakeholders, domain=None, range=Optional[Union[Union[dict, ProjectStakeholder], list[Union[dict, ProjectStakeholder]]]])

slots.studies = Slot(uri=PEHTERMS.studies, name="studies", curie=PEHTERMS.curie('studies'),
                   model_uri=PEHTERMS.studies, domain=None, range=Optional[Union[dict[Union[str, StudyId], Union[dict, Study]], list[Union[dict, Study]]]])

slots.project_roles = Slot(uri=PEHTERMS.project_roles, name="project_roles", curie=PEHTERMS.curie('project_roles'),
                   model_uri=PEHTERMS.project_roles, domain=None, range=Optional[Union[Union[str, "ProjectRole"], list[Union[str, "ProjectRole"]]]])

slots.study_stakeholders = Slot(uri=PEHTERMS.study_stakeholders, name="study_stakeholders", curie=PEHTERMS.curie('study_stakeholders'),
                   model_uri=PEHTERMS.study_stakeholders, domain=None, range=Optional[Union[Union[dict, StudyStakeholder], list[Union[dict, StudyStakeholder]]]])

slots.research_population_type = Slot(uri=PEHTERMS.research_population_type, name="research_population_type", curie=PEHTERMS.curie('research_population_type'),
                   model_uri=PEHTERMS.research_population_type, domain=None, range=Optional[Union[str, "ResearchPopulationType"]])

slots.study_roles = Slot(uri=PEHTERMS.study_roles, name="study_roles", curie=PEHTERMS.curie('study_roles'),
                   model_uri=PEHTERMS.study_roles, domain=None, range=Optional[Union[Union[str, "StudyRole"], list[Union[str, "StudyRole"]]]])

slots.observation_groups = Slot(uri=PEHTERMS.observation_groups, name="observation_groups", curie=PEHTERMS.curie('observation_groups'),
                   model_uri=PEHTERMS.observation_groups, domain=None, range=Optional[Union[dict[Union[str, ObservationGroupId], Union[dict, ObservationGroup]], list[Union[dict, ObservationGroup]]]])

slots.observations = Slot(uri=PEHTERMS.observations, name="observations", curie=PEHTERMS.curie('observations'),
                   model_uri=PEHTERMS.observations, domain=None, range=Optional[Union[dict[Union[str, ObservationId], Union[dict, Observation]], list[Union[dict, Observation]]]])

slots.linktype = Slot(uri=PEHTERMS.linktype, name="linktype", curie=PEHTERMS.curie('linktype'),
                   model_uri=PEHTERMS.linktype, domain=None, range=Optional[Union[str, "LinkType"]])

slots.physical_entities = Slot(uri=PEHTERMS.physical_entities, name="physical_entities", curie=PEHTERMS.curie('physical_entities'),
                   model_uri=PEHTERMS.physical_entities, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.physical_entity_links = Slot(uri=PEHTERMS.physical_entity_links, name="physical_entity_links", curie=PEHTERMS.curie('physical_entity_links'),
                   model_uri=PEHTERMS.physical_entity_links, domain=None, range=Optional[Union[Union[dict, PhysicalEntityLink], list[Union[dict, PhysicalEntityLink]]]])

slots.physical_entity = Slot(uri=PEHTERMS.physical_entity, name="physical_entity", curie=PEHTERMS.curie('physical_entity'),
                   model_uri=PEHTERMS.physical_entity, domain=None, range=Optional[Union[str, PhysicalEntityId]])

slots.study_entities = Slot(uri=PEHTERMS.study_entities, name="study_entities", curie=PEHTERMS.curie('study_entities'),
                   model_uri=PEHTERMS.study_entities, domain=None, range=Optional[Union[dict[Union[str, StudyEntityId], Union[dict, StudyEntity]], list[Union[dict, StudyEntity]]]])

slots.study_entity_id_list = Slot(uri=PEHTERMS.study_entity_id_list, name="study_entity_id_list", curie=PEHTERMS.curie('study_entity_id_list'),
                   model_uri=PEHTERMS.study_entity_id_list, domain=None, range=Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]])

slots.study_entity_links = Slot(uri=PEHTERMS.study_entity_links, name="study_entity_links", curie=PEHTERMS.curie('study_entity_links'),
                   model_uri=PEHTERMS.study_entity_links, domain=None, range=Optional[Union[Union[dict, StudyEntityLink], list[Union[dict, StudyEntityLink]]]])

slots.study_entity = Slot(uri=PEHTERMS.study_entity, name="study_entity", curie=PEHTERMS.curie('study_entity'),
                   model_uri=PEHTERMS.study_entity, domain=None, range=Optional[Union[str, StudyEntityId]])

slots.recruited_in_project = Slot(uri=PEHTERMS.recruited_in_project, name="recruited_in_project", curie=PEHTERMS.curie('recruited_in_project'),
                   model_uri=PEHTERMS.recruited_in_project, domain=None, range=Optional[Union[str, ProjectId]])

slots.sampled_in_project = Slot(uri=PEHTERMS.sampled_in_project, name="sampled_in_project", curie=PEHTERMS.curie('sampled_in_project'),
                   model_uri=PEHTERMS.sampled_in_project, domain=None, range=Optional[Union[str, ProjectId]])

slots.physical_label = Slot(uri=PEHTERMS.physical_label, name="physical_label", curie=PEHTERMS.curie('physical_label'),
                   model_uri=PEHTERMS.physical_label, domain=None, range=Optional[str])

slots.location = Slot(uri=PEHTERMS.location, name="location", curie=PEHTERMS.curie('location'),
                   model_uri=PEHTERMS.location, domain=None, range=Optional[str])

slots.observation_type = Slot(uri=PEHTERMS.observation_type, name="observation_type", curie=PEHTERMS.curie('observation_type'),
                   model_uri=PEHTERMS.observation_type, domain=None, range=Optional[Union[str, "ObservationType"]])

slots.observation_design = Slot(uri=PEHTERMS.observation_design, name="observation_design", curie=PEHTERMS.curie('observation_design'),
                   model_uri=PEHTERMS.observation_design, domain=None, range=Optional[Union[dict, ObservationDesign]])

slots.observable_entity_property_sets = Slot(uri=PEHTERMS.observable_entity_property_sets, name="observable_entity_property_sets", curie=PEHTERMS.curie('observable_entity_property_sets'),
                   model_uri=PEHTERMS.observable_entity_property_sets, domain=None, range=Optional[Union[Union[dict, ObservableEntityPropertySet], list[Union[dict, ObservableEntityPropertySet]]]])

slots.observation_result_type = Slot(uri=PEHTERMS.observation_result_type, name="observation_result_type", curie=PEHTERMS.curie('observation_result_type'),
                   model_uri=PEHTERMS.observation_result_type, domain=None, range=Optional[Union[str, "ObservationResultType"]])

slots.observation_results = Slot(uri=PEHTERMS.observation_results, name="observation_results", curie=PEHTERMS.curie('observation_results'),
                   model_uri=PEHTERMS.observation_results, domain=None, range=Optional[Union[dict[Union[str, ObservationResultId], Union[dict, ObservationResult]], list[Union[dict, ObservationResult]]]])

slots.observation_result_id_list = Slot(uri=PEHTERMS.observation_result_id_list, name="observation_result_id_list", curie=PEHTERMS.curie('observation_result_id_list'),
                   model_uri=PEHTERMS.observation_result_id_list, domain=None, range=Optional[Union[Union[str, ObservationResultId], list[Union[str, ObservationResultId]]]])

slots.observable_entity_type = Slot(uri=PEHTERMS.observable_entity_type, name="observable_entity_type", curie=PEHTERMS.curie('observable_entity_type'),
                   model_uri=PEHTERMS.observable_entity_type, domain=None, range=Optional[Union[str, "ObservableEntityType"]])

slots.observable_entity_types = Slot(uri=PEHTERMS.observable_entity_types, name="observable_entity_types", curie=PEHTERMS.curie('observable_entity_types'),
                   model_uri=PEHTERMS.observable_entity_types, domain=None, range=Optional[Union[Union[str, "ObservableEntityType"], list[Union[str, "ObservableEntityType"]]]])

slots.observable_entity_id_list = Slot(uri=PEHTERMS.observable_entity_id_list, name="observable_entity_id_list", curie=PEHTERMS.curie('observable_entity_id_list'),
                   model_uri=PEHTERMS.observable_entity_id_list, domain=None, range=Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]])

slots.observable_entities = Slot(uri=PEHTERMS.observable_entities, name="observable_entities", curie=PEHTERMS.curie('observable_entities'),
                   model_uri=PEHTERMS.observable_entities, domain=None, range=Optional[Union[dict[Union[str, StudyEntityId], Union[dict, StudyEntity]], list[Union[dict, StudyEntity]]]])

slots.observable_entity = Slot(uri=PEHTERMS.observable_entity, name="observable_entity", curie=PEHTERMS.curie('observable_entity'),
                   model_uri=PEHTERMS.observable_entity, domain=None, range=Optional[Union[str, StudyEntityId]])

slots.identifying_observable_property_id_list = Slot(uri=PEHTERMS.identifying_observable_property_id_list, name="identifying_observable_property_id_list", curie=PEHTERMS.curie('identifying_observable_property_id_list'),
                   model_uri=PEHTERMS.identifying_observable_property_id_list, domain=None, range=Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]])

slots.required_observable_property_id_list = Slot(uri=PEHTERMS.required_observable_property_id_list, name="required_observable_property_id_list", curie=PEHTERMS.curie('required_observable_property_id_list'),
                   model_uri=PEHTERMS.required_observable_property_id_list, domain=None, range=Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]])

slots.optional_observable_property_id_list = Slot(uri=PEHTERMS.optional_observable_property_id_list, name="optional_observable_property_id_list", curie=PEHTERMS.curie('optional_observable_property_id_list'),
                   model_uri=PEHTERMS.optional_observable_property_id_list, domain=None, range=Optional[Union[Union[str, ObservablePropertyId], list[Union[str, ObservablePropertyId]]]])

slots.observable_properties = Slot(uri=PEHTERMS.observable_properties, name="observable_properties", curie=PEHTERMS.curie('observable_properties'),
                   model_uri=PEHTERMS.observable_properties, domain=None, range=Optional[Union[dict[Union[str, ObservablePropertyId], Union[dict, ObservableProperty]], list[Union[dict, ObservableProperty]]]])

slots.observable_property = Slot(uri=PEHTERMS.observable_property, name="observable_property", curie=PEHTERMS.curie('observable_property'),
                   model_uri=PEHTERMS.observable_property, domain=None, range=Optional[Union[str, ObservablePropertyId]])

slots.observed_values = Slot(uri=PEHTERMS.observed_values, name="observed_values", curie=PEHTERMS.curie('observed_values'),
                   model_uri=PEHTERMS.observed_values, domain=None, range=Optional[Union[Union[dict, ObservedValue], list[Union[dict, ObservedValue]]]])

slots.unit = Slot(uri=PEHTERMS.unit, name="unit", curie=PEHTERMS.curie('unit'),
                   model_uri=PEHTERMS.unit, domain=None, range=Optional[Union[str, UnitId]])

slots.raw_value = Slot(uri=PEHTERMS.raw_value, name="raw_value", curie=PEHTERMS.curie('raw_value'),
                   model_uri=PEHTERMS.raw_value, domain=None, range=Optional[str])

slots.raw_unit = Slot(uri=PEHTERMS.raw_unit, name="raw_unit", curie=PEHTERMS.curie('raw_unit'),
                   model_uri=PEHTERMS.raw_unit, domain=None, range=Optional[str])

slots.imputed_value = Slot(uri=PEHTERMS.imputed_value, name="imputed_value", curie=PEHTERMS.curie('imputed_value'),
                   model_uri=PEHTERMS.imputed_value, domain=None, range=Optional[str])

slots.imputed_unit = Slot(uri=PEHTERMS.imputed_unit, name="imputed_unit", curie=PEHTERMS.curie('imputed_unit'),
                   model_uri=PEHTERMS.imputed_unit, domain=None, range=Optional[str])

slots.normalised_value = Slot(uri=PEHTERMS.normalised_value, name="normalised_value", curie=PEHTERMS.curie('normalised_value'),
                   model_uri=PEHTERMS.normalised_value, domain=None, range=Optional[str])

slots.normalised_unit = Slot(uri=PEHTERMS.normalised_unit, name="normalised_unit", curie=PEHTERMS.curie('normalised_unit'),
                   model_uri=PEHTERMS.normalised_unit, domain=None, range=Optional[str])

slots.value_as_string = Slot(uri=PEHTERMS.value_as_string, name="value_as_string", curie=PEHTERMS.curie('value_as_string'),
                   model_uri=PEHTERMS.value_as_string, domain=None, range=Optional[str])

slots.quality_data = Slot(uri=PEHTERMS.quality_data, name="quality_data", curie=PEHTERMS.curie('quality_data'),
                   model_uri=PEHTERMS.quality_data, domain=None, range=Optional[Union[Union[dict, QualityData], list[Union[dict, QualityData]]]])

slots.quality_context_key = Slot(uri=PEHTERMS.quality_context_key, name="quality_context_key", curie=PEHTERMS.curie('quality_context_key'),
                   model_uri=PEHTERMS.quality_context_key, domain=None, range=Optional[str])

slots.quality_value = Slot(uri=PEHTERMS.quality_value, name="quality_value", curie=PEHTERMS.curie('quality_value'),
                   model_uri=PEHTERMS.quality_value, domain=None, range=Optional[str])

slots.provenance_data = Slot(uri=PEHTERMS.provenance_data, name="provenance_data", curie=PEHTERMS.curie('provenance_data'),
                   model_uri=PEHTERMS.provenance_data, domain=None, range=Optional[Union[Union[dict, ProvenanceData], list[Union[dict, ProvenanceData]]]])

slots.provenance_context_key = Slot(uri=PEHTERMS.provenance_context_key, name="provenance_context_key", curie=PEHTERMS.curie('provenance_context_key'),
                   model_uri=PEHTERMS.provenance_context_key, domain=None, range=Optional[str])

slots.provenance_value = Slot(uri=PEHTERMS.provenance_value, name="provenance_value", curie=PEHTERMS.curie('provenance_value'),
                   model_uri=PEHTERMS.provenance_value, domain=None, range=Optional[str])

slots.data_requests = Slot(uri=PEHTERMS.data_requests, name="data_requests", curie=PEHTERMS.curie('data_requests'),
                   model_uri=PEHTERMS.data_requests, domain=None, range=Optional[Union[dict[Union[str, DataRequestId], Union[dict, DataRequest]], list[Union[dict, DataRequest]]]])

slots.layouts = Slot(uri=PEHTERMS.layouts, name="layouts", curie=PEHTERMS.curie('layouts'),
                   model_uri=PEHTERMS.layouts, domain=None, range=Optional[Union[dict[Union[str, DataLayoutId], Union[dict, DataLayout]], list[Union[dict, DataLayout]]]])

slots.sections = Slot(uri=PEHTERMS.sections, name="sections", curie=PEHTERMS.curie('sections'),
                   model_uri=PEHTERMS.sections, domain=None, range=Optional[Union[dict[Union[str, DataLayoutSectionId], Union[dict, DataLayoutSection]], list[Union[dict, DataLayoutSection]]]])

slots.section_type = Slot(uri=PEHTERMS.section_type, name="section_type", curie=PEHTERMS.curie('section_type'),
                   model_uri=PEHTERMS.section_type, domain=None, range=Optional[Union[str, "DataLayoutSectionType"]])

slots.observable_entity_grouping_id_list = Slot(uri=PEHTERMS.observable_entity_grouping_id_list, name="observable_entity_grouping_id_list", curie=PEHTERMS.curie('observable_entity_grouping_id_list'),
                   model_uri=PEHTERMS.observable_entity_grouping_id_list, domain=None, range=Optional[Union[Union[str, StudyEntityId], list[Union[str, StudyEntityId]]]])

slots.elements = Slot(uri=PEHTERMS.elements, name="elements", curie=PEHTERMS.curie('elements'),
                   model_uri=PEHTERMS.elements, domain=None, range=Optional[Union[Union[dict, DataLayoutElement], list[Union[dict, DataLayoutElement]]]])

slots.element_type = Slot(uri=PEHTERMS.element_type, name="element_type", curie=PEHTERMS.curie('element_type'),
                   model_uri=PEHTERMS.element_type, domain=None, range=Optional[Union[str, "DataLayoutElementType"]])

slots.element_style = Slot(uri=PEHTERMS.element_style, name="element_style", curie=PEHTERMS.curie('element_style'),
                   model_uri=PEHTERMS.element_style, domain=None, range=Optional[Union[str, "DataLayoutElementStyle"]])

slots.is_observable_entity_key = Slot(uri=PEHTERMS.is_observable_entity_key, name="is_observable_entity_key", curie=PEHTERMS.curie('is_observable_entity_key'),
                   model_uri=PEHTERMS.is_observable_entity_key, domain=None, range=Optional[Union[bool, Bool]])

slots.is_foreign_key = Slot(uri=PEHTERMS.is_foreign_key, name="is_foreign_key", curie=PEHTERMS.curie('is_foreign_key'),
                   model_uri=PEHTERMS.is_foreign_key, domain=None, range=Optional[Union[bool, Bool]])

slots.data_roles = Slot(uri=PEHTERMS.data_roles, name="data_roles", curie=PEHTERMS.curie('data_roles'),
                   model_uri=PEHTERMS.data_roles, domain=None, range=Optional[Union[Union[str, "DataRole"], list[Union[str, "DataRole"]]]])

slots.contacts = Slot(uri=PEHTERMS.contacts, name="contacts", curie=PEHTERMS.curie('contacts'),
                   model_uri=PEHTERMS.contacts, domain=None, range=Optional[Union[Union[dict, Contact], list[Union[dict, Contact]]]])

slots.contact_roles = Slot(uri=PEHTERMS.contact_roles, name="contact_roles", curie=PEHTERMS.curie('contact_roles'),
                   model_uri=PEHTERMS.contact_roles, domain=None, range=Optional[Union[Union[str, "ContactRole"], list[Union[str, "ContactRole"]]]])

slots.contact_email = Slot(uri=PEHTERMS.contact_email, name="contact_email", curie=PEHTERMS.curie('contact_email'),
                   model_uri=PEHTERMS.contact_email, domain=None, range=Optional[str])

slots.contact_phone = Slot(uri=PEHTERMS.contact_phone, name="contact_phone", curie=PEHTERMS.curie('contact_phone'),
                   model_uri=PEHTERMS.contact_phone, domain=None, range=Optional[str])

slots.request_properties = Slot(uri=PEHTERMS.request_properties, name="request_properties", curie=PEHTERMS.curie('request_properties'),
                   model_uri=PEHTERMS.request_properties, domain=None, range=Optional[str])

slots.data_stakeholders = Slot(uri=PEHTERMS.data_stakeholders, name="data_stakeholders", curie=PEHTERMS.curie('data_stakeholders'),
                   model_uri=PEHTERMS.data_stakeholders, domain=None, range=Optional[Union[Union[str, DataStakeholderId], list[Union[str, DataStakeholderId]]]])

slots.research_objectives = Slot(uri=PEHTERMS.research_objectives, name="research_objectives", curie=PEHTERMS.curie('research_objectives'),
                   model_uri=PEHTERMS.research_objectives, domain=None, range=Optional[Union[Union[str, ResearchObjectiveId], list[Union[str, ResearchObjectiveId]]]])

slots.processing_actions = Slot(uri=PEHTERMS.processing_actions, name="processing_actions", curie=PEHTERMS.curie('processing_actions'),
                   model_uri=PEHTERMS.processing_actions, domain=None, range=Optional[Union[Union[str, ProcessingActionId], list[Union[str, ProcessingActionId]]]])

slots.processing_steps = Slot(uri=PEHTERMS.processing_steps, name="processing_steps", curie=PEHTERMS.curie('processing_steps'),
                   model_uri=PEHTERMS.processing_steps, domain=None, range=Optional[Union[Union[str, ProcessingStepId], list[Union[str, ProcessingStepId]]]])

slots.remark_on_content = Slot(uri=PEHTERMS.remark_on_content, name="remark_on_content", curie=PEHTERMS.curie('remark_on_content'),
                   model_uri=PEHTERMS.remark_on_content, domain=None, range=Optional[str])

slots.remark_on_methodology = Slot(uri=PEHTERMS.remark_on_methodology, name="remark_on_methodology", curie=PEHTERMS.curie('remark_on_methodology'),
                   model_uri=PEHTERMS.remark_on_methodology, domain=None, range=Optional[str])

slots.observed_entity_properties = Slot(uri=PEHTERMS.observed_entity_properties, name="observed_entity_properties", curie=PEHTERMS.curie('observed_entity_properties'),
                   model_uri=PEHTERMS.observed_entity_properties, domain=None, range=Optional[Union[Union[dict, ObservedEntityProperty], list[Union[dict, ObservedEntityProperty]]]])

slots.processing_description = Slot(uri=PEHTERMS.processing_description, name="processing_description", curie=PEHTERMS.curie('processing_description'),
                   model_uri=PEHTERMS.processing_description, domain=None, range=Optional[str])

slots.objective_type = Slot(uri=PEHTERMS.objective_type, name="objective_type", curie=PEHTERMS.curie('objective_type'),
                   model_uri=PEHTERMS.objective_type, domain=None, range=Optional[Union[str, "ObjectiveType"]])

slots.authors = Slot(uri=PEHTERMS.authors, name="authors", curie=PEHTERMS.curie('authors'),
                   model_uri=PEHTERMS.authors, domain=None, range=Optional[Union[str, list[str]]])

slots.start_date = Slot(uri=PEHTERMS.start_date, name="start_date", curie=PEHTERMS.curie('start_date'),
                   model_uri=PEHTERMS.start_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.end_date = Slot(uri=PEHTERMS.end_date, name="end_date", curie=PEHTERMS.curie('end_date'),
                   model_uri=PEHTERMS.end_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.delivery_date = Slot(uri=PEHTERMS.delivery_date, name="delivery_date", curie=PEHTERMS.curie('delivery_date'),
                   model_uri=PEHTERMS.delivery_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.observation_start_date = Slot(uri=PEHTERMS.observation_start_date, name="observation_start_date", curie=PEHTERMS.curie('observation_start_date'),
                   model_uri=PEHTERMS.observation_start_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.observation_end_date = Slot(uri=PEHTERMS.observation_end_date, name="observation_end_date", curie=PEHTERMS.curie('observation_end_date'),
                   model_uri=PEHTERMS.observation_end_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.collection_date = Slot(uri=PEHTERMS.collection_date, name="collection_date", curie=PEHTERMS.curie('collection_date'),
                   model_uri=PEHTERMS.collection_date, domain=None, range=Optional[Union[str, XSDDate]])