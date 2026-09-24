from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity


class _BaseField(BaseEntity):
    """Methods for retrieving fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/mail/index.html
    """

    @type_checker
    def get(
            self,
            name: Text,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields description

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/index.html

        The method returns the description of a field by name.

        Args:
            name: Name of the field whose description is to be retrieved;

            select: List of description fields to be returned in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "name": name,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of fields

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/index.html

        The method returns a list of available fields.

        Args:
            select: List of description fields that need to be returned in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if select.__class__ is not list:
            select = list(select)

        params = {
            "select": select,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
