from typing import Optional, Text, Union

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
            last_id: Optional[Union[int, Text]] = None,
            first_id: Optional[Union[int, Text]] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if last_id is not None:
            params["LAST_ID"] = last_id

        if first_id is not None:
            params["FIRST_ID"] = first_id

        if limit is not None:
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
            search_message: Optional[Text] = None,
            date_from: Optional[Text] = None,
            date_to: Optional[Text] = None,
            date: Optional[Text] = None,
            order: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            last_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "CHAT_ID": chat_id,
        }

        if search_message is not None:
            params["SEARCH_MESSAGE"] = search_message

        if date_from is not None:
            params["DATE_FROM"] = date_from

        if date_to is not None:
            params["DATE_TO"] = date_to

        if date is not None:
            params["DATE"] = date

        if order is not None:
            params["ORDER"] = order

        if limit is not None:
            params["LIMIT"] = limit

        if last_id is not None:
            params["LAST_ID"] = last_id

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )
