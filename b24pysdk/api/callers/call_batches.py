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
    """"""

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
        """"""
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
        """"""
        if isinstance(self._methods, Mapping):
            return list(self._methods.items())
        else:
            return list(enumerate(self._methods))

    @staticmethod
    def _force_dict(collection: Union[Dict, List]) -> JSONDict:
        """
        Batch method can return its results in the form of either a dictionary or a list.
        This function converts results to dictionaries for uniformity.
        """
        if isinstance(collection, dict):
            return collection
        else:
            return {str(index): element for index, element in enumerate(collection)}

    def _combine_responses(self, responses: JSONList) -> JSONDict:
        """"""

        first_response, last_response = responses[0], responses[-1]

        combined_response: JSONDict = dict(
            result=dict(
                result=dict(),
                result_error=dict(),
                result_total=dict(),
                result_next=dict(),
                result_time=dict(),
            ),
            time=dict(
                start=first_response["time"]["start"],
                finish=last_response["time"]["finish"],
                duration=0,
                processing=0,
                date_start=first_response["time"]["date_start"],
                date_finish=last_response["time"]["date_finish"],
            ),
        )

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
        """"""

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
    Using 'batch' API method, call multiple API methods in one hit to Bitrix for performance benefits. Unlike call_batch(), works with any number of API methods

    Note: one call to batch method allows you to make up to 50 actual REST API requests in one hit, mitigating requests intensity limits.

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        methods:
                Collection of methods to call. Each item in a collection should be a tuple containing rest api method and its parameters.
                If the collection provided is a mapping, its keys are used to assosiate methods with their respective results.
        halt: whether to halt the sequence of requests in case of an error
        timeout: timeout in seconds
        prefer_version: preferred API version to resolve the batch method against
        bitrix_token:

    Returns:
        dictionary containing the result of the batch method call and information about call time
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
