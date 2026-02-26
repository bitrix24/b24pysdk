from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .base_relationship import BaseRelationship

__all__ = [
    "Contact",
]


class Contact(BaseRelationship):
    """These methods provide capabilities for managing Contacts linked to the Deals, Leads and Companies (CRM entity).

    Documentation:
        - for deals: https://apidocs.bitrix24.com/api-reference/crm/deals/contacts/index.html
        - for leads: https://apidocs.bitrix24.com/api-reference/crm/leads/management-communication/index.html
        - for companies: https://apidocs.bitrix24.com/api-reference/crm/companies/contacts/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields for entity-contact connection.

        Documentation:

        - `for leads; <https://apidocs.bitrix24.com/api-reference/crm/leads/management-communication/crm-lead-contact-fields.html>`__

        - `for deals; <https://apidocs.bitrix24.com/api-reference/crm/deals/contacts/crm-deal-contact-fields.html>`__

        - `for companies. <https://apidocs.bitrix24.com/api-reference/crm/companies/contacts/crm-company-contact-fields.html>`__

        The method retrieves the description of the fields for the entity-contact relationship, where entity is one of the available CRM-entities: Lead, Deal or Company.

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
        """Add contact binding to CRM entity.

        Documentation:

        - `for leads; <https://apidocs.bitrix24.com/api-reference/crm/leads/management-communication/crm-lead-contact-add.html>`__

        - `for deals; <https://apidocs.bitrix24.com/api-reference/crm/deals/contacts/crm-deal-contact-add.html>`__

        - `for companies. <https://apidocs.bitrix24.com/api-reference/crm/companies/contacts/crm-company-contact-add.html>`__

        This method adds a contact binding to the specified CRM entity, where entity is one of the available CRM-entities: Lead, Deal or Company.

        Args:
            bitrix_id: The identifier of the CRM entity to which the contact needs to be added;

            fields: Object format:
                {
                    "CONTACT_ID": "value",

                    "SORT": "value",

                    "IS_PRIMARY": "value"
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
        """Remove contact from CRM entity.

        Documentation:

        - `for leads; <https://apidocs.bitrix24.com/api-reference/crm/leads/management-communication/crm-lead-contact-delete.html>`__

        - `for deals; <https://apidocs.bitrix24.com/api-reference/crm/deals/contacts/crm-deal-contact-delete.html>`__

        - `for companies. <https://apidocs.bitrix24.com/api-reference/crm/companies/contacts/crm-company-contact-delete.html>`__

        The method removes a contact from the specified CRM entity, where entity is one of the available CRM-entities: Lead, Deal or Company.

        Args:
            bitrix_id: The identifier of the CRM entity from which to remove the contact binding;

            fields: Object format:
                {
                    "CONTACT_ID": "value",
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
