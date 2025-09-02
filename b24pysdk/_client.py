from typing import Dict, Mapping, Sequence, Union, overload

from . import scopes
from .bitrix_api.bitrix_token import AbstractBitrixToken
from .bitrix_api.classes import BitrixAPIBatchesRequest, BitrixAPIBatchRequest, BitrixAPIRequest
from .utils.types import Key, Timeout


class Client:
    """"""

    __slots__ = (
        "_bitrix_token",
        "_kwargs",
        "crm",
        "department",
        "user",
    )

    _bitrix_token: AbstractBitrixToken
    _kwargs: Dict
    crm: scopes.CRM
    department: scopes.Department
    user: scopes.User

    def __init__(
            self,
            bitrix_token: AbstractBitrixToken,
            **kwargs,
    ):
        self._bitrix_token = bitrix_token
        self._kwargs = kwargs
        self.crm = scopes.CRM(self)
        self.department = scopes.Department(self)
        self.user = scopes.User(self)

    def __str__(self):
        return f"<Client of portal {self._bitrix_token.domain}>"

    def __repr__(self):
        return f"{self.__class__.__name__}(bitrix_token={self._bitrix_token})"

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Mapping[Key, BitrixAPIRequest],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    @overload
    def call_batch(
            self,
            bitrix_api_requests: Sequence[BitrixAPIRequest],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    def call_batch(
            self,
            bitrix_api_requests: Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
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
            **self._kwargs,
        )

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Mapping[Key, BitrixAPIRequest],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    @overload
    def call_batches(
            self,
            bitrix_api_requests: Sequence[BitrixAPIRequest],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchRequest: ...

    def call_batches(
            self,
            bitrix_api_requests: Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> BitrixAPIBatchesRequest:
        """"""
        return BitrixAPIBatchesRequest(
            bitrix_token=self._bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
            **self._kwargs,
        )
