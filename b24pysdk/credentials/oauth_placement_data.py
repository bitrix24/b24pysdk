import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, Mapping, Optional, Text

from .._constants import PYTHON_VERSION
from ..constants import B24AppStatus, Protocol
from ..error import BitrixValidationError
from ..utils.types import JSONDict
from .oauth_token import OAuthToken

if TYPE_CHECKING:
    from ..api.responses import B24AppInfoResult

__all__ = [
    "OAuthPlacementData",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthPlacementData:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    oauth_token: OAuthToken
    domain: Text
    protocol: Protocol
    lang: Text
    app_sid: Text
    member_id: Text
    status: B24AppStatus
    placement: Optional[Text] = None
    placement_options: Optional[JSONDict] = None

    @classmethod
    def from_dict(cls, payload: Mapping[Text, Any], /) -> "OAuthPlacementData":
        try:
            oauth_token = OAuthToken.from_placement_data(payload)

            domain = payload["DOMAIN"]
            protocol = Protocol(int(payload["PROTOCOL"]))
            lang = payload["LANG"]
            app_sid = payload["APP_SID"]
            member_id = payload["member_id"]
            status = B24AppStatus(payload["status"])
            placement = payload.get("PLACEMENT")
            placement_options = payload.get("PLACEMENT_OPTIONS")

            if placement_options and isinstance(placement_options, str):
                placement_options = json.loads(placement_options)

            return cls(
                oauth_token=oauth_token,
                domain=domain,
                protocol=protocol,
                lang=lang,
                app_sid=app_sid,
                member_id=member_id,
                status=status,
                placement=placement,
                placement_options=placement_options,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in placement data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid placement data: {error}") from error

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """"""
        if all((
                self.member_id == app_info.install.member_id,
                self.domain == app_info.install.domain,
        )):
            return True
        else:
            raise self.ValidationError("Invalid placement data")

    def to_dict(self) -> JSONDict:
        """"""
        return asdict(self)
