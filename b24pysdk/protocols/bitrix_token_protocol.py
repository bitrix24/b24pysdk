from typing import Mapping, Optional, Protocol, Sequence, Text, overload

from ..constants.version import B24APIVersion
from ..utils.types import B24APIVersionLiteral, B24Requests, B24RequestTuple, JSONDict, Key, Timeout


class BitrixTokenProtocol(Protocol):

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...


class BitrixTokenFullProtocol(BitrixTokenProtocol, Protocol):

    @overload
    def call_batch(
            self,
            methods: Mapping[Key, B24RequestTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    @overload
    def call_batch(
            self,
            methods: Sequence[B24RequestTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    def call_batch(
            self,
            methods: B24Requests,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Mapping[Key, B24RequestTuple],
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Sequence[B24RequestTuple],
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    def call_batches(
            self,
            methods: B24Requests,
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    def call_list(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...

    def call_list_fast(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            descending: bool = False,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            prefer_version: B24APIVersionLiteral = B24APIVersion.V2,
    ) -> JSONDict: ...
