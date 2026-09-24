from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, List, Optional, Text, Union

from ...utils.converters import int_from_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_file_schema import BaseFileSchema

__all__ = [
    "ListElementFile",
    "ListFieldListItem",
]


@dataclass(**frozen_dataclass_kwargs())
class ListFieldListItem:
    """Selectable value exposed by a Bitrix24 list field."""
    bitrix_id: int
    value: Text


@dataclass(**frozen_dataclass_kwargs())
class ListElementFile(BaseFileSchema):
    """File stored in a Bitrix24 list-element property.

    A value read from Bitrix24 contains only the property-value ID and file ID,
    so the SDK cannot download it directly. Browser URLs remain available from
    ``BaseListElement.get_file_urls()``.

    A local file created with ``from_bytes()``, ``from_base64()``,
    ``from_file()`` or ``from_path()`` can be assigned to a ``FileField`` and
    is serialized as ``[name, base64]``. A multiple ``FileField`` serializes
    each local file independently and therefore produces a list of such pairs.
    """

    property_value_id: Optional[int] = None
    bitrix_id: Optional[int] = None

    @classmethod
    def from_bitrix(
            cls,
            bitrix_data: Mapping[Union[int, Text], Union[int, Text]],
            /,
            **_context: Any,
    ) -> "ListElementFile":
        """Create a remote list-element file from one property-value mapping."""

        if not isinstance(bitrix_data, Mapping):
            raise TypeError(
                "Bitrix24 list-element file value must be a mapping, "
                f"got {type(bitrix_data).__name__}.",
            )

        if len(bitrix_data) != 1:
            raise ValueError("Bitrix24 list-element file value must contain exactly one file.")

        property_value_id, bitrix_id = next(iter(bitrix_data.items()))

        property_value_id = int_from_bitrix(property_value_id, is_required=True)
        bitrix_id = int_from_bitrix(bitrix_id, is_required=True)

        return cls(property_value_id=property_value_id, bitrix_id=bitrix_id)

    def to_bitrix(self) -> List[Text]:
        """Convert a local file to the list-element upload representation."""

        if not self.is_local:
            raise ValueError(
                "A remote list-element file cannot be written by file ID. "
                "Assign a local ListElementFile created with from_bytes(), "
                "from_base64(), from_file() or from_path().",
            )

        name = self.name

        if name is None:
            raise ValueError("A local list-element file requires a file name.")

        return [name, self.to_base64()]

    @property
    def download_url(self) -> Text:
        """Raise because list-element file values do not contain download URLs."""

        if self.is_local:
            raise ValueError("A local list-element file does not have a download URL.")

        raise ValueError(
            "A remote list-element file cannot be downloaded directly. "
            "Use BaseListElement.get_file_urls() to obtain browser URLs.",
        )
