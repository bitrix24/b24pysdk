from typing import Callable, Generic, Optional, Text, Union

from ...utils.type_vars import BAResultT, BValueT

__all__ = [
    "BitrixResultAdapter",
]


class BitrixResultAdapter(Generic[BAResultT, BValueT]):
    """Adapter unwrapping a Bitrix24 result before optional value conversion."""

    __slots__ = ("_result_adapter", "_wrapper")

    _result_adapter: Optional[Callable[[BAResultT], BValueT]]
    _wrapper: Optional[Text]

    def __init__(
            self,
            result_adapter: Optional[Callable[[BAResultT], BValueT]] = None,
            *,
            wrapper: Optional[Text] = None,
    ):
        self._result_adapter = result_adapter
        self._wrapper = wrapper

    def __call__(self, bitrix_result: BAResultT, /) -> Union[BAResultT, BValueT]:
        """Unwrap and optionally convert a Bitrix24 result."""

        if self._wrapper is not None:
            bitrix_result = self._unwrap_result(bitrix_result)

        if self._result_adapter is None:
            return bitrix_result

        return self._result_adapter(bitrix_result)

    def _unwrap_result(self, bitrix_result: BAResultT, /) -> BAResultT:
        """Extract value stored under the configured wrapper key."""

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                "Expected wrapped Bitrix24 result to be a dict, "
                f"got {type(bitrix_result).__name__}.",
            )

        if self._wrapper not in bitrix_result:
            raise TypeError(f"Expected wrapper {self._wrapper!r} in Bitrix24 result.")

        return bitrix_result[self._wrapper]
