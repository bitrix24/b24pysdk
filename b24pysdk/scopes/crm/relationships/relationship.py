from abc import abstractmethod

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM
from ..item.base_item import BaseItem
from .items import Items


class Relationship(BaseCRM):
    """These methods provide functionality for working with Company-Contact and Contact-CRM entity bindings, where the CRM entity can be a Lead, Deal, or Company.
    """

    def __init__(self, item: BaseItem):
        super().__init__(item._scope)
        self._path = self._get_path(item)

    @property
    def items(self) -> "Items":
        """"""
        return Items(self)

    @abstractmethod
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields for the connection between entities.

        This method retrieves the fields of the connection between a Contact or Company and the specified CRM entity (Lead, Deal, Contact, or Company).
        Note that a Contact can be linked to a Lead, Deal, or Company, and a Company can be linked to a Contact.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @abstractmethod
    def add(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a connection between CRM entities.

        This method adds connection between Contact or Company and the specified CRM entity (Lead, Deal, Contact, or Company).
        Note that a Contact can be linked to a Lead, Deal, or Company, and a Company can be linked to a Contact.

        Args:
            bitrix_id: Identifier of the CRM entity to be linked;

            fields: Object format:
                {
                    "CONTACT_ID" or "COMPANY_ID": "value",

                    "SORT": "value",

                    "IS_PRIMARY": "value"
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @abstractmethod
    def delete(
            self,
            bitrix_id: int,
            *,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete connection between CRM entities.

        The method removes a Contact from a Lead, Deal, or Company, and removes a Company from a Contact.

        Args:
            bitrix_id: Identifier of the CRM entity to be linked;

            fields: Object format:
                {
                    "COMPANY_ID" or "CONTACT_ID": value
                }

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
