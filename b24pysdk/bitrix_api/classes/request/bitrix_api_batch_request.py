from typing import TYPE_CHECKING, Dict, Final, List, Mapping, Optional, Sequence, Text, Union, overload

from ....utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from ..response import B24APIBatchResult, BitrixAPIBatchResponse
from .bitrix_api_request import BitrixAPIRequest

if TYPE_CHECKING:
    from ...bitrix_token import AbstractBitrixToken


class BitrixAPIBatchesRequest(BitrixAPIRequest):
    """"""

    _API_METHOD: Final[Text] = "batch"

    __slots__ = ("_bitrix_api_requests", "_halt")

    _bitrix_api_requests: Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]]
    _halt: bool
    _response: Optional[BitrixAPIBatchResponse]

    @overload
    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Mapping[Key, BitrixAPIRequest],
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ): ...

    @overload
    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Sequence[BitrixAPIRequest],
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ): ...

    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            api_method=self._API_METHOD,
            timeout=timeout,
            **kwargs,
        )
        self._bitrix_api_requests = bitrix_api_requests
        self._halt = halt

    def __str__(self):
        return f"<{self.__class__.__name__} {self._api_method}({self._bitrix_api_requests_string})>"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"bitrix_api_requests={self._bitrix_api_requests_string}, "
            f"halt={self._halt}, "
            f"timeout={self._timeout})"
        )

    @overload
    @property
    def bitrix_api_requests(self) -> Mapping[Key, BitrixAPIRequest]: ...

    @overload
    @property
    def bitrix_api_requests(self) -> Sequence[BitrixAPIRequest]: ...

    @property
    def bitrix_api_requests(self) -> Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]]:
        """"""
        return self._bitrix_api_requests

    @property
    def _bitrix_api_requests_string(self) -> Text:
        """"""
        return f"<{type(self._bitrix_api_requests).__name__} of {len(self._bitrix_api_requests)} BitrixAPIRequests>"

    @property
    def halt(self) -> bool:
        """"""
        return self._halt

    @overload
    @property
    def methods(self) -> Mapping[Key, B24BatchRequestData]: ...

    @overload
    @property
    def methods(self) -> Sequence[B24BatchRequestData]: ...

    @property
    def methods(self) -> Union[Dict[Key, B24BatchRequestData], List[B24BatchRequestData]]:
        """"""

        if isinstance(self._bitrix_api_requests, Mapping):
            methods = dict()

            for key, bitrix_api_request in self.bitrix_api_requests.items():
                methods[key] = bitrix_api_request._as_tuple

        else:
            methods = list()

            for bitrix_api_request in self.bitrix_api_requests:
                methods.append(bitrix_api_request._as_tuple)

        return methods

    @property
    def response(self) -> BitrixAPIBatchResponse:
        """"""
        return self._response or self.call()

    @property
    def result(self) -> B24APIBatchResult:
        """"""
        return self.response.result

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batches(
            methods=self.methods,
            halt=self._halt,
            timeout=self._timeout,
            **self._kwargs,
        )

    def call(self) -> BitrixAPIBatchResponse:
        """"""
        self._response = BitrixAPIBatchResponse.from_dict(self._call())
        return self._response


class BitrixAPIBatchRequest(BitrixAPIBatchesRequest):
    """"""

    __slots__ = ("_ignore_size_limit",)

    _ignore_size_limit: bool

    @overload
    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Mapping[Key, BitrixAPIRequest],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ): ...

    @overload
    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Sequence[BitrixAPIRequest],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ): ...

    def __init__(
            self,
            *,
            bitrix_token: "AbstractBitrixToken",
            bitrix_api_requests: Union[Mapping[Key, BitrixAPIRequest], Sequence[BitrixAPIRequest]],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            timeout=timeout,
            **kwargs,
        )
        self._ignore_size_limit = ignore_size_limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"bitrix_api_requests={self._bitrix_api_requests_string}, "
            f"halt={self._halt}, "
            f"ignore_size_limit={self._ignore_size_limit}, "
            f"timeout={self._timeout})"
        )

    @property
    def ignore_size_limit(self) -> bool:
        """"""
        return self._ignore_size_limit

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batch(
            methods=self.methods,
            halt=self._halt,
            ignore_size_limit=self._ignore_size_limit,
            timeout=self._timeout,
            **self._kwargs,
        )
