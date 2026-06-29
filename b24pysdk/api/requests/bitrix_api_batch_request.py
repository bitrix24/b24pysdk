from typing import TYPE_CHECKING, Final, Generic, Mapping, Sequence, Text, overload

from ...protocols import BitrixTokenFullProtocol
from ...schemas.api import BatchResponseData
from ...utils.type_vars import BABatchRequestsT
from ...utils.types import B24Requests, B24RequestTuple, Key
from ..responses import B24APIBatchResult, BitrixAPIBatchResponse
from .bitrix_api_base_request import BitrixAPIBaseRequest

if TYPE_CHECKING:
    from .bitrix_api_request import BitrixAPIRequest

__all__ = [
    "BitrixAPIBatchRequest",
    "BitrixAPIBatchesRequest",
]


class BitrixAPIBatchesRequest(BitrixAPIBaseRequest[BitrixAPIBatchResponse, B24APIBatchResult], Generic[BABatchRequestsT]):
    """
    Lazy request object for executing multiple Bitrix24 batch requests.

    Accepts a mapping or sequence of ``BitrixAPIRequest`` objects, converts
    them into batch-compatible request tuples, and executes them through
    ``call_batches``.
    """

    _API_METHOD: Final[Text] = "batch"

    __slots__ = ("_bitrix_api_requests", "_halt")

    _bitrix_api_requests: BABatchRequestsT
    _halt: bool

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            bitrix_api_requests: BABatchRequestsT,
            halt: bool = False,
            **kwargs,
    ):
        """
        Initialize a multi-batch request.

        Args:
            bitrix_token: Token-like object used to execute Bitrix24 API calls.
            bitrix_api_requests: Mapping or sequence of request objects to execute.
            halt: Whether to stop batch execution after the first failed command.
            **kwargs: Extra options forwarded to the token call.
        """
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
        """
        Return the contained request class name for human-readable output.

        Returns:
            Request type name for the first item, or this class name when the
            request collection is empty.
        """

        if not self._bitrix_api_requests:
            return self.__class__.__name__

        if isinstance(self._bitrix_api_requests, Mapping):
            bitrix_api_request = next(iter(self._bitrix_api_requests.values()))
        else:
            bitrix_api_request = self._bitrix_api_requests[0]

        return type(bitrix_api_request).__name__

    @property
    def _bitrix_api_requests_string(self) -> Text:
        """
        Return a compact description of the wrapped request collection.

        Returns:
            String containing collection type, size, and request item type.
        """
        return f"<{type(self._bitrix_api_requests).__name__} of {len(self._bitrix_api_requests)} {self._bitrix_api_requests_type_string}>"

    @overload
    def _methods(self: "BitrixAPIBatchesRequest[Mapping[Key, BitrixAPIRequest]]") -> Mapping[Key, B24RequestTuple]: ...

    @overload
    def _methods(self: "BitrixAPIBatchesRequest[Sequence[BitrixAPIRequest]]") -> Sequence[B24RequestTuple]: ...

    @property
    def _methods(self) -> B24Requests:
        """
        Convert wrapped request objects into Bitrix batch method definitions.

        Preserves mapping keys for mapping input and preserves order for
        sequence input.

        Returns:
            Batch request definitions accepted by token batch callers.
        """

        if isinstance(self._bitrix_api_requests, Mapping):
            methods = {}

            for key, bitrix_api_request in self._bitrix_api_requests.items():
                bitrix_api_request: "BitrixAPIRequest"
                methods[key] = bitrix_api_request._as_tuple

        else:
            methods = []

            for bitrix_api_request in self._bitrix_api_requests:
                bitrix_api_request: "BitrixAPIRequest"
                methods.append(bitrix_api_request._as_tuple)

        return methods

    def _convert_response(self, json_response: BatchResponseData) -> BitrixAPIBatchResponse:
        """
        Convert raw JSON response into ``BitrixAPIBatchResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed Bitrix batch response.
        """
        return BitrixAPIBatchResponse.from_dict(json_response)

    def _call(self) -> BatchResponseData:
        """
        Execute wrapped requests using the multi-batch caller.

        Returns:
            Raw JSON response returned by ``call_batches``.
        """
        return self._bitrix_token.call_batches(
            methods=self._methods,
            halt=self._halt,
            **self._kwargs,
        )


class BitrixAPIBatchRequest(BitrixAPIBatchesRequest[BABatchRequestsT], Generic[BABatchRequestsT]):
    """
    Lazy request object for executing one Bitrix24 batch request.

    Accepts a mapping or sequence of ``BitrixAPIRequest`` objects, converts
    them into batch-compatible request tuples, and executes them through
    ``call_batch``.
    """

    __slots__ = ("_ignore_size_limit",)

    _ignore_size_limit: bool

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            bitrix_api_requests: BABatchRequestsT,
            halt: bool = False,
            ignore_size_limit: bool = False,
            **kwargs,
    ):
        """
        Initialize a single batch request.

        Args:
            bitrix_token: Token-like object used to execute Bitrix24 API calls.
            bitrix_api_requests: Mapping or sequence of request objects to execute.
            halt: Whether to stop batch execution after the first failed command.
            ignore_size_limit: When ``False``, raise ``ValueError`` if the command
                collection exceeds the SDK batch limit. When ``True``, truncate
                the collection to the allowed number of commands.
            **kwargs: Extra options forwarded to the token call.
        """
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

    def _call(self) -> BatchResponseData:
        """
        Execute wrapped requests using the single-batch caller.

        Returns:
            Raw JSON response returned by ``call_batch``.
        """
        return self._bitrix_token.call_batch(
            methods=self._methods,
            halt=self._halt,
            ignore_size_limit=self._ignore_size_limit,
            **self._kwargs,
        )
