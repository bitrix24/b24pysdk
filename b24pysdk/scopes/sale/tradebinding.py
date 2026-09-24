from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Tradebinding",
]


class Tradebinding(BaseEntity):
    """Methods for managing order sources to orders links in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/trade-binding/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "tradeBinding"

    @type_checker
    def get_fields(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get available order fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/trade-binding/sale-trade-binding-get-fields.html

        The method returns the available order fields from sources.

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
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of orders from sources

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/trade-binding/sale-trade-binding-list.html

        The method returns a list of orders from sources.

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
