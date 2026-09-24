from dataclasses import dataclass
from typing import Annotated, List, Optional, Text, TypedDict, Union

from ...constants.group import GroupPermissionRole, GroupPermissionRoleLiteral
from ...utils.converters import bool_from_bitrix, bool_to_bitrix, int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import B24BoolStrictLiteral
from .._base_schema import BaseSchema

__all__ = [
    "SonetGroupMember",
    "SonetGroupMemberData",
    "SonetGroupMembersData",
    "SonetGroupUserGroup",
    "SonetGroupUserGroupData",
    "SonetGroupUserGroupsData",
]


class SonetGroupMemberData(TypedDict):
    USER_ID: Union[int, Text]
    ROLE: Annotated[Text, GroupPermissionRoleLiteral]


SonetGroupMembersData = List[SonetGroupMemberData]


@dataclass(**frozen_dataclass_kwargs())
class SonetGroupMember(BaseSchema[SonetGroupMemberData]):
    """Active participant returned by ``sonet_group.user.get``."""

    user_id: int
    role: GroupPermissionRole

    @classmethod
    def from_bitrix(cls, bitrix_data: SonetGroupMemberData, /) -> "SonetGroupMember":
        return cls(
            user_id=int_from_bitrix(bitrix_data["USER_ID"], is_required=True),
            role=GroupPermissionRole(bitrix_data["ROLE"]),
        )

    def to_bitrix(self) -> SonetGroupMemberData:
        return {
            "USER_ID": int_to_bitrix(self.user_id, is_required=True),
            "ROLE": self.role.value,
        }


class _SonetGroupUserGroupOptionalData(TypedDict, total=False):
    IS_EXTRANET: Annotated[Text, B24BoolStrictLiteral]


class SonetGroupUserGroupData(_SonetGroupUserGroupOptionalData):
    GROUP_ID: Union[int, Text]
    GROUP_NAME: Text
    ROLE: Annotated[Text, GroupPermissionRoleLiteral]
    GROUP_IMAGE_ID: Optional[Union[int, Text]]
    GROUP_IMAGE: Text


SonetGroupUserGroupsData = List[SonetGroupUserGroupData]


@dataclass(**frozen_dataclass_kwargs())
class SonetGroupUserGroup(BaseSchema[SonetGroupUserGroupData]):
    """Group membership returned by ``sonet_group.user.groups`` for the current user."""

    group_id: int
    group_name: Text
    role: GroupPermissionRole
    group_image_id: Optional[int]
    group_image: Optional[Text]
    is_extranet: bool

    @classmethod
    def from_bitrix(cls, bitrix_data: SonetGroupUserGroupData, /) -> "SonetGroupUserGroup":
        return cls(
            group_id=int_from_bitrix(bitrix_data["GROUP_ID"], is_required=True),
            group_name=text_from_bitrix(bitrix_data["GROUP_NAME"], is_required=True),
            role=GroupPermissionRole(bitrix_data["ROLE"]),
            group_image_id=int_from_bitrix(bitrix_data.get("GROUP_IMAGE_ID")),
            group_image=text_from_bitrix(bitrix_data.get("GROUP_IMAGE")),
            is_extranet=bool_from_bitrix(bitrix_data.get("IS_EXTRANET")) or False,
        )

    def to_bitrix(self) -> SonetGroupUserGroupData:
        bitrix_data: SonetGroupUserGroupData = {
            "GROUP_ID": int_to_bitrix(self.group_id, is_required=True),
            "GROUP_NAME": text_to_bitrix(self.group_name, is_required=True),
            "ROLE": self.role.value,
            "GROUP_IMAGE_ID": int_to_bitrix(self.group_image_id),
            "GROUP_IMAGE": text_to_bitrix(self.group_image) or "",
        }

        if self.is_extranet:
            bitrix_data["IS_EXTRANET"] = bool_to_bitrix(True, is_required=True)

        return bitrix_data
