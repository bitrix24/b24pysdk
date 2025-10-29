from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Text

from ..._constants import PYTHON_VERSION as _PV
from ...constants import B24AppStatus
from ...utils.types import JSONDict
from .bitrix_api_time_response import BitrixAPITimeResponse

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class B24AppInfoInstallResult:
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
    def from_dict(cls, json_response: JSONDict) -> "B24AppInfoInstallResult":
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

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class B24AppInfoResult:
    """"""

    client_id: Text
    scope: List[Text]
    expires: datetime
    install: B24AppInfoInstallResult
    user_id: int

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "B24AppInfoResult":
        return cls(
            client_id=json_response["client_id"],
            scope=json_response["scope"].split(","),
            expires=datetime.fromisoformat(json_response["expires"]),
            install=B24AppInfoInstallResult.from_dict(json_response["install"]),
            user_id=int(json_response["user_id"]),
        )

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass(**_DATACLASS_KWARGS)
class BitrixAppInfoResponse:
    """"""

    result: B24AppInfoResult
    time: BitrixAPITimeResponse

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAppInfoResponse":
        return cls(
            result=B24AppInfoResult.from_dict(json_response["result"]),
            time=BitrixAPITimeResponse.from_dict(json_response["time"]),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
