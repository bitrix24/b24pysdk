from typing import Dict, Optional, Sequence, Union

from . import scopes
from .bitrix_api.bitrix_token import AbstractBitrixToken
from .bitrix_api.classes import BitrixAPIBatchesRequest, BitrixAPIBatchRequest, BitrixAPIListRequest, BitrixAPIRequest
from .utils.types import Key, Timeout


class Client:
    """"""

    __slots__ = (
        "_bitrix_token",
        "crm",
        "user",
    )

    _bitrix_token: AbstractBitrixToken
    crm: scopes.CRM
    user: scopes.User

    def __init__(
            self,
            bitrix_token: AbstractBitrixToken,
    ):
        self._bitrix_token = bitrix_token
        self.crm = scopes.CRM(self)
        self.user = scopes.User(self)

    def __str__(self):
        return f"<Client of portal {self._bitrix_token.domain}>"

    def __repr__(self):
        return f"{self.__class__.__name__}(bitrix_token={self._bitrix_token})"

    def call_batch(
            self,
            bitrix_api_requests: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest:
        """"""
        return BitrixAPIBatchRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            ignore_size_limit=ignore_size_limit,
            timeout=timeout,
        )

    def call_batches(
            self,
            bitrix_api_requests: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchesRequest:
        """"""
        return BitrixAPIBatchesRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
        )

    def call_list(
            self,
            bitrix_api_request: BitrixAPIRequest,
            limit: Optional[int] = None,
    ) -> BitrixAPIListRequest:
        """"""
        return BitrixAPIListRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_request=bitrix_api_request,
            limit=limit,
        )
