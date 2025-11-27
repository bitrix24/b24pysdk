from typing import Mapping, Optional, Protocol, Sequence, Text, overload

from ...utils.types import B24BatchMethods, B24BatchMethodTuple, JSONDict, Key, Timeout


class BitrixTokenProtocol(Protocol):
    """"""

    domain: Text

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> JSONDict: ...


class BitrixTokenFullProtocol(BitrixTokenProtocol, Protocol):
    """"""

    @overload
    def call_batch(
            self,
            methods: Mapping[Key, B24BatchMethodTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    @overload
    def call_batch(
            self,
            methods: Sequence[B24BatchMethodTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    def call_batch(
            self,
            methods: B24BatchMethods,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Mapping[Key, B24BatchMethodTuple],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Sequence[B24BatchMethodTuple],
            halt: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    def call_batches(
            self,
            methods: B24BatchMethods,
            halt: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    def call_list(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> JSONDict: ...

    def call_list_fast(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            descending: bool = False,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> JSONDict: ...
