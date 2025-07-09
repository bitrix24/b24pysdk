from typing import Dict, Optional, Sequence, Union

from ...utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from ..bitrix_token import AbstractBitrixToken
from .bitrix_api_batch_response import B24APIBatchResult, BitrixAPIBatchResponse
from .bitrix_api_request import BitrixAPIRequest

API_METHOD = "batch"


class BitrixAPIBatchesRequest(BitrixAPIRequest):
    """"""

    __slots__ = ("_bitrix_api_request", "_halt")

    _bitrix_api_request: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]]
    _halt: bool
    _response: Optional[BitrixAPIBatchResponse]

    def __init__(
            self,
            *,
            bitrix_token: AbstractBitrixToken,
            bitrix_api_requests: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            timeout: Timeout = None,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            api_method=API_METHOD,
            timeout=timeout,
        )
        self._bitrix_api_request = bitrix_api_requests
        self._halt = halt

    @property
    def bitrix_api_requests(self) -> Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]]:
        return self._bitrix_api_request

    @property
    def halt(self) -> bool:
        return self._halt

    @property
    def methods(self) -> Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]]:
        if isinstance(self._bitrix_api_request, dict):
            methods = dict()

            for key, bitrix_api_request in self._bitrix_api_request.items():
                methods[key] = bitrix_api_request.as_tuple()

        else:
            methods = list()

            for bitrix_api_request in self._bitrix_api_request:
                methods.append(bitrix_api_request.as_tuple())

        return methods

    @property
    def response(self) -> BitrixAPIBatchResponse:
        return self._response or self.execute()

    @property
    def result(self) -> B24APIBatchResult:
        return self.response.result

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batches(
            methods=self.methods,
            halt=self._halt,
            timeout=self._timeout,
        )

    def execute(self) -> BitrixAPIBatchResponse:
        """"""
        self._response = BitrixAPIBatchResponse.from_dict(self._call())
        return self._response


class BitrixAPIBatchRequest(BitrixAPIBatchesRequest):
    """"""

    __slots__ = ("_ignore_size_limit",)

    _ignore_size_limit: bool

    def __init__(
            self,
            *,
            bitrix_token: AbstractBitrixToken,
            bitrix_api_requests: Union[Dict[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
        )
        self._ignore_size_limit = ignore_size_limit

    @property
    def ignore_size_limit(self) -> bool:
        return self._ignore_size_limit

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batch(
            methods=self.methods,
            halt=self._halt,
            ignore_size_limit=self._ignore_size_limit,
            timeout=self._timeout,
        )
