from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Messages",
]


class Messages(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            dialog_id: Text,
            *,
            last_id: Optional[Union[int, Text]] = MISSING,
            first_id: Optional[Union[int, Text]] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if first_id is not MISSING:
            params["FIRST_ID"] = first_id

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            chat_id: int,
            *,
            search_message: Optional[Text] = MISSING,
            date_from: Optional[Text] = MISSING,
            date_to: Optional[Text] = MISSING,
            date: Optional[Text] = MISSING,
            order: Optional[JSONDict] = MISSING,
            limit: Optional[int] = MISSING,
            last_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params: JSONDict = {
            "CHAT_ID": chat_id,
        }

        if search_message is not MISSING:
            params["SEARCH_MESSAGE"] = search_message

        if date_from is not MISSING:
            params["DATE_FROM"] = date_from

        if date_to is not MISSING:
            params["DATE_TO"] = date_to

        if date is not MISSING:
            params["DATE"] = date

        if order is not MISSING:
            params["ORDER"] = order

        if limit is not MISSING:
            params["LIMIT"] = limit

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )
