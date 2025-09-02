from typing import Dict, Final, Mapping, Sequence, Text, Union, overload

from ..._constants import MAX_BATCH_SIZE
from ...utils.encoding import encode_params
from ...utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from ._base_caller import BaseCaller
from .call_method import call_method

_BatchMethods = Union[Mapping[Key, B24BatchRequestData], Sequence[B24BatchRequestData]]


class _BatchCaller(BaseCaller):
    """"""

    _API_METHOD: Final[Text] = "batch"
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_halt", "_ignore_size_limit", "_methods")

    _methods: _BatchMethods
    _halt: bool
    _ignore_size_limit: bool

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            methods: _BatchMethods,
            halt: bool = False,
            ignore_size_limit: bool = False,
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
        self._halt = halt
        self._ignore_size_limit = ignore_size_limit
        self._methods = self._validate_methods(methods)

    def _validate_methods(self, methods: _BatchMethods) -> _BatchMethods:
        """"""
        if len(methods) > self._MAX_BATCH_SIZE:
            if self._ignore_size_limit:
                return methods[:self._MAX_BATCH_SIZE]
            else:
                raise ValueError(f"Maximum batch size is {MAX_BATCH_SIZE}!")
        else:
            return methods

    @property
    def _cmd(self) -> Dict[Key, Text]:
        """"""

        cmd = dict()

        if isinstance(self._methods, Mapping):
            for key, (api_method, params) in self._methods.items():
                cmd[key] = f"{api_method}?{encode_params(params)}"
        else:
            for index, (api_method, params) in enumerate(self._methods):
                cmd[index] = f"{api_method}?{encode_params(params)}"

        return cmd

    def _fetch_response(self) -> JSONDict:
        """"""
        return call_method(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            api_method=self._api_method,
            params=dict(
                cmd=self._cmd,
                halt=self._halt,
            ),
            timeout=self._timeout,
            **self._kwargs,
        )

    def call(self) -> JSONDict:
        """"""
        return self._fetch_response()


@overload
def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Mapping[Key, B24BatchRequestData],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict: ...


@overload
def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Sequence[B24BatchRequestData],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict: ...


def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: _BatchMethods,
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict:
    """
    Using 'batch' API method, call multiple API methods in one hit to Bitrix for performance benefits.

    Note: one call to batch method allows you to make up to 50 actual REST API requests in one hit, mitigating request intensity limits.

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        methods:
                Collection of methods to call. Each item in a collection should be a tuple containing rest api method and its parameters.
                If the collection provided is a mapping, its keys are used to assosiate methods with their respective results.
        halt: whether to halt the sequence of requests in case of an error
        ignore_size_limit: if the number of methods exceeds maximum, truncate methods sequence instead of raising an error
        timeout: timeout in seconds

    Returns:
        dictionary containing the result of the batch method call and information about call time
    """
    return _BatchCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        methods=methods,
        halt=halt,
        ignore_size_limit=ignore_size_limit,
        timeout=timeout,
        **kwargs,
    ).call()
