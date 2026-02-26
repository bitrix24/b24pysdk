from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Mode",
]


class Mode(BaseEntity):
    """"""

    @type_checker
    def pin(
            self,
            chat_id: Union[int, Text],
            *,
            activate: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        if activate is not None:
            params["ACTIVATE"] = B24BoolStrict(activate).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pin_all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.pin_all,
            timeout=timeout,
        )

    @type_checker
    def silent(
            self,
            chat_id: Union[int, Text],
            *,
            activate: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        if activate is not None:
            params["ACTIVATE"] = B24BoolStrict(activate).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.silent,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpin_all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.unpin_all,
            timeout=timeout,
        )
