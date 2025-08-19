from typing import TYPE_CHECKING, Iterable

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict
from ..base_crm import BaseCRM, Timeout

if TYPE_CHECKING:
    from .relationship import Relationship


class Items(BaseCRM):
    """These methods manage bindings between a specified CRM entity (such as a Contact, Lead, Deal, or Company) and a collection of similar-type CRM entities.
    """

    def __init__(self, relationship: "Relationship"):
        super().__init__(relationship._scope)
        self._path = self._get_path(relationship)

    @type_checker
    def set(
            self,
            bitrix_id: int,
            items: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add set of CRM entities to the specified one.

        The method adds a collection of CRM similar-type CRM entities to the specified one.
        Note that you can only add a collection of Contacts to a Lead, Deal or Company and collection of Companies to a Contact.

        Args:
            bitrix_id: Identifier of the CRM entity to which collection needs to be added;

            items: Object format:
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
            "items": list(items),
        }

        return self._make_bitrix_api_request(
            api_method=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a collection associated with CRM entity.

        This method retrieves a similar-typed collection associated with specified CRM entity.
        Note that you can only get a collection of Contacts from a Lead, Deal or Company and collection of Companies from a Contact.

        Args:
            bitrix_id: Identifier of the CRM entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Clear a collection of similar-typed linked to the specified entity.

        The method clears the set of similar-typed CRM entities associated with the specified entity.
        Note that Contacts can be associated with Lead, Deal or Company and Company can be associated with Contact.

        Args:
            bitrix_id: Identifier of the CRM entity;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
