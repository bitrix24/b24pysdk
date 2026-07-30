from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest, BitrixAPIValuesRequest
from ......schemas.crm.details_configuration import CRMDetailsConfigurationSection, CRMDetailsConfigurationSectionsData
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
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
            user_id: Optional[int] = MISSING,
            scope: Optional[Text] = MISSING,
            extras: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[Optional[CRMDetailsConfigurationSectionsData], CRMDetailsConfigurationSection]:
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
            Instance of BitrixAPIValuesRequest
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
            data: CRMDetailsConfigurationSectionsData,
            user_id: Optional[int] = MISSING,
            scope: Optional[str] = MISSING,
            extras: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            scope: Optional[str] = MISSING,
            extras: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            extras: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
