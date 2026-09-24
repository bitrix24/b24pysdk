from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Fields",
]


class Fields(BaseEntity):
    """A set of methods for managing field visibility settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/fields/index.html
    """

    @type_checker
    def get_settings(
            self,
            type_id: int,
            *,
            stage_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the complete set of field visibility settings

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/fields/rpa-fields-get-settings.html

        This method retrieves the complete set of field visibility settings for the stage with the identifier stageId in the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            stage_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
        }

        if stage_id is not MISSING:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_settings,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_settings(
            self,
            type_id: int,
            fields: JSONDict,
            *,
            stage_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set full visibility settings

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/fields/rpa-fields-set-settings.html

        This method sets the full visibility settings for fields at the stage with the identifier stageId of the process with the identifier typeId.

        Args:
            type_id: Identifier of the process;

            fields: Array with fields visibility settings;

            stage_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
            "fields": fields,
        }

        if stage_id is not MISSING:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_settings,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_visibility_settings(
            self,
            type_id: int,
            visibility: Text,
            fields: Iterable[Text],
            *,
            stage_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change field visibility settings

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/fields/rpa-fields-set-visibility-settings.html

        This method updates the visibility settings of fields for the process with the identifier typeId at the stage with the identifier stageId.
        Other settings remain unchanged.

        Args:
            type_id: Identifier of the process;

            visibility: Identifier of the visibility for which the settings are being changed;

            fields: Array of fields for which the settings need to be changed;

            stage_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if fields.__class__ is not list:
            fields = list(fields)

        params: JSONDict = {
            "typeId": type_id,
            "visibility": visibility,
            "fields": fields,
        }

        if stage_id is not MISSING:
            params["stageId"] = stage_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_visibility_settings,
            params=params,
            timeout=timeout,
        )
