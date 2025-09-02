from typing import Dict, Final, List, Mapping, Sequence, Text, Tuple, Union, overload

from ..._constants import MAX_BATCH_SIZE
from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Key, Timeout
from ._base_caller import BaseCaller
from .call_batch import call_batch

_BatchMethods = Union[Mapping[Key, B24BatchRequestData], Sequence[B24BatchRequestData]]


class _BatchesCaller(BaseCaller):
    """"""

    _API_METHOD: Final[Text] = "batch"
    _BATCH_RESULT_FIELDS: Final[Tuple] = ("result", "result_error", "result_total", "result_next", "result_time")
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_halt", "_methods")

    _methods: _BatchMethods
    _halt: bool

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            methods: _BatchMethods,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ):
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=self._API_METHOD,
            timeout=timeout,
            **kwargs,
        )
        self._methods = methods
        self._halt = halt

    def _fetch_batch_response(self, methods: _BatchMethods) -> JSONDict:
        """"""
        return call_batch(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=methods,
            halt=self._halt,
            timeout=self._timeout,
            **self._kwargs,
        )

    def _get_flat_methods(self) -> List[Tuple[Key, B24BatchRequestData]]:
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

        if last_response["time"].get("operating_reset_at") is not None:
            combined_response["time"]["operating_reset_at"] = last_response["time"]["operating_reset_at"]

        if last_response["time"].get("operating") is not None:
            combined_response["time"]["operating"] = last_response["time"]["operating"]

        for response in responses:
            result = response["result"]
            time = response["time"]

            for key in self._BATCH_RESULT_FIELDS:
                combined_response["result"][key].update(self._force_dict(result.get(key, {})))

            combined_response["time"]["duration"] += time["duration"]
            combined_response["time"]["processing"] += time["processing"]

        return combined_response

    def call(self) -> JSONDict:
        """"""

        total_methods = len(self._methods)

        if total_methods <= self._MAX_BATCH_SIZE:
            return self._fetch_batch_response(methods=self._methods)

        flat_methods: List[Tuple[Key, B24BatchRequestData]] = self._get_flat_methods()

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
        methods: Mapping[Key, B24BatchRequestData],
        halt: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict: ...


@overload
def call_batches(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Sequence[B24BatchRequestData],
        halt: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict: ...


def call_batches(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: _BatchMethods,
        halt: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict:
    """
    Using 'batch' API method, call multiple API methods in one hit to Bitrix for performance benefits. Unlike call_batch(), works with any number of API methods

    Note: one call to batch method allows you to make up to 50 actual REST API requests in one hit, mitigating request intensity limits.

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        methods:
                Collection of methods to call. Each item in a collection should be a tuple containing rest api method and its parameters.
                If the collection provided is a mapping, its keys are used to assosiate methods with their respective results.
        halt: whether to halt the sequence of requests in case of an error
        timeout: timeout in seconds

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
        **kwargs,
    ).call()
