from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Last",
]


class Last(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            skip_openlines: Optional[Union[bool, B24BoolStrict]] = None,
            skip_chat: Optional[Union[bool, B24BoolStrict]] = None,
            skip_dialog: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if skip_openlines is not None:
            params["SKIP_OPENLINES"] = B24BoolStrict(skip_openlines).to_b24()

        if skip_chat is not None:
            params["SKIP_CHAT"] = B24BoolStrict(skip_chat).to_b24()

        if skip_dialog is not None:
            params["SKIP_DIALOG"] = B24BoolStrict(skip_dialog).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
