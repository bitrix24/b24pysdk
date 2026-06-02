from typing import Dict, Final, List, Mapping, Optional, Sequence, Text, Tuple, Union, overload

from ..._constants import MAX_BATCH_SIZE
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...utils.types import B24APIVersionLiteral, B24Requests, B24RequestTuple, JSONDict, JSONList, Key, Timeout
from ._base_caller import BaseCaller
from .call_batch import call_batch

__all__ = [
    "call_batches",
]


class _BatchesCaller(BaseCaller):
    """
    Caller that executes an arbitrary number of methods via classic batch chunks.

    Bitrix classic batch has a per-request command limit. This caller splits a
    large method collection into chunks, executes each chunk with ``call_batch``,
    and merges all batch responses into one response shaped like a normal batch
    result.
    """

    _API_METHOD: Final[Text] = "batch"
    _BATCH_RESULT_FIELDS: Final[Tuple] = ("result", "result_error", "result_total", "result_next", "result_time")
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_halt", "_methods")

    _methods: B24Requests
    _halt: bool

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            methods: B24Requests,
            halt: bool = False,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        """
        Initialize a multi-batch caller.

        Args:
            domain: Bitrix24 portal domain.
            auth_token: OAuth access token or webhook token.
            is_webhook: Whether ``auth_token`` is a webhook token.
            methods: Mapping or sequence of ``(api_method, params)`` tuples.
            halt: Stop processing further chunks when a batch response contains
                command errors.
            prefer_version: Preferred API version for resolving the ``batch``
                calls.
            bitrix_token: Optional token wrapper used to execute nested calls
                through retry and refresh logic.
            **kwargs: Extra requester options forwarded to ``call_batch``.
        """
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=self._API_METHOD,
            prefer_version=prefer_version,
            bitrix_token=bitrix_token,
            **kwargs,
        )
        self._methods = methods
        self._halt = halt

    def _fetch_batch_response(self, methods: B24Requests) -> JSONDict:
        """Execute one classic batch chunk using the current auth context."""
        return call_batch(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=methods,
            halt=self._halt,
            bitrix_token=self._bitrix_token,
            **self._kwargs,
        )

    def _get_flat_methods(self) -> List[Tuple[Key, B24RequestTuple]]:
        """
        Return methods as ``(result_key, request_tuple)`` pairs.

        Mapping input keeps caller-provided keys. Sequence input receives
        numeric indexes so merged results can still be addressed consistently.
        """
        if isinstance(self._methods, Mapping):
            return list(self._methods.items())
        else:
            return list(enumerate(self._methods))

    @staticmethod
    def _force_dict(collection: Union[Dict, List]) -> JSONDict:
        """
        Normalize a batch result section to a dictionary.

        Bitrix can return command results as either a dictionary keyed by
        command names or a list keyed by command position. The merge code works
        with dictionaries, so list-shaped sections are converted to
        ``{"0": item0, "1": item1, ...}``.
        """
        if isinstance(collection, dict):
            return collection
        else:
            return {str(index): element for index, element in enumerate(collection)}

    def _combine_responses(self, responses: JSONList) -> JSONDict:
        """
        Merge several classic batch responses into a single batch-like response.

        Command result sections are normalized to dictionaries and combined by
        key. Timing fields are aggregated so the final response describes the
        whole multi-batch operation.
        """

        first_response, last_response = responses[0], responses[-1]

        combined_response: JSONDict = {
            "result": {
                "result": {},
                "result_error": {},
                "result_total": {},
                "result_next": {},
                "result_time": {},
            },
            "time": {
                "start": first_response["time"]["start"],
                "finish": last_response["time"]["finish"],
                "duration": 0,
                "processing": 0,
                "date_start": first_response["time"]["date_start"],
                "date_finish": last_response["time"]["date_finish"],
            },
        }

        combined_result: JSONDict = combined_response["result"]
        combined_time: JSONDict = combined_response["time"]

        operating_reset_at = last_response["time"].get("operating_reset_at")

        if operating_reset_at is not None:
            combined_time["operating_reset_at"] = operating_reset_at

        for response in responses:
            result = response["result"]
            time = response["time"]

            for key in self._BATCH_RESULT_FIELDS:
                value = result.get(key)

                if value:
                    combined_result[key].update(self._force_dict(value))

            combined_time["duration"] += time["duration"]
            combined_time["processing"] += time["processing"]

            operating = time.get("operating")

            if operating is not None:
                combined_time["operating"] = combined_time.get("operating", 0) + operating

        return combined_response

    def call(self) -> JSONDict:
        """
        Execute all configured methods, splitting them into batch-size chunks.

        If the collection fits into one classic batch request, the method
        delegates directly to ``call_batch``. Larger collections are split into
        ``MAX_BATCH_SIZE`` chunks and their responses are merged.
        """

        total_methods = len(self._methods)

        if total_methods <= self._MAX_BATCH_SIZE:
            return self._fetch_batch_response(methods=self._methods)

        flat_methods: List[Tuple[Key, B24RequestTuple]] = self._get_flat_methods()

        batch_responses: JSONList = list()

        for index in range(0, total_methods, self._MAX_BATCH_SIZE):
            methods_chunk = dict(flat_methods[index:index + self._MAX_BATCH_SIZE])
            batch_response = self._fetch_batch_response(methods=methods_chunk)
            batch_responses.append(batch_response)

            if self._halt and batch_response["result"]["result_error"]:
                break

        return self._combine_responses(batch_responses)


@overload
def call_batches(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Mapping[Key, B24RequestTuple],
        halt: bool = False,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        timeout: Timeout = None,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict: ...


@overload
def call_batches(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Sequence[B24RequestTuple],
        halt: bool = False,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        timeout: Timeout = None,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict: ...


def call_batches(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: B24Requests,
        halt: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict:
    """
    Execute any number of Bitrix REST methods through classic batch requests.

    Unlike ``call_batch``, this helper accepts collections larger than one
    classic batch request. It splits them into ``MAX_BATCH_SIZE`` chunks,
    executes the chunks sequentially, and returns a merged batch-like response.

    Args:
        domain: Bitrix24 portal domain.
        auth_token: OAuth access token or webhook token.
        is_webhook: Whether ``auth_token`` is a webhook token.
        methods: Mapping or sequence of ``(api_method, params)`` tuples. Mapping
            keys are used as result keys returned by Bitrix.
        halt: Stop processing further chunks when a command error appears.
        timeout: Request timeout in seconds.
        prefer_version: Preferred API version to resolve the ``batch`` method.
        bitrix_token: Optional token wrapper used by nested execution.
        **kwargs: Extra requester options, such as retry configuration.

    Returns:
        Parsed merged batch response with command results, errors, pagination
        metadata returned by Bitrix, and aggregated timing.
    """
    return _BatchesCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        methods=methods,
        halt=halt,
        timeout=timeout,
        prefer_version=prefer_version,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
