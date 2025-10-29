import json
from dataclasses import asdict, dataclass
from typing import Dict, Literal, Optional, Text, cast

from ..._constants import PYTHON_VERSION as _PV
from ...constants import B24AppStatus
from ...error import BitrixValidationError
from ...utils.types import JSONDict
from .oauth_token import OAuthToken

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthPlacementData:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    oauth_token: OAuthToken
    domain: Text
    protocol: Literal[0, 1]
    lang: Text
    app_sid: Text
    member_id: Text
    status: B24AppStatus
    placement: Optional[Text]
    placement_options: Optional[JSONDict]

    @classmethod
    def from_dict(cls, placement_data: JSONDict) -> "OAuthPlacementData":
        try:
            oauth_token = OAuthToken.from_placement_data(placement_data)

            domain = placement_data["DOMAIN"]
            protocol = int(placement_data["PROTOCOL"])
            lang = placement_data["LANG"]
            app_sid = placement_data["APP_SID"]
            member_id = placement_data["member_id"]
            status = B24AppStatus(placement_data["status"])
            placement = placement_data.get("PLACEMENT")
            placement_options = placement_data.get("PLACEMENT_OPTIONS")

            if placement_options and isinstance(placement_options, str):
                placement_options = json.loads(placement_options)

            return cls(
                oauth_token=oauth_token,
                domain=domain,
                protocol=cast(Literal[0, 1], protocol),
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

    def to_dict(self) -> Dict:
        return asdict(self)
