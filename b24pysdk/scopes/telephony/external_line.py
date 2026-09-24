from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ExternalLine",
]


class ExternalLine(BaseEntity):
    """Class for working with external telephony lines.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "externalLine"

    @type_checker
    def add(
            self,
            number: Text,
            *,
            name: Optional[Text] = MISSING,
            crm_auto_create: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add external line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-line-add.html

        The method adds an external line to the application.

        Args:
            number: External line number;

            name: External line name;

            crm_auto_create: Auto-creation of a CRM object for outgoing calls;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "NUMBER": number,
        }

        if name is not MISSING:
            params["NAME"] = name

        if crm_auto_create is not MISSING:
            params["CRM_AUTO_CREATE"] = bool_to_bitrix(crm_auto_create, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            number: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete external line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-line-delete.html

        The method removes an external line from the application.

        Args:
            number: The number of the external line;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "NUMBER": number,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of external lines

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-line-get.html

        The method returns a list of external lines for the application.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            *,
            number: Optional[Text] = MISSING,
            name: Optional[Text] = MISSING,
            crm_auto_create: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update external line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/telephony-external-line-update.html

        The method modifies the parameters of the application's external line.

        Args:
            number: The number of the external line;

            name: External line name;

            crm_auto_create: Auto-creation of a CRM object for outgoing calls

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if number is not MISSING:
            params["NUMBER"] = number

        if name is not MISSING:
            params["NAME"] = name

        if crm_auto_create is not MISSING:
            params["CRM_AUTO_CREATE"] = bool_to_bitrix(crm_auto_create, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params or None,
            timeout=timeout,
        )
