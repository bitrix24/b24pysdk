from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field

__all__ = [
    "Followup",
]


class Followup(BaseEntity):
    """Class for retrieving follow-up calls.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/follow-up/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def get(
            self,
            call_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            mention_format: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get call follow-up

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/follow-up/call-followup-get.html

        The method returns the follow-up of a single call by its identifier.

        Args:
            call_id: Call identifier;

            select: A list of fields and nested paths to be returned in the response;

            mention_format: Format for user mentions in AI text fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "callId": call_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if mention_format is not MISSING:
            params["mentionFormat"] = mention_format

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            filter: JSONDict,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            order: Optional[JSONDict] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            mention_format: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of follow-up calls

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/follow-up/call-followup-list.html

        The method returns a list of follow-up calls for a specified period.

        Args:
            filter: Selection criteria;

            select: List of fields and nested paths to be returned in the list items;

            order: Sorting parameters;

            pagination: Cursor pagination parameters;

            mention_format: Format for user mentions in AI text fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "filter": filter,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if order is not MISSING:
            params["order"] = order

        if pagination is not MISSING:
            params["pagination"] = pagination

        if mention_format is not MISSING:
            params["mentionFormat"] = mention_format

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
