from typing import Optional, Text

from ......bitrix_api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, JSONList, Timeout
from .base_configuration import BaseConfiguration

__all__ = [
    "Configuration",
]


class Configuration(BaseConfiguration):
    """These methods allow you to configure sections within the detail form of CRM entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/index.html
    """

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            user_id: Optional[int] = None,
            scope: Optional[Text] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get parameters of CRM item detail configuration.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/crm-item-details-configuration-get.html

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
        return self._get(
            entity_type_id=entity_type_id,
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            *,
            entity_type_id: int,
            data: JSONList,
            user_id: Optional[int] = None,
            scope: Optional[str] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set parameters for CRM item detail card configuration.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/item-details-configuration/crm-item-details-configuration-set.html

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
        return self._set(
            entity_type_id=entity_type_id,
            data=data,
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def reset(
            self,
            *,
            entity_type_id: int,
            user_id: Optional[int],
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
        return self._reset(
            entity_type_id=entity_type_id,
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def force_common_scope_for_all(
            self,
            *,
            entity_type_id: int,
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
        return self._force_common_scope_for_all(
            entity_type_id=entity_type_id,
            extras=extras,
            timeout=timeout,
        )
