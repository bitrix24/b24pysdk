from dataclasses import dataclass
from typing import Annotated, Literal, Optional, Text, TypedDict
from zoneinfo import ZoneInfo

from ..constants.user import PersonalGender
from ..utils.converters import timezone_from_bitrix, timezone_to_bitrix
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
            bitrix_id=int(bitrix_data["ID"]),
            admin=bitrix_data["ADMIN"],
            name=bitrix_data["NAME"],
            last_name=bitrix_data["LAST_NAME"],
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
            "ID": self.bitrix_id,
            "ADMIN": self.admin,
            "NAME": self.name,
            "LAST_NAME": self.last_name,
            "PERSONAL_GENDER": self.personal_gender.value,
            "TIME_ZONE": timezone_to_bitrix(self.time_zone) or "",
        }
