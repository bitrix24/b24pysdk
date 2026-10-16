from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Mode",
]


class Mode(BaseEntity):
    """Class for managing dialog modes for operators.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def pin(
            self,
            chat_id: Union[int, Text],
            *,
            activate: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Pin or unpin a dialog

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-mode-pin.html

        The method pins or unpins a dialog to the current operator.

        Args:
            chat_id: Identifier of the open line chat;

            activate: Pinning flag;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        if activate is not MISSING:
            params["ACTIVATE"] = bool_to_bitrix(activate, is_required=True)

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
        """Pin all available dialogs to the operator

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-mode-pin-all.html

        The method pins all available active dialogs to the current operator.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.pin_all,
            timeout=timeout,
        )

    @type_checker
    def silent(
            self,
            chat_id: Union[int, Text],
            *,
            activate: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Switch the dialog to silent mode

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-mode-silent.html

        The method enables or isables the silent messaging mode in the dialog.

        Args:
            chat_id: Identifier of the open line chat;

            activate: Activation flag;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        if activate is not MISSING:
            params["ACTIVATE"] = bool_to_bitrix(activate, is_required=True)

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
        """Unpin all operator dialogs

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-mode-unpin-all.html

        The method unpins all available pinned dialogs from the current operator.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.unpin_all,
            timeout=timeout,
        )
