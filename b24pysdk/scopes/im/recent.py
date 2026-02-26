from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Recent",
]


class Recent(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            skip_openlines: Optional[Union[bool, B24BoolStrict]] = None,
            skip_chat: Optional[Union[bool, B24BoolStrict]] = None,
            skip_dialog: Optional[Union[bool, B24BoolStrict]] = None,
            last_update: Optional[Text] = None,
            only_openlines: Optional[Union[bool, B24BoolStrict]] = None,
            last_sync_date: Optional[Text] = None,
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

        if last_update is not None:
            params["LAST_UPDATE"] = last_update

        if only_openlines is not None:
            params["ONLY_OPENLINES"] = B24BoolStrict(only_openlines).to_b24()

        if last_sync_date is not None:
            params["LAST_SYNC_DATE"] = last_sync_date

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            skip_openlines: Optional[Union[bool, B24BoolStrict]] = None,
            skip_dialog: Optional[Union[bool, B24BoolStrict]] = None,
            skip_chat: Optional[Union[bool, B24BoolStrict]] = None,
            last_message_date: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if skip_openlines is not None:
            params["SKIP_OPENLINES"] = B24BoolStrict(skip_openlines).to_b24()

        if skip_dialog is not None:
            params["SKIP_DIALOG"] = B24BoolStrict(skip_dialog).to_b24()

        if skip_chat is not None:
            params["SKIP_CHAT"] = B24BoolStrict(skip_chat).to_b24()

        if last_message_date is not None:
            params["LAST_MESSAGE_DATE"] = last_message_date

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def hide(
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
            api_wrapper=self.hide,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pin(
            self,
            dialog_id: Text,
            pin: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            PIN=B24BoolStrict(pin).to_b24(),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unread(
            self,
            dialog_id: Text,
            action: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
            ACTION=B24BoolStrict(action).to_b24(),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.unread,
            params=params,
            timeout=timeout,
        )
