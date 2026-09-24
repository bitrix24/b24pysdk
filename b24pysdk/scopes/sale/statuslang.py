from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Statuslang",
]


class Statuslang(BaseEntity):
    """Methods for managing localization of order and delivery statuses in online stores.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "statusLang"

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add localization

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/sale-status-lang-add.html

        The method adds localization for the order or delivery status.

        Args:
            fields: Field values for adding status localization;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_by_filter(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete localization

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/sale-status-lang-delete-by-filter.html

        The method deletes the localization records of the order or delivery status by status ID and language.

        Args:
            fields: Values of the filter fields for deleting the localization record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_by_filter,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get localization fields for statuses

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/sale-status-lang-get-fields.html

        The method retrieves the available localization fields for order or delivery statuses.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def get_list_langs(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of languages for localization

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/sale-status-lang-get-list-langs.html

        The method retrieves a list of possible languages for localizations.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list_langs,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of localizations

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/status-lang/sale-status-lang-list.html

        The method retrieves a list of localizations for order or delivery statuses.

        Args:
            select: An array of fields to be selected;

            filter: An object for filtering the selected records;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
