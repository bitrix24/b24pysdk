from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Text

from ..._constants import PYTHON_VERSION
from ...constants import B24AppStatus
from ...utils.types import JSONDict
from .abstract_bitrix_response import AbstractBitrixResponse

__all__ = [
    "B24AppInfoInstall",
    "B24AppInfoResult",
    "BitrixAppInfoResponse",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class B24AppInfoInstall:
    """"""

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
    def from_dict(cls, json_response: JSONDict) -> "B24AppInfoInstall":
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
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class B24AppInfoResult:
    """"""

    client_id: Text
    scope: List[Text]
    expires: datetime
    install: B24AppInfoInstall
    user_id: int

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "B24AppInfoResult":
        return cls(
            client_id=json_response["client_id"],
            scope=json_response["scope"].split(","),
            expires=datetime.fromisoformat(json_response["expires"]),
            install=B24AppInfoInstall.from_dict(json_response["install"]),
            user_id=int(json_response["user_id"]),
        )

    def to_dict(self) -> JSONDict:
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class BitrixAppInfoResponse(AbstractBitrixResponse[B24AppInfoResult]):
    """"""

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAppInfoResponse":
        return cls(
            result=B24AppInfoResult.from_dict(json_response["result"]),
            time=cls._convert_time(json_response["time"]),
        )
