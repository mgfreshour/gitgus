"""Salesforce Object Description."""

from re import sub
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel, ConfigDict
from stringcase import snakecase, camelcase, pascalcase


class Base(BaseModel):
    """Base Model."""

    model_config = ConfigDict(
        alias_generator=camelcase,
        frozen=True,
        extra="forbid",
    )


class ActionOverride(Base):
    """Salesforce Object Description Action Override."""

    form_factor: Optional[str]
    is_available_in_touch: bool
    name: str
    page_id: str
    url: Optional[str]


class ChildRelationship(Base):
    """Child Relationship."""

    cascade_delete: bool
    child_s_object: str
    deprecated_and_hidden: bool
    field: str
    junction_id_list_names: List[str]
    junction_reference_to: List[str]
    relationship_name: Optional[str]
    restricted_delete: bool


class PicklistValue(Base):
    """Picklist Values."""

    active: bool
    default_value: bool
    label: Optional[str]
    valid_for: Optional[str]
    value: str


class FilteredLookupInfo(Base):
    """Filtered Lookup Info."""

    controlling_fields: List[str]
    dependent: bool
    optional_filter: bool


class Field(Base):
    """Field."""

    aggregatable: bool
    ai_prediction_field: bool
    auto_number: bool
    byte_length: int
    calculated_formula: Optional[str]
    calculated: bool
    cascade_delete: bool
    case_sensitive: bool
    compound_field_name: Optional[str]
    controller_name: Optional[str]
    createable: bool
    custom: bool
    default_value_formula: Optional[str]
    default_value: Optional[Union[str, int, float, bool]]
    defaulted_on_create: bool
    dependent_picklist: bool
    deprecated_and_hidden: bool
    digits: int
    display_location_in_decimal: bool
    encrypted: bool
    external_id: bool
    extra_type_info: Optional[str]
    filterable: bool
    filtered_lookup_info: Optional[FilteredLookupInfo]
    formula_treat_null_number_as_zero: bool
    groupable: bool
    high_scale_number: bool
    html_formatted: bool
    id_lookup: bool
    inline_help_text: Optional[str]
    label: str
    length: int
    mask_type: Optional[str]
    mask: Optional[str]
    name_field: bool
    name_pointing: bool
    name: str
    nillable: bool
    permissionable: bool
    picklist_values: List[PicklistValue]
    polymorphic_foreign_key: bool
    precision: int
    query_by_distance: bool
    reference_target_field: Optional[str]
    reference_to: List[str]
    relationship_name: Optional[str]
    relationship_order: Optional[str]
    restricted_delete: bool
    restricted_picklist: bool
    scale: int
    search_prefilterable: bool
    soap_type: str
    sortable: bool
    type: str
    unique: bool
    updateable: bool
    write_requires_master_read: bool

    @property
    def deprecated(self) -> bool:
        """
        Return deprecation status.

        :returns: deprecation status
        """
        if self.deprecated_and_hidden:
            return True
        if "deprecated" in self.name.lower():
            return False
        if "deprecated" in self.label.lower():
            return True
        if "depreciated" in self.label.lower():
            return True
        if self.inline_help_text and "deprecated" in self.inline_help_text.lower():
            return True
        return False

    @property
    def hydrated_name(self):
        name = self.name_snakecase
        if name[-3:] == "_id":
            name = name[:-3]
        return name + "_name"

    @property
    def name_snakecase(self) -> str:
        """
        Name as snake_case.

        :returns: name as snake_case
        """
        overrides = {
            "SM_Change_Type__c": "sm_change_environment",
            "SM_ChangeType__c": "sm_change_type",
        }
        if self.name in overrides:
            return overrides[self.name]

        name = self.name.replace("__c", "")
        # lowercase consecutive uppercase characters
        name = sub(r"(?<=[A-Z])[A-Z]+(?=[A-Z]|_|$)", lambda m: m.group(0).lower(), name)
        name = snakecase(name).replace("__", "_")
        return {
            "id": "id_",
            "type": "type_",
            "schema": "schema_",
            "object": "object_",
        }.get(name, name)

    @property
    def name_capwords(self) -> str:
        """
        Name as CapWords.

        :returns: name as CapWords
        """
        return str(pascalcase(self.name_snakecase).replace("_", ""))

    @property
    def enum_values(self) -> Optional[List[str]]:
        """
        Enum values.

        :returns: enum values
        """
        if self.type == "picklist" and self.restricted_picklist:
            return [x.value for x in self.picklist_values]
        else:
            return None

    @property
    def json_schema_type(self) -> dict:
        """
        JSON schema type.

        :returns: JSON schema type
        """
        return {
            "tns:ID": {"type": "string"},
            "xsd:boolean": {"type": "boolean"},
            "xsd:date": {"type": "string", "format": "date"},
            "xsd:dateTime": {"type": "string", "format": "date-time"},
            "xsd:double": {"type": "number"},
            "xsd:int": {"type": "integer"},
            "xsd:string": {"type": "string"},
        }[self.soap_type]

    @property
    def json_schema_definition(self) -> Optional[dict]:
        """
        JSON schema property for field.

        :returns: JSON schema property for field
        """
        if self.enum_values:
            return {
                f"{self.name_capwords}Enum": {
                    "title": f"{self.name_capwords}Enum",
                    "description": f"{self.label}.",
                    "enum": self.enum_values,
                    **self.json_schema_type,
                }
            }
        else:
            return None

    @property
    def json_schema_property(self) -> dict:
        """
        JSON schema property for field.

        :returns: JSON schema property for field
        """
        if self.enum_values:
            return {
                self.name: {
                    "allOf": [{"$ref": f"#/definitions/{self.name_capwords}Enum"}],
                    "title": self.label,
                }
            }
        else:
            return {self.name: {"title": self.label, **self.json_schema_type}}

    @property
    def python_type(self) -> str:
        """
        Python type annotation.

        :returns: type annotation
        """
        if self.enum_values:
            annotation = self.name_capwords + "Enum"
        else:
            annotation = {
                "tns:ID": "str",
                "xsd:boolean": "bool",
                "xsd:date": "date",
                "xsd:dateTime": "datetime",
                "xsd:double": "float",
                "xsd:int": "int",
                "xsd:string": "str",
            }[self.soap_type]
        if self.nillable or self.custom:
            annotation = f"Optional[{annotation}]"
        return annotation

    @property
    def python_type_optional(self) -> str:
        """
        Python type annotation, always Optional.

        :returns: type annotation string
        """
        annotation = self.python_type
        if not annotation.startswith("Optional"):
            annotation = f"Optional[{annotation}]"
        return annotation

    @property
    def example_value(self) -> Union[str, int, float, bool, None]:
        """
        Build example value for field.

        :returns: example value
        """
        if self.nillable or self.custom:
            return None
        elif self.soap_type in {"urn:address", "urn:location"}:
            return None
        elif self.enum_values:
            return self.enum_values[0]
        elif self.python_type == "str":
            return "VALUE"
        elif self.python_type == "int":
            return 1
        elif self.python_type == "float":
            return 2.0
        elif self.python_type == "bool":
            return True
        elif self.python_type == "datetime":
            return "2020-05-26T04:31:44"
        elif self.python_type == "date":
            return "2020-05-26"
        return None


class InfoURLs(Base):
    """Record Type Info URLs."""

    layout: str


class NamedLayoutInfo(Base):
    """Named Layout Info."""

    name: str
    urls: InfoURLs


class RecordTypeInfo(Base):
    """Record Type Info."""

    active: bool
    available: bool
    default_record_type_mapping: bool
    developer_name: str
    master: bool
    name: str
    record_type_id: str
    urls: InfoURLs


class SupportedScope(Base):
    """Supported Scope."""

    label: str
    name: str


class URLs(Base):
    """URLs."""

    approval_layouts: Optional[str] = None
    case_article_suggestions: Optional[str] = None
    case_row_article_suggestions: Optional[str] = None
    compact_layouts: Optional[str] = None
    describe: str
    layouts: Optional[str]
    listviews: Optional[str] = None
    named_layouts: Optional[str] = None
    password_utilities: Optional[str] = None
    quick_actions: Optional[str]
    row_template: str
    sobject: str
    ui_detail_template: Optional[str]
    ui_edit_template: Optional[str]
    ui_new_record: Optional[str]


class SObjectDescription(Base):
    """Salesforce Object Description."""

    action_overrides: List[ActionOverride]
    activateable: bool
    associate_entity_type: Optional[str]
    associate_parent_entity: Optional[str]
    child_relationships: List[ChildRelationship]
    compact_layoutable: bool
    createable: bool
    custom_setting: bool
    custom: bool
    deep_cloneable: bool
    default_implementation: Optional[str]
    deletable: bool
    deprecated_and_hidden: bool
    extended_by: Optional[str]
    extends_interfaces: Optional[str]
    feed_enabled: bool
    fields: List[Field]
    has_subtypes: bool
    implemented_by: Optional[str]
    implements_interfaces: Optional[str]
    is_interface: bool
    is_subtype: bool
    key_prefix: Optional[str]
    label_plural: str
    label: str
    layoutable: bool
    listviewable: Optional[str]
    lookup_layoutable: Optional[str]
    mergeable: bool
    mru_enabled: bool
    name: str
    named_layout_infos: List[NamedLayoutInfo]
    network_scope_field_name: Optional[str]
    queryable: bool
    record_type_infos: List[RecordTypeInfo]
    replicateable: bool
    retrieveable: bool
    search_layoutable: bool
    searchable: bool
    sobject_describe_option: str
    supported_scopes: List[SupportedScope]
    triggerable: bool
    undeletable: bool
    updateable: bool
    urls: URLs

    @property
    def label_clean(self) -> str:
        """
        Label (cleaned).

        :returns: cleaned label
        """
        return sub(r"^([A-Z]{2,} )", "", self.label)

    @property
    def label_snakecase(self) -> str:
        """
        Label as snake_case.

        :returns: label as snake_case
        """
        return self.label_clean.replace(" ", "_").lower()

    @property
    def label_capwords(self) -> str:
        """
        Label as CapWords.

        :returns: label as CapWords
        """
        return str(pascalcase(self.label_snakecase))

    @property
    def label_plural_snakecase(self) -> str:
        """
        Label plural as snake_case.

        :returns: label as snake_case
        """
        clean = sub(r"^([A-Z]{2,} )", "", self.label_plural)
        return clean.replace(" ", "_").lower()

    @property
    def fields_all(self) -> List[Field]:
        """
        Get all fields.

        :returns: list of active fields
        """
        return list(
            {
                x.name_snakecase: x
                for x in self.fields
                if x.soap_type not in {"urn:address", "urn:location"}
            }.values()
        )

    @property
    def fields_queryable(self) -> List[Field]:
        """
        Get queryable fields.

        :returns: list of queryable fields
        """
        return [x for x in self.fields_all if x.filterable]

    @property
    def fields_creatable(self) -> List[Field]:
        """
        Get creatable fields.

        :returns: list of creatable fields
        """
        return [x for x in self.fields_all if x.createable]

    @property
    def can_be_created(self) -> bool:
        """
        Get creatable fields.

        :returns: list of creatable fields
        """
        return any(x.createable for x in self.fields_all)

    @property
    def can_be_updated(self) -> bool:
        """
        Get updatable fields.

        :returns: list of updatable fields
        """
        return any(x.updateable for x in self.fields_all)

    @property
    def json_schema(self) -> dict:
        """
        Get JSON Schema.

        :returns: JSON Schema
        """
        return build_json_schema(
            self.name,
            f"{self.label}.",
            self.fields_all,
            required=[
                x.name for x in self.fields_all if not x.nillable and not x.custom
            ],
        )


def build_json_schema(
    title: str,
    description: str,
    fields: List[Field],
    required: Optional[List[str]] = None,
) -> dict:
    """
    Build JSON Schema.

    :param title: title for schema
    :param description: description for schema
    :param fields: fields to use
    :param required: required keys
    :returns: JSON schema
    """
    schema: dict = {
        "description": description,
        "title": title,
        "type": "object",
    }
    properties = {}
    definitions = {}
    for field in fields:
        properties.update(field.json_schema_property)
        if field.json_schema_definition:
            definitions.update(field.json_schema_definition)
    schema["properties"] = properties
    if definitions:
        schema["definitions"] = definitions
    if required:
        schema["required"] = required
    return schema
