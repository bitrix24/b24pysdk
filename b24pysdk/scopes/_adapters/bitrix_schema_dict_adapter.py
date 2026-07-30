from typing import Dict, Generic, Optional, Text, Type, Union

from ...utils.type_vars import BSDataT, BSDictT

__all__ = [
    "BitrixSchemaDictAdapter",
]


class BitrixSchemaDictAdapter(Generic[BSDataT, BSDictT]):
    """Adapter converting Bitrix24 dictionary results to schema dictionaries."""

    __slots__ = ("_schema_dict_class", "_wrapper")

    _schema_dict_class: Type[BSDictT]
    _wrapper: Optional[Text]

    def __init__(self, schema_dict_class: Type[BSDictT], *, wrapper: Optional[Text] = None):
        self._schema_dict_class = schema_dict_class
        self._wrapper = wrapper

    def __call__(
            self,
            bitrix_result: Union[
                Dict[Text, BSDataT],
                Dict[Text, Dict[Text, BSDataT]],
            ],
            /,
    ) -> BSDictT:
        """Convert a Bitrix24 mapping result to a schema dictionary."""

        if self._wrapper is not None:
            bitrix_result = self._unwrap_result(bitrix_result)

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                f"Expected Bitrix24 result to be a dict, got {type(bitrix_result).__name__}.",
            )

        return self._schema_dict_class.from_bitrix(bitrix_result)

    def _unwrap_result(self, bitrix_result: Dict[Text, Dict[Text, BSDataT]], /) -> Dict[Text, BSDataT]:
        """Extract dictionary result stored under the configured wrapper key."""

        if not isinstance(bitrix_result, dict):
            raise TypeError(
                "Expected wrapped Bitrix24 result to be a dict, "
                f"got {type(bitrix_result).__name__}.",
            )

        if self._wrapper not in bitrix_result:
            raise TypeError(f"Expected wrapper {self._wrapper!r} in Bitrix24 result.")

        return bitrix_result[self._wrapper]
