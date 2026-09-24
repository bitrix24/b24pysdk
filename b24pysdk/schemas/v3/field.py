from dataclasses import dataclass
from typing import List, Optional, Text, TypedDict

from ...utils.converters import (
    bool_from_bitrix,
    dict_from_bitrix,
    dict_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict
from .._base_schema import BaseSchema

__all__ = [
    "V3Field",
    "V3FieldData",
]


class V3FieldData(TypedDict):
    """Raw field description returned by REST API v3 field methods."""
    name: Text
    type: Text
    title: Text
    description: Optional[Text]
    validationRules: List[JSONDict]
    requiredGroups: Optional[List[Text]]
    filterable: bool
    sortable: bool
    editable: bool
    multiple: bool
    elementType: Optional[Text]


@dataclass(**frozen_dataclass_kwargs())
class V3Field(BaseSchema[V3FieldData]):
    """Description of an entity field returned by Bitrix24 REST API v3."""

    name: Text
    type: Text
    title: Text
    description: Optional[Text]
    validation_rules: List[JSONDict]
    required_groups: Optional[List[Text]]
    filterable: bool
    sortable: bool
    editable: bool
    multiple: bool
    element_type: Optional[Text]

    @classmethod
    def from_bitrix(
            cls,
            bitrix_data: V3FieldData,
            /,
    ) -> "V3Field":
        return cls(
            name=text_from_bitrix(bitrix_data["name"], is_required=True),
            type=text_from_bitrix(bitrix_data["type"], is_required=True),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
            description=text_from_bitrix(bitrix_data["description"]),
            validation_rules=[
                dict_from_bitrix(validation_rule, is_required=True)
                for validation_rule in bitrix_data["validationRules"]
            ],
            required_groups=(
                None
                if bitrix_data["requiredGroups"] is None
                else [
                    text_from_bitrix(required_group, is_required=True)
                    for required_group in bitrix_data["requiredGroups"]
                ]
            ),
            filterable=bool_from_bitrix(bitrix_data["filterable"], is_required=True),
            sortable=bool_from_bitrix(bitrix_data["sortable"], is_required=True),
            editable=bool_from_bitrix(bitrix_data["editable"], is_required=True),
            multiple=bool_from_bitrix(bitrix_data["multiple"], is_required=True),
            element_type=text_from_bitrix(bitrix_data["elementType"]),
        )

    def to_bitrix(self) -> V3FieldData:
        return {
            "name": text_to_bitrix(self.name, is_required=True),
            "type": text_to_bitrix(self.type, is_required=True),
            "title": text_to_bitrix(self.title, is_required=True),
            "description": text_to_bitrix(self.description),
            "validationRules": [
                dict_to_bitrix(validation_rule, is_required=True)
                for validation_rule in self.validation_rules
            ],
            "requiredGroups": (
                None
                if self.required_groups is None
                else [
                    text_to_bitrix(required_group, is_required=True)
                    for required_group in self.required_groups
                ]
            ),
            "filterable": self.filterable,
            "sortable": self.sortable,
            "editable": self.editable,
            "multiple": self.multiple,
            "elementType": text_to_bitrix(self.element_type),
        }
