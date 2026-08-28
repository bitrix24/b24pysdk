from dataclasses import dataclass
from typing import Any, List, Optional, Text

from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_file_schema import BaseFileSchema

__all__ = [
    "UserFile",
]


@dataclass(**frozen_dataclass_kwargs())
class UserFile(BaseFileSchema):
    """File stored in a standard Bitrix24 user file field.

    A remote file is read from Bitrix24 as a direct URL, for example from
    ``PERSONAL_PHOTO``. Both remote and local files are serialized as the
    ``[name, Base64]`` pair expected by user file fields such as
    ``PERSONAL_PHOTO``. Remote content is downloaded lazily when conversion is
    required.

    The remote file name is populated from the download response when Bitrix24
    provides it in ``Content-Disposition``.
    """

    url: Optional[Text] = None

    @classmethod
    def from_bitrix(cls, bitrix_data: Text, /, **_context: Any) -> "UserFile":
        """Create a remote user file from a URL returned by Bitrix24."""

        if not isinstance(bitrix_data, str):
            raise TypeError(
                "Bitrix24 user file value must be a string URL, "
                f"got {type(bitrix_data).__name__}.",
            )

        if not bitrix_data:
            raise ValueError("Bitrix24 user file URL must be a non-empty string.")

        return cls(url=bitrix_data)

    def to_bitrix(self) -> List[Text]:
        """Convert this user file to the Bitrix24 write representation.

        Remote files are downloaded when necessary and serialized as a new
        ``[name, Base64]`` upload value. Downloaded content is reused from the
        file cache on subsequent conversions.
        """

        if self.is_local and self.name is None:
            raise ValueError("A local user file requires a file name.")

        content = self.to_base64()

        if self.name is None:
            raise ValueError("User file name is unavailable after downloading the file.")

        return [
            self.name,
            content,
        ]

    @property
    def download_url(self) -> Text:
        """Return the absolute URL used to download this user file."""

        if self.url is None:
            raise ValueError("Local user file has no download URL.")

        return self.url
