from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Text

from ...constants import B24AppStatus
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict
from .abstract_bitrix_response import AbstractBitrixResponse

__all__ = [
    "B24AppInfoInstall",
    "B24AppInfoResult",
    "BitrixAppInfoResponse",
]


@dataclass(**frozen_dataclass_kwargs(eq=False))
class B24AppInfoInstall:
    """
    Bitrix24 application installation metadata.

    Describes the current application installation on a portal, including
    installation status, portal identifiers, granted scopes, and endpoint URLs.
    """

    installed: bool
    version: int
    status: B24AppStatus
    scope: List[Text]
    domain: Text
    uri: Text
    client_endpoint: Text
    member_id: Text
    member_type: Text

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "B24AppInfoInstall":
        """
        Create a B24AppInfoInstall instance from raw install data.

        Args:
            json_response: Raw ``install`` section from ``app.info`` response.

        Returns:
            Parsed application installation metadata.
        """
        return cls(
            installed=json_response["installed"],
            version=int(json_response["version"]),
            status=B24AppStatus(json_response["status"]),
            scope=json_response["scope"].split(","),
            domain=json_response["domain"],
            uri=json_response["uri"],
            client_endpoint=json_response["client_endpoint"],
            member_id=json_response["member_id"],
            member_type=json_response["member_type"],
        )

    def to_dict(self) -> JSONDict:
        """
        Convert installation metadata to dictionary.

        Returns:
            Dictionary representation of the installation metadata.
        """
        return asdict(self)


@dataclass(**frozen_dataclass_kwargs(eq=False))
class B24AppInfoResult:
    """
    Parsed result of the Bitrix24 ``app.info`` method.

    Contains OAuth application metadata, granted scopes, token expiration
    timestamp, installation information, and current user identifier.
    """

    client_id: Text
    scope: List[Text]
    expires: datetime
    install: B24AppInfoInstall
    user_id: int

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "B24AppInfoResult":
        """
        Create a B24AppInfoResult instance from raw ``app.info`` result data.

        Args:
            json_response: Raw ``result`` section from ``app.info`` response.

        Returns:
            Parsed application info result.
        """
        return cls(
            client_id=json_response["client_id"],
            scope=json_response["scope"].split(","),
            expires=datetime.fromisoformat(json_response["expires"]),
            install=B24AppInfoInstall.from_dict(json_response["install"]),
            user_id=int(json_response["user_id"]),
        )

    def to_dict(self) -> JSONDict:
        """
        Convert application info result to dictionary.

        Returns:
            Dictionary representation of the application info result.
        """
        return asdict(self)


@dataclass(**frozen_dataclass_kwargs(eq=False))
class BitrixAppInfoResponse(AbstractBitrixResponse[B24AppInfoResult]):
    """
    Typed response for the Bitrix24 ``app.info`` method.

    Stores parsed application information in ``result`` and Bitrix24 timing
    metadata in ``time``.
    """

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAppInfoResponse":
        """
        Create a BitrixAppInfoResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by ``app.info``.

        Returns:
            Parsed ``app.info`` response.
        """
        return cls(
            result=B24AppInfoResult.from_dict(json_response["result"]),
            time=cls._convert_time(json_response["time"]),
        )
