from dataclasses import dataclass
from typing import Any, List, Optional, Text, TypedDict

from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import Self
from ._base_file_schema import BaseFileSchema

__all__ = [
    "BitrixFileResponseData",
    "URLFile",
]


class BitrixFileResponseData(TypedDict):
    """Data returned by a successful Bitrix24 file download."""
    content: bytes
    name: Optional[Text]


@dataclass(**frozen_dataclass_kwargs())
class URLFile(BaseFileSchema):
    """File read from Bitrix24 as a URL and written as ``[name, Base64]``.

    Remote content is downloaded lazily and cached by ``BaseFileSchema``. Local
    content can be created with its ``from_bytes()``, ``from_base64()``,
    ``from_file()`` and ``from_path()`` constructors.
    """

    url: Optional[Text] = None

    @classmethod
    def from_bitrix(cls, bitrix_data: Text, /, **_context: Any) -> Self:
        """Create a remote file from a URL returned by Bitrix24."""

        if not isinstance(bitrix_data, str):
            raise TypeError(f"Bitrix24 file value must be a string URL, got {type(bitrix_data).__name__}.")

        if not bitrix_data:
            raise ValueError("Bitrix24 file URL must be a non-empty string.")

        return cls(url=bitrix_data)

    def to_bitrix(self) -> List[Text]:
        """Convert this file to the ``[name, Base64]`` upload representation."""

        if self.is_local and self.name is None:
            raise ValueError("A local URL file requires a file name.")

        content = self.to_base64()

        if self.name is None:
            raise ValueError("File name is unavailable after downloading the file.")

        return [self.name, content]

    @property
    def download_url(self) -> Text:
        """Return the URL used to download this remote file."""

        if self.url is None:
            raise ValueError("Local URL file has no download URL.")

        return self.url
