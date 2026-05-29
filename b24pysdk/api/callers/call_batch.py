from typing import Dict, Final, Mapping, Optional, Sequence, Text, Union, overload

from ..._constants import MAX_BATCH_SIZE
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...utils.encoding import encode_params
from ...utils.types import B24APIVersionLiteral, B24Requests, B24RequestTuple, JSONDict, Key, Timeout
from ._base_caller import BaseCaller
from .call_method import call_method

__all__ = [
    "call_batch",
]


class _BatchCaller(BaseCaller):
    """
    Caller for one classic Bitrix ``batch`` request.

    The classic batch API accepts a ``cmd`` mapping where every value is encoded
    as ``method?query``. This caller validates the number of commands according
    to the SDK classic batch limit and serializes method tuples into that
    Bitrix format.
    """

    _API_METHOD: Final[Text] = "batch"
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_halt", "_ignore_size_limit", "_methods")

    _methods: B24Requests
    _halt: bool
    _ignore_size_limit: bool

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            methods: B24Requests,
            halt: bool = False,
            ignore_size_limit: bool = False,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        """
        Initialize a classic batch request.

        Args:
            domain: Bitrix24 portal domain.
            auth_token: OAuth access token or webhook token.
            is_webhook: Whether ``auth_token`` is a webhook token.
            methods: Mapping or sequence of ``(api_method, params)`` tuples.
            halt: Whether Bitrix should stop executing commands after the first
                failed command.
            ignore_size_limit: When ``True``, truncate command collection to the
                SDK batch limit instead of raising ``ValueError``.
            prefer_version: Preferred API version for resolving the ``batch``
                call itself.
            bitrix_token: Optional token wrapper used to execute nested calls
                through retry and refresh logic.
            **kwargs: Extra requester options forwarded to lower-level callers.
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
        self._halt = halt
        self._ignore_size_limit = ignore_size_limit
        self._methods = self._validate_methods(methods)

    def _validate_methods(self, methods: B24Requests) -> B24Requests:
        """
        Validate command count against the classic batch size limit.

        Returns the original collection when it fits the limit. If the
        collection is too large, either truncates it when ``ignore_size_limit``
        is enabled or raises ``ValueError`` to prevent an invalid API request.
        """
        if len(methods) > self._MAX_BATCH_SIZE:
            if self._ignore_size_limit:

                message = f"Batch size {len(methods)} exceeds limit {MAX_BATCH_SIZE}. Truncating to first {MAX_BATCH_SIZE} requests."
                self._config.logger.warning(message)

                if isinstance(methods, Mapping):
                    return dict(list(methods.items())[:self._MAX_BATCH_SIZE])
                else:
                    return methods[:self._MAX_BATCH_SIZE]
            else:
                raise ValueError(f"Maximum batch size is {MAX_BATCH_SIZE}!")
        else:
            return methods

    @property
    def _cmd(self) -> Dict[Key, Text]:
        """
        Serialize batch method tuples into Bitrix ``cmd`` format.

        Mapping input preserves caller-provided keys in the response. Sequence
        input uses numeric indexes. Method parameters are URL-encoded because
        the classic batch endpoint expects each command as a query string.
        """

        cmd: Dict[Key, Text] = dict()

        if isinstance(self._methods, Mapping):
            for key, (api_method, params) in self._methods.items():
                cmd[key] = f"{api_method}?{encode_params(params)}"
        else:
            for index, (api_method, params) in enumerate(self._methods):
                cmd[index] = f"{api_method}?{encode_params(params)}"

        return cmd

    @property
    def _dynamic_params(self) -> JSONDict:
        """Return the payload expected by the classic Bitrix ``batch`` method."""
        return dict(cmd=self._cmd, halt=self._halt)

    def _fetch_response(self) -> JSONDict:
        """
        Execute the batch request through the token wrapper or raw method caller.

        When a ``BitrixToken`` wrapper is available, nested execution goes
        through token retry/refresh logic. Otherwise the function calls the
        low-level ``call_method`` directly with stored auth context.
        """
        if self._bitrix_token:
            return self._bitrix_token.call_method(
                api_method=self._api_method,
                params=self._dynamic_params,
                **self._kwargs,
            )
        else:
            return call_method(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                api_method=self._api_method,
                params=self._dynamic_params,
                **self._kwargs,
            )

    def call(self) -> JSONDict:
        """Execute the configured batch request and return the parsed response."""
        return self._fetch_response()


@overload
def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Mapping[Key, B24RequestTuple],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict: ...


@overload
def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: Sequence[B24RequestTuple],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict: ...


def call_batch(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        methods: B24Requests,
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict:
    """
    Execute multiple Bitrix REST methods in one classic ``batch`` request.

    The classic batch endpoint accepts up to ``MAX_BATCH_SIZE`` commands in one
    call. This helper is intended for one physical batch request; use
    ``call_batches`` when the command collection can exceed that limit and
    should be split into several batch requests automatically.

    Args:
        domain: Bitrix24 portal domain.
        auth_token: OAuth access token or webhook token.
        is_webhook: Whether ``auth_token`` is a webhook token.
        methods: Mapping or sequence of ``(api_method, params)`` tuples. Mapping
            keys are used as result keys returned by Bitrix.
        halt: Whether Bitrix should stop on the first command error.
        ignore_size_limit: Truncate to ``MAX_BATCH_SIZE`` instead of raising when
            too many commands are passed.
        timeout: Request timeout in seconds.
        prefer_version: Preferred API version to resolve the ``batch`` method.
        bitrix_token: Optional token wrapper used by nested execution.
        **kwargs: Extra requester options, such as retry configuration.

    Returns:
        Parsed Bitrix batch response with command results, command errors, and
        timing metadata.
    """
    return _BatchCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        methods=methods,
        halt=halt,
        ignore_size_limit=ignore_size_limit,
        timeout=timeout,
        prefer_version=prefer_version,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
