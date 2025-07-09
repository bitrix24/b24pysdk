from typing import Optional, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..item.details.configuration import Configuration as BaseConfiguration


class Configuration(BaseConfiguration):
    """The group of methods manages the settings of the CRM card for two views: 'General view' and 'My view'. Works for leads, deals, contacts and companies.

    Documentation:
    https://apidocs.bitrix24.com/api-reference/crm/deals/custom-form/index.html
    https://apidocs.bitrix24.com/api-reference/crm/leads/custom-form/index.html
    https://apidocs.bitrix24.com/api-reference/crm/contacts/custom-form/index.html
    https://apidocs.bitrix24.com/api-reference/crm/companies/custom-form/index.html
    """

    @type_checker
    def get(
            self,
            *,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Get parameters of CRM card configuration.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/deals/custom-form/crm-deal-details-configuration-get.html
        https://apidocs.bitrix24.com/api-reference/crm/leads/custom-form/crm-lead-details-configuration-get.html
        https://apidocs.bitrix24.com/api-reference/crm/contacts/custom-form/crm-contact-details-configuration-get.html
        https://apidocs.bitrix24.com/api-reference/crm/companies/custom-form/crm-company-details-configuration-get.html

        The method retrieves the settings of CRM cards.

        Args:
            scope: The scope of the settings, where allowed values are:

                - P - personal settings,

                - C - general settings;

            user_id: User identifier, if not specified, the current user is taken and requiring only when getting personal settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(
            scope=scope,
            user_id=user_id,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            *,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Set parameters for the CRM detail card.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/deals/custom-form/crm-deal-details-configuration-set.html
        https://apidocs.bitrix24.com/api-reference/crm/leads/custom-form/crm-lead-details-configuration-set.html
        https://apidocs.bitrix24.com/api-reference/crm/contacts/custom-form/crm-contact-details-configuration-set.html
        https://apidocs.bitrix24.com/api-reference/crm/companies/custom-form/crm-company-details-configuration-set.html

        The method allows you to set the settings for CRM cards.

        Args:
            scope: The scope of the settings, where allowed values are:

                - P - personal settings,

                - C - general settings;

            user_id: User identifier, if not specified, the current user is taken and requiring only when setting personal settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._set(
            data=list(),
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def reset(
            self,
            *,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """The method resets the settings of CRM cards.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/deals/custom-form/crm-deal-details-configuration-reset.html
        https://apidocs.bitrix24.com/api-reference/crm/leads/custom-form/crm-lead-details-configuration-reset.html
        https://apidocs.bitrix24.com/api-reference/crm/contacts/custom-form/crm-contact-details-configuration-reset.html
        https://apidocs.bitrix24.com/api-reference/crm/companies/custom-form/crm-company-details-configuration-reset.html

        Args:
            scope: The scope of the settings, where allowed values are:

                - P - personal settings,

                - C - general settings;

            user_id: User identifier, if not specified, the current user is taken and requiring only when resetting personal settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._reset(
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def force_common_scope_for_all(
            self,
            *,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Set common CRM card.

        Documentation:
        https://apidocs.bitrix24.com/api-reference/crm/deals/custom-form/crm-deal-details-configuration-force-common-scope-for-all.html
        https://apidocs.bitrix24.com/api-reference/crm/leads/custom-form/crm-lead-details-configuration-force-common-scope-for-all.html
        https://apidocs.bitrix24.com/api-reference/crm/contacts/custom-form/crm-contact-details-configuration-force-common-scope-for-all.html
        https://apidocs.bitrix24.com/api-reference/crm/companies/custom-form/crm-company-details-configuration-force-common-scope-for-all.html

        The method forcibly sets a common CRM card for all users.

        Args:
            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._force_common_scope_for_all(
            extras=extras,
            timeout=timeout,
        )
