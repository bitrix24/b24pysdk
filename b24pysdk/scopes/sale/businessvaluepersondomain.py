from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Businessvaluepersondomain",
]


class Businessvaluepersondomain(BaseEntity):
    """A set of methods for working with statuses of payer types in online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/business-value-person-domain/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "businessValuePersonDomain"

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add correspondence to a natural or legal person

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/business-value-person-domain/sale-business-value-person-domain-add.html

        The method adds correspondence for the selected payer type to a natural or legal person.

        Args:
             fields: Field values for creating correspondence to a natural or legal person;

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
        """Delete the correspondence with a natural or legal person

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/business-value-person-domain/sale-business-value-person-domain-delete-by-filter.html

        The method removes the correspondence with a natural or legal person.

        Args:
            fields: Field values for deleting the correspondence with a natural or legal person;

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
        """Get fields corresponding to a natural or legal person

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/business-value-person-domain/sale-business-value-person-domain-get-fields.html

        The method retrieves fields corresponding to a natural or legal person.

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
        """Get a list of matches for a natural or legal person

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/business-value-person-domain/sale-business-value-person-domain-list.html

        The method retrieves a list of payer type domain mappings.

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
