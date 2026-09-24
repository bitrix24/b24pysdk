from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Mailbox",
]


class Mailbox(BaseEntity):
    """Methods for retrieving user's mailboxes.

    Documentation: https://apidocs.bitrix24.com/api-reference/mail/mailbox/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get mailbox

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/mailbox/mail-mailbox-get.html

        The method retrieves a mailbox by its identifier.

        Args:
            bitrix_id: Mailbox identifier;

            select: Optional list of fields to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
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
            *,
            name: Optional[Text] = MISSING,
            email: Optional[Text] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of mailboxes

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/mailbox/mail-mailbox-list.html

        The method retrieves a list of the current user's mailboxes based on specified conditions.

        Args:
            name: Mailbox name fragment for filtering;

            email: Email fragment for filtering;

            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if name is not MISSING:
            params["name"] = name

        if email is not MISSING:
            params["email"] = email

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def senders(
            self,
            pagination: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get senders

        Documentation: https://apidocs.bitrix24.com/api-reference/mail/mailbox/mail-mailbox-senders.html

        The method returns a list of senders available to the current user.

        Args:
            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "pagination": pagination,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.senders,
            params=params,
            timeout=timeout,
        )
