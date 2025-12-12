from dataclasses import asdict, dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Text

from ..._config import Config
from ..._constants import PYTHON_VERSION as _PV
from ...error import BitrixValidationError
from ...utils.types import JSONDict
from ._utils import parse_flattened_keys
from .renewed_oauth_token import RenewedOAuthToken

if TYPE_CHECKING:
    from ..responses import B24AppInfoResult

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class OAuthEventData:
    """"""

    class ValidationError(BitrixValidationError):
        """"""

    event: Text
    event_handler_id: int
    ts: datetime
    auth: RenewedOAuthToken
    data: Optional[JSONDict] = None

    @classmethod
    def from_dict(cls, event_data: Mapping[Text, Any]) -> "OAuthEventData":
        try:
            parsed_event_data = parse_flattened_keys(event_data)

            event = parsed_event_data["event"]
            event_handler_id = int(parsed_event_data["event_handler_id"])
            ts = datetime.fromtimestamp(int(parsed_event_data["ts"]), tz=Config().tz)
            auth = RenewedOAuthToken.from_dict(parsed_event_data["auth"])
            data = parsed_event_data.get("data")

            return cls(
                event=event,
                event_handler_id=event_handler_id,
                ts=ts,
                auth=auth,
                data=data,
            )

        except KeyError as error:
            raise cls.ValidationError(f"Missing required field in event data: {error.args[0]}") from error

        except Exception as error:
            raise cls.ValidationError(f"Invalid event data: {error}") from error

    def to_dict(self) -> Dict:
        return asdict(self)

    def validate_against_app_info(self, app_info: "B24AppInfoResult") -> bool:
        """"""
        try:
            return self.auth.validate_against_app_info(app_info)
        except self.auth.ValidationError as error:
            raise self.ValidationError("Invalid oauth event data") from error
