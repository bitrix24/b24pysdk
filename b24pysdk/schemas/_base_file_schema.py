import base64
import binascii
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Optional, Text, Union

from ..api.requesters import BitrixFileRequester
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import Self, Timeout
from ._base_schema import BaseSchema
from .file import BitrixFileResponseData

__all__ = [
    "BaseFileSchema",
]


@dataclass(**frozen_dataclass_kwargs())
class BaseFileSchema(BaseSchema[Any], ABC):
    """Base schema for file values.

    A concrete file schema can represent either remote content or local content
    prepared for a later write request. Remote files are downloaded through
    ``BitrixFileRequester`` using the URL supplied by the concrete file type.
    Downloaded content is cached as immutable ``bytes`` so repeated reads do not
    issue additional requests. If the response contains a file name in
    ``Content-Disposition``, it is stored when the file is first downloaded.
    Local constructors normalize their input to immutable ``bytes`` immediately.

    File read and write representations can differ between Bitrix24 entities.
    Subclasses therefore implement ``from_bitrix()``, ``to_bitrix()`` and the
    ``download_url`` property. ``from_bitrix()`` may additionally use context
    supplied by the owning field, for example a Bitrix24 portal domain.
    """

    _download_cache: Optional[bytes] = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )
    _local_content: Optional[bytes] = field(
        default=None,
        init=False,
        repr=False,
    )
    _name: Optional[Text] = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )

    @classmethod
    @abstractmethod
    def from_bitrix(cls, bitrix_data: Any, /, **context: Any) -> Self:
        """Create a remote file schema from Bitrix24 data and optional context."""
        raise NotImplementedError

    @classmethod
    def from_bytes(
            cls,
            content: bytes,
            *,
            name: Optional[Text] = None,
    ) -> Self:
        """Create a local file from immutable bytes."""

        if not isinstance(content, bytes):
            raise TypeError(f"File content must be bytes, got {type(content).__name__}.")

        return cls()._set_local_content(content, name=name)

    @classmethod
    def from_base64(
            cls,
            content: Union[Text, bytes],
            *,
            name: Optional[Text] = None,
    ) -> Self:
        """Create a local file from Base64-encoded content."""

        if not isinstance(content, (str, bytes)):
            raise TypeError(
                "Base64 file content must be str or bytes, "
                f"got {type(content).__name__}.",
            )

        try:
            decoded_content = base64.b64decode(content, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Invalid Base64 file content.") from error

        return cls.from_bytes(decoded_content, name=name)

    @classmethod
    def from_file(
            cls,
            file: BinaryIO,
            *,
            name: Optional[Text] = None,
    ) -> Self:
        """Create a local file from a binary file-like object.

        The object is read from its current position and is not closed. If
        ``name`` is omitted, a path-like ``file.name`` attribute is used when
        available.
        """

        read = getattr(file, "read", None)

        if not callable(read):
            raise TypeError("file must be a readable binary file-like object.")

        content = read()

        if not isinstance(content, bytes):
            raise TypeError(
                "Binary file-like object read() must return bytes, "
                f"got {type(content).__name__}.",
            )

        if name is None:
            file_name = getattr(file, "name", None)

            if isinstance(file_name, (str, os.PathLike)):
                name = Path(file_name).name

        return cls.from_bytes(content, name=name)

    @classmethod
    def from_path(
            cls,
            path: Union[Text, os.PathLike],
            *,
            name: Optional[Text] = None,
    ) -> Self:
        """Create a local file from a filesystem path."""

        file_path = Path(path)

        return cls.from_bytes(
            file_path.read_bytes(),
            name=file_path.name if name is None else name,
        )

    def _set_name(self, name: Optional[Text], /) -> Self:
        """Store an optional file name without changing the file identity."""

        if name is not None and (not isinstance(name, str) or not name):
            raise ValueError("File name must be a non-empty string or None.")

        object.__setattr__(self, "_name", name)
        return self

    def _set_local_content(self, content: bytes, *, name: Optional[Text]) -> Self:
        """Store local file content and its optional name."""

        object.__setattr__(self, "_local_content", content)
        self._set_name(name)

        return self

    def _set_downloaded_content(
            self,
            content: bytes,
            *,
            name: Optional[Text],
    ) -> Self:
        """Cache downloaded file content and its name when available."""

        object.__setattr__(self, "_download_cache", content)

        if self._name is None and name is not None:
            self._set_name(name)

        return self

    @property
    def name(self) -> Optional[Text]:
        """Return the file name, downloading remote content when necessary."""

        if self._name is None and not self.is_local:
            self.read()

        return self._name

    @property
    def extension(self) -> Optional[Text]:
        """Return the final file-name suffix, downloading when necessary."""

        name = self.name

        if name is None:
            return None

        return Path(name).suffix or None

    @property
    def is_local(self) -> bool:
        """Return whether this file was created from local content."""
        return self._local_content is not None

    @property
    @abstractmethod
    def download_url(self) -> Text:
        """Return the absolute URL used to download the remote file."""
        raise NotImplementedError

    def _download(self, *, timeout: Timeout = None) -> BitrixFileResponseData:
        """Download remote file data without consulting the content cache."""
        return BitrixFileRequester(
            url=self.download_url,
            timeout=timeout,
        ).call()

    def read(self, *, timeout: Timeout = None) -> bytes:
        """Return file content as bytes, downloading it at most once."""

        if self._local_content is not None:
            return self._local_content

        content = self._download_cache

        if content is None:
            response = self._download(timeout=timeout)
            content = response["content"]

            self._set_downloaded_content(
                content,
                name=response["name"],
            )

        return content

    def download(self, *, timeout: Timeout = None) -> bytes:
        """Return file content as bytes using the same cache as ``read()``."""
        return self.read(timeout=timeout)

    def open(self, *, timeout: Timeout = None) -> BytesIO:
        """Return an independent in-memory binary stream for the file content."""
        return BytesIO(self.read(timeout=timeout))

    def to_base64(self, *, timeout: Timeout = None) -> Text:
        """Return file content encoded as an ASCII Base64 string."""
        return base64.b64encode(self.read(timeout=timeout)).decode("ascii")

    def save_to(
            self,
            path: Union[Text, os.PathLike],
            *,
            timeout: Timeout = None,
    ) -> Path:
        """Write file content to ``path`` and return the resulting path."""

        file_path = Path(path)
        file_path.write_bytes(self.read(timeout=timeout))

        return file_path
