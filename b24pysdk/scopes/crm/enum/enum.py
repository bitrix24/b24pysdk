from ....bitrix_api.classes import BitrixAPIRequest
from ....scopes.crm.base_crm import BaseCRM
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .settings import Settings


class Enum(BaseCRM):
    """The methods return information about the values of types: address type, activity type, object type, and others.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/index.html
    """

    @property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @type_checker
    def activitydirection(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get activity direction enumeration elements.

        DocumentationL https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-activity-direction.html

        The method returns activity directions for the DIRECTION field of deals, emails, and calls.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitydirection),
            timeout=timeout,
        )

    @type_checker
    def activitynotifytype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get enumeration items 'Activity notification type'.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-activity-notify-type.html

        The method returns notification types for the NOTIFY_TYPE field of meetings and calls.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitynotifytype),
            timeout=timeout,
        )

    @type_checker
    def activitypriority(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get enumeration items 'Activity priority'.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-activity-priority.html

        The method returns a list of properties for the PRIORITY field of deals.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitypriority),
            timeout=timeout,
        )

    @type_checker
    def activitystatus(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get enumeration items 'Status'.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-activity-status.html

        The method returns a list of statuses for the STATUS field of deals.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitystatus),
            timeout=timeout,
        )

    @type_checker
    def activitytype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get enumeration item 'Activity types'.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-activity-type.html

        The method returns a list of types for the TYPE_ID field of activities.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.activitytype),
            timeout=timeout,
        )

    @type_checker
    def addresstype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get address types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-address-type.html

        The method returns a list of address types.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.addresstype),
            timeout=timeout,
        )

    @type_checker
    def contenttype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get enumeration items for 'Description type'.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/outdated/crm-enum-content-type.html

        The method returns description types for the DESCRIPTION_TYPE field of deals.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.contenttype),
            timeout=timeout,
        )

    @type_checker
    def getorderownertypes(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get object types for order binding.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-get-order-owner-types.html

        The method returns a list of object types to which an order can be bound.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.getorderownertypes),
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of CRM enumeration elements.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-fields.html

        The method returns information about the fields of enumeration elements.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def ownertype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get CRM object types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-owner-type.html

        The method returns the identifiers of CRM object types and smart processes.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.ownertype),
            timeout=timeout,
        )
