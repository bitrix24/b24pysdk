from abc import ABC
from typing import Optional, Text

from ......api.requests import BitrixAPIRequest
from ......utils.types import JSONDict, JSONList, Timeout
from ...._base_crm import BaseCRM

__all__ = [
    "BaseConfiguration",
]


class BaseConfiguration(BaseCRM, ABC):
    """These methods allow you to configure sections within the detail form of CRM entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/index.html
    """

    def _get(
            self,
            *,
            entity_type_id: Optional[int] = None,
            user_id: Optional[int] = None,
            scope: Optional[Text] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get parameters of CRM item detail configuration.

        The method returns the settings of the detail form for a specific CRM entity.
        It can work with both personal settings of the specified user and shared settings defined for all users.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM entities;

            user_id: Identifier of the user whose configuration you want to retrieve;

            scope: Scope of the settings. Allowed values:

                - 'P' — personal settings (by default)

                - 'C' — shared settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return self._make_bitrix_api_request(
            api_wrapper=self._get,
            params=params,
            timeout=timeout,
        )

    def _set(
            self,
            *,
            entity_type_id: Optional[int] = None,
            data: JSONList,
            user_id: Optional[int] = None,
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set parameters for CRM item detail card configuration.

        The method sets the settings for the detail card of a specific CRM object.
        It records personal settings for the specified user or common settings for all users.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM objects;

            data: List of section describing the configuration of field sections in the item card;

            user_id: Identifier of the user for whom you want to set the configuration;

            scope: Scope of the settings. Allowed values:

                - 'P' — personal settings (by default)

                - 'C' — shared settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "data": data,
        }

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return self._make_bitrix_api_request(
            api_wrapper=self._set,
            params=params,
            timeout=timeout,
        )

    def _reset(
            self,
            *,
            entity_type_id: Optional[int] = None,
            user_id: Optional[int] = None,
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Reset item card parameters.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/crm-item-details-configuration-reset.html

        This method resets the item card settings to their default values.
        It removes the personal settings of the specified user or the shared settings defined for all users.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM entities;

            user_id: Identifier of the user whose configuration you want to retrieve;

            scope: Scope of the settings. Allowed values:

                - 'P' — personal settings (by default)

                - 'C' — shared settings;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if user_id is not None:
            params["userId"] = user_id

        if scope is not None:
            params["scope"] = scope

        if extras is not None:
            params["extras"] = extras

        return self._make_bitrix_api_request(
            api_wrapper=self._reset,
            params=params,
            timeout=timeout,
        )

    def _force_common_scope_for_all(
            self,
            *,
            entity_type_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set common detail for all users.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/crm-item-details-configuration-forceCommonScopeForAll.html

        This method forcibly sets a common detail for all users, removing their personal detail settings.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM entities;

            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        if extras is not None:
            params["extras"] = extras

        return self._make_bitrix_api_request(
            api_wrapper=self._force_common_scope_for_all,
            params=params,
            timeout=timeout,
        )
