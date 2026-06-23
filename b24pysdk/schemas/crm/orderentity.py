from typing import TypedDict

from .field import CRMFieldsData, CRMFieldsDict

__all__ = [
    "OrderentityFieldsDict",
    "OrderentityFieldsResultData",
]


class OrderentityFieldsResultData(TypedDict):
    orderEntity: CRMFieldsData


class OrderentityFieldsDict(CRMFieldsDict):
    """
    CRM order entity fields returned under the ``orderEntity`` wrapper key.
    """
    _WRAPPER = "orderEntity"
