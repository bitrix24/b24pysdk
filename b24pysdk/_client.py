from typing import Dict, Sequence, Union

from . import scopes
from .bitrix_api.bitrix_token import AbstractBitrixToken
from .bitrix_api.classes import BitrixAPIBatchesRequest, BitrixAPIBatchRequest, BitrixAPIRequest
from .utils.types import Key, Timeout


class Client:
    """"""

    __slots__ = ("bitrix_token", "crm")

    bitrix_token: AbstractBitrixToken
    crm: scopes.CRM

    def __init__(self, bitrix_token: AbstractBitrixToken):
        self.bitrix_token = bitrix_token
        self.crm = scopes.CRM(self)

    def call_batch(
            self,
            bitrix_api_requests: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest:
        """"""
        return BitrixAPIBatchRequest(
            bitrix_token=self.bitrix_token,
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
    ):
        """"""
        return BitrixAPIBatchesRequest(
            bitrix_token=self.bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
        )
