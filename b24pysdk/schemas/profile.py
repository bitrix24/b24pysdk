from dataclasses import dataclass
from typing import Annotated, Literal, Optional, Text, TypedDict
from zoneinfo import ZoneInfo

from ..constants.user import PersonalGender
from ..utils.converters import (
    bool_from_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
    timezone_from_bitrix,
    timezone_to_bitrix,
)
from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "Profile",
    "ProfileData",
]


class ProfileData(TypedDict):
    ID: int
    ADMIN: bool
    NAME: Text
    LAST_NAME: Text
    PERSONAL_GENDER: Annotated[Text, Literal["", "F", "M"]]
    TIME_ZONE: Text


@dataclass(**frozen_dataclass_kwargs())
class Profile(BaseSchema[ProfileData]):
    """
    Current user profile returned by the ``profile`` method.

    The method returns basic information about the current user without
    requiring additional Bitrix24 scopes.
    """

    bitrix_id: int
    admin: bool
    name: Text
    last_name: Text
    personal_gender: PersonalGender
    time_zone: Optional[ZoneInfo]

    @classmethod
    def from_bitrix(cls, bitrix_data: ProfileData, /) -> "Profile":
        """
        Create a Profile schema from raw Bitrix24 profile data.

        Args:
            bitrix_data: Raw ``result`` object returned by the ``profile`` method.

        Returns:
            Profile schema with Python-friendly field names and types.
        """
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            admin=bool_from_bitrix(bitrix_data["ADMIN"], is_required=True),
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            last_name=text_from_bitrix(bitrix_data["LAST_NAME"], is_required=True),
            personal_gender=PersonalGender(bitrix_data["PERSONAL_GENDER"]),
            time_zone=timezone_from_bitrix(bitrix_data["TIME_ZONE"]),
        )

    def to_bitrix(self) -> ProfileData:
        """
        Convert the profile schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 field names.
        """
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "ADMIN": bool_from_bitrix(self.admin, is_required=True),
            "NAME": text_to_bitrix(self.name, is_required=True),
            "LAST_NAME": text_to_bitrix(self.last_name, is_required=True),
            "PERSONAL_GENDER": self.personal_gender.value,
            "TIME_ZONE": timezone_to_bitrix(self.time_zone) or "",
        }
