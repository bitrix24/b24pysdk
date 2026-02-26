from functools import cached_property
from typing import Annotated, Iterable, Literal, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM
from .items import Items

__all__ = [
    "Calllist",
]


class Calllist(BaseCRM):
    """The class provides capabilities for managing methods that allows to call multiple clients in succession.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/index.html
    """

    @cached_property
    def items(self) -> Items:
        """"""
        return Items(self)

    @type_checker
    def add(
            self,
            *,
            entity_type: Annotated[Text, Literal["CONTACT", "COMPANY"]],
            entities: Iterable[int],
            webform_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new call list.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-add.html

        The method creates a new call list.

        Args:
            entity_type: Type of the object:

                - CONTACT - for contact,

                - COMPANY - for company;

            entities: Array of IDs of contacts or companies;

            webform_id: ID of the CRM form that will be displayed in call list form;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if entities.__class__ is not list:
            entities = list(entities)

        params = {
            "ENTITY_TYPE": entity_type,
            "ENTITIES": entities,
        }

        if webform_id is not None:
            params["WEBFORM_ID"] = webform_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the call list.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-get.html

        The method returns information about the call list by its identifier, without the list of participants.

        Args:
            bitrix_id: Identifier of the call list;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of call lists.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-list.html

        The method returns a list of call activities.

        Args:
            select: Array of fields to retrieve;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not None:
            params["FILTER"] = filter

        if order is not None:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def statuslist(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of call statuses.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-statuslist.html

        The method returns a list of call statuses.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.statuslist,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            *,
            list_id: int,
            entity_type: Annotated[Text, Literal["CONTACT", "COMPANY"]],
            entities: Iterable[int],
            webform_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update call list composition.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/call-list/crm-calllist-update.html

        The method allows you to add or remove participants from an existing call list and update the associated CRM form.

        Args:
            list_id: Identifier of the call list;

            entity_type: Type of the object:

                - CONTACT - for contact,

                - COMPANY - for company;

            entities: Array of IDs of contacts or companies;

            webform_id: ID of the CRM form that will be displayed in call list form;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if entities.__class__ is not list:
            entities = list(entities)

        params = {
            "LIST_ID": list_id,
            "ENTITY_TYPE": entity_type,
            "ENTITIES": entities,
        }

        if webform_id is not None:
            params["WEBFORM_ID"] = webform_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
