from dataclasses import dataclass
from typing import Final, List, Optional, Text

from ..utils.converters import (
    float_from_bitrix,
    float_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "Address",
    "Coordinates",
]


_ADDRESS_PARTS_COUNT: Final[int] = 3
_COORDINATES_PARTS_COUNT: Final[int] = 2


@dataclass(**frozen_dataclass_kwargs())
class Coordinates(BaseSchema[Text]):
    """Geographic coordinates used in a Bitrix24 address field.

    Bitrix24 stores coordinates as a ``latitude;longitude`` string.
    """

    latitude: float
    longitude: float

    @classmethod
    def from_bitrix(cls, bitrix_data: Text, /) -> "Coordinates":
        """Create coordinates from a raw Bitrix24 coordinates string."""

        raw_value = text_from_bitrix(bitrix_data, is_required=True)
        parts = raw_value.split(";", _COORDINATES_PARTS_COUNT - 1)

        if not (
                len(parts) == _COORDINATES_PARTS_COUNT
                and parts[0]
                and parts[1]
        ):
            raise ValueError(
                "Bitrix24 address coordinates must contain latitude and "
                "longitude separated by ';'.",
            )

        return cls(
            latitude=float_from_bitrix(parts[0], is_required=True),
            longitude=float_from_bitrix(parts[1], is_required=True),
        )

    def to_bitrix(self) -> Text:
        """Convert coordinates to a Bitrix24 coordinates string."""

        latitude = float_to_bitrix(self.latitude, is_required=True)
        longitude = float_to_bitrix(self.longitude, is_required=True)

        return f"{latitude};{longitude}"


@dataclass(**frozen_dataclass_kwargs())
class Address(BaseSchema[Text]):
    """Structured value of a Bitrix24 address field.

    Bitrix24 stores an address as one string with three ``|``-separated
    sections: address text, coordinates and location address ID.
    Coordinates and location address ID may be empty.
    """

    value: Text
    coordinates: Optional[Coordinates] = None
    location_address_id: Optional[int] = None

    @classmethod
    def from_bitrix(cls, bitrix_data: Text, /) -> "Address":
        """Create an address schema from a raw Bitrix24 address string."""

        raw_value: Text = text_from_bitrix(bitrix_data, is_required=True)
        parts: List[Text] = raw_value.rsplit("|", _ADDRESS_PARTS_COUNT - 1)

        if len(parts) == _ADDRESS_PARTS_COUNT - 1:
            parts.append("")

        if len(parts) != _ADDRESS_PARTS_COUNT:
            raise ValueError(
                "Bitrix24 address value must contain address, coordinates and "
                "optional location address ID sections separated by '|'.",
            )

        value, coordinates_value, location_address_id_value = parts

        return cls(
            value=value,
            coordinates=Coordinates.from_bitrix(coordinates_value) if coordinates_value else None,
            location_address_id=int_from_bitrix(location_address_id_value),
        )

    def to_bitrix(self) -> Text:
        """Convert the address schema to a Bitrix24 address string."""

        address_parts = (
            text_to_bitrix(self.value, is_required=True),
            self.coordinates.to_bitrix() if self.coordinates is not None else "",
        )

        if self.location_address_id is None:
            return "|".join(address_parts)

        location_address_id = int_to_bitrix(self.location_address_id, is_required=True)

        return "|".join((
            *address_parts,
            str(location_address_id),
        ))
