from typing import Mapping, Optional, Protocol, Sequence, Text, Union, overload

from ..constants.version import B24APIVersion
from ..schemas.api import BatchResponseData, ListFastResponseData, ListResponseData
from ..utils.types import B24APIVersionLiteral, B24Requests, B24RequestTuple, JSONDict, Key, Timeout


class BitrixTokenProtocol(Protocol):
    """
    Protocol for Bitrix24 token-like clients.

    Defines the minimal interface required to call a single Bitrix24 REST API
    method.
    """

    def call_method(
        self,
        api_method: Text,
        params: Optional[JSONDict] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> JSONDict:
        """
        Call a single Bitrix24 REST API method.

        Args:
            api_method: Bitrix24 REST API method name.
            params: Optional request parameters.
            timeout: Optional request timeout.
            prefer_version: Preferred Bitrix24 API version.

        Returns:
            API response as a JSON-compatible dictionary.
        """


class BitrixTokenFullProtocol(BitrixTokenProtocol, Protocol):
    """
    Extended protocol for full-featured Bitrix24 token clients.

    Adds batch calls and list-loading helpers to the basic single-method API.
    """

    @overload
    def call_batch(
        self,
        methods: Mapping[Key, B24RequestTuple],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData: ...

    @overload
    def call_batch(
        self,
        methods: Sequence[B24RequestTuple],
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData: ...

    def call_batch(
        self,
        methods: B24Requests,
        halt: bool = False,
        ignore_size_limit: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData:
        """
        Execute a Bitrix24 batch request.

        Args:
            methods: Batch methods as a mapping or sequence of request tuples.
            halt: Whether to stop execution after the first failed command.
            ignore_size_limit: Whether to skip SDK-side batch size validation.
            timeout: Optional request timeout.
            prefer_version: Preferred Bitrix24 API version.

        Returns:
            Batch API response as a JSON-compatible dictionary.
        """

    @overload
    def call_batches(
        self,
        methods: Mapping[Key, B24RequestTuple],
        halt: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData: ...

    @overload
    def call_batches(
        self,
        methods: Sequence[B24RequestTuple],
        halt: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData: ...

    def call_batches(
        self,
        methods: B24Requests,
        halt: bool = False,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> BatchResponseData:
        """
        Execute multiple Bitrix24 batch requests.

        Args:
            methods: Methods to execute as mapping or sequence of request tuples.
            halt: Whether to stop execution after the first failed command.
            timeout: Optional request timeout.
            prefer_version: Preferred Bitrix24 API version.

        Returns:
            Combined batch responses as a JSON-compatible dictionary.
        """

    def call_list(
        self,
        api_method: Text,
        params: Optional[JSONDict] = None,
        limit: Optional[int] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> ListResponseData:
        """
        Load a paginated Bitrix24 REST API list.

        Args:
            api_method: Bitrix24 REST API list method name.
            params: Optional request parameters.
            limit: Optional maximum number of items to load.
            timeout: Optional request timeout.
            prefer_version: Preferred Bitrix24 API version.

        Returns:
            Loaded list response as a JSON-compatible dictionary.
        """

    def call_list_fast(
        self,
        api_method: Text,
        params: Optional[JSONDict] = None,
        descending: bool = False,
        limit: Optional[int] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> ListFastResponseData:
        """
        Load a Bitrix24 REST API list using optimized pagination.

        Args:
            api_method: Bitrix24 REST API list method name.
            params: Optional request parameters.
            descending: Whether to load items in descending order.
            limit: Optional maximum number of items to load.
            timeout: Optional request timeout.
            prefer_version: Preferred Bitrix24 API version.

        Returns:
            Loaded list response as a JSON-compatible dictionary.
        """
