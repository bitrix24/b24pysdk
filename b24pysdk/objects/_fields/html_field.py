from typing import TYPE_CHECKING, List, Mapping, Optional, Text, Type, Union

from ...utils.types import JSONDict
from .text_field import TextField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "HTMLField",
]


class HTMLField(TextField):
    """Read HTML response envelopes as text and serialize writes as text.

    A mapping such as ``{"TYPE": "HTML", "TEXT": "<b>Title</b>"}`` contributes
    only its ``TEXT`` value; ``TYPE`` is not validated or retained. Plain text
    responses are accepted too. Outgoing conversion is inherited from
    ``TextField`` and does not recreate the response envelope.
    """

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
