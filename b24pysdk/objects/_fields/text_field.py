import re
from typing import TYPE_CHECKING, ClassVar, List, Optional, Pattern, Text, Type, Union

from ...utils.converters import text_from_bitrix, text_to_bitrix
from .base_field import BaseField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "TextField",
    "URLField",
]


class TextField(BaseField[Text, Text]):
    """Field that exposes a Bitrix24 text value as ``str``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["TextField", Optional[Text], List[Text]]: ...

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[Text]:
        """Convert a single raw Bitrix24 text value to ``str``."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return text_from_bitrix(value, is_required=True)

        return text_from_bitrix(value, is_required=False)

    def _convert_to_bitrix(self, value: Optional[Text]) -> Optional[Text]:
        """Convert a single Python ``str`` value to a Bitrix24 text value."""

        if self.is_required:
            if value is None:
                raise ValueError(f"Field {self.attr_name!r} is required.")

            return text_to_bitrix(value, is_required=True)

        return text_to_bitrix(value, is_required=False)


class URLField(TextField):
    """Text field that accepts HTTP and HTTPS URLs only."""

    _URL_PATTERN: ClassVar[Pattern[Text]] = re.compile(
        r"https?://[^\r\n<>\"']+",
        flags=re.IGNORECASE,
    )

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["URLField", Optional[Text], List[Text]]: ...

    @classmethod
    def _validate_url(cls, value: Text) -> Text:
        """Validate and return an HTTP or HTTPS URL."""

        if cls._URL_PATTERN.fullmatch(value) is None:
            raise ValueError(f"Invalid HTTP or HTTPS URL: {value!r}.")

        return value

    def _convert_from_bitrix(self, value: Optional[Text]) -> Optional[Text]:
        """Convert and validate a single raw Bitrix24 URL value."""

        converted_value = super()._convert_from_bitrix(value)

        if converted_value is None:
            return None

        return self._validate_url(converted_value)

    def _convert_to_bitrix(self, value: Optional[Text]) -> Optional[Text]:
        """Validate and convert a single Python URL value."""

        converted_value = super()._convert_to_bitrix(value)

        if converted_value is None:
            return None

        return self._validate_url(converted_value)
