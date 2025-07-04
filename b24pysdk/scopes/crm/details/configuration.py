from typing import Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..item.details.configuration import Configuration as BaseConfiguration


class Configuration(BaseConfiguration):
    """The group of methods manages the settings of the card for two views: 'General view' and 'My view'

    Documentation:
    """

    @type_checker
    def get(
            self,
            *args,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Get parameters of deal configuration.

        Documentation:

        The method retrieves the settings of deal cards.

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
            entity_type_id=self.details.entity_type_id,
            user_id=user_id,
            scope=scope,
            extras=extras,
        )

    @type_checker
    def set(
            self,
            *args,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Set parameters for the CRM deal detail card.

        Documentation:

        The method allows you to set the settings for deal cards.

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
            entity_type_id=self.details.entity_type_id,
            data=list(),
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def reset(
            self,
            *args,
            scope: Optional[Text] = None,
            user_id: Optional[int] = None,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """The method resets the settings of deal cards.

        Documentation:

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
            entity_type_id=self.details.entity_type_id,
            user_id=user_id,
            scope=scope,
            extras=extras,
            timeout=timeout,
        )

    @type_checker
    def force_common_scope_for_all(
            self,
            *args,
            extras: Optional[JSONDict] = None,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Set common deal card.

        Documentation:

        The method forcibly sets a common deal card for all users.

        Args:
            extras: Additional parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._force_common_scope_for_all(
            entity_type_id=self.details.entity_type_id,
            extras=extras,
            timeout=timeout,
        )
