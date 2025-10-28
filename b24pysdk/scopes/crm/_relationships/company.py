from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .base_relationship import BaseRelationship

__all__ = [
    "Company",
]


class Company(BaseRelationship):
    """The methods provide capabilities for working with companies linked to the contacts.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/company/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields for Contact-Company.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/company/crm-contact-company-fields.html

        The method returns the description of fields for the contact-company relationship.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(timeout=timeout)

    @type_checker
    def add(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a Company to the specified Contact.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/company/crm-contact-company-add.html

        The method adds a company to the specified contact.

        Args:
            bitrix_id: Identifier of the contact;

            fields: Object format:
                {
                    field_1: value_1,
                    field_2: value_2,
                    ...,
                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().add(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/contacts/company/crm-contact-company-delete.html

        This method removes a company from the specified contact.

        Args:
            bitrix_id: Identifier of the specified contact.

            fields: Object format:
                {
                    "COMPANY_ID": value
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().delete(
            bitrix_id,
            fields=fields,
            timeout=timeout,
        )
