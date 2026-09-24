from typing import TYPE_CHECKING, List, Mapping, Optional, Text, Type, Union

from ...utils.types import JSONDict
from .text_field import TextField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "HTMLField",
]


class HTMLField(TextField):
    """Field that exposes a Bitrix24 HTML value as ``str``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["HTMLField", Optional[Text], List[Text]]: ...

    def _convert_from_bitrix(self, value: Optional[Union[JSONDict, Text]]) -> Optional[Text]:
        """Extract text from a raw Bitrix24 HTML value."""

        if isinstance(value, Mapping):
            value = value.get("TEXT")

        return super()._convert_from_bitrix(value)
