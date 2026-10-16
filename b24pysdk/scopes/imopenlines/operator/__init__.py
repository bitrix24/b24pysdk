from functools import cached_property
from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .another import Another

__all__ = [
    "Operator",
]


class Operator(BaseEntity):
    """Class for managing operators work with open channel dialogues.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/index.html
    """

    @cached_property
    def another(self) -> Another:
        """"""
        return Another(self)

    @type_checker
    def answer(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Take the dialogue for yourself

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-answer.html

        The method assigns the dialog of the open line to the current operator.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.answer,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def finish(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Finish dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-finish.html

        The method ends the open line dialogue on behalf of the current operator.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.finish,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def skip(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Skip dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-skip.html

        The method transfers the current dialog to the next operator in the queue.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.skip,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def spam(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark a conversation as 'spam'

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-spam.html

        The method marks an open line as spam and ends it.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.spam,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def transfer(
            self,
            chat_id: Union[int, Text],
            *,
            transfer_id: Optional[Union[int, Text]] = MISSING,
            user_id: Optional[int] = MISSING,
            queue_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Transfer dialog to another operator or to another line

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/operators/imopenlines-operator-transfer.html

        The method transfers a dialog to another operator or to the queue of another open line.

        Args:
            chat_id: Identifier of the open line chat;

            transfer_id: Universal parameter for transferring the dialog;

            user_id: Identifier of the operator to whom the dialog should be transferred;

            queue_id: Identifier of the line to which the dialog should be transferred;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        if transfer_id is not MISSING:
            params["TRANSFER_ID"] = transfer_id

        if user_id is not MISSING:
            params["USER_ID"] = transfer_id

        if queue_id is not MISSING:
            params["QUEUE_ID"] = transfer_id

        return self._make_bitrix_api_request(
            api_wrapper=self.transfer,
            params=params,
            timeout=timeout,
        )
