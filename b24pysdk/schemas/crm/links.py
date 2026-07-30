from abc import ABC
from dataclasses import dataclass
from typing import Annotated, Generic, List, Optional, Text, TypedDict, TypeVar

from ...utils.converters import bool_from_bitrix, bool_to_bitrix, int_from_bitrix, int_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import B24BoolStrictLiteral
from .._base_schema import BaseSchema

__all__ = [
    "CompanyLink",
    "CompanyLinkData",
    "CompanyLinksData",
    "ContactLink",
    "ContactLinkData",
    "ContactLinksData",
]


class _BaseLinkOptionalData(TypedDict, total=False):
    ROLE_ID: int


class _BaseLinkData(_BaseLinkOptionalData):
    SORT: int
    IS_PRIMARY: Annotated[Text, B24BoolStrictLiteral]


_BaseLinkDataT = TypeVar("_BaseLinkDataT", bound=_BaseLinkData)


@dataclass(**frozen_dataclass_kwargs())
class _BaseLink(BaseSchema[_BaseLinkDataT], ABC, Generic[_BaseLinkDataT]):
    """
    Base class for CRM entity link schemas.

    It stores common Python-friendly fields shared by CRM link schemas.
    """
    sort: int
    role_id: Optional[int]
    is_primary: bool


class CompanyLinkData(_BaseLinkData):
    COMPANY_ID: int


CompanyLinksData = List[CompanyLinkData]


@dataclass(**frozen_dataclass_kwargs())
class CompanyLink(_BaseLink[CompanyLinkData]):
    """
    Company link returned by ``crm.contact.company.items.get``.
    """

    company_id: int

    @classmethod
    def from_bitrix(cls, bitrix_data: CompanyLinkData, /) -> "CompanyLink":
        """
        Create a CompanyLink schema from Bitrix24 data.
        """
        return cls(
            sort=int_from_bitrix(bitrix_data["SORT"], is_required=True),
            role_id=int_from_bitrix(bitrix_data.get("ROLE_ID")),
            is_primary=bool_from_bitrix(bitrix_data["IS_PRIMARY"], is_required=True),
            company_id=int_from_bitrix(bitrix_data["COMPANY_ID"], is_required=True),
        )

    def to_bitrix(self) -> CompanyLinkData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.
        """

        bitrix_data: CompanyLinkData = {
            "COMPANY_ID": int_to_bitrix(self.company_id, is_required=True),
            "SORT": int_to_bitrix(self.sort, is_required=True),
            "IS_PRIMARY": bool_to_bitrix(self.is_primary, is_required=True),
        }

        if self.role_id is not None:
            bitrix_data["ROLE_ID"] = int_to_bitrix(self.role_id, is_required=True)

        return bitrix_data



class ContactLinkData(_BaseLinkData):
    CONTACT_ID: int


ContactLinksData = List[ContactLinkData]


@dataclass(**frozen_dataclass_kwargs())
class ContactLink(_BaseLink[ContactLinkData]):
    """
    Contact link returned by CRM contact binding methods.

    Used by ``crm.deal.contact.items.get``,
    ``crm.lead.contact.items.get`` and ``crm.company.contact.items.get``.
    """

    contact_id: int

    @classmethod
    def from_bitrix(cls, bitrix_data: ContactLinkData, /) -> "ContactLink":
        """
        Create a ContactLink schema from Bitrix24 data.
        """
        return cls(
            sort=int_from_bitrix(bitrix_data["SORT"], is_required=True),
            role_id=int_from_bitrix(bitrix_data.get("ROLE_ID")),
            is_primary=bool_from_bitrix(bitrix_data["IS_PRIMARY"], is_required=True),
            contact_id=int_from_bitrix(bitrix_data["CONTACT_ID"], is_required=True),
        )

    def to_bitrix(self) -> ContactLinkData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.
        """

        bitrix_data: ContactLinkData = {
            "CONTACT_ID": int_to_bitrix(self.contact_id, is_required=True),
            "SORT": int_to_bitrix(self.sort, is_required=True),
            "IS_PRIMARY": bool_to_bitrix(self.is_primary, is_required=True),
        }

        if self.role_id is not None:
            bitrix_data["ROLE_ID"] = int_to_bitrix(self.role_id, is_required=True)

        return bitrix_data
