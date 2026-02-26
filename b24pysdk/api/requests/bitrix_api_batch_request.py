from typing import TYPE_CHECKING, Final, Generic, Mapping, Sequence, Text, TypeVar, Union, overload

from ...protocols import BitrixTokenFullProtocol
from ...utils.types import B24Requests, B24RequestTuple, JSONDict, Key
from ..responses import BitrixAPIBatchResponse
from .bitrix_api_base_request import BitrixAPIBaseRequest

if TYPE_CHECKING:
    from .bitrix_api_request import BitrixAPIRequest

__all__ = [
    "BitrixAPIBatchRequest",
    "BitrixAPIBatchesRequest",
]

_BARQST = TypeVar(
    "_BARQST",
    bound=Union[
        Mapping[Key, "BitrixAPIRequest"],
        Sequence["BitrixAPIRequest"],
    ],
)


class BitrixAPIBatchesRequest(BitrixAPIBaseRequest[BitrixAPIBatchResponse], Generic[_BARQST]):
    """"""

    _API_METHOD: Final[Text] = "batch"

    __slots__ = ("_bitrix_api_requests", "_halt")

    _bitrix_api_requests: _BARQST
    _halt: bool

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            bitrix_api_requests: _BARQST,
            halt: bool = False,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            api_method=self._API_METHOD,
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
            f"halt={self._halt})"
        )

    @property
    def _bitrix_api_requests_type_string(self) -> Text:
        """"""
        return type(self._bitrix_api_requests[0]).__name__ if self._bitrix_api_requests else "BitrixAPIRequests"

    @property
    def _bitrix_api_requests_string(self) -> Text:
        """"""
        return f"<{type(self._bitrix_api_requests).__name__} of {len(self._bitrix_api_requests)} {self._bitrix_api_requests_type_string}>"

    @overload
    def _methods(self: "BitrixAPIBatchesRequest[Mapping[Key, BitrixAPIRequest]]") -> Mapping[Key, B24RequestTuple]: ...

    @overload
    def _methods(self: "BitrixAPIBatchesRequest[Sequence[BitrixAPIRequest]]") -> Sequence[B24RequestTuple]: ...

    @property
    def _methods(self) -> B24Requests:
        """"""

        if isinstance(self._bitrix_api_requests, Mapping):
            methods = dict()

            for key, bitrix_api_request in self._bitrix_api_requests.items():
                bitrix_api_request: "BitrixAPIRequest"
                methods[key] = bitrix_api_request._as_tuple

        else:
            methods = list()

            for bitrix_api_request in self._bitrix_api_requests:
                bitrix_api_request: "BitrixAPIRequest"
                methods.append(bitrix_api_request._as_tuple)

        return methods

    @staticmethod
    def _convert_response(json_response: JSONDict) -> BitrixAPIBatchResponse:
        """"""
        return BitrixAPIBatchResponse.from_dict(json_response)

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batches(
            methods=self._methods,
            halt=self._halt,
            **self._kwargs,
        )


class BitrixAPIBatchRequest(BitrixAPIBatchesRequest[_BARQST], Generic[_BARQST]):
    """"""

    __slots__ = ("_ignore_size_limit",)

    _ignore_size_limit: bool

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            bitrix_api_requests: _BARQST,
            halt: bool = False,
            ignore_size_limit: bool = False,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            bitrix_api_requests=bitrix_api_requests,
            halt=halt,
            **kwargs,
        )
        self._ignore_size_limit = ignore_size_limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"bitrix_api_requests={self._bitrix_api_requests_string}, "
            f"halt={self._halt}, "
            f"ignore_size_limit={self._ignore_size_limit})"
        )

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_batch(
            methods=self._methods,
            halt=self._halt,
            ignore_size_limit=self._ignore_size_limit,
            **self._kwargs,
        )
